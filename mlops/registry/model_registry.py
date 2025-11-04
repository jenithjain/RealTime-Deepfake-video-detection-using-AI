"""
Model Registry for MLOps
Manages model versions, metadata, and deployment
"""

import json
import shutil
from pathlib import Path
from datetime import datetime


class ModelRegistry:
    """Manage model versions and deployment"""
    
    def __init__(self, registry_dir='mlops/registry'):
        self.registry_dir = Path(registry_dir)
        self.models_dir = self.registry_dir / 'models'
        self.metadata_file = self.registry_dir / 'registry.json'
        
        # Create directories
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        # Load registry
        self.registry = self._load_registry()
    
    def _load_registry(self):
        """Load model registry"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {
            'models': [],
            'production_version': None,
            'staging_version': None
        }
    
    def _save_registry(self):
        """Save model registry"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def register_model(self, version, metrics, description=''):
        """
        Register a new model version
        
        Args:
            version: Version string (e.g., 'v1.0.0')
            metrics: Dict of metrics
            description: Optional description
        """
        model_path = self.models_dir / version
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model directory not found: {model_path}")
        
        # Create metadata
        metadata = {
            'version': version,
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'description': description,
            'status': 'registered',
            'path': str(model_path)
        }
        
        # Add to registry
        self.registry['models'].append(metadata)
        self._save_registry()
        
        print(f"✅ Model {version} registered")
        print(f"   Metrics: {metrics}")
        
        return metadata
    
    def list_models(self):
        """List all registered models"""
        return self.registry['models']
    
    def get_model(self, version):
        """Get model metadata by version"""
        for model in self.registry['models']:
            if model['version'] == version:
                return model
        raise ValueError(f"Model {version} not found")
    
    def promote_to_staging(self, version):
        """Promote model to staging"""
        model = self.get_model(version)
        
        old_staging = self.registry.get('staging_version')
        self.registry['staging_version'] = version
        
        # Update status
        for m in self.registry['models']:
            if m['version'] == version:
                m['status'] = 'staging'
            elif m['version'] == old_staging:
                m['status'] = 'registered'
        
        self._save_registry()
        print(f"✅ Model {version} promoted to staging")
    
    def promote_to_production(self, version):
        """Promote model to production"""
        model = self.get_model(version)
        
        old_production = self.registry.get('production_version')
        self.registry['production_version'] = version
        
        # Update status
        for m in self.registry['models']:
            if m['version'] == version:
                m['status'] = 'production'
            elif m['version'] == old_production:
                m['status'] = 'archived'
        
        self._save_registry()
        print(f"✅ Model {version} promoted to production")
        if old_production:
            print(f"   Previous version {old_production} archived")
    
    def compare_models(self, version1, version2):
        """Compare two model versions"""
        model1 = self.get_model(version1)
        model2 = self.get_model(version2)
        
        print(f"\n📊 Comparing {version1} vs {version2}:")
        print(f"\n{version1}:")
        for metric, value in model1['metrics'].items():
            print(f"  {metric}: {value}")
        
        print(f"\n{version2}:")
        for metric, value in model2['metrics'].items():
            print(f"  {metric}: {value}")
            
            # Calculate improvement
            if metric in model1['metrics']:
                diff = value - model1['metrics'][metric]
                pct = (diff / model1['metrics'][metric] * 100) if model1['metrics'][metric] > 0 else 0
                print(f"    Improvement: {diff:+.4f} ({pct:+.2f}%)")
    
    def get_production_model(self):
        """Get current production model"""
        version = self.registry.get('production_version')
        if not version:
            raise ValueError("No production model set")
        return self.get_model(version)


if __name__ == '__main__':
    registry = ModelRegistry()
    
    print("📋 Model Registry")
    print(f"Production: {registry.registry.get('production_version', 'None')}")
    print(f"Staging: {registry.registry.get('staging_version', 'None')}")
    print(f"\nRegistered models: {len(registry.list_models())}")
