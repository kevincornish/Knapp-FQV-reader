from PyQt6.QtWidgets import (
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QStyledItemDelegate,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
import pickle


def read_pickle_file(file_path):
    with open(file_path, "rb") as fp:
        return pickle.load(fp)


def write_pickle_file(file_path, data):
    with open(file_path, "wb") as fp:
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


class ColourCell(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(ColourCell, self).initStyleOption(option, index)

        value = int(index.data(Qt.ItemDataRole.DisplayRole))

        if 0 <= value <= 3:
            option.backgroundBrush = QBrush(QColor(0, 150, 0))
        elif 4 <= value <= 6:
            option.backgroundBrush = QBrush(QColor(255, 165, 0))
        elif value >= 7:
            option.backgroundBrush = QBrush(QColor(255, 0, 0))


def setup_results_table(results, result_type):
    results_table = QTableWidget()
    results_table.setRowCount(250)
    results_table.setColumnCount(1)
    results_table.setHorizontalHeaderLabels([result_type])

    containers = {}

    for container in range(1, 251):
        containers[container] = QTableWidgetItem(
            str(results.get(f"container_{container}", 0))
        )
        results_table.setItem(container - 1, 0, containers[container])
        containers[container].setFlags(
            containers[container].flags() & ~Qt.ItemFlag.ItemIsEditable
        )
        if int(containers[container].text()) > 7:
            containers[container].setData(Qt.ItemDataRole.UserRole, "high_value")

    colour_cell = ColourCell()
    results_table.setItemDelegate(colour_cell)

    return results_table, containers
