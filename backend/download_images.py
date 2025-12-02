import os
import shutil
import argparse
import time
from icrawler.builtin import BingImageCrawler

def download_images_bing(query, num_images=100, output_dir='dataset'):
    # Create directory if it doesn't exist
    save_dir = os.path.join(output_dir, query)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Refine query to avoid restaurants (add 'scenery' or 'cultural heritage')
    search_query = f"{query} 전경"
    print(f"Searching for images of '{search_query}' (original: {query}) using Bing...")
    
    # Use BingImageCrawler with filters
    # type='photo' excludes cliparts/lines
    crawler = BingImageCrawler(storage={'root_dir': save_dir})
    
    # Run the crawler with filters
    try:
        # filters='photo' helps, and the refined query helps more
        crawler.crawl(keyword=search_query, max_num=num_images, filters=dict(type='photo'))
        print(f"\nSuccessfully downloaded images to '{save_dir}'")
    except Exception as e:
        print(f"Search failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cultural Heritage Image Downloader")
    parser.add_argument("--batch", action="store_true", help="Run in batch mode using landmarks.txt")
    parser.add_argument("--count", type=int, default=50, help="Number of images per class")
    parser.add_argument("--query", type=str, help="Single query to download")
    
    args = parser.parse_args()

    if args.batch:
        # Batch mode from CLI
        if os.path.exists('landmarks.txt'):
            with open('landmarks.txt', 'r', encoding='utf-8') as f:
                landmarks = [line.strip() for line in f if line.strip()]
            
            print(f"Starting batch download for {len(landmarks)} landmarks...")
            print(f"Images per class: {args.count}")
            
            for i, landmark in enumerate(landmarks):
                print(f"\n[{i+1}/{len(landmarks)}] Processing: {landmark}")
                download_images_bing(landmark, num_images=args.count)
                time.sleep(1)
        else:
            print("Error: 'landmarks.txt' not found.")
            
    elif args.query:
        # Single query from CLI
        download_images_bing(args.query, num_images=args.count)
        
    else:
        # Interactive mode (default)
        print("--- Bulk Image Downloader (Powered by icrawler) ---")
        print("1. Single Search (하나만 검색)")
        print("2. Download Recommended Landmarks (추천 문화재 10종 일괄 다운로드)")
        print("3. Download from landmarks.txt (전체 목록 다운로드)")
        
        choice = input("Choose option (1, 2, or 3): ").strip()
        
        if choice == '1':
            query = input("Enter search query (e.g., 경복궁): ")
            count = int(input("How many images? (default 50): ") or 50)
            download_images_bing(query, num_images=count)
            
        elif choice == '2':
            landmarks = [
                "숭례문", "경복궁", "불국사", "석굴암", "다보탑", 
                "첨성대", "창덕궁", "수원 화성", "광화문", "동궁과 월지"
            ]
            count = int(input("How many images per class? (default 50): ") or 50)
            for item in landmarks:
                download_images_bing(item, num_images=count)
                
        elif choice == '3':
            if os.path.exists('landmarks.txt'):
                with open('landmarks.txt', 'r', encoding='utf-8') as f:
                    landmarks = [line.strip() for line in f if line.strip()]
                
                print(f"Found {len(landmarks)} landmarks in list.")
                count = int(input(f"How many images per class? (default 50, Total {len(landmarks)} classes): ") or 50)
                
                print(f"Starting batch download for {len(landmarks)} landmarks...")
                for i, landmark in enumerate(landmarks):
                    print(f"\n[{i+1}/{len(landmarks)}] Processing: {landmark}")
                    download_images_bing(landmark, num_images=count)
                    time.sleep(1)
            else:
                print("Error: 'landmarks.txt' not found.")
        else:
            print("Invalid choice.")
