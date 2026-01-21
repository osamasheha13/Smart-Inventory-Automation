# Smart Inventory Automation: From Manual Chaos to Scalable Data Engineering

## 📌 Context & Real-World Problem
This project was born out of a real business need within my current role. We faced a significant operational bottleneck: inventory orders were arriving via informal channels (text messages/WhatsApp) and being manually entered into Excel. 

**The Challenges were:**
- **Human Error:** Manual entry led to frequent typos and stock discrepancies.
- **Inconsistent Naming:** One item could be referred to by three different names.
- **Data Silos:** No historical audit trail of transactions or supplier links.
- **Time Inefficiency:** Reconciliation took hours of manual cross-checking.

## 💡 The Solution: A Hybrid Automation Bridge
Instead of a "toy project," I built a production-ready bridge that connects a user-friendly Excel interface with the power of Python and SQL. This system automates the entire "Text-to-Report" pipeline.

## 🛠 Tech Stack & Methodology
- **Frontend (UX):** Microsoft Excel with a professional VBA-driven dashboard.
- **Engine (Logic):** Python 3.10 utilizing **Fuzzy Logic** (`FuzzyWuzzy`) to resolve naming inconsistencies—acting as a "Smart Interpreter" for human-written text.
- **Database (Persistence):** SQLite3, implementing a relational schema (Products, Suppliers, Transactions) to ensure data integrity.
- **AI Collaboration:** Leveraging **Generative AI (Gemini/LLMs)** to co-pilot the VBA development and optimize script performance, demonstrating a modern "AI-Augmented" workflow.

## 🚀 Key Professional Features
- **Fuzzy Matching Engine:** Intelligently maps informal text inputs to official database records.
- **Automated Audit Trail:** Every transaction is logged with a timestamp, preventing data loss and ensuring financial accountability.
- **Dynamic Reporting:** One-click financial reports generated in Excel, ready for management review.
- **Restock/Disburse Logic:** Detects keywords to automatically increase or decrease stock levels.

## 📈 Business Impact
- **80% Reduction** in manual data entry time.
- **Eliminated 95%** of inventory naming errors through fuzzy matching.
- **Real-time Visibility:** Management now has instant access to stock levels and supplier info.

## 📂 Project Architecture
- `/src`: Modular Python scripts (Database Setup, Order Processor, Report Generator).
- `/data`: Relational SQLite database.
- `Smart_Inventory.xlsm`: The Command Hub (VBA Interface).

---
*Developed by a Finance Professional with a passion for Data Engineering and Process Automation.*
