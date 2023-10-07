from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from BLL import tip_material_bll, mod_produto_bll
from DTO import mod_produto_dto


class FrmCadModProduto(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)

        self.title('Cadastro de Modelo Produto')

        w = 520
        h = 450
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d'%(w,h,x,y))
        self.resizable(0, 0)
        self.grab_set()

        self.dic_tipo = {}

        self.var_id = StringVar()
        self.var_tipo = StringVar()
        self.var_descricao = StringVar()
        self.var_msg = StringVar()

        self.criar_widgets()

        self.carregar_tipo()
        self.preparar()

    def limpar_campos(self):
        self.var_id.set('')
        self.var_descricao.set('')
        self.var_msg.set('')

    def preparar(self):
        self.limpar_campos()
        self.listar('todos')
        self.txt_descricao['state'] = 'disabled'
        self.cb_tipo['state'] = 'disabled'
        self.btn_gravar['state'] = 'disabled'
        self.btn_excluir['state'] = 'disabled'

    def carregar_tipo(self):
        bll = tip_material_bll.TipMaterialBll()
        r = bll.retornar_dados('todos')
        lst = []
        for i in r:
            lst.append(str(i[1]))
            self.dic_tipo[str(i[1])] = int(i[0])

        self.cb_tipo['values'] = lst
        self.cb_tipo.current(0)

    def listar(self, tipo, prms=None):
        self.lst_mod = []
        bll = mod_produto_bll.ModProdutoBll()
        r = bll.retornar_dados(tipo, prms)
        
        self.treeview.delete(*self.treeview.get_children())
        for i in r:
            self.lst_mod.append(i)
            self.treeview.insert('', 'end', text='', values=(str(i[0]), str(i[2])))

    def criar_widgets(self):
        fonte_padrao =  'Verdana 10 bold'

        fr0 = Frame(self, relief=SOLID, borderwidth=1)
        fr0.place(x=10, y=10, width=500, height=50)

        fr1 = Frame(self, relief=SOLID, borderwidth=1)
        fr1.place(width=500, height=370, x=10, y=70)

        self.lbl_msg = Label(fr0, font=('Tahoma 22 bold'),relief=RAISED, bg='#B0C4DE', textvariable=self.var_msg)
        self.lbl_msg.pack(expand=True, fill=X)

        Label(fr1, text='ID:', font=fonte_padrao).place(x=10, y=10)
        self.lbl_id = Label(fr1, font=fonte_padrao, width=15, relief=SOLID, bg='#C0C0C0', textvariable=self.var_id, anchor=W)
        self.lbl_id.place(x=10, y=30)

        Label(fr1, text='Tipo Material:', font=fonte_padrao).place(x=160, y=10)
        self.cb_tipo = ttk.Combobox(fr1, font=fonte_padrao, textvariable=self.var_tipo)
        self.cb_tipo.place(x=160, y=30)

        Label(fr1, text='Descrição:', font=fonte_padrao).place(x=10, y=55)
        self.txt_descricao = Entry(fr1, font=fonte_padrao, width=50, textvariable=self.var_descricao)
        self.txt_descricao.place(x=10, y=80)

        self.treeview = ttk.Treeview(fr1)
        self.treeview['columns'] = ('um', 'dois')
        self.treeview.column('#0', width=20, minwidth=20, stretch=NO)
        self.treeview.column('um', width=50, minwidth=20, stretch=NO)

        self.treeview.heading('um', text='ID', anchor=W)
        self.treeview.heading('dois', text='DESCRIÇÃO', anchor=W)

        vsb = ttk.Scrollbar(fr1, orient=VERTICAL, command=self.treeview.yview)

        self.treeview.configure(yscrollcommand=vsb.set)

        self.treeview.bind('<<TreeviewSelect>>', self.item_selecionado)

        vsb.place(x=460, y=120, height=200)
        self.treeview.place(x=10, y=120, width=460, height=200)

        self.btn_novo = Button(fr1, text='Novo', font=fonte_padrao, width=7, command=self.novo)
        self.btn_novo.place(x=10, y=330)
        self.btn_gravar = Button(fr1, text='Gravar', font=fonte_padrao, width=7, command=self.gravar)
        self.btn_gravar.place(x=90, y=330)
        self.btn_excluir = Button(fr1, text='Excluir', font=fonte_padrao, width=7, command=self.excluir)
        self.btn_excluir.place(x=170, y=330)

    def item_selecionado(self, event):
        ID = self.treeview.focus()

        for i in self.lst_mod:
            if i.count(int(self.treeview.item(ID)['values'][0])):
                self.var_id.set(str(i[0]))
                self.var_tipo.set(i[1])
                self.var_descricao.set(i[2])

                self.txt_descricao['state'] = 'normal'
                self.cb_tipo['state'] = 'normal'
                self.btn_gravar['state'] = 'normal'
                self.btn_excluir['state'] = 'normal'

                self.var_msg.set('Alterar Registro')
                self.lbl_msg['fg'] = '#A52A2A'

    def novo(self):
        self.txt_descricao['state'] = 'normal'
        self.cb_tipo['state'] = 'readonly'
        self.btn_gravar['state'] = 'normal'
        self.btn_excluir['state'] = 'disabled'

        self.var_descricao.set('')
        self.var_id.set('')

        self.txt_descricao.focus()

        self.var_msg.set('Novo Registro')
        self.lbl_msg['fg'] = '#00008B'

    def gravar(self):
        obj = mod_produto_dto.ModProdutoDto()
        obj.tipo = self.dic_tipo[self.var_tipo.get()]
        obj.descricao = self.var_descricao.get().upper()

        bll = mod_produto_bll.ModProdutoBll()
        v = bll.validar_campo(obj)
        if v != 's':
            messagebox.showwarning('Aviso',str(v), parent=self)
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
        p = messagebox.askquestion('Excluir', 'Deseja excluir este registro', parent=self)
        if p == 'yes':
            ID = int(self.var_id.get())
            bll = mod_produto_bll.ModProdutoBll()
            r = bll.excluir(ID)
            if r == 1:
                messagebox.showinfo('Excluído', 'Registro excluído com sucesso!', parent=self)
                self.preparar()
            else:
                messagebox.showerror('Erro', str(r), parent=self)
