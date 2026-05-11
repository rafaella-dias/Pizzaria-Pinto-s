from db import db
from datetime import datetime

class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    imagem = db.Column(db.String(255))
    disponivel = db.Column(db.Boolean, default=True)
    variacoes = db.relationship('ProdutoPreco', backref='produto', lazy=True, cascade="all, delete-orphan")


class ProdutoPreco(db.Model):
    __tablename__ = "produto_precos"

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    tamanho = db.Column(db.String(20), nullable=False)
    preco = db.Column(db.Float, nullable=False)


class Pedido(db.Model): 
    __tablename__ = "pedidos"
    
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="pendente")
    data = db.Column(db.DateTime, default=datetime.utcnow)


class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    tamanho = db.Column(db.String(20))