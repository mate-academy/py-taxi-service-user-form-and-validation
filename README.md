<div align="center">

# 🚕 Taxi Service — Formulários de Usuário
### Validação e gestão de condutores em Django

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Study](https://img.shields.io/badge/Tipo-Projeto%20educacional-475569?style=for-the-badge)

</div>

## 🎯 Sobre o projeto

Implementação de estudo de **forms** e validações para registros de condutores em uma aplicação Django.

**Código relevante:** branch [`taxi-user-form-validation`](https://github.com/WalterMatheusgg/py-taxi-service-user-form-and-validation/tree/taxi-user-form-validation). Desenvolvido como parte de exercícios práticos com Django; não representa um sistema comercial de transporte.

## ✨ Funcionalidades e estrutura

| Área | Recurso presente na implementação |
|:--|:--|
| **Formulários** | Inclusão de `taxi/forms.py` para entrada e validação de dados. |
| **Condutores** | Views de cadastro, edição e detalhes de motoristas. |
| **Templates** | Telas de formulário e confirmação de remoção. |
| **Rotas** | Ampliação dos caminhos de navegação e operações. |

## 🏗️ Arquitetura

```mermaid
flowchart LR
A["Navegador"] --> B["Django URLs + Views"]
B --> C["Models e regras"]
C --> D[("SQLite")]
B --> E["Templates HTML"]
```

Organização principal da aplicação:

```text
taxi/             # Models, views, admin e rotas
taxi_service/     # Configuração Django
templates/        # Páginas HTML (quando aplicável)
manage.py         # Comandos do Django
```

## 🚀 Executar localmente

Use um ambiente Python isolado, com versão compatível com as dependências do projeto.

```bash
git clone -b taxi-user-form-validation https://github.com/WalterMatheusgg/py-taxi-service-user-form-and-validation.git
cd py-taxi-service-user-form-and-validation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py runserver
```

Acesse **http://127.0.0.1:8000/**.

Para testar funcionalidades existentes:

```bash
python manage.py test
```

**Observação:** não executei o projeto ou a suíte nesta revisão. Em algumas etapas, os testes são fornecidos como parte do enunciado do curso e podem exigir configuração adicional.

## 🔒 Limites e cuidados

A branch possui commits divergentes de `master`; confirme se deseja preservar alterações únicas da branch principal antes de excluí-la.

Use somente dados de teste. Não reutilize senhas presentes em fixtures, mantenha `DEBUG` desabilitado em servidores públicos e revise dependências antes de qualquer implantação externa.

## 👨‍💻 Repositório

**Walter Matheus Soares da Silva** · [GitHub](https://github.com/WalterMatheusgg)

Outros projetos do portfólio: [NEXUS CRM](https://github.com/WalterMatheusgg/NEXUS) · [Biblioteca Digital](https://github.com/WalterMatheusgg/library-service/tree/develop)
