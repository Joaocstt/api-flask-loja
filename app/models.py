from loja import db, ma

class Produtos(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(90), unique=True, nullable=False)
    value = db.Column(db.Double)
    quantity = db.Column(db.Integer)

    def __init__(self, name, value, quantity):
        self.name = name
        self.value = value
        self.quantity = quantity

    def json(self):
        return {'name':self.name, 'value': self.value, 'quantity': self.quantity}

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "value", "quantity")

product_schema = UserSchema()
products_schema = UserSchema(many=True)
        