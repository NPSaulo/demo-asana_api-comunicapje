from datetime import datetime, timedelta
from asana_api import create_tasks_pubs
from comunicapje import capturar_pubs

NOME_ADVOGADO = "SAULO NIEDERLE PEREIRA"
#HOJE = datetime.now()
#convertendo a data em texto no formato AAAA-MM-DD
#HOJE_STR = HOJE.strftime('%Y-%m-%d')
HOJE_STR = "2025-08-26"

def main():
    #pegando publicações do advogado acima definido na data de hoje API do ComunicaPJE
    pubs = capturar_pubs(nome_adv=NOME_ADVOGADO, data_inicio=HOJE_STR, data_fim=HOJE_STR)
    #criando uma tarefa para cada publicação no Asana por meio de sua API
    create_tasks_pubs(pubs=pubs, hoje=HOJE_STR)

if __name__ == "__main__":
    main()