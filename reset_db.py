from db import init_db

# This calls the function to drop the events table and create a new one.
init_db(recreate=True)

print("Database has been reset successfully.")