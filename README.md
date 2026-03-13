# VigiaSaúde

VigiaSaúde é uma plataforma web para **monitoramento e visualização de dados epidemiológicos**, com foco inicial na **dengue**. O sistema coleta dados automaticamente através de um processo de ingestão periódica e os disponibiliza em uma interface web para consulta e análise.

O objetivo do projeto é demonstrar uma arquitetura completa de aplicação web em produção, incluindo **coleta automatizada de dados, armazenamento em banco relacional, interface administrativa e deploy em servidor Linux**.

---

# Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

* **Python 3**
* **Django** – framework web principal
* **MariaDB / MySQL** – banco de dados relacional
* **Docker** – containerização do banco de dados
* **Gunicorn** – servidor WSGI para aplicações Python
* **Nginx** – servidor web e proxy reverso
* **Certbot** – geração automática de certificados HTTPS
* **Cron** – execução automática de tarefas agendadas

---

# Funcionalidades

* Importação automatizada de dados de dengue
* Armazenamento estruturado em banco de dados relacional
* Painel administrativo para gerenciamento dos dados
* API backend para consumo de informações
* Execução diária de tarefas de coleta de dados
* Deploy configurado com HTTPS em ambiente Linux

---

# Arquitetura da Aplicação

A aplicação segue uma arquitetura comum para aplicações Django em produção:

Nginx → Gunicorn → Django → MariaDB

Nginx atua como proxy reverso, encaminhando requisições HTTP/HTTPS para o Gunicorn, que executa a aplicação Django. O banco de dados MariaDB roda em um container Docker.

---

# Estrutura do Projeto

```
vigiasaude/
│
├── manage.py
├── vigiasaude/          # Configuração principal do Django
├── apps/                # Aplicações Django
├── static/              # Arquivos estáticos
├── media/               # Arquivos enviados por usuários
├── venv/                # Ambiente virtual Python
└── .env                 # Variáveis de ambiente
```

---

# Configuração do Ambiente

Clone o repositório:

```
git clone https://github.com/seuusuario/vigiasaude.git
cd vigiasaude
```

Crie o ambiente virtual:

```
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências:

```
pip install -r requirements.txt
```

---

# Variáveis de Ambiente

Crie um arquivo `.env` contendo as configurações do banco de dados:

```
DB_NAME=vigiasaude
DB_USER=usuario
DB_PASSWORD=senha
DB_HOST=127.0.0.1
DB_PORT=3306
```

---

# Migrações do Banco de Dados

Execute as migrações:

```
python manage.py migrate
```

Crie um usuário administrador:

```
python manage.py createsuperuser
```

---

# Execução Local

Para rodar o servidor de desenvolvimento:

```
python manage.py runserver
```

Acesse:

```
http://127.0.0.1:8000
```

Painel administrativo:

```
http://127.0.0.1:8000/admin
```

---

# Importação Automática de Dados

O projeto possui um comando customizado responsável por importar dados epidemiológicos:

```
python manage.py importar_dengue
```

Esse comando pode ser executado manualmente ou agendado para execução automática.

---

# Agendamento Automático

Para executar a importação diariamente foi configurado um cronjob:

```
0 2 * * * cd /root/vigiasaude/vigiasaude && /root/vigiasaude/vigiasaude/venv/bin/python manage.py importar_dengue
```

Isso executa o processo **todos os dias às 02:00 da manhã**.

---

# Deploy em Produção

O deploy foi realizado em um servidor Linux utilizando:

* Nginx como proxy reverso
* Gunicorn como servidor WSGI
* Certbot para configuração automática de HTTPS
* Docker para execução do banco MariaDB

Fluxo de requisição:

Cliente → Nginx → Gunicorn → Django → MariaDB

---

# Segurança

* HTTPS configurado via Certbot
* Proxy reverso com Nginx
* Separação de variáveis sensíveis via `.env`
* Banco de dados isolado em container Docker

---

# Possíveis Melhorias Futuras

* Dashboard interativo para visualização de dados
* API pública para consulta de estatísticas
* Visualização geográfica dos dados
* Integração com outras fontes epidemiológicas

---

# Licença

Este projeto foi desenvolvido para fins educacionais e de demonstração de arquitetura de aplicações web.
