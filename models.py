from datetime import datetime
from config import db

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float)
    pressure = db.Column(db.Float)
    flow_rate = db.Column(db.Float)

    def to_dict(self):
        return {
            "timestamp": self.timestamp.strftime("%H:%M:%S"),
            "temperature": self.temperature,
            "pressure": self.pressure,
            "flow_rate": self.flow_rate,
        }
