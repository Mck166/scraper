import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Auto install WebDriver
import time

# Set up logging to print progress to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode for faster execution (no browser UI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Use webdriver-manager to automatically download and manage ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to extract hrefs from li elements with class "span6 first forsale"
def extract_links_from_page(url):
    try:
        driver.get(url)
        logging.info(f"Accessing URL: {url}")
        time.sleep(0.5)  # Ensure the page fully loads (you can adjust this delay as needed)

        # Locate all li elements with class "span6 first forsale"
        hrefs = []
        li_elements = driver.find_elements(By.CSS_SELECTOR, "li.span6.first.forsale a")
        for li_element in li_elements:
            href_value = li_element.get_attribute("href")
            if href_value:
                hrefs.append(href_value)

        if hrefs:
            logging.info(f"Found {len(hrefs)} links on {url}")
        else:
            logging.info(f"No valid links found on {url}")
        
        return hrefs
    except Exception as e:
        logging.error(f"Error accessing URL: {url}, Error: {str(e)}")
        return []

# Function to read URLs from a file and extract hrefs
def process_urls_from_file(input_file, output_file):
    all_links = []
    
    try:
        with open(input_file, 'r') as file:
            urls = [line.strip() for line in file.readlines() if line.strip()]
            logging.info(f"Processing {len(urls)} URLs from file: {input_file}")
            
            for idx, url in enumerate(urls):
                logging.info(f"Processing URL {idx + 1} of {len(urls)}: {url}")
                page_links = extract_links_from_page(url)
                if page_links:
                    for link in page_links:
                        logging.info(f"Found href: {link}")
                all_links.extend(page_links)
                
        # Save the collected links to the output file
        with open(output_file, 'w') as output:
            for link in all_links:
                output.write(f"{link}\n")
        logging.info(f"Saved {len(all_links)} total links to {output_file}")
    
    except FileNotFoundError:
        logging.error(f"File not found: {input_file}")

# Input and output file paths
input_file = "street_links.txt"
output_file = "address_links.txt"

# Process the URLs and save found links
process_urls_from_file(input_file, output_file)

# Close the WebDriver
driver.quit()
