import sqlite3
import os

def initialize_system():
    # Set absolute path for the database file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "..", "data", "inventory_core.db")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Step 1: Drop existing tables safely
        cursor.execute("DROP TABLE IF EXISTS Transactions")
        cursor.execute("DROP TABLE IF EXISTS Products")
        cursor.execute("DROP TABLE IF EXISTS Suppliers")

        # Step 2: Create Suppliers Table 
        cursor.execute("""
            CREATE TABLE Suppliers (
                Supplier_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Supplier_Name TEXT NOT NULL,
                Category TEXT,
                Contact_Person TEXT,
                Location TEXT
            )
        """)

        # Step 3: Create Products Table
        cursor.execute("""
            CREATE TABLE Products (
                Product_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Product_Name TEXT NOT NULL,
                Category TEXT,
                Current_Stock INTEGER DEFAULT 0,
                Min_Stock_Level INTEGER DEFAULT 10,
                Supplier_ID INTEGER,
                FOREIGN KEY (Supplier_ID) REFERENCES Suppliers (Supplier_ID)
            )
        """)

        # Step 4: Create Transactions Table
        cursor.execute("""
            CREATE TABLE Transactions (
                Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Product_ID INTEGER,
                Quantity_Changed INTEGER,
                Action_Type TEXT,
                Destination TEXT,
                Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (Product_ID) REFERENCES Products (Product_ID)
            )
        """)

        # Step 5: Insert Mock Data for Suppliers
        suppliers_data = [
            ('Global-Pharma', 'Antibiotics', 'John Smith', 'London'),
            ('Vaccine-Direct', 'Vaccines', 'Sarah Muller', 'Berlin'),
            ('Medi-Supply Co', 'Antiseptics', 'Ahmed Hassan', 'Cairo')
        ]
        cursor.executemany("""
            INSERT INTO Suppliers (Supplier_Name, Category, Contact_Person, Location) 
            VALUES (?,?,?,?)
        """, suppliers_data)

        # Step 6: Insert Mock Data for Products (Linked to Supplier IDs)
        # Assuming Supplier IDs are 1, 2, 3 after insertion
        products_data = [
            ('Amoxicillin 500mg', 'Antibiotics', 150, 20, 1),
            ('Iodine Solution', 'Antiseptics', 45, 10, 3),
            ('Newcastle Vaccine', 'Vaccines', 500, 50, 2)
        ]
        cursor.executemany("""
            INSERT INTO Products (Product_Name, Category, Current_Stock, Min_Stock_Level, Supplier_ID) 
            VALUES (?,?,?,?,?)
        """, products_data)

        conn.commit()
        conn.close()
        print("[SUCCESS] Database fully initialized with Suppliers and Products.")

    except Exception as e:
        print(f"[ERROR] Reset failed: {e}")

if __name__ == "__main__":
    initialize_system()