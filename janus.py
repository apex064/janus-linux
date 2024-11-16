import sys
import subprocess
import requests
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer

class JanusActivator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("APEX A12 activator")
        self.setGeometry(600, 300,600,300)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.sn_label = QLabel("Serial Number: Loading...")
        self.device_label = QLabel("Device Name: Loading...")
        self.ios_label = QLabel("iOS Version: Loading...")
        self.activation_status_label = QLabel("Activation Status: Not Checked")

        self.activate_button = QPushButton("Activate")
        self.activate_button.setEnabled(False)
        self.activate_button.clicked.connect(self.start_activation)

        self.layout.addWidget(self.sn_label)
        self.layout.addWidget(self.device_label)
        self.layout.addWidget(self.ios_label)
        self.layout.addWidget(self.activation_status_label)

        # Spacer for better layout
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)

        self.layout.addWidget(self.activate_button)
        self.setLayout(self.layout)

        # Show device details first
        self.show_device_info()
        
        # Start checking SN in the background after device details are shown
        QTimer.singleShot(2000, self.check_sn_in_background)

    def show_device_info(self):
        serial_number = self.execute_command("ideviceinfo", "-k", "SerialNumber")
        device_name = self.execute_command("ideviceinfo", "-k", "DeviceName")
        ios_version = self.execute_command("ideviceinfo", "-k", "ProductVersion")

        self.sn_label.setText(f"Serial Number: {serial_number or 'Unknown'}")
        self.device_label.setText(f"Device Name: {device_name or 'Unknown'}")
        self.ios_label.setText(f"iOS Version: {ios_version or 'Unknown'}")

    def check_sn_in_background(self):
        serial_number = self.execute_command("ideviceinfo", "-k", "SerialNumber")

        if not serial_number:
            self.show_popup("Error", "Device not connected or unable to retrieve details.")
            sys.exit()

        url = f"https://a12janusunion.cloud/J12A/tentaAE/A12BChecker.php?sn={serial_number}"
        response = requests.get(url).text.strip()

        if response == "authorized":
            self.sn_label.setText(f"Serial Number: {serial_number}")
            self.activate_button.setEnabled(True)
        else:
            self.sn_label.setText("Serial Number: Unauthorized Device")
            self.show_popup("Error", "Unauthorized device. Please contact support.")
            self.activate_button.setEnabled(False)

    def execute_command(self, command, *args):
        try:
            process = subprocess.Popen([command] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()
            return output.decode('utf-8').strip()
        except Exception as e:
            return ""

    def start_activation(self):
        self.show_popup("Activation", "Starting Activation process! Make sure to connect your device.")
        self.execute_command("ideviceactivation", "activate", "-s", "https://a12janusunion.cloud/J12A/monstrinho.php")
        
        # Adding 10-20 seconds delay before checking activation state
        time.sleep(15)
    
        activation_state = self.execute_command("ideviceinfo", "-k", "ActivationState")
        if activation_state == "FactoryActivated":
            self.show_popup("Success", "Activation successful!")
        else:
            self.show_popup("Failure", "Activation failed! Try again.")

    def show_popup(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

def main():
    app = QApplication(sys.argv)
    QMessageBox.information(None, "Welcome", "Made by apex, THIS IS a tethered tool")
    window = JanusActivator()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
