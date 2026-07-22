# ShopLite — Flask + MongoDB E-Commerce App

A minimal but fully functional e-commerce app. Browse products, add to cart, and place orders.

## Stack
- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML + CSS + Vanilla JS (Jinja2 templates)
- **Cart**: Flask session (server-side, no login required)

## Project Structure
```
ecommerce/
├── app.py                  # All routes + MongoDB logic
├── requirements.txt
├── templates/
│   ├── base.html           # Shared nav + footer
│   ├── index.html          # Product listing
│   ├── product.html        # Product detail + add to cart
│   ├── cart.html           # Cart management
│   ├── checkout.html       # Order form
│   └── confirmation.html   # Order success page
└── static/
    ├── css/main.css
    └── js/main.js
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MongoDB
Make sure MongoDB is running locally on port 27017:
```bash
# macOS (Homebrew)
brew services start mongodb-community

# Ubuntu / Debian
sudo systemctl start mongod

# Or use a cloud URI (MongoDB Atlas)
export MONGO_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
```

### 3. Run the app
```bash
python app.py
```

Visit **http://localhost:5000**

The app auto-seeds 8 sample products on first run.

## Environment Variables
| Variable    | Default                    | Description           |
|-------------|----------------------------|-----------------------|
| `MONGO_URI` | `mongodb://localhost:27017/` | MongoDB connection string |
| `SECRET_KEY`| `dev-secret-key-change-in-prod` | Flask session secret |

Always set a strong `SECRET_KEY` in production.

## Routes
| Route                  | Method     | Description                  |
|------------------------|------------|------------------------------|
| `/`                    | GET        | Product listing (+ filter)   |
| `/product/<id>`        | GET        | Product detail               |
| `/cart/add`            | POST       | Add item to cart             |
| `/cart/update`         | POST       | Change qty or remove item    |
| `/cart`                | GET        | View cart                    |
| `/checkout`            | GET / POST | Show form / place order      |
| `/seller`              | GET / POST | Public product submission    |
| `/order/<id>`          | GET        | Order confirmation           |

## MongoDB Collections
- **products** — `{ name, price, description, category, vendor, stock }`
- **orders** — `{ customer, items, total, placed_at, status }`

## Extending This App
- Add user auth → Flask-Login + a `users` collection
- Add payments → Stripe Checkout
- Add admin panel → a `/admin` blueprint with product CRUD
- Make cart persistent → store cart in MongoDB keyed by session ID
