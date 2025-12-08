# Sistema de Gestão Rodofrio

Sistema web desenvolvido para a disciplina de **Programação II**, integrando conceitos de Engenharia de Software e Banco de Dados. O objetivo é substituir o controle manual de planilhas da empresa Rodofrio por uma aplicação web robusta, segura e responsiva.

## Funcionalidades

**Autenticação e Segurança:** Login com JWT (JSON Web Tokens) e controle de sessão.
**Controle de Acesso (RBAC):** Diferenciação de menus e rotas para **Administrador** (Colaborador Interno) e **Técnico Terceirizado**.
**CRUDs Completos:** Gestão de Clientes, Caminhões e Ordens de Serviço.
**Dashboard Dinâmico:** Visão geral com contadores e total faturado em tempo real.
**Ordenação e Filtros:** Pesquisa dinâmica e ordenação por status, data ou valor.
**Regras de Negócio:** Conciliação de serviços (Técnico lança -> Pendente -> Admin Confirma).

## Tecnologias Utilizadas

### Front-end
**React + Vite:** Para uma interface rápida e moderna.
**Material UI (MUI):** Biblioteca de componentes para garantir responsividade e estética profissional.
**Axios:** Para comunicação com a API.
**React Router Dom:** Para navegação SPA (Single Page Application).

### Back-end
**Node.js + Express:** Servidor API RESTful.
**PostgreSQL:** Banco de dados relacional.
**Cors:** Para segurança de requisições.

---

## Como Rodar o Projeto

### Pré-requisitos
* Node.js instalado.
* PostgreSQL instalado e rodando.
* Yarn instalado (`npm install -g yarn`).

### 1. Configurar o Banco de Dados
Crie um banco de dados no PostgreSQL chamado `rodofrio_db` e execute o script SQL (bd.sql) para criar as tabelas e os usuários iniciais.

### 1.1 Configurar Variáveis de Ambiente
Na pasta `backend`, renomeie o arquivo `.env.example` para `.env`.
Abra o arquivo e edite a senha do banco de dados conforme a sua configuração local do PostgreSQL:

DB_USER=postgres
DB_HOST=localhost
DB_NAME=rodofrio_db
DB_PASSWORD=postgres  <-- COLOQUE SUA SENHA AQUI
DB_PORT=5432
SEGREDO_JWT=SEGREDO_DO_LUAN

### 2. Rodar o Back-end
Abra o terminal na pasta backend:

# Instalar dependências
yarn

# Rodar o servidor (estando na pasta backend)
nodemon src/server.js

### 3. Rodar o Front-end
Abra um novo terminal na pasta frontend:

# Instalar dependências
yarn

# Rodar a interface
yarn dev

### 4. Acessos para Teste
# Perfil Administrador (Vê tudo + Confirma serviços):
Login: admin@rodofrio.com
Senha: 123

# Perfil Técnico (Acesso restrito):
Login: sergio.tecnico@email.com
Senha: 123