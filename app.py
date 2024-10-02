from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_marshmallow import Marshmallow
from datetime import date
from typing import List
from marshmallow import ValidationError, fields
from sqlalchemy import select, delete
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()

user = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')


app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{user}:{password}@localhost/{db_name}'

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)
ma = Marshmallow(app)

#================= Models =================#

class Customer(Base):
    __tablename__ = 'customer'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(db.String(75), nullable=False)
    email: Mapped[str] = mapped_column(db.String(150))
    phone: Mapped[str] = mapped_column(db.String(16))

    orders: Mapped[List["Orders"]] = db.relationship(back_populates='customer')


order_products = db.Table(
    "order_products",
    Base.metadata,
    db.Column('order_id', db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.ForeignKey('products.id'), primary_key=True)
)


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    delivery_date: Mapped[date] = mapped_column(db.Date)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customer.id'))

    customer: Mapped['Customer'] = db.relationship(back_populates='orders')

    products: Mapped[List['Products']] = db.relationship(secondary='order_products')


class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(db.String(225), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    availability: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    stock: Mapped[int] = mapped_column(db.Integer, nullable=False)  # Added stock column for stock management

#=============== Marshmallow Schema ==================#

class CustomerSchema(ma.Schema):
    id = fields.Integer(required=False)
    customer_name = fields.String(required=True)
    email = fields.Email()
    phone = fields.String()

    class Meta:
        fields = ('id', 'customer_name', 'email', 'phone')


class OrderSchema(ma.Schema):
    id = fields.Integer(required=False)
    order_date = fields.Date(required=True)
    delivery_date = fields.Date()
    customer_id = fields.Integer(required=True)
    items = []

    class Meta:
        fields = ('id', 'order_date', 'delivery_date', 'customer_id', 'items')


class productsSchema(ma.Schema):
    id = fields.Integer(required=False)
    product_name = fields.String(required=True)
    price = fields.Float(required=True)
    availability = fields.Boolean()
    stock = fields.Integer(required=True)  # Added stock field to schema

    class Meta:
        fields = ('id', 'product_name', 'price', 'availability', 'stock')


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

product_schema = productsSchema()
products_schema = productsSchema(many=True)

#================= API Routes ====================#

@app.route('/')
def home():
    return "Welcome to the E-commerce API!"

#=============== Customer Routes ===============#

@app.route("/customers", methods=['GET'])
def get_customers():
    query = select(Customer)
    result = db.session.execute(query).scalars()
    customers = result.all()
    return customers_schema.jsonify(customers)


@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    query = select(Customer).where(Customer.id == id)
    result = db.session.execute(query).scalars().first()
    if result is None:
        return jsonify({"message": "Customer not found"}), 404
    return customer_schema.jsonify(result)


@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_customer = Customer(customer_name=customer_data['customer_name'], email=customer_data['email'], phone=customer_data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'Message': "New customer added successfully!"}), 201


@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    query = select(Customer).where(Customer.id == id)
    result = db.session.execute(query).scalar()
    if result is None:
        return jsonify({"message": "Customer not found"}), 404

    customer = result
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in customer_data.items():
        setattr(customer, field, value)

    db.session.commit()
    return jsonify({'message': "Customer details have been updated"})


@app.route("/customers/<int:id>", methods=['DELETE'])
def delete_customer(id):
    query = delete(Customer).where(Customer.id == id)
    result = db.session.execute(query)
    if result.rowcount == 0:
        return jsonify({"Message": "Customer not found!"}), 404
    db.session.commit()
    return jsonify({"Message": "Customer successfully deleted!"}), 200

#=============== Product Routes ===============#

@app.route("/products", methods=['POST'])
def add_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_product = Products(product_name=product_data['product_name'], price=product_data['price'], availability=product_data['availability'], stock=product_data['stock'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"Message": "New product added successfully!"}), 201


@app.route("/products", methods=['GET'])
def get_products():
    query = select(Products)
    result = db.session.execute(query).scalars()
    products = result.all()
    return products_schema.jsonify(products)


@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    query = select(Products).where(Products.id == id)
    result = db.session.execute(query).scalars().first()
    if result is None:
        return jsonify({"message": "Product not found"}), 404
    return product_schema.jsonify(result)


@app.route('/products/<int:id>', methods=['PUT'])
def update_products(id):
    query = select(Products).where(Products.id == id)
    result = db.session.execute(query).scalar()
    if result is None:
        return jsonify({"message": "Product not found"}), 404

    product = result
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in product_data.items():
        setattr(product, field, value)

    db.session.commit()
    return jsonify({'message': "Product details have been updated"})


@app.route("/products/<int:id>", methods=['DELETE'])
def delete_product(id):
    query = delete(Products).where(Products.id == id)
    result = db.session.execute(query)
    if result.rowcount == 0:
        return jsonify({"Message": "Product not found!"}), 404
    db.session.commit()
    return jsonify({"Message": "Product successfully deleted!"}), 200

#=============== Stock Management Routes ===============#

@app.route("/products/<int:id>/stock", methods=['PUT'])
def update_stock(id):
    query = select(Products).where(Products.id == id)
    result = db.session.execute(query).scalar()
    if result is None:
        return jsonify({"message": "Product not found"}), 404

    product = result
    new_stock = request.json.get('stock')
    product.stock = new_stock
    db.session.commit()

    return jsonify({'message': "Product stock updated successfully"})

#=============== Order Routes ===============#

@app.route("/orders", methods=['POST'])
def add_orders():
    try:
        orders_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_orders = Orders(order_date=orders_data['order_date'], delivery_date=orders_data['delivery_date'], customer_id=orders_data['customer_id'])
    db.session.add(new_orders)
    db.session.commit()

    return jsonify({"Message": "New orders added successfully!"}), 201


@app.route("/orders", methods=['GET'])
def get_orders():
    query = select(Orders)
    result = db.session.execute(query).scalars()
    orders = result.all()
    return orders_schema.jsonify(orders)


@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    query = select(Orders).where(Orders.id == id)
    result = db.session.execute(query).scalars().first()
    if result is None:
        return jsonify({"message": "Order not found"}), 404
    return order_schema.jsonify(result)

#=============== Order Total Calculation ===============#

@app.route("/orders/<int:id>/total", methods=['GET'])
def calculate_order_total(id):
    query = select(Orders).where(Orders.id == id)
    result = db.session.execute(query).scalars().first()
    if result is None:
        return jsonify({"message": "Order not found"}), 404

    order = result
    total_price = sum([product.price for product in order.products])
    return jsonify({"Order Total": total_price})

#=============== Order Cancellation ===============#

@app.route("/orders/<int:id>/cancel", methods=['PUT'])
def cancel_order(id):
    query = select(Orders).where(Orders.id == id)
    result = db.session.execute(query).scalar()
    if result is None:
        return jsonify({"message": "Order not found"}), 404

    # Assuming "cancel" means deleting the order
    db.session.delete(result)
    db.session.commit()

    return jsonify({'message': "Order has been cancelled"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
