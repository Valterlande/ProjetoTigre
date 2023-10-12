from DAL import tela_dal


class TelaBll:
    def __init__(self):
        self.dal = tela_dal.TelaDal()

    def validar_campos(self, obj):
        r = 'ok'
        if obj.descricao == '':
            r = Exception('O campo descrição é de preenchimento obrigatório!')
        elif len(obj.prateleira) < 6:
            r = Exception('O campo prateleira deve conter no mínimo seis(6) caracteres!')
        return r 

    def inserir(self, obj):
        return self.dal.inserir(obj)

    def editar(self, obj):
        return self.dal.editar(obj)

    def excluir(self, ID):
        return self.dal.excluir(ID)

    def retornar_dados(self, tipo, prms=None):
        return self.dal.retornar_dados(tipo, prms)
