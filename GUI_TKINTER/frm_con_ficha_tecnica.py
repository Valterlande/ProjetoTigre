from tkinter import *
from tkinter import messagebox, ttk
import subprocess, os, glob, random, webbrowser


class FrmConFichaTecnica(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        self.title('Consulta Ficha Técnica')
        w = 410
        h = 300
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d' %(w, h, x, y))
        self.resizable(0, 0)
        self.grab_set()

        self.criar_widgets()
        self.listar_arquivos()

    def criar_widgets(self):
        # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'

        # Variáveis
        self.var_msg = StringVar()
        self.var_arquivo = StringVar()

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID)
        fr1.place(x=10, y=10, height=50, width=390)

        fr2 = Frame(self, borderwidth=1, relief=SOLID)
        fr2.place(x=10, y=70, height=220, width=390)

        # Widgets do Frame fr1
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED, bg='#B0C4DE')
        self.lbl_msg.pack(expand=True, fill=X)

        self.var_msg.set('Consulta de Ficha Técnica')
        self.lbl_msg['fg'] = '#00008B'

        # Widgets do Frame fr2
        self.lst_arquivos = Listbox(fr2, font=fonte_padrao, relief=SOLID,listvariable=self.var_arquivo)
        vsb = Scrollbar(fr2, orient=VERTICAL, command=self.lst_arquivos.yview)
        self.lst_arquivos.configure(yscrollcommand=vsb.set)
        vsb.place(x=365, y=10, height=160)
        self.lst_arquivos.place(x=10, y=10, width=355, height=160)

        self.btn_verificar = Button(fr2, font=fonte_padrao, text='Verificar', command=self.verificar)
        self.btn_verificar.place(x=300, y=180, width=80)

    def listar_arquivos(self):
        self.caminho = 'C:\\Produtos\\'
        if not os.path.exists(self.caminho):
            messagebox.showerror('Erro', 'O sistema não coseguiu encontar o caminho do arquivos.\nContate o suporte.', parent=self)
            return

        for i in glob.glob(os.path.join(self.caminho, '*.pdf')):
            self.lst_arquivos.insert(END, i[12:-4])

        self.lst_arquivos.focus()
        self.lst_arquivos.selection_set(0)

    def verificar(self):
        try:
            nome_arquivo = self.lst_arquivos.get(ACTIVE)
            subprocess.Popen(self.caminho+nome_arquivo+'.pdf', shell=True)
            #webbrowser.open('https://kron.com.br/produto/transdutor-analogico-de-corrente-ca/', new=0, autoraise=True)

        except Exception as ex:
            messagebox.showerror('Erro', 'Erro ao tentar abrir o arquivo.\nErro: {}'.format(ex), parent=self)
            return
