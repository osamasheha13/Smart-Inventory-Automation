import sqlite3
import os
from fuzzywuzzy import process

def run_processing():
    # Set absolute paths for stability
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'data', 'inventory_core.db')
    orders_input = os.path.join(base_dir, 'data', 'orders_mock.txt')

    if not os.path.exists(orders_input):
        print(f"[ERROR] File not found: {orders_input}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Load products for fuzzy matching
    cursor.execute("SELECT Product_ID, Product_Name FROM Products")
    products = cursor.fetchall()
    product_names = [p[1] for p in products]
    name_to_id = {p[1]: p[0] for p in products}

    current_station = "Main Warehouse"

    with open(orders_input, 'r') as file:
        for line in file:
            line = line.strip()
            if not line: continue
            
            # Identify the station or source
            if ":" in line:
                current_station = line.split(":")[-1].strip()
                continue

            try:
                # Check if the line is an addition (ADD) or a disbursement
                is_restock = "ADD" in line.upper()
                clean_line = line.upper().replace("ADD", "").strip()
                
                parts = clean_line.split(maxsplit=1)
                qty = int(parts[0])
                item_name = parts[1]

                # Fuzzy match the product name
                match, score = process.extractOne(item_name, product_names)

                if score > 75:
                    p_id = name_to_id[match]
                    
                    # Logic: if ADD is present, quantity is positive; else, negative
                    final_qty = qty if is_restock else -qty
                    action_type = 'RESTOCK' if is_restock else 'DISBURSEMENT'

                    # Update Stock
                    cursor.execute("UPDATE Products SET Current_Stock = Current_Stock + ? WHERE Product_ID = ?", (final_qty, p_id))
                    
                    # Log Transaction
                    cursor.execute("""
                        INSERT INTO Transactions (Product_ID, Quantity_Changed, Action_Type, Destination)
                        VALUES (?, ?, ?, ?)
                    """, (p_id, final_qty, action_type, current_station))
                    
                    print(f"[{action_type}] {match}: {final_qty} units. Location: {current_station}")
                else:
                    print(f"[SKIP] Low match score ({score}%) for: {item_name}")

            except Exception as e:
                print(f"[ERROR] Skipping line '{line}': {e}")
    # Clear the orders file after successful processing
    try:
        with open(orders_input, 'w') as file:
            file.write("# Orders processed successfully.\n# Ready for new entries.\n")
        print("[CLEANUP] orders_mock.txt has been cleared.")
    except Exception as e:
        print(f"[WARNING] Could not clear orders file: {e}")

    conn.commit()
    conn.close()
    print("\n--- Processing Finished Successfully ---")

if __name__ == "__main__":
    run_processing()

