from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common import exceptions

from common.s3 import s3
from common.file import FileController
from contextlib import contextmanager
from datetime import datetime
from selenium import webdriver
from time import sleep
import pandas as pd
import binascii
import logging
import json
import sys
import os

from common.settings import Settings

LOGGER.setLevel(logging.WARNING) #Selenium log

class Licitacao:
    def __init__(self, testing=False):
        self.settings = Settings()  
        if(testing):
            self.folder = self.settings.TEST_RAW_FOLDER
            self.s3_folder = self.settings.TEST_S3_FOLDER_RAW
        else:
            self.folder = self.settings.RAW_FOLDER
            self.s3_folder = self.settings.S3_FOLDER_RAW
  
        self.driver = webdriver.Firefox(executable_path=self.settings.DRIVER_PATH)

    def getListOfPages(self, stringOfPages):
        """ Retorna um dataframe com a lista de paginas """
        number = []
        listOfPages = []
        pageNumber = ''

        for t in stringOfPages:
            try:
                """ Se nao conseguir castar pra inteiro, é uma quebra de linha (/n) """     
                number.append(int(t))
            except:               
                if len(t) > 0:
                    for n in number:
                        pageNumber = pageNumber + str(n)         
                    listOfPages.append(int(pageNumber))
                    number.clear()
                    pageNumber = ''

        df = pd.DataFrame(listOfPages, columns = ['pageNumber'])
        df['selected'] = False      
        return df      


    def validateDirectory(self, filepath):    
        if not os.path.exists(filepath):
            try:
                os.makedirs(filepath)
            except Exception as e:
                logging.error('ERRO while creating path: {} \n Error: {}'.format(filepath,e))


    def getButtonID(self, licitacaoNumber):
        """ O elemento ID ctl00_cph1_gdpProcs_ctlxx_imDetalhes controle o processo de listagem da página
            onde o xx é o número seguencial do link.
            Iniciando sempre em ctl00_cph1_gdpProcs_ctl02_imDetalhes
            e finalizando em    ctl00_cph1_gdpProcs_ctl11_imDetalhes
        """    
        ids = {
            1:  "ctl00_cph1_gdpProcs_ctl02_imDetalhes",
            2:  "ctl00_cph1_gdpProcs_ctl03_imDetalhes",
            3:  "ctl00_cph1_gdpProcs_ctl04_imDetalhes",
            4:  "ctl00_cph1_gdpProcs_ctl05_imDetalhes",
            5:  "ctl00_cph1_gdpProcs_ctl06_imDetalhes",
            6:  "ctl00_cph1_gdpProcs_ctl07_imDetalhes",
            7:  "ctl00_cph1_gdpProcs_ctl08_imDetalhes",
            8:  "ctl00_cph1_gdpProcs_ctl09_imDetalhes",
            9:  "ctl00_cph1_gdpProcs_ctl10_imDetalhes",
            10: "ctl00_cph1_gdpProcs_ctl11_imDetalhes"
        }    

        return ids.get(licitacaoNumber)


    def encodeLicitacao(self, licitacaoCode):
        """ Gera um hash hexadecimal para o código da licitação,
            utilizado como chave da licitação
        """
        licitacaoCode = licitacaoCode.replace(" ", "")
        return binascii.hexlify(bytearray(licitacaoCode, 'utf-8'))


    def decodeLicId(self, licHash):
        return binascii.unhexlify(licHash).decode('utf-8')


    def getFileName(self, licitacaoData):
        """
            Returns PATH and FULL FILE NAME
            Path Structure:
            tmp/
            tmp/raw/
            tmp/raw/data/
            tmp/raw/data/{year}/
            tmp/raw/data/{year}/{month}/
            tmp/raw/data/{year}/{month}/{day}/
            tmp/raw/data/{year}/{month}/{day}/{id}
        """
        datetimeFormat = datetime.strptime(licitacaoData['abertura'], '%d/%m/%Y %H:%M:%S')
        hashName = str(self.encodeLicitacao(licitacaoData['id']))

        file_path = os.path.join(self.folder, 
                                str(datetimeFormat.year), 
                                '0' + str(datetimeFormat.month) if(datetimeFormat.month < 10) else str(datetimeFormat.month),
                                '0' + str(datetimeFormat.day) if(datetimeFormat.day < 10) else str(datetimeFormat.day),
                                hashName)
        file_name = os.path.join(file_path, hashName + '.html')
        licitacaoData['file_path'] = file_path

        return file_path, file_name


    def fornecedoresPage(self, licitacaoData):
        """ Processos realizados sobre os fornecedores,
            se a licitação estiver concluída deverá acessar o mapa comparativo
            que contém os valores e itens por fornecedor
        """
        licitacaoStatus = self.driver.find_element_by_id('ctl00_cph1_ucCab_tdStatus').text
        if(licitacaoStatus.upper() == 'CONCLUÍDO'):    
            try:
                self.driver.find_element_by_id('ctl00_cph1_btnMapa').click()    
                #self.driver.find_element_by_id('ctl00_cph1_ucCab_imbFornecedores').click() Se nao achar o btnMapa pode validar aqui os participantes
                # Tem casos que o link existe mas o sistem tem algum erro

                while(licitacaoData['licitacaoUrl'] == self.driver.current_url):
                    sleep(2)            
                
                if(len(self.driver.find_elements_by_class_name('caixa.msg_checado')) > 0):
                    raise Exception
                
                file_name = os.path.join(licitacaoData['file_path'], 'map_fornecedores.html')        
                licitacaoData['url_mapa_fornecedores'] = self.driver.current_url
                
                itens = self.driver.find_elements_by_css_selector('[src="../../../App_Themes/Curitiba/Imagem/ico_mais.gif"]')

                """
                    Licitações com grande volume de itens
                    demoram mais para abrir os fornecedores
                """     
                sleep5 = False               
                if(len(itens) > 20):
                    sleep5 = True
                
                while(len(itens) > 0):        
                    itens[0].click() 
                    if(licitacaoData['id'] == 'PE 192/2015 SMMA'): # Licitacao que contem um lote mais de 100 itens
                        sleep(10)
                    elif(sleep5):
                        sleep(5)
                    else:
                        sleep(2)
                    itens = self.driver.find_elements_by_css_selector('[src="../../../App_Themes/Curitiba/Imagem/ico_mais.gif"]')               
                

                logging.debug('Salvando mapa de fornecedores')
                file = open(file_name,'w') 
                file.write(str(self.driver.page_source))
                file.close()

                self.driver.back() 
                while(licitacaoData['url_mapa_fornecedores'] == self.driver.current_url):
                    sleep(1)           
            except:
                # O excpet ocorre dentro da p[agina]
                licitacaoData['url_mapa_fornecedores'] = self.driver.current_url 
                self.driver.back() 
                while(licitacaoData['url_mapa_fornecedores'] == self.driver.current_url):
                    sleep(1)  
            finally:
                #TODO Validar pagina == pesquisa
                self.driver.back()
                while('https://e-compras.curitiba.pr.gov.br/publico/processos/consulta/frmpesquisadetalhada.aspx' 
                        != self.driver.current_url):
                    sleep(1)


    def licitacaoPage(self, licitacaoData):
        """ Processos realizados dentro da página de licitacao """       
        file_path ,file_name = self.getFileName(licitacaoData)
        self.validateDirectory(file_path)

        file = open(file_name,'w') 
        file.write(str(self.driver.page_source))
        file.close()

        # Existem processos cancelados que não possuem fornecedores
        nFornecedores = self.driver.find_element_by_id('ctl00_cph1_ucCab_lblNumForn').text
        if(int(nFornecedores) > 0):
            self.fornecedoresPage(licitacaoData)
            self.driver.implicitly_wait(5)


    def uploadToS3(self):
        logging.info('Enviando arquivos brutos para o S3')
        files = FileController().runThroughFiles(self.folder)
        client = s3()
        for file in files:
            client.upload(file, file.replace('tmp\\data\\', '').replace('\\','/'))  

        logging.info('Arquivos enviados com sucesso!')
        

    def run(self, startPage=None, lastPage=None, inicio=None, fim=None):  
        self.uploadToS3()
        sys.exit()
        if(startPage != None):
            startPage = startPage -1 # A primeira página é 0
        else: 
            startPage = 0

        self.driver.get(self.settings.BASE_URL) # Página inicial do e-compras

        # Filtra pelas datas
        if(inicio != None and fim != None):
            inputInicio = self.driver.find_element_by_id('ctl00_cph1_txtInicio')
            inputInicio.send_keys(inicio)
            inputFim = self.driver.find_element_by_id('ctl00_cph1_txtFim')
            inputFim.send_keys(fim)


        # Ao clicar em pesquisar sem filtro irá listar todas as páginas
        element = self.driver.find_element_by_id('ctl00_cph1_btnPesquisar')
        element.click()
        sleep(1)

        # Elemento do seletor de página, o objeto é perdido com o self.driver.back
        pageSelector = self.driver.find_element_by_css_selector('[name="ctl00$cph1$gdpProcs$ctl13$ctl01"')
    
        dfPages = self.getListOfPages(pageSelector.text)

        #pageMin = dfPages['pageNumber'].min()
                
        # Inicia da página enviada por variável
        if(startPage > 0):
            pageSelector.find_element_by_css_selector('[value="{}"]'.format(startPage)).click()        
            sleep(2)

        if(lastPage == None):
            pageMax = dfPages['pageNumber'].max()
        else:
            pageMax = lastPage

        firstPage = True
        for pageNumber in range(pageMax):
            # O ID do elemento que possui a página seleciona muda se não é a primeira
            if( startPage == pageMax):
                pageSelector = self.driver.find_element_by_css_selector('[name="ctl00$cph1$gdpProcs$ctl09$ctl02"')
            elif(pageNumber > 0 or startPage > 0):                                                        
                pageSelector = self.driver.find_element_by_css_selector('[name="ctl00$cph1$gdpProcs$ctl13$ctl02"')                                                                               
            else:
                pageSelector = self.driver.find_element_by_css_selector('[name="ctl00$cph1$gdpProcs$ctl13$ctl01"')

            currentPage = pageSelector.find_element_by_css_selector('[selected="selected"').text
            logging.info('-------------------------Página Atual: ' + currentPage)

            # Percorre os 10 elementos com links para licitações
            for i in range(10):
                countWaiting = 0
                logging.debug('Licitacao: ' + str(i+1))
                licitacaoData = dict()
                buttonId = self.getButtonID(i+1) # Botão com link para a licitação
                lic = self.driver.find_element_by_id(buttonId)
                row = lic.find_element_by_xpath('..').find_element_by_xpath('..')

                # Get data from licitacao
                id = row.find_element_by_xpath('td[1]').text
                nome = row.find_element_by_xpath('td[2]').text
                status = row.find_element_by_xpath('td[3]').text
                abertura = row.find_element_by_xpath('td[4]').text
                licitacaoData.update({'id':id})
                licitacaoData.update({'nome':nome})
                licitacaoData.update({'status':status})
                licitacaoData.update({'abertura':abertura})  

                urlPesquisa = self.driver.current_url
                logging.debug(licitacaoData['id'])
                lic.click()  
                sleep(2)

                # Fix for page not changing                
                while(urlPesquisa == self.driver.current_url):
                    try:
                        lic = self.driver.find_element_by_id(buttonId)
                        lic.click() 
                    except exceptions.StaleElementReferenceException as e:
                        sleep(5)  
            
                licitacaoData.update({'licitacaoUrl':self.driver.current_url})
                self.licitacaoPage(licitacaoData) # Processos da página de licitacao     
                sleep(1)
                while(licitacaoData['licitacaoUrl'] == self.driver.current_url):
                    countWaiting = countWaiting + 1
                    logging.debug('waiting..')
                    sleep(2)                  
                    if(countWaiting == 4): 
                        self.driver.back() 
                
            if(firstPage):
                # Incrementa apartir da startPage que possui o ID do CSS correto
                nextPage = int(startPage) + 1                 
                try:
                    pageSelector = self.driver.find_element_by_css_selector('[name="ctl00$cph1$gdpProcs$ctl13$ctl01"')
                    firstPage = False 
                except Exception as e:
                    pageSelector = self.driver.find_element_by_css_selector('[name="ctl00$cph1$gdpProcs$ctl13$ctl02"')
                    firstPage = False 
            else:
                nextPage = nextPage + 1
                try:
                    pageSelector = self.driver.find_element_by_css_selector('[name="ctl00$cph1$gdpProcs$ctl13$ctl02"')
                except exceptions.NoSuchElementException:
                    pageSelector = self.driver.find_element_by_css_selector('[name="ctl00$cph1$gdpProcs$ctl13$ctl01"')

            pageSelector.find_element_by_css_selector('[value="{}"]'.format(nextPage)).click()
            sleep(5)

        self.uploadToS3()


        