import requests
import os
from bs4 import BeautifulSoup
import time

# Use a headless browser to render JavaScript
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_manuscript_pages(url, start_page=2, end_page=None):
    base_url = url.split('#')[0]
    folder_path = 'data/manuscript'
    
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    
    # Initialize the Chrome driver once
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    page = start_page
    start_time = time.time()
    total_pages = 0
    while end_page is None or page <= end_page:
        page_url = f"{base_url}#page/{page}/mode/2up"
        
        driver.get(page_url)
        time.sleep(5)  # Wait for JavaScript to render
        
        page_source = driver.page_source
        
        soup = BeautifulSoup(page_source, 'html.parser')
        
        img_tags = soup.select('#BookReader > div.BRcontainer > div.BRtwopageview img')
        
        if img_tags:
            for idx, img_tag in enumerate(img_tags):
                if 'src' in img_tag.attrs:
                    img_url = img_tag['src']
                    img_response = requests.get(img_url)
                    
                    if img_response.status_code == 200:
                        file_name = f"page_{page}_{idx + 1}.jpg"
                        file_path = os.path.join(folder_path, file_name)
                        
                        with open(file_path, 'wb') as file:
                            file.write(img_response.content)
                        
                        print(f"Saved image {idx + 1} for page {page}")
                    else:
                        print(f"Failed to download image {idx + 1} for page {page}")
                else:
                    print(f"No source found for image {idx + 1} on page {page}")
        else:
            print(f"No images found for page {page}")
        # Increment to the next even page number
        page += 2
        total_pages += 2
        
        # Add a small delay to avoid overwhelming the server
        time.sleep(0.1)
        
        # Calculate and print time estimate
        elapsed_time = time.time() - start_time
        avg_time_per_page = elapsed_time / total_pages
        remaining_pages = (end_page - page + 2) if end_page else "unknown"
        if remaining_pages != "unknown":
            estimated_time = avg_time_per_page * remaining_pages
            hours, remainder = divmod(estimated_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"Estimated time remaining: {int(hours)}h {int(minutes)}m {int(seconds)}s")
    
    # Close the driver after all pages are processed
    driver.quit()
    
    print("Scraping completed")

# Example usage:
scrape_manuscript_pages("https://www.bdl.servizirl.it/bdl/bookreader/index.html?path=fe&cdOggetto=23675#page/2/mode/2up", start_page=60, end_page=576)


