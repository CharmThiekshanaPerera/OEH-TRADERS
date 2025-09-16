from fastapi import FastAPI, APIRouter, HTTPException, Query, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict
import uuid
from datetime import datetime, timezone, timedelta
import jwt
import hashlib
import secrets

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# JWT Configuration
JWT_SECRET = "your-secret-key-here"  # In production, use environment variable
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

security = HTTPBearer()

# Enhanced Models
class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    original_price: Optional[float] = None
    category: str
    subcategory: str
    brand: str
    image_url: str
    gallery_images: List[str] = []
    rating: float
    review_count: int
    in_stock: bool
    stock_quantity: int
    specifications: dict
    features: List[str]
    tags: List[str]
    is_restricted: bool = False
    weight: Optional[str] = None
    dimensions: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    original_price: Optional[float] = None
    category: str
    subcategory: str
    brand: str
    image_url: str
    gallery_images: List[str] = []
    rating: float = 4.5
    review_count: int = 0
    in_stock: bool = True
    stock_quantity: int = 100
    specifications: dict = {}
    features: List[str] = []
    tags: List[str] = []
    is_restricted: bool = False
    weight: Optional[str] = None
    dimensions: Optional[str] = None

class Category(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    slug: str
    description: str
    image_url: str
    product_count: int = 0

class CategoryWithCount(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    image_url: str
    product_count: int

class Brand(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    logo_url: str
    description: str
    website: Optional[str] = None

class BrandWithCount(BaseModel):
    id: str
    name: str
    logo_url: str
    description: str
    website: Optional[str] = None
    product_count: int

# User Authentication Models (separate from dealers)
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    first_name: str
    last_name: str
    company_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = "United States"
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = "United States"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    company_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None

# Dealer Authentication Models (existing)
class Dealer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    company_name: str
    contact_name: str
    phone: str
    address: str
    license_number: str
    is_approved: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DealerCreate(BaseModel):
    email: EmailStr
    password: str
    company_name: str
    contact_name: str
    phone: str
    address: str
    license_number: str

class DealerLogin(BaseModel):
    email: EmailStr
    password: str

class DealerResponse(BaseModel):
    id: str
    email: EmailStr
    company_name: str
    contact_name: str
    phone: str
    address: str
    license_number: str
    is_approved: bool
    is_active: bool

# Quote System Models
class QuoteItem(BaseModel):
    product_id: str
    quantity: int
    price: float
    notes: Optional[str] = None

class Quote(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    items: List[QuoteItem]
    total_amount: float
    
    # Additional quote information
    project_name: str
    intended_use: str
    delivery_date: Optional[datetime] = None
    delivery_address: str
    billing_address: str
    company_size: Optional[str] = None
    budget_range: Optional[str] = None
    additional_requirements: Optional[str] = None
    
    status: str = "pending"  # pending, reviewed, approved, declined
    admin_notes: Optional[str] = None
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QuoteCreate(BaseModel):
    user_id: str
    items: List[QuoteItem]
    project_name: str
    intended_use: str
    delivery_date: Optional[datetime] = None
    delivery_address: str
    billing_address: str
    company_size: Optional[str] = None
    budget_range: Optional[str] = None
    additional_requirements: Optional[str] = None

class QuoteResponse(BaseModel):
    id: str
    user_name: str
    user_email: str
    company_name: Optional[str]
    items: List[QuoteItem]
    total_amount: float
    project_name: str
    intended_use: str
    delivery_date: Optional[datetime]
    delivery_address: str
    billing_address: str
    company_size: Optional[str]
    budget_range: Optional[str]
    additional_requirements: Optional[str]
    status: str
    admin_notes: Optional[str]
    created_at: datetime
    updated_at: datetime

# Chat System Models
class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    sender_type: str  # "user" or "admin"
    sender_name: str
    message: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatMessageCreate(BaseModel):
    user_id: str
    sender_type: str
    sender_name: str
    message: str

# Shopping Cart Models (enhanced for users)
class CartItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class Cart(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    items: List[CartItem] = []
    total: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AddToCartRequest(BaseModel):
    product_id: str
    quantity: int = 1

# Utility functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_jwt_token(user_id: str, user_type: str = "user") -> str:
    payload = {
        "user_id": user_id,
        "user_type": user_type,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str) -> Optional[Dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {
            "user_id": payload.get("user_id"),
            "user_type": payload.get("user_type", "user")
        }
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token_data = verify_jwt_token(credentials.credentials)
    if not token_data or token_data["user_type"] != "user":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user = await db.users.find_one({"id": token_data["user_id"], "is_active": True})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    return User(**user)

async def get_current_dealer(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dealer:
    token_data = verify_jwt_token(credentials.credentials)
    if not token_data or token_data["user_type"] != "dealer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    dealer = await db.dealers.find_one({"id": token_data["user_id"], "is_active": True})
    if not dealer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Dealer not found or inactive"
        )
    
    return Dealer(**dealer)

# Initialize sample data
@api_router.post("/initialize-data")
async def initialize_sample_data():
    # Clear existing data
    await db.products.delete_many({})
    await db.categories.delete_many({})
    await db.brands.delete_many({})
    
    # Sample categories
    categories = [
        {
            "name": "Body Armor & Protection",
            "slug": "body-armor",
            "description": "Professional body armor, plates, and protective gear",
            "image_url": "https://images.unsplash.com/photo-1704278483976-9cca15325bc0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwzfHx0YWN0aWNhbCUyMGdlYXJ8ZW58MHx8fHwxNzU3Mzc1OTk5fDA&ixlib=rb-4.1.0&q=85"
        },
        {
            "name": "Tactical Apparel",
            "slug": "tactical-apparel", 
            "description": "Uniforms, boots, gloves, and tactical clothing",
            "image_url": "https://images.unsplash.com/photo-1705564667318-923901fb916a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwyfHx0YWN0aWNhbCUyMGdlYXJ8ZW58MHx8fHwxNzU3Mzc1OTk5fDA&ixlib=rb-4.1.0&q=85"
        },
        {
            "name": "Tactical Gear & Equipment",
            "slug": "tactical-gear",
            "description": "Backpacks, pouches, holsters, and tactical accessories",
            "image_url": "https://images.unsplash.com/photo-1714384716870-6d6322bf5a7f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwxfHx0YWN0aWNhbCUyMGdlYXJ8ZW58MHx8fHwxNzU3Mzc1OTk5fDA&ixlib=rb-4.1.0&q=85"
        },
        {
            "name": "Optics & Scopes",
            "slug": "optics",
            "description": "Red dots, scopes, night vision, and optical equipment",
            "image_url": "https://images.unsplash.com/photo-1704278483831-c3939b1b041b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHw0fHx0YWN0aWNhbCUyMGdlYXJ8ZW58MHx8fHwxNzU3Mzc1OTk5fDA&ixlib=rb-4.1.0&q=85"
        },
        {
            "name": "Weapons & Accessories",
            "slug": "weapons",
            "description": "Firearms, magazines, and weapon accessories",
            "image_url": "https://images.pexels.com/photos/78783/submachine-gun-rifle-automatic-weapon-weapon-78783.jpeg"
        },
        {
            "name": "Training & Simulation",
            "slug": "training",
            "description": "Training equipment and simulation gear",
            "image_url": "https://images.unsplash.com/photo-1637252166739-b47f8875f304?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxtaWxpdGFyeSUyMGVxdWlwbWVudHxlbnwwfHx8fDE3NTczNzYwMDd8MA&ixlib=rb-4.1.0&q=85"
        }
    ]
    
    for cat in categories:
        category = Category(**cat)
        await db.categories.insert_one(category.dict())
    
    # Sample brands with tactical logo placeholders
    brands = [
        {"name": "5.11 Tactical", "logo_url": "https://images.unsplash.com/photo-1753723883109-a575c639c0a3?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODB8MHwxfHNlYXJjaHwyfHx0YWN0aWNhbCUyMGdlYXIlMjBsb2dvc3xlbnwwfHx8fDE3NTgwMDMyNTF8MA&ixlib=rb-4.1.0&q=85", "description": "Professional tactical gear and apparel"},
        {"name": "Blackhawk", "logo_url": "https://images.unsplash.com/photo-1636136370671-7ec07f284a2f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzR8MHwxfHNlYXJjaHwxfHx0YWN0aWNhbHxlbnwwfHx8fDE3NTgwMDMyNzR8MA&ixlib=rb-4.1.0&q=85", "description": "Military and law enforcement equipment"},
        {"name": "Crye Precision", "logo_url": "https://images.unsplash.com/photo-1655706443789-7682c46bcb8b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwzfHxtaWxpdGFyeSUyMGxvZ29zfGVufDB8fHx8MTc1ODAwMzI3MHww&ixlib=rb-4.1.0&q=85", "description": "Advanced combat systems and gear"},
        {"name": "Oakley SI", "logo_url": "https://images.unsplash.com/photo-1711097658585-73d97ef42bf6?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwxfHxtaWxpdGFyeSUyMGxvZ29zfGVufDB8fHx8MTc1ODAwMzI3MHww&ixlib=rb-4.1.0&q=85", "description": "Standard Issue tactical eyewear and gear"},
        {"name": "Condor Outdoor", "logo_url": "https://via.placeholder.com/200x80/2d2d2d/ffffff?text=CONDOR+TACTICAL", "description": "Tactical gear and outdoor equipment"},
        {"name": "Ops-Core", "logo_url": "https://via.placeholder.com/200x80/1a1a1a/ffffff?text=OPS-CORE", "description": "Advanced helmet and protection systems"},
        {"name": "Safariland", "logo_url": "https://via.placeholder.com/200x80/333333/ffffff?text=SAFARILAND", "description": "Law enforcement holsters and duty gear"},
        {"name": "Mechanix Wear", "logo_url": "https://via.placeholder.com/200x80/dc2626/ffffff?text=MECHANIX", "description": "Professional work and tactical gloves"}
    ]
    
    for brand in brands:
        brand_obj = Brand(**brand)
        await db.brands.insert_one(brand_obj.dict())
    
    # Sample products with varied stock status
    products = [
        {
            "name": "Tactical Plate Carrier Vest",
            "description": "Professional-grade plate carrier with MOLLE webbing system. Designed for military and law enforcement use.",
            "price": 299.99,
            "original_price": 399.99,
            "category": "Body Armor & Protection",
            "subcategory": "Plate Carriers",
            "brand": "5.11 Tactical",
            "image_url": "https://images.unsplash.com/photo-1704278483976-9cca15325bc0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwzfHx0YWN0aWNhbCUyMGdlYXJ8ZW58MHx8fHwxNzU3Mzc1OTk5fDA&ixlib=rb-4.1.0&q=85",
            "rating": 4.8,
            "review_count": 156,
            "in_stock": True,
            "stock_quantity": 25,
            "features": ["MOLLE Compatible", "Adjustable Shoulder Straps", "Quick Release System", "Drag Handle"],
            "tags": ["tactical", "military", "law-enforcement", "protection"],
            "specifications": {"Material": "1000D Cordura", "Weight": "2.1 lbs", "Size": "One Size Fits Most"},
            "weight": "2.1 lbs"
        },
        {
            "name": "Combat Tactical Boots",
            "description": "Durable tactical boots designed for extreme conditions. Waterproof and slip-resistant.",
            "price": 189.99,
            "category": "Tactical Apparel",
            "subcategory": "Boots",
            "brand": "5.11 Tactical",
            "image_url": "https://images.unsplash.com/photo-1705564667318-923901fb916a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwyfHx0YWN0aWNhbCUyMGdlYXJ8ZW58MHx8fHwxNzU3Mzc1OTk5fDA&ixlib=rb-4.1.0&q=85",
            "rating": 4.6,
            "review_count": 89,
            "in_stock": True,
            "stock_quantity": 50,
            "features": ["Waterproof", "Slip-Resistant Sole", "Breathable Lining", "Reinforced Toe"],
            "tags": ["boots", "tactical", "waterproof", "military"],
            "specifications": {"Material": "Full-grain leather", "Height": "8 inches", "Weight": "2.5 lbs per pair"}
        },
        {
            "name": "Tactical Assault Backpack",
            "description": "3-day assault pack with multiple compartments and MOLLE attachment points.",
            "price": 129.99,
            "original_price": 169.99,
            "category": "Tactical Gear & Equipment",
            "subcategory": "Backpacks",
            "brand": "Blackhawk",
            "image_url": "https://images.unsplash.com/photo-1714384716870-6d6322bf5a7f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwxfHx0YWN0aWNhbCUyMGdlYXJ8ZW58MHx8fHwxNzU3Mzc1OTk5fDA&ixlib=rb-4.1.0&q=85",
            "rating": 4.7,
            "review_count": 234,
            "in_stock": True,
            "stock_quantity": 15,
            "features": ["40L Capacity", "MOLLE Compatible", "Hydration Ready", "Reinforced Bottom"],
            "tags": ["backpack", "tactical", "molle", "assault-pack"],
            "specifications": {"Capacity": "40L", "Material": "600D Polyester", "Dimensions": "19x13x8 inches"}
        },
        {
            "name": "Red Dot Sight Optic",
            "description": "Professional red dot sight with unlimited eye relief and parallax-free performance.",
            "price": 449.99,
            "category": "Optics & Scopes",
            "subcategory": "Red Dot Sights",
            "brand": "Ops-Core",
            "image_url": "https://images.unsplash.com/photo-1704278483831-c3939b1b041b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHw0fHx0YWN0aWNhbCUyMGdlYXJ8ZW58MHx8fHwxNzU3Mzc1OTk5fDA&ixlib=rb-4.1.0&q=85",
            "rating": 4.9,
            "review_count": 67,
            "in_stock": True,
            "stock_quantity": 8,
            "features": ["Parallax Free", "Unlimited Eye Relief", "Shockproof", "Waterproof"],
            "tags": ["optics", "red-dot", "tactical", "precision"],
            "is_restricted": True,
            "specifications": {"Battery Life": "50,000 hours", "Weight": "0.8 lbs", "Mount": "Picatinny Rail"}
        },
        {
            "name": "Tactical Combat Uniform Set",
            "description": "Complete ACU uniform set with reinforced knees and elbows. Flame resistant fabric.",
            "price": 89.99,
            "category": "Tactical Apparel",
            "subcategory": "Uniforms",
            "brand": "Crye Precision",
            "image_url": "https://images.pexels.com/photos/33812346/pexels-photo-33812346.jpeg",
            "rating": 4.5,
            "review_count": 178,
            "in_stock": True,
            "stock_quantity": 35,
            "features": ["Flame Resistant", "Reinforced Knees", "Multiple Pockets", "Adjustable Cuffs"],
            "tags": ["uniform", "tactical", "flame-resistant", "combat"],
            "specifications": {"Material": "50/50 NYCO", "Colors": "Multicam, OCP", "Sizes": "XS-3XL"}
        },
        {
            "name": "Ballistic Helmet System",
            "description": "Advanced combat helmet with NVG mount and accessory rails. NIJ Level IIIA protection.",
            "price": 899.99,
            "category": "Body Armor & Protection",
            "subcategory": "Helmets",
            "brand": "Ops-Core",
            "image_url": "https://images.pexels.com/photos/33819675/pexels-photo-33819675.jpeg",
            "rating": 4.9,
            "review_count": 45,
            "in_stock": False,  # Out of stock
            "stock_quantity": 0,
            "features": ["NIJ Level IIIA", "NVG Mount", "Accessory Rails", "Comfort Padding"],
            "tags": ["helmet", "ballistic", "protection", "tactical"],
            "is_restricted": True,
            "specifications": {"Protection Level": "NIJ Level IIIA", "Weight": "3.2 lbs", "Shell": "Carbon Fiber"}
        },
        {
            "name": "Tactical Knee Pads",
            "description": "Professional knee protection for tactical operations. Comfortable and durable.",
            "price": 39.99,
            "category": "Body Armor & Protection",
            "subcategory": "Protective Gear",
            "brand": "Blackhawk",
            "image_url": "https://images.pexels.com/photos/33759979/pexels-photo-33759979.jpeg",
            "rating": 4.4,
            "review_count": 312,
            "in_stock": True,
            "stock_quantity": 100,
            "features": ["Adjustable Straps", "Non-slip Design", "Durable Padding", "Lightweight"],
            "tags": ["knee-pads", "protection", "tactical", "gear"],
            "specifications": {"Material": "Neoprene & Nylon", "Weight": "0.8 lbs", "Size": "Adjustable"}
        },
        {
            "name": "Night Vision Monocular",
            "description": "Gen 3 night vision monocular for tactical operations. High-resolution imaging.",
            "price": 2499.99,
            "category": "Optics & Scopes",
            "subcategory": "Night Vision",
            "brand": "Ops-Core",
            "image_url": "https://images.unsplash.com/photo-1549563793-ae7c90155169?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHw0fHxtaWxpdGFyeSUyMGVxdWlwbWVudHxlbnwwfHx8fDE3NTczNjAwMDd8MA&ixlib=rb-4.1.0&q=85",
            "rating": 4.8,
            "review_count": 23,
            "in_stock": False,  # Out of stock
            "stock_quantity": 0,
            "features": ["Gen 3 Tube", "Auto-Gated", "High Resolution", "Durable Housing"],
            "tags": ["night-vision", "optics", "tactical", "surveillance"],
            "is_restricted": True,
            "specifications": {"Generation": "Gen 3", "Resolution": "64 lp/mm", "Weight": "1.2 lbs"}
        },
        # Additional products for better filtering testing
        {
            "name": "Tactical Gloves Pro",
            "description": "Professional tactical gloves with reinforced palm and fingertips.",
            "price": 45.99,
            "category": "Tactical Apparel",
            "subcategory": "Gloves",
            "brand": "Condor Outdoor",
            "image_url": "https://images.unsplash.com/photo-1705564667318-923901fb916a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwyfHx0YWN0aWNhbCUyMGdlYXJ8ZW58MHx8fHwxNzU3Mzc1OTk5fDA&ixlib=rb-4.1.0&q=85",
            "rating": 4.3,
            "review_count": 156,
            "in_stock": True,
            "stock_quantity": 75,
            "features": ["Reinforced Palm", "Touchscreen Compatible", "Breathable", "Durable"],
            "tags": ["gloves", "tactical", "protection"],
            "specifications": {"Material": "Synthetic Leather", "Sizes": "S-XL"}
        },
        {
            "name": "Weapon Cleaning Kit",
            "description": "Comprehensive cleaning kit for tactical weapons maintenance.",
            "price": 59.99,
            "category": "Weapons & Accessories",
            "subcategory": "Maintenance",
            "brand": "Oakley SI",
            "image_url": "https://images.pexels.com/photos/78783/submachine-gun-rifle-automatic-weapon-weapon-78783.jpeg",
            "rating": 4.6,
            "review_count": 89,
            "in_stock": True,
            "stock_quantity": 30,
            "features": ["Multi-Caliber", "Portable Case", "Quality Tools", "Instructions"],
            "tags": ["cleaning", "maintenance", "weapons"],
            "specifications": {"Compatible": "Multiple Calibers", "Weight": "1.5 lbs"}
        }
    ]
    
    for product in products:
        product_obj = Product(**product)
        await db.products.insert_one(product_obj.dict())
    
    return {"message": "Sample data initialized successfully"}

# User Authentication Endpoints
@api_router.post("/users/register")
async def register_user(user_data: UserCreate):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create new user
    user_dict = user_data.dict()
    hashed_password = hash_password(user_data.password)
    user = User(**{k: v for k, v in user_dict.items() if k != "password"})
    
    # Store with password
    user_with_password = user.dict()
    user_with_password["password"] = hashed_password
    
    await db.users.insert_one(user_with_password)
    
    return {"message": "User registration successful"}

@api_router.post("/users/login")
async def login_user(login_data: UserLogin):
    user = await db.users.find_one({"email": login_data.email})
    if not user or not verify_password(login_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    token = create_jwt_token(user["id"], "user")
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse(**user)
    }

@api_router.get("/users/profile", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return UserResponse(**current_user.dict())

# Dealer Authentication Endpoints (existing)
@api_router.post("/dealers/register")
async def register_dealer(dealer_data: DealerCreate):
    # Check if dealer already exists
    existing_dealer = await db.dealers.find_one({"email": dealer_data.email})
    if existing_dealer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dealer with this email already exists"
        )
    
    # Create new dealer
    dealer_dict = dealer_data.dict()
    hashed_password = hash_password(dealer_data.password)
    dealer = Dealer(**{k: v for k, v in dealer_dict.items() if k != "password"})
    
    # Store with password
    dealer_with_password = dealer.dict()
    dealer_with_password["password"] = hashed_password
    
    await db.dealers.insert_one(dealer_with_password)
    
    return {"message": "Dealer registration successful. Awaiting approval."}

@api_router.post("/dealers/login")
async def login_dealer(login_data: DealerLogin):
    dealer = await db.dealers.find_one({"email": login_data.email})
    if not dealer or not verify_password(login_data.password, dealer["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not dealer["is_approved"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dealer account pending approval"
        )
    
    if not dealer["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dealer account is inactive"
        )
    
    token = create_jwt_token(dealer["id"], "dealer")
    return {
        "access_token": token,
        "token_type": "bearer",
        "dealer": DealerResponse(**dealer)
    }

@api_router.get("/dealers/profile", response_model=DealerResponse)
async def get_dealer_profile(current_dealer: Dealer = Depends(get_current_dealer)):
    return DealerResponse(**current_dealer.dict())

# Enhanced Shopping Cart Endpoints (User-based)
@api_router.post("/cart/add")
async def add_to_cart(request: AddToCartRequest, current_user: User = Depends(get_current_user)):
    # Check if product exists and is in stock
    product = await db.products.find_one({"id": request.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if not product["in_stock"] or product["stock_quantity"] < request.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # Find or create cart for user
    cart = await db.carts.find_one({"user_id": current_user.id})
    
    if not cart:
        cart = Cart(user_id=current_user.id, items=[])
        cart_dict = cart.dict()
    else:
        # Remove MongoDB _id field
        cart_dict = {k: v for k, v in cart.items() if k != "_id"}
    
    # Check if item already in cart
    item_found = False
    for item in cart_dict["items"]:
        if item["product_id"] == request.product_id:
            item["quantity"] += request.quantity
            item_found = True
            break
    
    if not item_found:
        cart_dict["items"].append({
            "product_id": request.product_id,
            "quantity": request.quantity,
            "price": product["price"]
        })
    
    # Calculate total
    cart_dict["total"] = sum(item["quantity"] * item["price"] for item in cart_dict["items"])
    cart_dict["updated_at"] = datetime.now(timezone.utc)
    
    # Save cart
    await db.carts.replace_one(
        {"user_id": current_user.id},
        cart_dict,
        upsert=True
    )
    
    return {"message": "Item added to cart", "cart": cart_dict}

@api_router.get("/cart")
async def get_cart(current_user: User = Depends(get_current_user)):
    cart = await db.carts.find_one({"user_id": current_user.id})
    if not cart:
        return {"items": [], "total": 0.0}
    
    # Get product details for each item
    enriched_items = []
    for item in cart["items"]:
        product = await db.products.find_one({"id": item["product_id"]})
        if product:
            # Remove MongoDB _id field to avoid serialization issues
            product_dict = {k: v for k, v in product.items() if k != "_id"}
            enriched_items.append({
                **item,
                "product": Product(**product_dict)
            })
    
    # Remove MongoDB _id field from cart
    cart_dict = {k: v for k, v in cart.items() if k != "_id"}
    cart_dict["items"] = enriched_items
    return cart_dict

@api_router.delete("/cart/item/{product_id}")
async def remove_from_cart(product_id: str, current_user: User = Depends(get_current_user)):
    cart = await db.carts.find_one({"user_id": current_user.id})
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Remove MongoDB _id field
    cart_dict = {k: v for k, v in cart.items() if k != "_id"}
    cart_dict["items"] = [item for item in cart_dict["items"] if item["product_id"] != product_id]
    cart_dict["total"] = sum(item["quantity"] * item["price"] for item in cart_dict["items"])
    cart_dict["updated_at"] = datetime.now(timezone.utc)
    
    await db.carts.replace_one({"user_id": current_user.id}, cart_dict)
    return {"message": "Item removed from cart"}

# Quote System Endpoints
@api_router.post("/quotes")
async def create_quote(quote_data: QuoteCreate, current_user: User = Depends(get_current_user)):
    # Calculate total amount
    total_amount = sum(item.quantity * item.price for item in quote_data.items)
    
    # Create quote
    quote = Quote(
        user_id=current_user.id,
        items=quote_data.items,
        total_amount=total_amount,
        project_name=quote_data.project_name,
        intended_use=quote_data.intended_use,
        delivery_date=quote_data.delivery_date,
        delivery_address=quote_data.delivery_address,
        billing_address=quote_data.billing_address,
        company_size=quote_data.company_size,
        budget_range=quote_data.budget_range,
        additional_requirements=quote_data.additional_requirements
    )
    
    await db.quotes.insert_one(quote.dict())
    
    # Clear user's cart after quote submission
    await db.carts.delete_one({"user_id": current_user.id})
    
    return {"message": "Quote submitted successfully", "quote_id": quote.id}

@api_router.get("/quotes", response_model=List[QuoteResponse])
async def get_user_quotes(current_user: User = Depends(get_current_user)):
    quotes = await db.quotes.find({"user_id": current_user.id}).sort("created_at", -1).to_list(length=None)
    
    quote_responses = []
    for quote in quotes:
        quote_dict = {k: v for k, v in quote.items() if k != "_id"}
        quote_responses.append(QuoteResponse(
            **quote_dict,
            user_name=f"{current_user.first_name} {current_user.last_name}",
            user_email=current_user.email,
            company_name=current_user.company_name
        ))
    
    return quote_responses

# Admin Endpoints for Quote Management
@api_router.get("/admin/quotes", response_model=List[QuoteResponse])
async def get_all_quotes():
    # In a real application, you'd add admin authentication here
    quotes = await db.quotes.find().sort("created_at", -1).to_list(length=None)
    
    quote_responses = []
    for quote in quotes:
        # Get user details
        user = await db.users.find_one({"id": quote["user_id"]})
        quote_dict = {k: v for k, v in quote.items() if k != "_id"}
        
        if user:
            quote_responses.append(QuoteResponse(
                **quote_dict,
                user_name=f"{user['first_name']} {user['last_name']}",
                user_email=user["email"],
                company_name=user.get("company_name")
            ))
    
    return quote_responses

@api_router.put("/admin/quotes/{quote_id}/status")
async def update_quote_status(quote_id: str, status: str, admin_notes: Optional[str] = None):
    # In a real application, you'd add admin authentication here
    update_data = {"status": status, "updated_at": datetime.now(timezone.utc)}
    if admin_notes:
        update_data["admin_notes"] = admin_notes
    
    result = await db.quotes.update_one(
        {"id": quote_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    return {"message": "Quote status updated successfully"}

# Chat System Endpoints
@api_router.post("/chat/send")
async def send_message(message_data: ChatMessageCreate, current_user: User = Depends(get_current_user)):
    # For user messages, override sender info
    message = ChatMessage(
        user_id=current_user.id,
        sender_type="user",
        sender_name=f"{current_user.first_name} {current_user.last_name}",
        message=message_data.message
    )
    
    await db.chat_messages.insert_one(message.dict())
    return {"message": "Message sent successfully"}

@api_router.get("/chat/{user_id}")
async def get_chat_messages(user_id: str, current_user: User = Depends(get_current_user)):
    # Users can only access their own chat
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    messages = await db.chat_messages.find({"user_id": user_id}).sort("created_at", 1).to_list(length=None)
    return [ChatMessage(**{k: v for k, v in msg.items() if k != "_id"}) for msg in messages]

@api_router.post("/admin/chat/send")
async def admin_send_message(message_data: ChatMessageCreate):
    # In a real application, you'd add admin authentication here
    message = ChatMessage(**message_data.dict())
    await db.chat_messages.insert_one(message.dict())
    return {"message": "Admin message sent successfully"}

# Enhanced Product endpoints with stock filtering (existing)
@api_router.get("/products", response_model=List[Product])
async def get_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    in_stock: Optional[bool] = None,
    limit: int = Query(default=20, le=100),
    skip: int = Query(default=0, ge=0)
):
    filter_query = {}
    
    if category:
        filter_query["category"] = category
    if brand:
        filter_query["brand"] = brand
    if min_price is not None:
        filter_query["price"] = {"$gte": min_price}
    if max_price is not None:
        if "price" in filter_query:
            filter_query["price"]["$lte"] = max_price
        else:
            filter_query["price"] = {"$lte": max_price}
    if search:
        filter_query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"tags": {"$in": [search.lower()]}}
        ]
    if in_stock is not None:
        filter_query["in_stock"] = in_stock
    
    products = await db.products.find(filter_query).skip(skip).limit(limit).to_list(length=None)
    return [Product(**product) for product in products]

@api_router.get("/categories/with-counts", response_model=List[CategoryWithCount])
async def get_categories_with_counts():
    # Get all categories
    categories = await db.categories.find().to_list(length=None)
    
    # Count products for each category
    categories_with_counts = []
    for category in categories:
        count = await db.products.count_documents({"category": category["name"]})
        category_dict = {k: v for k, v in category.items() if k != "_id"}
        category_dict["product_count"] = count
        categories_with_counts.append(CategoryWithCount(**category_dict))
    
    return categories_with_counts

@api_router.get("/brands/with-counts", response_model=List[BrandWithCount])
async def get_brands_with_counts():
    # Get all brands
    brands = await db.brands.find().to_list(length=None)
    
    # Count products for each brand
    brands_with_counts = []
    for brand in brands:
        count = await db.products.count_documents({"brand": brand["name"]})
        brand_dict = {k: v for k, v in brand.items() if k != "_id"}
        brand_dict["product_count"] = count
        brands_with_counts.append(BrandWithCount(**brand_dict))
    
    return brands_with_counts

@api_router.get("/products/price-range")
async def get_price_range():
    pipeline = [
        {
            "$group": {
                "_id": None,
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"}
            }
        }
    ]
    
    result = await db.products.aggregate(pipeline).to_list(1)
    if result:
        return {"min_price": result[0]["min_price"], "max_price": result[0]["max_price"]}
    else:
        return {"min_price": 0, "max_price": 1000}

@api_router.get("/products/featured", response_model=List[Product])
async def get_featured_products():
    products = await db.products.find({"rating": {"$gte": 4.7}}).limit(8).to_list(length=None)
    return [Product(**product) for product in products]

@api_router.get("/products/trending", response_model=List[Product])
async def get_trending_products():
    products = await db.products.find({"review_count": {"$gte": 100}}).limit(6).to_list(length=None)
    return [Product(**product) for product in products]

@api_router.get("/products/deals", response_model=List[Product])
async def get_deals():
    products = await db.products.find({"original_price": {"$exists": True, "$ne": None}}).limit(6).to_list(length=None)
    return [Product(**product) for product in products]

@api_router.get("/products/new-arrivals", response_model=List[Product])
async def get_new_arrivals():
    # Get products sorted by creation date (newest first)
    products = await db.products.find({}).sort("created_at", -1).limit(8).to_list(length=None)
    return [Product(**product) for product in products]

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)

@api_router.get("/categories", response_model=List[Category])
async def get_categories():
    categories = await db.categories.find().to_list(length=None)
    return [Category(**category) for category in categories]

@api_router.get("/brands", response_model=List[Brand])
async def get_brands():
    brands = await db.brands.find().to_list(length=None)
    return [Brand(**brand) for brand in brands]

# Original status endpoints
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

@api_router.get("/")
async def root():
    return {"message": "TacticalGear API v2.0 - B2B Platform with User Auth & Quote System"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()