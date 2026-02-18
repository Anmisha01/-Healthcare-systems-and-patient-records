"""
Integration tests for the healthcare system
Tests complete workflows across multiple components
Updated for the final Healthcare System implementation
"""
import unittest
import os
import tempfile
from auth_system import AuthSystem
from patient_records import PatientRecords


class TestIntegration(unittest.TestCase):
    """Integration test cases"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.users_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.users_file.close()
        
        self.records_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.records_file.close()
        
        self.auth = AuthSystem(users_file=self.users_file.name)
        self.records = PatientRecords(
            records_file=self.records_file.name,
            master_password='integration_test_password_2024'
        )
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.users_file.name):
            os.unlink(self.users_file.name)
        if os.path.exists(self.records_file.name):
            os.unlink(self.records_file.name)
    
    def test_complete_user_workflow(self):
        """Test complete workflow: register, login, add patient, add visit, view patient"""
        # Step 1: Register user
        success, msg = self.auth.register_user('dr_jones', 'secure_pass_123', 'doctor')
        self.assertTrue(success)
        self.assertEqual(msg, "User registered successfully")
        
        # Step 2: Login
        session_token, msg = self.auth.authenticate('dr_jones', 'secure_pass_123')
        self.assertIsNotNone(session_token)
        self.assertEqual(msg, "Login successful")
        
        # Step 3: Verify session
        session = self.auth.verify_session(session_token)
        self.assertIsNotNone(session)
        self.assertEqual(session['username'], 'dr_jones')
        self.assertEqual(session['role'], 'doctor')
        
        # Step 4: Add patient (as logged-in user)
        patient_id = self.records.add_patient(
            name="Integration Test Patient",
            date_of_birth="1990-05-15",
            blood_type="O+",
            allergies="None",
            medical_history="Healthy"
        )
        self.assertIsNotNone(patient_id)
        
        # Step 5: Add visit
        success = self.records.add_visit(
            patient_id,
            diagnosis="Annual Checkup",
            prescription="None",
            notes="All vitals normal, patient in good health"
        )
        self.assertTrue(success)
        
        # Step 6: Retrieve and verify patient
        patient = self.records.get_patient(patient_id)
        self.assertEqual(patient['name'], "Integration Test Patient")
        self.assertEqual(patient['blood_type'], "O+")
        self.assertEqual(len(patient['visits']), 1)
        self.assertEqual(patient['visits'][0]['diagnosis'], "Annual Checkup")
        
        # Step 7: Update patient information
        update_success = self.records.update_patient(
            patient_id,
            allergies="Peanuts",
            medical_history="Developed peanut allergy in 2024"
        )
        self.assertTrue(update_success)
        
        # Step 8: Verify update
        updated_patient = self.records.get_patient(patient_id)
        self.assertEqual(updated_patient['allergies'], "Peanuts")
        
        # Step 9: Logout
        logout_success = self.auth.logout(session_token)
        self.assertTrue(logout_success)
        
        # Step 10: Verify session is invalid
        session = self.auth.verify_session(session_token)
        self.assertIsNone(session)
    
    def test_multiple_doctors_multiple_patients(self):
        """Test multiple doctors managing different patients"""
        # Register multiple doctors
        self.auth.register_user('dr_smith', 'password123', 'doctor')
        self.auth.register_user('dr_brown', 'password456', 'doctor')
        self.auth.register_user('nurse_jane', 'password789', 'nurse')
        
        # All login
        token1, _ = self.auth.authenticate('dr_smith', 'password123')
        token2, _ = self.auth.authenticate('dr_brown', 'password456')
        token3, _ = self.auth.authenticate('nurse_jane', 'password789')
        
        self.assertIsNotNone(token1)
        self.assertIsNotNone(token2)
        self.assertIsNotNone(token3)
        
        # Verify different roles
        self.assertEqual(self.auth.verify_session(token1)['role'], 'doctor')
        self.assertEqual(self.auth.verify_session(token2)['role'], 'doctor')
        self.assertEqual(self.auth.verify_session(token3)['role'], 'nurse')
        
        # Add patients
        patient1 = self.records.add_patient("Patient A", "1980-01-01", "A+", "", "")
        patient2 = self.records.add_patient("Patient B", "1985-02-02", "B-", "", "")
        patient3 = self.records.add_patient("Patient C", "1990-03-03", "O+", "", "")
        
        # Add visits for patients
        self.records.add_visit(patient1, "Cold", "Rest", "")
        self.records.add_visit(patient2, "Flu", "Medication", "")
        self.records.add_visit(patient1, "Follow-up", "Recovered", "")
        
        # Verify all patients exist
        self.assertIsNotNone(self.records.get_patient(patient1))
        self.assertIsNotNone(self.records.get_patient(patient2))
        self.assertIsNotNone(self.records.get_patient(patient3))
        
        # Search functionality works
        results = self.records.search_patients("Patient")
        self.assertEqual(len(results), 3)
        
        # Patient 1 should have 2 visits
        p1 = self.records.get_patient(patient1)
        self.assertEqual(len(p1['visits']), 2)
    
    def test_data_security_across_sessions(self):
        """Test that data remains secure across multiple sessions"""
        # Create and save data
        self.auth.register_user('secure_doctor', 'secure_pass_999', 'doctor')
        
        patient_id = self.records.add_patient(
            "Secure Patient",
            "1995-03-20",
            "AB+",
            "Confidential allergies",
            "Confidential history"
        )
        
        self.records.add_visit(
            patient_id,
            "Confidential diagnosis",
            "Confidential prescription",
            "Confidential notes"
        )
        
        # Simulate app restart by creating new instances
        new_auth = AuthSystem(users_file=self.users_file.name)
        new_records = PatientRecords(
            records_file=self.records_file.name,
            master_password='integration_test_password_2024'
        )
        
        # Verify user data is still accessible
        token, msg = new_auth.authenticate('secure_doctor', 'secure_pass_999')
        self.assertIsNotNone(token)
        
        # Verify patient data is still accessible
        patient = new_records.get_patient(patient_id)
        self.assertIsNotNone(patient)
        self.assertEqual(patient['name'], "Secure Patient")
        self.assertEqual(patient['allergies'], "Confidential allergies")
        self.assertEqual(len(patient['visits']), 1)
        
        # Verify encryption by checking raw files
        with open(self.records_file.name, 'r') as f:
            raw_content = f.read()
        
        self.assertNotIn("Secure Patient", raw_content)
        self.assertNotIn("Confidential allergies", raw_content)
        self.assertNotIn("Confidential diagnosis", raw_content)
    
    def test_user_registration_and_patient_creation_workflow(self):
        """Test realistic workflow of user registration followed by patient management"""
        # Day 1: Admin sets up system and creates accounts
        self.auth.register_user('admin', 'admin_password_123', 'admin')
        self.auth.register_user('doctor1', 'doctor_pass_123', 'doctor')
        self.auth.register_user('nurse1', 'nurse_pass_123', 'nurse')
        
        # Day 2: Doctor logs in and adds first patient
        doc_token, _ = self.auth.authenticate('doctor1', 'doctor_pass_123')
        self.assertIsNotNone(doc_token)
        
        patient1 = self.records.add_patient(
            "First Patient Ever",
            "1970-01-01",
            "A+",
            "None",
            "Healthy individual"
        )
        
        # Add initial visit
        self.records.add_visit(
            patient1,
            "New patient registration",
            "None",
            "Baseline vitals recorded"
        )
        
        # Day 3: Nurse logs in and updates patient
        nurse_token, _ = self.auth.authenticate('nurse1', 'nurse_pass_123')
        self.assertIsNotNone(nurse_token)
        
        self.records.add_visit(
            patient1,
            "Follow-up appointment",
            "Vitamins recommended",
            "Patient feeling well"
        )
        
        # Verify complete patient history
        patient = self.records.get_patient(patient1)
        self.assertEqual(len(patient['visits']), 2)
        self.assertEqual(patient['visits'][0]['diagnosis'], "New patient registration")
        self.assertEqual(patient['visits'][1]['diagnosis'], "Follow-up appointment")
    
    def test_concurrent_operations(self):
        """Test concurrent user sessions and patient operations"""
        # Create multiple users
        for i in range(5):
            self.auth.register_user(f'user{i}', f'password{i}', 'doctor')
        
        # All users login simultaneously
        tokens = []
        for i in range(5):
            token, _ = self.auth.authenticate(f'user{i}', f'password{i}')
            tokens.append(token)
            self.assertIsNotNone(token)
        
        # All sessions should be valid
        for token in tokens:
            session = self.auth.verify_session(token)
            self.assertIsNotNone(session)
        
        # All users add patients
        patient_ids = []
        for i in range(5):
            pid = self.records.add_patient(f"Patient {i}", "1990-01-01", "O+")
            patient_ids.append(pid)
        
        # Verify all patients were added
        all_patients = self.records.get_all_patients()
        self.assertEqual(len(all_patients), 5)
        
        # All users logout
        for token in tokens:
            success = self.auth.logout(token)
            self.assertTrue(success)
        
        # All sessions should now be invalid
        for token in tokens:
            session = self.auth.verify_session(token)
            self.assertIsNone(session)
    
    def test_search_and_update_workflow(self):
        """Test searching for patients and updating their records"""
        # Setup: Create user and patients
        self.auth.register_user('doctor', 'password123', 'doctor')
        token, _ = self.auth.authenticate('doctor', 'password123')
        
        # Add multiple patients with similar names
        p1 = self.records.add_patient("John Smith", "1980-01-01", "A+")
        p2 = self.records.add_patient("John Doe", "1985-02-02", "B-")
        p3 = self.records.add_patient("Jane Smith", "1990-03-03", "O+")
        
        # Search for "John"
        results = self.records.search_patients("John")
        self.assertEqual(len(results), 2)
        
        # Search for "Smith"
        results = self.records.search_patients("Smith")
        self.assertEqual(len(results), 2)
        
        # Update one of the Johns
        self.records.update_patient(p1, medical_history="Updated history")
        
        # Search again and verify update
        results = self.records.search_patients("John Smith")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['medical_history'], "Updated history")
    
    def test_delete_workflow(self):
        """Test patient deletion workflow"""
        # Setup
        self.auth.register_user('doctor', 'password123', 'doctor')
        
        # Add patients
        p1 = self.records.add_patient("Patient 1", "1990-01-01", "A+")
        p2 = self.records.add_patient("Patient 2", "1990-01-01", "B-")
        p3 = self.records.add_patient("Patient 3", "1990-01-01", "O+")
        
        # Verify 3 patients
        self.assertEqual(len(self.records.get_all_patients()), 3)
        
        # Delete one patient
        success = self.records.delete_patient(p2)
        self.assertTrue(success)
        
        # Verify 2 patients remain
        self.assertEqual(len(self.records.get_all_patients()), 2)
        
        # Verify deleted patient is gone
        self.assertIsNone(self.records.get_patient(p2))
        
        # Verify other patients still exist
        self.assertIsNotNone(self.records.get_patient(p1))
        self.assertIsNotNone(self.records.get_patient(p3))
    
    def test_session_expiry_workflow(self):
        """Test that expired sessions are properly handled"""
        from datetime import datetime, timedelta
        
        # Register and login
        self.auth.register_user('doctor', 'password123', 'doctor')
        token, _ = self.auth.authenticate('doctor', 'password123')
        
        # Session should be valid initially
        session = self.auth.verify_session(token)
        self.assertIsNotNone(session)
        
        # Manually expire the session
        self.auth.sessions[token]['expires'] = datetime.now() - timedelta(hours=1)
        
        # Session should now be invalid
        session = self.auth.verify_session(token)
        self.assertIsNone(session)
        
        # Session should be removed from sessions dict
        self.assertNotIn(token, self.auth.sessions)


if __name__ == '__main__':
    unittest.main(verbosity=2)