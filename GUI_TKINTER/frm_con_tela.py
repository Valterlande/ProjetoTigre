from tkinter import *
from tkinter import ttk, messagebox
from BLL import tela_bll, tip_material_bll, mod_produto_bll
import random
from GUI_TKINTER import frm_atu_tela
from Ferramentas import variaveis_globais


class FormConTela(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        w = 800
        h = 600
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d'%(w,h,x,y))

        self.title('Consulta Telas')

        self.criar_widgets()
        self.listar_tipos()
        self.listar_modelos()

    def criar_widgets(self):
        # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'

        # Variáveis
        self.var_msg = StringVar()
        self.var_tipo = StringVar()
        self.var_mod = StringVar()
        self.var_busca = StringVar()
        self.var_ckb_tipo = BooleanVar()
        self.var_ckb_mod = BooleanVar()
        self.var_display = StringVar()

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID,height=50)
        fr1.pack(fill=X, pady=2, padx=2)

        fr2 = Frame(self, borderwidth=1, relief=SOLID, height=130)
        fr2.pack(fill=X, pady=2, padx=2)

        fr3 = Frame(self, borderwidth=1, relief=SOLID, height=100)
        fr3.pack(pady=2, padx=2, fill=X)

        fr4 = Frame(self, borderwidth=1, relief=SOLID)
        fr4.pack(padx=2, pady=2, expand=True, fill=BOTH)

        # Widgets do Frame fr1
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE')
        self.lbl_msg.pack(expand=True, fill=X)

        self.var_msg.set('Consulta de Telas')
        self.lbl_msg['fg'] = '#00008B'

        # Widgets do Frame fr2
        lf_tipo = LabelFrame(fr2, font=fonte_padrao, borderwidth=1, relief=SOLID, text='Tipo:')
        lf_tipo.place(x=5,y=5, width=200, height=60)

        self.cb_tipo = ttk.Combobox(lf_tipo, font=fonte_padrao, textvariable=self.var_tipo, state='readonly')
        self.cb_tipo.bind('<<ComboboxSelected>>', self.listar_modelos)
        self.cb_tipo.place(x=5, y=5, width=100)

        self.ckb_tipo = Checkbutton(lf_tipo, font=fonte_padrao, text='Todos', variable=self.var_ckb_tipo, command=self.checar_tipo)
        self.ckb_tipo.place(x=120, y=5)

        lf_mod = LabelFrame(fr2, font=fonte_padrao, borderwidth=1, relief=SOLID, text='Modelo:')
        lf_mod.place(x=210,y=5, width=800, height=60)

        self.cb_mod = ttk.Combobox(lf_mod, font=fonte_padrao, textvariable=self.var_mod, state='readonly')
        self.cb_mod.bind('<<ComboboxSelected>>', self.click_cb_modelo)
        self.cb_mod.place(x=5, y=5, width=600)

        self.ckb_mod = Checkbutton(lf_mod, font=fonte_padrao, text='Todos', variable=self.var_ckb_mod, command=self.checar_modelo)
        self.ckb_mod.place(x=620, y=5)

        Label(fr2, font=fonte_padrao, text='Dígite a busca:').place(x=500, y=90)
        self.txt_busca = Entry(fr2, font=fonte_padrao, textvariable=self.var_busca)
        self.txt_busca.bind('<Return>', self.buscar)
        self.txt_busca.place(x=620,y=90, width=300)
        self.btn_buscar = Button(fr2, font=fonte_padrao, text='Buscar', command=self.buscar)
        self.btn_buscar.place(x=930, y=90, width=80)

        # Widgets do Frame fr3
        self.lbl_display = Label(fr3, font=('Consolas 18 bold'), textvariable=self.var_display, anchor=W, justify=LEFT,border=2, relief=RAISED, bg='#FFDEAD')
        self.lbl_display.pack(fill=X, expand=True)

        # Widgets do Frame fr4
        self.tree = ttk.Treeview(fr4, columns=('a','b','c', 'd', 'e', 'f'))
        self.tree.column('#0', width=20, minwidth=20, stretch=NO)
        self.tree.column('a', width=80, minwidth=80, stretch=NO)
        self.tree.column('b', width=100, minwidth=100, stretch=NO)
        self.tree.column('c', width=250, minwidth=250, stretch=NO)
        self.tree.column('d', width=400, minwidth=400)

        self.tree.heading('a', text='ID', anchor=W)
        self.tree.heading('b', text='TIPO', anchor=W)
        self.tree.heading('c', text='MODELO', anchor=W)
        self.tree.heading('d', text='DESCRIÇÃO', anchor=W)
        self.tree.heading('e', text='PRATELEIRA', anchor=W)
        self.tree.heading('f', text='OBS', anchor=W)
        
        vsb = ttk.Scrollbar(fr4, orient=VERTICAL, command=self.tree.yview)
        self.tree.bind('<<TreeviewSelect>>', self.click_tree)
        self.tree.bind('<Double-1>', self.duplo_click)
        self.tree.configure(yscrollcommand=vsb.set)

        vsb.pack(side=RIGHT, fill=Y)
        self.tree.pack(expand='true', fill=BOTH)

    def limpar_campos(self):
        self.var_mod.set('')
        self.var_busca.set('')
        self.var_display.set('')
        self.tree.delete(*self.tree.get_children())

    def listar_tipos(self):
        bll = tip_material_bll.TipMaterialBll()
        r = bll.retornar_dados('todos')

        lst = []
        for i in r:
            lst.append(i[1])

        self.tam = (len(lst)-1)
        self.cb_tipo['values'] = lst
        self.cb_tipo.current(random.randint(0, self.tam))

    def listar_modelos(self, event=None):
        self.limpar_campos()
        lst = []
        bll = mod_produto_bll.ModProdutoBll()
        r = bll.retornar_dados('tipo', self.var_tipo.get())

        for i in r:
            lst.append(i[2])
        
        self.cb_mod['values'] = lst
        self.cb_mod.current(0)

    def click_cb_modelo(self, event=None):
        self.var_busca.set('')
        self.tree.delete(*self.tree.get_children())
        self.var_display.set('')
        self.txt_busca.focus()

    def checar_tipo(self):
        if self.var_ckb_tipo.get():
            self.cb_tipo['state'] = 'disabled'
            self.cb_mod['state'] = 'disabled'
            self.ckb_mod['state'] = 'disabled'

            self.ckb_mod.deselect()

            self.var_tipo.set('')
            self.limpar_campos()
        else:
            self.cb_mod['state'] = 'readonly'
            self.cb_tipo['state'] = 'readonly'
            self.ckb_mod['state'] = 'normal'
            self.cb_tipo.current(random.randint(0, self.tam))
            self.listar_modelos()

    def checar_modelo(self):
        if self.var_ckb_mod.get():
            self.ckb_tipo['state'] = 'disabled'
            self.cb_tipo['state'] = 'disabled'
            self.cb_mod['state'] = 'disabled'

            self.limpar_campos()
        else:
            self.ckb_tipo['state'] = 'normal'
            self.cb_tipo['state'] = 'readonly'
            self.cb_mod['state'] = 'readonly'
            self.listar_modelos()

    def buscar(self, event=None):
        bll = tela_bll.TelaBll()
        r = bll.retornar_dados('tipo+modelo+descricao', ('%'+self.var_tipo.get()+'%', '%'+self.var_mod.get()+'%', '%'+self.var_busca.get()+'%'))

        self.tree.delete(*self.tree.get_children())
        for i in r:
            self.tree.insert('','end',text='', values=(str(i[0]), i[1], i[2], i[3], i[4], i[5]))

    def click_tree(self, event=None):
        ID = self.tree.focus()

        lst = self.tree.item(ID)['values']

        self.var_display.set('Tipo:......... {}\nModelo:....... {}\nDescrição:.... {}\nPrateleira(s): {}'.format(lst[1], lst[2], lst[3], lst[4]))
    
    def duplo_click(self, event=None):

        if variaveis_globais.usu_acesso >= 2:
            ID = self.tree.focus()
            lst = self.tree.item(ID)['values']

            frm_atu_tela.FrmAtuTela(lst)
