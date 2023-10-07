from tkinter import messagebox
from GUI import frm_base_mov
from BLL import material_bll, mov_material_bll
from DTO import material_dto, mov_material_dto
from datetime import date
from Ferramentas import variaveis_globais


class FrmSaiMaterial(frm_base_mov.FrmBaseMov):
    def __init__(self, titulo='Saída de Materiais'):
        frm_base_mov.FrmBaseMov.__init__(self, titulo)

        self.var_msg.set('Saída')
        self.lbl_msg['fg'] = '#FF0000'

        tupla = ('Impresso', 'Imprimir', 'Retrabalho')
        self.cb_origem['values'] = tupla
        self.cb_origem.current(1)
        self.cb_destino['state'] = 'disabled'
        self.btn_confirmar['command']=self.confirmar


    def confirmar(self):
        # Objeto movimetação de material
        obj_mov = mov_material_dto.MovMaterialDto()
        obj_mov.material = int(self.var_id.get())
        obj_mov.origem = self.var_origem.get()
        obj_mov.destino = 'Externo'
        obj_mov.tipo = 'Saída'
        obj_mov.usuario = variaveis_globais.usu_id
        obj_mov.qtd = self.var_qtd.get()
        obj_mov.data = date.today()

        bll_mov = mov_material_bll.MovMaterialBll()

        if self.var_origem.get() == 'Imprimir':
            val = self.var_imprimir.get()
        elif self.var_origem.get() == 'Impresso':
            val = self.var_impresso.get()
        else:
            val = self.var_retrabalho.get()

        validar = bll_mov.validar_campos(obj_mov, val)
        if validar != 'ok':
            messagebox.showwarning('Aviso', str(validar), parent=self)
            return

        res = messagebox.askquestion('Confirmar', 'Deseja confirmar esta movimentação?', parent=self)
        if res == 'yes':
            
            if self.var_origem.get() == 'Imprimir':
                self.var_imprimir.set((self.var_imprimir.get() - self.var_qtd.get()))
            elif self.var_origem.get() == 'Impresso':
                self.var_impresso.set((self.var_impresso.get() - self.var_qtd.get()))
            else:
                self.var_retrabalho.set((self.var_retrabalho.get() - self.var_qtd.get()))

            self.var_saldo.set((self.var_saldo.get() - self.var_qtd.get()))
            # Objeto material
            obj_mat = material_dto.MaterialDto()
            obj_mat.ID = int(self.var_id.get())
            obj_mat.qtd_retrabalho = self.var_retrabalho.get()
            obj_mat.qtd_imprimir = self.var_imprimir.get()
            obj_mat.qtd_impresso = self.var_impresso.get()
            obj_mat.saldo = self.var_saldo.get()

            bll_mat = material_bll.MaterialBll()
            r = bll_mat.mov_material(obj_mat)
            if r == 1:
                print('Atualizado material')
                s = bll_mov.inserir(obj_mov)
                if s == 1:
                    self.var_qtd.set(0)
                    self.txt_busca.focus()
                    messagebox.showinfo('Confirmado', 'Movimentação confirmada com suecesso!', parent=self)
                else:
                    messagebox.showerror('Erro', str(s), parent=self)
                    return
            else:
                messagebox.showerror('Erro', str(r), parent=self)
                return
