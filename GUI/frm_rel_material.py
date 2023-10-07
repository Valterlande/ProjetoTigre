from tkinter import *
from tkinter import ttk, messagebox
from BLL import tip_material_bll
from Ferramentas import gerar_relatorios


class FrmRelMaterial(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        w = 470
        h = 330
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d' % (w,h,x,y))
        self.resizable(0,0)
        self.grab_set()
        self.title('Relatório Material')

        self.criar_widgets()
        self.listar_tipos()

    def criar_widgets(self):
        # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'

        # Variáveis
        self.var_msg = StringVar()
        self.var_tipo = StringVar()
        self.var_ckb = BooleanVar()

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID)
        fr1.place(x=10, y=10, height=50, width=450)

        fr2 = Frame(self, borderwidth=1, relief=SOLID)
        fr2.place(x=10, y=70, height=250, width=450)

        # Widgets do Frame fr1
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE')
        self.lbl_msg.pack(expand=True, fill=X)

        self.var_msg.set('Relatório de Materiais')
        self.lbl_msg['fg'] = '#00008B'

        # Widgets do Frame fr2
        lbf = LabelFrame(fr2, font=fonte_padrao, text='Tipo:', relief=SOLID)
        lbf.place(x=5, y=5, width=250, height=60)

        self.cb_tipo = ttk.Combobox(lbf, font=fonte_padrao, textvariable=self.var_tipo, state='readonly')
        self.cb_tipo.place(x=5, y=5, width=150)

        self.ckb_tipo = Checkbutton(lbf, font=fonte_padrao, text='Todos', variable=self.var_ckb, command=self.click_ckb_tipo)
        self.ckb_tipo.place(x=170, y=5)

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

    def click_ckb_tipo(self):
        if self.var_ckb.get():
            self.cb_tipo['state'] = 'disabled'
            self.var_tipo.set('')
        else:
            self.cb_tipo['state'] = 'readonly'
            self.cb_tipo.current(0)

    def gerar(self):
        r = gerar_relatorios.gerar_relatorio_material(self.var_tipo.get())
        if r != 'OK':
            messagebox.showerror('Erro', 'Erro ao gerar relatório.\nContate o suporte.\nErro: '+str(r), parent=self)
            return
