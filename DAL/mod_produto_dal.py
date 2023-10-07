from DAL import data_base


class ModProdutoDal:
    def __init__(self):
        self.db = data_base.DataBase()

    def inserir(self, obj):
        sql = 'INSERT INTO tb_mod_produto (tip_material_id, mod_descricao) VALUES (?,?)'
        return self.db.executar(sql, (obj.tipo, obj.descricao), True)

    def editar(self, obj):
        sql = 'UPDATE tb_mod_produto SET tip_material_id=?, mod_descricao=? WHERE mod_id=?'
        return self.db.executar(sql, (obj.tipo, obj.descricao, obj.ID), True)

    def excluir(self, ID):
        sql = 'DELETE FROM tb_mod_produto WHERE mod_id=?'
        return self.db.executar(sql, (ID,), True)

    def retonar_dados(self, tipo, prms=None):
        sql = '''SELECT mod_id, tb_tip_material.tip_descricao, mod_descricao FROM tb_mod_produto 
                 INNER JOIN tb_tip_material ON (tb_mod_produto.tip_material_id=tb_tip_material.tip_id)'''

        if tipo == 'id':
            sql = sql + ' WHERE mod_id=?'
            prms = (prms,)
        elif tipo == 'tipo':
            sql = sql + ' WHERE tb_tip_material.tip_descricao=? ORDER BY mod_descricao'
            prms = (prms,)
        else:
            sql = sql + ' ORDER BY mod_descricao'
            
        
        return self.db.executar(sql, prms)
        