# 🍊 NutriClinic - Sistema de Agendamento Nutricional

O **NutriClinic** é uma aplicação Fullstack desenvolvida para facilitar o agendamento de consultas entre Nutricionistas e Pacientes. Com uma interface amigável e um backend robusto, o sistema resolve problemas comuns de choque de horários, fusos horários e controle da agenda.

## 🚀 Funcionalidades

* **Autenticação Segura**: Login utilizando JWT (JSON Web Tokens).
* **Controle de Acesso (RBAC)**: Visões e permissões diferentes para perfis de PATIENT e NUTRITIONIST.
* **Painel do Paciente**:
  * Visualização da agenda completa do nutricionista.
  * Agendamento de consultas de 30 em 30 minutos.
  * Bloqueio automático de slots ocupados (em tempo real).
* **Painel do Nutricionista**:
  * Visão geral da agenda diária num prático grid 4x5.
  * Navegação entre diferentes dias da semana de forma simples.
  * Bloqueio manual de horários (para folgas, pausas, etc).
  * Gestão e cancelamento de consultas.
* **Resiliência de Fuso Horário**: Manipulação correta de timestamps (UTC e Local Time) para garantir precisão nas consultas.

## 🛠️ Tecnologias Utilizadas

**Backend:**
* [Python 3](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/) - Framework web rápido e moderno.
* [SQLAlchemy](https://www.sqlalchemy.org/) - ORM (Object Relational Mapper)
* [Alembic](https://alembic.sqlalchemy.org/) - Migrations de banco de dados
* [SQLite](https://www.sqlite.org/) - Banco de dados leve (pode ser substituído por PostgreSQL)
* [Pydantic](https://docs.pydantic.dev/) - Validação de dados

**Frontend:**
* HTML5, CSS3, JavaScript Vanilla
* Arquitetura SPA (Single Page Application) simples.
* Comunicação via REST API com Fetch API.
* Estilização minimalista e responsiva, com paleta em tons quentes (Pêssego e Laranja).

## ⚙️ Como Executar o Projeto Localmente

### 1. Clonar o Repositório
`ash
git clone https://github.com/seu-usuario/clinic-scheduler-api.git
cd clinic-scheduler-api
`

### 2. Rodar o Backend (API)
Crie um ambiente virtual e instale as dependências:
`ash
python -m venv .venv
# Ativar no Windows:
.\.venv\Scripts\activate
# Ativar no Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
`

Rode as migrações para criar as tabelas do banco de dados:
`ash
alembic upgrade head
`

Inicie o servidor local:
`ash
uvicorn app.main:app --reload
`
A API estará rodando em: http://localhost:8000

> 💡 **Dica:** O Swagger automático da API pode ser acessado em http://localhost:8000/docs

### 3. Rodar o Frontend
Em outro terminal (na raiz do projeto), levante um servidor HTTP simples na pasta rontend:
`ash
python -m http.server 5500 -d frontend
`
Acesse a aplicação no navegador através de: http://localhost:5500

---
*Desenvolvido como projeto de estudos e portfólio. Foco em arquitetura Backend e APIs.*