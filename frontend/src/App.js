import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link, useNavigate } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Navigation Component
const Navigation = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  return (
    <nav className="bg-black text-white shadow-lg fixed w-full top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link to="/" className="text-2xl font-bold text-red-500">
              TacticalGear
            </Link>
          </div>
          
          {/* Desktop Menu */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-8">
              <Link to="/" className="hover:text-red-400 transition-colors">Home</Link>
              <Link to="/products" className="hover:text-red-400 transition-colors">Products</Link>
              <Link to="/categories" className="hover:text-red-400 transition-colors">Categories</Link>
              <Link to="/brands" className="hover:text-red-400 transition-colors">Brands</Link>
              <Link to="/about" className="hover:text-red-400 transition-colors">About</Link>
              <Link to="/contact" className="hover:text-red-400 transition-colors">Contact</Link>
            </div>
          </div>
          
          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-white hover:text-red-400"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
        
        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-gray-900">
              <Link to="/" className="block hover:text-red-400 transition-colors py-2">Home</Link>
              <Link to="/products" className="block hover:text-red-400 transition-colors py-2">Products</Link>
              <Link to="/categories" className="block hover:text-red-400 transition-colors py-2">Categories</Link>
              <Link to="/brands" className="block hover:text-red-400 transition-colors py-2">Brands</Link>
              <Link to="/about" className="block hover:text-red-400 transition-colors py-2">About</Link>
              <Link to="/contact" className="block hover:text-red-400 transition-colors py-2">Contact</Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

// Hero Section with Slideshow
const HeroSection = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  
  const slides = [
    {
      image: "https://images.unsplash.com/photo-1714384716870-6d6322bf5a7f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwxfHx0YWN0aWNhbCUyMGdlYXJ8ZW58MHx8fHwxNzU3Mzc1OTk5fDA&ixlib=rb-4.1.0&q=85",
      title: "Professional Tactical Gear",
      subtitle: "Equipment trusted by military and law enforcement worldwide"
    },
    {
      image: "https://images.unsplash.com/photo-1705564667318-923901fb916a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwyfHx0YWN0aWNhbCUyMGdlYXJ8ZW58MHx8fHwxNzU3Mzc1OTk5fDA&ixlib=rb-4.1.0&q=85",
      title: "Combat Ready Apparel",
      subtitle: "Durable uniforms and tactical clothing for any mission"
    },
    {
      image: "https://images.unsplash.com/photo-1704278483976-9cca15325bc0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwzfHx0YWN0aWNhbCUyMGdlYXJ8ZW58MHx8fHwxNzU3Mzc1OTk5fDA&ixlib=rb-4.1.0&q=85",
      title: "Advanced Protection Systems",
      subtitle: "Body armor and protective equipment for maximum safety"
    }
  ];
  
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);
  
  return (
    <div className="relative h-screen overflow-hidden">
      {slides.map((slide, index) => (
        <div
          key={index}
          className={`absolute inset-0 transition-opacity duration-1000 ${
            index === currentSlide ? 'opacity-100' : 'opacity-0'
          }`}
        >
          <div 
            className="h-full bg-cover bg-center bg-no-repeat"
            style={{ backgroundImage: `url(${slide.image})` }}
          >
            <div className="absolute inset-0 bg-black bg-opacity-50"></div>
            <div className="relative flex items-center justify-center h-full text-center text-white">
              <div className="max-w-4xl px-4">
                <h1 className="text-5xl md:text-7xl font-bold mb-6">{slide.title}</h1>
                <p className="text-xl md:text-2xl mb-8">{slide.subtitle}</p>
                <button className="bg-red-600 hover:bg-red-700 text-white px-8 py-4 text-lg font-semibold rounded-lg transition-colors">
                  Shop Now
                </button>
              </div>
            </div>
          </div>
        </div>
      ))}
      
      {/* Slide indicators */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-2">
        {slides.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentSlide(index)}
            className={`w-3 h-3 rounded-full transition-colors ${
              index === currentSlide ? 'bg-red-500' : 'bg-white bg-opacity-50'
            }`}
          />
        ))}
      </div>
    </div>
  );
};

// Home Page Components
const TrendingGear = ({ products }) => (
  <section className="py-16 bg-gray-100">
    <div className="max-w-7xl mx-auto px-4">
      <h2 className="text-4xl font-bold text-center mb-12">TRENDING GEAR</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {products.slice(0, 6).map((product) => (
          <div key={product.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
            <img src={product.image_url} alt={product.name} className="w-full h-64 object-cover"/>
            <div className="p-6">
              <h3 className="text-xl font-semibold mb-2">{product.name}</h3>
              <p className="text-gray-600 mb-4">{product.description.substring(0, 100)}...</p>
              <div className="flex justify-between items-center">
                <span className="text-2xl font-bold text-red-600">${product.price}</span>
                <div className="flex items-center">
                  <span className="text-yellow-400">★</span>
                  <span className="ml-1 text-gray-600">{product.rating}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </section>
);

const DepartmentOfDeals = ({ deals }) => (
  <section className="py-16 bg-red-900 text-white">
    <div className="max-w-7xl mx-auto px-4">
      <h2 className="text-4xl font-bold text-center mb-12">DEPARTMENT OF DEALS</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {deals.map((product) => (
          <div key={product.id} className="bg-black bg-opacity-50 rounded-lg overflow-hidden hover:bg-opacity-70 transition-all">
            <img src={product.image_url} alt={product.name} className="w-full h-48 object-cover"/>
            <div className="p-6">
              <h3 className="text-xl font-semibold mb-2">{product.name}</h3>
              <div className="flex items-center space-x-2 mb-4">
                <span className="text-2xl font-bold">${product.price}</span>
                {product.original_price && (
                  <span className="text-lg line-through text-gray-400">${product.original_price}</span>
                )}
                <span className="bg-red-500 px-2 py-1 rounded text-sm">
                  SAVE ${(product.original_price - product.price).toFixed(2)}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </section>
);

const PopularCategories = ({ categories }) => (
  <section className="py-16">
    <div className="max-w-7xl mx-auto px-4">
      <h2 className="text-4xl font-bold text-center mb-12">POPULAR CATEGORIES</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {categories.map((category) => (
          <div key={category.id} className="relative group cursor-pointer">
            <div className="overflow-hidden rounded-lg">
              <img 
                src={category.image_url} 
                alt={category.name}
                className="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-500"
              />
              <div className="absolute inset-0 bg-black bg-opacity-40 group-hover:bg-opacity-60 transition-all">
                <div className="absolute bottom-4 left-4 text-white">
                  <h3 className="text-2xl font-bold">{category.name}</h3>
                  <p className="text-sm">{category.description}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </section>
);

const TopBrands = ({ brands }) => (
  <section className="py-16 bg-gray-100">
    <div className="max-w-7xl mx-auto px-4">
      <h2 className="text-4xl font-bold text-center mb-12">TOP BRANDS</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
        {brands.map((brand) => (
          <div key={brand.id} className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer">
            <img src={brand.logo_url} alt={brand.name} className="w-full h-12 object-contain mb-4"/>
            <h4 className="text-center font-semibold">{brand.name}</h4>
          </div>
        ))}
      </div>
    </div>
  </section>
);

const CustomerTopPicks = ({ products }) => (
  <section className="py-16">
    <div className="max-w-7xl mx-auto px-4">
      <h2 className="text-4xl font-bold text-center mb-12">CUSTOMER TOP PICKS</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {products.slice(0, 4).map((product) => (
          <div key={product.id} className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="relative">
              <img src={product.image_url} alt={product.name} className="w-full h-48 object-cover"/>
              <div className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded text-sm">
                ★ {product.rating}
              </div>
            </div>
            <div className="p-4">
              <h3 className="font-semibold mb-2">{product.name}</h3>
              <p className="text-2xl font-bold text-red-600">${product.price}</p>
              <p className="text-sm text-gray-600">{product.review_count} reviews</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  </section>
);

const TacticalExperts = () => (
  <section className="py-16 bg-black text-white">
    <div className="max-w-7xl mx-auto px-4">
      <h2 className="text-4xl font-bold text-center mb-12">TACTICAL EXPERTS</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="text-center">
          <div className="w-24 h-24 bg-red-600 rounded-full mx-auto mb-4 flex items-center justify-center">
            <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 className="text-xl font-bold mb-2">Expert Knowledge</h3>
          <p>Our team consists of military and law enforcement professionals</p>
        </div>
        <div className="text-center">
          <div className="w-24 h-24 bg-red-600 rounded-full mx-auto mb-4 flex items-center justify-center">
            <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/>
            </svg>
          </div>
          <h3 className="text-xl font-bold mb-2">Quality Assurance</h3>
          <p>Every product is tested and verified by our tactical experts</p>
        </div>
        <div className="text-center">
          <div className="w-24 h-24 bg-red-600 rounded-full mx-auto mb-4 flex items-center justify-center">
            <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
              <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
            </svg>
          </div>
          <h3 className="text-xl font-bold mb-2">24/7 Support</h3>
          <p>Get expert advice and support whenever you need it</p>
        </div>
      </div>
    </div>
  </section>
);

const Footer = () => (
  <footer className="bg-black text-white py-12">
    <div className="max-w-7xl mx-auto px-4">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <h3 className="text-2xl font-bold text-red-500 mb-4">TacticalGear</h3>
          <p className="text-gray-400">Professional tactical equipment for military, law enforcement, and civilian use.</p>
        </div>
        <div>
          <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
          <ul className="space-y-2 text-gray-400">
            <li><Link to="/products" className="hover:text-white">Products</Link></li>
            <li><Link to="/categories" className="hover:text-white">Categories</Link></li>
            <li><Link to="/brands" className="hover:text-white">Brands</Link></li>
            <li><Link to="/about" className="hover:text-white">About Us</Link></li>
          </ul>
        </div>
        <div>
          <h4 className="text-lg font-semibold mb-4">Support</h4>
          <ul className="space-y-2 text-gray-400">
            <li><Link to="/contact" className="hover:text-white">Contact Us</Link></li>
            <li><Link to="/faq" className="hover:text-white">FAQ</Link></li>
            <li><Link to="/shipping" className="hover:text-white">Shipping Info</Link></li>
            <li><Link to="/returns" className="hover:text-white">Returns</Link></li>
          </ul>
        </div>
        <div>
          <h4 className="text-lg font-semibold mb-4">Legal</h4>
          <ul className="space-y-2 text-gray-400">
            <li><Link to="/terms" className="hover:text-white">Terms of Service</Link></li>
            <li><Link to="/privacy" className="hover:text-white">Privacy Policy</Link></li>
            <li><Link to="/compliance" className="hover:text-white">Compliance</Link></li>
          </ul>
        </div>
      </div>
      <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
        <p>&copy; 2025 TacticalGear. All rights reserved. Professional tactical equipment supplier.</p>
      </div>
    </div>
  </footer>
);

// Home Page
const Home = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);
  const [deals, setDeals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeData = async () => {
      try {
        // Initialize sample data first
        await axios.post(`${API}/initialize-data`);
        
        // Then fetch all data
        const [productsRes, categoriesRes, brandsRes, dealsRes] = await Promise.all([
          axios.get(`${API}/products`),
          axios.get(`${API}/categories`),
          axios.get(`${API}/brands`),
          axios.get(`${API}/products/deals`)
        ]);
        
        setProducts(productsRes.data);
        setCategories(categoriesRes.data);
        setBrands(brandsRes.data);
        setDeals(dealsRes.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    initializeData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-2xl">Loading...</div>
      </div>
    );
  }

  return (
    <div>
      <HeroSection />
      <TrendingGear products={products} />
      <DepartmentOfDeals deals={deals} />
      <CustomerTopPicks products={products} />
      <PopularCategories categories={categories} />
      <TopBrands brands={brands} />
      <TacticalExperts />
    </div>
  );
};

// Products Page with Advanced Filtering
const Products = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);
  const [filters, setFilters] = useState({
    category: '',
    brand: '',
    minPrice: '',
    maxPrice: '',
    search: ''
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
    fetchFilters();
  }, [filters]);

  const fetchProducts = async () => {
    try {
      const params = new URLSearchParams();
      Object.keys(filters).forEach(key => {
        if (filters[key]) params.append(key === 'minPrice' ? 'min_price' : key === 'maxPrice' ? 'max_price' : key, filters[key]);
      });
      
      const response = await axios.get(`${API}/products?${params}`);
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchFilters = async () => {
    try {
      const [categoriesRes, brandsRes] = await Promise.all([
        axios.get(`${API}/categories`),
        axios.get(`${API}/brands`)
      ]);
      setCategories(categoriesRes.data);
      setBrands(brandsRes.data);
    } catch (error) {
      console.error('Error fetching filters:', error);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8">Tactical Products</h1>
        
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Advanced Side Filter */}
          <div className="lg:w-1/4">
            <div className="bg-white p-6 rounded-lg shadow-lg sticky top-24">
              <h3 className="text-xl font-bold mb-6">Filters</h3>
              
              {/* Search */}
              <div className="mb-6">
                <label className="block text-sm font-medium mb-2">Search</label>
                <input
                  type="text"
                  value={filters.search}
                  onChange={(e) => handleFilterChange('search', e.target.value)}
                  className="w-full p-2 border rounded-lg"
                  placeholder="Search products..."
                />
              </div>
              
              {/* Category Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium mb-2">Category</label>
                <select
                  value={filters.category}
                  onChange={(e) => handleFilterChange('category', e.target.value)}
                  className="w-full p-2 border rounded-lg"
                >
                  <option value="">All Categories</option>
                  {categories.map(cat => (
                    <option key={cat.id} value={cat.name}>{cat.name}</option>
                  ))}
                </select>
              </div>
              
              {/* Brand Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium mb-2">Brand</label>
                <select
                  value={filters.brand}
                  onChange={(e) => handleFilterChange('brand', e.target.value)}
                  className="w-full p-2 border rounded-lg"
                >
                  <option value="">All Brands</option>
                  {brands.map(brand => (
                    <option key={brand.id} value={brand.name}>{brand.name}</option>
                  ))}
                </select>
              </div>
              
              {/* Price Range */}
              <div className="mb-6">
                <label className="block text-sm font-medium mb-2">Price Range</label>
                <div className="flex gap-2">
                  <input
                    type="number"
                    value={filters.minPrice}
                    onChange={(e) => handleFilterChange('minPrice', e.target.value)}
                    className="w-1/2 p-2 border rounded-lg"
                    placeholder="Min"
                  />
                  <input
                    type="number"
                    value={filters.maxPrice}
                    onChange={(e) => handleFilterChange('maxPrice', e.target.value)}
                    className="w-1/2 p-2 border rounded-lg"
                    placeholder="Max"
                  />
                </div>
              </div>
              
              {/* Clear Filters */}
              <button
                onClick={() => setFilters({ category: '', brand: '', minPrice: '', maxPrice: '', search: '' })}
                className="w-full bg-gray-500 text-white py-2 rounded-lg hover:bg-gray-600"
              >
                Clear Filters
              </button>
            </div>
          </div>
          
          {/* Products Grid */}
          <div className="lg:w-3/4">
            <div className="mb-4">
              <p className="text-gray-600">{products.length} products found</p>
            </div>
            
            {loading ? (
              <div className="text-center py-8">Loading products...</div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {products.map(product => (
                  <div key={product.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
                    <img src={product.image_url} alt={product.name} className="w-full h-64 object-cover"/>
                    <div className="p-6">
                      <h3 className="text-xl font-semibold mb-2">{product.name}</h3>
                      <p className="text-gray-600 text-sm mb-2">{product.brand}</p>
                      <p className="text-gray-700 mb-4">{product.description.substring(0, 100)}...</p>
                      <div className="flex justify-between items-center mb-4">
                        <div>
                          <span className="text-2xl font-bold text-red-600">${product.price}</span>
                          {product.original_price && (
                            <span className="text-lg line-through text-gray-400 ml-2">${product.original_price}</span>
                          )}
                        </div>
                        <div className="flex items-center">
                          <span className="text-yellow-400">★</span>
                          <span className="ml-1 text-gray-600">{product.rating}</span>
                          <span className="ml-1 text-gray-500">({product.review_count})</span>
                        </div>
                      </div>
                      {product.features.length > 0 && (
                        <div className="mb-4">
                          <p className="text-sm font-semibold mb-1">Key Features:</p>
                          <ul className="text-sm text-gray-600">
                            {product.features.slice(0, 2).map((feature, idx) => (
                              <li key={idx}>• {feature}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      <div className="flex space-x-2">
                        <button className="flex-1 bg-red-600 text-white py-2 rounded-lg hover:bg-red-700 transition-colors">
                          View Details
                        </button>
                        <button className="px-4 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors">
                          ♡
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Other Pages
const Categories = () => {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get(`${API}/categories`);
        setCategories(response.data);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };
    fetchCategories();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8">Product Categories</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {categories.map(category => (
            <div key={category.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
              <img src={category.image_url} alt={category.name} className="w-full h-48 object-cover"/>
              <div className="p-6">
                <h3 className="text-2xl font-bold mb-2">{category.name}</h3>
                <p className="text-gray-600">{category.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const Brands = () => {
  const [brands, setBrands] = useState([]);

  useEffect(() => {
    const fetchBrands = async () => {
      try {
        const response = await axios.get(`${API}/brands`);
        setBrands(response.data);
      } catch (error) {
        console.error('Error fetching brands:', error);
      }
    };
    fetchBrands();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8">Our Brands</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {brands.map(brand => (
            <div key={brand.id} className="bg-white rounded-lg shadow-lg p-8 text-center hover:shadow-xl transition-shadow">
              <img src={brand.logo_url} alt={brand.name} className="w-32 h-16 object-contain mx-auto mb-4"/>
              <h3 className="text-2xl font-bold mb-2">{brand.name}</h3>
              <p className="text-gray-600">{brand.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const About = () => (
  <div className="min-h-screen bg-gray-50 pt-16">
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">About TacticalGear</h1>
      <div className="bg-white rounded-lg shadow-lg p-8">
        <p className="text-lg mb-6">
          TacticalGear is your premier destination for professional tactical equipment, serving military personnel, 
          law enforcement officers, and civilian customers worldwide. With over a decade of experience, we understand 
          the critical importance of reliable, high-quality gear in demanding situations.
        </p>
        <p className="text-lg mb-6">
          Our team consists of former military and law enforcement professionals who personally test and validate 
          every product we offer. We maintain strict quality standards and work directly with leading manufacturers 
          to ensure you receive authentic, battle-tested equipment.
        </p>
        <p className="text-lg">
          From body armor and tactical apparel to advanced optics and training equipment, we provide comprehensive 
          solutions for all your tactical needs. Trust TacticalGear for mission-critical equipment that performs 
          when it matters most.
        </p>
      </div>
    </div>
  </div>
);

const Contact = () => (
  <div className="min-h-screen bg-gray-50 pt-16">
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Contact Us</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-6">Get in Touch</h2>
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold">Phone</h3>
              <p className="text-gray-600">1-800-TACTICAL (1-800-822-8422)</p>
            </div>
            <div>
              <h3 className="font-semibold">Email</h3>
              <p className="text-gray-600">info@tacticalgear.com</p>
            </div>
            <div>
              <h3 className="font-semibold">Address</h3>
              <p className="text-gray-600">
                123 Tactical Way<br/>
                Defense City, DC 20001<br/>
                United States
              </p>
            </div>
            <div>
              <h3 className="font-semibold">Hours</h3>
              <p className="text-gray-600">
                Monday - Friday: 8:00 AM - 6:00 PM EST<br/>
                Saturday: 9:00 AM - 4:00 PM EST<br/>
                Sunday: Closed
              </p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-6">Send Message</h2>
          <form className="space-y-4">
            <input 
              type="text" 
              placeholder="Your Name" 
              className="w-full p-3 border rounded-lg"
            />
            <input 
              type="email" 
              placeholder="Your Email" 
              className="w-full p-3 border rounded-lg"
            />
            <input 
              type="text" 
              placeholder="Subject" 
              className="w-full p-3 border rounded-lg"
            />
            <textarea 
              placeholder="Your Message" 
              rows="5"
              className="w-full p-3 border rounded-lg"
            />
            <button className="w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700">
              Send Message
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
);

const Terms = () => (
  <div className="min-h-screen bg-gray-50 pt-16">
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Terms of Service</h1>
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="space-y-6">
          <section>
            <h2 className="text-2xl font-bold mb-4">1. Agreement to Terms</h2>
            <p>By accessing and using TacticalGear services, you agree to be bound by these Terms of Service and all applicable laws and regulations.</p>
          </section>
          
          <section>
            <h2 className="text-2xl font-bold mb-4">2. Product Usage</h2>
            <p>Tactical equipment sold through our platform is intended for legitimate military, law enforcement, and lawful civilian use only. Customers are responsible for compliance with all local, state, and federal regulations.</p>
          </section>
          
          <section>
            <h2 className="text-2xl font-bold mb-4">3. Age Verification</h2>
            <p>Certain products require age verification. Customers must be 18 years or older to purchase restricted items and may need to provide additional documentation.</p>
          </section>
          
          <section>
            <h2 className="text-2xl font-bold mb-4">4. Export Restrictions</h2>
            <p>Many tactical products are subject to export restrictions under ITAR and EAR regulations. International customers are responsible for import compliance.</p>
          </section>
          
          <section>
            <h2 className="text-2xl font-bold mb-4">5. Limitation of Liability</h2>
            <p>TacticalGear shall not be liable for any indirect, incidental, special, or consequential damages arising from the use of our products or services.</p>
          </section>
        </div>
      </div>
    </div>
  </div>
);

const Privacy = () => (
  <div className="min-h-screen bg-gray-50 pt-16">
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Privacy Policy</h1>
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="space-y-6">
          <section>
            <h2 className="text-2xl font-bold mb-4">Information We Collect</h2>
            <p>We collect information you provide directly, such as account details, purchase history, and communication preferences. We also collect technical information about your device and usage patterns.</p>
          </section>
          
          <section>
            <h2 className="text-2xl font-bold mb-4">How We Use Your Information</h2>
            <p>Your information is used to process orders, provide customer support, comply with legal requirements, and improve our services. We may also use it for security purposes and fraud prevention.</p>
          </section>
          
          <section>
            <h2 className="text-2xl font-bold mb-4">Information Sharing</h2>
            <p>We do not sell or rent your personal information. We may share information with service providers, law enforcement when required by law, and business partners for legitimate business purposes.</p>
          </section>
          
          <section>
            <h2 className="text-2xl font-bold mb-4">Data Security</h2>
            <p>We implement industry-standard security measures to protect your information, including encryption, secure servers, and regular security audits.</p>
          </section>
          
          <section>
            <h2 className="text-2xl font-bold mb-4">Your Rights</h2>
            <p>You have the right to access, update, or delete your personal information. Contact us at privacy@tacticalgear.com for assistance with privacy-related requests.</p>
          </section>
        </div>
      </div>
    </div>
  </div>
);

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Navigation />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<Products />} />
          <Route path="/categories" element={<Categories />} />
          <Route path="/brands" element={<Brands />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/terms" element={<Terms />} />
          <Route path="/privacy" element={<Privacy />} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </div>
  );
}

export default App;