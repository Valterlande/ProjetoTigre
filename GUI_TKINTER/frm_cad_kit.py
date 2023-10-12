from tkinter import *
from tkinter import messagebox, ttk
from BLL import kit_bll, material_bll
from DTO import kit_dto


class FrmCadKit(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        w = 550
        h = 520
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d'%(w,h,x,y))
        self.resizable(0, 0)
        self.grab_set()

        self.title('Cadastro Kit')

        self.dic_material = {}

        self.criar_widgets()
        self.carregar_material()
        self.listar()

    def criar_widgets(self):
        # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'

        # Variáveis acossiada aos widgtes
        self.var_id = StringVar()
        self.var_codigo = StringVar()
        self.var_material = StringVar()
        self.var_descricao = StringVar()
        self.var_busca = StringVar()
        self.var_msg = StringVar()

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID)
        fr1.place(x=10, y=10, height=50, width=530)

        fr2 = Frame(self, borderwidth=1, relief=SOLID)
        fr2.place(x=10, y=70, height=150, width=530)

        fr3 = Frame(self, borderwidth=1, relief=SOLID)
        fr3.place(x=10, y=230, height=280, width=530)

        limitar = self.register(func=self.limitar_campo)

        # Widgets do Frame fr1
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE')
        self.lbl_msg.pack(expand=True, fill=X)

        # Widgets do Frame fr2
        Label(fr2, font=fonte_padrao, text='ID:').place(x=10, y=10)
        self.lbl_id = Label(fr2, font=fonte_padrao, relief=SOLID, bg='#C0C0C0', textvariable=self.var_id, anchor=W)
        self.lbl_id.place(x=10, y=30, width=100)

        Label(fr2, font=fonte_padrao, text='Código:').place(x=120, y=10)
        self.txt_codigo = Entry(fr2, font=fonte_padrao, textvariable=self.var_codigo, validate='key', validatecommand=(limitar, '%P'))
        self.txt_codigo.place(x=120, y=30, width=100)

        Label(fr2, font=fonte_padrao, text='Material:').place(x=10, y=55)
        self.cb_material = ttk.Combobox(fr2, font=fonte_padrao, textvariable=self.var_material, state='readonly')
        self.cb_material.place(x=10, y=75, width=510)

        Label(fr2, font=fonte_padrao, text='Descrição:').place(x=10, y=100)
        self.txt_descricao = Entry(fr2, font=fonte_padrao, textvariable=self.var_descricao)
        self.txt_descricao.place(x=10, y=120, width=510)

        # Widgets do Farme fr3
        self.txt_busca = Entry(fr3, font=fonte_padrao, textvariable=self.var_busca, validate='key', validatecommand=(limitar, '%P'))
        self.txt_busca.bind('<Return>', self.listar)
        self.txt_busca.place(x=10, y=10, width=100)

        self.btn_buscar = Button(fr3, font=fonte_padrao, text='Buscar', command=self.listar)
        self.btn_buscar.place(x=120, y=10, width=80)

        self.tree = ttk.Treeview(fr3, columns=('a', 'b'))
        self.tree.column('#0', width=20, minwidth=20, stretch=NO)
        self.tree.column('a', width=80, minwidth=80, stretch=NO)

        self.tree.heading('a', text='CÓDIGO', anchor=W)
        self.tree.heading('b', text='DESCRIÇÃO', anchor=W)

        vsb = ttk.Scrollbar(fr3, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.bind('<<TreeviewSelect>>', self.item_selecionado)

        vsb.place(x=510, y=45, height=180)
        self.tree.place(x=10, y=45, height=180, width=500)

        self.btn_novo = Button(fr3, font=fonte_padrao, text='Novo', command=self.novo)
        self.btn_novo.place(x=10,y=240, width=80)
        self.btn_gravar = Button(fr3, font=fonte_padrao, text='Gravar', command=self.gravar)
        self.btn_gravar.place(x=100,y=240, width=80)
        self.btn_excluir = Button(fr3, font=fonte_padrao, text='Excluir', command=self.excluir)
        self.btn_excluir.place(x=190,y=240, width=80)

    def limitar_campo(self, t):
        if len(t) > 6:
            return False
        return True

    def limpar_campos(self):
        self.var_id.set('')
        self.var_codigo.set('')
        self.var_descricao.set('')
        self.var_msg.set('')

    def listar(self, event=None):
        bll = kit_bll.KitBll()
        r = bll.retornar_dados('codigo%', '%'+self.var_busca.get()+'%')

        self.lst_dados = r

        self.tree.delete(*self.tree.get_children())
        for i in r:
            self.tree.insert('', 'end', text='', values=(i[1], i[4]))
        
        self.btn_novo.focus()

    def carregar_material(self):
        lst = []
        bll = material_bll.MaterialBll()
        r = bll.retornar_dados('todos')
        for i in r:
            lst.append(i[1]+' - '+i[3])
            self.dic_material[i[1]+' - '+i[3]] = i[0]

        self.cb_material['values'] = lst
        self.cb_material.current(0)

    def novo(self):
        self.limpar_campos()
        self.txt_codigo.focus()

        self.var_msg.set('Novo Registro')
        self.lbl_msg['fg'] = '#00008B'

    def gravar(self):
        obj = kit_dto.KitDto()
        obj.codigo = self.var_codigo.get()
        obj.material = self.dic_material[self.var_material.get()]
        obj.descricao = self.var_descricao.get()

        bll = kit_bll.KitBll()
        v = bll.validar_campos(obj)
        if v != 'ok':
            messagebox.showwarning('Aviso', str(v), parent=self)
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
            self.limpar_campos()
            self.listar()
        else:
            messagebox.showerror('Erro', str(r), parent=self)

    def excluir(self):
        res = messagebox.askquestion('Excluir', 'Deseja excluir este registro?', parent=self)
        if res == 'yes':
            ID = int(self.var_id.get())
            bll = kit_bll.KitBll()
            r = bll.excluir(ID)
            if r == 1:
                messagebox.showinfo('Excluído', 'Registro excluído com sucesso!', parent=self)
                self.limpar_campos()
                self.listar()
            else:
                messagebox.showerror('Erro', str(r), parent=self)

    def item_selecionado(self, event=None):
        ID = self.tree.focus()

        for i in self.lst_dados:
            if i.count(str(self.tree.item(ID)['values'][0])):
                self.var_id.set(str(i[0]))
                self.var_codigo.set(i[1])
                self.var_material.set(i[2] + ' - ' + i[3])
                self.var_descricao.set(i[4])

                self.var_msg.set('Alterar Registro')
                self.lbl_msg['fg'] = '#A52A2A'
                continue
