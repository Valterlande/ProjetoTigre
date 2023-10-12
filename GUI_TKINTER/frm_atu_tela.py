from tkinter import *
from tkinter import messagebox, ttk
from BLL import mod_produto_bll, tip_material_bll, tela_bll
from DTO import tela_dto
import random


class FrmAtuTela(Toplevel):
    def __init__(self, lst):
        Toplevel.__init__(self)

        w = 610
        h = 320
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title('Edição de Tela')
        self.resizable(False, False)
        self.grab_set()

        self.dic_tipo = {}
        self.dic_modelo = {}

        self.criar_widgets()
        self.carregar_tipos()
        self.carregar_modelos()

        self.preencher_campos(lst)

    def criar_widgets(self):
        # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'
        
        # Variáveis ligadas as Widgtes
        self.var_msg = StringVar()
        self.var_id = StringVar()
        self.var_tipo = StringVar()
        self.var_modelo = StringVar()
        self.var_descricao = StringVar()
        self.var_prateleira = StringVar()
        self.var_busca = StringVar()
        self.var_rb = IntVar()

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID)
        fr1.place(x=10, y=10, height=50, width=590)

        fr2 = Frame(self, borderwidth=1, relief=SOLID)
        fr2.place(x=10, y=70, height=180, width=590)

        fr3 = Frame(self, borderwidth=1, relief=SOLID)
        fr3.place(x=10, y=260, height=50, width=590)

        # Widgets do Frame fr1
        self.var_msg.set('Editando Registro')
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE')
        self.lbl_msg.pack(expand=True, fill=X)
        self.lbl_msg['fg'] = '#00008B'
        
        # Widgets do Frame fr2
        Label(fr2, font=fonte_padrao, text='ID:').place(x=10, y=10)
        self.lbl_id = Label(fr2, font=fonte_padrao, relief=SOLID, bg='#C0C0C0', textvariable=self.var_id, anchor=W)
        self.lbl_id.place(x=10, y=30, width=100)

        Label(fr2, font=fonte_padrao, text='Tipo:').place(x=120, y=10)
        self.cb_tipo = ttk.Combobox(fr2, font=fonte_padrao, textvariable=self.var_tipo, state='readonly')
        self.cb_tipo.bind('<<ComboboxSelected>>', self.carregar_modelos)
        self.cb_tipo.place(x=120, y=30, width=100)

        Label(fr2, font=fonte_padrao, text='Modelo:').place(x=230, y=10)
        self.cb_modelo = ttk.Combobox(fr2, font=fonte_padrao, textvariable=self.var_modelo, state='readonly')
        self.cb_modelo.place(x=230, y=30, width=350)

        Label(fr2, font=fonte_padrao, text='Descrição:').place(x=10,y=55)
        self.txt_descricao = Entry(fr2, font=fonte_padrao, textvariable=self.var_descricao)
        self.txt_descricao.place(x=10, y=75, width=350)

        Label(fr2, font=fonte_padrao, text='Prateleira:').place(x=370,y=55)
        self.txt_prateleira = Entry(fr2, font=fonte_padrao, textvariable=self.var_prateleira)
        self.txt_prateleira.place(x=370, y=75, width=210)

        Label(fr2, font=fonte_padrao, text='Obs:').place(x=10,y=90)
        self.text_obs = Text(fr2, font=fonte_padrao, height=3)
        self.text_obs.place(x=10, y=110, width=570)

        self.btn_alterar = Button(fr3, font=fonte_padrao, text='Alterar', command=self.alterar)
        self.btn_alterar.place(x=10, y=10, width=80)
        self.btn_excluir = Button(fr3, font=fonte_padrao, text='Excluir', command=self.excluir)
        self.btn_excluir.place(x=100, y=10, width=80)

    def preencher_campos(self, lst):
        self.var_id.set(str(lst[0]))
        self.var_tipo.set(lst[1])
        self.carregar_modelos()
        self.var_modelo.set(lst[2])
        self.var_descricao.set(lst[3])
        self.var_prateleira.set(lst[4])
        self.text_obs.insert(END, lst[5])

    def carregar_tipos(self):
        lst = []
        bll = tip_material_bll.TipMaterialBll()
        r = bll.retornar_dados('todos')
        for i in r:
            lst.append(i[1])
            self.dic_tipo[i[1]] = i[0]

        self.cb_tipo['values'] = lst
        self.cb_tipo.current(random.randint(0, (len(lst)-1)))

    def carregar_modelos(self, event=None):
        lst = []
        bll = mod_produto_bll.ModProdutoBll()
        r = bll.retornar_dados('tipo', self.var_tipo.get())
        for i in r:
            lst.append(i[2])
            self.dic_modelo[i[2]] = i[0]

        self.cb_modelo['values'] = lst
        self.cb_modelo.current(random.randint(0, (len(lst)-1)))

    def alterar(self):
        obj = tela_dto.TelaDto()
        obj.ID = int(self.var_id.get())
        obj.tipo = self.dic_tipo[self.var_tipo.get()]
        obj.modelo = self.dic_modelo[self.var_modelo.get()]
        obj.descricao = self.var_descricao.get()
        obj.prateleira = self.var_prateleira.get().upper()
        obj.obs = self.text_obs.get('1.0', END)

        bll = tela_bll.TelaBll()
        v = bll.validar_campos(obj)
        if v != 'ok':
            messagebox.showwarning('Aviso', str(v), parent=self)
            return

        r = bll.editar(obj)
        msg = 'Registro alterado com sucesso!'

        if r == 1:
            messagebox.showinfo('Gravado', msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror('Erro', str(r), parent=self)

    def excluir(self):
        p = messagebox.askquestion('Excluir', 'Deseja excluir este registro?', parent=self)
        if p == 'yes':
            ID = int(self.var_id.get())
            bll = tela_bll.TelaBll()
            r = bll.excluir(ID)
            if r == 1:
                messagebox.showinfo('Excluído', 'Registro excluído com sucesso!', parent=self)
                self.destroy()
            else:
                messagebox.showerror('Erro', str(r), parent=self)