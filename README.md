# 🎼 MuseScore Notesheet Downloader

A Flask-based web application that allows users to download notesheets from [MuseScore](https://musescore.com/). The application extracts and converts sheet music images into PDF format for easy access and printing.

## 🚀 Features
- Extracts notesheets from MuseScore pages.
- Converts SVG images into a clean, printable PDF format.
- Provides a simple web interface for users to enter a MuseScore URL.
- Runs seamlessly in a Docker container.

---

## 🛠 Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.11+
- Google Chrome or Chromium
- Chrome WebDriver
- Docker (if running inside a container)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/musescore-downloader.git
cd musescore-downloader
```

### 2️⃣ Install Dependencies
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Run the Flask App
```bash
python run.py
```
The app should now be accessible at `http://127.0.0.1:5000/`.

---

## 🐳 Running with Docker

### 1️⃣ Build the Docker Image
```bash
docker build -t musescore-downloader .
```

### 2️⃣ Run the Container
```bash
docker run -p 5000:5000 musescore-downloader
```

The application will be available at `http://localhost:5000/`.

---

## 📜 Usage
1. Open the web interface.
2. Enter the URL of the MuseScore notesheet.
3. Click the **Download** button.
4. Your PDF will be generated and downloaded.

---

## ⚙️ Environment Variables
To configure the app, create a `.env` file:
```
FLASK_APP=run.py
FLASK_ENV=production
CHROMEDRIVER_PATH=/usr/bin/chromedriver
```

---

## ❓ Troubleshooting
**1. Selenium WebDriver Issues**
   - Ensure you have **Google Chrome** installed.
   - Verify that the **chromedriver** version matches your Chrome version.
   - If running in Docker, install Chromium and the correct driver inside the container.

**2. File Permission Issues**
   - Ensure the application has write permissions to save generated PDFs.

**3. "No Such Element" Error in Docker**
   - Increase wait times (`WebDriverWait`) to allow elements to load.
   - Run Chrome with `--no-sandbox` and `--disable-dev-shm-usage` flags.

---

## 🤝 Contributing
Pull requests are welcome! Please follow best practices and open an issue for discussion before making changes.

---

## 📜 License
This project is licensed under the MIT License.

---

### 🎵 Happy Downloading! 🎶

