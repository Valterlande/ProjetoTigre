from tkinter import *
from tkinter import messagebox, ttk
from BLL import tip_material_bll, mod_produto_bll, tela_bll
from DTO import tela_dto
import random


class FrmCadTela(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        w = 610
        h = 550
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title('Cadastro de Tela')
        self.resizable(False, False)
        self.grab_set()

        self.dic_tipo = {}
        self.dic_modelo = {}

        self.criar_widgets()
        self.carregar_tipos()
        self.carregar_modelos()
        self.listar()

    def criar_widgets(self):
        # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'
        
        # Variáveis ligadas as Widgtes
        self.var_msg = StringVar()
        self.var_id = StringVar()
        self.var_tipo = StringVar()
        self.var_modelo = StringVar()
        self.var_descricao = StringVar()
        self.var_prateleira = StringVar()
        self.var_busca = StringVar()
        self.var_rb = IntVar()

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID)
        fr1.place(x=10, y=10, height=50, width=590)

        fr2 = Frame(self, borderwidth=1, relief=SOLID)
        fr2.place(x=10, y=70, height=180, width=590)

        fr3 = Frame(self, borderwidth=1, relief=SOLID)
        fr3.place(x=10, y=260, height=280, width=590)

        # Widgets do Frame fr1
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE')
        self.lbl_msg.pack(expand=True, fill=X)
        
        # Widgets do Frame fr2
        Label(fr2, font=fonte_padrao, text='ID:').place(x=10, y=10)
        self.lbl_id = Label(fr2, font=fonte_padrao, relief=SOLID, bg='#C0C0C0', textvariable=self.var_id, anchor=W)
        self.lbl_id.place(x=10, y=30, width=100)

        Label(fr2, font=fonte_padrao, text='Tipo:').place(x=120, y=10)
        self.cb_tipo = ttk.Combobox(fr2, font=fonte_padrao, textvariable=self.var_tipo, state='readonly')
        self.cb_tipo.bind('<<ComboboxSelected>>', self.carregar_modelos)
        self.cb_tipo.place(x=120, y=30, width=100)

        Label(fr2, font=fonte_padrao, text='Modelo:').place(x=230, y=10)
        self.cb_modelo = ttk.Combobox(fr2, font=fonte_padrao, textvariable=self.var_modelo, state='readonly')
        self.cb_modelo.place(x=230, y=30, width=350)

        Label(fr2, font=fonte_padrao, text='Descrição:').place(x=10,y=55)
        self.txt_descricao = Entry(fr2, font=fonte_padrao, textvariable=self.var_descricao)
        self.txt_descricao.place(x=10, y=75, width=350)

        Label(fr2, font=fonte_padrao, text='Prateleira:').place(x=370,y=55)
        self.txt_prateleira = Entry(fr2, font=fonte_padrao, textvariable=self.var_prateleira)
        self.txt_prateleira.place(x=370, y=75, width=210)

        Label(fr2, font=fonte_padrao, text='Obs:').place(x=10,y=90)
        self.text_obs = Text(fr2, font=fonte_padrao, height=3)
        self.text_obs.place(x=10, y=110, width=570)

        # Widgets do Frame fr3
        self.rb_id = Radiobutton(fr3, font=fonte_padrao, text='ID', variable=self.var_rb, value=0, command=self.rb)
        self.rb_id.place(x=10, y=10)

        self.rb_descricao = Radiobutton(fr3, font=fonte_padrao, text='Descrição', variable=self.var_rb, value=1, command=self.rb)
        self.rb_descricao.place(x=60, y=10)
        self.rb_descricao.select()

        self.txt_busca = Entry(fr3, font=fonte_padrao, textvariable=self.var_busca)
        self.txt_busca.bind('<Return>', self.listar)
        self.txt_busca.place(x=170, y=10)

        self.btn_buscar = Button(fr3, font=fonte_padrao, text='Buscar', command=self.listar)
        self.btn_buscar.place(x=360, y=10, width=80)

        self.tree = ttk.Treeview(fr3, columns=('a', 'b'))
        self.tree.column('#0', width=20, minwidth=20, stretch=NO)
        self.tree.column('a', width=80, minwidth=20, stretch=NO)

        self.tree.heading('a', text='ID', anchor=W)
        self.tree.heading('b', text='DESCRIÇÃO', anchor=W)

        vsb = ttk.Scrollbar(fr3, orient=VERTICAL, command=self.tree.yview)

        self.tree.bind('<<TreeviewSelect>>', self.item_selecionado)
        self.tree.configure(yscrollcommand=vsb.set)

        vsb.place(x=565, y=45, height=180)
        self.tree.place(x=10, y=45, width=556, height=180)

        self.btn_novo = Button(fr3, font=fonte_padrao, text='Novo', command=self.novo)
        self.btn_novo.place(x=10, y=240, width=80)
        self.btn_gravar = Button(fr3, font=fonte_padrao, text='Gravar', command=self.gravar)
        self.btn_gravar.place(x=100, y=240, width=80)
        self.btn_excluir = Button(fr3, font=fonte_padrao, text='Excluir', command=self.excluir)
        self.btn_excluir.place(x=190, y=240, width=80)

    def carregar_tipos(self):
        lst = []
        bll = tip_material_bll.TipMaterialBll()
        r = bll.retornar_dados('todos')
        for i in r:
            lst.append(i[1])
            self.dic_tipo[i[1]] = i[0]

        self.cb_tipo['values'] = lst
        self.cb_tipo.current(random.randint(0, (len(lst)-1)))

    def carregar_modelos(self, event=None):
        lst = []
        bll = mod_produto_bll.ModProdutoBll()
        r = bll.retornar_dados('tipo', self.var_tipo.get())
        for i in r:
            lst.append(i[2])
            self.dic_modelo[i[2]] = i[0]

        self.cb_modelo['values'] = lst
        self.cb_modelo.current(random.randint(0, (len(lst)-1)))

    def limpar_campos(self):
        self.var_id.set('')
        self.var_descricao.set('')
        self.var_prateleira.set('')
        self.text_obs.delete('1.0', END)
        self.var_msg.set('')

    def novo(self):
        self.limpar_campos()
        self.btn_excluir['state'] = 'disabled'
        self.cb_tipo.focus()

        self.var_msg.set('Novo Registro')
        self.lbl_msg['fg'] = '#00008B'

    def rb(self):
        self.limpar_campos()
        self.var_busca.set('')
        self.txt_busca.focus()

    def gravar(self):
        obj = tela_dto.TelaDto()
        obj.tipo = self.dic_tipo[self.var_tipo.get()]
        obj.modelo = self.dic_modelo[self.var_modelo.get()]
        obj.descricao = self.var_descricao.get()
        obj.prateleira = self.var_prateleira.get().upper()
        obj.obs = self.text_obs.get('1.0', END)

        bll = tela_bll.TelaBll()
        v = bll.validar_campos(obj)
        if v != 'ok':
            messagebox.showwarning('Aviso', str(v), parent=self)
            return

        if self.var_id.get() ==  '':
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
        p = messagebox.askquestion('Excluir', 'Deseja excluir este registro?', parent=self)
        if p == 'yes':
            ID = int(self.var_id.get())
            bll = tela_bll.TelaBll()
            r = bll.excluir(ID)
            if r == 1:
                messagebox.showinfo('Excluído', 'Registro excluído com sucesso!', parent=self)
                self.limpar_campos()
                self.listar()
            else:
                messagebox.showerror('Erro', str(r), parent=self)

    def listar(self, event=None):
        if self.var_rb.get() == 0:
            tipo = 'id'
            prms = self.var_busca.get()
        elif self.var_rb.get() == 1:
            tipo = 'descricao'
            prms = '%'+self.var_busca.get()+'%'

        self.lst_dados = []
        bll = tela_bll.TelaBll()
        r = bll.retornar_dados(tipo, prms)
        self.lst_dados = r
        self.tree.delete(*self.tree.get_children())

        for i in r:
            self.tree.insert('', 'end', text='', values=(str(i[0]), i[3]))

    def item_selecionado(self, event):
        ID = self.tree.focus()
        self.text_obs.delete('1.0', END)

        for i in self.lst_dados:
            if i.count(self.tree.item(ID)['values'][0]):
                self.var_id.set(str(i[0]))
                self.var_tipo.set(i[1])
                self.carregar_modelos()
                self.var_modelo.set(i[2])
                self.var_descricao.set(i[3])
                self.var_prateleira.set(i[4])
                self.text_obs.insert(END, i[5])
                self.btn_excluir['state'] = 'normal'

                self.var_msg.set('Alterar Registro')
                self.lbl_msg['fg'] = '#A52A2A'
                break
