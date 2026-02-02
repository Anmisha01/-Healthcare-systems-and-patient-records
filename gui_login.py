from PyQt5 import QtWidgets

class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")

        self.user = QtWidgets.QLineEdit()
        self.pwd = QtWidgets.QLineEdit()
        self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)

        form = QtWidgets.QFormLayout(self)
        form.addRow("Username", self.user)
        form.addRow("Password", self.pwd)

        btn = QtWidgets.QPushButton("Login")
        btn.clicked.connect(self.accept)
        form.addWidget(btn)

    def get_credentials(self):
        if self.exec_() == QtWidgets.QDialog.Accepted:
            return self.user.text().strip(), self.pwd.text().strip()
        return None, None
