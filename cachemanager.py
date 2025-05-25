from typing import Optional, Dict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """Class responsible for managing the cache of the pool scheduling engine"""
    
    def __init__(self, ttl: int = 3600):
        self.cache = {}
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[Dict]:
        """Get a value from the cache if it exists and is not expired"""
        if key not in self.cache:
            return None
            
        cache_entry = self.cache[key]
        if datetime.now() - cache_entry['timestamp'] > timedelta(seconds=self.ttl):
            del self.cache[key]
            return None
            
        return cache_entry['data']
    
    def set(self, key: str, value: Dict) -> None:
        """Set a value in the cache with current timestamp"""
        self.cache[key] = {
            'data': value,
            'timestamp': datetime.now()
        }
    
    def clear_expired(self) -> None:
        """Clear all expired entries from the cache"""
        current_time = datetime.now()
        expired_keys = [
            key for key, entry in self.cache.items()
            if current_time - entry['timestamp'] > timedelta(seconds=self.ttl)
        ]
        for key in expired_keys:
            del self.cache[key]

    def clear_patient_cache(self, patient_id: str) -> None:
        """Clear all cache entries related to a specific patient
        
        Args:
            patient_id (str): The ID of the patient whose cache should be cleared
        """
        # Find all keys that contain the patient ID
        patient_keys = [
            key for key in self.cache.keys()
            if patient_id in key
        ]
        
        # Remove all found keys
        for key in patient_keys:
            del self.cache[key]
            
        logger.info(f"Cleared cache for patient {patient_id}")