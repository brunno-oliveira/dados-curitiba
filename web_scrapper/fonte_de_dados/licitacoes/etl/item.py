from etl.licitacao import Licitacao

class Item(Licitacao):
    def __init__(self,licitacao,item=None):
        super().__init__(
                licitacao[0],
                licitacao[1],
                licitacao[2],
                licitacao[3],
                licitacao[4],
                licitacao[5],
                licitacao[6],
                licitacao[7],
                licitacao[8],
                licitacao[9],
                licitacao[10],
                licitacao[11],
                licitacao[12],
                licitacao[13],
                licitacao[14])
        if(item != None):
            self.seq_item = item[0]
            self.nomeItem = item[1]
        else:
            self.seq_item = None
            self.nomeItem = None

    def toObject(self):
        licitacao = self.folder,self.id,self.empresa, self.status,self.objeto, self.setor_de_compras,self.responsavel,self.abertura_propostas,self.encerramento_propostas, self.inicio_sessao,self.encerramento_sessao, self.n_fornecedores,self.n_me_epp, self.n_propostas_validas, self.n_recusas
        item =  self.seq_item, self.nomeItem
        return licitacao, item


    def toStringItem(self):
        return (
            'Squencia Item: {seq_item}\n' +
            'Nome: {nomeItem}'
        ).format(
            seq_item=self.seq_item,
            nomeItem=self.nomeItem           
          )