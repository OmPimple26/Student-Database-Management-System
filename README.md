# Student-Database-Management-System
🎓 Student Database Management System built with Python 🐍. Manage student records with ease — add ➕, update ✏️, delete 🗑️, and search 🔍 functionalities. Simple yet scalable project, perfect for learning database operations &amp; CRUD applications 📊.

🚀 A full-featured **Student & Faculty Database Management System** built with **Python, Streamlit, SQLite, and Plotly**.  
It provides an easy-to-use interface for **managing students, faculty, and departments**, along with **interactive visualizations** 📊.  

---

## ✨ Features  

- 👩‍🎓 **Student Management** – Add ➕, Update ✏️, Remove 🗑️ student records  
- 👨‍🏫 **Faculty Management** – Add, Update, Remove faculty records  
- 🏫 **Department Overview** – View student & faculty counts per department  
- 📊 **Analytics** –  
  - Student-to-Department Ratio  
  - Faculty-to-Department Ratio  
  - Girl-to-Boy Ratio  
- 🔍 **Search Functionality** – Search across Students, Faculty, and Departments  
- 🔑 **Admin Login** – Role-based access with separate admin panel  
- 🗄️ **Database** – Powered by **SQLite3**  
- 🎭 **Fake Data Generator** – Insert up to **10,000+ fake records** using `faker`  

---

## 🛠️ Tech Stack  

- **Frontend / UI**: Streamlit 🌐  
- **Database**: SQLite3 🗄️  
- **Data Visualization**: Plotly 📊, Pandas 🐼  
- **Fake Data Generator**: Faker 🎭  
- **Language**: Python 🐍  

---

## 📂 Project Structure  

├── app.py              # Main Streamlit App
├── database_setup.py   # Database schema & helper functions
├── fake_data.py        # Script to generate fake records
├── requirements.txt    # Python dependencies
├── university.db       # SQLite database file

---

## ⚡ Installation  

# 1️⃣ Clone the repository
git clone https://github.com/your-username/Student-Database-Management-System.git
cd Student-Database-Management-System

# 2️⃣ (Optional) Create & activate virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Mac/Linux

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ (Optional) Generate fake data (10,000+ students & faculty)
python fake_data.py

# 5️⃣ Run the Streamlit app
streamlit run app.py
🔑 Admin Login
Username: admin

Password: admin

🤝 Contributing
Contributions are welcome! Feel free to fork, open issues, or submit pull requests.

📜 License
This project is open-source and available under the MIT License.
