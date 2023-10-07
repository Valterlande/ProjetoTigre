from tkinter import *
from Ferramentas import variaveis_globais


class FrmSobre(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        self.title('Sobre: {}'.format(variaveis_globais.NOME_APP))
        w = 400
        h = 300
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d'%(w,h,x,y))
        self.resizable(0, 0)
        self.grab_set()

        self.criar_widgets()
        self.seta_texto()

    def criar_widgets(self):
        # Fonte padrão
        fonte_padrao = 'Consolas 11 bold'

        # Variáveis
        self.var_msg = StringVar()

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID, bg='#B0C4DE')
        fr1.place(x=10, y=10, height=280, width=380)

        fr2 = Frame(fr1, bg='#B0C4DE')
        fr2.pack(side=BOTTOM, fill=X)

        # Widgets do Frmae fr1
        lbl_msg = Label(fr1, font=fonte_padrao, textvariable=self.var_msg, justify=LEFT, bg='#B0C4DE')
        lbl_msg.pack(expand=YES, fill=BOTH)

        btn_sair = Button(fr2, font=fonte_padrao, text='Sair', width=8, command=self.sair, relief=GROOVE)
        btn_sair.pack(side=RIGHT, padx=10, pady=10)

    def seta_texto(self):
        msg ='{}\n\nVersão: {}\n\nDesenvolvido por:. Valterlande Mendes\nFeito em: ........ Python3, tkinter\nBanco de Dados:... SQLite3\n\nÚltima Atualização: 06/08/2020'.format(
            variaveis_globais.NOME_APP, variaveis_globais.VERSAO)

        self.var_msg.set(msg)

    def sair(self):
        self.destroy()
