import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import json
import os

class IrisDataset(Dataset):
    # Custom Dataset for Iris data
    def __init__(self, X, y):
        self.X = torch.FloatTensor(X)
        self.y = torch.LongTensor(y)
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

class IrisNet(nn.Module):
    # Feedforward Neural Network for Iris classification
    def __init__(self, input_dim=4, hidden1=5, hidden2=6, num_classes=3):
        super(IrisNet, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden1)
        self.fc2 = nn.Linear(hidden1, hidden2)
        self.fc3 = nn.Linear(hidden2, num_classes)
        self.relu = nn.ReLU()
    
    # Forward pass
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def load_and_preprocess_data(filepath='./data/iris.csv'):
    # Load and preprocess the Iris dataset
    df = pd.read_csv(filepath)
    
    X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values
    y = df['species'].values
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    return X_train, X_test, y_train, y_test, label_encoder

def train_model(model, train_loader, criterion, optimizer, epochs=100):
    # Train the model
    model.train()
    # Training loop
    for epoch in range(epochs):
        running_loss = 0.0
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        
        if (epoch + 1) % 20 == 0:
            avg_loss = running_loss / len(train_loader)
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")

def evaluate_model(model, test_loader):
    # Evaluate the model
    model.eval()
    correct = 0
    total = 0
    test_loss = 0.0
    all_predictions = []
    all_labels = []
    
    criterion = nn.CrossEntropyLoss()
    
    # Evaluation loop
    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            test_loss += loss.item()
            
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            all_predictions.extend(predicted.numpy())
            all_labels.extend(labels.numpy())
    
    # Calculate accuracy
    accuracy = correct / total
    avg_loss = test_loss / len(test_loader)
    
    return avg_loss, accuracy, all_predictions, all_labels

def main():
    print("=" * 80)
    print("Iris Classification - PyTorch")
    print("=" * 80)
    
    # Load and preprocess data
    X_train, X_test, y_train, y_test, label_encoder = load_and_preprocess_data()
    
    # Display dataset information
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"Classes: {list(label_encoder.classes_)}")
    print("-" * 80)
    
    # Create datasets and dataloaders
    train_dataset = IrisDataset(X_train, y_train)
    test_dataset = IrisDataset(X_test, y_test)
    
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)
    
    # Initialize model, loss function, and optimizer
    model = IrisNet()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    print("Model Architecture:")
    print(model)
    print("-" * 80)
    
    train_model(model, train_loader, criterion, optimizer, epochs=100)
    
    print("-" * 80)
    test_loss, test_accuracy, predictions, true_labels = evaluate_model(model, test_loader)
    
    # Display results
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    # Save results to JSON
    results = {
        'framework': 'PyTorch',
        'test_loss': float(test_loss),
        'test_accuracy': float(test_accuracy),
        'predictions': [int(p) for p in predictions],
        'true_labels': [int(t) for t in true_labels],
        'class_names': label_encoder.classes_.tolist()
    }
    
    # Ensure results directory exists
    os.makedirs('results', exist_ok=True)
    with open('results/iris_pytorch_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to results/iris_pytorch_results.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
