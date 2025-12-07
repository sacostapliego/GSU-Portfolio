import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms
import json
import os
import ray
from ray.train import ScalingConfig
from ray.train.torch import TorchTrainer
import ray.train.torch

class MNISTCNN(nn.Module):
    # CNN for MNIST classification
    def __init__(self):
        # Initialize the CNN architecture
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

def train_func(config):
    # Training function to be executed on each Ray worker
    import ray.train
    
    # Extract training indices and data directory from config
    train_indices = config['train_indices']
    data_dir = config['data_dir']
    
    # Data transformations
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    # Use absolute path provided from main
    train_dataset = datasets.MNIST(data_dir, train=True, download=False, transform=transform)
    test_dataset = datasets.MNIST(data_dir, train=False, download=False, transform=transform)
    
    # Get worker rank for data splitting
    world_rank = ray.train.get_context().get_world_rank()
    world_size = ray.train.get_context().get_world_size()
    
    # Split training indices across workers
    indices_per_worker = len(train_indices) // world_size
    start_idx = world_rank * indices_per_worker
    end_idx = start_idx + indices_per_worker if world_rank < world_size - 1 else len(train_indices)
    
    worker_train_indices = train_indices[start_idx:end_idx]
    
    print(f"Worker {world_rank}/{world_size}: Training on {len(worker_train_indices)} samples")
    
    # Create subset for this worker
    train_subset = Subset(train_dataset, worker_train_indices)
    
    train_loader = DataLoader(train_subset, batch_size=128, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False)
    
    train_loader = ray.train.torch.prepare_data_loader(train_loader)
    test_loader = ray.train.torch.prepare_data_loader(test_loader)
    
    # Initialize model, loss function, and optimizer
    model = MNISTCNN()
    model = ray.train.torch.prepare_model(model)
    
    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Training loop
    epochs = 10
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for batch_idx, (data, target) in enumerate(train_loader):
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        
        if world_rank == 0:
            avg_loss = running_loss / len(train_loader)
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")
    
    model.eval()
    test_loss = 0.0
    correct = 0
    total = 0
    
    # Evaluation loop
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            loss = criterion(output, target)
            test_loss += loss.item()
            
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            total += target.size(0)
    
    accuracy = correct / total
    avg_test_loss = test_loss / len(test_loader)
    
    ray.train.report({
        'test_loss': avg_test_loss,
        'test_accuracy': accuracy
    })

# Main function
def main():
    print("=" * 80)
    print("MNIST Classification - PyTorch with Ray")
    print("=" * 80)
    
    # Get absolute path to data directory
    data_dir = os.path.abspath('./data')
    print(f"Data directory: {data_dir}")
    
    # Data transformations
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    # Load datasets to verify data exists
    print("Loading MNIST dataset...")
    train_dataset = datasets.MNIST(data_dir, train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST(data_dir, train=False, download=True, transform=transform)
    
    # Display dataset information
    print(f"Training samples: {len(train_dataset)}")
    print(f"Testing samples: {len(test_dataset)}")
    print("-" * 80)
    
    # Initialize Ray
    ray.init(address='auto', ignore_reinit_error=True)
    
    # Create indices for splitting
    train_indices = list(range(len(train_dataset)))
    
    # Configuration for training
    train_config = {
        'train_indices': train_indices,
        'data_dir': data_dir  # Pass absolute path to workers
    }
    
    # Scaling configuration for distributed training
    scaling_config = ScalingConfig(
        num_workers=2,
        use_gpu=False,
        resources_per_worker={"CPU": 1}
    )
    
    # Initialize and run the Ray TorchTrainer
    trainer = TorchTrainer(
        train_loop_per_worker=train_func,
        train_loop_config=train_config,
        scaling_config=scaling_config
    )
    
    #  Run the training
    result = trainer.fit()
    
    print("-" * 80)
    print("Distributed training completed. Retraining locally for final evaluation...")
    print("-" * 80)
    
    # Retrain locally for final results
    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False)
    
    # Initialize model, loss function, and optimizer
    model = MNISTCNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Training loop
    epochs = 10
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for batch_idx, (data, target) in enumerate(train_loader):
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        
        avg_loss = running_loss / len(train_loader)
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")
    
    # Evaluate the model
    model.eval()
    test_loss = 0.0
    correct = 0
    total = 0
    
    # Evaluation loop
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            loss = criterion(output, target)
            test_loss += loss.item()
            
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            total += target.size(0)
    
    # Calculate final metrics
    test_accuracy = correct / total
    avg_test_loss = test_loss / len(test_loader)
    
    print("-" * 80)
    # Display final results
    print(f"Test Loss: {avg_test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    
    # Save results to JSON
    results = {
        'framework': 'PyTorch with Ray',
        'test_loss': float(avg_test_loss),
        'test_accuracy': float(test_accuracy),
        'train_samples': len(train_dataset),
        'test_samples': len(test_dataset)
    }
    
    os.makedirs('results', exist_ok=True)
    with open('results/mnist_pytorch_ray_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to results/mnist_pytorch_ray_results.json")
    print("=" * 80)
    
    ray.shutdown()

if __name__ == "__main__":
    main()