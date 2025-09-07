# Python Generators – Task 0

## 🎯 Objective
Set up a MySQL database and seed it with user data from a CSV file.  
This prepares the foundation for creating a generator that streams rows one by one.

---

## 📦 Requirements
- Python 3.8+
- MySQL server installed and running
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)  

Install dependencies:
```bash
pip install mysql-connector-python
```

---

## 🗄️ Database Setup
- **Database name**: `ALX_prodev`
- **Table**: `user_data`
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)

---

## 📂 Files
- `seed.py` → Handles DB connection, database/table creation, and CSV seeding  
- `0-main.py` → Entry script to test database setup and verify seeding  
- `user_data.csv` → Sample dataset (names, emails, ages)

---

## ▶️ How to Run

### 1. Verify Database in MySQL Shell
```sql
SHOW DATABASES;
USE ALX_prodev;
SHOW TABLES;
SELECT * FROM user_data LIMIT 5;
```

### 2. Run the Python script
```bash
python 0-main.py
```

---

## ✅ Sample Output
```text
Database ALX_prodev ensured.
✅ Connection successful
Table user_data created successfully
Data inserted successfully
✅ Database ALX_prodev is present
📊 Sample rows: [
  ('00110337-645e-4e67-92e8-c3b04359ae15', 'Spencer Shields', 'Calvin_Hayes15@gmail.com', Decimal('67')),
  ('00703991-29d9-4074-a2d3-163e6638c8a3', 'Fannie Kunde', 'Myron.Tromp@hotmail.com', Decimal('98')),
  ...
]
```

---

## 🔑 Key Notes
- The sample rows come directly from `user_data.csv`.  
- The script auto-creates the database and table if they do not exist.  
- Run `SELECT COUNT(*) FROM user_data;` in MySQL shell to check total rows inserted.
