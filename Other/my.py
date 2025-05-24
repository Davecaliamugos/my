from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QComboBox, 
                            QTextEdit, QWidget, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

class ALUSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ALU Simulator")
        self.setFixedSize(500, 700)
        
        # Set dark theme
        self.set_dark_theme()
        
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("ALU BASIC SIMULATOR")
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #4FC3F7;")
        main_layout.addWidget(title)
        
        # Input fields
        input_layout = QHBoxLayout()
        self.input_a = QLineEdit()
        self.input_a.setPlaceholderText("Enter Binary Number")
        self.input_b = QLineEdit()
        self.input_b.setPlaceholderText("Enter Binary Number")
        input_layout.addWidget(self.input_a)
        input_layout.addWidget(self.input_b)
        main_layout.addLayout(input_layout)
        
        # Operation selection
        op_layout = QHBoxLayout()
        op_layout.addWidget(QLabel("Select Operation:"))
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["ADD", "SUB", "AND", "OR"])
        op_layout.addWidget(self.operation_combo)
        main_layout.addLayout(op_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        execute_btn = QPushButton("Execute")
        execute_btn.setStyleSheet("background-color: #00BFA5; color: white; font-weight: bold;")
        execute_btn.clicked.connect(self.execute_operation)
        reset_btn = QPushButton("Reset")
        reset_btn.setStyleSheet("background-color: #FF7043; color: white; font-weight: bold;")
        reset_btn.clicked.connect(self.reset_fields)
        btn_layout.addWidget(execute_btn)
        btn_layout.addWidget(reset_btn)
        main_layout.addLayout(btn_layout)
        
        # Result field
        main_layout.addWidget(QLabel("Result:"))
        self.result_field = QLineEdit()
        self.result_field.setReadOnly(True)
        main_layout.addWidget(self.result_field)
        
        # Explanation
        main_layout.addWidget(QLabel("Step-by-step Explanation:"))
        
        # Scrollable explanation area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.explanation_text = QTextEdit()
        self.explanation_text.setReadOnly(True)
        scroll.setWidget(self.explanation_text)
        main_layout.addWidget(scroll)
        
        # Set styles
        self.set_styles()
    
    def set_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(30, 35, 45))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 30, 40))
        dark_palette.setColor(QPalette.AlternateBase, QColor(35, 40, 50))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(50, 55, 65))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(dark_palette)
    
    def set_styles(self):
        self.setStyleSheet("""
            QLineEdit {
                background-color: #1E1E2D;
                color: #E0E0E0;
                border: 1px solid #444;
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox {
                background-color: #1E1E2D;
                color: #E0E0E0;
                border: 1px solid #444;
                padding: 5px;
                border-radius: 3px;
            }
            QTextEdit {
                background-color: #1E1E2D;
                color: #E0E0E0;
                border: 1px solid #444;
                padding: 5px;
            }
            QScrollArea {
                border: 1px solid #444;
            }
        """)
    
    def execute_operation(self):
        a = self.input_a.text().strip()
        b = self.input_b.text().strip()
        op = self.operation_combo.currentText()

        if not (self.is_valid_binary(a) and self.is_valid_binary(b)):
            self.result_field.setText("Error")
            self.explanation_text.setPlainText("Please enter valid binary numbers (containing only 0 and 1).")
            return

        max_len = max(len(a), len(b))
        a = a.zfill(max_len)
        b = b.zfill(max_len)

        try:
            explanation = ""
            result = ""

            if op == 'ADD':
                explanation, result = self.binary_add(a, b)
            elif op == 'SUB':
                explanation, result = self.binary_sub(a, b)
            elif op == 'AND':
                explanation, result = self.binary_and(a, b)
            elif op == 'OR':
                explanation, result = self.binary_or(a, b)
            else:
                self.result_field.setText("Error")
                self.explanation_text.setPlainText("Unknown operation.")
                return

            self.result_field.setText(result)
            self.explanation_text.setPlainText(explanation)

        except Exception as e:
            self.result_field.setText("Error")
            self.explanation_text.setPlainText(str(e))
    
    def is_valid_binary(self, s):
        return all(c in '01' for c in s) and s != ''
    
    def binary_add(self, a, b):
        explanation = f"Adding {a} + {b}\n\n"
        carry = 0
        result_bits = []
        explanation += "Bit-by-bit addition from right to left:\n"
        for i in reversed(range(len(a))):
            bit_a = int(a[i])
            bit_b = int(b[i])
            total = bit_a + bit_b + carry
            result_bit = total % 2
            prev_carry = carry
            carry = total // 2
            explanation += f"Bit {i}: {bit_a} + {bit_b} + carry {prev_carry} = {total} -> Result bit = {result_bit}, Next carry = {carry}\n"
            result_bits.insert(0, str(result_bit))
        if carry:
            explanation += f"Final carry = {carry}\n"
            result_bits.insert(0, '1')
        result = ''.join(result_bits)
        explanation += f"\nFinal binary result: {result}"
        return explanation, result
    
    def binary_sub(self, a, b):
        int_a = int(a, 2)
        int_b = int(b, 2)
        if int_a < int_b:
            return "Error: Subtraction results in negative number (not supported).", ""
        explanation = f"Subtracting {b} from {a}\n\n"

        def twos_complement(bin_str):
            inverted = ''.join('1' if x=='0' else '0' for x in bin_str)
            # Add 1
            carry = 1
            result = []
            for bit in reversed(inverted):
                r = int(bit) + carry
                result_bit = r % 2
                carry = r // 2
                result.insert(0, str(result_bit))
            return ''.join(result)

        explanation += f"Step 1: Find two's complement of {b}:\n"
        twos_b = twos_complement(b.zfill(len(a)))
        explanation += f"  Invert bits and add 1: {twos_b}\n\n"
        explanation += f"Step 2: Add {a} and two's complement of {b}:\n"
        add_exp, add_res = self.binary_add(a, twos_b)
        explanation += add_exp + "\n\n"
        if len(add_res) > len(a):
            add_res = add_res[1:]
            explanation += "Discard final carry (overflow) bit.\n"
        explanation += f"Result is {add_res} (Decimal {int(add_res, 2)})"
        return explanation, add_res
    
    def binary_and(self, a, b):
        explanation = f"Bitwise AND on {a} and {b}:\n\n"
        result_bits = []
        for i in range(len(a)):
            bit_a = a[i]
            bit_b = b[i]
            res_bit = '1' if bit_a == '1' and bit_b == '1' else '0'
            explanation += f"Bit {i}: {bit_a} AND {bit_b} = {res_bit}\n"
            result_bits.append(res_bit)
        result = ''.join(result_bits)
        explanation += f"\nResult: {result}"
        return explanation, result
    
    def binary_or(self, a, b):
        explanation = f"Bitwise OR on {a} and {b}:\n\n"
        result_bits = []
        for i in range(len(a)):
            bit_a = a[i]
            bit_b = b[i]
            res_bit = '1' if bit_a == '1' or bit_b == '1' else '0'
            explanation += f"Bit {i}: {bit_a} OR {bit_b} = {res_bit}\n"
            result_bits.append(res_bit)
        result = ''.join(result_bits)
        explanation += f"\nResult: {result}"
        return explanation, result
    
    def reset_fields(self):
        self.input_a.clear()
        self.input_b.clear()
        self.result_field.clear()
        self.explanation_text.clear()

if __name__ == "_main_":
    app = QApplication([])
    window = ALUSimulator()
    window.show()
    app.exec_()