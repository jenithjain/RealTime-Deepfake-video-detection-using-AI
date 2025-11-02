"""
Check and display training metrics from saved model checkpoint
"""

import torch
import os

# Path to your trained model
MODEL_PATH = "weights/best_model.pth"

print("=" * 80)
print("🔍 CHECKING MODEL TRAINING METRICS")
print("=" * 80)

if not os.path.exists(MODEL_PATH):
    print(f"❌ Model not found at: {MODEL_PATH}")
    print("\nPlease train a model first using one of these methods:")
    print("1. TRAIN_WILDDEEPFAKE.ipynb (Google Colab)")
    print("2. python finetune_advanced.py")
    exit(1)

print(f"\n📁 Loading model from: {MODEL_PATH}")
print(f"📊 File size: {os.path.getsize(MODEL_PATH) / (1024*1024):.2f} MB\n")

# Load checkpoint
try:
    checkpoint = torch.load(MODEL_PATH, map_location='cpu')
    print("✅ Model loaded successfully!\n")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit(1)

# Check what's in the checkpoint
print("=" * 80)
print("📦 CHECKPOINT CONTENTS")
print("=" * 80)

if isinstance(checkpoint, dict):
    print(f"\nCheckpoint is a dictionary with {len(checkpoint)} keys:\n")
    for key in checkpoint.keys():
        print(f"  • {key}")
    
    print("\n" + "=" * 80)
    print("📊 TRAINING METRICS (if available)")
    print("=" * 80)
    
    # Check for common metric keys
    metric_keys = ['epoch', 'train_loss', 'val_loss', 'train_acc', 'val_acc', 
                   'accuracy', 'precision', 'recall', 'f1_score', 'best_acc',
                   'best_loss', 'learning_rate', 'optimizer_state_dict']
    
    found_metrics = False
    for key in metric_keys:
        if key in checkpoint:
            found_metrics = True
            value = checkpoint[key]
            if isinstance(value, (int, float)):
                if 'loss' in key.lower():
                    print(f"  • {key}: {value:.4f}")
                elif 'acc' in key.lower() or 'precision' in key.lower() or 'recall' in key.lower() or 'f1' in key.lower():
                    print(f"  • {key}: {value*100:.2f}%" if value <= 1 else f"  • {key}: {value:.2f}%")
                elif 'epoch' in key.lower():
                    print(f"  • {key}: {value}")
                elif 'lr' in key.lower() or 'learning_rate' in key.lower():
                    print(f"  • {key}: {value:.6f}")
            else:
                print(f"  • {key}: {type(value).__name__}")
    
    if not found_metrics:
        print("\n⚠️  No training metrics found in checkpoint.")
        print("The model was saved with only the state_dict (model weights).")
    
    # Check model state dict
    if 'model_state_dict' in checkpoint:
        state_dict = checkpoint['model_state_dict']
        print(f"\n📊 Model Architecture Info:")
        print(f"  • Total parameters: {len(state_dict)} layers")
        
        # Count total parameters
        total_params = 0
        for key, value in state_dict.items():
            if hasattr(value, 'numel'):
                total_params += value.numel()
        print(f"  • Total trainable parameters: {total_params:,}")
        print(f"  • Model size: ~{total_params * 4 / (1024*1024):.2f} MB (float32)")
    
    # Print all available info
    print("\n" + "=" * 80)
    print("📋 DETAILED CHECKPOINT INFO")
    print("=" * 80)
    for key, value in checkpoint.items():
        if key != 'model_state_dict' and key != 'optimizer_state_dict':
            print(f"\n{key}:")
            if isinstance(value, (int, float, str)):
                print(f"  {value}")
            elif isinstance(value, dict):
                print(f"  Dictionary with {len(value)} items")
            elif isinstance(value, list):
                print(f"  List with {len(value)} items")
            else:
                print(f"  {type(value).__name__}")

else:
    print("\n⚠️  Checkpoint is a state_dict (model weights only)")
    print("No training metrics were saved with this model.")
    print(f"\nModel contains {len(checkpoint)} layers")
    
    # Count parameters
    total_params = 0
    for key, value in checkpoint.items():
        if hasattr(value, 'numel'):
            total_params += value.numel()
    print(f"Total trainable parameters: {total_params:,}")

print("\n" + "=" * 80)
print("💡 RECOMMENDATIONS")
print("=" * 80)

print("""
If you want to see training metrics:

1. Train a new model with metrics tracking:
   - Use TRAIN_WILDDEEPFAKE.ipynb (saves metrics)
   - Or modify finetune_advanced.py to save metrics

2. Evaluate current model on test data:
   python evaluate_improved.py --model_path ./weights/best_model.pth

3. The model appears to be working (based on your backend logs)
   - Predictions are in range 0.0-1.0 ✓
   - No errors during inference ✓
   - Face detection working ✓

Current model performance (from logs):
  - Predictions range: 0.09 to 0.68
  - Average: ~0.30 (mostly classifying as REAL)
  - This suggests the model needs retraining on better data
""")

print("=" * 80)
