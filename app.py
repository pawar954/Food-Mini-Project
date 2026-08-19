import sqlite3
import gradio as gr

from database import get_connection
from create_tables import create_tables

from login import check_customer_login

from admin_auth import (
    validate_admin,
    create_admin,
    show_admins
)

from admin_activity import (
    log_activity,
    show_activity
)

from create_product import (
    add_product,
    update_product,
    show_products,
    delete_product,
    search_product
)

from create_inventory import (
    add_inventory,
    update_inventory,
    show_inventory,
    delete_inventory,
    search_inventory
)


# ============================================================
# INITIAL DATABASE SETUP
# ============================================================

create_tables()


# ============================================================
# PRODUCT HELPERS
# ============================================================

def get_product_names():

    products = show_products()

    return [
        product[1]
        for product in products
    ]


def get_product_details(product_name):

    if not product_name:
        return None, "", None

    products = show_products()

    for product in products:

        product_id = product[0]
        name = product[1]
        price = product[2]

        if name == product_name:

            return product_id, name, price

    return None, "", None


# ============================================================
# INVENTORY HELPERS
# ============================================================

def get_inventory_product_names():

    inventory = show_inventory()

    return [
        item[1]
        for item in inventory
    ]


def get_products_not_in_inventory():

    products = show_products()
    inventory = show_inventory()

    inventory_product_ids = {
        item[0]
        for item in inventory
    }

    return [
        product[1]
        for product in products
        if product[0] not in inventory_product_ids
    ]


def get_inventory_product_details(product_name):

    if not product_name:
        return None, ""

    inventory = show_inventory()

    for item in inventory:

        product_id = item[0]
        name = item[1]

        if name == product_name:

            return product_id, name

    return None, ""


def get_inventory_quantity(product_name):

    if not product_name:
        return None

    inventory = show_inventory()

    for item in inventory:

        if item[1] == product_name:
            return item[2]

    return None


# ============================================================
# DROPDOWN REFRESH
# ============================================================

def refresh_product_dropdowns():

    choices = get_product_names()

    return (
        gr.update(choices=choices, value=None),
        gr.update(choices=choices, value=None)
    )


def refresh_inventory_dropdowns():

    add_choices = get_products_not_in_inventory()
    inventory_choices = get_inventory_product_names()

    return (
        gr.update(choices=add_choices, value=None),
        gr.update(choices=inventory_choices, value=None),
        gr.update(choices=inventory_choices, value=None)
    )


# ============================================================
# PRODUCT - ADD
# ============================================================

def add_product_admin(admin_id, product_name, price):

    if not product_name or not product_name.strip():

        return (
            "❌ Product name is required.",
            show_products()
        )

    if price is None:

        return (
            "❌ Price is required.",
            show_products()
        )

    if price < 0:

        return (
            "❌ Price cannot be negative.",
            show_products()
        )

    product_name = product_name.strip()

    product_id = add_product(
        product_name,
        float(price)
    )

    if product_id is None:

        return (
            "❌ Product already exists or could not be added.",
            show_products()
        )

    if admin_id is not None:

        log_activity(
            admin_id,
            "ADD_PRODUCT",
            f"Added product '{product_name}' with price {price}"
        )

    return (
        f"✅ Product '{product_name}' added successfully. "
        f"Product ID: {product_id}",
        show_products()
    )


# ============================================================
# PRODUCT - UPDATE
# ============================================================

def update_product_admin(
    admin_id,
    selected_product,
    new_product_name,
    new_price
):

    if not selected_product:

        return (
            "❌ Please select a product.",
            show_products()
        )

    if not new_product_name or not new_product_name.strip():

        return (
            "❌ Product name is required.",
            show_products()
        )

    if new_price is None:

        return (
            "❌ Price is required.",
            show_products()
        )

    if new_price < 0:

        return (
            "❌ Price cannot be negative.",
            show_products()
        )

    product_id, old_name, old_price = get_product_details(
        selected_product
    )

    if product_id is None:

        return (
            "❌ Product not found.",
            show_products()
        )

    new_product_name = new_product_name.strip()

    result = update_product(
        product_id,
        new_product_name,
        float(new_price)
    )

    if result:

        if admin_id is not None:

            log_activity(
                admin_id,
                "UPDATE_PRODUCT",
                f"Updated product '{old_name}' to "
                f"'{new_product_name}', price {old_price} to {new_price}"
            )

        return (
            f"✅ Product '{old_name}' updated successfully. "
            f"Product ID: {product_id}",
            show_products()
        )

    return (
        "❌ Product update failed. Product name may already exist.",
        show_products()
    )


# ============================================================
# PRODUCT - DELETE
# ============================================================

def delete_product_admin(admin_id, selected_product):

    if not selected_product:

        return (
            "❌ Please select a product.",
            show_products()
        )

    product_id, product_name, price = get_product_details(
        selected_product
    )

    if product_id is None:

        return (
            "❌ Product not found.",
            show_products()
        )

    result = delete_product(product_id)

    if result:

        if admin_id is not None:

            log_activity(
                admin_id,
                "DELETE_PRODUCT",
                f"Deleted product '{product_name}' "
                f"(Product ID: {product_id})"
            )

        return (
            f"✅ Product '{product_name}' deleted successfully.",
            show_products()
        )

    return (
        "❌ Product could not be deleted.",
        show_products()
    )


# ============================================================
# PRODUCT SEARCH
# ============================================================

def search_product_admin(search_type, search_value):

    if search_type == "All Products":

        return show_products()

    if not search_value or not str(search_value).strip():

        return []

    try:

        if search_type == "Product ID":

            return search_product(
                product_id=int(float(search_value))
            )

        if search_type == "Product Name":

            return search_product(
                product_name=str(search_value).strip()
            )

    except (ValueError, TypeError):

        return []

    return []


# ============================================================
# INVENTORY - ADD
# ============================================================

def add_inventory_admin(
    admin_id,
    selected_product,
    quantity
):

    if not selected_product:

        return (
            "❌ Please select a product.",
            show_inventory()
        )

    if quantity is None:

        return (
            "❌ Quantity is required.",
            show_inventory()
        )

    if quantity < 0:

        return (
            "❌ Quantity cannot be negative.",
            show_inventory()
        )

    product_id, product_name, price = get_product_details(
        selected_product
    )

    if product_id is None:

        return (
            "❌ Product not found.",
            show_inventory()
        )

    result = add_inventory(
        product_id,
        int(quantity)
    )

    if result:

        if admin_id is not None:

            log_activity(
                admin_id,
                "ADD_INVENTORY",
                f"Added inventory for '{product_name}', "
                f"quantity {int(quantity)}"
            )

        return (
            f"✅ Inventory added for '{product_name}'. "
            f"Product ID: {product_id}",
            show_inventory()
        )

    return (
        "❌ Inventory could not be added. "
        "Product may already have inventory.",
        show_inventory()
    )


# ============================================================
# INVENTORY - UPDATE
# ============================================================

def update_inventory_admin(
    admin_id,
    selected_product,
    quantity
):

    if not selected_product:

        return (
            "❌ Please select an inventory product.",
            show_inventory()
        )

    if quantity is None:

        return (
            "❌ Quantity is required.",
            show_inventory()
        )

    if quantity < 0:

        return (
            "❌ Quantity cannot be negative.",
            show_inventory()
        )

    product_id, product_name = get_inventory_product_details(
        selected_product
    )

    if product_id is None:

        return (
            "❌ Product is not currently in inventory.",
            show_inventory()
        )

    old_quantity = get_inventory_quantity(
        selected_product
    )

    result = update_inventory(
        product_id,
        int(quantity)
    )

    if result:

        if admin_id is not None:

            log_activity(
                admin_id,
                "UPDATE_INVENTORY",
                f"Updated inventory for '{product_name}' "
                f"from {old_quantity} to {int(quantity)}"
            )

        return (
            f"✅ Inventory for '{product_name}' updated successfully.",
            show_inventory()
        )

    return (
        "❌ Inventory update failed.",
        show_inventory()
    )


# ============================================================
# INVENTORY - DELETE
# ============================================================

def delete_inventory_admin(
    admin_id,
    selected_product
):

    if not selected_product:

        return (
            "❌ Please select an inventory product.",
            show_inventory()
        )

    product_id, product_name = get_inventory_product_details(
        selected_product
    )

    if product_id is None:

        return (
            "❌ Product is not currently in inventory.",
            show_inventory()
        )

    result = delete_inventory(product_id)

    if result:

        if admin_id is not None:

            log_activity(
                admin_id,
                "DELETE_INVENTORY",
                f"Deleted inventory for '{product_name}' "
                f"(Product ID: {product_id})"
            )

        return (
            f"✅ Inventory for '{product_name}' deleted successfully.",
            show_inventory()
        )

    return (
        "❌ Inventory could not be deleted.",
        show_inventory()
    )


# ============================================================
# INVENTORY SEARCH
# ============================================================

def search_inventory_admin(search_type, search_value):

    if search_type == "All Inventory":

        return show_inventory()

    if not search_value or not str(search_value).strip():

        return []

    try:

        if search_type == "Product ID":

            return search_inventory(
                product_id=int(float(search_value))
            )

        if search_type == "Product Name":

            return search_inventory(
                product_name=str(search_value).strip()
            )

    except (ValueError, TypeError):

        return []

    return []


# ============================================================
# ORDERS
# ============================================================

def show_orders():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                o.order_id,
                c.name,
                o.created_at,
                o.status,
                o.total_amount
            FROM orders o
            JOIN customers c
                ON o.customer_id = c.customer_id
            ORDER BY o.order_id DESC
        """)

        return cursor.fetchall()

    except sqlite3.Error:

        return []

    finally:

        connection.close()


def view_orders_admin(admin_id):

    orders = show_orders()

    if admin_id is not None:

        log_activity(
            admin_id,
            "VIEW_ORDERS",
            "Admin viewed customer orders"
        )

    return orders


# ============================================================
# ADMIN ACTIVITY
# ============================================================

def get_admin_activity():

    try:

        return show_activity()

    except sqlite3.Error:

        return []


# ============================================================
# ADMIN MANAGEMENT - ADD
# ============================================================

def add_admin_admin(
    current_admin_id,
    full_name,
    username,
    password
):

    if not full_name or not full_name.strip():

        return (
            "❌ Full name is required.",
            show_admins()
        )

    if not username or not username.strip():

        return (
            "❌ Username is required.",
            show_admins()
        )

    if not password:

        return (
            "❌ Password is required.",
            show_admins()
        )

    full_name = full_name.strip()
    username = username.strip()

    admin_id = create_admin(
        username,
        password,
        full_name
    )

    if admin_id is None:

        return (
            "❌ Username already exists or admin could not be created.",
            show_admins()
        )

    if current_admin_id is not None:

        log_activity(
            current_admin_id,
            "ADD_ADMIN",
            f"Added admin '{username}' ({full_name})"
        )

    return (
        f"✅ Admin '{full_name}' added successfully. "
        f"Admin ID: {admin_id}",
        show_admins()
    )


# ============================================================
# ADMIN LOGIN
# ============================================================

def process_admin_login(
    username,
    password
):

    if not username or not username.strip():

        return (
            "❌ Username is required.",
            gr.update(visible=True),
            gr.update(visible=False),
            None,
            ""
        )

    if not password:

        return (
            "❌ Password is required.",
            gr.update(visible=True),
            gr.update(visible=False),
            None,
            ""
        )

    username = username.strip()

    admin = validate_admin(
        username,
        password
    )

    if admin is None:

        return (
            "❌ Invalid username or password.",
            gr.update(visible=True),
            gr.update(visible=False),
            None,
            ""
        )

    admin_id = admin[0]
    full_name = admin[2]

    log_activity(
        admin_id,
        "LOGIN",
        "Admin logged in"
    )

    return (
        f"✅ Welcome {full_name}",
        gr.update(visible=False),
        gr.update(visible=True),
        admin_id,
        full_name
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

def create_admin_dashboard(admin_id_state):

    with gr.Column(
        visible=False,
        elem_classes="admin-page"
    ) as admin_dashboard:

        # ====================================================
        # HEADER
        # ====================================================

        with gr.Row():

            with gr.Column(scale=8):

                gr.Markdown(
                    "# 🍴 Food Management System"
                )

                gr.Markdown(
                    "## Admin Dashboard"
                )

                admin_welcome = gr.Markdown(
                    "Welcome, Administrator 👋"
                )

            with gr.Column(
                scale=1,
                min_width=120
            ):

                logout_button = gr.Button(
                    "🚪 Logout",
                    variant="stop"
                )


        # ====================================================
        # DASHBOARD MENU
        # ====================================================

        with gr.Column(
            elem_classes="dashboard-menu"
        ) as dashboard_menu:

            gr.Markdown(
                "### Select what you want to manage"
            )

            product_menu_button = gr.Button(
                "📦 Manage Products",
                variant="primary",
                size="lg"
            )

            inventory_menu_button = gr.Button(
                "📊 Manage Inventory",
                variant="primary",
                size="lg"
            )

            orders_menu_button = gr.Button(
                "📋 View Orders",
                variant="secondary",
                size="lg"
            )

            admin_management_button = gr.Button(
                "👨‍💼 Admin Management",
                variant="secondary",
                size="lg"
            )

            activity_menu_button = gr.Button(
                "📝 Admin Activity Log",
                variant="secondary",
                size="lg"
            )


        # ====================================================
        # PRODUCT PAGE
        # ====================================================

        with gr.Column(visible=False) as product_page:

            with gr.Row():

                back_product_button = gr.Button(
                    "←",
                    variant="secondary",
                    scale=0,
                    min_width=50
                )

            gr.Markdown("# 📦 Manage Products")

            gr.Markdown(
                "Add, view, update and delete products."
            )

            gr.Markdown("## Select Product Operation")

            product_add_option = gr.Button(
                "➕ Add Product",
                variant="primary"
            )

            product_view_option = gr.Button(
                "📋 View Products",
                variant="secondary"
            )

            product_update_option = gr.Button(
                "✏️ Update Product",
                variant="secondary"
            )

            product_delete_option = gr.Button(
                "🗑️ Delete Product",
                variant="stop"
            )


            # ------------------------------------------------
            # ADD
            # ------------------------------------------------

            with gr.Column(visible=False) as product_add_section:

                gr.Markdown("## ➕ Add Product")

                with gr.Row():

                    product_name_input = gr.Textbox(
                        label="Product Name",
                        placeholder="Enter product name"
                    )

                    product_price_input = gr.Number(
                        label="Price",
                        minimum=0
                    )

                add_product_button = gr.Button(
                    "➕ Add Product",
                    variant="primary"
                )

                add_product_status = gr.Textbox(
                    label="Status",
                    interactive=False
                )


            # ------------------------------------------------
            # VIEW
            # ------------------------------------------------

            with gr.Column(visible=False) as product_view_section:

                gr.Markdown("## 📋 View Products")

                product_search_type = gr.Dropdown(
                    choices=[
                        "All Products",
                        "Product ID",
                        "Product Name"
                    ],
                    value="All Products",
                    label="Search By"
                )

                product_search_value = gr.Textbox(
                    label="Search Value",
                    placeholder="Enter Product ID or Product Name"
                )

                search_product_button = gr.Button(
                    "🔍 Search Product",
                    variant="primary"
                )

                product_table = gr.Dataframe(
                    headers=[
                        "Product ID",
                        "Product Name",
                        "Price"
                    ],
                    value=show_products(),
                    interactive=False
                )

                refresh_products_button = gr.Button(
                    "🔄 Show All Products",
                    variant="secondary"
                )


            # ------------------------------------------------
            # UPDATE
            # ------------------------------------------------

            with gr.Column(visible=False) as product_update_section:

                gr.Markdown("## ✏️ Update Product")

                update_product_select = gr.Dropdown(
                    choices=get_product_names(),
                    label="Select Product",
                    value=None
                )

                with gr.Row():

                    update_product_name = gr.Textbox(
                        label="New Product Name"
                    )

                    update_product_price = gr.Number(
                        label="New Price",
                        minimum=0
                    )

                update_product_button = gr.Button(
                    "✏️ Update Product",
                    variant="primary"
                )

                update_product_status = gr.Textbox(
                    label="Status",
                    interactive=False
                )


            # ------------------------------------------------
            # DELETE
            # ------------------------------------------------

            with gr.Column(visible=False) as product_delete_section:

                gr.Markdown("## 🗑️ Delete Product")

                delete_product_select = gr.Dropdown(
                    choices=get_product_names(),
                    label="Select Product",
                    value=None
                )

                delete_product_button = gr.Button(
                    "🗑️ Delete Product",
                    variant="stop"
                )

                delete_product_status = gr.Textbox(
                    label="Status",
                    interactive=False
                )


        # ====================================================
        # INVENTORY PAGE
        # ====================================================

        with gr.Column(visible=False) as inventory_page:

            with gr.Row():

                back_inventory_button = gr.Button(
                    "←",
                    variant="secondary",
                    scale=0,
                    min_width=50
                )

            gr.Markdown("# 📊 Manage Inventory")

            gr.Markdown(
                "Manage stock quantity for your products."
            )

            gr.Markdown("## Select Inventory Operation")

            inventory_add_option = gr.Button(
                "➕ Add Inventory",
                variant="primary"
            )

            inventory_view_option = gr.Button(
                "📋 View Inventory",
                variant="secondary"
            )

            inventory_update_option = gr.Button(
                "✏️ Update Inventory",
                variant="secondary"
            )

            inventory_delete_option = gr.Button(
                "🗑️ Delete Inventory",
                variant="stop"
            )


            # ------------------------------------------------
            # ADD
            # ------------------------------------------------

            with gr.Column(visible=False) as inventory_add_section:

                gr.Markdown("## ➕ Add Inventory")

                add_inventory_select = gr.Dropdown(
                    choices=get_products_not_in_inventory(),
                    label="Select Product",
                    value=None
                )

                add_inventory_quantity = gr.Number(
                    label="Quantity",
                    minimum=0
                )

                add_inventory_button = gr.Button(
                    "➕ Add Inventory",
                    variant="primary"
                )

                add_inventory_status = gr.Textbox(
                    label="Status",
                    interactive=False
                )


            # ------------------------------------------------
            # VIEW
            # ------------------------------------------------

            with gr.Column(visible=False) as inventory_view_section:

                gr.Markdown("## 📋 View Inventory")

                inventory_search_type = gr.Dropdown(
                    choices=[
                        "All Inventory",
                        "Product ID",
                        "Product Name"
                    ],
                    value="All Inventory",
                    label="Search By"
                )

                inventory_search_value = gr.Textbox(
                    label="Search Value",
                    placeholder="Enter Product ID or Product Name"
                )

                search_inventory_button = gr.Button(
                    "🔍 Search Inventory",
                    variant="primary"
                )

                inventory_table = gr.Dataframe(
                    headers=[
                        "Product ID",
                        "Product Name",
                        "Quantity"
                    ],
                    value=show_inventory(),
                    interactive=False
                )

                refresh_inventory_button = gr.Button(
                    "🔄 Show All Inventory",
                    variant="secondary"
                )


            # ------------------------------------------------
            # UPDATE
            # ------------------------------------------------

            with gr.Column(visible=False) as inventory_update_section:

                gr.Markdown("## ✏️ Update Inventory")

                update_inventory_select = gr.Dropdown(
                    choices=get_inventory_product_names(),
                    label="Select Inventory Product",
                    value=None
                )

                update_inventory_quantity = gr.Number(
                    label="New Quantity",
                    minimum=0
                )

                update_inventory_button = gr.Button(
                    "✏️ Update Inventory",
                    variant="primary"
                )

                update_inventory_status = gr.Textbox(
                    label="Status",
                    interactive=False
                )


            # ------------------------------------------------
            # DELETE
            # ------------------------------------------------

            with gr.Column(visible=False) as inventory_delete_section:

                gr.Markdown("## 🗑️ Delete Inventory")

                delete_inventory_select = gr.Dropdown(
                    choices=get_inventory_product_names(),
                    label="Select Inventory Product",
                    value=None
                )

                delete_inventory_button = gr.Button(
                    "🗑️ Delete Inventory",
                    variant="stop"
                )

                delete_inventory_status = gr.Textbox(
                    label="Status",
                    interactive=False
                )


        # ====================================================
        # ORDERS PAGE
        # ====================================================

        with gr.Column(visible=False) as orders_page:

            with gr.Row():

                back_orders_button = gr.Button(
                    "←",
                    variant="secondary",
                    scale=0,
                    min_width=50
                )

            gr.Markdown("# 📋 View Orders")

            gr.Markdown(
                "View all customer orders."
            )

            orders_table = gr.Dataframe(
                headers=[
                    "Order ID",
                    "Customer Name",
                    "Order Date",
                    "Status",
                    "Total Amount"
                ],
                value=show_orders(),
                interactive=False
            )

            refresh_orders_button = gr.Button(
                "🔄 Refresh Orders",
                variant="secondary"
            )


        # ====================================================
        # ADMIN MANAGEMENT PAGE
        # ====================================================

        with gr.Column(
            visible=False
        ) as admin_management_page:

            with gr.Row():

                back_admin_management_button = gr.Button(
                    "←",
                    variant="secondary",
                    scale=0,
                    min_width=50
                )

            gr.Markdown("# 👨‍💼 Admin Management")

            gr.Markdown(
                "Add new administrators and view existing administrators."
            )

            gr.Markdown("## Select Admin Operation")

            admin_add_option = gr.Button(
                "➕ Add Admin",
                variant="primary"
            )

            admin_view_option = gr.Button(
                "📋 View Admins",
                variant="secondary"
            )


            # ------------------------------------------------
            # ADD ADMIN
            # ------------------------------------------------

            with gr.Column(
                visible=False
            ) as admin_add_section:

                gr.Markdown("## ➕ Add Admin")

                admin_full_name_input = gr.Textbox(
                    label="Full Name",
                    placeholder="Enter full name"
                )

                admin_username_input = gr.Textbox(
                    label="Username",
                    placeholder="Enter username"
                )

                admin_password_input = gr.Textbox(
                    label="Password",
                    type="password",
                    placeholder="Enter password"
                )

                add_admin_button = gr.Button(
                    "➕ Add Admin",
                    variant="primary"
                )

                add_admin_status = gr.Textbox(
                    label="Status",
                    interactive=False
                )


            # ------------------------------------------------
            # VIEW ADMINS
            # ------------------------------------------------

            with gr.Column(
                visible=False
            ) as admin_view_section:

                gr.Markdown("## 📋 All Admins")

                admin_table = gr.Dataframe(
                    headers=[
                        "Admin ID",
                        "Username",
                        "Full Name",
                        "Status"
                    ],
                    value=show_admins(),
                    interactive=False
                )

                refresh_admins_button = gr.Button(
                    "🔄 Refresh Admins",
                    variant="secondary"
                )


        # ====================================================
        # ACTIVITY PAGE
        # ====================================================

        with gr.Column(
            visible=False
        ) as activity_page:

            with gr.Row():

                back_activity_button = gr.Button(
                    "←",
                    variant="secondary",
                    scale=0,
                    min_width=50
                )

            gr.Markdown("# 📝 Admin Activity Log")

            gr.Markdown(
                "Track admin login, logout and management activities."
            )

            activity_table = gr.Dataframe(
                headers=[
                    "Log ID",
                    "Username",
                    "Action",
                    "Details",
                    "Action Time"
                ],
                value=get_admin_activity(),
                interactive=False
            )

            refresh_activity_button = gr.Button(
                "🔄 Refresh Activity Log",
                variant="secondary"
            )


        # ====================================================
        # PRODUCT SECTION NAVIGATION
        # ====================================================

        def show_product_section(section):

            return (
                gr.update(visible=section == "add"),
                gr.update(visible=section == "view"),
                gr.update(visible=section == "update"),
                gr.update(visible=section == "delete")
            )


        product_add_option.click(
            lambda: show_product_section("add"),
            outputs=[
                product_add_section,
                product_view_section,
                product_update_section,
                product_delete_section
            ]
        )

        product_view_option.click(
            lambda: show_product_section("view"),
            outputs=[
                product_add_section,
                product_view_section,
                product_update_section,
                product_delete_section
            ]
        )

        product_update_option.click(
            lambda: show_product_section("update"),
            outputs=[
                product_add_section,
                product_view_section,
                product_update_section,
                product_delete_section
            ]
        )

        product_delete_option.click(
            lambda: show_product_section("delete"),
            outputs=[
                product_add_section,
                product_view_section,
                product_update_section,
                product_delete_section
            ]
        )


        # ====================================================
        # INVENTORY SECTION NAVIGATION
        # ====================================================

        def show_inventory_section(section):

            return (
                gr.update(visible=section == "add"),
                gr.update(visible=section == "view"),
                gr.update(visible=section == "update"),
                gr.update(visible=section == "delete")
            )


        inventory_add_option.click(
            lambda: show_inventory_section("add"),
            outputs=[
                inventory_add_section,
                inventory_view_section,
                inventory_update_section,
                inventory_delete_section
            ]
        )

        inventory_view_option.click(
            lambda: show_inventory_section("view"),
            outputs=[
                inventory_add_section,
                inventory_view_section,
                inventory_update_section,
                inventory_delete_section
            ]
        )

        inventory_update_option.click(
            lambda: show_inventory_section("update"),
            outputs=[
                inventory_add_section,
                inventory_view_section,
                inventory_update_section,
                inventory_delete_section
            ]
        )

        inventory_delete_option.click(
            lambda: show_inventory_section("delete"),
            outputs=[
                inventory_add_section,
                inventory_view_section,
                inventory_update_section,
                inventory_delete_section
            ]
        )


        # ====================================================
        # ADMIN SECTION NAVIGATION
        # ====================================================

        def show_admin_section(section):

            return (
                gr.update(visible=section == "add"),
                gr.update(visible=section == "view")
            )


        admin_add_option.click(
            lambda: show_admin_section("add"),
            outputs=[
                admin_add_section,
                admin_view_section
            ]
        )

        admin_view_option.click(
            lambda: show_admin_section("view"),
            outputs=[
                admin_add_section,
                admin_view_section
            ]
        )


        # ====================================================
        # PRODUCT SELECTION
        # ====================================================

        def select_update_product(product_name):

            product_id, name, price = get_product_details(
                product_name
            )

            if product_id is None:

                return "", None

            return name, price


        update_product_select.change(
            select_update_product,
            inputs=update_product_select,
            outputs=[
                update_product_name,
                update_product_price
            ]
        )


        # ====================================================
        # INVENTORY SELECTION
        # ====================================================

        def select_inventory_product(product_name):

            return get_inventory_quantity(product_name)


        update_inventory_select.change(
            select_inventory_product,
            inputs=update_inventory_select,
            outputs=update_inventory_quantity
        )


        # ====================================================
        # PAGE NAVIGATION
        # ====================================================

        def show_product_page():

            return (
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False)
            )


        def show_inventory_page():

            return (
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False)
            )


        def show_orders_page():

            return (
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False)
            )


        def show_admin_management_page():

            return (
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False)
            )


        def show_activity_page():

            return (
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True)
            )


        def back_to_dashboard():

            return (
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False)
            )


        # ====================================================
        # DASHBOARD BUTTONS
        # ====================================================

        page_outputs = [
            dashboard_menu,
            product_page,
            inventory_page,
            orders_page,
            admin_management_page,
            activity_page
        ]


        product_menu_button.click(
            show_product_page,
            outputs=page_outputs
        )

        inventory_menu_button.click(
            show_inventory_page,
            outputs=page_outputs
        )

        orders_menu_button.click(
            show_orders_page,
            outputs=page_outputs
        )

        admin_management_button.click(
            show_admin_management_page,
            outputs=page_outputs
        )

        activity_menu_button.click(
            show_activity_page,
            outputs=page_outputs
        )


        # ====================================================
        # BACK BUTTONS
        # ====================================================

        back_product_button.click(
            back_to_dashboard,
            outputs=page_outputs
        )

        back_inventory_button.click(
            back_to_dashboard,
            outputs=page_outputs
        )

        back_orders_button.click(
            back_to_dashboard,
            outputs=page_outputs
        )

        back_admin_management_button.click(
            back_to_dashboard,
            outputs=page_outputs
        )

        back_activity_button.click(
            back_to_dashboard,
            outputs=page_outputs
        )


        # ====================================================
        # ADD PRODUCT
        # ====================================================

        add_product_button.click(
            add_product_admin,
            inputs=[
                admin_id_state,
                product_name_input,
                product_price_input
            ],
            outputs=[
                add_product_status,
                product_table
            ]
        ).then(
            refresh_product_dropdowns,
            outputs=[
                update_product_select,
                delete_product_select
            ]
        ).then(
            refresh_inventory_dropdowns,
            outputs=[
                add_inventory_select,
                update_inventory_select,
                delete_inventory_select
            ]
        )


        # ====================================================
        # SEARCH PRODUCT
        # ====================================================

        search_product_button.click(
            search_product_admin,
            inputs=[
                product_search_type,
                product_search_value
            ],
            outputs=product_table
        )


        refresh_products_button.click(
            show_products,
            outputs=product_table
        )


        # ====================================================
        # UPDATE PRODUCT
        # ====================================================

        update_product_button.click(
            update_product_admin,
            inputs=[
                admin_id_state,
                update_product_select,
                update_product_name,
                update_product_price
            ],
            outputs=[
                update_product_status,
                product_table
            ]
        ).then(
            refresh_product_dropdowns,
            outputs=[
                update_product_select,
                delete_product_select
            ]
        ).then(
            refresh_inventory_dropdowns,
            outputs=[
                add_inventory_select,
                update_inventory_select,
                delete_inventory_select
            ]
        )


        # ====================================================
        # DELETE PRODUCT
        # ====================================================

        delete_product_button.click(
            delete_product_admin,
            inputs=[
                admin_id_state,
                delete_product_select
            ],
            outputs=[
                delete_product_status,
                product_table
            ]
        ).then(
            refresh_product_dropdowns,
            outputs=[
                update_product_select,
                delete_product_select
            ]
        ).then(
            refresh_inventory_dropdowns,
            outputs=[
                add_inventory_select,
                update_inventory_select,
                delete_inventory_select
            ]
        )


        # ====================================================
        # ADD INVENTORY
        # ====================================================

        add_inventory_button.click(
            add_inventory_admin,
            inputs=[
                admin_id_state,
                add_inventory_select,
                add_inventory_quantity
            ],
            outputs=[
                add_inventory_status,
                inventory_table
            ]
        ).then(
            refresh_inventory_dropdowns,
            outputs=[
                add_inventory_select,
                update_inventory_select,
                delete_inventory_select
            ]
        )


        # ====================================================
        # SEARCH INVENTORY
        # ====================================================

        search_inventory_button.click(
            search_inventory_admin,
            inputs=[
                inventory_search_type,
                inventory_search_value
            ],
            outputs=inventory_table
        )


        refresh_inventory_button.click(
            show_inventory,
            outputs=inventory_table
        )


        # ====================================================
        # UPDATE INVENTORY
        # ====================================================

        update_inventory_button.click(
            update_inventory_admin,
            inputs=[
                admin_id_state,
                update_inventory_select,
                update_inventory_quantity
            ],
            outputs=[
                update_inventory_status,
                inventory_table
            ]
        ).then(
            refresh_inventory_dropdowns,
            outputs=[
                add_inventory_select,
                update_inventory_select,
                delete_inventory_select
            ]
        )


        # ====================================================
        # DELETE INVENTORY
        # ====================================================

        delete_inventory_button.click(
            delete_inventory_admin,
            inputs=[
                admin_id_state,
                delete_inventory_select
            ],
            outputs=[
                delete_inventory_status,
                inventory_table
            ]
        ).then(
            refresh_inventory_dropdowns,
            outputs=[
                add_inventory_select,
                update_inventory_select,
                delete_inventory_select
            ]
        )


        # ====================================================
        # ADD ADMIN
        # ====================================================

        add_admin_button.click(
            add_admin_admin,
            inputs=[
                admin_id_state,
                admin_full_name_input,
                admin_username_input,
                admin_password_input
            ],
            outputs=[
                add_admin_status,
                admin_table
            ]
        )


        # ====================================================
        # VIEW ADMINS
        # ====================================================

        admin_view_option.click(
            lambda: show_admins(),
            outputs=admin_table
        )

        refresh_admins_button.click(
            show_admins,
            outputs=admin_table
        )


        # ====================================================
        # ORDERS
        # ====================================================

        refresh_orders_button.click(
            view_orders_admin,
            inputs=admin_id_state,
            outputs=orders_table
        )


        # ====================================================
        # ACTIVITY
        # ====================================================

        refresh_activity_button.click(
            get_admin_activity,
            outputs=activity_table
        )


    return (
        admin_dashboard,
        logout_button,
        admin_welcome
    )


# ============================================================
# MAIN APPLICATION
# ============================================================

def create_app():

    css = """

    body {
        background-color: #0f172a !important;
    }

    .gradio-container {
        background-color: #0f172a !important;
        color: white !important;
    }

    .login-card,
    .dashboard-menu,
    .admin-page {
        max-width: 850px;
        margin-left: auto;
        margin-right: auto;
    }

    .login-card {
        margin-top: 60px;
        padding: 35px;
        border-radius: 18px;
        background-color: #172033 !important;
    }

    .dashboard-menu {
        padding: 30px;
        border-radius: 18px;
        background-color: #172033 !important;
    }

    h1,
    h2,
    h3,
    h4,
    p,
    label,
    span {
        color: white !important;
    }

    .gr-button-primary {
        background-color: #2563eb !important;
        border-color: #2563eb !important;
        color: white !important;
    }

    .gr-button-primary:hover {
        background-color: #1d4ed8 !important;
    }

    .gr-button-secondary {
        background-color: #475569 !important;
        border-color: #64748b !important;
        color: white !important;
    }

    .gr-button-secondary:hover {
        background-color: #64748b !important;
    }

    .gr-button-stop {
        background-color: #7f1d1d !important;
        border-color: #991b1b !important;
        color: white !important;
    }

    input,
    textarea,
    .gr-input,
    .gr-text-input,
    .gr-number-input {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    .input-container {
        background-color: #1e293b !important;
        border-color: #475569 !important;
    }

    .wrap {
        background-color: #1e293b !important;
        color: white !important;
        border-color: #475569 !important;
    }

    .wrap input {
        background-color: #1e293b !important;
        color: white !important;
    }

    .table-wrap,
    .dataframe {
        background-color: #1e293b !important;
        color: white !important;
    }

    textarea[disabled],
    input[disabled] {
        background-color: #1e293b !important;
        color: white !important;
        border-color: #475569 !important;
    }

    .admin-page {
        padding-bottom: 40px;
    }

    input[type="number"] {
        background-color: #1e293b !important;
        color: white !important;
    }

    """


    # ========================================================
    # GRADIO
    # ========================================================

    with gr.Blocks(
        title="Food Management System",
        css=css
    ) as app:

        admin_id_state = gr.State(None)
        admin_name_state = gr.State("")


        # ====================================================
        # LOGIN SELECTION
        # ====================================================

        with gr.Column(
            visible=True,
            elem_classes="login-card"
        ) as login_page:

            gr.Markdown("# 🍴 Food Management System")

            gr.Markdown("## Select Login Type")

            admin_login_open_button = gr.Button(
                "👨‍💼 Admin Login",
                variant="primary",
                size="lg"
            )

            customer_login_open_button = gr.Button(
                "👤 Customer Login",
                variant="secondary",
                size="lg"
            )


        # ====================================================
        # ADMIN LOGIN
        # ====================================================

        with gr.Column(
            visible=False,
            elem_classes="login-card"
        ) as admin_login_page:

            gr.Markdown("# 👨‍💼 Admin Login")

            admin_username = gr.Textbox(
                label="Username",
                placeholder="Enter username"
            )

            admin_password = gr.Textbox(
                label="Password",
                type="password",
                placeholder="Enter password"
            )

            admin_login_button = gr.Button(
                "🔐 Login",
                variant="primary",
                size="lg"
            )

            admin_login_status = gr.Textbox(
                label="Status",
                interactive=False
            )


        # ====================================================
        # CUSTOMER LOGIN
        # ====================================================

        with gr.Column(
            visible=False,
            elem_classes="login-card"
        ) as customer_login_page:

            gr.Markdown("# 👤 Customer Login")

            customer_username = gr.Textbox(
                label="Username",
                placeholder="Enter username"
            )

            customer_password = gr.Textbox(
                label="Password",
                type="password",
                placeholder="Enter password"
            )

            customer_login_button = gr.Button(
                "🔐 Login",
                variant="secondary",
                size="lg"
            )

            customer_login_status = gr.Textbox(
                label="Status",
                interactive=False
            )


        # ====================================================
        # ADMIN DASHBOARD
        # ====================================================

        (
            admin_dashboard_component,
            logout_button,
            admin_welcome
        ) = create_admin_dashboard(
            admin_id_state
        )


        # ====================================================
        # OPEN ADMIN LOGIN
        # ====================================================

        def open_admin_login():

            return (
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False)
            )


        admin_login_open_button.click(
            open_admin_login,
            outputs=[
                login_page,
                admin_login_page,
                customer_login_page
            ]
        )


        # ====================================================
        # OPEN CUSTOMER LOGIN
        # ====================================================

        def open_customer_login():

            return (
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True)
            )


        customer_login_open_button.click(
            open_customer_login,
            outputs=[
                login_page,
                admin_login_page,
                customer_login_page
            ]
        )


        # ====================================================
        # ADMIN LOGIN
        # ====================================================

        admin_login_button.click(
            process_admin_login,
            inputs=[
                admin_username,
                admin_password
            ],
            outputs=[
                admin_login_status,
                admin_login_page,
                admin_dashboard_component,
                admin_id_state,
                admin_name_state
            ]
        ).then(
            lambda name: f"Welcome, {name} 👋",
            inputs=admin_name_state,
            outputs=admin_welcome
        )


        # ====================================================
        # CUSTOMER LOGIN
        # ====================================================

        def process_customer_login(
            username,
            password
        ):

            success, message = check_customer_login(
                username,
                password
            )

            return message


        customer_login_button.click(
            process_customer_login,
            inputs=[
                customer_username,
                customer_password
            ],
            outputs=customer_login_status
        )


        # ====================================================
        # LOGOUT
        # ====================================================

        def logout_and_show_login(admin_id):

            if admin_id is not None:

                log_activity(
                    admin_id,
                    "LOGOUT",
                    "Admin logged out"
                )

            return (
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                None,
                "",
                "",
                "",
                "✅ Logged out successfully."
            )


        logout_button.click(
            logout_and_show_login,
            inputs=admin_id_state,
            outputs=[
                login_page,
                admin_login_page,
                admin_dashboard_component,
                admin_id_state,
                admin_name_state,
                admin_username,
                admin_password,
                admin_login_status
            ]
        )


    return app


# ============================================================
# RUN
# ============================================================

app = create_app()


if __name__ == "__main__":

    app.launch(
        theme=gr.themes.Base(
            primary_hue="blue",
            secondary_hue="slate",
            neutral_hue="slate"
        )
    )