from tkinter import *
from tkinter import ttk, messagebox
from BLL import mod_produto_bll, tip_material_bll
from Ferramentas import gerar_relatorios


class FrmRelTela(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        w = 470
        h = 330
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d' % (w,h,x,y))
        self.resizable(0,0)
        self.grab_set()
        self.title('Relatório Telas')

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
        self.var_ckb_tipo = BooleanVar()
        self.var_ckb_mod = BooleanVar()
        
        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID)
        fr1.place(x=10, y=10, height=50, width=450)

        fr2 = Frame(self, borderwidth=1, relief=SOLID)
        fr2.place(x=10, y=70, height=250, width=450)

        # Widgets do Frame fr1
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE')
        self.lbl_msg.pack(expand=True, fill=X)

        self.var_msg.set('Relatório de Telas')
        self.lbl_msg['fg'] = '#00008B'

        # Widgets do Frame fr2
        lbf1 = LabelFrame(fr2, font=fonte_padrao, text='Tipo:', relief=SOLID)
        lbf1.place(x=5, y=5, width=250, height=60)

        self.cb_tipo = ttk.Combobox(lbf1, font=fonte_padrao, textvariable=self.var_tipo, state='readonly')
        self.cb_tipo.bind('<<ComboboxSelected>>', self.listar_modelos)
        self.cb_tipo.place(x=5, y=5, width=150)

        self.ckb_tipo = Checkbutton(lbf1, font=fonte_padrao, text='Todos', variable=self.var_ckb_tipo,command=self.click_ckb_tipo)
        self.ckb_tipo.place(x=160, y=5)

        lbf2 = LabelFrame(fr2, font=fonte_padrao, text='Modelo:', relief=SOLID)
        lbf2.place(x=5, y=70, width=440, height=60)

        self.cb_mod = ttk.Combobox(lbf2, font=fonte_padrao, textvariable=self.var_mod, state='readonly')
        self.cb_mod.place(x=5, y=5, width=350)

        self.ckb_mod = Checkbutton(lbf2, font=fonte_padrao, text='Todos', variable=self.var_ckb_mod, command=self.click_ckb_mod)
        self.ckb_mod.place(x=360, y=5)

        self.btn_gerar = Button(fr2, font=fonte_padrao, text='Gerar', command=self.gerar)
        self.btn_gerar.place(x=360, y=210, width=80)

    def listar_tipos(self):
        bll = tip_material_bll.TipMaterialBll()
        r = bll.retornar_dados('todos')
        lst = []
        for i in r:
            lst.append(i[1])
        
        self.cb_tipo['values'] = lst
        self.cb_tipo.current(0)

    def listar_modelos(self, event=None):
        bll = mod_produto_bll.ModProdutoBll()
        r = bll.retornar_dados('tipo', self.var_tipo.get())
        lst = []
        for i in r:
            lst.append(i[2])
        
        self.cb_mod['values'] = lst
        self.cb_mod.current(0)

    def click_ckb_tipo(self):
        if not self.var_ckb_tipo.get():
            self.cb_tipo['state'] = 'readonly'
            self.cb_mod['state'] = 'readonly'
            self.ckb_mod['state'] = 'normal'
            self.cb_tipo.current(0)
            self.listar_modelos()
        else:
            self.cb_tipo['state'] = 'disabled'
            self.cb_mod['state'] = 'disabled'
            self.ckb_mod['state'] = 'disabled'
            self.var_tipo.set('')
            self.var_mod.set('')

    def click_ckb_mod(self):
        if not self.var_ckb_mod.get():
            self.cb_mod['state'] = 'readonly'
            self.cb_tipo['state'] = 'readonly'
            self.ckb_tipo[ 'state'] = 'normal'
            self.cb_mod.current(0)
        else:
            self.cb_mod['state'] = 'disabled'
            self.cb_tipo['state'] = 'disabled'
            self.ckb_tipo[ 'state'] = 'disabled'
            self.var_mod.set('')

    def gerar(self):
        r = gerar_relatorios.gerar_relatorio_tela(self.var_tipo.get(),self.var_mod.get())
        if r != 'OK':
            messagebox.showerror('Erro', 'Erro ao gerar relatório.\nContate o suporte.\nErro: '+str(r), parent=self)
            return
            