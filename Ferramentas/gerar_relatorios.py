import subprocess
from datetime import datetime
from BLL import kit_bll, material_bll, tela_bll, mov_material_bll
from Ferramentas import variaveis_globais


def gerar_relatorio_kit(prms=''):
    e = 'OK'
    bll = kit_bll.KitBll()
    r = bll.retornar_dados('material', '%'+prms+'%')

    nome_arquivo = 'Relatório de Kits'

    try:
        arquivo = open( variaveis_globais.CAMINHO_REL+nome_arquivo+'.txt', 'w')
        
        arquivo.write('{:>10} {:>70}\n\n\n'.format(datetime.today().strftime('%H:%M:%S %d/%m/%Y'), 'Resp.: '+variaveis_globais.usu_usuario))
        arquivo.write('| {:^6} | {:^8} | {:^76} |\n'.format('CÓDIGO', 'MATERIAL', 'DESCRIÇÃO'))
        arquivo.write('+'+'-'*8+'+'+'-'*10+'+'+'-'*78+'+\n')
        for i in r:
            arquivo.write('| {:^6} | {:^8} | {:^76} |\n'.format(i[1],str(i[2]), i[4]))

        arquivo.close()

        subprocess.Popen(variaveis_globais.CAMINHO_REL+nome_arquivo+'.txt', shell=True)
            
    except Exception as ex:
        e = Exception(str(ex))
    return e
    
def gerar_relatorio_material(prms=''):
    e = 'OK'
    bll = material_bll.MaterialBll()
    r = bll.retornar_dados('tipo', '%'+prms+'%')

    nome_arquivo = 'Relatório de Materiais'

    try:
        arquivo = open(variaveis_globais.CAMINHO_REL+nome_arquivo+'.txt', 'w')

        arquivo.write('{:>10} {:>70}\n\n\n'.format(datetime.today().strftime('%H:%M:%S %d/%m/%Y'), 'Resp.: '+variaveis_globais.usu_usuario))
        arquivo.write('| {:^6} | {:^8} | {:^42} | {:^5} | {:^6} | {:^5} | {:^6} |\n'.format('CÓDIGO', 'TIPO', 'DESCRIÇÃO', 'RET.', 'IMPRE.', 'IMP.', 'SALDO'))
        arquivo.write('+'+'-'*8+'+'+'-'*10+'+'+'-'*44+'+'+'-'*7+'+'+'-'*8+'+'+'-'*7+'+'+'-'*8+'+\n')

        for i in r:
            arquivo.write('| {:^6} | {:^8} | {:^42} | {:^5} | {:^6} | {:^5} | {:^6} |\n'.format(i[1], i[2], i[3][:42], i[4], i[5], i[6], i[7]))
        
        arquivo.close()

        subprocess.Popen(variaveis_globais.CAMINHO_REL+nome_arquivo+'.txt', shell=True)
        #subprocess.Popen(['notepad', caminho+nome_arquivo+'.txt'])

        # Pode abrir o bloco de nota desse jeito também
        #os.system('notepad '+caminho+'Relatório de Material.txt')
        
    except Exception as ex:
        e = Exception(str(ex))
    return e

def gerar_relatorio_tela(tipo='',modelo=''):
    e = 'OK'
    bll = tela_bll.TelaBll()
    r = bll.retornar_dados('tipo+modelo+descricao', ('%'+tipo+'%', '%'+modelo+'%', '%'+''+'%'))

    nome_arquivo = 'Relatório de Telas'

    try:
        arquivo = open(variaveis_globais.CAMINHO_REL+nome_arquivo+'.txt', 'w')

        arquivo.write('{:>10} {:>70}\n\n'.format(datetime.today().strftime('%H:%M:%S %d/%m/%Y'), 'Resp.: '+variaveis_globais.usu_usuario))
        arquivo.write('{:>20} {:>20}\n\n'.format(tipo, modelo))
        arquivo.write('+'+'-'*98+'+\n')
        cont = 0

        for i in r:
            part_a = '| ID: {:<10} Tipo: {:<10} Modelo: {:<10}'.format(i[0], i[1], i[2])
            conte_a = 99 - len(part_a)

            part_b = '| Descrição: {:<5} Prateleira(s): {:<5}'.format(i[3][:52], i[4][:15])
            b = len(part_b)
            if b >= 0:
                conte_b = 99 - b
            else:
                conte_b = 100

            arquivo.write('{} {:>{}}\n'.format(part_a, ' |', conte_a))
            arquivo.write('{} {:>{}}\n'.format(part_b, ' |', conte_b))
            arquivo.write('+'+'-'*98+'+\n')
            cont += 1
            if cont == 25:
                cont = 0
                arquivo.write('\n\n\n\n')
                arquivo.write('+'+'-'*98+'+\n')

        arquivo.close()

        subprocess.Popen(variaveis_globais.CAMINHO_REL+nome_arquivo+'.txt', shell=True)

    except Exception as ex:
        e = Exception(str(ex))
    return e

def gerar_relatorio_mov_material(dt_inicial,dt_final,tipo=''):
    e = 'OK'
    bll = mov_material_bll.MovMaterialBll()

    r = bll.retornar_dados('dat+tip', (dt_inicial, dt_final, '%'+tipo+'%'))

    nome_arquivo = 'Relatório de Mov. Materiais'

    try:
        arquivo = open(variaveis_globais.CAMINHO_REL+nome_arquivo+'.txt', 'w')

        #arquivo.write('-'*100+'\n') # Adequar em uma página
        arquivo.write('{:>10} {:>70}\n{:>50}\n\n'.format(datetime.today().strftime('%H:%M:%S %d/%m/%Y'), 'Resp.: '+variaveis_globais.usu_usuario, 'Período: '+dt_inicial.strftime('%d/%m/%Y')+' á '+dt_final.strftime('%d/%m/%Y')))
        arquivo.write('| {:^6} | {:^26} | {:^10} | {:^10} | {:^10} | {:^6} | {:^10} |\n'.format('CÓDIGO', 'DESCRIÇÃO', 'TIPO', 'ORIGEM', 'DESTINO', 'QTD', 'DATA'))
        arquivo.write('+'+'-'*8+'+'+'-'*28+'+'+'-'*12+'+'+'-'*12+'+'+'-'*12+'+'+'-'*8+'+'+'-'*12+'+\n')

        for i in r:
            arquivo.write('| {:^6} | {:^26} | {:^10} | {:^10} | {:^10} | {:^6} | {:^10} |\n'.format(i[1],i[2][:26],i[3][:10],i[4][:10],i[5][:10],str(i[6]),i[7]))

        arquivo.close()

        #subprocess.Popen(['notepad',caminho+nome_arquivo+'.txt'])
        subprocess.Popen(variaveis_globais.CAMINHO_REL+nome_arquivo+'.txt', shell=True)
    except Exception as ex:
        e = Exception(str(ex))
    return e
