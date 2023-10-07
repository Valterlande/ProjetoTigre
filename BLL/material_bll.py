from DAL import material_dal


class MaterialBll:
    def __init__(self):
        self.dal = material_dal.MaterialDal()

    def validar_campos(self, obj):
        r = 'ok'
        if len(obj.codigo) < 6:
            r = Exception('O Campo código deve conter seis(6) números!')
        elif obj.descricao == '':
            r = Exception('O campo descrição, é de preenchimento obrigatório!')
        return r

    def inserir(self, obj):
        return self.dal.inserir(obj)

    def editar(self, obj):
        return self.dal.editar(obj)

    def mov_material(self, obj):
        return self.dal.mov_material(obj)

    def excluir(self, ID):
        return self.dal.excluir(ID)

    def retornar(self):
        return self.dal.retornar()

    def retornar_dados(self, tipo, prms=None):
        return self.dal.retornar_dados(tipo, prms)