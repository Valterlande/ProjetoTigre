from tkinter import *
from tkinter import messagebox
from Ferramentas import variaveis_globais, funcoes
from GUI import frm_preferencia


class FrmAutPreferencia(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        self.iconbitmap(variaveis_globais.CAMINHO_IMAGEM_ICONES + 'icone_ativar'+variaveis_globais.preferencia_img+'.ico')
        w = 250
        h = 250
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d'%(w,h,x,y))
        self.title('Preferências')
        self.resizable(False, False)
        self.grab_set()

        self.tetativas = 3

        self.criar_widgets()

    def criar_widgets(self):
          # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'

        # Variáveis
        self.var_chave = StringVar()
        self.var_msg = StringVar()

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID)
        fr1.place(x=10, y=10, height=50, width=230)

        fr2 = Frame(self, borderwidth=1, relief=SOLID)
        fr2.place(x=10, y=70, height=170, width=230)

        # Widgets do Frame fr1
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE', fg='#00008B')
        self.lbl_msg.pack(expand=True, fill=X)

        self.var_msg.set('Autorizaçao')

        # Widgets do Frame fr2
        Label(fr2, font=fonte_padrao, text='Chave:').place(x=10, y=10)
        self.txt_chave = Entry(fr2, font=fonte_padrao, relief=SOLID, textvariable=self.var_chave, show='*')
        self.txt_chave.bind('<Return>', self.confirmar)
        self.txt_chave.focus()
        self.txt_chave.place(x=10, y=35, width=210)

        self.btn_confirmar = Button(fr2, font=fonte_padrao, text='Confirmar', command=self.confirmar)
        self.btn_confirmar.place(x=130, y=135, width=90)

        funcoes.carregar_cores(self, self.lbl_msg)

    def confirmar(self, event=None):
        self.tetativas -= 1
        if self.var_chave.get() == '':
            messagebox.showwarning('Aviso', 'O campo chave de ser preenchido', parent=self)
            return
        if self.var_chave.get().upper() == variaveis_globais.CHAVE:
            frm_preferencia.FrmPreferencia(permissao=True)
            self.destroy()
        else:
            messagebox.showwarning('Aviso', 'Chave incorreta.', parent=self)
            if self.tetativas <= 0:
                messagebox.showwarning('Aviso','Tentativas de autorização encerradas.', parent=self)
                self.destroy()
            else:
                self.var_chave.set('')
