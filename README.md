# MVP Florê Cosméticos

Sistema inicial de controle de estoque para a Florê Cosméticos, desenvolvido em Python, Flask e SQLite.

## Funcionalidades
- Cadastro de produtos (nome, categoria, preço, quantidade e estoque mínimo).
- Consulta e pesquisa por nome ou categoria.
- Entrada e saída de estoque, com validação para impedir estoque negativo.
- Destaque de produtos no limite ou abaixo do estoque mínimo.

## Como executar
1. Instale Python 3.10 ou superior.
2. Crie e ative um ambiente virtual (opcional, recomendado).
3. Instale as dependências: `pip install -r requirements.txt`.
4. Execute: `python app.py`.
5. Acesse `http://127.0.0.1:5000`.

O banco `flore.db` é criado automaticamente na primeira execução.

## Testes
Execute `pytest` na pasta do projeto.

## Observação
Este é um MVP acadêmico inicial. Antes de uso real, configure uma chave secreta segura, implemente autenticação e realize testes adicionais de segurança e usabilidade.
## Funcionalidades do sistema

- Cadastro de produtos.
- Consulta de produtos.
- Entrada de estoque.
- Saída de estoque.
- Aviso de estoque baixo.
- Armazenamento em banco de dados SQLite.
## Objetivo do projeto

Facilitar o controle de estoque da Florê Cosméticos, ajudando a reduzir erros nos registros, evitar perdas de produtos e melhorar o acompanhamento das reposições.
