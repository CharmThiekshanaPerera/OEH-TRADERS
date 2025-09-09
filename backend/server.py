from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timezone

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

# Tactical Gear Models
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

class Brand(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    logo_url: str
    description: str
    website: Optional[str] = None

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
    
    # Sample brands
    brands = [
        {"name": "5.11 Tactical", "logo_url": "https://via.placeholder.com/150x60/1a1a1a/ffffff?text=5.11", "description": "Professional tactical gear and apparel"},
        {"name": "Blackhawk", "logo_url": "https://via.placeholder.com/150x60/000000/ffffff?text=BLACKHAWK", "description": "Military and law enforcement equipment"},
        {"name": "Crye Precision", "logo_url": "https://via.placeholder.com/150x60/2d2d2d/ffffff?text=CRYE", "description": "Advanced combat systems and gear"},
        {"name": "Oakley SI", "logo_url": "https://via.placeholder.com/150x60/1a1a1a/ffffff?text=OAKLEY", "description": "Standard Issue tactical eyewear and gear"},
        {"name": "Condor Outdoor", "logo_url": "https://via.placeholder.com/150x60/0f0f0f/ffffff?text=CONDOR", "description": "Tactical gear and outdoor equipment"},
        {"name": "Ops-Core", "logo_url": "https://via.placeholder.com/150x60/333333/ffffff?text=OPS-CORE", "description": "Advanced helmet and protection systems"}
    ]
    
    for brand in brands:
        brand_obj = Brand(**brand)
        await db.brands.insert_one(brand_obj.dict())
    
    # Sample products
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
            "in_stock": True,
            "stock_quantity": 5,
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
            "in_stock": True,
            "stock_quantity": 3,
            "features": ["Gen 3 Tube", "Auto-Gated", "High Resolution", "Durable Housing"],
            "tags": ["night-vision", "optics", "tactical", "surveillance"],
            "is_restricted": True,
            "specifications": {"Generation": "Gen 3", "Resolution": "64 lp/mm", "Weight": "1.2 lbs"}
        }
    ]
    
    for product in products:
        product_obj = Product(**product)
        await db.products.insert_one(product_obj.dict())
    
    return {"message": "Sample data initialized successfully"}

# Product endpoints
@api_router.get("/products", response_model=List[Product])
async def get_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
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
    
    products = await db.products.find(filter_query).skip(skip).limit(limit).to_list(length=None)
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
    products = await db.products.find({"original_price": {"$exists": True}}).limit(6).to_list(length=None)
    return [Product(**product) for product in products]

# Original status endpoints
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

@api_router.get("/")
async def root():
    return {"message": "TacticalGear API v1.0"}

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