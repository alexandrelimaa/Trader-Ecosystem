import sqlite3
conexao = sqlite3.connect('Journal.db')
cursor = conexao.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS my_orders (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               ativo TEXT,
               resultado REAL,
               data TEXT
    )
    ''')
conexao.commit()
cursor.execute(
'INSERT INTO my_orders (ativo, resultado, data) VALUES (?, ?, ?)',
               ('WINFUTV', 150.50, '2026-08-10')
)
conexao.commit()

print('--- Todas as operações ---')
cursor.execute('Select * from my_orders')
for linha in cursor.fetchall():
    print(linha)

print('--- Só o dia 2026-08-10---')
cursor.execute('Select * from my_orders where data = ?', ('2026-08-10',))
for linha in cursor.fetchall():
    print(linha)

print('--- Resultado do dia 2026-08-10---')
cursor.execute('Select Sum(resultado) from my_orders where data = ?', ('2026-08-10',))
total = cursor.fetchone()[0]
print('O Resultado total do dia :', total)

print('--- Deletando linha 1 ---')
cursor.execute('Delete from my_orders where id = ?', (1,))
cursor.execute('Select * from my_orders')
for linha in cursor.fetchall():
    print(linha)
conexao.commit()

cursor.execute('DROP TABLE my_orders')
conexao.commit()
print('Tabela Apagada com sucesso!')

conexao.close()