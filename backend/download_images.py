import os
import shutil
from icrawler.builtin import BingImageCrawler

def download_images(query, num_images=100, output_dir='dataset'):
    # Create directory if it doesn't exist
    save_dir = os.path.join(output_dir, query)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print(f"Searching for images of '{query}' using Bing...")
    
    # Use BingImageCrawler (often more stable for bulk downloads without API keys)
    crawler = BingImageCrawler(storage={'root_dir': save_dir})
    
    # Run the crawler
    crawler.crawl(keyword=query, max_num=num_images)
    
    print(f"\nSuccessfully downloaded images to '{save_dir}'")

if __name__ == "__main__":
    print("--- Bulk Image Downloader (Powered by icrawler) ---")
    query = input("Enter search term (e.g., gyeongbokgung): ")
    count_input = input("How many images? (default 50): ")
    
    count = int(count_input) if count_input.strip() else 50
    
    download_images(query, count, 'dataset')
