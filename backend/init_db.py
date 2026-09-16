import json
import os
from database import engine, SessionLocal, Base
from models import ProductDB, CategoryDB

# Create tables
Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    
    # Check if DB is already populated
    if db.query(ProductDB).count() > 0:
        print("Database already initialized.")
        db.close()
        return

    # Load categories
    if os.path.exists("data/categories.json"):
        with open("data/categories.json", "r") as f:
            categories = json.load(f)
            for c_name in categories:
                cat = CategoryDB(name=c_name)
                db.add(cat)
    
    # Load products
    if os.path.exists("data/products.json"):
        with open("data/products.json", "r") as f:
            products = json.load(f)
            for p in products:
                prod = ProductDB(
                    name=p.get("name"),
                    price=p.get("price"),
                    cat=p.get("cat"),
                    badge=p.get("badge"),
                    description=p.get("description"),
                    img=p.get("img"),
                    active=p.get("active", True)
                )
                db.add(prod)
    
    db.commit()
    db.close()
    print("Database initialized from JSON.")

if __name__ == "__main__":
    init_db()
