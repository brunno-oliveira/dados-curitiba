from etl.mapa_fornecedores import MapaFornecedores
from common.settings import Settings
from common.file import FileController
from etl.licitacao import Licitacao
from common.file import FileController
from bs4 import BeautifulSoup
from common.s3 import s3
import logging
import os
import re

class Etl:
    def __init__(self,testing=False):
        self.settings = Settings()
        FileController().validateDataFolders()
        if(testing):
            self.folder = self.settings.TEST_RAW_FOLDER
            self.path_csv = self.settings.TEST_FORNECEDORES_CSV
        else:
            self.folder = self.settings.RAW_FOLDER
            self.path_csv = self.settings.STAGE_FORNECEDORES_CSV

    def licitacao(self,text,filepath,_licitacao):        
        """ Percorre o HTML da licitacao linha por linha e identifica os valores chaves """
        _licitacao.folder = filepath
        for line in text:
            # ID
            if(line.find('ctl00_cph1_ucCab_tdNome"') > 0):
                prefix = re.findall('.*ctl00_cph1_ucCab_tdNome.*">',line)
                id = line.replace(prefix[0],'')
                sufix = re.findall('</td.*',id)
                id = id.replace(sufix[0],'').strip() 
                _licitacao.id = id   
            # EMPRESA           
            elif(line.find('ctl00_cph1_ucCab_tdEmpresa') > 0):
                prefix = re.findall('.*ctl00_cph1_ucCab_tdEmpresa.*">',line)
                empresa = line.replace(prefix[0],'')
                sufix = re.findall('</td.*',empresa)
                empresa = empresa.replace(sufix[0],'').strip()
                _licitacao.empresa = empresa                      
            # STATUS
            elif(line.find('ctl00_cph1_ucCab_tdStatus') > 0):                                        
                prefix = re.findall('.*ctl00_cph1_ucCab_tdStatus.*">',line)
                status = line.replace(prefix[0],'')
                sufix = re.findall('</td.*',status)
                status = status.replace(sufix[0],'').strip()
                _licitacao.status = status
            # SETOR DE COMPRAS
            elif(line.find('ctl00_cph1_ucCab_tdSetor') > 0):                                        
                prefix = re.findall('.*ctl00_cph1_ucCab_tdSetor">',line)
                setor_de_compras = line.replace(prefix[0],'')
                sufix = re.findall('</td.*',setor_de_compras)
                setor_de_compras = setor_de_compras.replace(sufix[0],'').strip()
                _licitacao.setor_de_compras = setor_de_compras
            # OBJETO
            elif(line.find('ctl00_cph1_ucCab_tdObjeto') > 0):                                        
                prefix = re.findall('.*ctl00_cph1_ucCab_tdObjeto.*">',line)
                objeto = line.replace(prefix[0],'')
                sufix = re.findall('</td.*',objeto)
                objeto = objeto.replace(sufix[0],'').strip()   
                _licitacao.objeto = objeto
            # RESPONSAVEL        
            elif(line.find('ctl00_cph1_ucCab_lblResp') > 0):                                        
                prefix = re.findall('.*ctl00_cph1_ucCab_lblResp.*">',line)
                responsavel = line.replace(prefix[0],'')
                sufix = re.findall('</span.*',responsavel)
                responsavel = responsavel.replace(sufix[0],'').strip()    
                _licitacao.responsavel = responsavel
            # ABERTURA PROPOSTAS
            elif(line.find('ctl00_cph1_ucCab_tdInicioProp') > 0):                                        
                prefix = re.findall('.*ctl00_cph1_ucCab_tdInicioProp.*">',line)
                abertura_propostas = line.replace(prefix[0],'')
                sufix = re.findall('</td.*',abertura_propostas)
                abertura_propostas = abertura_propostas.replace(sufix[0],'').strip()    
                _licitacao.abertura_propostas = abertura_propostas
            # ENCERRAMENTO PROPOSTAS
            elif(line.find('ctl00_cph1_ucCab_tdEncerraProp') > 0):                                        
                prefix = re.findall('.*ctl00_cph1_ucCab_tdEncerraProp.*">',line)
                encerramento_propostas = line.replace(prefix[0],'')
                sufix = re.findall('</td.*',encerramento_propostas)
                encerramento_propostas = encerramento_propostas.replace(sufix[0],'').strip()    
                _licitacao.encerramento_propostas = encerramento_propostas
            # INICIO SESSAO
            elif(line.find('ctl00_cph1_ucCab_tdInicioSessao') > 0):                                        
                prefix = re.findall('.*ctl00_cph1_ucCab_tdInicioSessao.*">',line)
                inicio_sessao = line.replace(prefix[0],'')
                sufix = re.findall('</td.*',inicio_sessao)
                inicio_sessao = inicio_sessao.replace(sufix[0],'').strip()                    
                _licitacao.inicio_sessao = inicio_sessao
            # ENCERRAMENTO SESSAO
            elif(line.find('ctl00_cph1_ucCab_tdEncerraSessao') > 0):                                        
                prefix = re.findall('.*ctl00_cph1_ucCab_tdEncerraSessao.*">',line)
                encerramento_sessao = line.replace(prefix[0],'')
                sufix = re.findall('</td.*',encerramento_sessao)
                encerramento_sessao = encerramento_sessao.replace(sufix[0],'').strip()                    
                _licitacao.encerramento_sessao = encerramento_sessao
            # NUMERO DE FORNECEDORES
            elif(line.find('ctl00_cph1_ucCab_lblNumForn') > 0):                                        
                prefix = re.findall('.*ctl00_cph1_ucCab_lblNumForn.*">',line)
                n_fornecedores = line.replace(prefix[0],'')
                sufix = re.findall('</span.*',n_fornecedores)
                n_fornecedores = n_fornecedores.replace(sufix[0],'').strip()                 
                _licitacao.n_fornecedores = n_fornecedores
            # NUMERO DE ME/EPP
            elif(line.find('ctl00_cph1_ucCab_tdNumFornMEEPP') > 0):                                        
                prefix = re.findall('.*ctl00_cph1_ucCab_tdNumFornMEEPP.*">',line)
                n_me_epp = line.replace(prefix[0],'')
                sufix = re.findall('</span.*',n_me_epp)
                n_me_epp = n_me_epp.replace(sufix[0],'').strip()                
                _licitacao.n_me_epp = n_me_epp
            # NUMERO DE PROPOSTAS VALIDAS
            elif(line.find('ctl00_cph1_ucCab_tdNumProp') > 0):                                        
                prefix = re.findall('.*ctl00_cph1_ucCab_tdNumProp.*">',line)
                n_propostas_validas = line.replace(prefix[0],'')
                sufix = re.findall('</td.*',n_propostas_validas)
                n_propostas_validas = n_propostas_validas.replace(sufix[0],'').strip()                   
                _licitacao.n_propostas_validas = n_propostas_validas
            # NUMERO DE RECUSAS
            elif(line.find('ctl00_cph1_ucCab_tdNumRecusasMEEPP') > 0):                                        
                prefix = re.findall('.*ctl00_cph1_ucCab_tdNumRecusasMEEPP.*">',line)
                n_recusas = line.replace(prefix[0],'')
                sufix = re.findall('</td.*',n_recusas)
                n_recusas = n_recusas.replace(sufix[0],'').strip()                
                _licitacao.n_recusas = n_recusas


    def run(self):        
        logging.info('Running etl')
        for year in os.listdir(self.folder):
            logging.debug('-----YEAR: ' + str(year))
            yearFolder = os.path.join(self.folder, year)

            for month in os.listdir(yearFolder):
                logging.debug('----MONTH: ' + str(month))
                monthFolder = os.path.join(yearFolder, month)

                for day in os.listdir(monthFolder):
                    dayFolder = os.path.join(monthFolder, day)

                    for licitacao in os.listdir(dayFolder):
                        licitacaoFolder = os.path.join(dayFolder, licitacao)
                        _licitacao = Licitacao()  

                        for file in os.listdir(licitacaoFolder):     
                            filepath = os.path.join(licitacaoFolder, file)                     
                            if(file == 'map_fornecedores.html'):
                                MapaFornecedores(_licitacao, self.path_csv).getMapaFornecedores(filepath)
                            else:
                                f = open(filepath, "r")
                                text = f.readlines()
                                self.licitacao(text,filepath,_licitacao)
                                f.close()
        
        logging.info('Subindo arquivo consoludado para o S3')
        s3().upload(self.path_csv, self.path_csv.replace('tmp\\data\\', '').replace('\\','/'))
        logging.info('Arquivo enviado com sucesso')

        