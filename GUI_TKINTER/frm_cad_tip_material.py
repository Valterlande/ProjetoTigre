from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from BLL import tip_material_bll
from DTO import tip_material_dto


class FrmCadTipMaterial(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)

        self.title('Cadastro de Tipo de Material')
        w = 440
        h = 450
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d' %(w, h, x, y))

        self.resizable(0,0)
        self.grab_set()

        self.var_descricao = StringVar()
        self.var_id = StringVar()
        self.var_msg = StringVar()

        self.criar_widgets()

        self.preparar()

    def limpar(self):
        self.var_id.set('')
        self.var_descricao.set('')
        self.var_msg.set('')

    def preparar(self):
        self.limpar()
        self.txt_descricao['state'] = 'disabled'
        self.btn_gravar['state'] = 'disabled'
        self.btn_excluir['state'] = 'disabled'
        self.listar()

    def criar_widgets(self):
        fonte_padrao =  'Verdana 10 bold'

        fr0 = Frame(self, borderwidth=1, relief=SOLID)
        fr0.place(height=50, width=420, x=10, y=10)

        frm = Frame(self, borderwidth=1, relief=SOLID)
        frm.place(height=370, width=420, x=10, y= 70)

        self.lbl_msg = Label(fr0, text='', textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, width=15, bg='#B0C4DE')
        self.lbl_msg.pack(expand=True, fill=X)

        Label(frm, text='ID:', font=fonte_padrao).place(x=10, y=10)
        self.lbl_id = Label(frm, font=fonte_padrao, relief=SOLID, width=15, textvariable=self.var_id, anchor=W, bg='#C0C0C0')
        self.lbl_id.place(x=10, y=30)

        Label(frm, text='Descrição:', font=fonte_padrao).place(x=10, y=60)
        self.txt_descricao = Entry(frm, font=fonte_padrao, width=25, relief=SOLID, textvariable=self.var_descricao)
        self.txt_descricao.place(x=10, y=80)

        self.treeview = ttk.Treeview(frm, columns=('a'))
        self.treeview.column('#0', width=5)
        self.treeview.heading('#0', text='ID', anchor=W)
        self.treeview.heading('#1', text='DESCRIÇÃO', anchor=W)

        vsb = ttk.Scrollbar(frm, orient=VERTICAL, command=self.treeview.yview)

        self.treeview.configure(yscrollcommand=vsb.set)

        self.treeview.bind('<<TreeviewSelect>>', self.item_selecionado)

        vsb.place(x=385, y=120, height=200)
        self.treeview.place(x=10, y=120, width=385, height=200)

        self.btn_novo = Button(frm, text='Novo', font=fonte_padrao, width=7, command=self.novo)
        self.btn_novo.place(x=10, y=330)
        self.btn_gravar = Button(frm, text='Gravar', font=fonte_padrao, width=7, command=self.gravar)
        self.btn_gravar.place(x=90, y=330)
        self.btn_excluir = Button(frm, text='Excluir', font=fonte_padrao, width=7, command=self.excluir)
        self.btn_excluir.place(x=170, y=330)

    def listar(self):
        bll = tip_material_bll.TipMaterialBll()
        r = bll.retornar_dados('todos')

        self.treeview.delete(*self.treeview.get_children())

        for i in r:
            self.treeview.insert('', 'end', text=str(i[0]), values=(i[1]))

    def novo(self):
        self.limpar()
        self.txt_descricao.focus()
        self.txt_descricao['state'] = 'normal'
        self.btn_gravar['state'] = 'normal'
        self.btn_excluir['state'] = 'disabled'
        self.var_msg.set('Novo Registro')
        self.lbl_msg['fg'] = '#00008B'

    def excluir(self):
        p = messagebox.askquestion('Excluir', 'Deseja excluir este registro?', parent=self)
        if p == 'yes':
            bll = tip_material_bll.TipMaterialBll()
            ID = int(self.var_id.get())
            r = bll.excluir(ID)
            if r == 1:
                messagebox.showinfo('Excluído', 'Registro excluído com sucesso!', parent=self)
                self.preparar()
            else:
                messagebox.showerror('Erro', str(r), parent=self)

    def gravar(self):
        obj = tip_material_dto.TipMaterialDto()
        obj.descricao = self.var_descricao.get().upper()
        ID = self.var_id.get()
        bll = tip_material_bll.TipMaterialBll()
        v = bll.validar_campo(obj)
        if v != 'OK':
            messagebox.showwarning('Aviso', str(v), parent=self)
            return
        
        if ID == '':
            r = bll.inserir(obj)
            msg = 'Registro incluído com sucesso!'
        else:
            obj.ID = int(ID)
            r = bll.editar(obj)
            msg = 'Registro alterado com sucesso!'

        if r == 1:
            messagebox.showinfo('Gravado', msg, parent=self)
            self.preparar()
        else:
            messagebox.showerror('Erro', str(r), parent=self)

    def item_selecionado(self, event):
        ID = self.treeview.focus()
        tupla = (int(self.treeview.item(ID)['text']), str(self.treeview.item(ID)['values'][0]))

        self.var_id.set(str(tupla[0]))
        self.var_descricao.set(str(tupla[1]))

        self.txt_descricao['state'] = 'normal'
        self.btn_gravar['state'] = 'normal'
        self.btn_excluir['state'] = 'normal'

        self.var_msg.set('Alterar Registro')
        self.lbl_msg['fg'] = '#A52A2A'
