### Visão Geral do Código

O objetivo deste conjunto de scripts é demonstrar como é possível automatizar a criação  de tarefas no **Asana** a partir de publicações judiciais. O sistema utiliza um Modelo de Linguagem Grande (LLM) para analisar o conteúdo de cada publicação e atribuir a tarefa ao responsável correto.

O fluxo é o seguinte:

1.  O script **`main.py`** é o ponto de partida. Ele define o nome do advogado a ser monitorado e a data atual.
2.  Ele chama uma função do script **`comunicapje.py`** para se conectar à **API do ComunicaPJE** e buscar as publicações mais recentes do advogado.
3.  Com a lista de publicações, `main.py` itera sobre cada uma e chama uma função do script **`claude_api.py`**.
4.  O `claude_api.py` envia o texto da publicação para a **API da Anthropic (Claude)**, que o analisa e o classifica em uma categoria predefinida (ex: `DEFESA_CONTRARRAZOES`, `AUDIENCIA_CONCILIACAO`, etc.).
5.  De volta ao `main.py`, o script utiliza a categoria retornada pelo modelo para determinar, através de uma lógica interna, qual membro da equipe é o responsável por aquele tipo de tarefa.
6.  Finalmente, o `main.py` chama a função apropriada no `asana_api.py` para se conectar à **API do Asana** e criar uma nova tarefa, já atribuída à pessoa certa e com um título que reflete seu conteúdo.

---

### Passo 0: Instalar o Python e as Bibliotecas Necessárias

Para rodar este script, você precisará do **Python** e de algumas bibliotecas.

1.  **Instale o Python**: Se ainda não o tiver, baixe a versão mais recente em [python.org](https://www.python.org/). Durante a instalação, marque a opção "Add Python to PATH".

2.  **Instale as bibliotecas**: Abra seu terminal (ou prompt de comando) e execute os seguintes comandos:
    ```bash
    pip install requests
    pip install asana
    pip install anthropic
    pip install python-dotenv
    ```

---

### Passo 1: Configurar Chaves de Acesso (Tokens)

Este projeto precisa de acesso a duas APIs: Asana e Anthropic. A maneira mais segura de gerenciar essas chaves é usando um arquivo de ambiente.

1.  **Crie um arquivo `.env`**: Na mesma pasta onde estão os scripts, crie um novo arquivo chamado `.env`.

2.  **Obtenha o Personal Access Token do Asana**:
    * Acesse sua conta do **Asana** e vá em **Minhas configurações** > **Aplicativos** > **Gerenciar Personal Access Tokens**.
    * Clique em **+ Criar novo token**, dê um nome a ele e salve o token gerado.
    * No seu arquivo `.env`, adicione a seguinte linha, substituindo `SEU_TOKEN_DO_ASANA` pelo token que você copiou:
        ```
        ASANA_ACCESS_TOKEN="SEU_TOKEN_DO_ASANA"
        ```

3.  **Obtenha a Chave de API da Anthropic (Claude)**:
    * Acesse o site da Anthropic e navegue até a seção de chaves de API (API Keys).
    * Gere uma nova chave de API.
    * No mesmo arquivo `.env`, adicione a seguinte linha, substituindo `SUA_CHAVE_DA_ANTHROPIC` pela chave que você gerou:
        ```
        ANTHROPIC_API_KEY="SUA_CHAVE_DA_ANTHROPIC"
        ```

---

### Passo 2: Obter IDs (GIDs) no Asana

O script precisa de dois tipos de IDs do Asana: o do **Projeto** onde as tarefas serão criadas e os dos **Usuários** que serão responsáveis por elas.

1.  **ID do Projeto**:
    * Para encontrar o `gid` do projeto, você pode usar a função `get_projects()` no script `asana_api.py`.
    * Abra o arquivo, substitua o valor de `ACESS_TOKEN` temporariamente pelo seu token, descomente a chamada da função `get_projects()` e execute o script `python asana_api.py`.
    * Ele listará todos os seus projetos. Encontre o `gid` do projeto desejado e anote-o.

2.  **IDs dos Usuários**:
    * A forma mais fácil de encontrar o `gid` de um usuário é acessar o perfil dele no Asana e copiar o número que aparece na URL do navegador.

---

### Passo 3: Configurar os Arquivos Python

Agora, vamos ajustar os scripts para usar os IDs que você coletou.

1.  **No arquivo `asana_api.py`**:
    * **(Opcional)** O script está configurado para ler o token do arquivo `.env`. Se preferir, você pode substituir o valor da variável `ACESS_TOKEN` diretamente no código.
    * Na função `criar_tarefa_categoria`, substitua o `gid` do projeto (`"1211086539650689"`) pelo ID do seu projeto que você anotou.

2.  **No arquivo `main.py`**:
    * Altere o valor da variável `NOME_ADVOGADO` para o nome completo do advogado que você quer monitorar.
    * No dicionário `RESPONSAVEIS_GIDS`, substitua os `gids` de exemplo pelos IDs reais dos usuários do Asana que você anotou. Cada categoria de tarefa deve ser mapeada para o `gid` do membro da equipe responsável por ela.

---

### Passo 4: Executar o Script

Com tudo configurado, você pode rodar o script principal.

1.  Abra um terminal na pasta onde os arquivos estão salvos.
2.  Execute o `main.py` com o comando:
    ```bash
    python main.py
    ```

O script irá buscar as publicações, classificá-las com o LLM e criar as tarefas no seu projeto do Asana, já delegadas para as pessoas certas.

---

### Nota sobre Funções de Demonstrações Anteriores

No arquivo `asana_api.py`, você notará a existência de outras funções para criar tarefas, como `criar_tarefas_pubs_area` e `criar_tarefas_pubs_resp`. Essas funções foram mantidas como um registro de demonstrações anteriores, que utilizavam lógicas mais simples (como buscar o responsável em um arquivo Excel). Elas **não são utilizadas** no fluxo atual, que se baseia na classificação de conteúdo feita pelo LLM.

---

### Possíveis Erros e Como Resolvê-los

* **Erro de Conexão com a API do ComunicaPJE**: O servidor pode estar temporariamente fora do ar. Espere alguns minutos e tente rodar o script novamente.
* **Erro de Autenticação no Asana**: Verifique se o token no seu arquivo `.env` (`ASANA_ACCESS_TOKEN`) está correto e não expirou.
* **Erro de Autenticação na Anthropic**: Verifique se a chave de API no seu arquivo `.env` (`ANTHROPIC_API_KEY`) está correta.
* **Erro com o `gid` do Projeto**: Certifique-se de que o ID do projeto inserido na função `criar_tarefa_categoria` está correto.