from DAL import data_base


class MovMaterialDal:
    def __init__(self):
        self.db = data_base.DataBase()

    def inserir(self, obj):
        query = 'INSERT INTO tb_mov_material (material_id, usuario_id, mov_tipo, mov_origem, mov_destino, mov_qtd, mov_data) VALUES (?,?,?,?,?,?,?)'
        return self.db.executar(query, (obj.material, obj.usuario, obj.tipo, obj.origem, obj.destino, obj.qtd, obj.data), True)

    def retornar_dados(self, tipo, prms=None):
        query = '''SELECT mov_id, tb_material.mat_codigo, tb_material.mat_descricao, mov_tipo, mov_origem, mov_destino, mov_qtd, mov_data, tb_usuario.usu_usuario FROM tb_mov_material 
                   INNER JOIN tb_material ON (tb_mov_material.material_id=tb_material.mat_id) 
                   INNER JOIN tb_usuario ON (tb_mov_material.usuario_id=tb_usuario.usu_id)'''

        if tipo == 'mat+tip+ori+des+usu':
            query = query + ' WHERE tb_material.mat_codigo LIKE ? AND mov_tipo LIKE ? AND mov_origem LIKE ? AND mov_destino LIKE ? AND tb_usuario.usu_usuario LIKE ?'
        elif tipo == 'dat+mat+tip+ori+des+usu':
            query = query + ' WHERE mov_data BETWEEN ? AND ? AND tb_material.mat_codigo LIKE ? AND mov_tipo LIKE ? AND mov_origem LIKE ? AND mov_destino LIKE ? AND tb_usuario.usu_usuario LIKE ?'
        elif tipo == 'dat+tip':
            query = query + ' WHERE mov_data BETWEEN ? AND ? AND mov_tipo LIKE ?'

        return self.db.executar(query, prms)