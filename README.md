# 🧑‍💼 Job Listing Web Application

A full-stack job portal that allows users to **post, filter, edit, delete**, and **scrape real jobs** from the web. Built with React (frontend), Flask (backend), MySQL (database), and Selenium (scraping bot).

---

## 🚀 Features

- ✅ Post a job with title, company, location, job type, tags, and description
- ✅ Edit and delete existing jobs
- ✅ Filter jobs by location, type, keyword, or tag
- ✅ Sort jobs by newest or oldest
- ✅ Scrape real jobs from [actuarylist.com](https://www.actuarylist.com) using Selenium
- ✅ Store and serve all jobs via Flask REST API
- ✅ Persistent storage using MySQL

---

## 🛠️ Tech Stack

| Layer       | Technology            |
|-------------|------------------------|
| Frontend    | React.js               |
| Backend     | Flask (Python)         |
| Database    | MySQL                  |
| Scraper     | Selenium + WebDriver   |
| API Format  | REST + JSON            |

---

## 📁 Project Structure




📦 1. Clone the Project

git clone <your-repo-url>
cd job-listing-app



🖥 2. Setup Backend (Flask + MySQL)
cd backend

# ✅ Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate  # On Mac/Linux

# ✅ Install required Python packages
pip install -r requirements.txt


Create DB manually (if not already created):

CREATE DATABASE job_portal;




🚀 3. Run Backend API

python app.py




4. Setup Frontend (React)
In a new terminal window:

cd frontend
npm install
npm start


🤖 5. Run the Scraper (Optional)
cd backend
python scrape.py



----------------------------------VIDEO  LINK ----------------------------------

https://drive.google.com/file/d/1Y_0HnLDE1mr8AtYo8eQRogq7Hjk6Du3y/view?usp=drive_link

