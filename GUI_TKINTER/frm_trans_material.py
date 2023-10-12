from tkinter import messagebox
from GUI_TKINTER import frm_base_mov
from BLL import material_bll, mov_material_bll
from DTO import material_dto, mov_material_dto
from datetime import date
from Ferramentas import variaveis_globais


class FrmTransMaterial(frm_base_mov.FrmBaseMov):
    def __init__(self, titulo='Transferência de Materiais'):
        frm_base_mov.FrmBaseMov.__init__(self, titulo)

        self.var_msg.set('Transferência')
        self.lbl_msg['fg'] = '#008000'

        tupla = ('Impresso', 'Imprimir')
        self.cb_origem['values'] = tupla
        self.cb_origem.current(1)
        self.cb_origem.bind('<<ComboboxSelected>>', self.carregar_destino)

        self.carregar_destino()

        self.btn_confirmar['command']=self.confirmar

    def carregar_destino(self, event=None):
        if self.var_origem.get() == 'Impresso':
            tupla = ('Retrabalho')
        elif self.var_origem.get() == 'Imprimir':
            tupla = ('Impresso', 'Retrabalho')

        self.cb_destino['values'] = tupla
        self.cb_destino.current(0)

    def confirmar(self):
        # Objeto movimetação de material
        obj_mov = mov_material_dto.MovMaterialDto()
        obj_mov.material = int(self.var_id.get())
        obj_mov.origem = self.var_origem.get()
        obj_mov.destino = self.var_destino.get()
        obj_mov.tipo = 'Transferência'
        obj_mov.usuario = variaveis_globais.usu_id
        obj_mov.qtd = self.var_qtd.get()
        obj_mov.data = date.today()

        bll_mov = mov_material_bll.MovMaterialBll()

        if self.var_origem.get() == 'Imprimir':
            val = self.var_imprimir.get()
        else:
            val = self.var_impresso.get()

        validar = bll_mov.validar_campos(obj_mov, val)
        if validar != 'ok':
            messagebox.showwarning('Aviso', str(validar), parent=self)
            return

        res = messagebox.askquestion('Confirmar', 'Deseja confirmar esta movimentação?', parent=self)
        if res == 'yes':
            if self.var_origem.get() == 'Imprimir':
                self.var_imprimir.set((self.var_imprimir.get() - self.var_qtd.get()))
                if self.var_destino.get() == 'Impresso':
                    self.var_impresso.set((self.var_impresso.get() + self.var_qtd.get()))
                else:
                    self.var_retrabalho.set((self.var_retrabalho.get() + self.var_qtd.get()))
            else:
                self.var_impresso.set((self.var_impresso.get() - self.var_qtd.get()))
                self.var_retrabalho.set((self.var_retrabalho.get() + self.var_qtd.get()))

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
