from common.settings import Settings
import logging
import os

class FileController:
    def __init__(self):
        self.settings = Settings()


    def validateDirectory(self, filepath):    
        if not os.path.exists(filepath):
            try:
                os.makedirs(filepath)
            except Exception as e:
                logging.error('ERRO while creating path: {} \n Error: {}'.format(filepath,e))

    
    def validateDataFolders(self):
        logging.info('Validando diretórios..')
        arr = []
        arr.append(self.settings.RAW_FOLDER)
        arr.append(self.settings.STAGE_FOLDER)
        arr.append(self.settings.TEST_RAW_FOLDER)
        arr.append(self.settings.TEST_STAGE_FOLDER)

        for folder in arr:
            self.validateDirectory(folder)


    def runThroughFiles(self, folder):
        logging.info('Gerando lista de arquivos')
        files = []
        for year in os.listdir(folder):
            yearFolder = os.path.join(folder, year)

            for month in os.listdir(yearFolder):
                logging.debug('-----YEAR: ' + str(year))
                monthFolder = os.path.join(yearFolder, month)

                for day in os.listdir(monthFolder):
                    logging.debug('----MONTH: ' + str(month))
                    dayFolder = os.path.join(monthFolder, day)

                    for licitacao in os.listdir(dayFolder):
                        licitacaoFolder = os.path.join(dayFolder, licitacao)

                        for file in os.listdir(licitacaoFolder):     
                            filepath = os.path.join(licitacaoFolder, file)          
                            files.append(filepath)
        return files
          