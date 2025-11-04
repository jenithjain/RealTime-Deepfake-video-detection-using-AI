"""
Model Deployment Script
Deploys models to staging or production
"""

import sys
import argparse
import shutil
from pathlib import Path

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from registry.model_registry import ModelRegistry


def deploy_model(version, environment='staging'):
    """
    Deploy model to specified environment
    
    Args:
        version: Model version to deploy
        environment: 'staging' or 'production'
    """
    registry = ModelRegistry()
    
    # Get model
    model = registry.get_model(version)
    model_path = Path(model['path']) / 'model.pth'
    
    if not model_path.exists():
        print(f"❌ Model file not found: {model_path}")
        return False
    
    # Deployment target
    if environment == 'staging':
        target_dir = Path('weights/staging')
        registry.promote_to_staging(version)
    elif environment == 'production':
        target_dir = Path('weights')
        registry.promote_to_production(version)
    else:
        print(f"❌ Invalid environment: {environment}")
        return False
    
    # Create target directory
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / 'best_model.pth'
    
    # Copy model
    shutil.copy(model_path, target_path)
    
    print(f"\n✅ Model {version} deployed to {environment}")
    print(f"   Source: {model_path}")
    print(f"   Target: {target_path}")
    print(f"   Metrics: {model['metrics']}")
    
    # Update backend to use new model
    if environment == 'production':
        print(f"\n🔄 Restart backend server to load new model:")
        print(f"   python backend_server.py")
    
    return True


def rollback(to_version):
    """Rollback to previous version"""
    print(f"\n🔄 Rolling back to {to_version}...")
    return deploy_model(to_version, 'production')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy model')
    parser.add_argument('--version', type=str, required=True, help='Model version')
    parser.add_argument('--env', type=str, default='staging', choices=['staging', 'production'], help='Environment')
    parser.add_argument('--rollback', action='store_true', help='Rollback to version')
    
    args = parser.parse_args()
    
    if args.rollback:
        rollback(args.version)
    else:
        deploy_model(args.version, args.env)
