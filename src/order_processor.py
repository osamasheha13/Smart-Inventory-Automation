import sqlite3
import pandas as pd
import os
import re
from fuzzywuzzy import process

def process_smart_orders():
    # 1. Setup Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "data", "inventory_core.db")
    input_file = os.path.join(base_dir, "..", "data", "orders_mock.txt")

    # Check if input file exists and is not empty
    if not os.path.exists(input_file) or os.stat(input_file).st_size == 0:
        print("[INFO] No orders to process. The input file is empty.")
        return

    # 2. Database Connection
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Load product list for Fuzzy Matching
        cursor.execute("SELECT Product_ID, Product_Name FROM Products")
        products_db = cursor.fetchall()
        
        if not products_db:
            print("[ERROR] No products found in database. Please run database_setup.py first.")
            return

        product_names = [p[1] for p in products_db]
        product_map = {p[1]: p[0] for p in products_db}

        # 3. Read Orders
        with open(input_file, "r") as file:
            lines = file.readlines()

        processed_any = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            try:
                # 4. Smart Quantity Extraction (Regex)
                # Finds all numbers and takes the largest one (likely the quantity)
                all_numbers = re.findall(r'(\d+)', line)
                if not all_numbers:
                    print(f"[SKIP] No quantity found in line: '{line}'")
                    continue
                
                # Logic: In medical orders, the largest number is usually the quantity
                quantity = int(max(all_numbers, key=int))

                # 5. Determine Action Type (ADD vs Disbursement)
                action = "RESTOCK" if "ADD" in line.upper() else "DISBURSE"
                qty_change = quantity if action == "RESTOCK" else -quantity

                # 6. Product Identification (Fuzzy Matching)
                # Clean line from numbers and common words to help the matcher
                clean_text = re.sub(r'\d+', '', line).upper()
                clean_text = clean_text.replace("ADD", "").replace("UNITS", "").replace("PLEASE", "").strip()
                
                best_match, score = process.extractOne(clean_text, product_names)

                # Threshold: Only process if we are > 60% sure
                if score > 60:
                    p_id = product_map[best_match]
                    
                    # A. Update Inventory Stock
                    cursor.execute("""
                        UPDATE Products 
                        SET Current_Stock = Current_Stock + ? 
                        WHERE Product_ID = ?
                    """, (qty_change, p_id))
                    
                    # B. Log to Transaction History
                    # We store the original line as 'Destination' for context
                    cursor.execute("""
                        INSERT INTO Transactions (Product_ID, Quantity_Changed, Action_Type, Destination)
                        VALUES (?, ?, ?, ?)
                    """, (p_id, qty_change, action, line))
                    
                    print(f"[SUCCESS] {action}: {best_match} ({quantity} units) | Match Score: {score}%")
                    processed_any = True
                else:
                    print(f"[WARNING] Low match score ({score}%) for line: '{line}'. Skipped.")

            except Exception as line_error:
                print(f"[ERROR] Could not process line '{line}': {line_error}")

        # 7. Finalize and Cleanup
        if processed_any:
            conn.commit()
            # Clear the input file after successful processing
            with open(input_file, "w") as file:
                file.write("") 
            print("\n[DONE] Orders processed and database updated.")
        else:
            print("\n[INFO] No valid orders were found to process.")

    except sqlite3.Error as db_error:
        print(f"[DATABASE ERROR] {db_error}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    process_smart_orders()
