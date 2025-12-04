import os
import random
from PIL import Image
import torchvision.transforms as transforms
import multiprocessing
import argparse

def process_class(args):
    """Worker function to process a single class"""
    class_name, data_dir, target_count = args
    class_dir = os.path.join(data_dir, class_name)
    
    try:
        images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        current_count = len(images)
        
        if current_count == 0:
            return f"Skipped '{class_name}': No images found."
            
        if current_count >= target_count:
            return None # Silent skip if already done
            
        needed = target_count - current_count
        
        # Define Augmentations (inside worker)
        augmenter = transforms.Compose([
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        ])
        
        for i in range(needed):
            try:
                src_img_name = random.choice(images)
                src_img_path = os.path.join(class_dir, src_img_name)
                
                with Image.open(src_img_path) as img:
                    img = img.convert('RGB')
                    aug_img = augmenter(img)
                    
                    save_name = f"aug_{i}_{src_img_name}"
                    save_path = os.path.join(class_dir, save_name)
                    aug_img.save(save_path)
            except Exception as e:
                # print(f"Error in {class_name}: {e}")
                continue
                
        return f"Processed '{class_name}': Generated {needed} images."
        
    except Exception as e:
        return f"Error processing class '{class_name}': {e}"

def augment_dataset_parallel(data_dir='dataset', target_count=200):
    if not os.path.exists(data_dir):
        print(f"Error: Directory '{data_dir}' not found.")
        return

    classes = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    total_classes = len(classes)
    print(f"Found {total_classes} classes. Starting parallel augmentation...")
    
    # Prepare arguments
    tasks = [(cls, data_dir, target_count) for cls in classes]
    
    # Use mostly all cores (leave 1-2 for system if needed, or just use all)
    num_cores = max(1, multiprocessing.cpu_count() - 1) 
    print(f"Using {num_cores} CPU cores for processing.")
    
    with multiprocessing.Pool(processes=num_cores) as pool:
        for i, result in enumerate(pool.imap_unordered(process_class, tasks)):
            if result:
                print(f"[{i+1}/{total_classes}] {result}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parallel Dataset Balancer")
    parser.add_argument("--target", type=int, default=200, help="Target number of images per class")
    parser.add_argument("--dir", type=str, default='dataset', help="Path to dataset directory")
    
    args = parser.parse_args()
    
    augment_dataset_parallel(args.dir, args.target)
