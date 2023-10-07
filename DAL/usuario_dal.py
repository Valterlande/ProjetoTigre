from DAL import data_base


class UsuarioDal:
    def __init__(self):
        self.db = data_base.DataBase()

    def inserir(self, obj):
        query = 'INSERT INTO tb_usuario (usu_nome, usu_usuario, usu_senha, usu_acesso) VALUES (?,?,?,?)'
        return self.db.executar(query, (obj.nome, obj.usuario, obj.senha, obj.acesso), True)

    def editar(self, obj):
        query = 'UPDATE tb_usuario SET usu_nome=?, usu_usuario=?, usu_senha=?, usu_acesso=? WHERE usu_id=?'
        return self.db.executar(query, (obj.nome, obj.usuario, obj.senha, obj.acesso, obj.ID), True)

    def excluir(self, ID):
        return self.db.executar('DELETE FROM tb_usuario WHERE usu_id=?', (ID,), True)

    def retornar_dados(self, tipo, prms=None):
        query = 'SELECT usu_id, usu_nome, usu_usuario, usu_senha, usu_acesso FROM tb_usuario'

        if tipo == 'id':
            query = query + ' WHERE usu_id=?'
            prms = (prms,)
        elif tipo == 'usuario':
            query = query + ' WHERE usu_usuario LIKE ?'
            prms = (prms,)
        elif tipo == 'usuario+senha':
            query = query + ' WHERE usu_usuario=? AND usu_senha=?'
        else:
            query = query + ' ORDER BY usu_usuario'

        return self.db.executar(query, prms)
        