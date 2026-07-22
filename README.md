# 🛍️ ShopLite

A lightweight e-commerce web application built with **Flask** and **MongoDB**.

ShopLite demonstrates the core features of an online shopping platform, including browsing products, viewing product details, managing a shopping cart, and placing orders. It is designed as a simple learning project using only Flask, MongoDB, HTML, CSS, and Vanilla JavaScript.

---

## ✨ Features

- Browse all available products
- View detailed product information
- Add products to the shopping cart
- Update cart quantity or remove items
- Checkout and place an order
- Store orders in MongoDB
- Public seller page for submitting products
- Automatic sample product seeding on first launch
- Session-based shopping cart (no login required)

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- PyMongo
- MongoDB

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript
- Jinja2 Templates

### Database
- MongoDB

---

## 📁 Project Structure

```
ecommerce/
│
├── app.py
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── product.html
│   ├── cart.html
│   ├── checkout.html
│   └── confirmation.html
│
└── static/
    ├── css/
    │   └── main.css
    └── js/
        └── main.js
```

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/your-username/ShopLite.git
cd ShopLite
```

---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

### Start MongoDB

If you're running MongoDB locally:

```bash
mongodb://localhost:27017/
```

Or use MongoDB Atlas by setting your connection string:

```bash
export MONGO_URI="your_mongodb_connection_string"
```

---

### Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://localhost:5000
```

The application automatically inserts a few sample products into the database on the first run.

---

## ⚙️ Environment Variables

| Variable | Default |
|----------|---------|
| `MONGO_URI` | `mongodb://localhost:27017/` |
| `SECRET_KEY` | `dev-secret-key-change-in-production` |

Example:

```bash
export SECRET_KEY="your-secret-key"
export MONGO_URI="mongodb://localhost:27017/"
```

---

## 📄 Available Routes

| Route | Description |
|-------|-------------|
| `/` | View all products |
| `/product/<id>` | Product details |
| `/cart` | Shopping cart |
| `/cart/add` | Add item to cart |
| `/cart/update` | Update cart quantity |
| `/checkout` | Checkout page |
| `/seller` | Submit a product |
| `/order/<id>` | Order confirmation |

---

## 🗄️ Database Collections

### products

```json
{
  "name": "",
  "price": 0,
  "description": "",
  "category": "",
  "vendor": "",
  "stock": 0
}
```

### orders

```json
{
  "customer": {},
  "items": [],
  "total": 0,
  "placed_at": "",
  "status": "Pending"
}
```

---

## 📌 Future Improvements

Some features planned for future development:

- User authentication
- Customer accounts
- Admin dashboard
- Product CRUD
- Product search
- Product categories
- Wishlist
- Order history
- Payment gateway integration (Stripe)
- Persistent shopping cart
- Product images
- Reviews and ratings
- Email order confirmation
- Responsive UI improvements

---

## 📚 What I Learned

This project helped me gain practical experience with:

- Flask routing
- Template rendering with Jinja2
- MongoDB CRUD operations
- Session management
- Building a shopping cart
- Form handling
- Organizing a small full-stack web application

---

## 🤝 Contributing

Contributions, ideas, and suggestions are always welcome.

Feel free to fork the repository, open an issue, or submit a pull request.

---

## 📜 License

This project is intended for educational purposes and personal learning.
