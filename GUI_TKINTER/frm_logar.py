from tkinter import *
from tkinter import messagebox
from Ferramentas import variaveis_globais
from BLL import usuario_bll


class FrmLogar(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        w = 350
        h = 400
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() /2 ) -  h / 2
        self.geometry('%dx%d+%d+%d'%(w,h,x,y))
        self.title('Logar')
        self.resizable(False, False)
        self.grab_set()
        self.transient(self.winfo_parent())

        self.criar_widgets()

    def criar_widgets(self):
         # Fonte padrão
        fonte_padrao = 'Verdana 12 bold'

        # Variáveis associados ao widgtes
        self.var_usu = StringVar()
        self.var_sen = StringVar()
 
        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID)
        fr1.place(x=10, y=10, height=50, width=330)

        fr2 = Frame(self, borderwidth=1, relief=SOLID)
        fr2.place(x=10, y=70, height=320, width=330)

        # Widgets do Frame fr1
        Label(fr1, text='LOGAR', font=('Tahoma 22 bold'), relief=RAISED, fg='#00008B', bg='#B0C4DE').pack(expand=True, fill=X)

        # Wigets do Frame fr2
        Label(fr2, font=fonte_padrao, text='Usuário: ').place(x=10, y=70)
        self.txt_usu = Entry(fr2, font=fonte_padrao, relief='solid', textvariable=self.var_usu)
        self.txt_usu.bind('<Return>', self.logar)
        self.txt_usu.place(x=10, y=100, width=305)
        self.txt_usu.focus()

        Label(fr2, font=fonte_padrao, text='Senha: ').place(x=10, y=150)
        self.txt_sen = Entry(fr2, font=fonte_padrao, relief='solid',show='*', textvariable=self.var_sen)
        self.txt_sen.bind('<Return>', self.logar)
        self.txt_sen.place(x=10, y=180, width=305)

        self.btn_logar = Button(fr2, font=fonte_padrao, text='Logar', command=self.logar)
        self.btn_logar.place(x=235, y=275, width=80)

    def logar(self, event=None):
        if self.var_usu.get() == '' or self.var_sen.get() == '':
            messagebox.showwarning('Aviso', 'O campo usuario e senha é de preenchimento obrigatório!', parent=self)
            return

        bll = usuario_bll.UsuarioBll()
        r = bll.retornar_dados('usuario+senha', prms=(self.var_usu.get(), self.var_sen.get()))

        if r != []:
            variaveis_globais.usu_id = r[0][0]
            variaveis_globais.usu_nome = r[0][1]
            variaveis_globais.usu_usuario = r[0][2]
            variaveis_globais.usu_acesso = r[0][4]
            variaveis_globais.logado = True
            variaveis_globais.cont = 0
            self.destroy()
        else:
           messagebox.showwarning('Aviso', 'Usuário ou senha inválido(s)', parent=self)
           self.var_usu.set('')
           self.var_sen.set('')
           self.txt_usu.focus()
