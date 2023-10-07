from Ferramentas import variaveis_globais
import os, time


def menu(titulo, L1='',L2='',L3='',L4='',L5='',L6='',L7='',L8='',L9='',L10='',L11='',L12='',L13='',L14='',L15='',L16='',L17='',L18='',L19='',L20=''):
        os.system('cls')
        print('+{:^75}+'.format('-'*75))
        print('|{:^75}|'.format(titulo))
        print('|{:<75}|'.format(L1))
        print('|{:<75}|'.format(L2))
        print('|{:<75}|'.format(L3))
        print('|{:<75}|'.format(L4))
        print('|{:<75}|'.format(L5))
        print('|{:<75}|'.format(L6))
        print('|{:<75}|'.format(L7))
        print('|{:<75}|'.format(L8))
        print('|{:<75}|'.format(L9))
        print('|{:<75}|'.format(L10))
        print('|{:<75}|'.format(L11))
        print('|{:<75}|'.format(L12))
        print('|{:<75}|'.format(L13))
        print('|{:<75}|'.format(L14))
        print('|{:<75}|'.format(L15))
        print('|{:<75}|'.format(L16))
        print('|{:<75}|'.format(L17))
        print('|{:<75}|'.format(L18))
        print('|{:<75}|'.format(L19))
        print('|{:<75}|'.format(L20))
        print('|{:<75}|'.format('Usuário: '+variaveis_globais.usu_usuario+' | Nível de Acesso: '+str(variaveis_globais.usu_acesso)))
        print('+{:^75}+'.format('-'*75))

def menu_consulta(titulo, lista, L1='',L2='',L3='',L4='',L5='',L6=''):
        os.system('cls')
        print('+{:^75}+'.format('-'*75))
        print('|{:^75}|'.format(titulo))
        print('|{:<75}|'.format(L1))
        print('|{:<75}|'.format(L2))
        print('|{:<75}|'.format(L3))
        print('|{:<75}|'.format(L4))
        print('|{:<75}|'.format(L5))
        print('|{:<75}|'.format(L6))

        for i in lista:
            print(i)
        print('|{:<75}|'.format(''))
        print('|{:<75}|'.format('Usuário: '+variaveis_globais.usu_usuario+' | Nível de Acesso: '+str(variaveis_globais.usu_acesso)))
        print('+{:^75}+'.format('-'*75))

def menu_busca(titulo, lista, L1='',L2='',L3='',L4='',L5='',L6=''):
        os.system('cls')
        print('+{:^175}+'.format('-'*175))
        print('|{:^175}|'.format(titulo))
        print('|{:<175}|'.format(L1))
        print('|{:<175}|'.format(L2))
        print('|{:<175}|'.format(L3))
        print('|{:<175}|'.format(L4))
        print('|{:<175}|'.format(L5))
        print('|{:<175}|'.format(L6))

        for i in lista:
            print(i)
        print('|{:<175}|'.format(''))
        print('|{:<175}|'.format(''))
        print('|{:<175}|'.format('Usuário: '+variaveis_globais.usu_usuario+' | Nível de Acesso: '+str(variaveis_globais.usu_acesso)))
        print('+{:^175}+'.format('-'*175))

def menu_splash_screen(L1='',L2='',L3='',L4='',L5='',L6='',L7='',L8='',L9='',L10=''):
    os.system('cls')
    print('+{:^75}+'.format('-'*75))
    print('|{:^75}|'.format(L1))
    print('|{:^75}|'.format(L2))
    print('|{:^75}|'.format(L3))
    print('|{:^75}|'.format(L4))
    print('|{:^75}|'.format(L5))
    print('|{:^75}|'.format(L6))
    print('|{:^75}|'.format(L7))
    print('|{:^75}|'.format(L8))
    print('|{:^75}|'.format(L9))
    print('|{:^75}|'.format(L10))
    print('+{:^75}+'.format('-'*75))

def digitar_operacao():
    while True:
        try:
            x = int(input('Dígite a operação: '))
        except:
            mensagem_erro()
            continue
        break
    return x

def mensagem_erro():
    print('\n{:<50}\n'.format('Erro!\nDígite somente as opções válidas!'))
    time.sleep(2)