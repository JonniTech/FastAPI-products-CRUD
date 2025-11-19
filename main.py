from fastapi import FastAPI,Depends
from model import Product
from models import table_models
from database import session,engine,get_db
from sqlalchemy.orm import Session

app = FastAPI()

table_models.Base.metadata.create_all(bind=engine)

products = [
    Product(id=1, name="Car", description="A nice red car", price=30.34, quantity=20),
    Product(id=2, name="Bike", description="A fast bike", price=15.99, quantity=50),
    Product(id=3, name="Truck", description="Heavy duty truck", price=60.50, quantity=10),
    Product(id=4, name="Scooter", description="Electric scooter", price=25.00, quantity=30),
    Product(id=5, name="Boat", description="Small boat", price=120.75, quantity=5),
    Product(id=6, name="Plane", description="Toy plane", price=45.99, quantity=12),
    Product(id=7, name="Skateboard", description="Wooden skateboard", price=20.00, quantity=25),
    Product(id=8, name="Helmet", description="Safety helmet", price=8.50, quantity=100),
    Product(id=9, name="Gloves", description="Racing gloves", price=12.00, quantity=40),
    Product(id=10, name="Watch", description="Smart watch", price=55.00, quantity=15),
]

@app.on_event("startup")
def init_db():
    db = Session(bind=engine)

    if db.query(table_models.Product).count == 0:
        for product in products:
            db.add(table_models.Product(**product.model_dump()))
    
    db.commit()

    
@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):
    list_of_products = db.query(table_models.Product).all()
    return list_of_products


@app.get("/product/{id}")
def get_single_product(id:int,db:Session = Depends(get_db)):
    single_product = db.query(table_models.Product).filter(table_models.Product.id == id).first()
    if single_product:
        return single_product
    return "product not found"
    

@app.post("/product")
def add_new_product(product:Product,db:Session = Depends(get_db)):
    new_product = db.add(table_models.Product(**product.model_dump()))
    db.commit()
    return {"success":True,"created_product":product}

@app.put("/product/{id}")
def update_product(id:int,product:Product,db:Session = Depends(get_db)):
    db_product = db.query(table_models.Product).filter(table_models.Product.id == id).first()
    
    if db_product:
        db_product.name = product.name
        db_product.description =  product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated successfully"
    else:
        return "product not exist"

@app.delete("/product/{id}")
def delete_product(id:int,db:Session =  Depends(get_db)):
    db_product = db.query(table_models.Product).filter(table_models.Product.id == id).first()

    if not db_product:
        return "product not found"
    
    db.delete(db_product)
    db.commit()
    return "Product deleted successful"