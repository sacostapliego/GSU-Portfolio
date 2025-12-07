import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import json
import os

class MNISTCNN(nn.Module):
    # CNN for MNIST classification
    def __init__(self):
        super(MNISTCNN, self).__init__()
        
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=0)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=0)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.flatten = nn.Flatten()
        self.dropout = nn.Dropout(0.5)
        self.fc1 = nn.Linear(32 * 5 * 5, 128)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(128, 10)
    # Forward pass
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        
        x = self.flatten(x)
        x = self.dropout(x)
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.fc2(x)
        
        return x

def load_data():
    #      Load MNIST dataset
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    # Load datasets
    train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST('./data', train=False, transform=transform)
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False)
    
    return train_loader, test_loader

def train_model(model, train_loader, criterion, optimizer, device, epochs=10):
    # Train the model
    model.train()
    # Training loop
    for epoch in range(epochs):
        running_loss = 0.0
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            
            # Zero the parameter gradients
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
        
        avg_loss = running_loss / len(train_loader)
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")


def evaluate_model(model, test_loader, device):
    # Evaluate the model
    model.eval()
    test_loss = 0.0
    correct = 0
    total = 0
    
    # Define loss function
    criterion = nn.CrossEntropyLoss()
    
    # Evaluation loop
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)
            test_loss += loss.item()
            
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            total += target.size(0)
    
    accuracy = correct / total
    avg_loss = test_loss / len(test_loader)
    
    return avg_loss, accuracy

def main():
    print("=" * 80)
    print("MNIST Classification - PyTorch CNN")
    print("=" * 80)
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Load and preprocess data
    train_loader, test_loader = load_data()
    
    # Display dataset info
    print(f"Training samples: {len(train_loader.dataset)}")
    print(f"Testing samples: {len(test_loader.dataset)}")
    print("-" * 80)
    
    # Build model
    model = MNISTCNN().to(device)
    
    # Display model architecture
    print("Model Architecture:")
    print(model)
    print("-" * 80)
    
    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Train the model
    train_model(model, train_loader, criterion, optimizer, device, epochs=10)
    
    print("-" * 80)
    # Evaluate the model
    test_loss, test_accuracy = evaluate_model(model, test_loader, device)
    
    # Display results
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    
    # Save results to JSON
    results = {
        'framework': 'PyTorch',
        'test_loss': float(test_loss),
        'test_accuracy': float(test_accuracy),
        'train_samples': len(train_loader.dataset),
        'test_samples': len(test_loader.dataset)
    }
    
    os.makedirs('results', exist_ok=True)
    with open('results/mnist_pytorch_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to results/mnist_pytorch_results.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
