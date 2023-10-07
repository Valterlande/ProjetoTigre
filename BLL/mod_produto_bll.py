from DAL import mod_produto_dal


class ModProdutoBll:
    def __init__(self):
        self.dal = mod_produto_dal.ModProdutoDal()

    def validar_campo(self, obj):
        r = 's'
        if obj.descricao == '':
            r = Exception('O campo descrição é de preenchimento obrigatório.')
        return r 

    def inserir(self, obj):
        return self.dal.inserir(obj)

    def editar(self, obj):
        return self.dal.editar(obj)

    def excluir(self, ID):
        return self.dal.excluir(ID)

    def retornar_dados(self, tipo, prms=None):
        return self.dal.retonar_dados(tipo, prms)
        