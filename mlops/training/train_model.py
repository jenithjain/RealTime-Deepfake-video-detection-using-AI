"""
MLOps Training Pipeline
Trains deepfake detection model on videos or images
"""

import os
import sys
import argparse
import yaml
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
import cv2
from pathlib import Path
import json
from datetime import datetime
from tqdm import tqdm
import numpy as np

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from efficientnet_pytorch import EfficientNet


class DeepfakeDataset(Dataset):
    """Dataset for deepfake detection - supports images and video frames"""
    
    def __init__(self, data_dir, transform=None, mode='images'):
        """
        Args:
            data_dir: Directory containing data
            transform: Image transformations
            mode: 'images' or 'videos'
        """
        self.data_dir = Path(data_dir)
        self.transform = transform
        self.mode = mode
        self.samples = []
        
        # Load data
        if mode == 'images':
            self._load_images()
        elif mode == 'videos':
            self._load_videos()
    
    def _load_images(self):
        """Load image dataset"""
        # Expect structure: data_dir/real/*.jpg, data_dir/fake/*.jpg
        real_dir = self.data_dir / 'real'
        fake_dir = self.data_dir / 'fake'
        
        if real_dir.exists():
            for img_path in real_dir.glob('*.jpg') + list(real_dir.glob('*.png')):
                self.samples.append((str(img_path), 0))  # 0 = real
        
        if fake_dir.exists():
            for img_path in fake_dir.glob('*.jpg') + list(fake_dir.glob('*.png')):
                self.samples.append((str(img_path), 1))  # 1 = fake
        
        print(f"Loaded {len(self.samples)} images ({len([s for s in self.samples if s[1]==0])} real, {len([s for s in self.samples if s[1]==1])} fake)")
    
    def _load_videos(self):
        """Load video dataset - extract frames"""
        # Expect structure: data_dir/real/*.mp4, data_dir/fake/*.mp4
        real_dir = self.data_dir / 'real'
        fake_dir = self.data_dir / 'fake'
        
        if real_dir.exists():
            for video_path in real_dir.glob('*.mp4'):
                frames = self._extract_frames(video_path, max_frames=10)
                for frame in frames:
                    self.samples.append((frame, 0))  # 0 = real
        
        if fake_dir.exists():
            for video_path in fake_dir.glob('*.mp4'):
                frames = self._extract_frames(video_path, max_frames=10)
                for frame in frames:
                    self.samples.append((frame, 1))  # 1 = fake
        
        print(f"Loaded {len(self.samples)} frames from videos")
    
    def _extract_frames(self, video_path, max_frames=10):
        """Extract frames from video"""
        frames = []
        cap = cv2.VideoCapture(str(video_path))
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_indices = np.linspace(0, total_frames-1, max_frames, dtype=int)
        
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame_rgb)
        
        cap.release()
        return frames
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        if self.mode == 'images':
            img_path, label = self.samples[idx]
            image = Image.open(img_path).convert('RGB')
        else:
            image, label = self.samples[idx]
            image = Image.fromarray(image)
        
        if self.transform:
            image = self.transform(image)
        
        return image, label


def train_model(config_path, data_dir, output_dir, version):
    """
    Train deepfake detection model
    
    Args:
        config_path: Path to config YAML
        data_dir: Path to training data
        output_dir: Path to save model
        version: Model version string
    """
    # Load config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Data transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    # Load dataset
    mode = config.get('data', {}).get('mode', 'images')
    dataset = DeepfakeDataset(data_dir, transform=transform, mode=mode)
    
    # Split dataset
    train_size = int(0.7 * len(dataset))
    val_size = int(0.15 * len(dataset))
    test_size = len(dataset) - train_size - val_size
    
    train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
        dataset, [train_size, val_size, test_size]
    )
    
    # Data loaders
    batch_size = config.get('training', {}).get('batch_size', 32)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    # Model
    model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=2)
    model = model.to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config.get('training', {}).get('learning_rate', 0.001))
    
    # Training loop
    epochs = config.get('training', {}).get('epochs', 50)
    best_val_acc = 0.0
    
    training_history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': []
    }
    
    print(f"\n🚀 Starting training for {epochs} epochs...")
    
    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        pbar = tqdm(train_loader, desc=f'Epoch {epoch+1}/{epochs}')
        for images, labels in pbar:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = outputs.max(1)
            train_total += labels.size(0)
            train_correct += predicted.eq(labels).sum().item()
            
            pbar.set_postfix({'loss': loss.item(), 'acc': 100.*train_correct/train_total})
        
        train_acc = 100. * train_correct / train_total
        train_loss = train_loss / len(train_loader)
        
        # Validation
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()
        
        val_acc = 100. * val_correct / val_total
        val_loss = val_loss / len(val_loader)
        
        # Save history
        training_history['train_loss'].append(train_loss)
        training_history['train_acc'].append(train_acc)
        training_history['val_loss'].append(val_loss)
        training_history['val_acc'].append(val_acc)
        
        print(f'Epoch {epoch+1}: Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%, Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%')
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            output_path = Path(output_dir) / version
            output_path.mkdir(parents=True, exist_ok=True)
            
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
                'config': config
            }, output_path / 'model.pth')
            
            print(f'✅ Saved best model with val_acc: {val_acc:.2f}%')
    
    # Save training history
    with open(output_path / 'training_history.json', 'w') as f:
        json.dump(training_history, f, indent=2)
    
    # Save metadata
    metadata = {
        'version': version,
        'timestamp': datetime.now().isoformat(),
        'config': config,
        'best_val_acc': best_val_acc,
        'epochs_trained': epochs,
        'dataset_size': len(dataset),
        'device': str(device)
    }
    
    with open(output_path / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f'\n✅ Training complete!')
    print(f'   Best validation accuracy: {best_val_acc:.2f}%')
    print(f'   Model saved to: {output_path}')
    
    return model, metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train deepfake detection model')
    parser.add_argument('--config', type=str, default='mlops/training/config.yaml', help='Path to config file')
    parser.add_argument('--data', type=str, default='mlops/data/train', help='Path to training data')
    parser.add_argument('--output', type=str, default='mlops/registry/models', help='Output directory')
    parser.add_argument('--version', type=str, default='v1.0.0', help='Model version')
    
    args = parser.parse_args()
    
    train_model(args.config, args.data, args.output, args.version)
