from app import db
from app.database import Product

def create_product(name, price, quantity):
    db.session.add(
        Product(
            name=name,
            price=price,
            quantity=quantity
        )
    )
    db.session.commit()

if __name__ == "__main__":
    create_product("Bananas", 10.00, 10)
    create_product("Oranges", 12.00, 50)
    products = Product.query.all()
    print(products)