import csv
from PyQt6.QtWidgets import (
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QStyledItemDelegate,
    QFileDialog,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
import pickle

ACCEPT_THRESHOLD = 3
GREYZONE_THRESHOLD = 6
REJECT_THRESHOLD = 7


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

        if 0 <= value <= ACCEPT_THRESHOLD:
            option.backgroundBrush = QBrush(QColor(0, 150, 0))
        elif ACCEPT_THRESHOLD < value <= GREYZONE_THRESHOLD:
            option.backgroundBrush = QBrush(QColor(255, 165, 0))
        elif value >= REJECT_THRESHOLD:
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
        if int(containers[container].text()) > REJECT_THRESHOLD:
            containers[container].setData(Qt.ItemDataRole.UserRole, "high_value")

    colour_cell = ColourCell()
    results_table.setItemDelegate(colour_cell)

    return results_table, containers


def export_table_to_csv(table: QTableWidget):
    path, ok = QFileDialog.getSaveFileName(None, "Save CSV", "", "CSV(*.csv)")
    if ok:
        columns = range(table.columnCount())
        header = [table.horizontalHeaderItem(column).text() for column in columns]
        with open(path, "w") as csvfile:
            writer = csv.writer(csvfile, dialect="excel", lineterminator="\n")
            writer.writerow(header)
            for row in range(table.rowCount()):
                writer.writerow(table.item(row, column).text() for column in columns)
