import requests
import pandas as pd
from datetime import datetime
from django.utils import timezone
from django.db.models import Max
from dengue.models import ControleAtualizacao, DadosDengueEstado
import zipfile
import io
from django.core.management.base import BaseCommand

URL = "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Dengue/csv/DENGBR26.csv.zip"

MAPEAMENTO_UF = {
    11: 'RO', 12: 'AC', 13: 'AM', 14: 'RR', 15: 'PA', 16: 'AP', 17: 'TO',
    21: 'MA', 22: 'PI', 23: 'CE', 24: 'RN', 25: 'PB', 26: 'PE', 27: 'AL',
    28: 'SE', 29: 'BA', 31: 'MG', 32: 'ES', 33: 'RJ', 35: 'SP', 41: 'PR',
    42: 'SC', 43: 'RS', 50: 'MS', 51: 'MT', 52: 'GO', 53: 'DF'
}

class Command(BaseCommand):
    help = "Importa dados da dengue direto da URL"

    def handle(self, *args, **options):

        self.stdout.write("[DEBUG] Baixando arquivo...")

        response = requests.get(URL)
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))

        nome_csv = [f for f in zip_file.namelist() if f.endswith('.csv')][0]

        cols = ['NU_ANO', 'SEM_NOT', 'SG_UF_NOT', 'CS_SEXO', 'NU_IDADE_N', 'HOSPITALIZ']

        with zip_file.open(nome_csv) as arquivo_csv:
            df = pd.read_csv(arquivo_csv, sep=',', usecols=cols, low_memory=False)

        self.stdout.write(self.style.SUCCESS("Arquivo carregado com sucesso!"))

        verificar_e_atualizar()

def verificar_e_atualizar():

    response = requests.get(URL)

    # Lê o ZIP em memória
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))

    # Pega o nome do primeiro arquivo dentro do ZIP
    nome_csv = zip_file.namelist()[0]

    # Abre o CSV dentro do ZIP
    with zip_file.open(nome_csv) as arquivo_csv:
        df = pd.read_csv(arquivo_csv, sep=',', low_memory=False)

    last_modified = response.headers.get("Last-Modified")

    if not last_modified:
        print("Não foi possível verificar atualização.")
        return

    data_site = datetime.strptime(
        last_modified,
        "%a, %d %b %Y %H:%M:%S %Z"
    )
    data_site = timezone.make_aware(data_site)

    controle, _ = ControleAtualizacao.objects.get_or_create(
        nome_arquivo="dengue_2026"
    )

    if controle.ultima_atualizacao and data_site <= controle.ultima_atualizacao:
        print("Banco já está atualizado.")
        return

    print("Arquivo atualizado! Processando direto da URL...")

    cols = ['NU_ANO', 'SEM_NOT', 'SG_UF_NOT', 'CS_SEXO', 'NU_IDADE_N', 'HOSPITALIZ']
    df = pd.read_csv(URL, sep=',', usecols=cols, low_memory=False)

    ultimo_registro = DadosDengueEstado.objects.aggregate(Max('semana'))
    ultima_semana = ultimo_registro['semana__max'] or 0

    df['semana_limpa'] = df['SEM_NOT'].apply(lambda x: int(str(x)[-2:]))

    df_filtrado = df[df['semana_limpa'] > ultima_semana].copy()

    if df_filtrado.empty:
        print("Nenhum dado novo encontrado.")
        return

    df_filtrado['SG_UF_NOT'] = pd.to_numeric(df_filtrado['SG_UF_NOT'], errors='coerce')
    df_filtrado['uf_sigla'] = df_filtrado['SG_UF_NOT'].map(MAPEAMENTO_UF)

    def extrair_idade(cod_idade):
        s = str(cod_idade)
        return int(s[1:]) if s.startswith('4') else 0

    df_filtrado['idade_real'] = df_filtrado['NU_IDADE_N'].apply(extrair_idade)

    def categorizar(idade):
        if idade <= 18: return 'f0_18'
        if idade <= 35: return 'f19_35'
        if idade <= 50: return 'f36_50'
        if idade <= 65: return 'f51_65'
        return 'f65'

    df_filtrado['categoria'] = df_filtrado['idade_real'].apply(categorizar)

    agregado = df_filtrado.groupby(
        ['NU_ANO', 'semana_limpa', 'uf_sigla']
    ).agg(
        masc=('CS_SEXO', lambda x: (x == 'M').sum()),
        fem=('CS_SEXO', lambda x: (x == 'F').sum()),
        hosp=('HOSPITALIZ', lambda x: (x == 1).sum()),
        f0_18=('categoria', lambda x: (x == 'f0_18').sum()),
        f19_35=('categoria', lambda x: (x == 'f19_35').sum()),
        f36_50=('categoria', lambda x: (x == 'f36_50').sum()),
        f51_65=('categoria', lambda x: (x == 'f51_65').sum()),
        f65=('categoria', lambda x: (x == 'f65').sum()),
    ).reset_index()

    print(f"Gravando {len(agregado)} novos registros...")

    for _, row in agregado.iterrows():
        DadosDengueEstado.objects.update_or_create(
            ano=row['NU_ANO'],
            semana=row['semana_limpa'],
            uf=row['uf_sigla'],
            defaults={
                'casos_masculino': row['masc'],
                'casos_feminino': row['fem'],
                'casos_hospitalizados': row['hosp'],
                'faixa_0_18': row['f0_18'],
                'faixa_19_35': row['f19_35'],
                'faixa_36_50': row['f36_50'],
                'faixa_51_65': row['f51_65'],
                'faixa_65_mais': row['f65'],
            }
        )

    controle.ultima_atualizacao = data_site
    controle.save()

    print("Sincronização finalizada com sucesso.")