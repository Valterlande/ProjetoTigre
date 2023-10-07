from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from BLL import tip_material_bll, mov_material_bll
from Ferramentas import gerar_relatorios


class FrmRelMovMaterial(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        w = 470
        h = 330
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d' % (w,h,x,y))
        self.resizable(0,0)
        self.grab_set()
        self.title('Relatório Mov. de Materiais')

        self.criar_widgets()
        self.listar_material()
        self.click_ckb_mat()

    def criar_widgets(self):
        # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'

        # Variáveis
        self.var_msg = StringVar()
        self.var_dti = StringVar()
        self.var_dtf = StringVar()
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

        self.var_msg.set('Relatório de Mov. Materiais')
        self.lbl_msg['fg'] = '#00008B'

        validar = self.register(func=self.validar)

        # Widgets do Frame fr2
        lbf1 = LabelFrame(fr2, font=fonte_padrao, text='Período:', relief=SOLID)
        lbf1.place(x=5, y=5, width=440, height=80)

        Label(lbf1, font=fonte_padrao, text='Data Inicial:').place(x=5, y=5)
        self.txt_dtinicial = Entry(lbf1, font=fonte_padrao, relief='solid',textvariable=self.var_dti, validate='key', validatecommand=(validar, '%P'))
        self.txt_dtinicial.place(x=5,y=30, width=100)

        Label(lbf1, font=fonte_padrao, text=' á ').place(x=110, y=30)

        Label(lbf1, font=fonte_padrao, text='Data Final:').place(x=140, y=5)
        self.txt_dtfinal = Entry(lbf1, font=fonte_padrao, relief='solid',textvariable=self.var_dtf)
        self.txt_dtfinal.place(x=140,y=30, width=100)

        lbf2 = LabelFrame(fr2, font=fonte_padrao, text='Parâmetros:', relief=SOLID)
        lbf2.place(x=5, y=90, width=440, height=110)

        self.ckb_mat = Checkbutton(lbf2, font=fonte_padrao, text='Todos Tipos', variable=self.var_ckb, command=self.click_ckb_mat)
        self.ckb_mat.select()
        self.ckb_mat.place(x=5, y=5)

        self.cb_mat = ttk.Combobox(lbf2, font=fonte_padrao, textvariable=self.var_mat)
        self.cb_mat.place(x=5, y=35, width=150)

        self.btn_gerar = Button(fr2, font=fonte_padrao, text='Gerar', command=self.gerar)
        self.btn_gerar.place(x=360, y=210, width=80)

    def listar_material(self):
        bll = mov_material_bll.MovMaterialBll()
        r = bll.retornar_dados('todos')
        lst = []
        for i in r:
            lst.append(i[3])
            
        l = sorted(set(lst))
        self.cb_mat['values'] = l
        self.cb_mat.current(0)

    def click_ckb_mat(self):
        if not self.var_ckb.get():
            self.cb_mat['state'] = 'readonly'
            self.cb_mat.current(0)
        else:
            self.cb_mat['state'] = 'disabled'
            self.var_mat.set('')

    # Falta implementar, não coseguir
    def validar(self, t):
        return True
        
    def gerar(self):
        try:
            dtini = datetime.strptime(self.var_dti.get(), '%d/%m/%Y').date()
            dtfim = datetime.strptime(self.var_dtf.get(), '%d/%m/%Y').date()
        except:
            messagebox.showwarning('Aviso', 'O Formato de data está errado.\nDígite a data neste formato 00/00/0000 (dia/mês/ano)', parent=self)
            return

        r = gerar_relatorios.gerar_relatorio_mov_material(dtini, dtfim, self.var_mat.get())
        if r != 'OK':
            messagebox.showerror('Erro', 'Erro ao gerar relatório.\nContate o suporte.\nErro: '+str(r), parent=self)
            return
        