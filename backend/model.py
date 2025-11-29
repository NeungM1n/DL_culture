import torch
import torch.nn as nn
from torchvision import models

def get_model(num_classes):
    # Load pre-trained ResNet18
    model = models.resnet18(pretrained=True)
    
    # Freeze early layers (optional, but good for small datasets)
    # for param in model.parameters():
    #     param.requires_grad = False
        
    # Replace the final fully connected layer
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    
    return model
