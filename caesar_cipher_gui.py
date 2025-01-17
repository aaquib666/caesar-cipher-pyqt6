import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QClipboard
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette

# Function to handle Caesar cipher
def caesar_cipher(text, shift, decrypt=False):
    result = ""
    if decrypt:
        shift = -shift
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                shifted_char = chr((ord(char) - ord('a') + shift_amount) % 26 + ord('a'))
            else:
                shifted_char = chr((ord(char) - ord('A') + shift_amount) % 26 + ord('A'))
            result += shifted_char
        else:
            result += char
    return result


# Main Window
class CaesarCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Caesar Cipher GUI")
        self.setGeometry(200, 200, 600, 400)

        self.is_dark_mode = self.detect_system_theme()  # Start with system theme
        self.initUI()

    def detect_system_theme(self):
        """Detect system's current theme (light or dark)."""
        system_theme = QApplication.palette().color(QPalette.ColorRole.Window).lightness()
        return system_theme < 128  # If the lightness is low, it's dark mode; otherwise, it's light mode.

    def initUI(self):
        # Define Font
        self.font = QFont("Sans-serif", 10)

        # Widgets
        self.input_label = QLabel("Input Text:")
        self.input_label.setFont(self.font)
        self.input_text = QTextEdit()
        self.input_text.setFont(self.font)

        self.shift_label = QLabel("Shift Amount:")
        self.shift_label.setFont(self.font)
        self.shift_input = QLineEdit()
        self.shift_input.setPlaceholderText("Enter Shift (ex: 3)")
        self.shift_input.setFont(self.font)

        self.operation_label = QLabel("Operation:")
        self.operation_label.setFont(self.font)
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["Encrypt", "Decrypt"])
        self.operation_combo.setFont(self.font)

        self.perform_button = QPushButton("Perform")
        self.perform_button.setFont(self.font)
        self.perform_button.clicked.connect(self.perform_operation)

        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.setFont(self.font)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        self.output_label = QLabel("Output Text:")
        self.output_label.setFont(self.font)
        self.output_text = QTextEdit()
        self.output_text.setFont(self.font)
        self.output_text.setReadOnly(True)

        self.toggle_button = QPushButton("Toggle Dark Mode")
        self.toggle_button.setFont(self.font)
        self.toggle_button.clicked.connect(self.toggle_dark_mode)

        # Apply initial stylesheets
        self.apply_stylesheets()

        # Layouts
        main_layout = QVBoxLayout()

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_text)

        shift_layout = QHBoxLayout()
        shift_layout.addWidget(self.shift_label)
        shift_layout.addWidget(self.shift_input)

        operation_layout = QHBoxLayout()
        operation_layout.addWidget(self.operation_label)
        operation_layout.addWidget(self.operation_combo)

        output_layout = QVBoxLayout()
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_text)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.perform_button)
        button_layout.addWidget(self.copy_button)

        toggle_layout = QHBoxLayout()
        toggle_layout.addWidget(self.toggle_button)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(shift_layout)
        main_layout.addLayout(operation_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(toggle_layout)

        # Central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def apply_stylesheets(self):
        if self.is_dark_mode:
            self.setStyleSheet("""
                background-color: #2e2e2e;
                color: white;
            """)
            self.input_text.setStyleSheet("""
                background-color: #3c3c3c;
                color: white;
                border: 2px solid #4a8fe7;
                padding: 5px;
            """)
            self.shift_input.setStyleSheet("""
                background-color: #3c3c3c;
                color: white;
                border: 2px solid #4a8fe7;
                padding: 5px;
            """)
            self.output_text.setStyleSheet("""
                background-color: #3c3c3c;
                color: white;
                border: 2px solid #4a8fe7;
                padding: 5px;
            """)
            button_style = """
                QPushButton {
                    background-color: #5c7aff;
                    color: white;
                    border: none;
                    padding: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #44e5e7;
                }
            """
            self.toggle_button.setText("Toggle Light Mode")
        else:
            self.setStyleSheet("""
                background-color: #f0f0f0;
                color: black;
            """)
            self.input_text.setStyleSheet("""
                background-color: #ffffff;
                color: black;
                border: 2px solid #4a8fe7;
                padding: 5px;
            """)
            self.shift_input.setStyleSheet("""
                background-color: #ffffff;
                color: black;
                border: 2px solid #4a8fe7;
                padding: 5px;
            """)
            self.output_text.setStyleSheet("""
                background-color: #ffffff;
                color: black;
                border: 2px solid #4a8fe7;
                padding: 5px;
            """)
            button_style = """
                QPushButton {
                    background-color: #5c7aff;
                    color: black;
                    border: none;
                    padding: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #44e5e7;
                }
            """
            self.toggle_button.setText("Toggle Dark Mode")

        self.perform_button.setStyleSheet(button_style)
        self.copy_button.setStyleSheet(button_style)
        self.toggle_button.setStyleSheet(button_style)

    def perform_operation(self):
        # Get input data
        text = self.input_text.toPlainText().strip()
        shift = self.shift_input.text().strip()
        operation = self.operation_combo.currentText().lower()

        # Validate inputs
        if not text:
            QMessageBox.warning(self, "Input Error", "Please enter some text.")
            return

        if not shift.isdigit():
            QMessageBox.warning(self, "Input Error", "Shift must be a valid number.")
            return

        shift = int(shift)
        if operation == "encrypt":
            result = caesar_cipher(text, shift)
        elif operation == "decrypt":
            result = caesar_cipher(text, shift, decrypt=True)
        else:
            QMessageBox.warning(self, "Operation Error", "Invalid operation selected.")
            return

        # Display the result
        self.output_text.setPlainText(result)

    def copy_to_clipboard(self):
        # Copy output text to clipboard
        clipboard = QApplication.clipboard()
        result = self.output_text.toPlainText()
        if result.strip():
            clipboard.setText(result)
            QMessageBox.information(self, "Copied", "Output text copied to clipboard.")
        else:
            QMessageBox.warning(self, "Copy Error", "No output text to copy.")

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_stylesheets()


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CaesarCipherApp()
    main_window.show()
    sys.exit(app.exec())