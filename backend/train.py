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
NUM_EPOCHS = 10        # 학습 반복 횟수 (너무 크면 과적합, 너무 작으면 학습 부족)
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

    # Data transformations
    data_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
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

    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    class_names = dataset.classes
    num_classes = len(class_names)
    
    print(f"Classes found: {class_names}")

    # Initialize model
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    model = get_model(num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=LEARNING_RATE, momentum=0.9)

    # Training loop
    for epoch in range(NUM_EPOCHS):
        running_loss = 0.0
        for inputs, labels in dataloader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f'Epoch {epoch+1}/{NUM_EPOCHS}, Loss: {running_loss/len(dataloader):.4f}')

    # Save model and class names
    torch.save(model.state_dict(), 'culture_model.pth')
    with open('class_names.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(class_names))
        
    print("Training complete. Model saved as 'culture_model.pth'")

if __name__ == '__main__':
    train_model()
