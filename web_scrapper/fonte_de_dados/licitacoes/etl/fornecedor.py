from etl.item import Item
import csv
import os

class Fornecedor(Item):
    def __init___(self,licitacao=None,item=None
                    ,statusFornecedor=None,nomeFornecedor=None
                    ,marcaModelo=None,valorUnidade=None
                    ,quantidade=None,valorTotal=None,dataHora=None):
        if(licitacao != None and item != None):
            super().__init__(licitacao,item[0],item[1])
        self.statusFornecedor = None
        self.nomeFornecedor = None
        self.marcaModelo = None
        self.valorUnidade = None
        self.quantidade = None
        self.valorTotal = None
        self.dataHora = None


    def toString(self):
        return (
            str(self.toStringLicitacao()) +
            str(self.toStringItem()) +
            'statusFornecedor: {statusFornecedor}\n' +
            'Nome Fornecedor: {nomeFornecedor}\n' +
            'Marca / Modelo: {marcaModelo}\n' +
            'Valor Unidade: {valorUnidade}\n' +
            'Quantidade: {quantidade}\n' +
            'Valor Total: {valorTotal}\n' +
            'Data Hora: {dataHora}' 
        ).format(
            statusFornecedor=self.statusFornecedor,
            nomeFornecedor=self.nomeFornecedor,
            marcaModelo=self.marcaModelo,
            valorUnidade=self.valorUnidade,
            quantidade=self.quantidade,
            valorTotal=self.valorTotal,
            dataHora=self.dataHora              
          )
    

    def toCsv(self,filepath=None):
        if(not os.path.exists(filepath)):
            with open(filepath, mode='w') as fornecedores:
                columns = [
                    'folder',
                    'id',
                    'empresa',
                    'status',
                    'setor_de_compras',
                    'objeto',
                    'responsavel',
                    'abertura_propostas',
                    'encerramento_propostas',
                    'inicio_sessao',
                    'encerramento_sessao',
                    'n_fornecedores',
                    'n_me_epp',
                    'n_propostas_validas',
                    'n_recusas',
                    'seq_item',
                    'nomeItem',
                    'statusFornecedor',
                    'nomeFornecedor',
                    'marcaModelo',
                    'valorUnidade',
                    'quantidade',
                    'valorTotal',
                    'dataHora'
                ]
                fornecedores_writer = csv.DictWriter(fornecedores,fieldnames=columns,delimiter=';')
                fornecedores_writer.writeheader()                    

        with open(filepath, mode='a',newline='') as fornecedores:
            fornecedores_writer = csv.writer(fornecedores, delimiter=';', quotechar='"')            
            fornecedores_writer.writerow([
                self.folder,
                self.id, 
                self.empresa,
                self.status,
                self.setor_de_compras,
                self.objeto,
                self.responsavel,
                self.abertura_propostas,
                self.encerramento_propostas,
                self.inicio_sessao,
                self.encerramento_sessao,
                self.n_fornecedores,
                self.n_me_epp,
                self.n_propostas_validas,
                self.n_recusas,
                self.seq_item,
                self.nomeItem,
                self.statusFornecedor,
                self.nomeFornecedor,
                self.marcaModelo,
                self.valorUnidade,
                self.quantidade,
                self.valorTotal,
                self.dataHora                   
            ])