from DAL import data_base


class MaterialDal:
    def __init__(self):
        self.db = data_base.DataBase()

    def inserir(self, obj):
        query = 'INSERT INTO tb_material (mat_codigo, tip_material_id, mat_descricao, mat_obs) VALUES (?,?,?,?)'
        return self.db.executar(query, (obj.codigo, obj.tipo, obj.descricao, obj.obs), True)

    def editar(self, obj):
        query = 'UPDATE tb_material SET mat_codigo=?, tip_material_id=?, mat_descricao=?, mat_obs=? WHERE mat_id=?'
        return self.db.executar(query, (obj.codigo, obj.tipo, obj.descricao, obj.obs, obj.ID), True)

    def mov_material(self, obj):
        query = 'UPDATE tb_material SET mat_retrabalho=?, mat_impresso=?, mat_imprimir=?, mat_saldo=? WHERE mat_id=?'
        return self.db.executar(query, (obj.qtd_retrabalho, obj.qtd_impresso, obj.qtd_imprimir, obj.saldo, obj.ID), True)

    def excluir(self, ID):
        return self.db.executar('DELETE FROM tb_material WHERE mat_id=?', (ID,), True)

    def retornar_dados(self, tipo, prms=None):
        query = '''SELECT mat_id, mat_codigo, tb_tip_material.tip_descricao, mat_descricao, mat_retrabalho, mat_impresso, mat_imprimir, mat_saldo, mat_obs FROM tb_material 
                   INNER JOIN tb_tip_material ON (tb_material.tip_material_id=tb_tip_material.tip_id)'''
        
        if tipo == 'id':
            query = query + ' WHERE mat_id=?'
            prms = (prms,)
        elif tipo == 'codigo':
            query = query + ' WHERE mat_codigo=?'
            prms = (prms,)
        elif tipo == 'codigo%':
            query = query + ' WHERE mat_codigo LIKE ? ORDER BY mat_codigo'
            prms = (prms,)
        elif tipo == 'descricao':
            query = query + ' WHERE mat_descricao LIKE ? ORDER BY mat_codigo'
            prms = (prms,)
        elif tipo == 'tipo':
            query = query + ' WHERE tb_tip_material.tip_descricao LIKE ? ORDER BY mat_codigo'
            prms = (prms,)
        else:
            query = query + " ORDER BY mat_codigo"
        
        return self.db.executar(query, prms)
        