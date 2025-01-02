import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTabWidget, QTableWidget, QTableWidgetItem, QComboBox, QDateEdit,
                             QHBoxLayout, QListWidget, QStackedWidget, QMessageBox, QSizePolicy)
from PyQt5.QtCore import Qt

class DashboardEmpresarial(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.clientes = []
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        self.produtos = []
        self.vendas = []

    def create_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    cpf TEXT,
                    rg TEXT,
                    data_nascimento TEXT,
                    sexo TEXT,
                    telefone TEXT,
                    endereco TEXT
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao criar a tabela: {e}")

    def initUI(self):
        self.setWindowTitle("ERP Empresarial")
        self.resize(1000, 700)
        self.apply_styles("styles.qss")

        # Layout principal com barra lateral
        main_layout = QHBoxLayout()

        # Barra lateral
        self.sidebar = QListWidget()
        self.sidebar.addItem("HOME")
        self.sidebar.addItem("Clientes")
        self.sidebar.addItem("Produtos")
        self.sidebar.addItem("Vendas")
        self.sidebar.addItem("Relatórios")
        self.sidebar.currentRowChanged.connect(self.display_page)

        # Layout para conteúdo principal
        content_layout = QVBoxLayout()
        self.stackedWidget = QStackedWidget()
        self.initHomeTab()
        self.initClientesTab()
        self.initProdutosTab()  # Adicionado
        self.initVendasTab()  # Adicionado
        self.initRelatoriosTab()  # Adicionado
        content_layout.addWidget(self.stackedWidget)

        # Adicionar barra lateral e conteúdo principal ao layout
        main_layout.addWidget(self.sidebar, 1)  # Barra lateral fixa
        main_layout.addLayout(content_layout, 4)  # Conteúdo (com pesquisa na HOME)

        self.setLayout(main_layout)

    def apply_styles(self, file_path):
        try:
            with open(file_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Arquivo de estilo '{file_path}' não encontrado.")

    def initHomeTab(self):
        page = QWidget()
        layout = QVBoxLayout()

        # Layout para campo de pesquisa no topo
        search_layout = QHBoxLayout()

        # Campo de pesquisa maior e responsivo
        self.pesquisaInput = QLineEdit()
        self.pesquisaInput.setPlaceholderText("Digite o nome do cliente...")
        self.pesquisaInput.setMinimumWidth(200)  # Largura mínima
        self.pesquisaInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Responsivo

        # Botão de pesquisa ao lado do campo
        pesquisaButton = QPushButton("Pesquisar")
        pesquisaButton.clicked.connect(self.pesquisar_cliente)
        pesquisaButton.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 16px; border-radius: 5px;")

        # Alinhamento para garantir que os elementos fiquem alinhados horizontalmente e no topo
        search_layout.addWidget(self.pesquisaInput)
        search_layout.addWidget(pesquisaButton)

        # Ajuste para garantir que ambos os elementos fiquem no topo
        search_layout.setAlignment(Qt.AlignTop)  # Alinhamento do topo
        search_layout.setContentsMargins(0, 10, 0, 0)  # Ajustar margens para melhorar o layout

        # Adicionar layout de pesquisa no topo
        layout.addLayout(search_layout)

        # Exibição de ficha de cliente abaixo do campo de pesquisa
        self.clienteInfo = QLabel("<p>Detalhes do cliente aparecerão aqui...</p>")
        layout.addWidget(self.clienteInfo)

        # Adicionar margem para o conteúdo da ficha de cliente
        layout.setContentsMargins(10, 20, 10, 10)  # Ajustar as margens de layout para não ficar muito distante

        # Adicionando o layout ao widget da página
        page.setLayout(layout)
        self.stackedWidget.addWidget(page)

    def pesquisar_cliente(self):
        pesquisa = self.pesquisaInput.text()
        if pesquisa:
            self.cursor.execute("SELECT * FROM clientes WHERE nome LIKE ?", ('%' + pesquisa + '%',))
            cliente = self.cursor.fetchone()

            if cliente:
                cliente_info = f"""
                <p><strong>Nome:</strong> {cliente[1]}</p>
                <p><strong>CPF:</strong> {cliente[2]}</p>
                <p><strong>RG:</strong> {cliente[3]}</p>
                <p><strong>Data de Nascimento:</strong> {cliente[4]}</p>
                <p><strong>Sexo:</strong> {cliente[5]}</p>
                <p><strong>Telefone:</strong> {cliente[6]}</p>
                <p><strong>Endereço:</strong> {cliente[7]}</p>
                """
                self.clienteInfo.setText(cliente_info)
            else:
                QMessageBox.warning(self, "Resultado da Pesquisa", "Nenhum cliente encontrado!")
        else:
            QMessageBox.warning(self, "Erro", "Digite um nome para pesquisar!")

    def initClientesTab(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<h2>Cadastro de Clientes</h2>"))

        # Campos para cadastro de cliente
        layout.addWidget(QLabel("Nome"))
        self.nomeInput = QLineEdit()
        layout.addWidget(self.nomeInput)

        layout.addWidget(QLabel("CPF"))
        self.cpfInput = QLineEdit()
        layout.addWidget(self.cpfInput)

        layout.addWidget(QLabel("RG"))
        self.rgInput = QLineEdit()
        layout.addWidget(self.rgInput)

        layout.addWidget(QLabel("Data de Nascimento"))
        self.dataNascimentoInput = QDateEdit()
        self.dataNascimentoInput.setCalendarPopup(True)  # Ativa o calendário
        layout.addWidget(self.dataNascimentoInput)

        layout.addWidget(QLabel("Sexo"))
        self.sexoInput = QComboBox()
        self.sexoInput.addItems(["Masculino", "Feminino"])
        layout.addWidget(self.sexoInput)

        layout.addWidget(QLabel("Telefone"))
        self.telefoneInput = QLineEdit()
        layout.addWidget(self.telefoneInput)

        layout.addWidget(QLabel("Endereço"))
        self.enderecoInput = QLineEdit()
        layout.addWidget(self.enderecoInput)

        addButton = QPushButton("Adicionar Cliente")
        addButton.clicked.connect(self.add_cliente)
        layout.addWidget(addButton)

        page.setLayout(layout)
        self.stackedWidget.addWidget(page)

    def add_cliente(self):
        nome = self.nomeInput.text()
        cpf = self.cpfInput.text()
        rg = self.rgInput.text()
        data_nascimento = self.dataNascimentoInput.text()
        sexo = self.sexoInput.currentText()
        telefone = self.telefoneInput.text()
        endereco = self.enderecoInput.text()

        if nome and cpf and rg and data_nascimento and sexo and telefone and endereco:
            self.cursor.execute("""
                INSERT INTO clientes (nome, cpf, rg, data_nascimento, sexo, telefone, endereco)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nome, cpf, rg, data_nascimento, sexo, telefone, endereco))
            self.conn.commit()
            QMessageBox.information(self, "Sucesso", "Cliente adicionado com sucesso!")
            self.nomeInput.clear()
            self.cpfInput.clear()
            self.rgInput.clear()
            self.dataNascimentoInput.clear()
            self.sexoInput.setCurrentIndex(0)
            self.telefoneInput.clear()
            self.enderecoInput.clear()
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")

    def initProdutosTab(self):  # Implementação da aba Produtos
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<h2>Cadastro de Produtos</h2>"))

        # Campos para cadastro de produto
        layout.addWidget(QLabel("Nome do Produto"))
        self.produtoNomeInput = QLineEdit()
        layout.addWidget(self.produtoNomeInput)

        layout.addWidget(QLabel("Preço"))
        self.produtoPrecoInput = QLineEdit()
        layout.addWidget(self.produtoPrecoInput)

        layout.addWidget(QLabel("Quantidade em Estoque"))
        self.produtoQuantidadeInput = QLineEdit()
        layout.addWidget(self.produtoQuantidadeInput)

        addButton = QPushButton("Adicionar Produto")
        addButton.clicked.connect(self.add_produto)
        layout.addWidget(addButton)

        page.setLayout(layout)
        self.stackedWidget.addWidget(page)

    def add_produto(self):
        nome = self.produtoNomeInput.text()
        preco = self.produtoPrecoInput.text()
        quantidade = self.produtoQuantidadeInput.text()

        if nome and preco and quantidade:
            # Salvar produto no banco de dados (produto.db ou outra tabela)
            QMessageBox.information(self, "Sucesso", "Produto adicionado com sucesso!")
            self.produtoNomeInput.clear()
            self.produtoPrecoInput.clear()
            self.produtoQuantidadeInput.clear()
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")

    def initVendasTab(self):  # Implementação da aba Vendas
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<h2>Vendas</h2>"))
        # Adicione campos e tabelas necessários para a aba Vendas

        page.setLayout(layout)
        self.stackedWidget.addWidget(page)

    def initRelatoriosTab(self):  # Implementação da aba Relatórios
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<h2>Relatórios</h2>"))
        # Adicione campos e tabelas necessários para a aba Relatórios

        page.setLayout(layout)
        self.stackedWidget.addWidget(page)

    def display_page(self, index):
        self.stackedWidget.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = DashboardEmpresarial()
    dashboard.show()
    sys.exit(app.exec_())
