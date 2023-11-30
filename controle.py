from PyQt5 import  uic,QtWidgets
import mysql.connector

conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="bancodedados"
    )
# criando a tabela produtos se o banco não tiver ela:
cursor = conexao.cursor()
cursor.execute("SHOW TABLES LIKE 'produtos'")
resultado = cursor.fetchone()

if resultado:
  print("A tabela já existe.")
else:
  print("A tabela não existe.")
  cursor.execute("CREATE TABLE produtos(id INT AUTO_INCREMENT PRIMARY KEY ,produto VARCHAR(255), fornecedor VARCHAR(255), preco INT)")
  print('Tabela criada!')

# função principal que preenche os dados que são colocados pelo usuário nos respectivos espaços e guarda no banco de dados
def adicionar():
    produto = interface.lineEdit.text() # linha de texto da interface que adiciona o produto
    fornecedor = interface.lineEdit_2.text() # linha de texto da interface que adiciona o fornecedor
    preco = interface.lineEdit_3.text() # linha de texto da interface que adiciona o preço

    cursor = conexao.cursor()

        # criar dados na tabela
    sql = "INSERT INTO produtos (produto, fornecedor, preco) VALUES (%s ,%s, %s)"
    dados =(produto, fornecedor, preco) 
    cursor.execute(sql, dados) # insere os dados na tabela 
    conexao.commit()

      # mostrando o que o usuário colocou   

    print("Produto:",produto)
    print("Fornecedor", fornecedor)
    print("Preço",preco)


def editar():    
    global numero_id # declarando numero_id como variavel global para usar em outras funções

    linha = estoque.tableWidget.currentRow() # seleciona a linha que usuário clicou
    
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM produtos") # o ID que o usuário clicou
    dados_lidos = cursor.fetchall() 
    valor_id = dados_lidos[linha][0] # inicia a seleção na posição zero que seria o primeiro ID
    cursor.execute("SELECT * FROM produtos WHERE id="+ str(valor_id)) # seleciona a linha do toda do ID que o usuário clicou 
    produto = cursor.fetchall()  # retorna todos os valores da linha selecionada
    tela_editar.show()

# atribui cada linha de texto da interface de edição a um dos itens da linha da tabela '0' rdita o ID, '1' edita o produto e assim por diante 
    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_3.setText(str(produto[0][1]))
    tela_editar.lineEdit_5.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    
    numero_id = valor_id
    conexao.commit()


def salvar():
      produto = tela_editar.lineEdit_3.text()
      fornecedor = tela_editar.lineEdit_5.text()
      preco = tela_editar.lineEdit_4.text()
      numero_id = tela_editar.lineEdit.text()
      
      # atualiza os dados no banco enviando o conteúdo para a tabela
      cursor = conexao.cursor()
      cursor.execute("UPDATE produtos SET produto = '{}', fornecedor = '{}', preco ='{}' WHERE id = {}".format(produto,fornecedor,preco,numero_id))
      conexao.commit()
      # atualizar as janelas
      tela_editar.close()
      estoque.close()
      consultar_estoque() 

def deletar():
    linha = estoque.tableWidget.currentRow() # linha selecionada
    estoque.tableWidget.removeRow(linha) # rmover a linha selecionada

    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM produtos") 
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id="+ str(valor_id)) # remover todos os dados da linha do ID selecionado
    conexao.commit()
    

# declarando as telas do Qtdesigner como variáveis para chamar mais tarde
app=QtWidgets.QApplication([])
interface=uic.loadUi("interface.ui") # menu principal
estoque=uic.loadUi("estoque.ui") # janela de consulta
tela_editar=uic.loadUi("editar.ui") # janela de edição

# função para chamar a tela de estoque(tabela de produtos)
def consultar_estoque():
    estoque.show()
cursor = conexao.cursor()
comando = "SELECT * FROM produtos"
cursor.execute(comando)
resultado = cursor.fetchall() # retorna todos os valores da tabela do banco de dados
conexao.commit()

# colocando o número de linhas e Colunas da tabela do Qtdesigner (define o tamanho da tabela)
estoque.tableWidget.setRowCount(len(resultado))
estoque.tableWidget.setColumnCount(4)

# dois for para posicionar os items de maneira certa e criar uma tabela organizada na aba da interface 
for i in range(0, len(resultado)):
               for j in range(0, 4):
                  estoque.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(resultado[i][j])))

# chama as telas do Qt designer
interface.pushButton.clicked.connect(adicionar) # botão enviar chama função adicionar
interface.pushButton_2.clicked.connect(consultar_estoque) # botão consultar chama função consultar-estoque
estoque.pushButton_3.clicked.connect(deletar) # botão deletar dentro da aba estoque chama a função deletar
estoque.pushButton_2.clicked.connect(editar) # botão editar dentro da aba estoque chama a função editar
tela_editar.pushButton.clicked.connect(salvar) # botão salvar dentro da aba de edição chama a função salvar que ira salvar os dados digitados no banco de dados
 
interface.show() # mostra a interface principal
app.exec() # para executar a interface do QT