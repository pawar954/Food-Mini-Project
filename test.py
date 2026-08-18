# test_code.py
# import sqlite3
# from create_customer import add_customer


# def test_add_customers():

#     customers = [
#         ("Neha", "9876543211", "neha@gmail.com"),
#         ("Ravi", "9876543212", "ravi@gmail.com"),
#         ("Sneha", "9876543213", "sneha@gmail.com"),
#         ("Priya", "9876543214", "priya@gmail.com")
#     ]

#     for customer in customers:

#         customer_id = add_customer(
#             customer[0],
#             customer[1],
#             customer[2]
#         )

#         print(
#             f"Customer created: "
#             f"ID={customer_id}, "
#             f"Name={customer[0]}"
#         )

# if __name__ == "__main__":
#     test_add_customers()

#=====================================================================================
# from database import get_connection

# def view_customers():

#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute("SELECT * FROM customers")

#     customers = cursor.fetchall()

#     for customer in customers:
#         print(customer)

#     connection.close()


# if __name__ == "__main__":
#     view_customers()

#========================================================================
# for products
# import sqlite3
# from create_product import add_product


# def test_add_products():

#     products = [
#         ("Margherita Pizza",299 ),
#         ("Veg Burger",149),
#         ("French Fries",99),
#         ("Paneer Tikka",249 ),
#         ("Masala Dosa",129),
#         ("White Sauce Pasta", 229),
#         ("Chocolate Brownie",129 ),
#         ("Cold Coffee",119 ),
#         ("Pav Bhaji",149 ),
#         ("Cheese Garlic Bread",159 )
#     ]

#     for product in products:

#         product_id = add_product(
#             product[0],
#             product[1]
#         )

#         print(
#             f"Products created: "
#             f"ID={product_id}, "
#             f"Name={product[0]}"
#         )

# if __name__ == "__main__":
#     test_add_products()


#===========================================================================================
# test inventory
# from create_inventory import add_inventory


# def test_add_inventory():

#     inventorys = [
#         (1,20),
#         (2,49),
#         (3,9),
#         (4,24),
#         (5,29),
#         (6,22),
#         (7,12),
#         (8,19),
#         (9,149),
#         (10,59)
#     ]

#     for inventory in inventorys:

#         inventory_id = add_inventory(
#             inventory[0],
#             inventory[1]
#         )

#         print(
#             f"Inventory created: "
#             f"Product ID={inventory_id}, "
#             f"Quantity={inventory[1]}"
#         )

# if __name__ == "__main__":
#     test_add_inventory()
#============================================================================================
#test orders
# from create_order import add_order


# def test_add_order():

#     orders = [
#         (1, "2026-08-16", "Pending", 548),
#         (2, "2026-08-16", "Confirmed", 399),
#         (3, "2026-08-16", "Preparing", 699),
#         (4, "2026-08-16", "Delivered", 249),
#         (5, "2026-08-16", "Pending", 459),
#         (6, "2026-08-16", "Confirmed", 799),
#         (7, "2026-08-16", "Preparing", 329),
#         (8, "2026-08-16", "Delivered", 599),
#         (9, "2026-08-16", "Pending", 449),
#         (10, "2026-08-16", "Confirmed", 899)
#     ]

#     for order in orders:

#         order_id = add_order(
#             order[0],
#             order[1],
#             order[2],
#             order[3]
#         )

#         print(
#             f"Order created: "
#             f"Order ID={order_id}, "
#             f"Customer ID={order[0]}, "
#             f"Status={order[2]}, "
#             f"Total={order[3]}"
#         )

# if __name__ == "__main__":
#     test_add_order()
#================================================================================================
#test order items

# from create_order_item import add_order_items


# def test_add_order_items():

#     order_items = [
#         (1, 1, 2, 299),
#         (1, 3, 1, 99),
#         (2, 2, 2, 149),
#         (2, 5, 1, 129),
#         (3, 4, 2, 249),
#         (3, 6, 1, 229),
#         (4, 7, 3, 129),
#         (5, 8, 2, 119),
#         (6, 9, 1, 149),
#         (7, 10, 2, 159)
#     ]

#     for item in order_items:

#         order_item_id = add_order_items(
#             item[0],
#             item[1],
#             item[2],
#             item[3]
#         )

#         print(
#             f"Order item created: "
#             f"ID={order_item_id}, "
#             f"Order ID={item[0]}, "
#             f"Product ID={item[1]}, "
#             f"Quantity={item[2]}, "
#             f"Unit Price={item[3]}"
#         )


# if __name__ == "__main__":
#     test_add_order_items()
    
    
#=================================================================================================
# #test  payments

# from create_payments import add_payment


# def test_add_payments():

#     payments = [
#         (1, "2026-08-16", 548, "Paid"),
#         (2, "2026-08-16", 399, "Paid"),
#         (3, "2026-08-16", 699, "Pending"),
#         (4, "2026-08-16", 249, "Paid"),
#         (5, "2026-08-16", 459, "Pending"),
#         (6, "2026-08-16", 799, "Paid"),
#         (7, "2026-08-16", 329, "Failed"),
#         (8, "2026-08-16", 599, "Paid"),
#         (9, "2026-08-16", 449, "Pending"),
#         (10, "2026-08-16", 899, "Paid")
#     ]

#     for payment in payments:

#         payment_id = add_payment(
#             payment[0],
#             payment[1],
#             payment[2],
#             payment[3]
#         )

#         print(
#             f"Payment created: "
#             f"Payment ID={payment_id}, "
#             f"Order ID={payment[0]}, "
#             f"Amount={payment[2]}, "
#             f"Status={payment[3]}"
#         )


# if __name__ == "__main__":
#     test_add_payments()


# ===============================================================================
