# Week 7 Lab BASIC: Introduction to Web Scraping with Python

ผู้จัดทำ: เมธาวี สิทธิชัยเนตร, รหัสนักศึกษา 663380372-6

ใช้ `requests` ดาวน์โหลดหน้าเว็บ [Automate the Boring Stuff with Python (3rd Edition)](https://automatetheboringstuff.com/3e/) แล้วใช้ `BeautifulSoup4` แปลง HTML เพื่อดึง **ชื่อหนังสือ** และ **รายชื่อบททั้งหมด**

## 📸 ผลลัพธ์ใน Terminal
![Terminal output](screenshots/terminal_output.png)

## วิธีรัน (Windows PowerShell)
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```
ถ้า PowerShell ขึ้น `running scripts is disabled` ให้เปิด PowerShell แบบ **Run as Administrator** แล้วรันคำสั่งนี้ จากนั้นพิมพ์ `Y`
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ผลลัพธ์ที่คาดหวัง
```
กำลังดาวน์โหลดเนื้อหาจาก: https://automatetheboringstuff.com/3e/
ดาวน์โหลดเนื้อหาสำเร็จ

--- ข้อมูลที่ Scrape ได้ ---
ชื่อหนังสือ: 3rd Edition

ชื่อบทต่างๆ:
1. Introduction
2. Chapter 1 – Python Basics
...
```

## โครงสร้างโปรเจกต์
```
web-scraping-intro/
├── src/
│   ├── __init__.py      # บอกว่า src เป็น Python package
│   └── scraper.py       # คลาส SimpleWebScraper (_get_html_content, scrape_main_titles)
├── screenshots/
│   └── terminal_output.png
├── main.py              # จุดเริ่มต้นโปรแกรม
├── requirements.txt     # requests, beautifulsoup4
├── .gitignore           # ไม่ commit venv/ และ __pycache__/
└── README.md
```

## หลักการทำงาน
1. `_get_html_content()` ใช้ `requests.get()` พร้อม header `User-Agent` (กัน 403) และ `timeout=30` แล้วตรวจ `raise_for_status()` จัดการ `HTTPError`, `ConnectionError`, `Timeout` และ `RequestException`
2. `scrape_main_titles()` ใช้ BeautifulSoup หาข้อมูล 2 ส่วน
   * ชื่อหนังสือ: `<article>`, `<header>` แล้ว `<h1>`
   * ชื่อบท: `<div class="content-body">` แล้ว `ul li a` (CSS selector)
   * ตรวจ `if element:` ก่อนใช้ทุกครั้ง ป้องกัน `AttributeError: 'NoneType'`

## ⚖️ จริยธรรม
ตรวจ `robots.txt` และ Terms of Service ก่อน scrape ทุกครั้ง ไม่ส่ง request ถี่จนเป็นภาระเซิร์ฟเวอร์ และถ้าเว็บมี API ให้ใช้ API แทน เว็บที่ใช้ในแล็บนี้เปิดให้อ่านเนื้อหาได้เพื่อการศึกษา
