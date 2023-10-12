from tkinter import *
from tkinter import ttk
from BLL import material_bll


class FrmConMaterial(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        w = 800
        h = 600
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d' % (w,h,x,y))

        self.title('Consulta Materiais')

        self.criar_widgets()

    def criar_widgets(self):
        # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'

        # Variáveis
        self.var_msg = StringVar()
        self.var_busca = StringVar()
        self.var_rb = IntVar()
        self.var_display = StringVar()

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID,height=50)
        fr1.pack(fill=X, pady=2, padx=2)

        fr2 = Frame(self, borderwidth=1, relief=SOLID, height=80)
        fr2.pack(fill=X, pady=2, padx=2)

        fr3 = Frame(self, borderwidth=1, relief=SOLID, height=100)
        fr3.pack(pady=2, padx=2, fill=X)

        fr4 = Frame(self, borderwidth=1, relief=SOLID)
        fr4.pack(padx=2, pady=2, expand=True, fill=BOTH)

        # Widgets do Frame fr1
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE')
        self.lbl_msg.pack(expand=True, fill=X)

        self.var_msg.set('Consulta de Materiais')
        self.lbl_msg['fg'] = '#00008B'

        # Widgets do Frame fr2
        lf_tipo = LabelFrame(fr2, font=fonte_padrao, borderwidth=1, relief=SOLID, text='Tipo de busca:')
        lf_tipo.place(x=5,y=5, width=200, height=60)

        self.rb_codigo = Radiobutton(lf_tipo, font=fonte_padrao, text='Código', variable=self.var_rb, value=0, command=self.click_rb)
        self.rb_codigo.place(x=5, y=5)

        self.rb_des = Radiobutton(lf_tipo, font=fonte_padrao, text='Descrição', variable=self.var_rb, value=1, command=self.click_rb)
        self.rb_des.place(x=80, y=5)

        Label(fr2, font=fonte_padrao, text='Dígite a busca:').place(x=250, y=25)
        self.txt_busca = Entry(fr2, font=fonte_padrao, textvariable=self.var_busca)
        self.txt_busca.bind('<Return>', self.buscar)
        self.txt_busca.place(x=365,y=25, width=200)
        self.btn_buscar = Button(fr2, font=fonte_padrao, text='Buscar', command=self.buscar)
        self.btn_buscar.place(x=570, y=25, width=80)

        # Widgets do Frame fr3
        self.lbl_display = Label(fr3, font=('Consolas 18 bold'), textvariable=self.var_display, anchor=W, justify=LEFT,border=2, relief=RAISED, bg='#FFDEAD')
        self.lbl_display.pack(fill=X, expand=True)

        # Widgets do Frame fr4
        self.tree = ttk.Treeview(fr4, columns=('a','b','c','d','e', 'f', 'g', 'h'))
        self.tree.column('#0', width=20, minwidth=20, stretch=NO)
        self.tree.column('a', width=80, minwidth=80, stretch=NO)
        self.tree.column('b', width=100, minwidth=100, stretch=NO)
        self.tree.column('c', width=400, minwidth=250)
        self.tree.column('d', width=80)
        self.tree.column('e', width=8)
        self.tree.column('f', width=80)
        self.tree.column('g', width=80)

        self.tree.heading('a', text='CÓDIGO', anchor=W)
        self.tree.heading('b', text='TIPO', anchor=W)
        self.tree.heading('c', text='DESCRIÇÃO', anchor=W)
        self.tree.heading('d', text='RETRABALHO', anchor=W)
        self.tree.heading('e', text='IMPRESSO', anchor=W)
        self.tree.heading('f', text='IMPRIMIR', anchor=W)
        self.tree.heading('g', text='SALDO', anchor=W)
        self.tree.heading('h', text='OBS', anchor=W)
        
        vsb = ttk.Scrollbar(fr4, orient=VERTICAL, command=self.tree.yview)
        self.tree.bind('<<TreeviewSelect>>', self.click_tree)
        self.tree.configure(yscrollcommand=vsb.set)

        vsb.pack(side=RIGHT, fill=Y)
        self.tree.pack(expand='true', fill=BOTH)

    def buscar(self, event=None):
        prms = '%'+self.var_busca.get()+'%'
        if self.var_rb.get() == 0:
            tipo = 'codigo%'
        else:
            tipo = 'descricao'
            
        bll = material_bll.MaterialBll()
        r = bll.retornar_dados(tipo, prms)

        self.tree.delete(*self.tree.get_children())

        for i in r:
            self.tree.insert('', 'end', text='', values=(i[1], i[2], i[3],i[4], i[5], i[6], i[7], i[8]))

    def click_rb(self):
        self.var_busca.set('')
        self.tree.delete(*self.tree.get_children())
        self.var_display.set('')
        self.txt_busca.focus()

    def click_tree(self, event=None):
        ID = self.tree.focus()
        r = self.tree.item(ID)['values']

        self.var_display.set('Código:..... {}\nTipo:....... {}\nDescrição:.. {}\nQuantidades: Retrabbalho = {} | Impresso = {} | Imprimir = {} | Saldo = {}'.format(
            r[0], r[1], r[2],r[3],r[4],r[5],r[6]
        ))
