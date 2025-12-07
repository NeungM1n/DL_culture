import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import get_model
import os
from collections import Counter, defaultdict
import sys

def evaluate_model(data_dir='dataset', model_path='culture_model_best.pth', batch_size=32):
    # Device configuration
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Data transforms (same as validation/inference)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Load dataset
    try:
        dataset = datasets.ImageFolder(data_dir, transform=transform)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    class_names = dataset.classes
    num_classes = len(class_names)
    print(f"Loaded {num_classes} classes.")

    # Load model
    model = get_model(num_classes)
    
    if not os.path.exists(model_path):
        print(f"Model file '{model_path}' not found.")
        return
        
    try:
        # Load weights (handling potential partial mismatch if needed, though best model should match)
        checkpoint = torch.load(model_path, map_location=device)
        model.load_state_dict(checkpoint)
        print(f"Loaded model from {model_path}")
    except Exception as e:
        print(f"Error loading model weights: {e}")
        return

    model = model.to(device)
    model.eval()

    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=4)

    print("Starting evaluation... (this may take a few minutes)")

    correct_top1 = 0
    correct_top5 = 0
    total = 0
    
    # Error Analysis
    # Key: (True Class, Predicted Class), Value: Count
    confusion_counts = Counter()
    
    # Key: True Class, Value: [Correct Count, Total Count]
    class_accuracy = defaultdict(lambda: [0, 0])

    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)
            
            # Top-1 Prediction
            _, pred_top1 = torch.max(outputs, 1)
            
            # Top-5 Prediction
            _, pred_top5 = outputs.topk(5, 1, True, True)
            pred_top5 = pred_top5.t()
            correct_top5 += pred_top5.eq(labels.view(1, -1).expand_as(pred_top5)).sum().item()

            # Update stats
            total += labels.size(0)
            correct_top1 += (pred_top1 == labels).sum().item()

            # Collect errors
            for i in range(labels.size(0)):
                true_label = labels[i].item()
                pred_label = pred_top1[i].item()
                
                class_accuracy[true_label][1] += 1 # Total count for this class
                
                if true_label == pred_label:
                    class_accuracy[true_label][0] += 1 # Correct count
                else:
                    confusion_counts[(class_names[true_label], class_names[pred_label])] += 1

    # --- Report ---
    acc_top1 = 100 * correct_top1 / total
    acc_top5 = 100 * correct_top5 / total
    
    print("\n" + "="*50)
    print(f"FINAL RESULTS")
    print("="*50)
    print(f"Total Images: {total}")
    print(f"Top-1 Accuracy: {acc_top1:.2f}% (Exact Match)")
    print(f"Top-5 Accuracy: {acc_top5:.2f}% (Answer in top 5 guesses)")
    print("="*50)

    print("\n[Top 10 Most Confused Pairs]")
    print("(Actual -> Predicted : Count)")
    for (true_name, pred_name), count in confusion_counts.most_common(10):
        print(f"{true_name} -> {pred_name} : {count} times")

    print("\n[Top 10 Hardest Classes (Lowest Accuracy)]")
    # Filter classes with at least 5 samples to avoid noise
    hardest_classes = []
    for label, (correct, total_count) in class_accuracy.items():
        if total_count >= 5:
            acc = 100 * correct / total_count
            hardest_classes.append((class_names[label], acc, total_count))
    
    hardest_classes.sort(key=lambda x: x[1]) # Sort by accuracy ascending
    
    for name, acc, count in hardest_classes[:10]:
        print(f"{name}: {acc:.1f}% ({count} samples)")

if __name__ == "__main__":
    evaluate_model()
