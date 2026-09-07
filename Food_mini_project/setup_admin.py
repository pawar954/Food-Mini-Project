from create_tables import create_tables
from admin_auth import create_admin

create_tables()

admin_id = create_admin(
    "shweta",
    "shweta123",
    "Shweta"
)

if admin_id:
    print("Shweta admin created successfully.")
else:
    print("Admin already exists or could not be created.")