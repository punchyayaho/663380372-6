# AD1 LabX ADV: Advanced Web Scraping & Introduction to Automated Agents

**Agentic Web Scraper ด้วย Python และ Selenium**
ผู้จัดทำ: เมธาวี สิทธิชัยเนตร, รหัสนักศึกษา 663380372-6

Agent แบบ config-driven: อ่านกฎการ scrape จาก `configs/example_site_config.json` แล้วเปิดเบราว์เซอร์ด้วย Selenium ไปที่ `start_url` ดึงข้อมูลสินค้า (ชื่อ, ราคา, URL, รูปภาพ) จากทุกการ์ดสินค้า กดปุ่ม "next" เพื่อไปหน้าถัดไปจนครบ `max_pages` แล้วบันทึกผลลง `data/scraped_products.json`

## 📸 ผลลัพธ์ (Screenshots)

### 1. ผลลัพธ์ของโค้ดใน Terminal
![Terminal output](screenshots/terminal_output.png)

### 2. ผลลัพธ์ในไฟล์ `data/scraped_products.json`
![scraped_products.json](screenshots/scraped_products_json.png)

## 🔑 แนวคิดหลักที่สาธิต
- **Selenium** สำหรับเนื้อหาไดนามิก (headless Chrome, implicit wait, explicit wait helper)
- **webdriver_manager** จัดการ ChromeDriver อัตโนมัติ (มี fallback ไปใช้ Selenium Manager ในตัว)
- **Config-Driven Automation**: พฤติกรรมของ scraper กำหนดไว้ในไฟล์ JSON ภายนอก
- **การออกแบบ Agent แบบโมดูล**: แยกไฟล์ `driver_manager`, `config_parser`, `scraper_agent`, `data_models`, `utils`
- **Robustness**: ตรวจสอบ config, ใช้ `try/finally` ปิดเบราว์เซอร์เสมอ, คืนค่า `None` เมื่อหา field ไม่เจอ, หน่วงเวลาระหว่างหน้า
- **Structured Data**: ใช้ `@dataclass Product` แล้วบันทึกเป็น JSON

## 📁 โครงสร้างโปรเจกต์
```
agentic-web-scraper/
├── src/
│   ├── __init__.py
│   ├── scraper_agent.py     # ตรรกะหลักของ agent (อ่าน config, ควบคุม selenium, pagination)
│   ├── config_parser.py     # โหลดและตรวจสอบ configuration
│   ├── data_models.py       # dataclass Product
│   ├── utils.py             # save JSON, wait, safe_click
│   └── driver_manager.py    # ตั้งค่า Selenium WebDriver (Chrome/Firefox, headless)
├── configs/
│   └── example_site_config.json
├── data/
│   └── scraped_products.json     # ข้อมูล output
├── docs/
│   └── ETHICS.md
├── screenshots/
│   ├── terminal_output.png
│   └── scraped_products_json.png
├── main.py
├── test_setup.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 วิธีรัน (Windows / VS Code)
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1        # PowerShell  (cmd ใช้: venv\Scripts\activate)
pip install -r requirements.txt
python test_setup.py               # ตรวจสอบ setup: ต้องเห็น Title: All products | Books to Scrape - Sandbox
python main.py
```

### ผลลัพธ์ที่ควรได้
```
Scraping page 1...
Scraping page 2...
Successfully scraped 40 items and saved to data/scraped_products.json
```

## ⚙️ Configuration (`configs/example_site_config.json`)
| Key | ความหมาย |
|---|---|
| `start_url` | หน้าเริ่มต้น |
| `max_pages` | จำนวนหน้าสูงสุดที่ agent จะ scrape |
| `delay_between_pages` | หน่วงเวลา (วินาที) ระหว่างหน้า |
| `item_container_selector` | CSS selector ของการ์ดสินค้า 1 ชิ้น |
| `pagination_selector` | CSS selector ของปุ่ม "next" |
| `item_data_selectors` | selector ของแต่ละ field (`name`, `price`, `description`, `url`, `image_url`) |

## ⚖️ จริยธรรม
ดู [docs/ETHICS.md](docs/ETHICS.md) โปรเจกต์นี้ scrape เฉพาะ books.toscrape.com ซึ่งเป็นเว็บที่สร้างขึ้นเพื่อการฝึกโดยเฉพาะ และหน่วงเวลาระหว่างหน้าทุกครั้ง
