from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfMerger
import os
import shutil
import unicodedata
import re
import tempfile

# Create a temporary directory for the user session data
temp_dir = tempfile.mkdtemp()

# Configure Chrome options to allow web scraping
options = Options()
options.add_argument('--headless')  # Enable headless mode
options.add_argument('--disable-gpu')  # Disable GPU usage
options.add_argument('--no-sandbox')  # Run without sandbox 
options.add_argument('--disable-software-rasterizer')  # Disable software rasterizer 
options.add_argument('--disable-dev-shm-usage')  # Prevent errors in Docker environment
options.add_argument('--window-size=1920,1080') # Necessary to run web scraper correctly inside Docker

# Create a temporary directory for the user data (or specify your own)
# Set the unique user-data-dir for Chrome
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_argument(f"user-data-dir={temp_dir}")
prefs = {"profile.managed_default_content_settings.images": 1}
options.add_experimental_option("prefs", prefs)

# Define directories for storing data
svg_folder = "./Data"
pdf_folder = "./PDFs"

# Use ChromeDriver with Brave
driver = webdriver.Chrome(options=options)
actions = ActionChains(driver)

def slugify(value, allow_unicode=False):
    """
    Function that converts a string into file name safe string, removing all special characters and spaces.
    Takes a string as input and returns modified string.
    """
    value = str(value)  
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def get_notesheet_pdf(url):
    """
    Function that takes a museScore URL as an input and returns a PDF file containing the notesheet.
    """
    img_urls = []
    title = ""

    # Open a website
    driver.get(url)
    wait = WebDriverWait(driver, 2)

    # Get correct file name based on scraped data and find all notesheet parent containers
    title = slugify(driver.find_element(By.CSS_SELECTOR, ".nFRPI.V4kyC.z85vg.N30cN").text)
    parentElems = driver.find_elements(By.CSS_SELECTOR, ".EEnGW.F16e6")

    # Get all image URLs from the notesheet parent containers
    for elem in parentElems:
        actions.move_to_element(elem).perform()
        img_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))
        img_urls.append(elem.find_element(By.TAG_NAME, "img").get_attribute("src"))

    driver.quit()

    # Prepare directories for storing SVG and PDF files
    os.makedirs(svg_folder, exist_ok=True)
    os.makedirs(pdf_folder, exist_ok=True)
    os.makedirs("./ResultPDFs", exist_ok=True)

    # Download SVG files from the image URLs
    for i in range(0, len(img_urls)):
        data = requests.get(img_urls[i], headers={"User-Agent": "Mozilla/5.0"})
        filename = f"image_{i+1}.svg"
        with open(f"{svg_folder}/{filename}", "wb") as f:
            f.write(data.content)

    # Convert SVG files to PDF files
    # Possible bottleneck - try different approach
    pdf_files = []
    for i, filename in enumerate(sorted(os.listdir(svg_folder))):
        if filename.endswith(".svg"):
            svg_path = os.path.join(svg_folder, filename)
            pdf_path = os.path.join(pdf_folder, f"page_{i+1}.pdf")

            drawing = svg2rlg(svg_path)

            # Get original SVG dimensions
            original_width = drawing.width
            original_height = drawing.height

            # Calculate scaling factors to fit the SVG within A4 dimensions
            scale_x = A4[0] / original_width
            scale_y = A4[1] / original_height
            scale = min(scale_x, scale_y)  # Use the smaller scale to fit within A4

            # Create a new drawing with A4 dimensions
            new_drawing = Drawing(A4[0], A4[1])

            # Apply scaling to the original drawing's contents
            drawing.scale(scale, scale)

            # Center the scaled SVG on the A4 page
            new_drawing.translate((A4[0] - original_width * scale) / 2,
                                (A4[1] - original_height * scale) / 2)

            # Add the scaled SVG to the new drawing
            new_drawing.add(drawing)

            renderPDF.drawToFile(new_drawing, pdf_path)

            pdf_files.append(pdf_path)

    # Merge all PDF files into a single document
    output_pdf = f"./ResultPDFs/{title}.pdf"
    doc_name = f"{title}.pdf"
    merger = PdfMerger()
    for pdf_file in sorted(pdf_files):
        merger.append(pdf_file)

    # Export resulting merged file
    merger.write(output_pdf)
    merger.close()

    # Clean up temporary directories
    shutil.rmtree(pdf_folder, ignore_errors=True)
    shutil.rmtree(svg_folder, ignore_errors=True)
    
    return doc_name