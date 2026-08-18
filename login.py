ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

CUSTOMER_USERNAME = "customer"
CUSTOMER_PASSWORD = "customer123"


def check_admin_login(username, password):

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return True, "Admin login successful."

    return False, "Invalid admin username or password."


def check_customer_login(username, password):

    if username == CUSTOMER_USERNAME and password == CUSTOMER_PASSWORD:
        return True, "Customer login successful."

    return False, "Invalid customer username or password."