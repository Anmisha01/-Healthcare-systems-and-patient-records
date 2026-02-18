"""
Unit tests for patient records management
Tests CRUD operations and encryption
Updated for the final Healthcare System implementation
"""
import unittest
import os
import tempfile
import json
from patient_records import PatientRecords


class TestPatientRecords(unittest.TestCase):
    """Test cases for patient records"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.records = PatientRecords(
            records_file=self.temp_file.name,
            master_password='test_password_123'
        )
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_patient(self):
        """Test adding a new patient"""
        patient_id = self.records.add_patient(
            name="John Doe",
            date_of_birth="1990-01-01",
            blood_type="A+",
            allergies="Penicillin",
            medical_history="None"
        )
        
        self.assertIsNotNone(patient_id)
        self.assertIsInstance(patient_id, str)
        self.assertIn(patient_id, self.records.records)
        
        patient = self.records.get_patient(patient_id)
        self.assertEqual(patient['name'], "John Doe")
        self.assertEqual(patient['blood_type'], "A+")
        self.assertEqual(patient['allergies'], "Penicillin")
    
    def test_add_patient_minimal_info(self):
        """Test adding patient with minimal required information"""
        patient_id = self.records.add_patient(
            name="Jane Smith",
            date_of_birth="1985-05-15",
            blood_type="B-"
        )
        
        self.assertIsNotNone(patient_id)
        patient = self.records.get_patient(patient_id)
        self.assertEqual(patient['name'], "Jane Smith")
        self.assertEqual(patient['allergies'], "")
        self.assertEqual(patient['medical_history'], "")
    
    def test_add_patient_unicode_name(self):
        """Test adding patient with unicode characters in name"""
        patient_id = self.records.add_patient(
            name="José García-Müller",
            date_of_birth="1992-03-20",
            blood_type="O+",
            allergies="",
            medical_history=""
        )
        
        patient = self.records.get_patient(patient_id)
        self.assertEqual(patient['name'], "José García-Müller")
    
    def test_get_patient(self):
        """Test retrieving a patient"""
        patient_id = self.records.add_patient(
            name="Jane Smith",
            date_of_birth="1985-05-15",
            blood_type="B-",
            allergies="None",
            medical_history="Asthma"
        )
        
        patient = self.records.get_patient(patient_id)
        self.assertIsNotNone(patient)
        self.assertEqual(patient['name'], "Jane Smith")
        self.assertEqual(patient['date_of_birth'], "1985-05-15")
        self.assertEqual(patient['blood_type'], "B-")
        self.assertEqual(patient['medical_history'], "Asthma")
        self.assertIn('created_at', patient)
        self.assertIn('visits', patient)
    
    def test_get_nonexistent_patient(self):
        """Test retrieving non-existent patient"""
        patient = self.records.get_patient("non_existent_id_12345")
        self.assertIsNone(patient)
    
    def test_update_patient(self):
        """Test updating patient information"""
        patient_id = self.records.add_patient(
            name="Bob Wilson",
            date_of_birth="1975-12-20",
            blood_type="O+",
            allergies="",
            medical_history=""
        )
        
        success = self.records.update_patient(
            patient_id,
            allergies="Latex",
            medical_history="Diabetes Type 2"
        )
        
        self.assertTrue(success)
        
        patient = self.records.get_patient(patient_id)
        self.assertEqual(patient['allergies'], "Latex")
        self.assertEqual(patient['medical_history'], "Diabetes Type 2")
        self.assertIn('last_updated', patient)
    
    def test_update_patient_name(self):
        """Test updating patient name"""
        patient_id = self.records.add_patient(
            name="Old Name",
            date_of_birth="1980-01-01",
            blood_type="A+"
        )
        
        self.records.update_patient(patient_id, name="New Name")
        patient = self.records.get_patient(patient_id)
        self.assertEqual(patient['name'], "New Name")
    
    def test_update_nonexistent_patient(self):
        """Test updating non-existent patient"""
        success = self.records.update_patient(
            "non_existent_id",
            allergies="Test"
        )
        self.assertFalse(success)
    
    def test_update_invalid_field(self):
        """Test updating with invalid field name"""
        patient_id = self.records.add_patient(
            name="Test Patient",
            date_of_birth="1990-01-01",
            blood_type="AB+"
        )
        
        # Try to update non-existent field
        self.records.update_patient(patient_id, invalid_field="value")
        patient = self.records.get_patient(patient_id)
        self.assertNotIn('invalid_field', patient)
    
    def test_add_visit(self):
        """Test adding a visit to patient record"""
        patient_id = self.records.add_patient(
            name="Alice Brown",
            date_of_birth="1992-03-10",
            blood_type="AB+",
            allergies="",
            medical_history=""
        )
        
        success = self.records.add_visit(
            patient_id,
            diagnosis="Common Cold",
            prescription="Rest and fluids",
            notes="Patient recovering well"
        )
        
        self.assertTrue(success)
        
        patient = self.records.get_patient(patient_id)
        self.assertEqual(len(patient['visits']), 1)
        visit = patient['visits'][0]
        self.assertEqual(visit['diagnosis'], "Common Cold")
        self.assertEqual(visit['prescription'], "Rest and fluids")
        self.assertEqual(visit['notes'], "Patient recovering well")
        self.assertIn('visit_id', visit)
        self.assertIn('date', visit)
    
    def test_add_visit_minimal_info(self):
        """Test adding visit with minimal information"""
        patient_id = self.records.add_patient(
            name="Test Patient",
            date_of_birth="1990-01-01",
            blood_type="O-"
        )
        
        success = self.records.add_visit(
            patient_id,
            diagnosis="Checkup",
            prescription="None"
        )
        
        self.assertTrue(success)
        patient = self.records.get_patient(patient_id)
        self.assertEqual(patient['visits'][0]['notes'], "")
    
    def test_add_multiple_visits(self):
        """Test adding multiple visits"""
        patient_id = self.records.add_patient(
            name="Charlie Davis",
            date_of_birth="1988-07-25",
            blood_type="A-",
            allergies="",
            medical_history=""
        )
        
        self.records.add_visit(patient_id, "Flu", "Tamiflu", "Day 1")
        self.records.add_visit(patient_id, "Follow-up", "Continue medication", "Day 7")
        self.records.add_visit(patient_id, "Final checkup", "Recovered", "Day 14")
        
        patient = self.records.get_patient(patient_id)
        self.assertEqual(len(patient['visits']), 3)
        self.assertEqual(patient['visits'][0]['diagnosis'], "Flu")
        self.assertEqual(patient['visits'][1]['diagnosis'], "Follow-up")
        self.assertEqual(patient['visits'][2]['diagnosis'], "Final checkup")
    
    def test_add_visit_nonexistent_patient(self):
        """Test adding visit to non-existent patient"""
        success = self.records.add_visit(
            "non_existent_id",
            "Test",
            "Test",
            "Test"
        )
        self.assertFalse(success)
    
    def test_search_patients(self):
        """Test searching patients by name"""
        self.records.add_patient("John Smith", "1990-01-01", "A+", "", "")
        self.records.add_patient("Jane Smith", "1985-05-15", "B-", "", "")
        self.records.add_patient("Bob Wilson", "1975-12-20", "O+", "", "")
        self.records.add_patient("Alice Smith-Jones", "1992-03-10", "AB+", "", "")
        
        results = self.records.search_patients("Smith")
        self.assertEqual(len(results), 3)
        
        names = [r['name'] for r in results]
        self.assertIn("John Smith", names)
        self.assertIn("Jane Smith", names)
        self.assertIn("Alice Smith-Jones", names)
    
    def test_search_case_insensitive(self):
        """Test case-insensitive search"""
        self.records.add_patient("Alice JOHNSON", "1992-03-10", "AB+", "", "")
        
        results = self.records.search_patients("johnson")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Alice JOHNSON")
        
        results = self.records.search_patients("JOHNSON")
        self.assertEqual(len(results), 1)
        
        results = self.records.search_patients("JoHnSoN")
        self.assertEqual(len(results), 1)
    
    def test_search_partial_match(self):
        """Test partial name matching"""
        self.records.add_patient("Christopher Anderson", "1980-01-01", "A+", "", "")
        
        results = self.records.search_patients("Chris")
        self.assertEqual(len(results), 1)
        
        results = self.records.search_patients("Anderson")
        self.assertEqual(len(results), 1)
        
        results = self.records.search_patients("ist")
        self.assertEqual(len(results), 1)
    
    def test_search_no_results(self):
        """Test search with no matching results"""
        self.records.add_patient("John Doe", "1990-01-01", "A+", "", "")
        
        results = self.records.search_patients("NonExistentName")
        self.assertEqual(len(results), 0)
    
    def test_get_all_patients(self):
        """Test getting all patients"""
        self.records.add_patient("Patient 1", "1990-01-01", "A+", "", "")
        self.records.add_patient("Patient 2", "1985-05-15", "B-", "", "")
        self.records.add_patient("Patient 3", "1975-12-20", "O+", "", "")
        
        all_patients = self.records.get_all_patients()
        self.assertEqual(len(all_patients), 3)
        self.assertIsInstance(all_patients, list)
    
    def test_get_all_patients_empty(self):
        """Test getting all patients when none exist"""
        all_patients = self.records.get_all_patients()
        self.assertEqual(len(all_patients), 0)
        self.assertIsInstance(all_patients, list)
    
    def test_delete_patient(self):
        """Test deleting a patient"""
        patient_id = self.records.add_patient(
            name="Test Patient",
            date_of_birth="2000-01-01",
            blood_type="O-",
            allergies="",
            medical_history=""
        )
        
        success = self.records.delete_patient(patient_id)
        self.assertTrue(success)
        
        patient = self.records.get_patient(patient_id)
        self.assertIsNone(patient)
        
        all_patients = self.records.get_all_patients()
        self.assertEqual(len(all_patients), 0)
    
    def test_delete_nonexistent_patient(self):
        """Test deleting non-existent patient"""
        success = self.records.delete_patient("non_existent_id")
        self.assertFalse(success)
    
    def test_data_encryption(self):
        """Test that data is encrypted on disk"""
        patient_id = self.records.add_patient(
            name="Confidential Patient",
            date_of_birth="1995-06-15",
            blood_type="B+",
            allergies="Top Secret Allergy",
            medical_history="Classified Information"
        )
        
        # Read raw file content
        with open(self.temp_file.name, 'r') as f:
            raw_data = f.read()
        
        # Ensure sensitive data is not in plaintext
        self.assertNotIn("Confidential Patient", raw_data)
        self.assertNotIn("Top Secret Allergy", raw_data)
        self.assertNotIn("Classified Information", raw_data)
        self.assertNotIn("1995-06-15", raw_data)
    
    def test_data_persistence(self):
        """Test that encrypted data persists correctly"""
        patient_id = self.records.add_patient(
            name="Persistent Patient",
            date_of_birth="1980-09-30",
            blood_type="AB-",
            allergies="None",
            medical_history="Hypertension"
        )
        
        # Add a visit
        self.records.add_visit(patient_id, "Annual Checkup", "Continue meds", "All good")
        
        # Create new instance with same file and password
        new_records = PatientRecords(
            records_file=self.temp_file.name,
            master_password='test_password_123'
        )
        
        patient = new_records.get_patient(patient_id)
        self.assertIsNotNone(patient)
        self.assertEqual(patient['name'], "Persistent Patient")
        self.assertEqual(patient['medical_history'], "Hypertension")
        self.assertEqual(len(patient['visits']), 1)
        self.assertEqual(patient['visits'][0]['diagnosis'], "Annual Checkup")
    
    def test_wrong_password_fails(self):
        """Test that wrong password cannot decrypt data"""
        self.records.add_patient("Test Patient", "1990-01-01", "A+", "", "")
        
        # Try to load with wrong password
        wrong_password_records = PatientRecords(
            records_file=self.temp_file.name,
            master_password='wrong_password_456'
        )
        
        # Should have no records (decryption failed)
        self.assertEqual(len(wrong_password_records.records), 0)
    
    def test_patient_id_uniqueness(self):
        """Test that patient IDs are unique"""
        id1 = self.records.add_patient("Patient 1", "1990-01-01", "A+")
        id2 = self.records.add_patient("Patient 2", "1990-01-01", "A+")
        id3 = self.records.add_patient("Patient 3", "1990-01-01", "A+")
        
        self.assertNotEqual(id1, id2)
        self.assertNotEqual(id2, id3)
        self.assertNotEqual(id1, id3)
    
    def test_visit_id_uniqueness(self):
        """Test that visit IDs are unique"""
        patient_id = self.records.add_patient("Test", "1990-01-01", "A+")
        
        self.records.add_visit(patient_id, "Visit 1", "Rx 1")
        self.records.add_visit(patient_id, "Visit 2", "Rx 2")
        self.records.add_visit(patient_id, "Visit 3", "Rx 3")
        
        patient = self.records.get_patient(patient_id)
        visit_ids = [v['visit_id'] for v in patient['visits']]
        
        self.assertEqual(len(visit_ids), len(set(visit_ids)))  # All unique
    
    def test_large_medical_history(self):
        """Test patient with large medical history"""
        large_history = "Medical history: " + ("Very detailed information. " * 500)
        
        patient_id = self.records.add_patient(
            name="Patient with History",
            date_of_birth="1970-01-01",
            blood_type="O+",
            allergies="",
            medical_history=large_history
        )
        
        patient = self.records.get_patient(patient_id)
        self.assertEqual(patient['medical_history'], large_history)


if __name__ == '__main__':
    unittest.main(verbosity=2)