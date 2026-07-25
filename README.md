Este projeto, denominado **bank-api**, consiste no desenvolvimento de uma API RESTful **assíncrona** robusta e segura para a gestão de operações bancárias, como depósitos, saques e consulta de extratos. A arquitetura foi desenhada para separar claramente as responsabilidades de segurança (autenticação), persistência de dados e regras de negócio.

Um dos diferenciais técnicos é o uso do **motor assíncrono** do FastAPI, que utiliza o mecanismo de *Event Loop* para gerenciar requisições de forma não-bloqueante. Isso garante que a aplicação mantenha alta performance mesmo lidando com múltiplas operações simultâneas, pois o servidor não fica "travado" aguardando o retorno do banco de dados.

### Tecnologias Utilizadas

O projeto utiliza o **Poetry** para o gerenciamento de dependências e isolamento do ambiente virtual (`pyproject.toml`), garantindo reprodutibilidade e organização.

| Tecnologia | Finalidade no Projeto |
| :--- | :--- |
| **FastAPI** | Framework web de alto desempenho para construção da API. |
| **SQLAlchemy (Async)** | ORM para mapeamento de dados com suporte a operações assíncronas. |
| **Pydantic (V2)** | Validação rigorosa de tipos e dados de entrada/saída (Schemas). |
| **Poetry** | Ferramenta de gerenciamento de dependências e empacotamento. |
| **PyJWT** | Implementação de segurança através de JSON Web Tokens (JWT). |
| **Passlib (Bcrypt)** | Criptografia (hashing) segura de senhas de usuários. |
| **Uvicorn** | Servidor ASGI para execução da aplicação FastAPI. |
| **Aiosqlite** | Driver que permite o acesso assíncrono ao banco de dados SQLite. |

---

### Tutorial de Funcionamento

Siga os passos abaixo para configurar e testar a API em seu ambiente local:

#### 1. Configuração do Ambiente
Certifique-se de ter o Python (>=3.12) e o Poetry instalados.
*   Instale as dependências: `poetry install`.
*   Crie um arquivo **.env** na raiz do projeto com as variáveis obrigatórias:
    *   `SECRET_KEY`: Sua chave secreta para criptografia JWT.
    *   `DATABASE_URL`: Ex: `sqlite+aiosqlite:///./bank.db`.

#### 2. Execução do Servidor
Inicie o servidor de desenvolvimento com o comando:
`uvicorn app.main:app --reload`.
A API utiliza um gerenciador de contexto (*lifespan*) para criar automaticamente as tabelas do banco de dados na primeira execução.

#### 3. Testando via Swagger UI
O FastAPI gera automaticamente uma documentação interativa acessível em: **`http://localhost:8000/docs`**.

**Roteiro sugerido de testes:**
1.  **Registro de Usuário (`POST /auth/register`):** Crie uma conta fornecendo username, e-mail e senha. O sistema criará automaticamente uma conta corrente vinculada com saldo zerado.
2.  **Login (`POST /auth/login`):** Informe suas credenciais para receber o **access_token**.
3.  **Autenticação (Authorize):** Clique no botão do "cadeado verde" no topo da página. Você pode preencher o usuário e senha diretamente no formulário ou colar o token manualmente.
4.  **Operações Bancárias (`POST /banking/transaction`):**
    *   **Depósito:** Realize um depósito informando um valor positivo.
    *   **Saque:** Tente realizar um saque. O sistema validará se há saldo suficiente e impedirá valores negativos.
5.  **Consulta de Extrato (`GET /banking/statement`):** Visualize o saldo atual e o histórico imutável de todas as transações realizadas.
