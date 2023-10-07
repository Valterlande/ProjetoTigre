from tkinter import *
from tkinter import ttk
from BLL import material_bll


class FrmBaseMov(Toplevel):
    def __init__(self, titulo):
        Toplevel.__init__(self)

        self.title(titulo)

        w = 500
        h = 350
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.resizable(0,0)
        self.grab_set()

        self.criar_widgets()
        self.busca_no()

    def criar_widgets(self):
        # Fonte padrão
        fonte_p = 'Arial 10 bold'

        # Variáveis associadas as Widgets
        self.var_busca = StringVar()
        self.var_msg = StringVar()
        self.var_id = StringVar()
        self.var_codigo = StringVar()
        self.var_tipo = StringVar()
        self.var_descricao = StringVar()
        self.var_origem = StringVar()
        self.var_destino = StringVar()
        self.var_retrabalho = IntVar()
        self.var_impresso = IntVar()
        self.var_imprimir = IntVar()
        self.var_saldo = IntVar()
        self.var_qtd = IntVar()

        # Frames e LabelFrames
        fr0 = Frame(self)
        fr0.pack(fill=X, padx=2, pady=2)

        fr1 = Frame(self)
        fr1.pack(fill=X, padx=2, pady=2)

        lbl_fr1 = LabelFrame(self, font=fonte_p, text='Dados')
        lbl_fr1.pack(padx=2, pady=2)

        fr2 = Frame(self)
        fr2.pack(expand='true', fill=X)
        
        lbl_fr2 = LabelFrame(fr2, font=fonte_p, text='Origem')
        lbl_fr2.pack(padx=2, side='left', fill=X)

        lbl_fr3 = LabelFrame(fr2, font=fonte_p, text='Destino')
        lbl_fr3.pack(padx=2, side='left', fill=X)

        lbl_fr4 = LabelFrame(fr2, font=fonte_p, text='Qtd')
        lbl_fr4.pack(padx=2, side='left', fill=X)

        fr3 = Frame(self)
        fr3.pack(fill=X, padx=2, pady=2)

        # Widgets do Frame fr0
        self.lbl_msg = Label(fr0,textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE', fg ='#00008B')
        self.lbl_msg.pack(expand=True, fill=X)

        # Widgets do Frame fr1
        Label(fr1, font=fonte_p, text='Busca:').pack(side='left', padx=2, pady=2)
        limitar = self.register(func=self.limitar_campo)
        self.txt_busca = Entry(fr1, font=fonte_p,textvariable=self.var_busca, validate='key', validatecommand=(limitar, '%P'))
        self.txt_busca.bind('<Return>', self.buscar)
        self.txt_busca.pack(side='left', padx=2, pady=2)
        self.btn_buscar = Button(fr1, font=fonte_p, text='Buscar', width=8, command=self.buscar)
        self.btn_buscar.pack(side='left', padx=2, pady=2)
        
        # Widgets do LabelFrame lbl_fr1
        Label(lbl_fr1, font=fonte_p, text='CÓDIGO:').grid(row=0, column=0, padx=2, pady=2, stick=W)
        Label(lbl_fr1, font=fonte_p, relief='solid', width=12, anchor='w',textvariable=self.var_codigo).grid(row=1, column=0, padx=2, stick=W, pady=2)
        Label(lbl_fr1, font=fonte_p, text='TIPO:').grid(row=0, column=1, padx=2, pady=2, stick=W)
        Label(lbl_fr1, font=fonte_p, relief='solid', width=12, anchor='w',textvariable=self.var_tipo).grid(row=1, column=1, padx=2, stick=W, pady=2)
        Label(lbl_fr1, font=fonte_p, text='DESCRIÇÃO:').grid(row=2, column=0, padx=2, stick=W, pady=2)
        Label(lbl_fr1, font=fonte_p, relief='solid', width=60, anchor='w',textvariable=self.var_descricao).grid(row=3, column=0, columnspan=4, padx=2, stick=W, pady=2)
        Label(lbl_fr1, font=fonte_p, text='RETRABALHO:').grid(row=4, column=0, padx=2, stick=W, pady=2)
        Label(lbl_fr1, font=fonte_p, text='IMPRESSO:').grid(row=4, column=1, padx=2, stick=W, pady=2)
        Label(lbl_fr1, font=fonte_p, text='IMPRIMIR:').grid(row=4, column=2, padx=2, stick=W, pady=2)
        Label(lbl_fr1, font=fonte_p, text='SALDO:').grid(row=4, column=3, padx=2, stick=W, pady=2)
        Label(lbl_fr1, font=fonte_p, relief='solid', width=12, anchor='w',textvariable=self.var_retrabalho).grid(row=5, column=0, padx=2, pady=2, stick=W)
        Label(lbl_fr1, font=fonte_p, relief='solid', width=12, anchor='w',textvariable=self.var_impresso).grid(row=5, column=1, padx=2, pady=2, stick=W)
        Label(lbl_fr1, font=fonte_p, relief='solid', width=12, anchor='w',textvariable=self.var_imprimir).grid(row=5, column=2, padx=2, pady=2, stick=W)
        Label(lbl_fr1, font=fonte_p, relief='solid', width=12, anchor='w',textvariable=self.var_saldo).grid(row=5, column=3, padx=2, pady=2, stick=W)

        # Widgets do LabelFrame lbl_fr2
        self.cb_origem = ttk.Combobox(lbl_fr2, font=fonte_p, state='readonly',textvariable=self.var_origem)
        self.cb_origem.pack()

        # Widgets do LabelFrame lbl_fr3
        self.cb_destino = ttk.Combobox(lbl_fr3, font=fonte_p, state='readonly',textvariable=self.var_destino)
        self.cb_destino.pack()

        # Widgets do LabelFrame lbl_fr4
        self.txt_qtd = Entry(lbl_fr4, font=fonte_p,textvariable=self.var_qtd)
        self.txt_qtd.pack()

        # Widgets do Frame fr3
        self.btn_confirmar = Button(fr3, font=fonte_p, text='Confirmar', width=8)
        self.btn_confirmar.pack(side='right', padx=2, pady=2)

    def limitar_campo(self, t):
        if len(t) > 6:
            return False
        return True

    def busca_yes(self):
        self.btn_confirmar['state'] = 'normal'
        self.txt_qtd['state'] = 'normal'

    def busca_no(self):
        self.btn_confirmar['state'] = 'disabled'
        self.txt_qtd['state'] = 'disabled'

    def buscar(self, event=None):
        self.busca_no()
        self.limpar_campos()
        bll = material_bll.MaterialBll()
        r = bll.retornar_dados('codigo', self.var_busca.get())

        if r != []:
            self.var_id.set(str(r[0][0]))
            self.var_codigo.set(r[0][1])
            self.var_tipo.set(r[0][2])
            self.var_descricao.set(r[0][3])
            self.var_retrabalho.set(r[0][4])
            self.var_impresso.set(r[0][5])
            self.var_imprimir.set(r[0][6])
            self.var_saldo.set(r[0][7])

            self.busca_yes()
    
    def limpar_campos(self):
        self.var_id.set('')
        self.var_codigo.set('')
        self.var_tipo.set('')
        self.var_descricao.set('')
        self.var_retrabalho.set(0)
        self.var_impresso.set(0)
        self.var_imprimir.set(0)
        self.var_saldo.set(0)
        self.var_qtd.set(0)
