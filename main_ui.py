"""
Main application interface for Healthcare System
"""
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTableWidget, QTableWidgetItem, QMessageBox, 
                            QTextEdit, QTabWidget, QGroupBox, QFormLayout,
                            QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from patient_records import PatientRecords


class MainWindow(QMainWindow):
    """Main application window"""
    
    logout_requested = None  # Will be set by main app
    
    def __init__(self, session_token, username):
        super().__init__()
        self.session_token = session_token
        self.username = username
        self.patient_records = PatientRecords()
        self.init_ui()
        self.load_patients()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f'Healthcare System - Welcome {self.username}')
        self.setGeometry(100, 100, 1400, 850)  # Larger window
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f7fafc;
            }
            QLabel {
                color: #2d3748;
                font-size: 14px;
            }
            QPushButton {
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
                background-color: #4299e1;
                color: white;
                border: none;
                min-height: 45px;
            }
            QPushButton:hover {
                background-color: #3182ce;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #cbd5e0;
                border-radius: 8px;
                background-color: white;
                font-size: 15px;
                min-height: 45px;
            }
            QTextEdit {
                padding: 12px;
                border: 2px solid #cbd5e0;
                border-radius: 8px;
                background-color: white;
                font-size: 15px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #4299e1;
                border-width: 3px;
            }
            QTableWidget {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #edf2f7;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 15px;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTabWidget::pane {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #edf2f7;
                color: #4a5568;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #2d3748;
            }
            QTabBar::tab:hover {
                background-color: #e2e8f0;
            }
            QGroupBox {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 15px;
                color: #2d3748;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header with larger elements
        header_layout = QHBoxLayout()
        title = QLabel('🏥 Healthcare System')
        title.setFont(QFont('Arial', 26, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        user_label = QLabel(f'👤 Logged in as: {self.username}')
        user_label.setStyleSheet("color: #718096; font-size: 15px; padding-right: 20px;")
        user_label.setFont(QFont('Arial', 14))
        header_layout.addWidget(user_label)
        
        logout_btn = QPushButton('Logout')
        logout_btn.setFixedWidth(120)
        logout_btn.clicked.connect(self.logout)
        header_layout.addWidget(logout_btn)
        
        layout.addLayout(header_layout)
        
        # Tab widget with larger tabs
        tabs = QTabWidget()
        tabs.setFont(QFont('Arial', 14))
        tabs.addTab(self.create_patients_tab(), 'Patients')
        tabs.addTab(self.create_add_patient_tab(), 'Add Patient')
        tabs.addTab(self.create_patient_details_tab(), 'Patient Details')
        
        layout.addWidget(tabs)
        
        central_widget.setLayout(layout)
    
    def create_patients_tab(self):
        """Create patients list tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Search bar with better styling
        search_layout = QHBoxLayout()
        search_label = QLabel('🔍 Search:')
        search_label.setFont(QFont('Arial', 14, QFont.Bold))
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search by patient name...')
        self.search_input.setMinimumHeight(45)
        self.search_input.setFont(QFont('Arial', 14))
        self.search_input.textChanged.connect(self.search_patients)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Patients table with better sizing
        self.patients_table = QTableWidget()
        self.patients_table.setColumnCount(5)
        self.patients_table.setHorizontalHeaderLabels(['ID', 'Name', 'DOB', 'Blood Type', 'Allergies'])
        self.patients_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.patients_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.patients_table.setAlternatingRowColors(True)
        self.patients_table.setFont(QFont('Arial', 13))
        self.patients_table.verticalHeader().setDefaultSectionSize(45)  # Row height
        self.patients_table.doubleClicked.connect(self.view_patient_details)
        
        # Additional table styling
        self.patients_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e2e8f0;
                selection-background-color: #bee3f8;
                selection-color: #2c5282;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:alternate {
                background-color: #f7fafc;
            }
        """)
        
        layout.addWidget(self.patients_table)
        
        # Info label
        info_label = QLabel('💡 Tip: Double-click any patient to view full details')
        info_label.setFont(QFont('Arial', 12))
        info_label.setStyleSheet("color: #718096; padding: 10px;")
        layout.addWidget(info_label)
        
        widget.setLayout(layout)
        return widget
    
    def create_add_patient_tab(self):
        """Create add patient tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        form_group = QGroupBox('Patient Information')
        form_group.setFont(QFont('Arial', 16, QFont.Bold))
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        # Create labels with proper styling
        name_label = QLabel('Name:')
        name_label.setFont(QFont('Arial', 14, QFont.Bold))
        
        dob_label = QLabel('Date of Birth:')
        dob_label.setFont(QFont('Arial', 14, QFont.Bold))
        
        blood_label = QLabel('Blood Type:')
        blood_label.setFont(QFont('Arial', 14, QFont.Bold))
        
        allergies_label = QLabel('Allergies:')
        allergies_label.setFont(QFont('Arial', 14, QFont.Bold))
        
        history_label = QLabel('Medical History:')
        history_label.setFont(QFont('Arial', 14, QFont.Bold))
        
        # Create input fields with better sizing
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter patient full name')
        
        self.dob_input = QLineEdit()
        self.dob_input.setPlaceholderText('YYYY-MM-DD (e.g., 1990-01-15)')
        
        self.blood_type_input = QLineEdit()
        self.blood_type_input.setPlaceholderText('e.g., A+, O-, B+, AB-')
        
        self.allergies_input = QTextEdit()
        self.allergies_input.setPlaceholderText('List any known allergies...')
        self.allergies_input.setMinimumHeight(100)
        self.allergies_input.setMaximumHeight(120)
        
        self.medical_history_input = QTextEdit()
        self.medical_history_input.setPlaceholderText('Enter relevant medical history...')
        self.medical_history_input.setMinimumHeight(150)
        self.medical_history_input.setMaximumHeight(180)
        
        # Add rows with custom labels
        form_layout.addRow(name_label, self.name_input)
        form_layout.addRow(dob_label, self.dob_input)
        form_layout.addRow(blood_label, self.blood_type_input)
        form_layout.addRow(allergies_label, self.allergies_input)
        form_layout.addRow(history_label, self.medical_history_input)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Add button - larger and more prominent
        add_btn = QPushButton('✓ Add Patient')
        add_btn.setFont(QFont('Arial', 16, QFont.Bold))
        add_btn.setMinimumHeight(55)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #48bb78;
                color: white;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #38a169;
            }
        """)
        add_btn.clicked.connect(self.add_patient)
        layout.addWidget(add_btn)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_patient_details_tab(self):
        """Create patient details tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Instructions
        instructions = QLabel('📋 Patient details will appear here when you double-click a patient in the Patients tab')
        instructions.setFont(QFont('Arial', 13))
        instructions.setStyleSheet("color: #718096; padding: 15px; background-color: #edf2f7; border-radius: 8px;")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Details text area with better styling
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setFont(QFont('Courier New', 13))
        self.details_text.setStyleSheet("""
            QTextEdit {
                background-color: #f7fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 20px;
                line-height: 1.6;
            }
        """)
        layout.addWidget(self.details_text)
        
        widget.setLayout(layout)
        return widget
    
    def load_patients(self):
        """Load all patients into table"""
        patients = self.patient_records.get_all_patients()
        self.patients_table.setRowCount(len(patients))
        
        for row, patient in enumerate(patients):
            self.patients_table.setItem(row, 0, QTableWidgetItem(patient['patient_id'][:8]))
            self.patients_table.setItem(row, 1, QTableWidgetItem(patient['name']))
            self.patients_table.setItem(row, 2, QTableWidgetItem(patient['date_of_birth']))
            self.patients_table.setItem(row, 3, QTableWidgetItem(patient['blood_type']))
            self.patients_table.setItem(row, 4, QTableWidgetItem(patient['allergies']))
    
    def search_patients(self):
        """Search patients by name"""
        query = self.search_input.text()
        if not query:
            self.load_patients()
            return
        
        results = self.patient_records.search_patients(query)
        self.patients_table.setRowCount(len(results))
        
        for row, patient in enumerate(results):
            self.patients_table.setItem(row, 0, QTableWidgetItem(patient['patient_id'][:8]))
            self.patients_table.setItem(row, 1, QTableWidgetItem(patient['name']))
            self.patients_table.setItem(row, 2, QTableWidgetItem(patient['date_of_birth']))
            self.patients_table.setItem(row, 3, QTableWidgetItem(patient['blood_type']))
            self.patients_table.setItem(row, 4, QTableWidgetItem(patient['allergies']))
    
    def add_patient(self):
        """Add new patient"""
        name = self.name_input.text().strip()
        dob = self.dob_input.text().strip()
        blood_type = self.blood_type_input.text().strip()
        allergies = self.allergies_input.toPlainText().strip()
        medical_history = self.medical_history_input.toPlainText().strip()
        
        if not name or not dob or not blood_type:
            QMessageBox.warning(self, 'Error', 'Please fill in all required fields')
            return
        
        patient_id = self.patient_records.add_patient(
            name, dob, blood_type, allergies, medical_history
        )
        
        QMessageBox.information(self, 'Success', f'Patient added successfully!\nID: {patient_id[:8]}')
        
        # Clear form
        self.name_input.clear()
        self.dob_input.clear()
        self.blood_type_input.clear()
        self.allergies_input.clear()
        self.medical_history_input.clear()
        
        # Reload table
        self.load_patients()
    
    def view_patient_details(self):
        """View patient details"""
        row = self.patients_table.currentRow()
        if row < 0:
            return
        
        patient_id_short = self.patients_table.item(row, 0).text()
        
        # Find full patient ID
        patients = self.patient_records.get_all_patients()
        patient = None
        for p in patients:
            if p['patient_id'].startswith(patient_id_short):
                patient = p
                break
        
        if patient:
            details = f"""
Patient Details
{'='*50}

Name: {patient['name']}
Date of Birth: {patient['date_of_birth']}
Blood Type: {patient['blood_type']}
Allergies: {patient['allergies']}

Medical History:
{patient['medical_history']}

Visit History:
{'='*50}
"""
            for visit in patient.get('visits', []):
                details += f"""
Date: {visit['date']}
Diagnosis: {visit['diagnosis']}
Prescription: {visit['prescription']}
Notes: {visit['notes']}
{'-'*50}
"""
            
            self.details_text.setPlainText(details)
    
    def logout(self):
        """Logout user"""
        reply = QMessageBox.question(self, 'Logout', 
                                     'Are you sure you want to logout?',
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            print(f"\n✓ User {self.username} logged out")
            
            # Close this window
            self.close()
            
            # Call the app controller's show_login if available
            if MainWindow.logout_requested:
                MainWindow.logout_requested()
            else:
                # Fallback: quit the application
                print("⚠ No logout handler found, quitting application")
                QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # For testing, create a dummy session
    window = MainWindow('test_token', 'test_user')
    window.show()
    sys.exit(app.exec_())