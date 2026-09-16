import os
import time
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt
import bcrypt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db, engine, Base
from models import ProductDB, CategoryDB

# Ensure tables are created
Base.metadata.create_all(bind=engine)

# Configuration
SECRET_KEY = "mia_secret_key_change_me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8
UPLOAD_DIR = "../frontend/images"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Admin credentials
ADMIN_USERNAME = "dafiashalom@gmail.com"
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
app.mount("/images", StaticFiles(directory="../frontend/images"), name="images")

# Pydantic Models
class ProductBase(BaseModel):
    name: str
    price: int
    cat: str
    img: str
    description: Optional[str] = None
    badge: Optional[str] = None
    active: bool = True

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

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
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductDB).all()

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    prod = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod

@app.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    cats = db.query(CategoryDB).all()
    return [c.name for c in cats]

# Auth Routes
@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
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
def create_product(product: ProductCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_product = ProductDB(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/admin/products/{product_id}", response_model=Product)
def update_product(product_id: int, updated_product: ProductCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in updated_product.dict().items():
        setattr(db_product, key, value)
        
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/admin/products/{product_id}")
def delete_product(product_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted"}

@app.post("/admin/categories")
def add_category(cat: str = Form(...), current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(CategoryDB).filter(CategoryDB.name == cat).first()
    if not existing:
        new_cat = CategoryDB(name=cat)
        db.add(new_cat)
        db.commit()
    cats = db.query(CategoryDB).all()
    return [c.name for c in cats]

@app.delete("/admin/categories/{cat_name}")
def delete_category(cat_name: str, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_cat = db.query(CategoryDB).filter(CategoryDB.name == cat_name).first()
    if db_cat:
        db.delete(db_cat)
        db.commit()
    cats = db.query(CategoryDB).all()
    return [c.name for c in cats]

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
        "url": f"http://127.0.0.1:8000/images/{new_filename}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
