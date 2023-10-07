from DAL import tip_material_dal


class TipMaterialBll:
    def __init__(self):
        self.dal = tip_material_dal.TipMaterialDal()

    def validar_campo(self, obj):
        r = 'OK'
        if len(obj.descricao) < 1:
            r = Exception('O campo descrição é de preenchimento obrigatório')
        return r 

    def inserir(self, obj):
        return self.dal.inserir(obj)
    
    def editar(self, obj):
        return self.dal.editar(obj)

    def excluir(self, ID):
        return self.dal.excluir(ID)

    def retornar_dados(self, tipo, prms=None):
        return self.dal.retornar_dados(tipo, prms)
    