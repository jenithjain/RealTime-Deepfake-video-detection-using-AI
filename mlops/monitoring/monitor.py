"""
Production Monitoring for MLOps
Tracks model performance, predictions, and alerts
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


class ProductionMonitor:
    """Monitor model performance in production"""
    
    def __init__(self, log_dir='mlops/monitoring/logs'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.predictions_file = self.log_dir / 'predictions.jsonl'
        self.metrics_file = self.log_dir / 'metrics.json'
        self.alerts_file = self.log_dir / 'alerts.json'
        
        self.metrics = self._load_metrics()
    
    def _load_metrics(self):
        """Load monitoring metrics"""
        if self.metrics_file.exists():
            with open(self.metrics_file, 'r') as f:
                return json.load(f)
        return {
            'total_predictions': 0,
            'fake_count': 0,
            'real_count': 0,
            'avg_confidence': 0.0,
            'avg_latency_ms': 0.0,
            'errors': 0,
            'last_updated': None
        }
    
    def _save_metrics(self):
        """Save monitoring metrics"""
        self.metrics['last_updated'] = datetime.now().isoformat()
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def log_prediction(self, prediction_data):
        """
        Log a prediction
        
        Args:
            prediction_data: Dict with:
                - prediction: 'fake' or 'real'
                - confidence: float
                - latency_ms: float
                - model_version: str
                - error: str (optional)
        """
        prediction_data['timestamp'] = datetime.now().isoformat()
        
        # Append to log
        with open(self.predictions_file, 'a') as f:
            f.write(json.dumps(prediction_data) + '\n')
        
        # Update metrics
        self.metrics['total_predictions'] += 1
        
        if 'error' in prediction_data:
            self.metrics['errors'] += 1
        else:
            if prediction_data['prediction'] == 'fake':
                self.metrics['fake_count'] += 1
            else:
                self.metrics['real_count'] += 1
            
            # Update averages
            total = self.metrics['total_predictions']
            self.metrics['avg_confidence'] = (
                (self.metrics['avg_confidence'] * (total - 1) + prediction_data['confidence']) / total
            )
            self.metrics['avg_latency_ms'] = (
                (self.metrics['avg_latency_ms'] * (total - 1) + prediction_data['latency_ms']) / total
            )
        
        self._save_metrics()
    
    def get_metrics(self):
        """Get current metrics"""
        return self.metrics
    
    def get_recent_predictions(self, hours=24):
        """Get predictions from last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        predictions = []
        
        if self.predictions_file.exists():
            with open(self.predictions_file, 'r') as f:
                for line in f:
                    pred = json.loads(line)
                    pred_time = datetime.fromisoformat(pred['timestamp'])
                    if pred_time >= cutoff:
                        predictions.append(pred)
        
        return predictions
    
    def check_alerts(self):
        """Check for alert conditions"""
        alerts = []
        
        # Check error rate
        if self.metrics['total_predictions'] > 0:
            error_rate = self.metrics['errors'] / self.metrics['total_predictions']
            if error_rate > 0.01:  # > 1%
                alerts.append({
                    'type': 'high_error_rate',
                    'severity': 'warning',
                    'message': f"Error rate: {error_rate*100:.2f}%",
                    'timestamp': datetime.now().isoformat()
                })
        
        # Check latency
        if self.metrics['avg_latency_ms'] > 500:
            alerts.append({
                'type': 'high_latency',
                'severity': 'warning',
                'message': f"Average latency: {self.metrics['avg_latency_ms']:.2f}ms",
                'timestamp': datetime.now().isoformat()
            })
        
        # Save alerts
        if alerts:
            with open(self.alerts_file, 'w') as f:
                json.dump(alerts, f, indent=2)
        
        return alerts
    
    def generate_report(self):
        """Generate monitoring report"""
        print("\n" + "="*60)
        print("📊 PRODUCTION MONITORING REPORT")
        print("="*60)
        
        print(f"\n📈 Overall Metrics:")
        print(f"  Total Predictions: {self.metrics['total_predictions']}")
        print(f"  Fake Detected: {self.metrics['fake_count']}")
        print(f"  Real Detected: {self.metrics['real_count']}")
        print(f"  Average Confidence: {self.metrics['avg_confidence']:.2%}")
        print(f"  Average Latency: {self.metrics['avg_latency_ms']:.2f}ms")
        print(f"  Errors: {self.metrics['errors']}")
        
        # Recent predictions
        recent = self.get_recent_predictions(hours=24)
        print(f"\n📊 Last 24 Hours:")
        print(f"  Predictions: {len(recent)}")
        
        if recent:
            fake_24h = sum(1 for p in recent if p.get('prediction') == 'fake')
            print(f"  Fake: {fake_24h} ({fake_24h/len(recent)*100:.1f}%)")
            print(f"  Real: {len(recent)-fake_24h} ({(len(recent)-fake_24h)/len(recent)*100:.1f}%)")
        
        # Alerts
        alerts = self.check_alerts()
        if alerts:
            print(f"\n🚨 Active Alerts: {len(alerts)}")
            for alert in alerts:
                print(f"  - [{alert['severity'].upper()}] {alert['message']}")
        else:
            print(f"\n✅ No active alerts")
        
        print("\n" + "="*60)


if __name__ == '__main__':
    monitor = ProductionMonitor()
    monitor.generate_report()
