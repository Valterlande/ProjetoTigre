from tkinter import *
from tkinter import messagebox
from Ferramentas import variaveis_globais
from datetime import date, timedelta
import os, random

class FrmAtivacao(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        w = 400
        h = 300
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d'%(w,h,x,y))
        self.title('Ativação')
        self.resizable(False, False)
        self.grab_set()

        self.criar_widgets()

    def criar_widgets(self):
          # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'

        # Variáveis
        self.var_msg = StringVar()
        self.var_dias = IntVar()
        self.var_chave = StringVar()

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID)
        fr1.place(x=10, y=10, height=50, width=380)

        fr2 = Frame(self, borderwidth=1, relief=SOLID)
        fr2.place(x=10, y=70, height=220, width=380)

        # Widgets do Frame fr1
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE', fg='#00008B')
        self.lbl_msg.pack(expand=True, fill=X)

        self.var_msg.set('Ativação do Sistema')

        # Widgets do Frame fr2
        Label(fr2, font=fonte_padrao, text='Qtd dias:').place(x=10, y=10)
        self.sp_dias = Spinbox(fr2, from_=10, to=90, font=fonte_padrao, state='readonly', textvariable=self.var_dias)
        self.sp_dias.focus()
        self.sp_dias.place(x=10, y=35, width=100)
    
        Label(fr2, font=fonte_padrao, text='Chave:').place(x=10, y=65)
        self.txt_chave = Entry(fr2, font=fonte_padrao, relief=SOLID, textvariable=self.var_chave,show='*')
        self.txt_chave.bind('<Return>', self.ativar)
        self.txt_chave.place(x=10, y=90, width=200)

        self.btn_ativar = Button(fr2, font=fonte_padrao, text='Ativar', command=self.ativar)
        self.btn_ativar.place(x=285, y=185, width=80)

    def ativar(self, event=None):
        if self.var_chave.get().upper() == variaveis_globais.CHAVE:
            caminho = 'Ferramentas\\'

            if not os.path.exists(caminho):
                messagebox.showerror('Erro', 'Erro ao ativar o sistema.\nContate o suporte', parent=self)
                return           

            dt_hj = date.today()
            dt_exp = date.fromordinal(dt_hj.toordinal()+self.var_dias.get()).strftime('%d-%m-%Y')

            arquivo = open(caminho+'tigre.txt', 'w')

            aux = 0
            tamanho = 10000
            while aux < tamanho:
                if aux == 1000:
                    arquivo.writelines(dt_exp[0:2])
                elif aux == 2000:
                    arquivo.writelines(dt_exp[3:5])
                elif aux == 3000:
                    arquivo.writelines(dt_exp[6:])
                else:
                    t = str(random.randint(0, 9))
                    arquivo.writelines(t)
                aux += 1

            #arquivo.write(dt_exp.strftime('%d-%m-%Y'))
            arquivo.close()

            messagebox.showinfo('Ativado', 'Sistema ativado com sucesso!', parent=self)
            variaveis_globais.ativado = True
            self.destroy()
        else:
            messagebox.showwarning('Inválida', 'Chave inválida', parent=self)
            self.var_chave.set('')
            return
