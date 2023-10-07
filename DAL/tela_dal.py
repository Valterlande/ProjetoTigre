from DAL import data_base


class TelaDal:
    def __init__(self):
        self.db = data_base.DataBase()

    def inserir(self, obj):
        sql = 'INSERT INTO tb_tela (tip_material_id, mod_produto_id, tel_descricao, tel_prateleira, tel_obs) VALUES (?,?,?,?,?)'
        return self.db.executar(sql, (obj.tipo, obj.modelo, obj.descricao, obj.prateleira, obj.obs), True)

    def editar(self, obj):
        sql = 'UPDATE tb_tela SET tip_material_id=?, mod_produto_id=?, tel_descricao=?, tel_prateleira=?, tel_obs=? WHERE tel_id=?'
        return self.db.executar(sql, (obj.tipo, obj.modelo, obj.descricao, obj.prateleira, obj.obs, obj.ID), True)

    def excluir(self, ID):
        sql = 'DELETE FROM tb_tela WHERE tel_id=?'
        return self.db.executar(sql, (ID,), True)

    def retornar_dados(self, tipo, prms=None):
        sql = '''SELECT tel_id, tb_tip_material.tip_descricao, tb_mod_produto.mod_descricao, tel_descricao, tel_prateleira, tel_obs FROM tb_tela 
                 INNER JOIN tb_tip_material ON (tb_tela.tip_material_id=tb_tip_material.tip_id) 
                 INNER JOIN tb_mod_produto ON (tb_tela.mod_produto_id=tb_mod_produto.mod_id)'''

        if tipo == 'id':
            sql = sql + ' WHERE tel_id=?'
            prms = (prms,)
        elif tipo == 'descricao':
            sql = sql + ' WHERE tel_descricao LIKE ? ORDER BY tel_descricao'
            prms = (prms,)
        elif tipo == 'tipo+modelo+descricao':
            sql = sql + ' WHERE tb_tip_material.tip_descricao LIKE ? AND tb_mod_produto.mod_descricao LIKE ? AND tel_descricao LIKE ? ORDER BY tel_descricao'
            
        return self.db.executar(sql, prms)
