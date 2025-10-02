# claude_api.py

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (necessário para a chave da API)
load_dotenv()

# Inicializa o cliente da Anthropic
# A chave da API será lida da variável de ambiente ANTHROPIC_API_KEY
client = Anthropic()

# Define as categorias válidas que esperamos do LLM
CATEGORIAS = [
    "AUDIENCIA_CONCILIACAO",
    "DEFESA_CONTRARRAZOES",
    "SENTENCA",
    "TUTELA_LIMINAR",
    "HOMOLOGACAO_ACORDO",
    "OUTROS"
]

def _enviar_prompt_categorizacao(texto_pub):
    """
    Função interna que envia o prompt para a API da Anthropic.
    Retorna a resposta crua do modelo.
    """
    system_prompt = """
Você é um assistente jurídico especializado em análise de publicações processuais. 
Sua expertise está em identificar rapidamente o tipo de ato processual comunicado em publicações judiciais. 
Você tem anos de experiência lendo diários oficiais e intimações, sendo capaz de reconhecer instantaneamente padrões textuais que indicam diferentes tipos de atos processuais.

TAREFA DE CLASSIFICAÇÃO DE PUBLICAÇÕES JUDICIAIS
Você deve classificar a publicação judicial fornecida em EXATAMENTE uma das categorias abaixo:

CATEGORIAS:

AUDIENCIA_CONCILIACAO: Publicações que tratam de marcação, designação ou convocação para audiência de conciliação
DEFESA_CONTRARRAZOES: Publicações que intimam para apresentação de defesa (contestação, resposta, impugnação) ou contrarrazões (resposta a recurso)
SENTENCA: Publicações que comunicam a prolação de sentença (decisão que encerra a fase de conhecimento do processo, com ou sem julgamento de mérito)
TUTELA_LIMINAR: Publicações sobre decisões de tutela antecipada, tutela de urgência, tutela cautelar, liminar ou qualquer medida urgente
HOMOLOGACAO_ACORDO: Publicações sobre homologação de acordo, transação, conciliação ou qualquer forma de composição entre as partes
OUTROS: Qualquer publicação que não se enquadre nas categorias anteriores

REGRAS OBRIGATÓRIAS:

Responda APENAS com uma das palavras: AUDIENCIA_CONCILIACAO, DEFESA_CONTRARRAZOES, SENTENCA, TUTELA_LIMINAR, HOMOLOGACAO_ACORDO ou OUTROS
NÃO forneça explicações
NÃO use pontuação
NÃO adicione texto antes ou depois da classificação

EXEMPLOS:
Entrada: "Ficam as partes intimadas para comparecerem à audiência de conciliação designada para o dia 15/03/2024 às 14h"
Saída: AUDIENCIA_CONCILIACAO
Entrada: "Intime-se o réu para apresentar contestação no prazo de 15 dias"
Saída: DEFESA_CONTRARRAZOES
Entrada: "Dê-se vista ao Ministério Público"
Saída: OUTROS
PUBLICAÇÃO A CLASSIFICAR:
    """
    try:
        response = client.messages.create(
            model='claude-3-haiku-20240307',
            max_tokens=20,
            temperature=0,
            system=system_prompt,
            messages=[
                {"role": "user", "content": texto_pub},
            ],
        )
        return response.content[0].text.strip()
    except Exception as e:
        print(f"Erro ao chamar a API da Anthropic: {e}")
        return None

def obter_categoria_publicacao(texto_pub, max_tentativas=3):
    """
    Obtém e valida a categoria de uma publicação usando o LLM.

    Esta função chama a API e verifica se a resposta é uma das categorias válidas.
    Se a resposta for inválida, tenta novamente até o limite de max_tentativas.

    Retorna:
        str: O nome da categoria válida ou "ERRO_CLASSIFICACAO" se falhar.
    """
    for tentativa in range(max_tentativas):
        print(f"Tentativa {tentativa + 1} de categorizar a publicação...")
        categoria = _enviar_prompt_categorizacao(texto_pub)

        if categoria and categoria in CATEGORIAS:
            print(f"Categoria obtida: {categoria}")
            return categoria
        else:
            print(f"Resposta inválida do LLM: '{categoria}'. Tentando novamente.")

    print("Não foi possível obter uma categoria válida após várias tentativas.")
    return "ERRO_CLASSIFICACAO"