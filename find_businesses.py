from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import chromedriver_autoinstaller

# Define the search term and the number of scrolls
search_term = "flower shops in Riyadh"
scroll_times = 5  # Number of times to scroll for more businesses

# Initialize URLs file
urls_filename = 'urls.txt'

# Function to write URLs to the file
def append_url_to_file(url):
    with open(urls_filename, 'a') as f:
        f.write(url + '\n')

# Function to define and set up the WebDriver
def driver_define():
    print('Chromedriver Installing')
    driver_path = chromedriver_autoinstaller.install()
    
    print('Chrome Browser Opening')
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s, options=options)
    return driver

# Function to search on Google Maps
def search_google_maps(driver, search_term):
    driver.get("https://www.google.com/maps")
    
    # Wait until search box appears and enter search term
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load
    time.sleep(5)

# Function to scroll through businesses and extract URLs
def scroll_and_collect_urls(driver, scroll_times):
    for i in range(scroll_times):
        print(f"Scrolling page {i + 1}...")
        
        # Get all business elements
        business_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href^="https://www.google.com/maps/place"]')
        
        # Loop through the business elements and extract URLs
        for business in business_elements:
            business_url = business.get_attribute('href')
            print(f"Found URL: {business_url}")
            append_url_to_file(business_url)
        
        # Scroll down to load more results
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for the page to load new businesses

# Load existing URLs into a set
def load_existing_urls():
    try:
        with open(urls_filename, 'r') as f:
            return set([line.strip() for line in f])
    except FileNotFoundError:
        return set()

# Function to append URL to the file if not already present
def append_url_to_file(url):
    if url not in existing_urls:
        with open(urls_filename, 'a') as f:
            f.write(url + '\n')
        existing_urls.add(url)
        print(f"New URL added: {url}")



if __name__ == "__main__":
    existing_urls = load_existing_urls()  # Load existing URLs at the start

    driver = driver_define()
    search_google_maps(driver, search_term)
    scroll_and_collect_urls(driver, scroll_times)
    driver.quit()

    print("URLs have been collected and saved to urls.txt.")
