from tkinter import *
from GUI import frm_principal
from Ferramentas import variaveis_globais

class SplashScreen(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        cor_fundo = '#BDB76B'
        cor_titulo = '#2F4F4F'

        # Variável
        var_msg = StringVar()
        var_versao = StringVar()

        w = 500
        h = 400
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        var_msg.set('Carregando...')
        var_versao.set('Versão: {}'.format(variaveis_globais.VERSAO))

        self.cont = 0
        def conta_tempo():
            if self.cont == 2:
                var_msg.set('Pronto! ☺')
            elif self.cont == 3:
                
                self.master.destroy()
                frm_principal.FrmPrincipal()
            self.cont += 1
            self.after(1000, conta_tempo)

        self.pack(side=TOP, fill=BOTH, expand=YES)
        self.config(bg=cor_fundo)

        lbl_msg = Label(self, textvariable=var_msg, font='Tahoma 11 bold', anchor=W, bg=cor_fundo)
        lbl_msg.pack(fill=X)
        lbl_versao = Label(self, textvariable=var_versao, font='Tahoma 11 bold', bg=cor_fundo)
        lbl_versao.pack(fill=X)
        lbl_titulo = Label(self, text=variaveis_globais.NOME_APP, font='Tahoma 46 bold', bg=cor_fundo, fg=cor_titulo)
        lbl_titulo.pack(side=TOP, expand=YES)

        self.master.overrideredirect(True)
        self.lift()

        conta_tempo()
