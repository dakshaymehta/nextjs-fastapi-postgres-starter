from db_engine import sync_engine

def test_connection():
    try:
        with sync_engine.connect() as connection:
            print("Successfully connected to the database!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_connection()

# This script is used to test the connection to the database.
# I just created it for my own testing purposes.