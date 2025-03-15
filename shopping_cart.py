import getpass

# Demo Marketplace Application

# Default data using Python basic Data Structures
users = {"user1": "password1", "user2": "password2"}  # User credentials
admins = {"admin1": "adminpass1"}  # Admin credentials
categories = {1: "Boots", 2: "Coats", 3: "Jackets", 4: "Caps"}  # Product categories
products = [
    {"id": 1, "name": "Leather Boots", "category_id": 1, "price": 120.00},
    {"id": 2, "name": "Winter Coat", "category_id": 2, "price": 150.00},
    {"id": 3, "name": "Denim Jacket", "category_id": 3, "price": 80.00},
    {"id": 4, "name": "Baseball Cap", "category_id": 4, "price": 20.00}
]
carts = {}  # User carts: {user_id: [{"product_id": x, "quantity": y}]}
sessions = {}  # Active sessions: {session_id: {"type": "user" or "admin", "username": "xyz"}}

# Helper Functions
def generate_session_id():
    return max(sessions.keys(), default=0) + 1

def display_catalog():
    print("\nProduct Catalog:")
    print("ID | Name            | Category     | Price")
    print("-" * 40)
    for product in products:
        print(f"{product['id']:2} | {product['name']:15} | {categories[product['category_id']]:12} | ₹{product['price']:.2f}")

def display_cart(user_id):
    if user_id in carts:
        print("\nYour Cart:")
        print("ID | Name            | Quantity | Price")
        print("-" * 40)
        total = 0
        for item in carts[user_id]:
            product = next(p for p in products if p["id"] == item["product_id"])
            print(f"{product['id']:2} | {product['name']:15} | {item['quantity']:8} | ₹{product['price'] * item['quantity']:.2f}")
            total += product['price'] * item['quantity']
        print(f"Total: ₹{total:.2f}")
    else:
        print("Your cart is empty.")

def add_to_cart(user_id, product_id, quantity):
    if user_id not in carts:
        carts[user_id] = []
    carts[user_id].append({"product_id": product_id, "quantity": quantity})
    print("Item added to cart.")

def remove_from_cart(user_id, product_id):
    if user_id in carts:
        carts[user_id] = [item for item in carts[user_id] if item["product_id"] != product_id]
        print("Item removed from cart.")
    else:
        print("Your cart is empty.")

def checkout(user_id):
    if user_id in carts and carts[user_id]:
        print("\nSelect Payment Option:")
        print("1. Net Banking")
        print("2. PayPal")
        print("3. UPI")
        choice = input("Enter your choice: ")
        if choice in ["1", "2", "3"]:
            total = sum(product["price"] * item["quantity"] for item in carts[user_id] for product in products if product["id"] == item["product_id"])
            print(f"You will be shortly redirected to the portal for Unified Payment Interface to make a payment of Rs. {total:.2f}")
            print("Your order is successfully placed.")
            carts[user_id] = []  # Clear the cart
        else:
            print("Invalid payment option.")
    else:
        print("Your cart is empty.")

# User Functions
def user_login():
    username = input("Enter username: ")
    password = getpass.getpass(prompt='Enter password: ', stream=None)
    #password = input("Enter password: ")
    if username in users and users[username] == password:
        session_id = generate_session_id()
        sessions[session_id] = {"type": "user", "username": username}
        print("User login successful!")
        return session_id
    else:
        print("Invalid credentials!")
        return None

def user_menu(session_id):
    user_id = session_id
    while True:
        print("\nUser Menu:")
        print("1. View Catalog")
        print("2. View Cart")
        print("3. Add Item to Cart")
        print("4. Remove Item from Cart")
        print("5. Checkout")
        print("6. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            display_catalog()
        elif choice == "2":
            display_cart(user_id)
        elif choice == "3":
            product_id = int(input("Enter product ID: "))
            quantity = int(input("Enter quantity: "))
            add_to_cart(user_id, product_id, quantity)
        elif choice == "4":
            product_id = int(input("Enter product ID: "))
            remove_from_cart(user_id, product_id)
        elif choice == "5":
            checkout(user_id)
        elif choice == "6":
            print("Logged out.")
            break
        else:
            print("Invalid choice!")

# Admin Functions
def admin_login():
    username = input("Enter admin username: ")
    password = getpass.getpass(prompt='Enter admin password: ', stream=None)
    #password = input("Enter admin password: ")
    if username in admins and admins[username] == password:
        session_id = generate_session_id()
        sessions[session_id] = {"type": "admin", "username": username}
        print("Admin login successful!")
        return session_id
    else:
        print("Invalid credentials!")
        return None

def admin_menu(session_id):
    while True:
        print("\n\033[31mAdmin Menu:\033[31m")
        print("\033[31m1. View Catalog\033[31m")
        print("\033[31m2. Add Product\033[31m")
        print("\033[31m3. Modify Product\033[31m")
        print("\033[31m4. Delete Product\033[31m")
        print("\033[31m5. Add Category\033[31m")
        print("\033[31m6. Delete Category\033[31m")
        print("\033[31m7. Logout\033[31m")
        choice = input("\033[31mEnter your choice: \033[31m")
        if choice == "1":
            display_catalog()
        elif choice == "2":
            name = input("\033[31mEnter product name: \033[31m")
            category_id = int(input("\033[31mEnter category ID: \033[31m"))
            price = float(input("\033[31mEnter price: \033[31m"))
            new_id = max(p["id"] for p in products) + 1
            if (category_id in categories):
                products.append({"id": new_id, "name": name, "category_id": category_id, "price": price})
                print("\033[31mProduct added successfully!\033[31m")
            else:
                print("\033[31mCategory ID chosen doesn't exists, please choose an already exists Category ID.\033[31m")
        elif choice == "3":
            product_id = int(input("\033[31mEnter product ID to modify: \033[31m"))
            product = next((p for p in products if p["id"] == product_id), None)
            if product:
                product["name"] = input("\033[31mEnter new name: \033[31m")
                product["category_id"] = int(input("\033[31mEnter new category ID: \033[31m"))
                product["price"] = float(input("\033[31mEnter new price: \033[31m"))
                print("\033[31mProduct modified successfully!\033[31m")
            else:
                print("\033[31mProduct not found.\033[31m")
        elif choice == "4":
            product_id = int(input("\033[31mEnter product ID to delete: \033[31m"))
            products[:] = [p for p in products if p["id"] != product_id]
            print("\033[31mProduct deleted successfully!\033[31m")
        elif choice == "5":
            category_name = input("\033[31mEnter new category name: \033[31m")
            new_id = max(categories.keys(), default=0) + 1
            categories[new_id] = category_name
            print("\033[31mCategory added successfully!\033[31m")
        elif choice == "6":
            category_id = int(input("\033[31mEnter category ID to delete: \033[31m"))
            if category_id in categories:
                del categories[category_id]
                products[:] = [p for p in products if p["category_id"] != category_id]
                print("\033[31mCategory deleted successfully!\033[31m")
            else:
                print("\033[31mCategory not found.\033[31m")
        elif choice == "7":
            print("\033[31mLogged out.\033[31m")
            break
        else:
            print("\033[31mInvalid choice!\033[31m")

# Main Application
def main():
    print("Welcome to the Demo Marketplace")
    while True:
        print("\nMain Menu:")
        print("1. User Login")
        print("2. Admin Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            session_id = user_login()
            if session_id:
                user_menu(session_id)
        elif choice == "2":
            session_id = admin_login()
            if session_id:
                admin_menu(session_id)
        elif choice == "3":
            print("Thank you for using the Demo Marketplace application.")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()