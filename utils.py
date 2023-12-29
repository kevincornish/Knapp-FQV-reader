from PyQt6.QtWidgets import QMessageBox
import pickle

def read_pickle_file(file_path):
    with open(file_path, 'rb') as fp:
        return pickle.load(fp)

def write_pickle_file(file_path, data):
    with open(file_path, 'wb') as fp:
        pickle.dump(data, fp)

def show_confirmation(parent, message):
    confirmation = QMessageBox.question(
        parent,
        "Confirmation",
        message,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No,
    )
    return confirmation == QMessageBox.StandardButton.Yes