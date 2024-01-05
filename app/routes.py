from flask import jsonify, request
from loja import app, db
from .models import Produtos, products_schema, product_schema


@app.route('/produtos', methods=['GET'])
def listaProduto():
    all_product = Produtos.query.all()
    return jsonify(products_schema.dump(all_product))

@app.route('/produtos/<int:id>', methods=['GET'])
def pegarProduto(id):
    produto = Produtos.query.get(id)
    return jsonify(product_schema.dump(produto))

@app.route('/produtos', methods=['POST'])
def incluirProduto():
    produto = request.get_json()
    
    existing_product = Produtos.query.filter_by(name=produto["name"]).first()

    if produto["name"] == "" or produto["value"] == "" or produto["quantity"] == "":
        return jsonify(errors="Os campos não podem estar vazios!")
    
    if type(produto["name"]) != str or type(produto["value"]) == str or type(produto["quantity"]) != int:
        return jsonify(errors="Os campos devem ser do tipo: name(str), price(float/int) e quantity(int)!")
    
    if produto["value"] < 0 or produto["quantity"] < 0:
        return jsonify(errors="O value e a quantidade não podem ser negativos!")
    
    if existing_product is not None:
        return jsonify(errors="Um produto com o mesmo nome já existe!")
        
    produto_add = Produtos(name=produto["name"], value=produto["value"], quantity=produto["quantity"])
    db.session.add(produto_add)
    db.session.commit()

    produto["id"] = produto_add.id

    return jsonify(produto), 201

@app.route('/produtos/<int:id>', methods=['DELETE'])
def excluirProduto(id):
    produto = Produtos.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify(mensagem="DELETED PRODUCT!"), 200

@app.route('/produtos/<int:id>', methods=['PUT'])
def editarProduto(id):

    produto = request.get_json()
    
    if produto["name"] == "" or produto["value"] == "" or produto["quantity"] == "":
        return jsonify(errors="Os campos não podem estar vazios!")
    
    if type(produto["name"]) != str or type(produto["value"]) == str or type(produto["quantity"]) != int:
        return jsonify(errors="Os campos devem ser do tipo: name(str), price(float/int) e quantity(int)!")
    
    if produto["value"] < 0 or produto["quantity"] < 0:
        return jsonify(errors="O value e a quantidade não podem ser negativos!")
    
    
    produto_editado = Produtos.query.get(id)
    produto_editado.id = id
    produto_editado.name = produto["name"]
    produto_editado.value = produto["value"]
    produto_editado.quantity = produto["quantity"]

    produto["id"] = produto_editado.id


    db.session.commit()
    return jsonify(produto), 201