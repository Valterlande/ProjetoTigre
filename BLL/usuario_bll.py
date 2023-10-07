from DAL import usuario_dal


class UsuarioBll:
    def __init__(self):
        self.dal = usuario_dal.UsuarioDal()

    def validar_campos(self, obj):
        r = 'ok'
        if obj.nome == '':
            r = Exception('O campo nome, é de preenchimento obrigatório!')
        elif len(obj.usuario) < 4:
            r = Exception('O campo usuário, deve conter no mínimo quatro"4" caracteres!')
        elif len(obj.senha) < 4:
            r = Exception('O campo senha, deve conter no mínimo quatro"4" caracteres!')
        return r 

    def inserir(self, obj):
        return self.dal.inserir(obj)
    
    def editar(self, obj):
        return self.dal.editar(obj)

    def excluir(self, ID):
        return self.dal.excluir(ID)

    def retornar_dados(self, tipo, prms=None):
        return self.dal.retornar_dados(tipo, prms)
        