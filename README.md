### Visão Geral do Código

O objetivo deste conjunto de scripts é automatizar a criação de tarefas no **Asana** a partir de publicações de processos judiciais de um advogado específico. O fluxo é o seguinte:

1.  O script **`main.py`** é o ponto de partida. Ele define o nome do advogado e a data atual.
2.  Ele chama uma função do script **`comunicapje.py`** para buscar as publicações mais recentes do advogado.
3.  O script **`comunicapje.py`** se conecta à **API do ComunicaPJE**, um serviço que disponibiliza informações de publicações judiciais. Ele busca as publicações do advogado na data especificada e organiza os dados relevantes, como o número do processo e o texto da publicação.
4.  Com a lista de publicações em mãos, o script `main.py` chama uma função do script **`asana_api.py`**.
5.  O script **`asana_api.py`** se conecta à **API do Asana**. Para cada publicação encontrada, ele cria uma nova tarefa no seu projeto do Asana, usando os dados da publicação, como o número do processo e o texto, para preencher a tarefa.

---

### Passo 0: Instalar o Python e as Bibliotecas Necessárias

Para rodar este script, você precisará ter o **Python** instalado na sua máquina e também instalar as bibliotecas **requests** e **asana**.

1.  **Instale o Python**: Se você ainda não tem o Python instalado, baixe a versão mais recente em [python.org](https://www.python.org/). Durante a instalação, certifique-se de marcar a opção "Add Python to PATH", que facilita o uso do Python pelo terminal.

2.  **Instale as bibliotecas**: Abra o seu terminal ou prompt de comando e execute os seguintes comandos para instalar as bibliotecas necessárias:
    ```
    pip install requests
    pip install asana
    ```

---

### Passo 1: Configurar o Asana

Para que o script funcione, você precisa fornecer a ele uma "chave" para acessar sua conta do Asana, chamada de **Personal Access Token**.

1.  Acesse sua conta do **Asana** no navegador.
2.  Vá em **Minhas configurações** > **Aplicativos**.
3.  Na seção "Desenvolvedor", clique em **Gerenciar Personal Access Tokens**.
4.  Clique em **+ Criar novo token**. Dê um nome, aceite os termos e salve o token em um local seguro.

**Atenção**: O token que está no arquivo `asana_api.py` (a variável `ACESS_TOKEN`) é apenas um exemplo. Você deve substituí-lo pelo seu próprio token.

---

### Passo 2: Obter o ID do Projeto no Asana

O script precisa saber em qual projeto do Asana ele deve criar as tarefas. Para encontrar o ID (conhecido como `gid`), você pode usar a função `get_projects()` no script `asana_api.py`.

1.  Abra o arquivo `asana_api.py`.
2.  Substitua o valor da variável **`ACESS_TOKEN`** pelo token que você acabou de gerar.
3.  Descomente a linha `get_projects()` (se ainda não estiver) e execute o script.

O script vai imprimir uma lista de todos os seus projetos do Asana. Encontre o projeto que você deseja usar e anote o número **`gid`** associado a ele. No exemplo do arquivo, o `gid` é `1211086539650689`.

---

### Passo 3: Configurar os Arquivos Python

Agora que você já tem o seu token e o ID do projeto, é hora de ajustar o código.

1.  **No arquivo `asana_api.py`**:
    * Substitua o valor da variável `ACESS_TOKEN` pelo seu token pessoal.
    * Substitua o `gid` do projeto na variável `body` da função `create_tasks_pubs` pelo ID que você anotou no passo anterior.

2.  **No arquivo `main.py`**:
    * Altere o valor da variável `NOME_ADVOGADO` para o nome completo do advogado que você quer monitorar.
    * O script está configurado para buscar publicações na data atual, com as variáveis `data_inicio` e `data_fim` sendo a data de hoje.

---

### Passo 4: Executar o Script

Com tudo configurado, você pode rodar o script principal.

1.  Abra um terminal ou prompt de comando.
2.  Navegue até a pasta onde os arquivos estão salvos.
3.  Execute o arquivo `main.py` com o comando:
    ```
    python main.py
    ```

O script vai se conectar à API do ComunicaPJE, buscar as publicações do advogado na data de hoje e, em seguida, criar uma tarefa no seu projeto do Asana para cada publicação encontrada. A tarefa terá o número do processo no título e o texto da publicação na descrição.

---

### Possíveis Erros e Como Resolvê-los

Ao usar o script, você pode encontrar alguns problemas comuns.

* **Erro de Conexão com a API do ComunicaPJE**: Às vezes, o servidor do ComunicaPJE pode estar fora do ar, o que causará um erro no script. Se isso acontecer, a solução é simples: espere alguns minutos e tente rodar o script novamente.

* **Erro de Autenticação no Asana**: Certifique-se de que o **Personal Access Token** que você inseriu no arquivo `asana_api.py` está correto. Se o token for inválido, o script não conseguirá criar as tarefas e exibirá uma exceção.

* **Erro com o `gid` do Projeto**: Verifique se o ID do projeto que você inseriu na função `create_tasks_pubs` em `asana_api.py` está correto. Um `gid` incorreto impedirá que as tarefas sejam criadas no local certo.