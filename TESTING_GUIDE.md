# 🎯 TacticalGear B2B E-Commerce Platform - Complete Testing Guide

## 🚀 Quick Start - Setup Sample Data

**IMPORTANT: Run this first to populate the system with sample data**

1. Visit: `https://your-domain.com/api/initialize-data` (POST request)
2. Visit: `https://your-domain.com/api/create-sample-users` (POST request)

Or use curl:
```bash
curl -X POST https://your-domain.com/api/initialize-data
curl -X POST https://your-domain.com/api/create-sample-users
```

## 👥 Sample Login Credentials

### 🔵 **REGULAR USERS** (Customer Accounts)

#### User 1: Corporate Security Manager
- **Email:** `john.doe@company.com`
- **Password:** `password123`
- **Company:** Tactical Solutions LLC
- **Role:** Security team equipment procurement
- **Features to test:** Cart, Quote submission, Chat

#### User 2: Government Defense
- **Email:** `sarah.wilson@defense.gov`
- **Password:** `password123`
- **Company:** Defense Department
- **Role:** Military equipment procurement
- **Features to test:** Advanced quotes, Bulk orders

#### User 3: Law Enforcement
- **Email:** `mike.johnson@police.org`
- **Password:** `password123`
- **Company:** Metro Police Department
- **Role:** Police equipment procurement
- **Features to test:** Restricted items, Training equipment

### 🟢 **DEALERS** (Wholesale Partners)

#### Dealer 1: Wholesale Partner
- **Email:** `dealer@tactical-wholesale.com`
- **Password:** `dealer123`
- **Company:** Tactical Wholesale Partners
- **Contact:** Robert Smith
- **Status:** Approved ✅

#### Dealer 2: Supply Chain
- **Email:** `admin@tactical-supply.com`
- **Password:** `dealer123`
- **Company:** Tactical Supply Co
- **Contact:** Lisa Anderson
- **Status:** Approved ✅

### 🔴 **ADMIN ACCESS**
- **Note:** Admin functions are available through API endpoints
- Use dealer credentials for admin-level testing
- Admin endpoints: `/api/admin/quotes`, `/api/admin/chat/send`

---

## 🧪 Complete Testing Workflow

### **Phase 1: User Registration & Authentication**

#### Test 1.1: New User Registration
1. Go to `/user-login`
2. Click "Need an account? Sign up"
3. Fill registration form with business details
4. Verify email validation and required fields
5. Confirm successful registration message

#### Test 1.2: User Login
1. Use sample credentials: `john.doe@company.com` / `password123`
2. Verify redirect to homepage
3. Check navigation shows user name and dropdown
4. Confirm "Login" button changes to user profile

#### Test 1.3: Dealer Login  
1. Go to `/dealer-login`
2. Use: `dealer@tactical-wholesale.com` / `dealer123`
3. Verify separate dealer navigation
4. Confirm dealer portal access

### **Phase 2: Product Browsing & Cart Management**

#### Test 2.1: Guest User Restrictions
1. **Logout** from any account
2. Browse products on homepage or `/products`
3. Click "Login to Add" buttons
4. **Expected:** Redirect to `/user-login`

#### Test 2.2: Authenticated Cart Management
1. **Login** as `john.doe@company.com`
2. Navigate to `/products`
3. Click "Add to Cart" on multiple products
4. **Expected:** "Product added to cart!" confirmation
5. Check cart icon shows item count
6. Visit `/cart` to see added items

#### Test 2.3: Advanced Product Filtering
1. Go to `/products`
2. Test filters:
   - **Categories** with product counts
   - **Brands** with product counts  
   - **Price range** slider
   - **Stock status** (In Stock/Out of Stock)
   - **Search** functionality
3. Verify filter combinations work

### **Phase 3: Quote-Based Checkout Process**

#### Test 3.1: Cart to Quote Conversion
1. **Login** as `sarah.wilson@defense.gov`
2. Add 3-5 products to cart
3. Go to `/cart`
4. Click "Request Quote"
5. **Expected:** Redirect to `/quote-checkout`

#### Test 3.2: Quote Submission Form
1. On `/quote-checkout` page, fill out:
   - **Project Name:** "Q2 Equipment Upgrade"
   - **Intended Use:** Select "Military/Defense"
   - **Delivery Date:** Select future date
   - **Delivery/Billing Address:** Auto-populated from profile
   - **Company Size:** Select appropriate size
   - **Budget Range:** Select range
   - **Additional Requirements:** Add custom notes
2. Click "Submit Quote Request"
3. **Expected:** Success message and redirect to `/profile`

#### Test 3.3: Quote History Verification
1. After quote submission, check `/profile`
2. **Expected:** New quote appears with "Pending" status
3. Verify all quote details are displayed correctly
4. Check quote items match cart contents

### **Phase 4: User Profile & Quote Management**

#### Test 4.1: Profile Information
1. Go to `/profile` while logged in
2. Verify user information display:
   - Name, email, company details
   - Address information
   - Profile avatar with initials

#### Test 4.2: Quote Status Tracking
1. On `/profile`, check "Quote Requests" section
2. **Expected:** Sample quotes with different statuses:
   - **Pending** quotes (newly submitted)
   - **Approved** quotes (with admin notes)
3. Verify status color coding
4. Check quote details expansion

#### Test 4.3: Quote Actions
1. Find approved quote in profile
2. Click "Discuss Order" link
3. **Expected:** Redirect to `/chat`

### **Phase 5: Chat Communication System**

#### Test 5.1: User-Initiated Chat
1. **Login** as `john.doe@company.com`
2. Go to `/chat` or click "💬 Chat with Support" from profile
3. **Expected:** See existing sample messages
4. Type new message: "I need help with my order"
5. Click "Send"
6. **Expected:** Message appears immediately

#### Test 5.2: Chat Message History
1. Verify message ordering (oldest to newest)
2. Check message timestamps
3. Verify user vs admin message styling:
   - **User messages:** Right-aligned, red background
   - **Admin messages:** Left-aligned, gray background

#### Test 5.3: Real-time Chat Functionality
1. Send multiple messages
2. Verify messages persist after page refresh
3. Check chat scrolls to bottom automatically

### **Phase 6: Navigation & User Experience**

#### Test 6.1: Responsive Navigation
1. Test on different screen sizes
2. Verify mobile menu functionality
3. Check all navigation links work

#### Test 6.2: User State Management
1. Login → verify navigation changes
2. Add items to cart → verify cart count
3. Logout → verify reset to guest state
4. Refresh page → verify login persists

#### Test 6.3: Route Protection
1. Try accessing `/cart` without login
2. Try accessing `/profile` without login
3. Try accessing `/chat` without login
4. **Expected:** Redirect to `/user-login`

### **Phase 7: Admin Testing (API Level)**

#### Test 7.1: View All Quotes
```bash
curl -X GET https://your-domain.com/api/admin/quotes
```
**Expected:** List of all submitted quotes with user details

#### Test 7.2: Update Quote Status
```bash
curl -X PUT "https://your-domain.com/api/admin/quotes/{quote_id}/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "approved", "admin_notes": "Approved for processing"}'
```

#### Test 7.3: Admin Chat Response
```bash
curl -X POST https://your-domain.com/api/admin/chat/send \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_id_here",
    "sender_type": "admin", 
    "sender_name": "Support Team",
    "message": "We have received your quote and will review it within 24 hours."
  }'
```

---

## 🎨 UI/UX Features to Verify

### **Homepage Components**
- ✅ Hero slideshow with tactical images
- ✅ Transparent brand logo carousel (auto-sliding)
- ✅ New Arrivals section with product cards
- ✅ Trending Gear with cart buttons
- ✅ Department of Deals with pricing
- ✅ Customer Top Picks showcase
- ✅ Popular Categories grid
- ✅ Top Brands display
- ✅ Tactical Experts information
- ✅ Complete footer with links

### **Advanced Filtering**
- ✅ Side filter panel with counts
- ✅ Dynamic price range slider
- ✅ Stock status filtering
- ✅ Category/brand selection with product counts
- ✅ Search functionality
- ✅ Clear filters option

### **Responsive Design**
- ✅ Mobile-first approach
- ✅ Tablet and desktop optimization
- ✅ Touch-friendly interface
- ✅ Proper scaling on all devices

### **Authentication UI**
- ✅ Professional login/registration forms
- ✅ Form validation and error handling
- ✅ User feedback messages
- ✅ Secure password handling

---

## 🚨 Error Scenarios to Test

### **Authentication Errors**
1. Invalid login credentials
2. Registration with existing email
3. Accessing protected routes without login
4. Token expiration handling

### **Cart/Quote Errors**
1. Adding out-of-stock items
2. Empty cart checkout attempt
3. Invalid quote form submission
4. Network errors during submission

### **Chat Errors**
1. Sending empty messages
2. Chat access without login
3. Message send failures

---

## 📊 Success Metrics

After completing all tests, verify:

- ✅ **User Registration:** New accounts created successfully
- ✅ **Authentication:** Login/logout working properly
- ✅ **Product Browsing:** Filtering and search functional
- ✅ **Cart Management:** Items added/removed correctly
- ✅ **Quote System:** Submissions processed properly
- ✅ **Profile Management:** User data displayed correctly
- ✅ **Chat System:** Messages sent/received successfully
- ✅ **Admin Functions:** Quote management working
- ✅ **Responsive Design:** Works on all screen sizes
- ✅ **Navigation:** All routes accessible and protected

---

## 🔧 Troubleshooting

### **Common Issues**
1. **"Error adding product to cart"** → Ensure user is logged in
2. **"Cart is empty"** → Login first, then add products
3. **Quote submission fails** → Check all required fields
4. **Chat messages not sending** → Verify authentication
5. **Profile not loading** → Confirm valid user session

### **Quick Fixes**
- **Clear browser cache** if state issues occur
- **Check console logs** for JavaScript errors
- **Verify API endpoints** are responding
- **Confirm sample data** is loaded properly

---

## 🎯 Key Business Features Demonstrated

1. **B2B Authentication:** Separate user and dealer systems
2. **Quote-Based Sales:** Professional procurement process
3. **User Profile Management:** Complete business information
4. **Admin Communication:** Direct chat support
5. **Advanced Filtering:** Professional product discovery
6. **Mobile Responsive:** Cross-device compatibility
7. **Secure Cart Management:** User-specific shopping
8. **Quote Tracking:** Status updates and management
9. **Professional UI/UX:** Tactical gear industry theming
10. **Scalable Architecture:** Ready for production deployment

This testing guide ensures comprehensive validation of all B2B e-commerce features and user workflows.