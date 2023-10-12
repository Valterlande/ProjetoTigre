from tkinter import *
from tkinter import messagebox, ttk
from GUI_TKINTER import frm_cad_tip_material, frm_cad_mod_produto, frm_cad_material, frm_cad_tela, frm_cad_kit, frm_ent_material, frm_sai_material, \
    frm_trans_material, frm_con_tela, frm_con_material, frm_con_kit, frm_rel_material, frm_rel_kit, frm_rel_tela, frm_rel_mov_material, \
        frm_logar, frm_cad_usuario, frm_con_ficha_tecnica, frm_ativacao, frm_sobre, frm_aut_preferencia
from Ferramentas import variaveis_globais
from datetime import datetime
import os


class FrmPrincipal(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)

        self.iconbitmap('Imagens\icone_principal.ico')
        w = 800
        h = 600
        x = (self.winfo_screenwidth() / 2) - w / 2
        y = (self.winfo_screenheight() / 2) - h / 2
        self.geometry('%dx%d+%d+%d'%(w, h , x, y))
        self.title(variaveis_globais.NOME_APP)

        self.protocol('WM_DELETE_WINDOW', self.fechar)

        self.criar_widgets()

        self.conta_tempo()

        self.logar()

        self.verivicar_ativacao()

    def criar_widgets(self):
        # Fonte padrão
        fonte_menu =  'Verdana 9 bold'

        # Imagens
        caminho = 'Imagens\\'
        self.img_log_nao = PhotoImage(file=caminho+'Logout.png')
        self.img_log_sim = PhotoImage(file=caminho+'Login.png')
        self.img_ati_nao = PhotoImage(file=caminho+'lock.png')
        self.img_ati_sim = PhotoImage(file=caminho+'unlock.png')
        img_entrada = PhotoImage(file=caminho+'inboxtray.png')
        img_saida = PhotoImage(file=caminho+'outboxtray.png')
        img_trans = PhotoImage(file=caminho+'ic_swap_vert.png')
        img_material = PhotoImage(file=caminho+'ic_layers.png')
        img_tela = PhotoImage(file=caminho+'blank-frame_icon-icons.com.png')
        img_kit = PhotoImage(file=caminho+'Business_packingboxes_negocio.png')
        img_ficha = PhotoImage(file=caminho+'ficha.png')

        # Variáveis
        self.var_status = StringVar()

        # Menus
        menu_principal = Menu(self)

        menu_acesso = Menu(menu_principal, tearoff=0, font=fonte_menu)
        menu_acesso.add_command(label='Logar', command=self.logar)
        menu_acesso.add_command(label='Deslogar', command=self.deslogando)
        menu_principal.add_cascade(label='Acesso', menu=menu_acesso)

        menu_op = Menu(menu_principal, tearoff=0, font=fonte_menu)
        menu_op.add_command(label='Entrada de Material', command=lambda : self.abrir_frms(frm_ent_material.FrmEntMaterial))
        menu_op.add_command(label='Saída de Material', command=lambda : self.abrir_frms(frm_sai_material.FrmSaiMaterial))
        menu_op.add_command(label='Transferência de Material', command=lambda : self.abrir_frms(frm_trans_material.FrmTransMaterial))
        menu_principal.add_cascade(label='Movimentações', menu=menu_op)

        menu_cad = Menu(menu_principal, tearoff=0, font=fonte_menu)
        menu_cad.add_command(label='Modelo Produto', command=lambda : self.abrir_frms(frm_cad_mod_produto.FrmCadModProduto, 2))
        menu_cad.add_separator()
        menu_cad.add_command(label='Material', command=lambda : self.abrir_frms(frm_cad_material.FrmCadMaterial, 2))
        menu_cad.add_command(label='Tipo Material', command=lambda : self.abrir_frms(frm_cad_tip_material.FrmCadTipMaterial, 2))
        menu_cad.add_separator()
        menu_cad.add_command(label='Tela', command=lambda : self.abrir_frms(frm_cad_tela.FrmCadTela, 2))
        menu_cad.add_separator()
        menu_cad.add_command(label='Kit', command=lambda : self.abrir_frms(frm_cad_kit.FrmCadKit, 2))
        menu_cad.add_separator()
        menu_cad.add_command(label='Usuário', command=lambda : self.abrir_frms(frm_cad_usuario.FrmCadUsuario, 3))
        menu_principal.add_cascade(label='Cadastros', menu=menu_cad)

        menu_con = Menu(menu_principal, tearoff=0, font=fonte_menu)
        menu_con.add_command(label='Kit', command=lambda : self.abrir_frms(frm_con_kit.FrmConKit))
        menu_con.add_command(label='Material', command=lambda : self.abrir_frms(frm_con_material.FrmConMaterial))
        menu_con.add_command(label='Tela', command=lambda : self.abrir_frms(frm_con_tela.FormConTela))
        menu_con.add_separator()
        menu_con.add_command(label='Ficha Técnica de Produto', command=lambda : self.abrir_frms(frm_con_ficha_tecnica.FrmConFichaTecnica))
        menu_principal.add_cascade(label='Consultas', menu=menu_con)

        menu_rel = Menu(menu_principal, tearoff=0, font=fonte_menu)
        menu_rel.add_command(label='Kit', command=lambda : self.abrir_frms(frm_rel_kit.FrmRelKit, 3))
        menu_rel.add_command(label='Material', command=lambda : self.abrir_frms(frm_rel_material.FrmRelMaterial, 3))
        menu_rel.add_command(label='Tela', command=lambda : self.abrir_frms(frm_rel_tela.FrmRelTela, 3))
        menu_rel.add_separator()
        menu_rel.add_command(label='Movimentação de Material', command=lambda : self.abrir_frms(frm_rel_mov_material.FrmRelMovMaterial, 3))
        menu_principal.add_cascade(label='Relatórios', menu=menu_rel)

        menu_conf = Menu(menu_principal, tearoff=0, font=fonte_menu)
        menu_conf.add_command(label='Ativação', command=self.ativar)
        menu_conf.add_command(label='Preferência', command=lambda : self.abrir_frms(frm_aut_preferencia.FrmAutPreferencia, 3))
        menu_principal.add_cascade(label='Configurações', menu=menu_conf)

        menu_aju = Menu(menu_principal, tearoff=0, font=fonte_menu)
        menu_aju.add_command(label='Sobre', command=self.sobre)
        menu_principal.add_cascade(label='Ajuda', menu=menu_aju)

        self.configure(menu=menu_principal)

        # Frames
        fr1 = Frame(self)
        fr1.pack(fill=X)

        fr2 = Frame(self, relief=GROOVE, borderwidth=1)
        fr2.pack(side=BOTTOM, fill=X)

        # Widgets do Frame fr1
        btn_entrada = Button(fr1, image=img_entrada, relief=FLAT, command=lambda : self.abrir_frms(frm_ent_material.FrmEntMaterial))
        btn_entrada.image = img_entrada
        btn_entrada.pack(side=LEFT,padx=2, pady=2)

        btn_saida = Button(fr1, image=img_saida, relief=FLAT,command=lambda : self.abrir_frms(frm_sai_material.FrmSaiMaterial))
        btn_saida.image = img_saida
        btn_saida.pack(side=LEFT,padx=2,pady=2)

        btn_trans = Button(fr1, image=img_trans, relief=FLAT, command=lambda : self.abrir_frms(frm_trans_material.FrmTransMaterial))
        btn_trans.image = img_trans
        btn_trans.pack(side=LEFT,padx=2,pady=2)

        btn_material = Button(fr1, image=img_material, relief=FLAT, command=lambda : self.abrir_frms(frm_con_material.FrmConMaterial))
        btn_material.image = img_material
        btn_material.pack(side=LEFT,padx=2,pady=2)

        btn_ficha = Button(fr1, image=img_ficha, relief=FLAT, command=lambda : self.abrir_frms(frm_con_ficha_tecnica.FrmConFichaTecnica))
        btn_ficha.image = img_ficha
        btn_ficha.pack(side=LEFT,padx=2,pady=2)

        btn_kit = Button(fr1, image=img_kit, relief=FLAT, command=lambda : self.abrir_frms(frm_con_kit.FrmConKit))
        btn_kit.image = img_kit
        btn_kit.pack(side=LEFT,padx=2,pady=2)

        btn_tela = Button(fr1, image=img_tela, relief=FLAT, command=lambda : self.abrir_frms(frm_con_tela.FormConTela))
        btn_tela.image = img_tela
        btn_tela.pack(side=LEFT,padx=2,pady=2)

        # Widgets do Frane fr2
        self.lbl_ativado = Label(fr2)
        self.lbl_ativado.pack(side=LEFT)

        self.lbl_logado = Label(fr2)
        self.lbl_logado.pack(side=LEFT)

        lbl_status = Label(fr2, font='Arial 12 bold', anchor='w', textvariable=self.var_status)
        lbl_status.pack(side=LEFT, expand=True, fill=X, padx=10)

        self.pb = ttk.Progressbar(fr2, length=150, maximum=variaveis_globais.TEMPO)
        self.pb.pack(side=RIGHT, padx=5)

    def seta_status(self):
        self.var_status.set('| Usuário: {} / Acesso: {} |'.format(variaveis_globais.usu_usuario, str(variaveis_globais.usu_acesso)))

        if variaveis_globais.ativado:
            self.lbl_ativado['image'] =self.img_ati_sim
        else:
            self.lbl_ativado['image'] =self.img_ati_nao

        if variaveis_globais.logado:
            self.lbl_logado['image'] = self.img_log_sim
        else:
            self.lbl_logado['image'] =self.img_log_nao

    def logar(self):
        if variaveis_globais.logado:
            res = messagebox.askquestion('Logar','Existe usuário logado no sistema.\nDeseja logar com um novo usuário?', parent=self)
            if res == 'yes':
                frm_logar.FrmLogar()
        else:
           frm_logar.FrmLogar() 

    def deslogando(self):
        if not variaveis_globais.logado:
            messagebox.showwarning('Aviso', 'Não há usuário logado no sistema!', parent=self)
            return

        res = messagebox.askquestion('Deslogar','Deseja realmente deslogar do sistema?', parent=self)
        if res == 'yes':
            self.deslogar()
      
    def deslogar(self):
        variaveis_globais.usu_acesso = 0
        variaveis_globais.usu_id = 0
        variaveis_globais.usu_nome = None
        variaveis_globais.usu_usuario = None
        variaveis_globais.logado = False
        self.pb.stop()

    def conta_tempo(self):
        self.seta_status()
        if variaveis_globais.logado:
            if variaveis_globais.cont == 0:
                self.pb.start(1000)
            variaveis_globais.cont += 1
            if variaveis_globais.cont >= variaveis_globais.TEMPO:
                self.deslogar()

        self.after(1000, self.conta_tempo)

    def abrir_frms(self, frm, nivel=1):
        if not variaveis_globais.ativado:
            messagebox.showwarning('Aviso', 'O sistema não está ativado!', parent=self)
            return

        if variaveis_globais.logado:
            if variaveis_globais.usu_acesso >= nivel:
                frm()
            else:
                messagebox.showwarning('Aviso', 'Área restrita para este usuário!', parent=self)
                return        
        else:
            messagebox.showwarning('Aviso', 'Não há usuário logado no sistema!', parent=self)
            return

    def ativar(self):
        if not variaveis_globais.ativado or variaveis_globais.usu_acesso >= 3:
            frm_ativacao.FrmAtivacao()
        else:
            messagebox.showinfo('Ativado', 'O sistema já está ativado!', parent=self)
            return

    def sobre(self):
        frm_sobre.FrmSobre()

    def verivicar_ativacao(self):
        caminho = 'Ferramentas\\tigre.txt'

        if not os.path.exists(caminho):
            messagebox.showerror('Erro', 'Erro ao verificar a ativação do sistema.\nContate o suporte', parent=self)
            return

        arquivo = open(caminho, 'r')
        dt_string = arquivo.read()
        arquivo.close()

        try:
            dt_hj = datetime.today()
            dt_format = '%d-%m-%Y'
            #dt_exp = datetime.strptime(dt_string, dt_format)

            dt_exp =  datetime(int(dt_string[3002:3006]), int(dt_string[2001:2003]), int(dt_string[1000:1002]))

            diferencia = (dt_exp - dt_hj).days

            if diferencia <= 0:
                variaveis_globais.ativado = False
                messagebox.showwarning('Aviso', 'O sistema não está ativado!', parent=self)
            else:
                variaveis_globais.ativado = True
                if diferencia >= 3 and diferencia <= 7:
                    messagebox.showinfo('Informação', 'Falta {} dia(s) para expirar a validação do sistema!'.format(diferencia), parent=self)
                elif diferencia <= 2:
                    messagebox.showwarning('Aviso', 'Falta {} dia(s) para expirar a validação do sistema!'.format(diferencia), parent=self)

        except Exception as ex:
            messagebox.showwarning('Aviso', 'O sistema não está ativado!', parent=self)
            return

    def fechar(self):
        res = messagebox.askquestion('Sair', 'Deseja sair do sistema?', parent=self)
        if res == 'yes':
            self.destroy()
