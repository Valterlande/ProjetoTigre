from DAL import data_base


class TipMaterialDal:
    def __init__(self):
        self.db = data_base.DataBase()

    def inserir(self, obj):
        return self.db.executar('INSERT INTO tb_tip_material (tip_descricao) VALUES (?)', (obj.descricao,), True)
    
    def editar(self, obj):
        return self.db.executar('UPDATE tb_tip_material SET tip_descricao=? WHERE tip_id=?', (obj.descricao, obj.ID), True)

    def excluir(self, ID):
        return self.db.executar('DELETE FROM tb_tip_material WHERE tip_id=?', (ID,), True)

    def retornar_dados(self, tipo, prms=None):
        sql = 'SELECT tip_id, tip_descricao FROM tb_tip_material'

        if tipo == 'id':
            sql = sql + ' WHERE tip_id=?'
            prms = (prms,)
        else:
            sql = sql + ' ORDER BY tip_descricao'
        
        return self.db.executar(sql, prms)
