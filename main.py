import os
import json
import time
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt
from passlib.context import CryptContext
import bcrypt
from pydantic import BaseModel

# Configuration
SECRET_KEY = "mia_secret_key_change_me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8
DATA_FILE = "data/products.json"
CAT_FILE = "data/categories.json"
UPLOAD_DIR = "uploads/images"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Admin credentials
ADMIN_USERNAME = "dafiashalom@gmail.com"
# "Test@2026" hashed with bcrypt
ADMIN_PASSWORD_HASH = "$2b$12$WEppdN1cGHqnkInZ4RUCKOrLq613Tyl2c1Czw.mcxHa4RShNKCFhq"

app = FastAPI(title="Mia's Crochet API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploads
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Models
class Product(BaseModel):
    id: int
    name: str
    price: int
    cat: str
    img: str
    desc: str
    badge: Optional[str] = None
    active: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Data management
def load_products():
    if not os.path.exists(DATA_FILE):
        initial_products = [
            { "id": 1, "name": "Bouquet Rose Éternelle", "price": 8500, "cat": "Fleurs", "img": "images/anya-chernykh-jq0B9v_rYtg-unsplash.jpg", "desc": "Un bouquet délicat crocheté à la main, parfait pour décorer votre intérieur durablement.", "active": True },
            { "id": 2, "name": "Top Crochet 'Solstice'", "price": 15000, "cat": "Vêtements", "img": "images/dwayne-joe-MBi1x-HBjKA-unsplash.jpg", "desc": "Top ajouré réalisé avec un fil de coton naturel, idéal pour les journées ensoleillées.", "active": True },
            { "id": 3, "name": "Box Cadeau 'Douceur'", "price": 18000, "cat": "Accessoires", "img": "images/maria-kovalets-RgEaD36YYGI-unsplash.jpg", "desc": "Une sélection de créations artisanales comprenant un chouchou, un porte-clés et une mini fleur.", "active": True },
            { "id": 4, "name": "Sac Cabas 'Mistral'", "price": 22000, "cat": "Accessoires", "img": "images/paul-hanaoka-4nabmlliGdU-unsplash.jpg", "desc": "Un sac spacieux et robuste, entièrement doublé, pour vos sorties estivales.", "active": True },
            { "id": 5, "name": "Robe de Plage 'Ondine'", "price": 35000, "cat": "Vêtements", "img": "images/dwayne-joe-MXhcH9EIEBw-unsplash.jpg", "desc": "Une robe longue et légère aux motifs complexes, une pièce d'exception.", "active": True },
            { "id": 6, "name": "Bouquet de Marguerites", "price": 7500, "cat": "Fleurs", "img": "images/dwayne-joe-f2WM_P7mQqM-unsplash.jpg", "desc": "Sept marguerites blanches au cœur jaune pour illuminer votre bureau.", "active": True },
            { "id": 7, "name": "Bustier 'Coucher de Soleil'", "price": 12500, "cat": "Vêtements", "img": "images/dwayne-joe-hF_Ygbj0HQo-unsplash.jpg", "desc": "Un bustier coloré aux nuances chaudes, ajustable pour un confort optimal.", "active": True },
            { "id": 8, "name": "Chouchou 'Pétale'", "price": 2500, "cat": "Accessoires", "img": "images/lizzi-sassman-M7ZuRWaaevw-unsplash.jpg", "desc": "Un accessoire délicat pour vos cheveux, doux et protecteur.", "active": True },
            { "id": 9, "name": "Vase de Tulipes", "price": 12000, "cat": "Fleurs", "img": "images/anya-chernykh-jq0B9v_rYtg-unsplash.jpg", "desc": "Un assortiment de tulipes aux couleurs vives.", "active": True }
        ]
        save_products(initial_products)
        return initial_products
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_products(products):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

def load_categories():
    if not os.path.exists(CAT_FILE):
        initial_cats = ["Fleurs", "Vêtements", "Accessoires", "Bonnets & Écharpes", "Cadeaux"]
        save_categories(initial_cats)
        return initial_cats
    with open(CAT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_categories(categories):
    os.makedirs(os.path.dirname(CAT_FILE), exist_ok=True)
    with open(CAT_FILE, "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=4, ensure_ascii=False)

# Auth helper
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    if username != ADMIN_USERNAME:
        raise credentials_exception
    return username

# Public Routes
@app.get("/products", response_model=List[Product])
async def get_products():
    return load_products()

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    products = load_products()
    for p in products:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/categories", response_model=List[str])
async def get_categories():
    return load_categories()

# Auth Routes
@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Direct bcrypt verification to avoid passlib/bcrypt 4.0 compatibility issues
    is_valid = False
    try:
        is_valid = bcrypt.checkpw(form_data.password.encode('utf-8'), ADMIN_PASSWORD_HASH.encode('utf-8'))
    except Exception:
        pass
        
    if form_data.username != ADMIN_USERNAME or not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Admin Routes
@app.post("/admin/products", response_model=Product)
async def create_product(product: Product, current_user: str = Depends(get_current_user)):
    products = load_products()
    # Auto-increment ID if not provided or to ensure uniqueness
    if products:
        new_id = max(p["id"] for p in products) + 1
    else:
        new_id = 1
    
    new_product = product.dict()
    new_product["id"] = new_id
    products.append(new_product)
    save_products(products)
    return new_product

@app.put("/admin/products/{product_id}", response_model=Product)
async def update_product(product_id: int, updated_product: Product, current_user: str = Depends(get_current_user)):
    products = load_products()
    for i, p in enumerate(products):
        if p["id"] == product_id:
            updated_data = updated_product.dict()
            updated_data["id"] = product_id # Keep same ID
            products[i] = updated_data
            save_products(products)
            return updated_data
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/admin/products/{product_id}")
async def delete_product(product_id: int, current_user: str = Depends(get_current_user)):
    products = load_products()
    products = [p for p in products if p["id"] != product_id]
    save_products(products)
    return {"message": "Product deleted"}

@app.post("/admin/categories")
async def add_category(cat: str = Form(...), current_user: str = Depends(get_current_user)):
    cats = load_categories()
    if cat not in cats:
        cats.append(cat)
        save_categories(cats)
    return cats

@app.delete("/admin/categories/{cat_name}")
async def delete_category(cat_name: str, current_user: str = Depends(get_current_user)):
    cats = load_categories()
    if cat_name in cats:
        cats.remove(cat_name)
        save_categories(cats)
    return cats

@app.post("/admin/upload")
async def upload_image(file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    allowed_extensions = ["jpg", "jpeg", "png", "webp"]
    extension = file.filename.split(".")[-1].lower()
    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    timestamp = int(time.time())
    new_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, new_filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    return {
        "filename": new_filename,
        "url": f"http://127.0.0.1:8000/uploads/images/{new_filename}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
