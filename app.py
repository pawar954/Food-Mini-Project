import sqlite3
import gradio as gr

from database import get_connection

from login import (
    check_admin_login,
    check_customer_login
)

from create_product import (
    add_product,
    update_product,
    show_products,
    delete_product
)

from create_inventory import (
    add_inventory,
    update_inventory,
    show_inventory,
    delete_inventory
)


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

            return (
                product_id,
                name,
                price
            )

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

            return (
                product_id,
                name
            )

    return None, ""


# ============================================================
# INVENTORY QUANTITY
# ============================================================

def get_inventory_quantity(product_name):

    if not product_name:
        return None

    inventory = show_inventory()

    for item in inventory:

        product_id = item[0]
        name = item[1]
        quantity = item[2]

        if name == product_name:
            return quantity

    return None


# ============================================================
# REFRESH PRODUCT DROPDOWNS
# ============================================================

def refresh_product_dropdowns():

    product_names = get_product_names()

    return (
        gr.update(
            choices=product_names,
            value=None
        ),

        gr.update(
            choices=product_names,
            value=None
        )
    )


# ============================================================
# REFRESH INVENTORY DROPDOWNS
# ============================================================

def refresh_inventory_dropdowns():

    add_choices = get_products_not_in_inventory()

    inventory_choices = get_inventory_product_names()

    return (
        gr.update(
            choices=add_choices,
            value=None
        ),

        gr.update(
            choices=inventory_choices,
            value=None
        ),

        gr.update(
            choices=inventory_choices,
            value=None
        )
    )


# ============================================================
# PRODUCT FUNCTIONS
# ============================================================

def add_product_admin(product_name, price):

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
        price
    )

    if product_id is None:

        return (
            "❌ Product already exists or could not be added.",
            show_products()
        )

    return (
        f"✅ Product '{product_name}' added successfully. "
        f"Product ID: {product_id}",
        show_products()
    )


# ============================================================
# UPDATE PRODUCT
# ============================================================

def update_product_admin(
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

    result = update_product(
        product_id,
        new_product_name.strip(),
        new_price
    )

    if result:

        return (
            f"✅ Product '{old_name}' updated successfully. "
            f"Product ID: {product_id}",
            show_products()
        )

    return (
        "❌ Product update failed. "
        "Product name may already exist.",
        show_products()
    )


# ============================================================
# DELETE PRODUCT
# ============================================================

def delete_product_admin(selected_product):

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

        return (
            f"✅ Product '{product_name}' deleted successfully. "
            f"Product ID: {product_id}",
            show_products()
        )

    return (
        "❌ Product could not be deleted. "
        "It may be used by inventory or orders.",
        show_products()
    )


# ============================================================
# INVENTORY FUNCTIONS
# ============================================================

def add_inventory_admin(
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
# UPDATE INVENTORY
# ============================================================

def update_inventory_admin(
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
            "❌ Product is not currently present in inventory.",
            show_inventory()
        )

    result = update_inventory(
        product_id,
        int(quantity)
    )

    if result:

        return (
            f"✅ Inventory for '{product_name}' updated successfully. "
            f"Product ID: {product_id}",
            show_inventory()
        )

    return (
        "❌ Inventory update failed.",
        show_inventory()
    )


# ============================================================
# DELETE INVENTORY
# ============================================================

def delete_inventory_admin(selected_product):

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
            "❌ Product is not currently present in inventory.",
            show_inventory()
        )

    result = delete_inventory(product_id)

    if result:

        return (
            f"✅ Inventory for '{product_name}' deleted successfully. "
            f"Product ID: {product_id}",
            show_inventory()
        )

    return (
        "❌ Inventory could not be deleted.",
        show_inventory()
    )


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
                o.order_date,
                o.status,
                o.total_amount
            FROM orders o
            JOIN customers c
                ON o.customer_id = c.customer_id
            ORDER BY o.order_id DESC
        """)

        orders = cursor.fetchall()

        return orders

    except sqlite3.Error:

        return []

    finally:

        connection.close()


# ============================================================
# ADMIN DASHBOARD
# ============================================================

def create_admin_dashboard():

    with gr.Column(
        visible=False,
        elem_classes="admin-page"
    ) as admin_dashboard:

        # ====================================================
        # HEADER
        # ====================================================

        gr.Markdown("# 🍴 Food Management System")

        gr.Markdown("## Admin Dashboard")

        gr.Markdown(
            "Welcome, Administrator 👋"
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
                "📦  Manage Products",
                variant="primary",
                size="lg"
            )

            inventory_menu_button = gr.Button(
                "📊  Manage Inventory",
                variant="primary",
                size="lg"
            )

            orders_menu_button = gr.Button(
                "📋  View Orders",
                variant="secondary",
                size="lg"
            )


        # ====================================================
        # PRODUCT PAGE
        # ====================================================

        with gr.Column(
            visible=False
        ) as product_page:

            gr.Markdown("# 📦 Manage Products")

            gr.Markdown(
                "Add, view, update and delete products."
            )

            back_product_button = gr.Button(
                "← Back to Dashboard",
                variant="secondary"
            )


            # =================================================
            # ADD PRODUCT
            # =================================================

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


            # =================================================
            # PRODUCT LIST
            # =================================================

            gr.Markdown("## 📋 All Products")

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
                "🔄 Refresh Products",
                variant="secondary"
            )


            # =================================================
            # UPDATE PRODUCT
            # =================================================

            gr.Markdown("## ✏️ Update Product")

            update_product_select = gr.Dropdown(
                choices=get_product_names(),
                label="Select Product",
                value=None,
                interactive=True
            )

            with gr.Row():

                update_product_name = gr.Textbox(
                    label="New Product Name",
                    placeholder="Enter new product name"
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


            # =================================================
            # DELETE PRODUCT
            # =================================================

            gr.Markdown("## 🗑️ Delete Product")

            delete_product_select = gr.Dropdown(
                choices=get_product_names(),
                label="Select Product",
                value=None,
                interactive=True
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

        with gr.Column(
            visible=False
        ) as inventory_page:

            gr.Markdown("# 📊 Manage Inventory")

            gr.Markdown(
                "Manage stock quantity for your products."
            )

            back_inventory_button = gr.Button(
                "← Back to Dashboard",
                variant="secondary"
            )


            # =================================================
            # ADD INVENTORY
            # =================================================

            gr.Markdown("## ➕ Add Inventory")

            add_inventory_select = gr.Dropdown(
                choices=get_products_not_in_inventory(),
                label="Select Product",
                value=None,
                interactive=True
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


            # =================================================
            # CURRENT INVENTORY
            # =================================================

            gr.Markdown("## 📋 Current Inventory")

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
                "🔄 Refresh Inventory",
                variant="secondary"
            )


            # =================================================
            # UPDATE INVENTORY
            # =================================================

            gr.Markdown("## ✏️ Update Inventory")

            update_inventory_select = gr.Dropdown(
                choices=get_inventory_product_names(),
                label="Select Inventory Product",
                value=None,
                interactive=True
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


            # =================================================
            # DELETE INVENTORY
            # =================================================

            gr.Markdown("## 🗑️ Delete Inventory")

            delete_inventory_select = gr.Dropdown(
                choices=get_inventory_product_names(),
                label="Select Inventory Product",
                value=None,
                interactive=True
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

        with gr.Column(
            visible=False
        ) as orders_page:

            gr.Markdown("# 📋 View Orders")

            gr.Markdown(
                "View all customer orders."
            )

            back_orders_button = gr.Button(
                "← Back to Dashboard",
                variant="secondary"
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
            fn=select_update_product,
            inputs=update_product_select,
            outputs=[
                update_product_name,
                update_product_price
            ]
        )


        # ====================================================
        # INVENTORY PRODUCT SELECTION
        # ====================================================

        def select_inventory_product(product_name):

            quantity = get_inventory_quantity(
                product_name
            )

            if quantity is None:

                return None

            return quantity


        update_inventory_select.change(
            fn=select_inventory_product,
            inputs=update_inventory_select,
            outputs=update_inventory_quantity
        )


        # ====================================================
        # NAVIGATION
        # ====================================================

        def show_product_page():

            return (
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False)
            )


        def show_inventory_page():

            return (
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False)
            )


        def show_orders_page():

            return (
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
                gr.update(visible=False)
            )


        # ====================================================
        # DASHBOARD BUTTONS
        # ====================================================

        product_menu_button.click(
            fn=show_product_page,
            outputs=[
                dashboard_menu,
                product_page,
                inventory_page,
                orders_page
            ]
        )


        inventory_menu_button.click(
            fn=show_inventory_page,
            outputs=[
                dashboard_menu,
                product_page,
                inventory_page,
                orders_page
            ]
        )


        orders_menu_button.click(
            fn=show_orders_page,
            outputs=[
                dashboard_menu,
                product_page,
                inventory_page,
                orders_page
            ]
        )


        # ====================================================
        # BACK BUTTONS
        # ====================================================

        back_product_button.click(
            fn=back_to_dashboard,
            outputs=[
                dashboard_menu,
                product_page,
                inventory_page,
                orders_page
            ]
        )


        back_inventory_button.click(
            fn=back_to_dashboard,
            outputs=[
                dashboard_menu,
                product_page,
                inventory_page,
                orders_page
            ]
        )


        back_orders_button.click(
            fn=back_to_dashboard,
            outputs=[
                dashboard_menu,
                product_page,
                inventory_page,
                orders_page
            ]
        )


        # ====================================================
        # ADD PRODUCT
        # ====================================================

        add_product_button.click(
            fn=add_product_admin,

            inputs=[
                product_name_input,
                product_price_input
            ],

            outputs=[
                add_product_status,
                product_table
            ]
        ).then(
            fn=refresh_product_dropdowns,

            outputs=[
                update_product_select,
                delete_product_select
            ]
        ).then(
            fn=refresh_inventory_dropdowns,

            outputs=[
                add_inventory_select,
                update_inventory_select,
                delete_inventory_select
            ]
        )


        # ====================================================
        # REFRESH PRODUCTS
        # ====================================================

        refresh_products_button.click(
            fn=show_products,
            outputs=product_table
        ).then(
            fn=refresh_product_dropdowns,
            outputs=[
                update_product_select,
                delete_product_select
            ]
        ).then(
            fn=refresh_inventory_dropdowns,
            outputs=[
                add_inventory_select,
                update_inventory_select,
                delete_inventory_select
            ]
        )


        # ====================================================
        # UPDATE PRODUCT
        # ====================================================

        update_product_button.click(
            fn=update_product_admin,

            inputs=[
                update_product_select,
                update_product_name,
                update_product_price
            ],

            outputs=[
                update_product_status,
                product_table
            ]
        ).then(
            fn=refresh_product_dropdowns,
            outputs=[
                update_product_select,
                delete_product_select
            ]
        ).then(
            fn=refresh_inventory_dropdowns,
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
            fn=delete_product_admin,

            inputs=[
                delete_product_select
            ],

            outputs=[
                delete_product_status,
                product_table
            ]
        ).then(
            fn=refresh_product_dropdowns,
            outputs=[
                update_product_select,
                delete_product_select
            ]
        ).then(
            fn=refresh_inventory_dropdowns,
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
            fn=add_inventory_admin,

            inputs=[
                add_inventory_select,
                add_inventory_quantity
            ],

            outputs=[
                add_inventory_status,
                inventory_table
            ]
        ).then(
            fn=refresh_inventory_dropdowns,

            outputs=[
                add_inventory_select,
                update_inventory_select,
                delete_inventory_select
            ]
        )


        # ====================================================
        # REFRESH INVENTORY
        # ====================================================

        refresh_inventory_button.click(
            fn=show_inventory,
            outputs=inventory_table
        ).then(
            fn=refresh_inventory_dropdowns,
            outputs=[
                add_inventory_select,
                update_inventory_select,
                delete_inventory_select
            ]
        )


        # ====================================================
        # UPDATE INVENTORY
        # ====================================================

        update_inventory_button.click(
            fn=update_inventory_admin,

            inputs=[
                update_inventory_select,
                update_inventory_quantity
            ],

            outputs=[
                update_inventory_status,
                inventory_table
            ]
        ).then(
            fn=refresh_inventory_dropdowns,
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
            fn=delete_inventory_admin,

            inputs=[
                delete_inventory_select
            ],

            outputs=[
                delete_inventory_status,
                inventory_table
            ]
        ).then(
            fn=refresh_inventory_dropdowns,
            outputs=[
                add_inventory_select,
                update_inventory_select,
                delete_inventory_select
            ]
        )


        # ====================================================
        # REFRESH ORDERS
        # ====================================================

        refresh_orders_button.click(
            fn=show_orders,
            outputs=orders_table
        )


    return admin_dashboard


# ============================================================
# MAIN APPLICATION
# ============================================================

def create_app():

    css = """

    /* ========================================================
       MAIN BACKGROUND
       ======================================================== */

    body {
        background-color: #0f172a !important;
    }

    .gradio-container {
        background-color: #0f172a !important;
        color: white !important;
    }


    /* ========================================================
       CARDS
       ======================================================== */

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


    /* ========================================================
       TEXT
       ======================================================== */

    h1,
    h2,
    h3,
    h4,
    p,
    label,
    span {
        color: white !important;
    }


    /* ========================================================
       PRIMARY BUTTON
       ======================================================== */

    .gr-button-primary {
        background-color: #2563eb !important;
        border-color: #2563eb !important;
        color: white !important;
    }

    .gr-button-primary:hover {
        background-color: #1d4ed8 !important;
    }


    /* ========================================================
       SECONDARY BUTTON
       ======================================================== */

    .gr-button-secondary {
        background-color: #475569 !important;
        border-color: #64748b !important;
        color: white !important;
    }

    .gr-button-secondary:hover {
        background-color: #64748b !important;
    }


    /* ========================================================
       DELETE BUTTON
       ======================================================== */

    .gr-button-stop {
        background-color: #7f1d1d !important;
        border-color: #991b1b !important;
        color: white !important;
    }


    /* ========================================================
       INPUT BOXES
       ======================================================== */

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


    /* ========================================================
       DROPDOWN
       ======================================================== */

    .wrap {
        background-color: #1e293b !important;
        color: white !important;
        border-color: #475569 !important;
    }

    .wrap input {
        background-color: #1e293b !important;
        color: white !important;
    }


    /* ========================================================
       DATAFRAME
       ======================================================== */

    .table-wrap,
    .dataframe {
        background-color: #1e293b !important;
        color: white !important;
    }


    /* ========================================================
       STATUS BOX
       ======================================================== */

    textarea[disabled],
    input[disabled] {
        background-color: #1e293b !important;
        color: white !important;
        border-color: #475569 !important;
    }


    /* ========================================================
       ADMIN PAGE
       ======================================================== */

    .admin-page {
        padding-bottom: 40px;
    }


    /* ========================================================
       NUMBER INPUT
       ======================================================== */

    input[type="number"] {
        background-color: #1e293b !important;
        color: white !important;
    }

    """


    # ========================================================
    # GRADIO APP
    # ========================================================

    with gr.Blocks(
        title="Food Management System",
        css=css
    ) as app:


        # ====================================================
        # LOGIN SELECTION
        # ====================================================

        with gr.Column(
            visible=True,
            elem_classes="login-card"
        ) as login_page:

            gr.Markdown(
                "# 🍴 Food Management System"
            )

            gr.Markdown(
                "## Select Login Type"
            )


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

            gr.Markdown(
                "# 👨‍💼 Admin Login"
            )


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

            gr.Markdown(
                "# 👤 Customer Login"
            )


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
        # OLD LANDING DASHBOARD
        # ====================================================

        with gr.Column(
            visible=False,
            elem_classes="login-card"
        ) as dashboard_page:

            gr.Markdown(
                "# 🍴 Food Management System"
            )

            gr.Markdown(
                "## Admin Dashboard"
            )

            gr.Markdown(
                "Welcome, Administrator 👋"
            )

            admin_success_status = gr.Textbox(
                label="Login Status",
                interactive=False
            )


        # ====================================================
        # CREATE ADMIN DASHBOARD
        # ====================================================

        admin_dashboard_component = create_admin_dashboard()


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
            fn=open_admin_login,

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
            fn=open_customer_login,

            outputs=[
                login_page,
                admin_login_page,
                customer_login_page
            ]
        )


        # ====================================================
        # ADMIN LOGIN
        # ====================================================

        def process_admin_login(
            username,
            password
        ):

            success, message = check_admin_login(
                username,
                password
            )

            # -----------------------------------------------
            # LOGIN SUCCESS
            # -----------------------------------------------

            if success:

                return (
                    message,
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=True)
                )

            # -----------------------------------------------
            # LOGIN FAILED
            # -----------------------------------------------

            return (
                message,
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False)
            )


        admin_login_button.click(
            fn=process_admin_login,

            inputs=[
                admin_username,
                admin_password
            ],

            outputs=[
                admin_login_status,
                admin_login_page,
                dashboard_page,
                admin_dashboard_component
            ]
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
            fn=process_customer_login,

            inputs=[
                customer_username,
                customer_password
            ],

            outputs=customer_login_status
        )


    return app


# ============================================================
# RUN APPLICATION
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