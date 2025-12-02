import os
import random
from PIL import Image
import torchvision.transforms as transforms

def augment_dataset(data_dir='dataset', target_count=200):
    if not os.path.exists(data_dir):
        print(f"Error: Directory '{data_dir}' not found.")
        return

    # Define Augmentations
    augmenter = transforms.Compose([
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        # transforms.RandomResizedCrop(size=(224, 224), scale=(0.8, 1.0)), # Optional: Crop
    ])

    classes = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    
    print(f"Found classes: {classes}")
    print(f"Target count per class: {target_count}")

    for class_name in classes:
        class_dir = os.path.join(data_dir, class_name)
        images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        current_count = len(images)
        
        print(f"\nProcessing '{class_name}': {current_count} images found.")
        
        if current_count >= target_count:
            print(f"  -> Already has enough images. Skipping.")
            continue

        if current_count == 0:
            print(f"  -> No images found to augment. Skipping.")
            continue
            
        needed = target_count - current_count
        print(f"  -> Generating {needed} augmented images...")
        
        for i in range(needed):
            # Randomly select an original image to augment
            src_img_name = random.choice(images)
            src_img_path = os.path.join(class_dir, src_img_name)
            
            try:
                with Image.open(src_img_path) as img:
                    img = img.convert('RGB')
                    
                    # Apply augmentation
                    aug_img = augmenter(img)
                    
                    # Save new image
                    save_name = f"aug_{i}_{src_img_name}"
                    save_path = os.path.join(class_dir, save_name)
                    aug_img.save(save_path)
                    
            except Exception as e:
                print(f"    Error processing {src_img_name}: {e}")

        print(f"  -> Done! Now has {len(os.listdir(class_dir))} images.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Dataset Balancer (Augmentation)")
    parser.add_argument("--target", type=int, default=200, help="Target number of images per class")
    parser.add_argument("--dir", type=str, default='dataset', help="Path to dataset directory")
    
    args = parser.parse_args()
    
    print("--- Dataset Balancer (Augmentation) ---")
    augment_dataset(args.dir, args.target)
