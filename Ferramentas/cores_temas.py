from Ferramentas import variaveis_globais
# Sequência de cores em hexadecimal

# 0 - Background (Label, Frame, Janela) exeto Label de título.
# 1 - Background (Button)
# 2 - Background (Label do título)
# 3 = Foregraund (Label do título)
# 4 = Foregraund (Button)
# 5 = Background (Label display)
# 6 = Foregraund (Label display)



cores_hexa = [
        ('#F8F8FF', '#C0C0C0', '#B0C4DE', '#00008B', '#000000', '#B0C4DE', '#000000'),
        ('#A9A9A9', '#D8BFD8', '#363636', '#FF1493', '#000000', '#ADD8E6', '#191970'),
        ('#E0FFFF', '#ADD8E6',  '#00BFFF', '#2F4F4F', '#0000FF', '#B0E0E6', '#000000'),
        ('#778899', '#000000',  '#696969', '#F0F8FF', '#FFFAFA', '#363636', '#FFFAFA')
]

def carregar_cores():
        return cores_hexa[variaveis_globais.preferencia_temas]
        #return cores_hexa[3]