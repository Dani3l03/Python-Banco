import mysql.connector

conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="bancodedados"
    )

# criação de banco de dados 

cursor = conexao.cursor()
cursor.execute("SHOW TABLES LIKE 'produtos'")
resultado = cursor.fetchone()

if resultado: 
  print(" O banco de dados já existe.")
else:
  print("o banco de dados não existe.")
  cursor.execute("CREATE DATABASE produtos")

# criação da tabela

cursor.execute("CREATE TABLE produtos(id INT AUTO_INCREMENT PRIMARY KEY,produto VARCHAR(255), fornecedor VARCHAR(255), preco INT)")

# criação de dados

sql = "INSERT INTO produtos(produto, fornecedor, preco) VALUES (%s, %s, %s)"
dados = ("Notebook", "Dell", 2)

cursor.execute(sql, dados)

conexao.commit()


# lendo as informações do banco de dados

cursor.execute("SELECT * FROM produtos ")
resultado2 = cursor.fetchall()

for i in resultado2:
    print(i)

# atualizar uma informação do banco de dados

adicionar = "UPDATE produtos SET produto=%s WHERE produto = %s"
atualizado = ("Notebook", "Smartphone")

cursor.execute(adicionar, atualizado)

conexao.commit()

# deletar uma informação do banco de dados

deletar = "DELETE FROM produtos WHERE produto = %s"
deletado = ('Notebook')
cursor.execute(deletar, deletado)

conexao.commit()
 
