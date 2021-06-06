from app import db
from app.database import Product

def create_product(name, price, quantity, category, active, reviews):
    db.session.add(
        Product(
            name=name,
            price=price,
            quantity=quantity,
            category=category,
            active=active,
            reviews=reviews
        )
    )
    db.session.commit()

if __name__ == "__main__":
    create_product("Cantalope", 10.00, 10, "danger", True, "worst product ever")
    create_product("Tangerine", 12.00, 510, "success", True, "its ok")
    create_product("Broccoli", 3.00, 250, "warning", True, "amazing product and fast shipping")
    products = Product.query.all()
    print(products)