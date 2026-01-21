import sqlite3
import pandas as pd
import os

def generate_professional_report():
    # Set absolute paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'data', 'inventory_core.db')
    report_folder = os.path.join(base_dir, 'reports')
    report_file = os.path.join(report_folder, 'Financial_Inventory_Analysis.xlsx')

    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    try:
        conn = sqlite3.connect(db_path)
        
        # SQL Query joining Products with Suppliers (Strategic View)
        query = """
        SELECT 
            p.Product_Name, 
            p.Category, 
            p.Current_Stock, 
            p.Min_Stock_Level,
            s.Supplier_Name,
            s.Location as Supplier_Location
        FROM Products p
        LEFT JOIN Suppliers s ON p.Category = s.Category 
        """
        # Note: We link by Category as an example for the logic
        
        df_inventory = pd.read_sql_query(query, conn)
        df_transactions = pd.read_sql_query("SELECT * FROM Transactions", conn)

        # Write final Excel with professional formatting
        with pd.ExcelWriter(report_file, engine='xlsxwriter') as writer:
            df_inventory.to_excel(writer, sheet_name='Stock_Status', index=False)
            df_transactions.to_excel(writer, sheet_name='Transaction_History', index=False)
            
            # Formatting (Briefly)
            workbook = writer.book
            worksheet = writer.sheets['Stock_Status']
            header_format = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
            
            for col_num, value in enumerate(df_inventory.columns.values):
                worksheet.write(0, col_num, value, header_format)

        print(f"[SUCCESS] Financial Report generated: {report_file}")
        conn.close()

    except Exception as e:
        print(f"[ERROR] Reporting failed: {e}")

if __name__ == "__main__":
    generate_professional_report()