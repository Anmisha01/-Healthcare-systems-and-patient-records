"""
Patient records management with encryption
All sensitive data is encrypted at rest
"""
import json
import os
from datetime import datetime
from crypto_utils import SymmetricEncryption
import uuid


class PatientRecords:
    """Manages encrypted patient records"""
    
    def __init__(self, records_file='patient_records.json', master_password='changeme'):
        self.records_file = records_file
        self.master_password = master_password
        self.salt_file = records_file + '.salt'
        
        # Load or generate salt
        self.salt = self._load_or_create_salt()
        
        # Derive encryption key using the salt
        self.encryption_key, _ = SymmetricEncryption.derive_key_from_password(
            master_password, 
            self.salt
        )
        
        self.records = self._load_records()
    
    def _load_or_create_salt(self):
        """Load existing salt or create new one"""
        if os.path.exists(self.salt_file):
            # Load existing salt
            try:
                with open(self.salt_file, 'rb') as f:
                    salt = f.read()
                print(f"✓ Loaded existing encryption salt from {self.salt_file}")
                return salt
            except Exception as e:
                print(f"⚠ Error loading salt file: {e}")
                print("  Creating new salt...")
        
        # Create new salt
        _, salt = SymmetricEncryption.derive_key_from_password(self.master_password)
        
        # Save salt for future use
        try:
            with open(self.salt_file, 'wb') as f:
                f.write(salt)
            print(f"✓ Created and saved new encryption salt to {self.salt_file}")
        except Exception as e:
            print(f"⚠ Warning: Could not save salt file: {e}")
        
        return salt
    
    def _load_records(self):
        """Load and decrypt patient records"""
        if not os.path.exists(self.records_file):
            print(f"ℹ No existing patient records file found at {self.records_file}")
            return {}
        
        try:
            with open(self.records_file, 'r') as f:
                encrypted_data = json.load(f)
            
            print(f"📂 Loading {len(encrypted_data)} patient record(s)...")
            
            # Decrypt each record
            records = {}
            failed_count = 0
            for patient_id, encrypted_record in encrypted_data.items():
                try:
                    decrypted = SymmetricEncryption.decrypt(
                        encrypted_record['data'],
                        self.encryption_key
                    )
                    records[patient_id] = json.loads(decrypted)
                except Exception as e:
                    print(f"✗ Failed to decrypt record {patient_id}: {e}")
                    failed_count += 1
            
            success_count = len(records)
            print(f"✓ Successfully loaded {success_count} patient record(s)")
            if failed_count > 0:
                print(f"⚠ Failed to decrypt {failed_count} record(s)")
            
            return records
        except Exception as e:
            print(f"✗ Error loading records file: {e}")
            return {}
    
    def _save_records(self):
        """Encrypt and save patient records"""
        encrypted_data = {}
        
        for patient_id, record in self.records.items():
            # Encrypt the record
            record_json = json.dumps(record)
            encrypted = SymmetricEncryption.encrypt(record_json, self.encryption_key)
            encrypted_data[patient_id] = {
                'data': encrypted,
                'last_updated': datetime.now().isoformat()
            }
        
        with open(self.records_file, 'w') as f:
            json.dump(encrypted_data, f, indent=2)
        
        print(f"💾 Saved {len(self.records)} patient record(s) to {self.records_file}")
    
    def add_patient(self, name, date_of_birth, blood_type, allergies="", medical_history=""):
        """Add a new patient record"""
        patient_id = str(uuid.uuid4())
        
        self.records[patient_id] = {
            'patient_id': patient_id,
            'name': name,
            'date_of_birth': date_of_birth,
            'blood_type': blood_type,
            'allergies': allergies,
            'medical_history': medical_history,
            'created_at': datetime.now().isoformat(),
            'visits': []
        }
        
        self._save_records()
        return patient_id
    
    def get_patient(self, patient_id):
        """Retrieve patient record"""
        return self.records.get(patient_id)
    
    def update_patient(self, patient_id, **kwargs):
        """Update patient record"""
        if patient_id not in self.records:
            return False
        
        for key, value in kwargs.items():
            if key in self.records[patient_id]:
                self.records[patient_id][key] = value
        
        self.records[patient_id]['last_updated'] = datetime.now().isoformat()
        self._save_records()
        return True
    
    def add_visit(self, patient_id, diagnosis, prescription, notes=""):
        """Add a visit record to patient"""
        if patient_id not in self.records:
            return False
        
        visit = {
            'visit_id': str(uuid.uuid4()),
            'date': datetime.now().isoformat(),
            'diagnosis': diagnosis,
            'prescription': prescription,
            'notes': notes
        }
        
        self.records[patient_id]['visits'].append(visit)
        self._save_records()
        return True
    
    def search_patients(self, query):
        """Search patients by name"""
        results = []
        query_lower = query.lower()
        
        for patient_id, record in self.records.items():
            if query_lower in record['name'].lower():
                results.append(record)
        
        return results
    
    def get_all_patients(self):
        """Get all patient records"""
        return list(self.records.values())
    
    def delete_patient(self, patient_id):
        """Delete patient record"""
        if patient_id in self.records:
            del self.records[patient_id]
            self._save_records()
            return True
        return False