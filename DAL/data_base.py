import sqlite3

class DataBase:
    def executar(self, sql, prms, commit=False):
        try:
            conn = sqlite3.connect('C:\\Dados\\SILKSCREEN.db')
            cursor = conn.cursor()
            print('Conectado')
            if prms == None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, prms)
            
            if commit:
                conn.commit()
                print('Gravado com sucesso!')
                r = cursor.rowcount
            else:
                r = cursor.fetchall()
            return r
        except sqlite3.Error as ex:
            return Exception('Erro referente ao banco de dados: %s'%ex)
        finally:
            cursor.close()
            conn.close()
            print('Desconectado')
