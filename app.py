from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)

# producto Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique= True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    unity = db.Column(db.Integer)

    def __init__(self, name, description, price, unity):
        self.name = name
        self.description = description
        self.price = price
        self.unity = unity

# product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'unity')
# init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create Product
@app.route('/product', methods=['POST'])
def addProduct():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    unity = request.json['unity']

    new_product = Product(name, description, price, unity)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# GET all Products
@app.route('/products', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)

    return jsonify(result)

# Get single Product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)

    return product_schema.jsonify(product)

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name= request.json['name']
  description= request.json['description']
  price = request.json['price']
  unity = request.json['unity']

  product.name = name
  product.description = description
  product.price = price
  product.unity = unity

  db.session.commit()

@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)

# Run server & Debug to Actualization
if __name__ == '__main__':
    app.run(port= 3000, debug= True)
