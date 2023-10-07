from DAL import mov_material_dal


class MovMaterialBll:
    def __init__(self):
        self.dal = mov_material_dal.MovMaterialDal()

    def validar_campos(self, obj, val=0):
        r = 'ok'
        if obj.tipo == 'Saída' or obj.tipo == 'Transferência':
            if obj.qtd > val:
                r = Exception('Inválido!\nA qtde. de movimentação, não pode ser maior que a qtde. no estoque ('+obj.origem+').')
        if obj.qtd < 1:
            r = Exception('O campo qtde., deve conter um valor maior que zero(0)!')
        return r

    def inserir(self, obj):
        return self.dal.inserir(obj)

    def retornar_dados(self, tipo, prms=None):
        return self.dal.retornar_dados(tipo, prms)
        