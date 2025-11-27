# CineRate - Sistema de Avaliação de Filmes

Sistema completo para gerenciamento e avaliação de filmes, com painel administrativo e interface para usuários.

## Funcionalidades

- **Catálogo de filmes** com informações completas
- **Sistema de avaliação** (0-10 estrelas)
- **Lançamentos 2024-2025** em destaque
- **Painel administrativo** com CRUD completo
- **Filtros** por nome e gênero
- **Estatísticas** em tempo real

## Tecnologias

- **Backend:** Python, Flask, SQLAlchemy
- **Frontend:** HTML5, CSS3, JavaScript
- **Ferramentas:** Flask-CORS, python-dotenv

## Instalação

### 1. Clone o repositório
git clone https://github.com/Footed1234/Site-com-API-Flask.git

cd Site-com-API-Flask
### 2. Ambiente virtual (opcional)
python -m venv venv

Windows: venv\Scripts\activate

Linux/Mac: source venv/bin/activate
### 3. Instale as dependências
pip install -r requirements.txt
### 4. Crie as tabelas
python Modelo.py

python Tabela.py
### 5. Execute o sistema
python main.py

Acesso
  - Admin:
    - Usuário: admin
    - Senha: admin123

- Usuário comum: Cadastre-se no sistema

## API
Principais endpoints:
- GET/POST /afilmes - Gerenciar filmes
- GET/POST /usuarios - Gerenciar usuários
- POST /avaliar - Registrar avaliações
- GET /lancamentos - Listar lançamentos

## Dependências
### requirements.txt

Flask==2.3.3

Flask-CORS==4.0.0

SQLAlchemy==2.0.23

python-dotenv==1.0.0

## Como Usar
### Usuários:
Faça cadastro ou login

Explore o catálogo de filmes

Clique em qualquer filme para avaliar

Use os filtros para encontrar filmes

### Administradores:
Faça login com credenciais admin

Acesse o painel administrativo

Gerencie filmes e usuários

Visualize estatísticas do sistema

# Desenvolvido por
- Henrique Ratis
- João Pedro
- Davi Rubio
- Fabrício Konishi
- Samuel Marostega

### 26/11/2025
