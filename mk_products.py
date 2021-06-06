from app import db
from app.database import Product

def create_product(name, price, quantity, category, active):
    db.session.add(
        Product(
            name=name,
            price=price,
            quantity=quantity,
            category=category,
            active=active
        )
    )
    db.session.commit()

if __name__ == "__main__":
    create_product("Cantalope", 10.00, 10, "danger", True)
    create_product("Tangerine", 12.00, 510, "success", True)
    create_product("Broccoli", 3.00, 250, "warning", True)
    products = Product.query.all()
    print(products)