from DAL import data_base


class KitDal:
    def __init__(self):
        self.db = data_base.DataBase()

    def inserir(self, obj):
        sql = 'INSERT INTO tb_kit (kit_codigo, material_id, kit_descricao) VALUES (?,?,?)'
        return self.db.executar(sql, (obj.codigo, obj.material, obj.descricao), True)

    def editar(self, obj):
        sql = 'UPDATE tb_kit SET kit_codigo=?, material_id=?, kit_descricao=? WHERE kit_id=?'
        return self.db.executar(sql, (obj.codigo, obj.material, obj.descricao, obj.ID), True)
    
    def excluir(self, ID):
        return self.db.executar('DELETE FROM tb_kit WHERE kit_id=?', (ID,), True)
    
    def retornar_dados(self, tipo, prms=None):
        sql = '''SELECT kit_id, kit_codigo, tb_material.mat_codigo, tb_material.mat_descricao, kit_descricao FROM tb_kit 
                 INNER JOIN tb_material ON (tb_kit.material_id=tb_material.mat_id)'''

        if tipo == 'id':
            sql = sql + ' WHERE kit_id=?'
            prms = (prms,)
        elif tipo == 'codigo':
            sql = sql + ' WHERE kit_codigo=?'
            prms = (prms,)
        elif tipo == 'codigo%':
            sql = sql + ' WHERE kit_codigo LIKE ? ORDER BY kit_codigo'
            prms = (prms,)
        elif tipo == 'descricao':
            sql = sql + ' WHERE kit_descricao LIKE ? ORDER BY kit_codigo'
            prms = (prms,)
        elif tipo == 'material':
            sql = sql + ' WHERE tb_material.mat_codigo LIKE ? ORDER BY kit_codigo'
            prms = (prms,)
        else:
            sql = sql + ' ORDER BY kit_codigo'

        return self.db.executar(sql, prms)
