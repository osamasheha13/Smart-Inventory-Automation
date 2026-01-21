# Smart Inventory Automation System (Python-VBA Integration)

## 📌 Project Overview
A professional hybrid automation solution designed to bridge the gap between legacy Excel-based workflows and modern database management. This system automates inventory processing using **Fuzzy Logic** for string matching and **SQLite** for robust data integrity.

## 🛠 Tech Stack
- **Frontend:** Microsoft Excel (VBA)
- **Engine:** Python 3.10+
- **Database:** SQLite3
- **Libraries:** Pandas, FuzzyWuzzy, XlsxWriter
- **Data Architecture:** 3-Table Schema (Products, Suppliers, Transactions)

## 🚀 Key Features
- **Fuzzy Matching Engine:** Handles inconsistent item naming in orders (e.g., "Amoxi 500" vs "Amoxicillin 500mg") with over 80% accuracy.
- **Bi-directional Processing:** Supports both "Disbursement" (Stock-out) and "Restocking" (Stock-in) via keyword detection.
- **Financial Reporting:** Generates automated Excel reports with conditional formatting for low-stock alerts.
- **Audit Trail:** Every transaction is logged with timestamps and destination tracking for full transparency.

## 💼 Business Value (FP&A Perspective)
- **Reduced Error Rate:** Minimized manual entry mistakes through automated script processing.
- **Scalability:** Transitioned from flat Excel sheets to a relational database model.
- **Operational Efficiency:** Automated the reconciliation process between order requests and inventory levels.

## 📂 Project Structure
- `/src`: Python scripts for database setup, processing, and reporting.
- `/data`: SQLite database and raw order input files.
- `/reports`: Automatically generated financial and status reports.
- `Smart_Inventory.xlsm`: The user interface and control hub.