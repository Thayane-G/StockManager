from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Produto(db.Model):

    __tablename__ = "produtos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    categoria = db.Column(
        db.String(50),
        nullable=False
    )

    preco = db.Column(
        db.Float,
        nullable=False
    )

    quantidade = db.Column(
        db.Integer,
        nullable=False
    )

    data_criacao = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):

        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "data_criacao": self.data_criacao.strftime("%Y-%m-%d %H:%M:%S")
        }