import sqlite3
conexao = sqlite3.connect('JournalOfc.db')
cursor = conexao.cursor()

#Criando a Tabela
cursor.execute('''
CREATE TABLE IF NOT EXISTS dadosop (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              Ativo Text,
              Data Text,
              Hora_abertura Text,
              Hora_fechamento Text,
              Tempo_op Integer,
              TET Integer,
              Qtd_compra Integer,
              Qtd_venda Integer,
              Lado Text,
              Preco_compra Real,
              Preco_venda Real,
              Resultado_pts Real,
              Resultado_cash Real
              )
              ''')
conexao.commit()
#Inserindo os dados
import pandas as pd
df=pd.read_csv('dados/Profit.dados.csv', encoding ='latin1', sep =';', skiprows = 5)
print(df.head())

#with open('dados/Profit.dados.csv', encoding ='latin1') as arquivo:
 #   for i , linha in enumerate(arquivo):
  #      print(i,repr(linha))
   #     if i> 10:
    #        break