from flask import Flask, render_template, request, redirect, url_for, session
from db import db
from models import Produto, Pedido, ItemPedido



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DataBasePizzariaPinto.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = "cloud"

db.init_app(app)



@app.route('/')
def home():
    return render_template('home.html')



@app.route('/cardapio')
def cardapio():
    produtos = Produto.query.all()
    return render_template('cardapio.html', produtos=produtos)



@app.route('/add-carrinho', methods=['POST'])
def add_carrinho():
    produto_id = int(request.form.get('produto_id'))
    produto = Produto.query.get(produto_id)

    if not produto:
        return redirect(url_for('cardapio'))
    
    if 'carrinho' not in session:
        session['carrinho'] = []

    carrinho = session['carrinho']

    produto_existe = False
    for item in carrinho:
        if item['id'] == produto.id:
            item['quantidade'] += 1
            produto_existe = True
            break

    if not produto_existe:
        carrinho.append({
            'id': produto.id,
            'nome': produto.nome,
            'preco': produto.preco,
            'quantidade': 1
        })

    session['carrinho'] = carrinho
    return redirect(url_for('carrinho'))



@app.route('/carrinho')
def carrinho():
    carrinho = session.get('carrinho', [])

    total = 0
    for item in carrinho:
        total += item['preco'] * item['quantidade']

    return render_template('carrinho.html', carrinho=carrinho, total=total)



@app.route('/finalizar', methods=['POST'])
def finalizar():
    carrinho = session.get('carrinho', [])

    if not carrinho:
        return redirect(url_for('carrinho'))

    nome_cliente = request.form.get('nome_cliente')

    total = 0
    for item in carrinho:
        total += item['preco'] * item['quantidade']

    pedido = Pedido(nome_cliente=nome_cliente, total=total)

    db.session.add(pedido)
    db.session.commit()

    for item in carrinho:
        item_pedido = ItemPedido(
            pedido_id=pedido.id,
            produto_id=item['id'],
            quantidade=item['quantidade'],
            preco_unitario=item['preco']
)
        db.session.add(item_pedido)

    db.session.commit()
    session.pop('carrinho')

    return redirect(url_for('sucesso', pedido_id=pedido.id))



@app.route('/sucesso/<int:pedido_id>')
def sucesso(pedido_id):
    pedido = Pedido.query.get(pedido_id)
    return render_template('sucesso.html', pedido=pedido)



@app.route('/admin')
def admin():
    produtos = Produto.query.all()
    pedidos = Pedido.query.filter(Pedido.status != "entregue").order_by(Pedido.data.desc()).all()
    return render_template('admin.html', produtos=produtos, pedidos=pedidos)



@app.route('/admin/pedido/<int:id>/status', methods=['POST'])
def alterar_status(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return redirect(url_for('admin'))

    novo_status = request.form.get('status')
    pedido.status = novo_status
    db.session.commit()

    return redirect(url_for('admin'))



@app.route('/admin/produto', methods=['POST'])
def cadastrar_produto():
    nome = request.form.get('nome')
    preco = float(request.form.get('preco'))
    imagem = request.form.get('imagem')

    produto = Produto(nome=nome, preco=preco, imagem=imagem)

    db.session.add(produto)
    db.session.commit()

    return redirect(url_for('admin'))
    


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)