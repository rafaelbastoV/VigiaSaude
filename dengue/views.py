from django.shortcuts import render

from django.http import JsonResponse
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from dengue.models import DadosDengueEstado, ControleAtualizacao

def index(request):
    return render(request, 'home.html')

def estatisticas_estados(request, ano):

    dados = (
        DadosDengueEstado.objects
        .filter(ano=ano)
        .values('uf')
        .annotate(
            masculino=Sum('casos_masculino'),
            feminino=Sum('casos_feminino'),
            hospitalizados=Sum('casos_hospitalizados'),

            faixa_0_18=Sum('faixa_0_18'),
            faixa_19_35=Sum('faixa_19_35'),
            faixa_36_50=Sum('faixa_36_50'),
            faixa_51_65=Sum('faixa_51_65'),
            faixa_65_mais=Sum('faixa_65_mais'),
        )
        .annotate(
            total=F('masculino') + F('feminino')
        )
        .order_by('-total')
    )

    resultado = []

    for estado in dados:
        total = estado["total"] or 1  # evita divisão por zero

        nao_hospitalizados = total - estado["hospitalizados"]

        resultado.append({
            "uf": estado["uf"],
            "total": total,

            "sexo": {
                "masculino": estado["masculino"],
                "feminino": estado["feminino"],
                "percentual_masculino": round((estado["masculino"] / total) * 100, 2),
                "percentual_feminino": round((estado["feminino"] / total) * 100, 2),
            },

            "hospitalizacao": {
                "hospitalizados": estado["hospitalizados"],
                "nao_hospitalizados": nao_hospitalizados,
                "percentual_hospitalizados": round((estado["hospitalizados"] / total) * 100, 2),
                "percentual_nao_hospitalizados": round((nao_hospitalizados / total) * 100, 2),
            },

            "faixa_etaria": {
                "0_18": {
                    "quantidade": estado["faixa_0_18"],
                    "percentual": round((estado["faixa_0_18"] / total) * 100, 2),
                },
                "19_35": {
                    "quantidade": estado["faixa_19_35"],
                    "percentual": round((estado["faixa_19_35"] / total) * 100, 2),
                },
                "36_50": {
                    "quantidade": estado["faixa_36_50"],
                    "percentual": round((estado["faixa_36_50"] / total) * 100, 2),
                },
                "51_65": {
                    "quantidade": estado["faixa_51_65"],
                    "percentual": round((estado["faixa_51_65"] / total) * 100, 2),
                },
                "65_mais": {
                    "quantidade": estado["faixa_65_mais"],
                    "percentual": round((estado["faixa_65_mais"] / total) * 100, 2),
                },
            }
        })

    return JsonResponse(resultado, safe=False)

def ultima_atualizacao(request):
    try:
        controle = ControleAtualizacao.objects.get(nome_arquivo="dengue_2026")

        print(controle.ultima_atualizacao)

        return JsonResponse({
            "ultima_atualizacao": controle.ultima_atualizacao
        })

    except ControleAtualizacao.DoesNotExist:
        return JsonResponse({
            "ultima_atualizacao": None
        })