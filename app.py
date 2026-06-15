from flask import Flask, request
from flask_cors import CORS
from models import db, Produto
from config import *

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# HOME
@app.route("/")
def home():
    return {
        "status": "success",
        "mensagem": "StockManager API funcionando!"
    }


# CREATE (CRIAR PRODUTO)
@app.route("/produtos", methods=["POST"])
def criar_produto():

    dados = request.get_json()

    if not dados:
        return {
            "status": "error",
            "mensagem": "JSON inválido ou vazio"
        }, 400

    nome = dados.get("nome")
    categoria = dados.get("categoria")
    preco = dados.get("preco")
    quantidade = dados.get("quantidade")

    if not nome or not categoria:
        return {"status": "error", "mensagem": "Nome e categoria são obrigatórios"}, 400

    if preco is None or preco <= 0:
        return {"status": "error", "mensagem": "Preço inválido"}, 400

    if quantidade is None or quantidade < 0:
        return {"status": "error", "mensagem": "Quantidade inválida"}, 400

    produto = Produto(
        nome=nome,
        categoria=categoria,
        preco=preco,
        quantidade=quantidade
    )

    db.session.add(produto)
    db.session.commit()

    return {
        "status": "success",
        "mensagem": "Produto criado com sucesso",
        "dados": produto.to_dict()
    }, 201


# READ ALL
@app.route("/produtos", methods=["GET"])
def listar_produtos():

    produtos = Produto.query.all()

    return {
        "status": "success",
        "dados": [p.to_dict() for p in produtos]
    }, 200


# READ BY ID
@app.route("/produtos/<int:id>", methods=["GET"])
def buscar_produto(id):

    produto = Produto.query.get(id)

    if not produto:
        return {"status": "error", "mensagem": "Produto não encontrado"}, 404

    return {
        "status": "success",
        "dados": produto.to_dict()
    }, 200


# UPDATE
@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):

    produto = Produto.query.get(id)

    if not produto:
        return {"status": "error", "mensagem": "Produto não encontrado"}, 404

    dados = request.get_json()

    produto.nome = dados.get("nome", produto.nome)
    produto.categoria = dados.get("categoria", produto.categoria)
    produto.preco = dados.get("preco", produto.preco)
    produto.quantidade = dados.get("quantidade", produto.quantidade)

    db.session.commit()

    return {
        "status": "success",
        "mensagem": "Produto atualizado com sucesso",
        "dados": produto.to_dict()
    }, 200


# DELETE
@app.route("/produtos/<int:id>", methods=["DELETE"])
def deletar_produto(id):

    produto = Produto.query.get(id)

    if not produto:
        return {"status": "error", "mensagem": "Produto não encontrado"}, 404

    db.session.delete(produto)
    db.session.commit()

    return {
        "status": "success",
        "mensagem": "Produto removido com sucesso"
    }, 200


if __name__ == "__main__":
    app.run(debug=True)