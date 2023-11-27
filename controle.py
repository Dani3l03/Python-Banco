from PyQt5 import  uic,QtWidgets
import mysql.connector

conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="bancodedados"
    )
#criando a tabela produtos se o banco não tiver ela:
cursor = conexao.cursor()
cursor.execute("SHOW TABLES LIKE 'produtos'")
resultado = cursor.fetchone()

if resultado: 
  print("A tabela já existe.")
else:
  print("A tabela não existe.")
  cursor.execute("CREATE TABLE produtos(id INT AUTO_INCREMENT PRIMARY KEY ,produto VARCHAR(255), fornecedor VARCHAR(255), preco INT)")
  print('Tabela criada!')

#função principal que preenche os dados que são colocados pelo usuário nos respectivos espaços e guarda no banco de dados
def funcao_principal():
    produto = interface.lineEdit.text()
    fornecedor = interface.lineEdit_2.text()
    preco = interface.lineEdit_3.text()

    cursor = conexao.cursor()

        # criar dados na tabela
    sql = "INSERT INTO produtos (produto, fornecedor, preco) VALUES (%s ,%s, %s)"
    dados =(produto, fornecedor, preco)
    cursor.execute(sql, dados)
    conexao.commit()

      # mostrando o que o usuário colocou   

    print("Produto:",produto)
    print("Fornecedor", fornecedor)
    print("Preço",preco)


def editar():    
    global numero_id

    linha = estoque.tableWidget.currentRow()
    
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id="+ str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_3.setText(str(produto[0][1]))
    tela_editar.lineEdit_5.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    
    numero_id = valor_id
    conexao.commit()


def salvar():
      global numero_id
      produto = tela_editar.lineEdit_3.text()
      fornecedor = tela_editar.lineEdit_5.text()
      preco = tela_editar.lineEdit_4.text()
      numero_id = tela_editar.lineEdit.text()
      
      # atualizar os dados no banco
      cursor = conexao.cursor()
      cursor.execute("UPDATE produtos SET produto = '{}', fornecedor = '{}', preco ='{}' WHERE id = {}".format(produto,fornecedor,preco,numero_id))
      conexao.commit()
      #atualizar as janelas
      tela_editar.close()
      estoque.close()

def deletar():
    linha = estoque.tableWidget.currentRow()
    estoque.tableWidget.removeRow(linha)

    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id="+ str(valor_id))
    

#declarando as tels=as do Qtdesigner como variáveis para chamar mais tarde
app=QtWidgets.QApplication([])
interface=uic.loadUi("interface.ui")
estoque=uic.loadUi("estoque.ui")
tela_editar=uic.loadUi("editar.ui")
tela_editar.pushButton.clicked.connect(salvar)

# função para chamar a tela de estoque(tabela de produtos)
def consultar_estoque():
    estoque.show()
cursor = conexao.cursor()
comando = "SELECT * FROM produtos"
cursor.execute(comando)
resultado = cursor.fetchall()

# colocando o número de linhas e Colunas da tabela do Qtdesigner (define o tamanho da tabela)
estoque.tableWidget.setRowCount(len(resultado))
estoque.tableWidget.setColumnCount(4)

# dois for para posicionar os items de maneira certa e criar uma tabela organzada na aba do Qtdesigner
for i in range(0, len(resultado)):
               for j in range(0, 4):
                  estoque.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(resultado[i][j])))

# chama as telas do Qt designer
interface.pushButton.clicked.connect(funcao_principal)
interface.pushButton_2.clicked.connect(consultar_estoque)
estoque.pushButton_3.clicked.connect(deletar)
estoque.pushButton_2.clicked.connect(editar)

interface.show()
app.exec()