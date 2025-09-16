import React, { useState, useEffect, createContext, useContext } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link, useNavigate } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Context for Authentication and Cart
const AppContext = createContext();

const AppProvider = ({ children }) => {
  const [dealer, setDealer] = useState(null);
  const [cart, setCart] = useState({ items: [], total: 0 });
  const [sessionId] = useState(() => Math.random().toString(36).substr(2, 9));

  useEffect(() => {
    // Check for stored token
    const token = localStorage.getItem('dealer_token');
    if (token) {
      fetchDealerProfile(token);
    }
    
    // Load cart
    fetchCart();
  }, []);

  const fetchDealerProfile = async (token) => {
    try {
      const response = await axios.get(`${API}/dealers/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setDealer(response.data);
    } catch (error) {
      localStorage.removeItem('dealer_token');
    }
  };

  const fetchCart = async () => {
    try {
      const response = await axios.get(`${API}/cart/${sessionId}`);
      setCart(response.data);
    } catch (error) {
      console.error('Error fetching cart:', error);
    }
  };

  const addToCart = async (productId, quantity = 1) => {
    try {
      await axios.post(`${API}/cart/add`, {
        product_id: productId,
        quantity,
        session_id: sessionId
      });
      fetchCart();
      return true;
    } catch (error) {
      console.error('Error adding to cart:', error);
      return false;
    }
  };

  const removeFromCart = async (productId) => {
    try {
      await axios.delete(`${API}/cart/${sessionId}/item/${productId}`);
      fetchCart();
    } catch (error) {
      console.error('Error removing from cart:', error);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await axios.post(`${API}/dealers/login`, { email, password });
      const { access_token, dealer: dealerData } = response.data;
      localStorage.setItem('dealer_token', access_token);
      setDealer(dealerData);
      return { success: true, dealer: dealerData };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  };

  const register = async (dealerData) => {
    try {
      await axios.post(`${API}/dealers/register`, dealerData);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Registration failed' };
    }
  };

  const logout = () => {
    localStorage.removeItem('dealer_token');
    setDealer(null);
  };

  return (
    <AppContext.Provider value={{
      dealer, cart, sessionId, login, register, logout, addToCart, removeFromCart, fetchCart
    }}>
      {children}
    </AppContext.Provider>
  );
};

const useApp = () => useContext(AppContext);

// Navigation Component
const Navigation = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { dealer, cart, logout } = useApp();
  const navigate = useNavigate();
  
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
          
          {/* Cart and Auth */}
          <div className="flex items-center space-x-4">
            <button 
              onClick={() => navigate('/cart')}
              className="relative hover:text-red-400 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m2.6 8L6 7H2m0 0h2m4 8a2 2 0 100 4 2 2 0 000-4zm10 0a2 2 0 100 4 2 2 0 000-4z" />
              </svg>
              {cart.items.length > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-5 h-5 text-xs flex items-center justify-center">
                  {cart.items.reduce((sum, item) => sum + item.quantity, 0)}
                </span>
              )}
            </button>
            
            {dealer ? (
              <div className="relative group">
                <button className="flex items-center space-x-2 hover:text-red-400">
                  <span>{dealer.contact_name}</span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <div className="absolute right-0 mt-2 w-48 bg-white text-black rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                  <Link to="/profile" className="block px-4 py-2 hover:bg-gray-100">Profile</Link>
                  <Link to="/orders" className="block px-4 py-2 hover:bg-gray-100">Orders</Link>
                  <button onClick={logout} className="w-full text-left px-4 py-2 hover:bg-gray-100">Logout</button>
                </div>
              </div>
            ) : (
              <Link to="/login" className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded transition-colors">
                Dealer Login
              </Link>
            )}
            
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

// Price Range Slider Component
const PriceRangeSlider = ({ minPrice, maxPrice, value, onChange }) => {
  return (
    <div className="px-3 py-2">
      <div className="flex justify-between text-sm text-gray-600 mb-2">
        <span>${value[0]}</span>
        <span>${value[1]}</span>
      </div>
      <div className="relative">
        <input
          type="range"
          min={minPrice}
          max={maxPrice}
          value={value[0]}
          onChange={(e) => onChange([parseInt(e.target.value), value[1]])}
          className="slider-thumb-1 absolute w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
        <input
          type="range"
          min={minPrice}
          max={maxPrice}
          value={value[1]}
          onChange={(e) => onChange([value[0], parseInt(e.target.value)])}
          className="slider-thumb-2 absolute w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
      </div>
    </div>
  );
};

// Brand Logo Slideshow Component
const BrandLogoSlideshow = ({ brands }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  
  const visibleLogos = 6; // Number of logos visible at once
  const duplicatedBrands = [...brands, ...brands]; // Duplicate for seamless loop
  
  useEffect(() => {
    if (brands.length === 0) return;
    
    const autoSlide = setInterval(() => {
      setCurrentIndex(prev => {
        const nextIndex = prev + 1;
        // Reset to 0 when we've scrolled through all original brands
        return nextIndex >= brands.length ? 0 : nextIndex;
      });
    }, 2000); // Auto slide every 2 seconds
    
    return () => clearInterval(autoSlide);
  }, [brands.length]);
  
  if (!brands || brands.length === 0) {
    return null;
  }
  
  return (
    <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-80 backdrop-blur-sm py-4">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-3">
          <p className="text-white text-sm font-semibold tracking-wider">
            TRUSTED BY PROFESSIONALS WORLDWIDE
          </p>
        </div>
        
        <div className="overflow-hidden">
          <div 
            className="flex transition-transform duration-700 ease-in-out"
            style={{ 
              transform: `translateX(-${currentIndex * (100 / visibleLogos)}%)`,
              width: `${(duplicatedBrands.length / visibleLogos) * 100}%`
            }}
          >
            {duplicatedBrands.map((brand, index) => (
              <div 
                key={`${brand.name}-${index}`}
                className="flex-shrink-0 px-4"
                style={{ width: `${100 / duplicatedBrands.length}%` }}
              >
                <div className="bg-white bg-opacity-90 rounded-lg p-4 h-20 flex items-center justify-center hover:bg-opacity-100 transition-all duration-300 transform hover:scale-105">
                  <img 
                    src={brand.logo_url} 
                    alt={brand.name}
                    className="max-h-12 max-w-full object-contain filter brightness-75 hover:brightness-100 transition-all duration-300"
                    loading="lazy"
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Progress dots */}
        <div className="flex justify-center mt-3 space-x-1">
          {brands.map((_, index) => (
            <div
              key={index}
              className={`w-2 h-2 rounded-full transition-all duration-300 ${
                index === currentIndex 
                  ? 'bg-red-500 scale-125' 
                  : 'bg-white bg-opacity-50'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

// Enhanced Hero Section with Brand Slideshow
const HeroSection = ({ brands = [] }) => {
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
                <Link to="/products" className="bg-red-600 hover:bg-red-700 text-white px-8 py-4 text-lg font-semibold rounded-lg transition-colors">
                  Shop Now
                </Link>
              </div>
            </div>
          </div>
        </div>
      ))}
      
      {/* Slide indicators */}
      <div className="absolute bottom-24 left-1/2 transform -translate-x-1/2 flex space-x-2">
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
      
      {/* Brand Logo Slideshow at bottom */}
      <BrandLogoSlideshow brands={brands} />
    </div>
  );
};

// Home Page Components (keeping all existing ones)
const TrendingGear = ({ products }) => {
  const { addToCart } = useApp();
  
  const handleAddToCart = async (productId) => {
    const success = await addToCart(productId);
    if (success) {
      alert('Product added to cart!');
    } else {
      alert('Error adding product to cart');
    }
  };

  return (
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
                <div className="flex justify-between items-center mb-4">
                  <span className="text-2xl font-bold text-red-600">${product.price}</span>
                  <div className="flex items-center">
                    <span className="text-yellow-400">★</span>
                    <span className="ml-1 text-gray-600">{product.rating}</span>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <button 
                    onClick={() => handleAddToCart(product.id)}
                    disabled={!product.in_stock}
                    className="flex-1 bg-red-600 text-white py-2 rounded-lg hover:bg-red-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
                  >
                    {product.in_stock ? 'Add to Cart' : 'Out of Stock'}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

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

// New Arrivals Carousel Component
const NewArrivals = ({ products }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const { addToCart } = useApp();
  
  const itemsPerView = {
    mobile: 1,
    tablet: 2, 
    desktop: 3
  };
  
  const [itemsToShow, setItemsToShow] = useState(itemsPerView.desktop);
  
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 768) {
        setItemsToShow(itemsPerView.mobile);
      } else if (window.innerWidth < 1024) {
        setItemsToShow(itemsPerView.tablet);
      } else {
        setItemsToShow(itemsPerView.desktop);
      }
    };
    
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  const maxIndex = Math.max(0, products.length - itemsToShow);
  
  const nextSlide = () => {
    setCurrentIndex(prev => (prev >= maxIndex ? 0 : prev + 1));
  };
  
  const prevSlide = () => {
    setCurrentIndex(prev => (prev <= 0 ? maxIndex : prev - 1));
  };
  
  const handleAddToCart = async (productId) => {
    const success = await addToCart(productId);
    if (success) {
      alert('Product added to cart!');
    } else {
      alert('Error adding product to cart');
    }
  };
  
  if (!products || products.length === 0) {
    return null;
  }
  
  return (
    <section className="py-16 bg-gradient-to-br from-gray-900 to-black text-white">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4">NEW ARRIVALS</h2>
          <p className="text-xl text-gray-300">Latest tactical gear and equipment</p>
          <div className="w-24 h-1 bg-red-500 mx-auto mt-4"></div>
        </div>
        
        <div className="relative">
          {/* Carousel Container */}
          <div className="overflow-hidden">
            <div 
              className="flex transition-transform duration-500 ease-in-out"
              style={{ 
                transform: `translateX(-${currentIndex * (100 / itemsToShow)}%)`,
                width: `${(products.length / itemsToShow) * 100}%`
              }}
            >
              {products.map((product) => (
                <div 
                  key={product.id}
                  className="px-3"
                  style={{ width: `${100 / products.length}%` }}
                >
                  <div className="bg-white text-black rounded-lg shadow-xl overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
                    <div className="relative">
                      <img 
                        src={product.image_url} 
                        alt={product.name}
                        className="w-full h-64 object-cover"
                      />
                      <div className="absolute top-4 left-4">
                        <span className="bg-red-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                          NEW
                        </span>
                      </div>
                      <div className="absolute top-4 right-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                          product.in_stock ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
                        }`}>
                          {product.in_stock ? 'IN STOCK' : 'OUT OF STOCK'}
                        </span>
                      </div>
                    </div>
                    
                    <div className="p-6">
                      <div className="mb-2">
                        <h3 className="text-xl font-bold mb-1 line-clamp-2">{product.name}</h3>
                        <p className="text-gray-600 text-sm font-medium">{product.brand}</p>
                      </div>
                      
                      <p className="text-gray-700 text-sm mb-4 line-clamp-2">
                        {product.description}
                      </p>
                      
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-1">
                          <div className="flex text-yellow-400">
                            {[...Array(5)].map((_, i) => (
                              <span key={i} className={i < Math.floor(product.rating) ? 'text-yellow-400' : 'text-gray-300'}>
                                ★
                              </span>
                            ))}
                          </div>
                          <span className="text-gray-600 text-sm">({product.review_count})</span>
                        </div>
                        <div className="text-right">
                          <div className="flex items-center space-x-2">
                            <span className="text-2xl font-bold text-red-600">${product.price}</span>
                            {product.original_price && (
                              <span className="text-sm line-through text-gray-400">
                                ${product.original_price}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                      
                      {product.features && product.features.length > 0 && (
                        <div className="mb-4">
                          <p className="text-sm font-semibold mb-2">Key Features:</p>
                          <ul className="text-sm text-gray-600 space-y-1">
                            {product.features.slice(0, 2).map((feature, idx) => (
                              <li key={idx} className="flex items-center">
                                <span className="w-1 h-1 bg-red-500 rounded-full mr-2"></span>
                                {feature}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      <div className="flex space-x-2">
                        <button 
                          onClick={() => handleAddToCart(product.id)}
                          disabled={!product.in_stock}
                          className="flex-1 bg-red-600 text-white py-3 px-4 rounded-lg hover:bg-red-700 transition-colors font-semibold disabled:bg-gray-400 disabled:cursor-not-allowed"
                        >
                          {product.in_stock ? 'Add to Cart' : 'Out of Stock'}
                        </button>
                        <button className="px-4 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Navigation Arrows */}
          {products.length > itemsToShow && (
            <>
              <button
                onClick={prevSlide}
                className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-red-600 hover:bg-red-700 text-white p-3 rounded-full shadow-lg transition-all duration-300 z-10"
                aria-label="Previous slide"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              
              <button
                onClick={nextSlide}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-red-600 hover:bg-red-700 text-white p-3 rounded-full shadow-lg transition-all duration-300 z-10"
                aria-label="Next slide"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </>
          )}
          
          {/* Dots Indicator */}
          {products.length > itemsToShow && (
            <div className="flex justify-center mt-8 space-x-2">
              {[...Array(maxIndex + 1)].map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentIndex(index)}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    index === currentIndex 
                      ? 'bg-red-500 scale-125' 
                      : 'bg-gray-400 hover:bg-gray-300'
                  }`}
                  aria-label={`Go to slide ${index + 1}`}
                />
              ))}
            </div>
          )}
        </div>
        
        {/* View All Button */}
        <div className="text-center mt-8">
          <Link 
            to="/products" 
            className="inline-block bg-transparent border-2 border-red-500 text-red-500 hover:bg-red-500 hover:text-white px-8 py-3 rounded-lg font-semibold transition-all duration-300"
          >
            View All New Arrivals
          </Link>
        </div>
      </div>
    </section>
  );
};

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
  const [newArrivals, setNewArrivals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeData = async () => {
      try {
        // Initialize sample data first
        await axios.post(`${API}/initialize-data`);
        
        // Then fetch all data
        const [productsRes, categoriesRes, brandsRes, dealsRes, newArrivalsRes] = await Promise.all([
          axios.get(`${API}/products`),
          axios.get(`${API}/categories`),
          axios.get(`${API}/brands`),
          axios.get(`${API}/products/deals`),
          axios.get(`${API}/products/new-arrivals`)
        ]);
        
        setProducts(productsRes.data);
        setCategories(categoriesRes.data);
        setBrands(brandsRes.data);
        setDeals(dealsRes.data);
        setNewArrivals(newArrivalsRes.data);
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
      <HeroSection brands={brands} />
      <NewArrivals products={newArrivals} />
      <TrendingGear products={products} />
      <DepartmentOfDeals deals={deals} />
      <CustomerTopPicks products={products} />   
      <PopularCategories categories={categories} />
      <TopBrands brands={brands} />
      <TacticalExperts />
    </div>
  );
};

// Enhanced Products Page with Advanced Filtering
const Products = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);
  const [priceRange, setPriceRange] = useState([0, 1000]);
  const [maxPriceRange, setMaxPriceRange] = useState([0, 3000]);
  const [filters, setFilters] = useState({
    category: '',
    brand: '',
    minPrice: '',
    maxPrice: '',
    search: '',
    inStock: ''
  });
  const [loading, setLoading] = useState(true);
  const { addToCart } = useApp();

  useEffect(() => {
    fetchProducts();
    fetchFilters();
    fetchPriceRange();
  }, [filters]);

  const fetchProducts = async () => {
    try {
      const params = new URLSearchParams();
      Object.keys(filters).forEach(key => {
        if (filters[key]) {
          const paramKey = key === 'minPrice' ? 'min_price' : 
                          key === 'maxPrice' ? 'max_price' : 
                          key === 'inStock' ? 'in_stock' : key;
          params.append(paramKey, filters[key]);
        }
      });
      
      // Add price range from slider
      if (priceRange[0] > maxPriceRange[0]) params.append('min_price', priceRange[0]);
      if (priceRange[1] < maxPriceRange[1]) params.append('max_price', priceRange[1]);
      
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
        axios.get(`${API}/categories/with-counts`),
        axios.get(`${API}/brands/with-counts`)
      ]);
      setCategories(categoriesRes.data);
      setBrands(brandsRes.data);
    } catch (error) {
      console.error('Error fetching filters:', error);
    }
  };

  const fetchPriceRange = async () => {
    try {
      const response = await axios.get(`${API}/products/price-range`);
      const { min_price, max_price } = response.data;
      setMaxPriceRange([min_price, max_price]);
      setPriceRange([min_price, max_price]);
    } catch (error) {
      console.error('Error fetching price range:', error);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleAddToCart = async (productId) => {
    const success = await addToCart(productId);
    if (success) {
      alert('Product added to cart!');
    } else {
      alert('Error adding product to cart');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8">Tactical Products</h1>
        
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Enhanced Advanced Side Filter */}
          <div className="lg:w-1/4">
            <div className="bg-white p-6 rounded-lg shadow-lg sticky top-24">
              <h3 className="text-xl font-bold mb-6">Advanced Filters</h3>
              
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
              
              {/* Category Filter with Counts */}
              <div className="mb-6">
                <label className="block text-sm font-medium mb-2">Categories</label>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="category"
                      value=""
                      checked={filters.category === ''}
                      onChange={(e) => handleFilterChange('category', e.target.value)}
                      className="mr-2"
                    />
                    <span>All Categories</span>
                  </label>
                  {categories.map(cat => (
                    <label key={cat.id} className="flex items-center justify-between">
                      <div className="flex items-center">
                        <input
                          type="radio"
                          name="category"
                          value={cat.name}
                          checked={filters.category === cat.name}
                          onChange={(e) => handleFilterChange('category', e.target.value)}
                          className="mr-2"
                        />
                        <span className="text-sm">{cat.name}</span>
                      </div>
                      <span className="text-xs bg-gray-200 px-2 py-1 rounded">{cat.product_count}</span>
                    </label>
                  ))}
                </div>
              </div>
              
              {/* Brand Filter with Counts */}
              <div className="mb-6">
                <label className="block text-sm font-medium mb-2">Brands</label>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="brand"
                      value=""
                      checked={filters.brand === ''}
                      onChange={(e) => handleFilterChange('brand', e.target.value)}
                      className="mr-2"
                    />
                    <span>All Brands</span>
                  </label>
                  {brands.map(brand => (
                    <label key={brand.id} className="flex items-center justify-between">
                      <div className="flex items-center">
                        <input
                          type="radio"
                          name="brand"
                          value={brand.name}
                          checked={filters.brand === brand.name}
                          onChange={(e) => handleFilterChange('brand', e.target.value)}
                          className="mr-2"
                        />
                        <span className="text-sm">{brand.name}</span>
                      </div>
                      <span className="text-xs bg-gray-200 px-2 py-1 rounded">{brand.product_count}</span>
                    </label>
                  ))}
                </div>
              </div>
              
              {/* Stock Status Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium mb-2">Stock Status</label>
                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="stock"
                      value=""
                      checked={filters.inStock === ''}
                      onChange={(e) => handleFilterChange('inStock', '')}
                      className="mr-2"
                    />
                    <span>All Products</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="stock"
                      value="true"
                      checked={filters.inStock === 'true'}
                      onChange={(e) => handleFilterChange('inStock', 'true')}
                      className="mr-2"
                    />
                    <span className="text-green-600">In Stock</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="stock"
                      value="false"
                      checked={filters.inStock === 'false'}
                      onChange={(e) => handleFilterChange('inStock', 'false')}
                      className="mr-2"
                    />
                    <span className="text-red-600">Out of Stock</span>
                  </label>
                </div>
              </div>
              
              {/* Dynamic Price Range Slider */}
              <div className="mb-6">
                <label className="block text-sm font-medium mb-2">Price Range</label>
                <PriceRangeSlider
                  minPrice={maxPriceRange[0]}
                  maxPrice={maxPriceRange[1]}
                  value={priceRange}
                  onChange={setPriceRange}
                />
              </div>
              
              {/* Clear Filters */}
              <button
                onClick={() => {
                  setFilters({ category: '', brand: '', minPrice: '', maxPrice: '', search: '', inStock: '' });
                  setPriceRange(maxPriceRange);
                }}
                className="w-full bg-gray-500 text-white py-2 rounded-lg hover:bg-gray-600"
              >
                Clear All Filters
              </button>
            </div>
          </div>
          
          {/* Products Grid */}
          <div className="lg:w-3/4">
            <div className="mb-4 flex justify-between items-center">
              <p className="text-gray-600">{products.length} products found</p>
              <select className="border rounded-lg px-3 py-2">
                <option>Sort by: Featured</option>
                <option>Price: Low to High</option>
                <option>Price: High to Low</option>
                <option>Rating: High to Low</option>
                <option>Newest First</option>
              </select>
            </div>
            
            {loading ? (
              <div className="text-center py-8">Loading products...</div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {products.map(product => (
                  <div key={product.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
                    <img src={product.image_url} alt={product.name} className="w-full h-64 object-cover"/>
                    <div className="p-6">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="text-xl font-semibold">{product.name}</h3>
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${
                          product.in_stock ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {product.in_stock ? `${product.stock_quantity} in stock` : 'Out of Stock'}
                        </span>
                      </div>
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
                        <button 
                          onClick={() => handleAddToCart(product.id)}
                          disabled={!product.in_stock}
                          className="flex-1 bg-red-600 text-white py-2 rounded-lg hover:bg-red-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
                        >
                          {product.in_stock ? 'Add to Cart' : 'Out of Stock'}
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

// Dealer Login Page
const DealerLogin = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    company_name: '',
    contact_name: '',
    phone: '',
    address: '',
    license_number: ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const { login, register } = useApp();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      if (isLogin) {
        const result = await login(formData.email, formData.password);
        if (result.success) {
          navigate('/');
        } else {
          setMessage(result.error);
        }
      } else {
        const result = await register(formData);
        if (result.success) {
          setMessage('Registration successful! Please wait for approval.');
          setIsLogin(true);
        } else {
          setMessage(result.error);
        }
      }
    } catch (error) {
      setMessage('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-16 flex items-center justify-center">
      <div className="max-w-md w-full mx-4">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-3xl font-bold text-center mb-8">
            {isLogin ? 'Dealer Login' : 'Dealer Registration'}
          </h2>
          
          {message && (
            <div className={`mb-4 p-3 rounded ${
              message.includes('successful') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
            }`}>
              {message}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full p-3 border rounded-lg"
            />
            
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
              className="w-full p-3 border rounded-lg"
            />

            {!isLogin && (
              <>
                <input
                  type="text"
                  name="company_name"
                  placeholder="Company Name"
                  value={formData.company_name}
                  onChange={handleChange}
                  required
                  className="w-full p-3 border rounded-lg"
                />
                
                <input
                  type="text"
                  name="contact_name"
                  placeholder="Contact Name"
                  value={formData.contact_name}
                  onChange={handleChange}
                  required
                  className="w-full p-3 border rounded-lg"
                />
                
                <input
                  type="tel"
                  name="phone"
                  placeholder="Phone Number"
                  value={formData.phone}
                  onChange={handleChange}
                  required
                  className="w-full p-3 border rounded-lg"
                />
                
                <textarea
                  name="address"
                  placeholder="Business Address"
                  value={formData.address}
                  onChange={handleChange}
                  required
                  className="w-full p-3 border rounded-lg"
                  rows="3"
                />
                
                <input
                  type="text"
                  name="license_number"
                  placeholder="License Number"
                  value={formData.license_number}
                  onChange={handleChange}
                  required
                  className="w-full p-3 border rounded-lg"
                />
              </>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 disabled:bg-gray-400"
            >
              {loading ? 'Processing...' : (isLogin ? 'Login' : 'Register')}
            </button>
          </form>

          <div className="mt-6 text-center">
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-red-600 hover:text-red-700"
            >
              {isLogin ? 'Need to register?' : 'Already have an account?'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Shopping Cart Page
const ShoppingCart = () => {
  const { cart, removeFromCart, sessionId } = useApp();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleCheckout = async () => {
    if (cart.items.length === 0) return;
    
    setLoading(true);
    try {
      const response = await axios.post(`${API}/orders`, {
        session_id: sessionId,
        shipping_address: "123 Main St, City, State 12345",
        billing_address: "123 Main St, City, State 12345"
      });
      
      alert(`Order created successfully! Order ID: ${response.data.order_id}`);
      navigate('/');
    } catch (error) {
      alert('Error creating order. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Shopping Cart</h1>
        
        {cart.items.length === 0 ? (
          <div className="text-center py-12">
            <svg className="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m2.6 8L6 7H2m0 0h2m4 8a2 2 0 100 4 2 2 0 000-4zm10 0a2 2 0 100 4 2 2 0 000-4z" />
            </svg>
            <h2 className="text-2xl font-semibold text-gray-600 mb-4">Your cart is empty</h2>
            <Link to="/products" className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700">
              Continue Shopping
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-semibold mb-4">Cart Items</h2>
                {cart.items.map((item) => (
                  <div key={item.product_id} className="flex items-center space-x-4 py-4 border-b">
                    <img 
                      src={item.product?.image_url} 
                      alt={item.product?.name}
                      className="w-20 h-20 object-cover rounded"
                    />
                    <div className="flex-1">
                      <h3 className="font-semibold">{item.product?.name}</h3>
                      <p className="text-gray-600">{item.product?.brand}</p>
                      <p className="text-sm text-gray-500">Quantity: {item.quantity}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold">${(item.price * item.quantity).toFixed(2)}</p>
                      <button 
                        onClick={() => removeFromCart(item.product_id)}
                        className="text-red-600 hover:text-red-700 text-sm"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-semibold mb-4">Order Summary</h2>
                <div className="space-y-2 mb-4">
                  <div className="flex justify-between">
                    <span>Subtotal:</span>
                    <span>${cart.total?.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Shipping:</span>
                    <span>Free</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Tax:</span>
                    <span>${(cart.total * 0.08).toFixed(2)}</span>
                  </div>
                  <div className="border-t pt-2">
                    <div className="flex justify-between font-semibold text-lg">
                      <span>Total:</span>
                      <span>${(cart.total * 1.08).toFixed(2)}</span>
                    </div>
                  </div>
                </div>
                <button
                  onClick={handleCheckout}
                  disabled={loading}
                  className="w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 disabled:bg-gray-400"
                >
                  {loading ? 'Processing...' : 'Proceed to Checkout'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Enhanced About Page with Policies
const About = () => (
  <div className="min-h-screen bg-gray-50 pt-16">
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-center mb-12">About TacticalGear</h1>
      
      {/* Company Overview */}
      <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <div>
            <h2 className="text-3xl font-bold mb-6">Our Mission</h2>
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
          <div>
            <img 
              src="https://images.unsplash.com/photo-1705564667318-923901fb916a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwyfHx0YWN0aWNhbCUyMGdlYXJ8ZW58MHx8fHwxNzU3Mzc1OTk5fDA&ixlib=rb-4.1.0&q=85" 
              alt="Tactical team"
              className="rounded-lg shadow-lg"
            />
          </div>
        </div>
      </div>

      {/* Our Values */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="w-16 h-16 bg-red-600 rounded-full flex items-center justify-center mb-4">
            <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 className="text-xl font-bold mb-2">Quality Assurance</h3>
          <p>Every product undergoes rigorous testing by our team of tactical professionals before approval.</p>
        </div>
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="w-16 h-16 bg-red-600 rounded-full flex items-center justify-center mb-4">
            <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/>
            </svg>
          </div>
          <h3 className="text-xl font-bold mb-2">Authentic Equipment</h3>
          <p>We source directly from authorized manufacturers to guarantee authenticity and warranty coverage.</p>
        </div>
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="w-16 h-16 bg-red-600 rounded-full flex items-center justify-center mb-4">
            <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
              <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
            </svg>
          </div>
          <h3 className="text-xl font-bold mb-2">Expert Support</h3>
          <p>Our customer service team includes active and former military/law enforcement personnel.</p>
        </div>
      </div>

      {/* Company Policies */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-3xl font-bold mb-8 text-center">Our Policies</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">Dealer Program</h3>
            <ul className="space-y-2 text-gray-700">
              <li>• Exclusive dealer pricing on bulk orders</li>
              <li>• Priority access to new product releases</li>
              <li>• Dedicated account management</li>
              <li>• Extended payment terms for qualified dealers</li>
              <li>• Marketing support and product training</li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-xl font-bold mb-4">Quality Guarantee</h3>
            <ul className="space-y-2 text-gray-700">
              <li>• 30-day return policy on all items</li>
              <li>• Manufacturer warranty on all products</li>
              <li>• Free exchanges for defective items</li>
              <li>• Expert product consultation</li>
              <li>• Satisfaction guarantee or money back</li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-xl font-bold mb-4">Compliance Standards</h3>
            <ul className="space-y-2 text-gray-700">
              <li>• ITAR compliance for export regulations</li>
              <li>• Age verification for restricted items</li>
              <li>• FFL compliance for regulated products</li>
              <li>• Industry certifications maintained</li>
              <li>• Regular compliance audits</li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-xl font-bold mb-4">Shipping & Security</h3>
            <ul className="space-y-2 text-gray-700">
              <li>• Secure packaging for all shipments</li>
              <li>• Discreet shipping options available</li>
              <li>• Tracking provided for all orders</li>
              <li>• Insurance on high-value items</li>
              <li>• Same-day processing for most orders</li>
            </ul>
          </div>
        </div>
      </div>
      
      {/* Certifications */}
      <div className="bg-black text-white rounded-lg p-8 mt-8">
        <h2 className="text-3xl font-bold mb-8 text-center">Certifications & Partnerships</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-red-600 rounded-full mx-auto mb-2"></div>
            <p className="text-sm">GSA Approved</p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-red-600 rounded-full mx-auto mb-2"></div>
            <p className="text-sm">ITAR Registered</p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-red-600 rounded-full mx-auto mb-2"></div>
            <p className="text-sm">ISO 9001</p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-red-600 rounded-full mx-auto mb-2"></div>
            <p className="text-sm">FFL Licensed</p>
          </div>
        </div>
      </div>
    </div>
  </div>
);

// Other existing pages (Categories, Brands, Contact, Terms, Privacy) remain the same
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
        <AppProvider>
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
            <Route path="/login" element={<DealerLogin />} />
            <Route path="/cart" element={<ShoppingCart />} />
          </Routes>
          <Footer />
        </AppProvider>
      </BrowserRouter>
    </div>
  );
}

export default App;