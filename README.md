# 🇸🇪 Scandinavian Delight – Full Stack Food Ordering Platform

A production-style Django web application that allows users to **build custom snacks from ingredients**, purchase ready-made snacks, and manage orders through a clean and scalable architecture.

Designed with **real-world e-commerce patterns**, focusing on usability, modularity, and extensibility.

---

## 🌟 Project Highlights

* 🧠 **Custom Snack Builder** (unique feature)
* 🛒 Unified cart system (ingredients + snacks + custom products)
* 💰 Dynamic pricing engine (grams-based + quantity-based + discounts)
* 📦 Order lifecycle management (Active → Delivered)
* 🔐 Authentication & user-specific cart
* ⚙️ Admin dashboard with inline order management
* 🧩 Scalable architecture ready for APIs / microservices

---

## 🚀 Features

### 🥗 Ingredients (Weight-Based System)

* Add ingredients with custom grams (e.g., 120g, 250g)
* Real-time price calculation using `price_per_100g`
* Flexible and extensible pricing model

---

### 🍫 Snacks (Quantity-Based System)

* Add snacks by quantity (e.g., 1, 5, 10 pcs)
* Built-in discount logic:

  * 5 pcs → 5% discount
  * 10 pcs → 25% discount
* Easily extendable discount tiers

---

### 🧠 Custom Snack Builder

> A standout feature for recruiters

Users can:

* Create multiple custom snacks (`MySnack_1`, `MySnack_2`, etc.)
* Add multiple ingredients with different gram values
* Save and reuse snack configurations
* Add custom snacks to cart as a **single product**

---

### 🛒 Smart Cart System

* Supports:

  * Ingredients
  * Snacks
  * Custom Snacks
* Unified pricing logic via `get_total_price()`
* Remove items dynamically
* Clean separation of item types using nullable relations

---

### 💳 Checkout & Orders

* Group all cart items into a single order
* Unique reference code generation
* Optional subscription:

  * Weekly
  * Monthly
* Order status tracking:

  * Active
  * Delivered

---

### 🔐 Authentication

* User registration & login
* User-specific cart and orders
* Secure session handling

---

### 🛠️ Admin Panel

* Manage:

  * Ingredients
  * Snacks
  * Orders
* Inline cart item visualization inside orders
* Revenue overview via total aggregation

---

## 🧱 Architecture Overview

```
User
 ├── CartItems
 │     ├── Ingredient (grams-based)
 │     ├── Snack (quantity-based)
 │     └── CustomSnack (grouped ingredients)
 │
 ├── Order
 │     └── CartItems (related_name)
 │
 └── CustomSnack
       └── CustomSnackItems (ingredient + grams)
```

---

## 📁 Project Structure

```
E-Food/
│
├── accounts/                # Authentication (login/signup)
│   ├── templates/accounts/
│   ├── views.py
│   └── forms.py
│
├── main/                    # Core business logic
│   ├── models.py            # Ingredient, Snack, CartItems, Order
│   ├── views.py             # Cart, checkout, snack builder
│   ├── templates/main/
│   └── urls.py
│
├── media/                   # Uploaded images
├── e_food/                  # Project settings
│   ├── settings.py
│   └── urls.py
│
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---

## ⚙️ Installation Guide

### 1. Clone the repository

```bash
git clone https://github.com/your-username/scandinavian-delight.git
cd scandinavian-delight
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create superuser

```bash
python manage.py createsuperuser
```

### 6. Run server

```bash
python manage.py runserver
```

---

## 🔗 Available Routes

| Feature     | URL                   |
| ----------- | --------------------- |
| Home        | `/`                   |
| Ingredients | `/ingredient/<slug>/` |
| Snacks      | `/snacks/`            |
| Cart        | `/cart/`              |
| Checkout    | `/checkout/`          |
| Orders      | `/order_details/`     |
| Admin       | `/admin/`             |

---

## 💡 Key Design Decisions

### ✔ Unified Cart Model

Instead of separate carts, a single `CartItems` model handles:

* Ingredients
* Snacks
* Custom Snacks
  → Reduces duplication and simplifies checkout logic.

---

### ✔ Dynamic Pricing Strategy

Encapsulated in model methods:

```python
def get_total_price(self):
```

→ Keeps business logic out of views.

---

### ✔ Extensible Discount System

Easily expandable:

```python
if quantity >= 10:
    discount = 0.25
elif quantity >= 5:
    discount = 0.05
```

---

### ✔ Custom Snack Abstraction

Avoids hacky grouping by introducing:

* `CustomSnack`
* `CustomSnackItem`

→ Clean, scalable, and recruiter-friendly design.

---

## 📈 Future Improvements

* REST API (Django REST Framework)
* React / Next.js frontend
* Payment integration (Stripe)
* Docker deployment
* PostgreSQL migration
* Redis caching
* Recommendation system (AI-based)

---

## 🧑‍💻 Author

**Your Name**
Full Stack Developer
📍 Sweden

* GitHub: [https://github.com/your-username](https://github.com/Khosiyat/)
* LinkedIn: [https://linkedin.com/in/your-profile](https://www.linkedin.com/in/khosiyat-sabir-ova-01603377/)

---

## 🏁 Why This Project Stands Out

This is not just CRUD.

It demonstrates:

* Real-world e-commerce logic
* Scalable Django architecture
* Clean separation of concerns
* Advanced modeling (custom product builder)

👉 Built to reflect **industry-level thinking**, not just coursework.
