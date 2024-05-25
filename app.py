import sys
import json
from PyQt5 import QtWidgets, QtCore, QtGui

# Define a class to represent each item in the dropdown list
class Item:
    def __init__(self, item_id, name, message):
        self.item_id = item_id
        self.name = name
        self.message = message

    def __str__(self):
        return f"{self.name} (ID: {self.item_id})"

# Define the main application window
class MetroBoardManagerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up window properties
        self.setWindowTitle("Metro Board Manager")
        self.setGeometry(100, 100, 400, 250)
        self.setWindowIcon(QtGui.QIcon('icon.ico')) #https://www.vecteezy.com/free-png/train Train PNGs by Vecteezy

        # Initialize dropdown list and list of items
        self.dropdown = QtWidgets.QComboBox()
        self.items = []

        # Initialize input fields for ID, Name, and Message
        self.id_input = QtWidgets.QLineEdit()
        self.name_input = QtWidgets.QLineEdit()
        self.message_input = QtWidgets.QLineEdit()

        # Load items from JSON file and update dropdown list
        self.load_items_from_json()
        self.update_dropdown()

        # Set up UI elements
        self.init_ui()

    def init_ui(self):
        # Create widgets (labels, input fields, buttons)
        self.create_widgets()

        # Create layout for UI elements
        self.create_layouts()

        # Update visibility of input fields based on item list
        self.update_visibility()

    def create_widgets(self):
        # Create labels for input fields
        self.id_label = QtWidgets.QLabel("ID:")
        self.name_label = QtWidgets.QLabel("Name:")
        self.message_label = QtWidgets.QLabel("Message:")

        # Connect input fields to update method when text changes
        self.id_input.textChanged.connect(self.update_selected_item)
        self.name_input.textChanged.connect(self.update_selected_item)
        self.message_input.textChanged.connect(self.update_selected_item)

        # Create buttons for adding, deleting, and updating the board
        self.add_button = QtWidgets.QPushButton("+")
        self.add_button.setStyleSheet("background-color: green; color: white;")
        self.add_button.setFixedSize(self.add_button.sizeHint().height(), self.add_button.sizeHint().height())
        self.add_button.clicked.connect(self.add_item)

        self.delete_button = QtWidgets.QPushButton("-")
        self.delete_button.setStyleSheet("background-color: red; color: white;")
        self.delete_button.setFixedSize(self.delete_button.sizeHint().height(), self.delete_button.sizeHint().height())
        self.delete_button.clicked.connect(self.delete_item)

        self.update_board_button = QtWidgets.QPushButton("Update Board")
        self.update_board_button.clicked.connect(self.update_board)

        # Connect dropdown list to update fields on selection change
        self.dropdown.currentIndexChanged.connect(self.update_fields_on_selection)

    def create_layouts(self):
        # Create layout for buttons (add, delete)
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.delete_button)

        # Create layout for dropdown list and buttons
        dropdown_layout = QtWidgets.QHBoxLayout()
        dropdown_layout.addWidget(self.dropdown)
        dropdown_layout.addLayout(buttons_layout)

        # Create vertical layout for all UI elements
        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addLayout(dropdown_layout)
        v_layout.addWidget(self.id_label)
        v_layout.addWidget(self.id_input)
        v_layout.addWidget(self.name_label)
        v_layout.addWidget(self.name_input)
        v_layout.addWidget(self.message_label)
        v_layout.addWidget(self.message_input)
        v_layout.addSpacing(10)
        v_layout.addWidget(self.update_board_button, alignment=QtCore.Qt.AlignCenter)

        # Set layout for central widget
        container = QtWidgets.QWidget()
        container.setLayout(v_layout)
        self.setCentralWidget(container)

    def add_item(self):
        # Add a new item to the list and update UI
        item_id = self.id_input.text()
        name = self.name_input.text()
        message = self.message_input.text()
        new_item = Item(item_id, name, message)
        self.items.append(new_item)
        self.save_items_to_json()
        self.update_dropdown()
        self.clear_input_fields()
        self.update_visibility()

    def delete_item(self):
        # Delete selected item from the list and update UI
        index = self.dropdown.currentIndex()
        if index >= 0:
            del self.items[index]
            self.save_items_to_json()
            self.update_dropdown()
            self.update_visibility()

    def display_selected_item(self, index):
        # Display selected item's details in input fields
        if index >= 0:
            item = self.items[index]
            self.id_input.setText(item.item_id)
            self.name_input.setText(item.name)
            self.message_input.setText(item.message)
        else:
            self.clear_input_fields()

    def update_selected_item(self):
        # Update selected item's details when input fields change
        if self.ignore_updates:  # Check if updates should be ignored
            return

        index = self.dropdown.currentIndex()
        if index >= 0:
            item = self.items[index]
            item.item_id = self.id_input.text()
            item.name = self.name_input.text()
            item.message = self.message_input.text()
            self.dropdown.setItemText(index, str(item))
            self.save_items_to_json()

    def clear_input_fields(self):
        # Clear input fields
        self.id_input.clear()
        self.name_input.clear()
        self.message_input.clear()

    def update_board(self):
        pass

    def save_items_to_json(self):
        # Save items to JSON file
        data = {}
        for item in self.items:
            data[item.item_id] = {"name": item.name, "message": item.message}
        with open("settings.json", "w") as f:
            json.dump(data, f)

    def load_items_from_json(self):
        # Load items from JSON file
        try:
            with open("settings.json", "r") as f:
                data = json.load(f)
                for item_id, values in data.items():
                    self.items.append(Item(item_id, values["name"], values["message"]))
            if self.items:  # Check if there are items in the list
                self.display_selected_item(0)  # Display data of the first item
        except FileNotFoundError:
            pass

    def update_dropdown(self):
        # Update dropdown list with items
        self.dropdown.clear()
        for item in self.items:
            self.dropdown.addItem(str(item))

    def update_visibility(self):
        # Update visibility of input fields based on item list
        if not self.items:
            self.id_label.hide()
            self.id_input.hide()
            self.name_label.hide()
            self.name_input.hide()
            self.message_label.hide()
            self.message_input.hide()
        else:
            self.id_label.show()
            self.id_input.show()
            self.name_label.show()
            self.name_input.show()
            self.message_label.show()
            self.message_input.show()

    def update_fields_on_selection(self, index):
        # Update input fields when selection changes
        self.ignore_updates = True  # Ignore updates temporarily
        self.display_selected_item(index)
        self.ignore_updates = False  # Resume updates

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MetroBoardManagerApp()
    window.show()
    sys.exit(app.exec_())
