# Importa as classes necessárias do Flask para criar a aplicação web
from flask import Flask, render_template, request, redirect, url_for, flash
# Importa o conector do MySQL para comunicação com o banco de dados
import mysql.connector

# Cria uma instância da aplicação Flask
app = Flask(__name__)
# Define uma chave secreta básica para a aplicação (não recomendada para produção)
app.secret_key = 'BAD_SECRET_KEY'
# Cria e empurra um contexto de aplicação (necessário para algumas operações do Flask)
app.app_context().push()

'''def get_db():
    return mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='',
        database='banco_n1'
    )'''

# Estabelece conexão com o banco de dados MySQL
db = mysql.connector.connect(
    host='localhost',  # Endereço do servidor MySQL
    port='3306',  # Porta do MySQL
    user='root',  # Usuário do banco de dados
    password='',  # Senha do banco de dados (vazia neste caso)
    database='banco_n1'  # Nome do banco de dados a ser utilizado
)
# Cria um cursor para executar comandos SQL (buffered=True para evitar problemas com resultados não lidos)
cursor = db.cursor(buffered=True)


# Define a rota principal da aplicação
@app.route('/')
def index():
    # Executa uma consulta SQL para selecionar todos os médicos ordenados por nome
    cursor.execute('SELECT * FROM medico ORDER BY nome')
    # Recupera todos os resultados da consulta
    medicos = cursor.fetchall()
    # Renderiza o template index.html passando os dados dos médicos
    return render_template('index.html', medicos=medicos)


# Define a rota para adicionar um novo médico, aceitando métodos GET e POST
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    # Verifica se a requisição é do tipo POST (envio de formulário)
    if request.method == 'POST':
        # Obtém os dados do formulário
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        sexo = request.form['sexo']
        especialidade = request.form['especialidade']

        # Executa o comando SQL para inserir um novo médico na tabela
        cursor.execute('''
            INSERT INTO medico (nome, cpf, telefone, endereco, sexo, especialidade)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (nome, cpf, telefone, endereco, sexo, especialidade))
        # Confirma a transação no banco de dados
        db.commit()
        # Exibe uma mensagem flash de sucesso
        flash('Médico cadastrado com sucesso!', 'success')
        # Redireciona para a página principal
        return redirect(url_for('index'))

    # Se a requisição for GET, renderiza o template de adicionar médico
    return render_template('adicionar.html')


# Define a rota para editar um médico existente, aceitando métodos GET e POST
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    # Verifica se a requisição é do tipo POST (envio de formulário de edição)
    if request.method == 'POST':
        # Obtém os dados do formulário
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        sexo = request.form['sexo']
        especialidade = request.form['especialidade']

        # Executa o comando SQL para atualizar os dados do médico
        cursor.execute('''
            UPDATE medico 
            SET nome = %s, cpf = %s, telefone = %s, endereco = %s, sexo = %s, especialidade = %s
            WHERE id = %s
        ''', (nome, cpf, telefone, endereco, sexo, especialidade, id))
        # Confirma a transação no banco de dados
        db.commit()
        # Exibe uma mensagem flash de sucesso
        flash('Dados do médico atualizados com sucesso!', 'success')
        # Redireciona para a página principal
        return redirect(url_for('index'))

    # Se a requisição for GET, busca os dados do médico para edição
    cursor.execute('SELECT * FROM medico WHERE id = %s', (id,))
    # Recupera o primeiro resultado da consulta
    medico = cursor.fetchone()

    # Verifica se o médico foi encontrado
    if medico:
        # Renderiza o template de edição com os dados do médico
        return render_template('editar.html', medico=medico)
    else:
        # Se o médico não for encontrado, exibe mensagem de erro e redireciona
        flash('Médico não encontrado!', 'danger')
        return redirect(url_for('index'))


# Define a rota para excluir um médico
@app.route('/excluir/<int:id>')
def excluir(id):
    # Executa o comando SQL para deletar o médico com o ID especificado
    cursor.execute('DELETE FROM medico WHERE id = %s', (id,))
    # Confirma a transação no banco de dados
    db.commit()
    # Exibe uma mensagem flash de sucesso
    flash('Médico removido com sucesso!', 'success')
    # Redireciona para a página principal
    return redirect(url_for('index'))


# Verifica se o script está sendo executado diretamente (não importado como módulo)
if __name__ == '__main__':
    # Inicia a aplicação Flask em modo de depuração
    app.run(debug=True)