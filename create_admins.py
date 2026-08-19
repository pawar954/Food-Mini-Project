from admin_auth import create_admin


# ============================================================
# CREATE SHWETA
# ============================================================

admin1 = create_admin(
    "shweta",
    "shweta123",
    "Shweta"
)


# ============================================================
# CREATE POOJA
# ============================================================

admin2 = create_admin(
    "pooja",
    "pooja123",
    "Pooja"
)


# ============================================================
# RESULT
# ============================================================

if admin1:

    print("Shweta admin created successfully.")

else:

    print("Shweta admin already exists.")


if admin2:

    print("Pooja admin created successfully.")

else:

    print("Pooja admin already exists.")