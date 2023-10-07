from tkinter import *
from tkinter import filedialog, messagebox, ttk
import os
from Ferramentas import variaveis_globais, funcoes


class FrmPreferencia(Toplevel):
    def __init__(self, permissao):
        Toplevel.__init__(self)

        self.iconbitmap(variaveis_globais.CAMINHO_IMAGEM_ICONES + 'icone_preferencia'+variaveis_globais.preferencia_img+'.ico')
        w = 500
        h = 500
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d'%(w,h,x,y))
        self.title('Preferências')
        self.resizable(False, False)
        self.grab_set()

        self.dic = {'Clássico':'_1', 'Alegre':'_2', 'Moderno':'_3'}

        self.criar_widgets()

        self.carregar_preferencias()

        self.bloquear(permissao=permissao)

    def criar_widgets(self):
          # Fonte padrão
        fonte_padrao = 'Verdana 10 bold'

        # Variáveis
        self.var_msg = StringVar()
        self.var_caminho_fichas = StringVar()
        self.var_caminho_banco = StringVar()
        self.var_icone = StringVar()
        self.var_tema = StringVar()

        # Frames
        fr1 = Frame(self, borderwidth=1, relief=SOLID)
        fr1.place(x=10, y=10, height=50, width=480)

        fr2 = Frame(self, borderwidth=1, relief=SOLID)
        fr2.place(x=10, y=70, height=420, width=480)

        # Widgets do Frame fr1
        self.lbl_msg = Label(fr1, textvariable=self.var_msg, font=('Tahoma 22 bold'), relief=RAISED)
        self.lbl_msg.pack(expand=True, fill=X)

        self.var_msg.set('Preferências')

        # Widgets do Frame fr2
        self.btn_add_ficha = Button(fr2, font=fonte_padrao, text='Adicionar caminho das fichas técnicas',command=self.abrir_caminho_ficha)
        self.btn_add_ficha.place(x=5, y=5)
        Label(fr2, font=fonte_padrao, textvariable=self.var_caminho_fichas, relief=SOLID, borderwidth=1).place(x=5, y=35)

        self.btn_add_banco = Button(fr2, font=fonte_padrao, text='Adicionar caminho do banco de dados',command=self.abrir_caminho_banco)
        self.btn_add_banco.place(x=5, y=60)
        Label(fr2, font=fonte_padrao, textvariable=self.var_caminho_banco, relief=SOLID, borderwidth=1).place(x=5, y=90)

        tup_icones = ('Clássico', 'Alegre', 'Moderno')
        Label(fr2, font=fonte_padrao, text='Escolha de Ícone: ').place(x=5, y=120)
        self.cb_icones = ttk.Combobox(fr2, font=fonte_padrao, values=tup_icones, state='readonly', textvariable=self.var_icone)
        self.cb_icones.place(x=150, y=120)

        tup_temas = ('Padrão', 'Visual', 'Azul', 'Escuro')
        Label(fr2, font=fonte_padrao, text='Escolha de Tema: ').place(x=5, y=150)
        self.cb_temas = ttk.Combobox(fr2, font=fonte_padrao, state='readonly', values=tup_temas, textvariable=self.var_tema)
        self.cb_temas.place(x=150, y=150)

        self.btn_gravar = Button(fr2, font=fonte_padrao, text='Gravar', command=self.gravar)
        self.btn_gravar.place(x=395, y=385, width=80)

        funcoes.carregar_cores(self, self.lbl_msg)
    
    def bloquear(self, permissao):
        if variaveis_globais.usu_acesso < 3 and permissao == False:
            self.btn_add_banco['state'] = 'disabled'
            self.btn_add_ficha['state'] = 'disabled'

    def carregar_preferencias(self):
        caminho = variaveis_globais.CAMINHO_FERRAMENTA
        try:
            if not os.path.exists(caminho):
                messagebox.showerror('Erro', 'Erro ao tentar gravar as preferências.\nContate o suporte', parent=self)
                return

            arquivo = open(caminho +  'preferências.txt', 'r')
            preferencias = arquivo.readlines()
            arquivo.close()

            self.var_caminho_fichas.set(preferencias[0][:-1])
            self.var_caminho_banco.set(preferencias[1][:-1])
            for k, v in self.dic.items():
                if v == preferencias[2][:-1]:
                    self.var_icone.set(k)

            self.cb_temas.current(int(preferencias[3][:-1]))

        except Exception as ex:
            messagebox.showwarning('Aviso', 'Sistema não conseguiu carreagar as preferências.\n'+str(ex), parent=self)
            return

    def abrir_caminho_ficha(self):
        caminho = filedialog.askdirectory(title = "Selecionar caminho")

        self.var_caminho_fichas.set(caminho+'/')

    def abrir_caminho_banco(self):
        caminho = filedialog.askdirectory(title = "Selecionar caminho")

        self.var_caminho_banco.set(caminho+'/')

    def gravar(self):

        tema = self.cb_temas.current()

        caminho = variaveis_globais.CAMINHO_FERRAMENTA

        p = messagebox.askquestion('Confirmar', 'Deseja relamente gravar as configurações?', parent=self)
        if p == 'yes':
            try:
                if not os.path.exists(caminho):
                    messagebox.showerror('Erro', 'Erro, caminho não encontrado.\nContate o suporte', parent=self)
                    return
                
                arquivo = open(caminho + 'preferências.txt', 'w')

                arquivo.write(self.var_caminho_fichas.get()+'\n')
                arquivo.write(self.var_caminho_banco.get()+'\n')
                arquivo.write(self.dic[self.var_icone.get()]+'\n')
                arquivo.write(str(tema) +'\n')

                arquivo.close()
            except Exception as ex:
                messagebox.showerror('Erro', 'Erro ao tentar gravar as configurações.\nERRO: '+str(ex), parent=self)
                return
            variaveis_globais.mudou_preferencia = True
            messagebox.showinfo('Gravado', 'Configurações gravada com sucesso!\nFavor reiniciar o sistema para validar todas as alterações.', parent=self)
            funcoes.carregar_preferencias()
            self.destroy()
            