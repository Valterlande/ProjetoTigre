from tkinter import *
from tkinter import ttk, messagebox
from BLL import material_bll, tip_material_bll
from DTO import material_dto


class FrmCadMaterial(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)

        self.title('Cadastro de Material')
        w = 572
        h = 600
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d' %(w, h, x, y))
        self.resizable(0, 0)
        self.grab_set()

        # Variáveis
        self.var_id = StringVar()
        self.var_tipo = StringVar()
        self.var_descricao = StringVar()
        self.var_codigo = StringVar()
        self.var_msg = StringVar()
        self.var_busca = StringVar()
        self.var_retrabalho = IntVar()
        self.var_impresso = IntVar()
        self.var_imprimir = IntVar()
        self.var_saldo = IntVar()

        self.criar_widgets()
        self.preparar()
        self.carregar_tipo()

    def criar_widgets(self):
        # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID)
        fr1.place(x=10, y=10, height=50, width=550)

        fr2 = Frame(self, borderwidth=1, relief=SOLID)
        fr2.place(x=10, y=70, height=230, width=550)

        fr3 = Frame(self, borderwidth=1, relief=SOLID)
        fr3.place(x=10, y=310, height=280, width=550)

        self.limitar = self.register(func=self.limitar_campo)

        # Widgets do Frame fr1
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE')
        self.lbl_msg.pack(expand=True, fill=X)

        # Widgets do Frame fr2
        Label(fr2, text='ID:', font=fonte_padrao).place(x=10, y=10)
        self.lbl_id = Label(fr2, font=fonte_padrao,  bg='#C0C0C0', relief=SOLID, textvariable=self.var_id, anchor=W)
        self.lbl_id.place(x=10, y=30, width=100)

        Label(fr2, text='Código:', font=fonte_padrao).place(x=120, y=10)
        self.txt_codigo = Entry(fr2, font=fonte_padrao, relief=SOLID, textvariable=self.var_codigo, validate='key', validatecommand=(self.limitar, '%P'))
        self.txt_codigo.place(x=120,y=30, width=100)

        Label(fr2, font=fonte_padrao, text='Tipo:').place(x=230, y=10)
        self.cb_tipo = ttk.Combobox(fr2, font=fonte_padrao, textvariable=self.var_tipo)
        self.cb_tipo.place(x=230, y=30)

        Label(fr2, text='Descrição:', font=fonte_padrao).place(x=10, y=55)
        self.txt_descricao = Entry(fr2, font=fonte_padrao, textvariable=self.var_descricao, relief=SOLID)
        self.txt_descricao.place(x=10, y=75, width=500)

        Label(fr2, font=fonte_padrao, text='Retrabalho:').place(x=10, y=100)
        Label(fr2, font=fonte_padrao, relief=SOLID, anchor=W, textvariable=self.var_retrabalho).place(x=10, y=120, width=100)
        Label(fr2, font=fonte_padrao, text='Impresso:').place(x=120, y=100)
        Label(fr2, font=fonte_padrao, relief=SOLID, anchor=W, textvariable=self.var_impresso).place(x=120, y=120, width=100)
        Label(fr2, font=fonte_padrao, text='Imprimir:').place(x=230, y=100)
        Label(fr2, font=fonte_padrao, relief=SOLID, anchor=W, textvariable=self.var_imprimir).place(x=230, y=120, width=100)
        Label(fr2, font=fonte_padrao, text='Saldo:').place(x=410, y=100)
        Label(fr2, font=fonte_padrao, relief=SOLID, anchor=W, textvariable=self.var_saldo).place(x=410, y=120, width=100)

        Label(fr2, font=fonte_padrao, text='Obs:').place(x=10, y=145)
        self.texto = Text(fr2, font=fonte_padrao, height=3, relief=GROOVE)
        vsb_texto = Scrollbar(fr2, orient=VERTICAL, command=self.texto.yview)

        self.texto.configure(yscrollcommand=vsb_texto.set)

        vsb_texto.place(x=510, y=165, height=50)
        self.texto.place(x=10, y=165, width=500)

        # Widgets do Frame fr3
        Label(fr3, font=fonte_padrao, text='Busca: ').place(x=10, y=10)
        self.txt_busca = Entry(fr3, font=fonte_padrao, textvariable=self.var_busca, validate='key', validatecommand=(self.limitar, '%P'))
        self.txt_busca.place(x=80, y=10)
        self.btn_buscar = Button(fr3, font=fonte_padrao, text='Buscar', command=self.listar)
        self.btn_buscar.place(x=280, y=10, width=80)

        self.tree = ttk.Treeview(fr3)
        self.tree['columns'] = ('a', 'b')
        self.tree.column('#0', width=20, minwidth=20, stretch=NO)
        self.tree.column('a', width=80, minwidth=20, stretch=NO)

        self.tree.heading('a', text='CÓDIGO', anchor='w')
        self.tree.heading('b', text='DESCRIÇÃO', anchor='w')

        vsb_tree = Scrollbar(fr3, orient=VERTICAL, command=self.tree.yview)

        self.tree.bind('<<TreeviewSelect>>', self.item_selecionado)
        self.tree.configure(yscrollcommand=vsb_tree.set)
        
        vsb_tree.place(x=510, y=50, height=180)
        self.tree.place(x=10, y=50, width=500, height=180)

        self.btn_novo = Button(fr3, text='Novo', font=fonte_padrao, command=self.novo)
        self.btn_novo.place(x=10, y=240, width=80)
        self.btn_gravar = Button(fr3, text='Gravar', font=fonte_padrao, command=self.gravar)
        self.btn_gravar.place(x=100, y=240, width=80)
        self.btn_excluir = Button(fr3, text='Excluir', font=fonte_padrao, command=self.excluir)
        self.btn_excluir.place(x=190, y=240, width=80)

    def limitar_campo(self, t):
        if len(t) > 6:
            return False
        return True

    def carregar_tipo(self):
        self.dic_tipo = {}
        lst = []
        bll = tip_material_bll.TipMaterialBll()
        r = bll.retornar_dados('todos')
        for i in r:
            lst.append(i[1])
            self.dic_tipo[i[1]] = i[0]

        self.cb_tipo['values'] = lst
        self.cb_tipo.current(0)

    def listar(self):
        bll = material_bll.MaterialBll()
        r = bll.retornar_dados('codigo%', '%'+self.var_busca.get()+'%')
        self.lst_dados = r

        self.tree.delete(*self.tree.get_children())
        for i in r:
            self.tree.insert('', 'end', text='', values=(i[1], i[3]))

    def limpar_campos(self):
        self.var_id.set('')
        self.var_descricao.set('')
        self.var_codigo.set('')
        self.texto.delete('1.0', END)

    def hab_des_widgets(self, codigo, tipo, descricao, obs, busca, buscar, gravar, excluir):
        self.txt_codigo['state'] = codigo
        self.cb_tipo['state'] = tipo
        self.txt_descricao['state'] = descricao
        self.texto['state'] = obs
        self.txt_busca['state'] = busca
        self.btn_buscar['state'] = buscar
        self.btn_gravar['state'] = gravar
        self.btn_excluir['state'] = excluir

    def preparar(self):
        self.limpar_campos()
        self.var_msg.set('')
        self.hab_des_widgets('disabled','disabled','disabled','disabled','disabled','disabled','disabled','disabled')
        self.listar()

    def item_selecionado(self, event):
        ID = self.tree.focus()
        self.texto.delete('1.0', END)

        for i in self.lst_dados:
            if i.count(str(self.tree.item(ID)['values'][0])):
                self.var_id.set(str(i[0]))
                self.var_codigo.set(i[1])
                self.var_tipo.set(i[2])
                self.var_descricao.set(i[3])
                self.var_retrabalho.set(i[4])
                self.var_impresso.set(i[5])
                self.var_imprimir.set(i[6])
                self.var_saldo.set(i[7])
                self.texto.insert(END, i[8])
                self.hab_des_widgets('normal', 'readonly', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal')

                self.var_msg.set('Alterar Registro')
                self.lbl_msg['fg'] = '#A52A2A'
                continue          

    def novo(self):
        self.limpar_campos()
        self.hab_des_widgets('normal', 'readonly','normal','normal','disabled','disabled','normal','disabled')
        self.txt_codigo.focus()

        self.var_msg.set('Novo Registro')
        self.lbl_msg['fg'] = '#00008B'

    def gravar(self):
        obj = material_dto.MaterialDto()
        obj.codigo = self.var_codigo.get()
        obj.tipo = self.dic_tipo[self.var_tipo.get()]
        obj.descricao = self.var_descricao.get().upper()
        obj.obs = self.texto.get('1.0', END)

        bll = material_bll.MaterialBll()
        validar = bll.validar_campos(obj)
        if validar != 'ok':
            messagebox.showwarning('Aviso', str(validar), parent=self)
            return
        
        if self.var_id.get() == '':
            r = bll.inserir(obj)
            msg = 'Registro incluído com sucesso!'
        else:
            obj.ID = int(self.var_id.get())
            r = bll.editar(obj)
            msg = 'Registro alterado com sucesso!'

        if r == 1:
            messagebox.showinfo('Gravado', msg, parent=self)
            self.preparar()
        else:
            messagebox.showerror('Erro', str(r), parent=self)

    def excluir(self):
        p = messagebox.askquestion('Excluir', 'Deseja excluir este registro?', parent=self)
        if p == 'yes':
            bll = material_bll.MaterialBll()
            ID = int(self.var_id.get())

            r = bll.excluir(ID)
            if r == 1:
                messagebox.showinfo('Excluído', 'Registro excluído com sucesso!', parent=self)
                self.preparar()
            else:
                messagebox.showerror('Erro', str(r), parent=self)
