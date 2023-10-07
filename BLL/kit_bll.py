from DAL import kit_dal


class KitBll:
    def __init__(self):
        self.dal = kit_dal.KitDal()

    def validar_campos(self, obj):
        r = 'ok'
        if len(obj.codigo) < 6:
            r = Exception('O campo código, deve conter seis(6) números!')
        elif obj.descricao == '':
            r = Exception('O campo descrição, é de preenchimento obrigatório!')
        return r

    def inserir(self, obj):
        return self.dal.inserir(obj)

    def editar(self, obj):
        return self.dal.editar(obj)

    def excluir(self, ID):
        return self.dal.excluir(ID)

    def retornar_dados(self, tipo, prms=None):
        return self.dal.retornar_dados(tipo, prms)    
