from etl.fornecedor import Fornecedor
from etl.licitacao import Licitacao
from etl.item import Item
import logging
import re

class MapaFornecedores:
    def __init__(self, licitacao, path_csv):
        self.path_csv = path_csv
        self.licitacao = licitacao


    def getItemSequence(self, item):
        """ Retorna a sequencia do item, ex
                                    Seq. Item 18 -
        """
        prefix = re.findall('.*Item ', item)
        # Nomenclatura diferente de Item
        if(len(prefix) == 0): 
            prefix = re.findall('.*Lote ', item)

        item = item.replace(prefix[0],'')
        sufix = re.findall('.* -',item)
        if(len(sufix) == 0):
            sufix = re.findall('.*\\n',item)         
            
        seqId = sufix[0]
        seqIdSufix = re.findall(' -',seqId)
        if(len(seqIdSufix) == 0):
            seqIdSufix = re.findall('\n',seqId)
        return seqId.replace(seqIdSufix[0],'')


    def getMapaFornecedores(self,filepath):
        f = open(filepath, "r")
        text = f.readlines()
        insideTableLances = False # Flag para identificar que está dentro da tabela
        isCabecalho = False # Identifica que é um cabeçalho de item
        isSeq = False # Identifica que sequecia de item
        fornecedor = None
        for line in text:
            if(line.find('id="ctl00_cph1_tlvLances"') > 0):
                  insideTableLances = True

            elif(insideTableLances):
                if(line.find('linha_cabecalho') > 0):
                    """
                        As Proximas linhas sao referente ao cabecalho do item. Ex>
                        <tr class="linha_cabecalho">
                        <td style="background-color:Transparent;"></td><td style="width:32px;"><input type="image" name="ctl00$cph1$tlvLances$ctl02$ctl00" src="../../../App_Themes/Curitiba/Imagem/ico_menos.gif"></td><td colspan="2">                            
                            Seq. Item 1 - 
                            BEBIDA LÁCTEA, fermentada, sabor coco, com leite pasteurizado ou reconstituído, integral ou parcialmente desnatado, açúcar ou xarope de açúcar, preparado de coco, fermento lácteo, embalagem plástica com 900 a 1.000ml.                            
                        </td>
                        </tr>
                    """
                    item = Item(self.licitacao.toObject())     
                    isCabecalho = True
                    continue

                elif(isCabecalho):
                    if(isSeq):
                        """ Se a leitura anterior for foi a sequencia do item,
                            a seguinte será o nome do item """
                        isSeq = False                                                   
                        itemName = line.strip()
                        item.nomeItem = itemName            
                    elif(line.find('Seq') > 0):   
                        # Item sequence
                        isSeq = True
                        itemSequencia = self.getItemSequence(line.strip())
                        item.seq_item = itemSequencia
                    elif(line.find('</tr>') > 0):   
                        isCabecalho = False          
                                       
                elif(line.find('alt="Ganhador"') > 0 or line.find('alt="Perdedor"') > 0):
                    """ Primeiro registo de um fornecedor,
                        sempre que executar essa linha será um novo registro """
                    if(fornecedor):
                        fornecedor.toCsv(self.path_csv)

                    a,b = item.toObject()
                    fornecedor = Fornecedor(a,b)  
                    if(line.find('alt="Perdedor"') > 0):
                        fornecedor.statusFornecedor = 'Perdedor'
                    elif(line.find('alt="Ganhador"') > 0):
                        fornecedor.statusFornecedor = 'Ganhador'
                    else:
                        fornecedor.statusFornecedor = 'STATUS ERRO'

                elif(line.find('Fornecedor:') > 0):
                    """ <p class="pDDU"><b>Fornecedor:</b>CWB WORD S COMERCIO E SERVIÇOS LTDA - EPP</p> """
                    nomeFornecedor = line.strip()
                    prefix = re.findall('.*Fornecedor:</b>',nomeFornecedor)
                    nomeFornecedor = nomeFornecedor.replace(prefix[0],'')
                    sufix = re.findall('</p>.*',nomeFornecedor)
                    nomeFornecedor = nomeFornecedor.replace(sufix[0], '')
                    fornecedor.nomeFornecedor = nomeFornecedor

                elif(line.find('Marca/Modelo') > 0):
                    """ <p class="pDDU"><b>Marca/Modelo:</b>FORPLAS/DUPLA EXTENSIVEL</p> """
                    marcaModelo = line.strip()
                    prefix = re.findall('.*Modelo:</b>',marcaModelo)
                    marcaModelo = marcaModelo.replace(prefix[0],'')
                    sufix = re.findall('</p>.*',marcaModelo)
                    marcaModelo = marcaModelo.replace(sufix[0], '')
                    fornecedor.marcaModelo = marcaModelo

                elif(line.find('<b>Valor Lance:</b>') > 0):
                    """ <p id="ctl00_cph1_tlvLances_ctl03_lance" class="pDDU"><b>Valor Lance:</b>R$3,8000</p> """
                    valorUnidade = line.strip()
                    prefix = re.findall('.*Valor Lance:</b>R\$',valorUnidade)
                    valorUnidade = valorUnidade.replace(prefix[0],'')
                    sufix = re.findall('</p>.*',valorUnidade)
                    valorUnidade = valorUnidade.replace(sufix[0], '')
                    valorUnidade = valorUnidade.replace('.','')
                    fornecedor.valorUnidade = valorUnidade                   

                elif(line.find('Quantidade:</b>') > 0):
                    """ <p class="pDDU"><b>Quantidade:</b>5500</p> """
                    quantidade = line.strip()
                    prefix = re.findall('.*Quantidade:</b>',quantidade)
                    quantidade = quantidade.replace(prefix[0],'')
                    sufix = re.findall('</p>.*',quantidade)
                    quantidade = quantidade.replace(sufix[0], '')      
                    fornecedor.quantidade = quantidade

                elif(line.find('Valor Total Lance:</b') > 0):
                    """ <p id="ctl00_cph1_tlvLances_ctl03_lanceTotal" class="pDDU"><b>Valor Total Lance:</b>R$20.900,0000</p> """
                    valorTotal = line.strip()
                    prefix = re.findall('.*Valor Total Lance:</b>R\$',valorTotal)
                    valorTotal = valorTotal.replace(prefix[0],'')
                    sufix = re.findall('</p>.*',valorTotal)
                    valorTotal = valorTotal.replace(sufix[0], '')          
                    valorTotal = valorTotal.replace('.','')  
                    fornecedor.valorTotal = valorTotal 

                elif(line.find('Data/Hora Lance: </b>') > 0):
                    """ <p class="pDDU"><b>Data/Hora Lance: </b>05/04/2017 10:32:29.833 """
                    dataHora = line.strip()
                    prefix = re.findall('.*Data/Hora Lance: </b>',dataHora)
                    dataHora = dataHora.replace(prefix[0],'')    
                    fornecedor.dataHora = dataHora
                   
                elif(line.find('</table>') > 0):
                    insideTableLances = False        