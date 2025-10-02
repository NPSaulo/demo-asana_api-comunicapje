from datetime import datetime, timedelta
from asana_api import criar_tarefas_pubs_resp, criar_tarefas_pubs_area, criar_tarefa_categoria
from comunicapje import capturar_pubs
from dados import DADOS_ASANA, DADOS_RESP, DADOS_AREA, DADOS_PROJETOS
from claude_api import obter_categoria_publicacao

NOME_ADVOGADO = "SAULO NIEDERLE PEREIRA"
HOJE = datetime.now()
#convertendo a data em texto no formato AAAA-MM-DD
HOJE_STR = HOJE.strftime('%Y-%m-%d')


RESPONSAVEIS_GIDS = {
    "AUDIENCIA_CONCILIACAO": "1211538004228102",  
    "DEFESA_CONTRARRAZOES": "1211537999224030",   
    "SENTENCA": "1211538004302305",             
    "TUTELA_LIMINAR": "1211538004413678",          
    "HOMOLOGACAO_ACORDO": "1211538004547247",      
    "OUTROS": "1211538004831189"                  
}



def main():
    #pegando publicações do advogado acima definido na data de hoje API do ComunicaPJE
    pubs = capturar_pubs(nome_adv=NOME_ADVOGADO, data_inicio=HOJE_STR, data_fim=HOJE_STR)
    #criando uma tarefa para cada publicação no Asana por meio de sua API
    #criar_tarefas_pubs_resp(pubs=pubs, hoje=HOJE_STR, DADOS_ASANA=DADOS_ASANA, DADOS_RESP=DADOS_RESP)
    #criar_tarefas_pubs_area(pubs=pubs, hoje=HOJE_STR, DADOS_AREA=DADOS_AREA, DADOS_PROJETOS=DADOS_PROJETOS)
    for pub in pubs:
        print("-" * 50)
        print(f"Processando publicação do processo: {pub['numeroprocessocommascara']}")

        # 3. Usa o LLM para obter a categoria da publicação
        categoria = obter_categoria_publicacao(pub['texto'])
        
        id_responsavel = None

        if categoria == "AUDIENCIA_CONCILIACAO":
            id_responsavel = RESPONSAVEIS_GIDS["AUDIENCIA_CONCILIACAO"]
        
        elif categoria == "DEFESA_CONTRARRAZOES":
            id_responsavel = RESPONSAVEIS_GIDS["DEFESA_CONTRARRAZOES"]

        elif categoria == "SENTENCA":
            id_responsavel = RESPONSAVEIS_GIDS["SENTENCA"]

        elif categoria == "TUTELA_LIMINAR":
            id_responsavel = RESPONSAVEIS_GIDS["TUTELA_LIMINAR"]
            
        elif categoria == "HOMOLOGACAO_ACORDO":
            id_responsavel = RESPONSAVEIS_GIDS["HOMOLOGACAO_ACORDO"]

        else:  #"OUTROS" ou "ERRO_CLASSIFICACAO"
            id_responsavel = RESPONSAVEIS_GIDS["OUTROS"]

        criar_tarefa_categoria(pub, categoria, id_responsavel, HOJE_STR)



if __name__ == "__main__":
    main()