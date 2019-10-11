class Licitacao():
     def __init__(self, folder=None, id=None, empresa=None, status=None,
         setor_de_compras=None, objeto=None, responsavel=None, abertura_propostas=None,
         encerramento_propostas = None,inicio_sessao = None,encerramento_sessao=None,
         n_fornecedores=None, n_me_epp=None, n_propostas_validas=None, n_recusas=None):
         self.folder = folder
         self.id = id
         self.empresa = empresa
         self.status = status
         self.setor_de_compras = setor_de_compras
         self.objeto = objeto
         self.responsavel  = responsavel
         self.abertura_propostas = abertura_propostas
         self.encerramento_propostas = encerramento_propostas
         self.inicio_sessao = inicio_sessao
         self.encerramento_sessao = encerramento_sessao
         self.n_fornecedores = n_fornecedores
         self.n_me_epp = n_me_epp
         self.n_propostas_validas = n_propostas_validas
         self.n_recusas = n_recusas         
         
     def toObject(self):
          return self.folder,self.id,self.empresa, self.status,self.objeto, self.setor_de_compras,self.responsavel,self.abertura_propostas,self.encerramento_propostas, self.inicio_sessao,self.encerramento_sessao, self.n_fornecedores,self.n_me_epp, self.n_propostas_validas, self.n_recusas


     def toStringLicitacao(self):
          return (
               'Folder: {folder}\n' +
               'Id: {id}\n' +
               'Empresa: {empresa}\n' +
               'Status: {status}\n' +
               'Setor de Compras: {setor_de_compras}\n' +
               'Objeto: {objeto}\n' +
               'Responsavel: {responsavel}\n' +
               'Abertura das Propostas: {abertura_propostas}\n' +
               'Encerramento das Propotas: {encerramento_propostas}\n' +
               'Inicio Sessao: {inicio_sessao}\n' +
               'Encerramento Sessao: {encerramento_sessao}\n' +
               'Quantidade de fornecedores: {n_fornecedores}\n' +
               'Quantidade de ME/EPP: {n_me_epp}\n' +
               'Quantidade de Propostas Validas: {n_propostas_validas}\n' +
               'Quantidade de Recisas: {n_recusas}'
          ).format(
               folder=self.folder,
               id=self.id,
               empresa=self.empresa,
               status=self.status,
               setor_de_compras=self.setor_de_compras,
               objeto=self.objeto,
               responsavel=self.responsavel,
               abertura_propostas=self.abertura_propostas,
               encerramento_propostas=self.encerramento_propostas,
               inicio_sessao=self.inicio_sessao,
               encerramento_sessao=self.encerramento_sessao,
               n_fornecedores=self.n_fornecedores,
               n_me_epp=self.n_me_epp,
               n_propostas_validas=self.n_propostas_validas,
               n_recusas=self.n_recusas               
          )
