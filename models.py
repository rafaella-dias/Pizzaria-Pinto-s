from db import db
from datetime import datetime


class Produto(db.Model): #cardápio
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(255))


class Pedido(db.Model): 
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="pendente")
    data = db.Column(db.DateTime, default=datetime.utcnow)


class ItemPedido(db.Model): #itens q estao no cardapio
    __tablename__ = "itens_pedido"

    id = db.Column(db.Integer, primary_key=True)

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id"),
        nullable=False
    )
    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id"),
        nullable=False
    )

    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)