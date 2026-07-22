from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")

# MongoDB connection
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["ecommerce"]
products_col = db["products"]
orders_col = db["orders"]


def seed_products():
    """Seed sample products if collection is empty."""
    if products_col.count_documents({}) == 0:
        sample_products = [
            {"name": "Wireless Headphones", "price": 4999.00, "description": "Crisp audio, 20-hour battery, foldable design.", "category": "Electronics", "vendor": "AudioX", "stock": 15, "image_url": ""},
            {"name": "Mechanical Keyboard", "price": 3499.00, "description": "Tactile switches, RGB backlight, compact TKL layout.", "category": "Electronics", "vendor": "KeyWorks", "stock": 10, "image_url": ""},
            {"name": "Leather Wallet", "price": 1299.00, "description": "Slim bifold, genuine leather, 6 card slots.", "category": "Accessories", "vendor": "LuxeCraft", "stock": 30, "image_url": ""},
            {"name": "Running Shoes", "price": 2999.00, "description": "Lightweight mesh upper, cushioned sole, unisex.", "category": "Footwear", "vendor": "StridePro", "stock": 20, "image_url": ""},
            {"name": "Stainless Water Bottle", "price": 799.00, "description": "500ml, keeps cold 24h, leak-proof lid.", "category": "Kitchen", "vendor": "PureSip", "stock": 50, "image_url": ""},
            {"name": "Yoga Mat", "price": 1499.00, "description": "6mm thick, non-slip surface, carrying strap included.", "category": "Sports", "vendor": "FlexFlow", "stock": 25, "image_url": ""},
            {"name": "Portable Charger", "price": 1999.00, "description": "10,000mAh, dual USB-A + USB-C, fast charge.", "category": "Electronics", "vendor": "ChargePlus", "stock": 18, "image_url": ""},
            {"name": "Sunglasses", "price": 2499.00, "description": "UV400 protection, polarized lens, lightweight frame.", "category": "Accessories", "vendor": "VisionMark", "stock": 12, "image_url": ""},
        ]
        products_col.insert_many(sample_products)


seed_products()


# ── Helpers ────────────────────────────────────────────────────────────────────

def get_cart():
    return session.get("cart", {})

def cart_count():
    return sum(item["qty"] for item in get_cart().values())

def cart_total():
    return sum(item["price"] * item["qty"] for item in get_cart().values())


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    category = request.args.get("category", "")
    query = {"category": category} if category else {}
    products = list(products_col.find(query))
    categories = products_col.distinct("category")
    for p in products:
        p["_id"] = str(p["_id"])
    return render_template("index.html", products=products, categories=categories,
                           selected_category=category, cart_count=cart_count())


@app.route("/product/<product_id>")
def product(product_id):
    try:
        p = products_col.find_one({"_id": ObjectId(product_id)})
    except Exception:
        return redirect(url_for("index"))
    if not p:
        return redirect(url_for("index"))
    p["_id"] = str(p["_id"])
    return render_template("product.html", product=p, cart_count=cart_count())


@app.route("/seller", methods=["GET", "POST"])
def seller():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        vendor = request.form.get("vendor", "").strip()
        description = request.form.get("description", "").strip()
        image_url = request.form.get("image_url", "").strip()
        price_raw = request.form.get("price", "")
        stock_raw = request.form.get("stock", "")

        try:
            price = float(price_raw)
            stock = int(stock_raw)
        except (TypeError, ValueError):
            flash("Please enter valid numbers for price and stock.", "error")
            return render_template("seller.html", cart_count=cart_count())

        if not all([name, category, vendor, description]) or price < 0 or stock < 0:
            flash("Please fill in all required fields with valid values.", "error")
            return render_template("seller.html", cart_count=cart_count())

        product = {
            "name": name,
            "price": price,
            "description": description,
            "category": category,
            "vendor": vendor,
            "stock": stock,
            "image_url": image_url,
        }
        products_col.insert_one(product)
        flash("Product added successfully and is now visible in the marketplace.", "success")
        return redirect(url_for("seller"))

    return render_template("seller.html", cart_count=cart_count())


@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id")
    qty = int(request.form.get("qty", 1))
    try:
        p = products_col.find_one({"_id": ObjectId(product_id)})
    except Exception:
        return redirect(url_for("index"))
    if not p:
        return redirect(url_for("index"))

    cart = get_cart()
    if product_id in cart:
        cart[product_id]["qty"] += qty
    else:
        cart[product_id] = {
            "name": p["name"],
            "price": p["price"],
            "qty": qty,
        }
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/cart/update", methods=["POST"])
def update_cart():
    product_id = request.form.get("product_id")
    action = request.form.get("action")
    cart = get_cart()
    if product_id in cart:
        if action == "increase":
            cart[product_id]["qty"] += 1
        elif action == "decrease":
            cart[product_id]["qty"] -= 1
            if cart[product_id]["qty"] <= 0:
                del cart[product_id]
        elif action == "remove":
            del cart[product_id]
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    cart_items = get_cart()
    total = cart_total()
    return render_template("cart.html", cart=cart_items, total=total, cart_count=cart_count())


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "GET":
        if not get_cart():
            return redirect(url_for("index"))
        return render_template("checkout.html", cart=get_cart(),
                               total=cart_total(), cart_count=cart_count())

    # POST — place order
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    address = request.form.get("address", "").strip()

    if not name or not email or not address:
        return render_template("checkout.html", cart=get_cart(), total=cart_total(),
                               cart_count=cart_count(), error="Please fill in all fields.")

    order = {
        "customer": {"name": name, "email": email, "address": address},
        "items": list(get_cart().values()),
        "total": cart_total(),
        "placed_at": datetime.utcnow(),
        "status": "confirmed",
    }
    result = orders_col.insert_one(order)
    order_id = str(result.inserted_id)
    session.pop("cart", None)
    return redirect(url_for("order_confirmation", order_id=order_id))


@app.route("/order/<order_id>")
def order_confirmation(order_id):
    try:
        order = orders_col.find_one({"_id": ObjectId(order_id)})
    except Exception:
        return redirect(url_for("index"))
    if not order:
        return redirect(url_for("index"))
    order["_id"] = str(order["_id"])
    return render_template("confirmation.html", order=order, cart_count=cart_count())


@app.route("/admin")
def admin():
    from datetime import timezone, timedelta
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    orders = list(orders_col.find().sort("placed_at", -1))
    for o in orders:
        o["_id"] = str(o["_id"])
        # make placed_at timezone-aware if it isn't
        if o.get("placed_at") and o["placed_at"].tzinfo is None:
            o["placed_at"] = o["placed_at"].replace(tzinfo=timezone.utc)

    products = list(products_col.find())
    for p in products:
        p["_id"] = str(p["_id"])

    total_revenue = sum(o.get("total", 0) for o in orders)
    today_orders = orders_col.count_documents({"placed_at": {"$gte": today_start}})

    stats = {
        "total_orders": len(orders),
        "total_revenue": total_revenue,
        "total_products": len(products),
        "today_orders": today_orders,
    }

    return render_template("admin.html", orders=orders, products=products,
                           stats=stats, cart_count=cart_count())


if __name__ == "__main__":
    app.run(debug=True)
