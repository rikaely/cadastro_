from main import app
from flask import request, render_template, redirect, url_for
from models.cadastro_model import *
from datetime import datetime  # Para converter a data corretamente
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Rota para exibir o formulário
@app.route("/cadastro/inserir")
def inserir():
    return render_template("cadastro/create.html")

# Rota para processar o formulário
@app.route("/cadastro/create", methods=['POST'])
def create():
    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        data_str = request.form['data_nascimento']  # Data como string
        login = request.form['login']
        senha = request.form['senha']
        tipo = request.form['tipo']

        # Convertendo a data do formato string para o tipo Date
        data_nascimento = datetime.strptime(data_str, '%Y-%m-%d').date()

        # Cria um novo cadastro
        new_cadastro = Cadastro(
            nome=nome,
            email=email,
            telefone=telefone,
            login=login,
            senha=senha,
            tipo=tipo,
            data_nascimento=data_nascimento,
            ativo=request.form['ativo'] if request.form['ativo'] else "Inativo"  # Se não marcado, é "Inativo"
            )

        # Cria uma nova sessão para o banco de dados
        db = SessionLocal()

        # Adiciona o novo cadastro ao banco de dados
        db.add(new_cadastro)
        db.commit()

        # Redireciona para a página de lista de cadastros
        return redirect(url_for('lista'))

# Rota para exibir a lista de cadastros
@app.route("/list")
def lista():
    # Cria uma nova sessão para o banco de dados
    db = SessionLocal()
    
    # Consulta todos os cadastros no banco de dados
    cadastros = db.query(Cadastro).all()
    
    # Renderiza o template com a lista de cadastros
    return render_template("cadastro/list.html", cadastros=cadastros)

# Rota para exibir o formulário de edição
@app.route("/cadastro/editar/<int:id>", methods=["GET"])
def editar(id):
    db = SessionLocal()
    cadastro = db.query(Cadastro).filter(Cadastro.id == id).first()
    db.close()
    return render_template("cadastro/edit.html", cadastro=cadastro)

# Rota para processar a atualização
@app.route("/cadastro/update/<int:id>", methods=["POST"])
def update(id):
    db = SessionLocal()
    cadastro = db.query(Cadastro).filter(Cadastro.id == id).first()

    if cadastro:
        cadastro.nome = request.form['nome']
        cadastro.email = request.form['email']
        cadastro.telefone = request.form['telefone']
        cadastro.data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date()
        cadastro.login = request.form['login']
        cadastro.senha = request.form['senha']
        cadastro.tipo = request.form['tipo']
        cadastro.ativo = request.form['ativo']  # Atualizando o status de Ativo/Inativo

        db.commit()
    db.close()

    return redirect(url_for('lista'))










