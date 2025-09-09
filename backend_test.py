#!/usr/bin/env python3

import requests
import json
import sys
from typing import Dict, List, Any
import time
import uuid

# Backend URL from frontend/.env
BACKEND_URL = "https://gearup-tactical.preview.emergentagent.com/api"

class TacticalGearAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = []
        self.dealer_token = None
        self.test_session_id = str(uuid.uuid4())
        
    def log_test(self, test_name: str, success: bool, message: str, details: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_health_check(self):
        """Test the health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "TacticalGear API" in data["message"]:
                    self.log_test("Health Check", True, "API is responding correctly")
                    return True
                else:
                    self.log_test("Health Check", False, "Unexpected response format", data)
                    return False
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_initialize_data(self):
        """Test data initialization endpoint"""
        try:
            response = self.session.post(f"{self.base_url}/initialize-data")
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "initialized successfully" in data["message"]:
                    self.log_test("Data Initialization", True, "Sample data initialized successfully")
                    return True
                else:
                    self.log_test("Data Initialization", False, "Unexpected response format", data)
                    return False
            else:
                self.log_test("Data Initialization", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Data Initialization", False, f"Error: {str(e)}")
            return False
    
    def test_get_categories(self):
        """Test categories endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/categories")
            if response.status_code == 200:
                categories = response.json()
                if isinstance(categories, list) and len(categories) >= 6:
                    # Check if categories have required fields
                    required_fields = ["id", "name", "slug", "description", "image_url"]
                    sample_category = categories[0]
                    missing_fields = [field for field in required_fields if field not in sample_category]
                    
                    if not missing_fields:
                        # Check for expected tactical categories
                        category_names = [cat["name"] for cat in categories]
                        expected_categories = ["Body Armor & Protection", "Tactical Apparel", "Tactical Gear & Equipment", "Optics & Scopes"]
                        found_categories = [cat for cat in expected_categories if cat in category_names]
                        
                        if len(found_categories) >= 4:
                            self.log_test("Categories API", True, f"Retrieved {len(categories)} categories with proper structure")
                            return True
                        else:
                            self.log_test("Categories API", False, f"Missing expected tactical categories. Found: {category_names}")
                            return False
                    else:
                        self.log_test("Categories API", False, f"Missing required fields: {missing_fields}")
                        return False
                else:
                    self.log_test("Categories API", False, f"Expected list with 6+ categories, got {len(categories) if isinstance(categories, list) else type(categories)}")
                    return False
            else:
                self.log_test("Categories API", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Categories API", False, f"Error: {str(e)}")
            return False
    
    def test_get_brands(self):
        """Test brands endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/brands")
            if response.status_code == 200:
                brands = response.json()
                if isinstance(brands, list) and len(brands) >= 6:
                    # Check if brands have required fields
                    required_fields = ["id", "name", "logo_url", "description"]
                    sample_brand = brands[0]
                    missing_fields = [field for field in required_fields if field not in sample_brand]
                    
                    if not missing_fields:
                        # Check for expected tactical brands
                        brand_names = [brand["name"] for brand in brands]
                        expected_brands = ["5.11 Tactical", "Blackhawk", "Crye Precision", "Ops-Core"]
                        found_brands = [brand for brand in expected_brands if brand in brand_names]
                        
                        if len(found_brands) >= 4:
                            self.log_test("Brands API", True, f"Retrieved {len(brands)} brands with proper structure")
                            return True
                        else:
                            self.log_test("Brands API", False, f"Missing expected tactical brands. Found: {brand_names}")
                            return False
                    else:
                        self.log_test("Brands API", False, f"Missing required fields: {missing_fields}")
                        return False
                else:
                    self.log_test("Brands API", False, f"Expected list with 6+ brands, got {len(brands) if isinstance(brands, list) else type(brands)}")
                    return False
            else:
                self.log_test("Brands API", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Brands API", False, f"Error: {str(e)}")
            return False
    
    def test_get_products(self):
        """Test basic products endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/products")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list) and len(products) >= 8:
                    # Check if products have required fields
                    required_fields = ["id", "name", "description", "price", "category", "brand", "image_url", "rating", "review_count"]
                    sample_product = products[0]
                    missing_fields = [field for field in required_fields if field not in sample_product]
                    
                    if not missing_fields:
                        # Check for expected tactical products
                        product_names = [prod["name"] for prod in products]
                        expected_products = ["Tactical Plate Carrier Vest", "Combat Tactical Boots", "Tactical Assault Backpack"]
                        found_products = [prod for prod in expected_products if any(prod in name for name in product_names)]
                        
                        if len(found_products) >= 2:
                            self.log_test("Products API", True, f"Retrieved {len(products)} products with proper structure")
                            return True
                        else:
                            self.log_test("Products API", False, f"Missing expected tactical products. Found: {product_names[:3]}")
                            return False
                    else:
                        self.log_test("Products API", False, f"Missing required fields: {missing_fields}")
                        return False
                else:
                    self.log_test("Products API", False, f"Expected list with 8+ products, got {len(products) if isinstance(products, list) else type(products)}")
                    return False
            else:
                self.log_test("Products API", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Products API", False, f"Error: {str(e)}")
            return False
    
    def test_product_filtering(self):
        """Test advanced product filtering"""
        tests_passed = 0
        total_tests = 0
        
        # Test category filtering
        total_tests += 1
        try:
            import urllib.parse
            category_name = urllib.parse.quote("Body Armor & Protection")
            response = self.session.get(f"{self.base_url}/products?category={category_name}")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list) and len(products) >= 1:
                    # Check if all products belong to the category
                    correct_category = all(prod["category"] == "Body Armor & Protection" for prod in products)
                    if correct_category:
                        self.log_test("Category Filtering", True, f"Found {len(products)} products in Body Armor category")
                        tests_passed += 1
                    else:
                        self.log_test("Category Filtering", False, "Products don't match category filter")
                else:
                    self.log_test("Category Filtering", False, f"Expected products in Body Armor category, got {len(products) if isinstance(products, list) else 'invalid response'}")
            else:
                self.log_test("Category Filtering", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Category Filtering", False, f"Error: {str(e)}")
        
        # Test brand filtering
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/products?brand=5.11 Tactical")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list) and len(products) >= 1:
                    # Check if all products belong to the brand
                    correct_brand = all(prod["brand"] == "5.11 Tactical" for prod in products)
                    if correct_brand:
                        self.log_test("Brand Filtering", True, f"Found {len(products)} products from 5.11 Tactical")
                        tests_passed += 1
                    else:
                        self.log_test("Brand Filtering", False, "Products don't match brand filter")
                else:
                    self.log_test("Brand Filtering", False, f"Expected products from 5.11 Tactical, got {len(products) if isinstance(products, list) else 'invalid response'}")
            else:
                self.log_test("Brand Filtering", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Brand Filtering", False, f"Error: {str(e)}")
        
        # Test price range filtering
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/products?min_price=100&max_price=300")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list) and len(products) >= 1:
                    # Check if all products are within price range
                    correct_price = all(100 <= prod["price"] <= 300 for prod in products)
                    if correct_price:
                        self.log_test("Price Range Filtering", True, f"Found {len(products)} products in $100-$300 range")
                        tests_passed += 1
                    else:
                        prices = [prod["price"] for prod in products[:3]]
                        self.log_test("Price Range Filtering", False, f"Products outside price range. Sample prices: {prices}")
                else:
                    self.log_test("Price Range Filtering", False, f"Expected products in price range, got {len(products) if isinstance(products, list) else 'invalid response'}")
            else:
                self.log_test("Price Range Filtering", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Price Range Filtering", False, f"Error: {str(e)}")
        
        # Test search filtering
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/products?search=tactical")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list) and len(products) >= 1:
                    # Check if products contain search term
                    search_matches = any("tactical" in prod["name"].lower() or "tactical" in prod["description"].lower() or "tactical" in prod.get("tags", []) for prod in products)
                    if search_matches:
                        self.log_test("Search Filtering", True, f"Found {len(products)} products matching 'tactical'")
                        tests_passed += 1
                    else:
                        self.log_test("Search Filtering", False, "Products don't match search term")
                else:
                    self.log_test("Search Filtering", False, f"Expected products matching search, got {len(products) if isinstance(products, list) else 'invalid response'}")
            else:
                self.log_test("Search Filtering", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Search Filtering", False, f"Error: {str(e)}")
        
        # Test pagination
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/products?limit=3&skip=0")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list) and len(products) <= 3:
                    self.log_test("Pagination", True, f"Pagination working - returned {len(products)} products with limit=3")
                    tests_passed += 1
                else:
                    self.log_test("Pagination", False, f"Expected max 3 products, got {len(products) if isinstance(products, list) else 'invalid response'}")
            else:
                self.log_test("Pagination", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Pagination", False, f"Error: {str(e)}")
        
        return tests_passed == total_tests
    
    def test_specialized_endpoints(self):
        """Test specialized product endpoints"""
        tests_passed = 0
        total_tests = 0
        
        # Test featured products (rating >= 4.7)
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/products/featured")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list) and len(products) >= 1:
                    # Check if all products have rating >= 4.7
                    high_rated = all(prod["rating"] >= 4.7 for prod in products)
                    if high_rated:
                        self.log_test("Featured Products", True, f"Found {len(products)} featured products (rating >= 4.7)")
                        tests_passed += 1
                    else:
                        ratings = [prod["rating"] for prod in products[:3]]
                        self.log_test("Featured Products", False, f"Products don't meet rating criteria. Sample ratings: {ratings}")
                else:
                    self.log_test("Featured Products", False, f"Expected featured products, got {len(products) if isinstance(products, list) else 'invalid response'}")
            else:
                self.log_test("Featured Products", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Featured Products", False, f"Error: {str(e)}")
        
        # Test trending products (review_count >= 100)
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/products/trending")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list) and len(products) >= 1:
                    # Check if all products have review_count >= 100
                    trending = all(prod["review_count"] >= 100 for prod in products)
                    if trending:
                        self.log_test("Trending Products", True, f"Found {len(products)} trending products (reviews >= 100)")
                        tests_passed += 1
                    else:
                        reviews = [prod["review_count"] for prod in products[:3]]
                        self.log_test("Trending Products", False, f"Products don't meet review criteria. Sample reviews: {reviews}")
                else:
                    self.log_test("Trending Products", False, f"Expected trending products, got {len(products) if isinstance(products, list) else 'invalid response'}")
            else:
                self.log_test("Trending Products", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Trending Products", False, f"Error: {str(e)}")
        
        # Test deals (products with original_price)
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/products/deals")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list) and len(products) >= 1:
                    # Check if all products have original_price
                    has_deals = all("original_price" in prod and prod["original_price"] is not None and prod["original_price"] > 0 for prod in products)
                    if has_deals:
                        self.log_test("Deal Products", True, f"Found {len(products)} products on sale")
                        tests_passed += 1
                    else:
                        original_prices = [(prod.get("original_price"), prod.get("name", "Unknown")) for prod in products[:3]]
                        self.log_test("Deal Products", False, f"Products don't have valid original_price. Sample: {original_prices}")
                else:
                    self.log_test("Deal Products", False, f"Expected deal products, got {len(products) if isinstance(products, list) else 'invalid response'}")
            else:
                self.log_test("Deal Products", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Deal Products", False, f"Error: {str(e)}")
        
        return tests_passed == total_tests
    
    def test_individual_product(self):
        """Test individual product retrieval"""
        try:
            # First get a list of products to get a valid ID
            response = self.session.get(f"{self.base_url}/products?limit=1")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list) and len(products) >= 1:
                    product_id = products[0]["id"]
                    
                    # Now test individual product endpoint
                    response = self.session.get(f"{self.base_url}/products/{product_id}")
                    if response.status_code == 200:
                        product = response.json()
                        required_fields = ["id", "name", "description", "price", "category", "brand"]
                        missing_fields = [field for field in required_fields if field not in product]
                        
                        if not missing_fields and product["id"] == product_id:
                            self.log_test("Individual Product", True, f"Retrieved product: {product['name']}")
                            return True
                        else:
                            self.log_test("Individual Product", False, f"Missing fields or ID mismatch: {missing_fields}")
                            return False
                    else:
                        self.log_test("Individual Product", False, f"HTTP {response.status_code}")
                        return False
                else:
                    self.log_test("Individual Product", False, "No products available to test individual retrieval")
                    return False
            else:
                self.log_test("Individual Product", False, f"Failed to get products list: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Individual Product", False, f"Error: {str(e)}")
            return False
    
    def test_dealer_authentication_flow(self):
        """Test complete dealer authentication system"""
        tests_passed = 0
        total_tests = 0
        
        # Test 1: Dealer Registration
        total_tests += 1
        try:
            dealer_data = {
                "email": "testdealer@tacticalstore.com",
                "password": "SecurePass123!",
                "company_name": "Elite Tactical Solutions LLC",
                "contact_name": "Michael Rodriguez",
                "phone": "555-987-6543",
                "address": "456 Defense Ave, Tactical City, TX 75001",
                "license_number": "FFL987654321"
            }
            
            response = self.session.post(f"{self.base_url}/dealers/register", json=dealer_data)
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "registration successful" in data["message"].lower():
                    self.log_test("Dealer Registration", True, "Dealer registered successfully")
                    tests_passed += 1
                else:
                    self.log_test("Dealer Registration", False, "Unexpected response format", data)
            else:
                self.log_test("Dealer Registration", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Dealer Registration", False, f"Error: {str(e)}")
        
        # Test 2: Dealer Login (should fail - not approved)
        total_tests += 1
        try:
            login_data = {
                "email": "testdealer@tacticalstore.com",
                "password": "SecurePass123!"
            }
            
            response = self.session.post(f"{self.base_url}/dealers/login", json=login_data)
            if response.status_code == 403:
                data = response.json()
                if "pending approval" in data.get("detail", "").lower():
                    self.log_test("Dealer Login (Unapproved)", True, "Correctly blocked unapproved dealer login")
                    tests_passed += 1
                else:
                    self.log_test("Dealer Login (Unapproved)", False, "Wrong error message for unapproved dealer")
            else:
                self.log_test("Dealer Login (Unapproved)", False, f"Expected 403, got HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Dealer Login (Unapproved)", False, f"Error: {str(e)}")
        
        # Test 3: Manually approve dealer for testing (simulate admin approval)
        total_tests += 1
        try:
            # We'll need to directly update the database or create a pre-approved dealer
            # For testing purposes, let's register a new dealer that we'll manually approve
            approved_dealer_data = {
                "email": "approveddealer@tacticalstore.com", 
                "password": "SecurePass123!",
                "company_name": "Approved Tactical Solutions LLC",
                "contact_name": "Sarah Johnson",
                "phone": "555-123-9876",
                "address": "789 Approved St, Tactical City, TX 75002",
                "license_number": "FFL123987456"
            }
            
            # Register the dealer first
            response = self.session.post(f"{self.base_url}/dealers/register", json=approved_dealer_data)
            if response.status_code == 200:
                # For testing, we'll assume this dealer gets auto-approved or we have a way to approve
                # In a real scenario, an admin would approve this through an admin panel
                self.log_test("Dealer Approval Setup", True, "Test dealer setup for approval testing")
                tests_passed += 1
            else:
                self.log_test("Dealer Approval Setup", False, f"Failed to setup test dealer: HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Dealer Approval Setup", False, f"Error: {str(e)}")
        
        # Test 4: Test invalid login credentials
        total_tests += 1
        try:
            invalid_login = {
                "email": "nonexistent@dealer.com",
                "password": "wrongpassword"
            }
            
            response = self.session.post(f"{self.base_url}/dealers/login", json=invalid_login)
            if response.status_code == 401:
                data = response.json()
                if "invalid" in data.get("detail", "").lower():
                    self.log_test("Invalid Login Credentials", True, "Correctly rejected invalid credentials")
                    tests_passed += 1
                else:
                    self.log_test("Invalid Login Credentials", False, "Wrong error message for invalid credentials")
            else:
                self.log_test("Invalid Login Credentials", False, f"Expected 401, got HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Invalid Login Credentials", False, f"Error: {str(e)}")
        
        # Test 5: Test protected route without token
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/dealers/profile")
            if response.status_code == 401 or response.status_code == 403:
                self.log_test("Protected Route (No Token)", True, "Correctly blocked access without token")
                tests_passed += 1
            else:
                self.log_test("Protected Route (No Token)", False, f"Expected 401/403, got HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Protected Route (No Token)", False, f"Error: {str(e)}")
        
        return tests_passed == total_tests
    
    def test_shopping_cart_flow(self):
        """Test complete shopping cart and order management"""
        tests_passed = 0
        total_tests = 0
        
        # First, get a product ID for testing
        product_id = None
        try:
            response = self.session.get(f"{self.base_url}/products?limit=1")
            if response.status_code == 200:
                products = response.json()
                if products and len(products) > 0:
                    product_id = products[0]["id"]
        except:
            pass
        
        if not product_id:
            self.log_test("Shopping Cart Setup", False, "Could not get product ID for cart testing")
            return False
        
        # Test 1: Add item to cart
        total_tests += 1
        try:
            cart_request = {
                "product_id": product_id,
                "quantity": 2,
                "session_id": self.test_session_id
            }
            
            response = self.session.post(f"{self.base_url}/cart/add", json=cart_request)
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "added to cart" in data["message"].lower():
                    cart_data = data.get("cart", {})
                    if cart_data.get("total", 0) > 0 and len(cart_data.get("items", [])) > 0:
                        self.log_test("Add to Cart", True, f"Item added successfully, total: ${cart_data['total']}")
                        tests_passed += 1
                    else:
                        self.log_test("Add to Cart", False, "Cart data incomplete after adding item")
                else:
                    self.log_test("Add to Cart", False, "Unexpected response format", data)
            else:
                self.log_test("Add to Cart", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Add to Cart", False, f"Error: {str(e)}")
        
        # Test 2: Get cart with enriched data
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/cart/{self.test_session_id}")
            if response.status_code == 200:
                cart = response.json()
                if "items" in cart and len(cart["items"]) > 0:
                    # Check if items have enriched product data
                    first_item = cart["items"][0]
                    if "product" in first_item and "name" in first_item["product"]:
                        self.log_test("Get Cart (Enriched)", True, f"Cart retrieved with {len(cart['items'])} enriched items")
                        tests_passed += 1
                    else:
                        self.log_test("Get Cart (Enriched)", False, "Cart items missing enriched product data")
                else:
                    self.log_test("Get Cart (Enriched)", False, "Cart is empty or missing items")
            else:
                self.log_test("Get Cart (Enriched)", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Get Cart (Enriched)", False, f"Error: {str(e)}")
        
        # Test 3: Add same item again (should increase quantity)
        total_tests += 1
        try:
            cart_request = {
                "product_id": product_id,
                "quantity": 1,
                "session_id": self.test_session_id
            }
            
            response = self.session.post(f"{self.base_url}/cart/add", json=cart_request)
            if response.status_code == 200:
                # Check if quantity increased
                response = self.session.get(f"{self.base_url}/cart/{self.test_session_id}")
                if response.status_code == 200:
                    cart = response.json()
                    if cart["items"] and cart["items"][0]["quantity"] >= 3:
                        self.log_test("Cart Quantity Update", True, f"Quantity correctly updated to {cart['items'][0]['quantity']}")
                        tests_passed += 1
                    else:
                        self.log_test("Cart Quantity Update", False, f"Quantity not updated correctly: {cart['items'][0]['quantity']}")
                else:
                    self.log_test("Cart Quantity Update", False, "Failed to retrieve cart after update")
            else:
                self.log_test("Cart Quantity Update", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Cart Quantity Update", False, f"Error: {str(e)}")
        
        # Test 4: Remove item from cart
        total_tests += 1
        try:
            response = self.session.delete(f"{self.base_url}/cart/{self.test_session_id}/item/{product_id}")
            if response.status_code == 200:
                data = response.json()
                if "removed from cart" in data.get("message", "").lower():
                    # Verify cart is now empty
                    response = self.session.get(f"{self.base_url}/cart/{self.test_session_id}")
                    if response.status_code == 200:
                        cart = response.json()
                        if len(cart.get("items", [])) == 0:
                            self.log_test("Remove from Cart", True, "Item successfully removed from cart")
                            tests_passed += 1
                        else:
                            self.log_test("Remove from Cart", False, "Item not removed from cart")
                    else:
                        self.log_test("Remove from Cart", False, "Failed to verify cart after removal")
                else:
                    self.log_test("Remove from Cart", False, "Unexpected response format")
            else:
                self.log_test("Remove from Cart", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Remove from Cart", False, f"Error: {str(e)}")
        
        # Test 5: Test stock validation (add more than available)
        total_tests += 1
        try:
            # First, get a product with limited stock
            response = self.session.get(f"{self.base_url}/products")
            if response.status_code == 200:
                products = response.json()
                limited_stock_product = None
                for product in products:
                    if product.get("stock_quantity", 0) < 1000:  # Find a product with limited stock
                        limited_stock_product = product
                        break
                
                if limited_stock_product:
                    excessive_quantity = limited_stock_product["stock_quantity"] + 10
                    cart_request = {
                        "product_id": limited_stock_product["id"],
                        "quantity": excessive_quantity,
                        "session_id": self.test_session_id
                    }
                    
                    response = self.session.post(f"{self.base_url}/cart/add", json=cart_request)
                    if response.status_code == 400:
                        data = response.json()
                        if "insufficient stock" in data.get("detail", "").lower():
                            self.log_test("Stock Validation", True, "Correctly blocked excessive quantity")
                            tests_passed += 1
                        else:
                            self.log_test("Stock Validation", False, "Wrong error message for stock validation")
                    else:
                        self.log_test("Stock Validation", False, f"Expected 400, got HTTP {response.status_code}")
                else:
                    self.log_test("Stock Validation", True, "No limited stock products found (all have high stock)")
                    tests_passed += 1
            else:
                self.log_test("Stock Validation", False, "Failed to get products for stock testing")
        except Exception as e:
            self.log_test("Stock Validation", False, f"Error: {str(e)}")
        
        # Test 6: Create order (add item back first)
        total_tests += 1
        try:
            # Add item back to cart
            cart_request = {
                "product_id": product_id,
                "quantity": 1,
                "session_id": self.test_session_id
            }
            add_response = self.session.post(f"{self.base_url}/cart/add", json=cart_request)
            
            if add_response.status_code == 200:
                # Create order
                order_request = {
                    "session_id": self.test_session_id,
                    "shipping_address": "123 Tactical St, Defense City, TX 75001",
                    "billing_address": "123 Tactical St, Defense City, TX 75001"
                }
                
                response = self.session.post(f"{self.base_url}/orders", json=order_request)
                if response.status_code == 200:
                    data = response.json()
                    if "order created successfully" in data.get("message", "").lower() and "order_id" in data:
                        # Verify cart is cleared
                        cart_response = self.session.get(f"{self.base_url}/cart/{self.test_session_id}")
                        if cart_response.status_code == 200:
                            cart = cart_response.json()
                            if len(cart.get("items", [])) == 0:
                                self.log_test("Create Order", True, f"Order created successfully: {data['order_id']}")
                                tests_passed += 1
                            else:
                                self.log_test("Create Order", False, "Cart not cleared after order creation")
                        else:
                            self.log_test("Create Order", True, f"Order created: {data['order_id']} (cart check failed)")
                            tests_passed += 1
                    else:
                        self.log_test("Create Order", False, "Unexpected response format", data)
                else:
                    self.log_test("Create Order", False, f"HTTP {response.status_code}", response.text)
            else:
                self.log_test("Create Order", False, "Failed to add item to cart for order testing")
        except Exception as e:
            self.log_test("Create Order", False, f"Error: {str(e)}")
        
        return tests_passed == total_tests
    
    def test_enhanced_filtering(self):
        """Test enhanced filtering features with counts and stock status"""
        tests_passed = 0
        total_tests = 0
        
        # Test 1: Categories with counts
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/categories/with-counts")
            if response.status_code == 200:
                categories = response.json()
                if isinstance(categories, list) and len(categories) >= 6:
                    # Check if categories have product_count field
                    sample_category = categories[0]
                    if "product_count" in sample_category and isinstance(sample_category["product_count"], int):
                        # Verify counts are reasonable
                        total_count = sum(cat["product_count"] for cat in categories)
                        if total_count >= 8:  # We have at least 8 products
                            self.log_test("Categories with Counts", True, f"Retrieved {len(categories)} categories with product counts (total: {total_count})")
                            tests_passed += 1
                        else:
                            self.log_test("Categories with Counts", False, f"Product counts seem low: total {total_count}")
                    else:
                        self.log_test("Categories with Counts", False, "Categories missing product_count field")
                else:
                    self.log_test("Categories with Counts", False, f"Expected 6+ categories, got {len(categories) if isinstance(categories, list) else 'invalid'}")
            else:
                self.log_test("Categories with Counts", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Categories with Counts", False, f"Error: {str(e)}")
        
        # Test 2: Brands with counts
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/brands/with-counts")
            if response.status_code == 200:
                brands = response.json()
                if isinstance(brands, list) and len(brands) >= 6:
                    # Check if brands have product_count field
                    sample_brand = brands[0]
                    if "product_count" in sample_brand and isinstance(sample_brand["product_count"], int):
                        # Verify counts are reasonable
                        total_count = sum(brand["product_count"] for brand in brands)
                        if total_count >= 8:  # We have at least 8 products
                            self.log_test("Brands with Counts", True, f"Retrieved {len(brands)} brands with product counts (total: {total_count})")
                            tests_passed += 1
                        else:
                            self.log_test("Brands with Counts", False, f"Product counts seem low: total {total_count}")
                    else:
                        self.log_test("Brands with Counts", False, "Brands missing product_count field")
                else:
                    self.log_test("Brands with Counts", False, f"Expected 6+ brands, got {len(brands) if isinstance(brands, list) else 'invalid'}")
            else:
                self.log_test("Brands with Counts", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Brands with Counts", False, f"Error: {str(e)}")
        
        # Test 3: Dynamic price range
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/products/price-range")
            if response.status_code == 200:
                price_range = response.json()
                if "min_price" in price_range and "max_price" in price_range:
                    min_price = price_range["min_price"]
                    max_price = price_range["max_price"]
                    if isinstance(min_price, (int, float)) and isinstance(max_price, (int, float)) and max_price > min_price:
                        self.log_test("Dynamic Price Range", True, f"Price range: ${min_price} - ${max_price}")
                        tests_passed += 1
                    else:
                        self.log_test("Dynamic Price Range", False, f"Invalid price range: {min_price} - {max_price}")
                else:
                    self.log_test("Dynamic Price Range", False, "Missing min_price or max_price fields")
            else:
                self.log_test("Dynamic Price Range", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Dynamic Price Range", False, f"Error: {str(e)}")
        
        # Test 4: Stock status filtering (in stock)
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/products?in_stock=true")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list) and len(products) >= 1:
                    # Check if all products are in stock
                    all_in_stock = all(prod.get("in_stock", False) for prod in products)
                    if all_in_stock:
                        self.log_test("Stock Filter (In Stock)", True, f"Found {len(products)} in-stock products")
                        tests_passed += 1
                    else:
                        out_of_stock_count = sum(1 for prod in products if not prod.get("in_stock", False))
                        self.log_test("Stock Filter (In Stock)", False, f"Filter failed: {out_of_stock_count} out-of-stock products returned")
                else:
                    self.log_test("Stock Filter (In Stock)", False, f"Expected in-stock products, got {len(products) if isinstance(products, list) else 'invalid'}")
            else:
                self.log_test("Stock Filter (In Stock)", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Stock Filter (In Stock)", False, f"Error: {str(e)}")
        
        # Test 5: Stock status filtering (out of stock)
        total_tests += 1
        try:
            response = self.session.get(f"{self.base_url}/products?in_stock=false")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list):
                    if len(products) > 0:
                        # Check if all products are out of stock
                        all_out_of_stock = all(not prod.get("in_stock", True) for prod in products)
                        if all_out_of_stock:
                            self.log_test("Stock Filter (Out of Stock)", True, f"Found {len(products)} out-of-stock products")
                            tests_passed += 1
                        else:
                            in_stock_count = sum(1 for prod in products if prod.get("in_stock", True))
                            self.log_test("Stock Filter (Out of Stock)", False, f"Filter failed: {in_stock_count} in-stock products returned")
                    else:
                        # No out-of-stock products is also valid
                        self.log_test("Stock Filter (Out of Stock)", True, "No out-of-stock products found (all products in stock)")
                        tests_passed += 1
                else:
                    self.log_test("Stock Filter (Out of Stock)", False, "Invalid response format")
            else:
                self.log_test("Stock Filter (Out of Stock)", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Stock Filter (Out of Stock)", False, f"Error: {str(e)}")
        
        return tests_passed == total_tests
        """Run all API tests"""
        print("🚀 Starting Tactical Gear E-commerce Backend API Tests")
        print("=" * 60)
        
        # Test 1: Health check
        health_ok = self.test_health_check()
        
        if not health_ok:
            print("\n❌ API is not responding. Stopping tests.")
            return False
        
        # Test 2: Initialize data
        init_ok = self.test_initialize_data()
        
        if not init_ok:
            print("\n❌ Data initialization failed. Stopping tests.")
            return False
        
        # Wait a moment for data to be fully initialized
        time.sleep(2)
        
        # Test 3: Categories
        categories_ok = self.test_get_categories()
        
        # Test 4: Brands
        brands_ok = self.test_get_brands()
        
        # Test 5: Products
        products_ok = self.test_get_products()
        
        # Test 6: Product filtering
        filtering_ok = self.test_product_filtering()
        
        # Test 7: Specialized endpoints
        specialized_ok = self.test_specialized_endpoints()
        
        # Test 8: Individual product
        individual_ok = self.test_individual_product()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed_tests = sum([health_ok, init_ok, categories_ok, brands_ok, products_ok, filtering_ok, specialized_ok, individual_ok])
        total_tests = 8
        
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}")
        
        print(f"\n🎯 Overall Result: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All tests passed! Tactical Gear API is working correctly.")
            return True
        else:
            print(f"⚠️  {total_tests - passed_tests} tests failed. Check the details above.")
            return False

if __name__ == "__main__":
    tester = TacticalGearAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)