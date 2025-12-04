import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import os
from model import get_model

# ==========================================
# [설정] 학습 파라미터 (여기서 값을 수정하세요)
# ==========================================
NUM_EPOCHS = 30        # 학습 반복 횟수 (GPU니까 30번으로 증가!)
BATCH_SIZE = 4         # 한 번에 학습할 이미지 수 (컴퓨터 성능에 따라 조절)
LEARNING_RATE = 0.001  # 학습 속도 (너무 크면 발산, 너무 작으면 느림)
DATA_DIR = 'dataset'   # 데이터셋 폴더 이름
# ==========================================

def train_model():
    # Check if dataset exists
    if not os.path.exists(DATA_DIR):
        print(f"Error: Dataset directory '{DATA_DIR}' not found.")
        print("Please create 'dataset' folder and put images in subfolders named after their class.")
        return

    # Data transformations with Augmentation
    data_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),  # 좌우 반전
        transforms.RandomRotation(15),      # 살짝 회전
        transforms.ColorJitter(brightness=0.2, contrast=0.2), # 밝기/대비 변화
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Load dataset
    try:
        dataset = datasets.ImageFolder(DATA_DIR, transform=data_transforms)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    if len(dataset) == 0:
        print("Error: No images found in dataset folder.")
        return

    class_names = dataset.classes
    num_classes = len(class_names)
    
    print(f"Classes found: {len(class_names)} classes")

    # Initialize model
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    model = get_model(num_classes)
    model = model.to(device)

    # [Resume] Load existing weights if requested
    if RESUME and os.path.exists('culture_model.pth'):
        print(f"Loading existing model weights from 'culture_model.pth'...")
        try:
            checkpoint = torch.load('culture_model.pth')
            model_state = model.state_dict()
            
            # Filter out unnecessary keys (mismatched shapes)
            pretrained_dict = {k: v for k, v in checkpoint.items() if k in model_state and v.size() == model_state[k].size()}
            
            # Overwrite entries in the existing state dict
            model_state.update(pretrained_dict) 
            
            # Load the new state dict
            model.load_state_dict(model_state)
            
            if len(pretrained_dict) < len(checkpoint):
                print(f"Partial load: {len(pretrained_dict)}/{len(checkpoint)} layers loaded. (FC layer reset due to class change)")
            else:
                print("Resume successful! (All layers loaded)")
                
        except Exception as e:
            print(f"Resume failed: {e}")

    # Optimized: Use dataset.targets instead of iterating the whole dataset
    class_counts = [0] * num_classes
    for label in dataset.targets:
        class_counts[label] += 1
    
    # Calculate weights
    total_samples = sum(class_counts)
    class_weights = [total_samples / (num_classes * count) if count > 0 else 1.0 for count in class_counts]
    class_weights_tensor = torch.FloatTensor(class_weights).to(device)

    # Optimized DataLoader
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=8, pin_memory=True)

    criterion = nn.CrossEntropyLoss(weight=class_weights_tensor)
    optimizer = optim.SGD(model.parameters(), lr=LEARNING_RATE, momentum=0.9)
    
    # [Scheduler] Reduce LR if accuracy stops improving
    # Removed verbose=True for compatibility with older PyTorch versions
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.1, patience=3)

    best_acc = 0.0

    # Training loop
    for epoch in range(NUM_EPOCHS):
        model.train() # Set to training mode
        running_loss = 0.0
        correct = 0
        total = 0
        
        for inputs, labels in dataloader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            
            # Calculate Accuracy
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        epoch_loss = running_loss / len(dataloader)
        epoch_acc = 100 * correct / total
        
        # Current Learning Rate
        current_lr = optimizer.param_groups[0]['lr']
        print(f'Epoch {epoch+1}/{NUM_EPOCHS}, Loss: {epoch_loss:.4f}, Acc: {epoch_acc:.2f}%, LR: {current_lr}')
        
        # Step Scheduler
        scheduler.step(epoch_acc)

        # Save Best Model
        if epoch_acc > best_acc:
            best_acc = epoch_acc
            torch.save(model.state_dict(), 'culture_model_best.pth')
            print(f"  -> New Best Model Saved! ({best_acc:.2f}%)")
        
        # Save Checkpoint (overwrite every epoch)
        torch.save(model.state_dict(), 'culture_model.pth')

    # Save class names
    with open('class_names.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(class_names))
        
    print(f"Training complete. Best Accuracy: {best_acc:.2f}%")
    print("Best model saved as 'culture_model_best.pth'")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Cultural Heritage Model Trainer")
    parser.add_argument("--epochs", type=int, default=30, help="Number of epochs")
    parser.add_argument("--batch", type=int, default=32, help="Batch size")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    parser.add_argument("--dir", type=str, default='dataset', help="Dataset directory")
    parser.add_argument("--resume", action="store_true", help="Resume training from existing model")
    
    args = parser.parse_args()
    
    # Update global variables with args
    NUM_EPOCHS = args.epochs
    BATCH_SIZE = args.batch
    LEARNING_RATE = args.lr
    DATA_DIR = args.dir
    RESUME = args.resume
    
    train_model()
