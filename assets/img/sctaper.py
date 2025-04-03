import requests
from bs4 import BeautifulSoup
import os
import shutil
import sys
from urllib.parse import urljoin, urlparse

def scrape_website(url, output_folder="website_clone"):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    os.makedirs(output_folder, exist_ok=True)
    
    index_file = os.path.join(output_folder, "index.html")
    with open(index_file, "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    
    assets_folder = os.path.join(output_folder, "assets")
    os.makedirs(assets_folder, exist_ok=True)
    
    for tag in soup.find_all(["link", "script", "img"]):
        file_url = None
        if tag.name == "link" and tag.get("rel") == ["stylesheet"]:
            file_url = tag.get("href")
        elif tag.name == "script" and tag.get("src"):
            file_url = tag.get("src")
        elif tag.name == "img" and tag.get("src"):
            file_url = tag.get("src")
        
        if file_url:
            file_url = urljoin(url, file_url)
            filename = save_file(file_url, assets_folder)
            if filename:
                tag["src" if tag.name in ["script", "img"] else "href"] = f"assets/{filename}"
    
    with open(index_file, "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    
    print(f"Website successfully cloned in '{output_folder}' and ready for hosting.")

def save_file(file_url, output_folder):
    try:
        response = requests.get(file_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            parsed_url = urlparse(file_url)
            filename = os.path.basename(parsed_url.path)
            
            if filename:
                filepath = os.path.join(output_folder, filename)
                with open(filepath, "wb") as file:
                    file.write(response.content)
                print(f"Saved: {filename}")
                return filename
    except Exception as e:
        print(f"Failed to save {file_url}: {e}")
    return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        website_url = sys.argv[1]
        scrape_website(website_url)
    else:
        print("Usage: python scraper.py <website_url>")
