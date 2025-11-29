import os
import requests
from bs4 import BeautifulSoup
import urllib.parse

def download_images(query, num_images=10, output_dir='dataset'):
    # Create directory if it doesn't exist
    save_dir = os.path.join(output_dir, query)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print(f"Searching for images of '{query}'...")
    
    # Google Images search URL
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbm=isch"
    
    # Headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find image elements (this selector might need adjustment as Google changes HTML)
        # Trying a more robust method for thumbnails
        img_tags = soup.find_all("img")
        
        count = 0
        for img in img_tags:
            if count >= num_images:
                break
                
            try:
                img_url = img.get('src')
                if img_url and img_url.startswith('http'):
                    # Download image
                    img_data = requests.get(img_url).content
                    
                    file_path = os.path.join(save_dir, f"{query}_{count+1}.jpg")
                    with open(file_path, 'wb') as f:
                        f.write(img_data)
                        
                    print(f"Downloaded: {file_path}")
                    count += 1
            except Exception as e:
                print(f"Error downloading image: {e}")
                
        print(f"\nSuccessfully downloaded {count} images to '{save_dir}'")
        
    except Exception as e:
        print(f"Search failed: {e}")

if __name__ == "__main__":
    print("--- Image Downloader ---")
    query = input("Enter search term (e.g., gyeongbokgung): ")
    count = int(input("How many images? (default 10): ") or 10)
    
    download_images(query, count, 'dataset')
