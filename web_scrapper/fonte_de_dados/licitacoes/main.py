from scrapper.licitacoes import Licitacao
from etl.etl import Etl
import logging
import boto3
import sys

#logging.getLogger().addHandler(logging.StreamHandler()) # Writes to console
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger("requests").setLevel(logging.CRITICAL)

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(process)-5d][%(asctime)s][%(filename)-20s][%(levelname)-8s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# FALTA A ULTIMA PAGINA !!!!
if __name__ == '__main__':   
    if(sys.argv[1] == 'crawler'):
        logging.info('Iniciando Web Crawler..')
        Licitacao().run(122,None,'01/01/2015','31/12/2015')
    elif(sys.argv[1] == 'etl'):
        logging.info('Iniciando ETL..')
        Etl().run()
    elif(sys.argv[1] == 'full'):
        logging.info('Iniciando Modo Full..')
        logging.info('Iniciando Web Crawler..')
        Licitacao().run(1)
        logging.info('Iniciando ETL..')
        Etl().run()
    elif(sys.argv[1] == 'test'):
        logging.info('Executando modo teste')
        Licitacao(True).run(3700,1)
        Etl(True).run()
    logging.info('Processo finalizado')
