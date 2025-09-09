#!/usr/bin/env python3

import requests
import json
import sys
from typing import Dict, List, Any
import time

# Backend URL from frontend/.env
BACKEND_URL = "https://gearup-tactical.preview.emergentagent.com/api"

class TacticalGearAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = []
        
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
                    has_deals = all("original_price" in prod and prod["original_price"] is not None for prod in products)
                    if has_deals:
                        self.log_test("Deal Products", True, f"Found {len(products)} products on sale")
                        tests_passed += 1
                    else:
                        self.log_test("Deal Products", False, "Products don't have original_price (not on sale)")
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
    
    def run_all_tests(self):
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