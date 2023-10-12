from tkinter import *
from tkinter import messagebox, ttk
from BLL import usuario_bll
from DTO import usuario_dto


class FrmCadUsuario(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)

        self.title('Cadastro Usuários')
        w = 645
        h = 380
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h  / 2
        self.geometry('%dx%d+%d+%d'%(w,h,x,y))
        self.resizable(False, False)
        self.grab_set()

        self.criar_widgets()
        self.listar()

    def criar_widgets(self):
        # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'

        # Váriavelis associado Widgets
        self.var_msg = StringVar()
        self.var_id = StringVar()
        self.var_nome = StringVar()
        self.var_usuario = StringVar()
        self.var_senha = StringVar()
        self.var_acesso = IntVar()

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID)
        fr1.place(x=10, y=10, height=50, width=625)

        fr2 = Frame(self, borderwidth=1, relief=SOLID)
        fr2.place(x=10, y=65, height=260, width=320)

        fr3 = Frame(self, borderwidth=1, relief=SOLID)
        fr3.place(x=335, y=65, height=260, width=300)

        fr4 = Frame(self, borderwidth=1, relief=SOLID)
        fr4.place(x=10, y=330, height=40, width=625)

        # Widgets do Frame fr1
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE')
        self.lbl_msg.pack(expand=True, fill=X)
        
        # Widgets do Frame fr2
        Label(fr2, font=fonte_padrao, text='ID:').place(x=5, y=5)
        self.lbl_id = Label(fr2, font=fonte_padrao,  bg='#C0C0C0', relief=SOLID, textvariable=self.var_id, anchor=W)
        self.lbl_id.place(x=5, y=25, width=100)

        Label(fr2, font=fonte_padrao, text='Nome:').place(x=5,y=50)
        self.txt_nome = Entry(fr2, font=fonte_padrao, textvariable=self.var_nome)
        self.txt_nome.place(x=5, y=70, width=300)

        Label(fr2, font=fonte_padrao, text='Usuário:').place(x=5, y=95)
        self.txt_usuario = Entry(fr2, font=fonte_padrao, textvariable=self.var_usuario)
        self.txt_usuario.place(x=5, y=120, width=300)

        Label(fr2, font=fonte_padrao, text='Senha:').place(x=5, y=145)
        self.txt_senha = Entry(fr2, font=fonte_padrao, show='*', textvariable=self.var_senha)
        self.txt_senha.place(x=5, y=170, width=300)

        Label(fr2, font=fonte_padrao, text='Acesso:').place(x=5, y=195)
        self.sp_acesso = Spinbox(fr2,from_=1, to=3, font=fonte_padrao, textvariable=self.var_acesso, state='readonly')
        self.sp_acesso.place(x=5, y=220, width=100)

        # Widgets do Frame fr3
        self.tree = ttk.Treeview(fr3)
        self.tree['columns'] = ('a', 'b')
        self.tree.column('#0', width=20, minwidth=20, stretch=NO)
        self.tree.column('a', width=80, minwidth=20, stretch=NO)

        self.tree.heading('a', text='ID', anchor='w')
        self.tree.heading('b', text='USUÁRIO', anchor='w')

        vsb_tree = Scrollbar(fr3, orient=VERTICAL, command=self.tree.yview)

        self.tree.bind('<<TreeviewSelect>>', self.item_selecionado)
        self.tree.configure(yscrollcommand=vsb_tree.set)
        
        vsb_tree.place(x=280, y=6, height=240)
        self.tree.place(x=5, y=5, width=270, height=240)

        # Widgets do Frame fr4
        self.btn_novo = Button(fr4, text='Novo', font=fonte_padrao, command=self.novo)
        self.btn_novo.place(x=5, y=5, width=80)
        self.btn_gravar = Button(fr4, text='Gravar', font=fonte_padrao, command=self.gravar)
        self.btn_gravar.place(x=95, y=5, width=80)
        self.btn_excluir = Button(fr4, text='Excluir', font=fonte_padrao, command=self.excluir, state='disabled')
        self.btn_excluir.place(x=185, y=5, width=80)

    def listar(self):
        bll = usuario_bll.UsuarioBll()
        r = bll.retornar_dados('todos')

        self.lst_dados = r
        self.tree.delete(*self.tree.get_children())
        for i in r:
            self.tree.insert('', 'end', text='', values=(str(i[0]), i[2]))

    def hab_des_widgets(self, nome, usuario, senha, gravar, excluir):
        self.txt_nome['state'] = nome
        self.txt_usuario['state'] = usuario
        self.txt_senha['state'] = senha
        self.btn_gravar['state'] = gravar
        self.btn_excluir['state'] = excluir

    def preparar(self):
        self.limpar_campos()
        self.hab_des_widgets('disabled','disabled','disabled','disabled','disabled')
        self.btn_novo.focus()

    def limpar_campos(self):
        self.var_id.set('')
        self.var_nome.set('')
        self.var_usuario.set('')
        self.var_senha.set('')
        self.var_msg.set('')

    def novo(self):
        self.limpar_campos()
        self.hab_des_widgets('normal','normal', 'normal', 'normal', 'disabled')
        self.txt_nome.focus()
        self.var_msg.set('Novo Registro')
        self.lbl_msg['fg'] = '#00008B'

    def gravar(self):
        obj = usuario_dto.UsuarioDto()
        obj.nome = self.var_nome.get()
        obj.usuario = self.var_usuario.get()
        obj.senha = self.var_senha.get()
        obj.acesso = self.var_acesso.get()

        bll = usuario_bll.UsuarioBll()
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
            self.listar()
        else:
            messagebox.showerror('Erro', str(r), parent=self)

    def excluir(self):
        res = messagebox.askquestion('Excluir', 'Deseja excluir este registro?', parent=self)
        if res == 'yes':
            bll = usuario_bll.UsuarioBll()
            ID = int(self.var_id.get())

            r = bll.excluir(ID)
            if r == 1:
                messagebox.showinfo('Excluído', 'Registro excluído com sucesso!', parent=self)
                self.preparar()
                self.listar()
            else:
                messagebox.showerror('Erro', str(r), parent=self) 

    def item_selecionado(self, event):
        ID = self.tree.focus()

        for i in self.lst_dados:
            if i.count(int(self.tree.item(ID)['values'][0])):
                self.var_id.set(str(i[0]))
                self.var_nome.set(i[1])
                self.var_usuario.set(i[2])
                self.var_senha.set(i[3])
                self.var_acesso.set(int(i[4]))

                self.var_msg.set('Alterar Registro')
                self.lbl_msg['fg'] = '#A52A2A'
                self.hab_des_widgets('normal', 'normal', 'normal', 'normal', 'normal')
                break
