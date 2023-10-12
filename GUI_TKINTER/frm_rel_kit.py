from tkinter import *
from tkinter import ttk, messagebox
from BLL import kit_bll
from Ferramentas import gerar_relatorios


class FrmRelKit(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        w = 470
        h = 330
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d' % (w,h,x,y))
        self.resizable(0,0)
        self.grab_set()
        self.title('Relatório Kits')

        self.criar_widgets()
        self.listar_materiais()
        self.click_ckb_material()

    def criar_widgets(self):
        # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'

        # Variáveis
        self.var_msg = StringVar()
        self.var_mat = StringVar()
        self.var_ckb = BooleanVar()

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID)
        fr1.place(x=10, y=10, height=50, width=450)

        fr2 = Frame(self, borderwidth=1, relief=SOLID)
        fr2.place(x=10, y=70, height=250, width=450)

        # Widgets do Frame fr1
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE')
        self.lbl_msg.pack(expand=True, fill=X)

        self.var_msg.set('Relatório de Kits')
        self.lbl_msg['fg'] = '#00008B'

        # Widgets do Frame fr2
        lbf = LabelFrame(fr2, font=fonte_padrao, text='Material:', relief=SOLID)
        lbf.place(x=5, y=5, width=430, height=80)

        self.ckb_mat = Checkbutton(lbf, font=fonte_padrao, text='Todos', variable=self.var_ckb, command=self.click_ckb_material)
        self.ckb_mat.select()
        self.ckb_mat.place(x=5, y=5)

        self.cb_mat = ttk.Combobox(lbf, font=fonte_padrao, textvariable=self.var_mat, state='readonly')
        self.cb_mat.place(x=5, y=30, width=410)

        self.btn_gerar = Button(fr2, font=fonte_padrao, text='Gerar', command=self.gerar)
        self.btn_gerar.place(x=360, y=210, width=80)

    def listar_materiais(self):
        bll = kit_bll.KitBll()
        r = bll.retornar_dados('todos')
        lst = []
        for i in r:
            lst.append(i[2]+' - '+i[3])
        
        l = sorted(set(lst))
        self.cb_mat['values'] = l
        self.cb_mat.current(0)

    def click_ckb_material(self):
        if not self.var_ckb.get():
            self.cb_mat['state'] = 'readonly'
            self.cb_mat.current(0)
            self.cb_mat.focus()
        else:
            self.cb_mat['state'] = 'disabled'
            self.var_mat.set('')

    def gerar(self):
        r = gerar_relatorios.gerar_relatorio_kit(self.var_mat.get()[:6])
        if r != 'OK':
            messagebox.showerror('Erro', 'Erro ao gerar relatório.\nContate o suporte.\nErro: '+str(r), parent=self)
            