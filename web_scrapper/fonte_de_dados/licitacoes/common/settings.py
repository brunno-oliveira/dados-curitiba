import os
class Settings():

    def __init__(self):
        super()

    BASE_URL = 'http://www.e-compras.curitiba.pr.gov.br/publico/processos/consulta/frmPesquisaDetalhada.aspx'
    DRIVER_PATH = 'PATH TO DRIVER'

    # DATA FOLDER
    DATA_FOLDER = os.path.join('tmp','data','licitacao')
    RAW_FOLDER = os.path.join(DATA_FOLDER,'raw')
    STAGE_FOLDER = os.path.join(DATA_FOLDER, 'stage')
    STAGE_FORNECEDORES_CSV = os.path.join(STAGE_FOLDER, 'fornecedores.csv')

    # TESTING FOLDERS
    TEST_FOLDER = os.path.join(DATA_FOLDER, 'test')
    TEST_RAW_FOLDER = os.path.join(TEST_FOLDER,'raw')
    TEST_STAGE_FOLDER = os.path.join(TEST_FOLDER, 'stage')
    TEST_FORNECEDORES_CSV = os.path.join(TEST_STAGE_FOLDER, 'fornecedores.csv')

    # AWS KEYS
    AWS_ACESS_KEY = 'XXXXXXX'
    AWS_SECRET_ACESS_KEY = 'XXXXXXX'

    AWS_BUCKET = 'igti-pa'
    TEST_S3_FOLDER_RAW = 'licitacao\test\raw' 
    S3_FOLDER_RAW = 'licitacao\raw'
    TEST_S3_FOLDER_STAGE = 'licitacao\test\stage' 
    S3_FOLDER_STAGE = 'licitacao\stage'
