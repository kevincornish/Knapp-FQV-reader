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
from constants import ACCEPT_THRESHOLD, GREYZONE_THRESHOLD, REJECT_THRESHOLD


def read_pickle_file(file_path):
    """
    Read data from a pickle file.

    Parameters:
        file_path (str): The path to the pickle file.

    Returns:
        object: The data read from the pickle file.
    """
    with open(file_path, "rb") as fp:
        return pickle.load(fp)


def write_pickle_file(file_path, data):
    """
    Write data to a pickle file.

    Parameters:
        file_path (str): The path to the pickle file.
        data (object): The data to be written to the file.
    """
    with open(file_path, "wb") as fp:
        pickle.dump(data, fp)


def show_confirmation(parent, message):
    """
    Display a confirmation dialog.

    Parameters:
        parent: The parent widget.
        message (str): The message to be displayed in the dialog.

    Returns:
        bool: True if the user clicks 'Yes', False otherwise.
    """
    confirmation = QMessageBox.question(
        parent,
        "Confirmation",
        message,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No,
    )
    return confirmation == QMessageBox.StandardButton.Yes


class ColourCell(QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def initStyleOption(self, option, index):
        """
        Initialize the style options for a table cell based on its value.

        Parameters:
            option: Style options for the cell.
            index: Index of the cell in the model.
        """
        super().initStyleOption(option, index)

        try:
            value = int(index.data(Qt.ItemDataRole.DisplayRole))
            # Colour cells based on the threshold values
            if 0 <= value <= ACCEPT_THRESHOLD:
                option.backgroundBrush = QBrush(QColor(0, 150, 0))
            elif ACCEPT_THRESHOLD < value <= GREYZONE_THRESHOLD:
                option.backgroundBrush = QBrush(QColor(255, 165, 0))
            elif value >= REJECT_THRESHOLD:
                option.backgroundBrush = QBrush(QColor(255, 0, 0))
        except ValueError:
            option.backgroundBrush = QBrush(QColor(0, 150, 0))


def setup_results_table(results, result_type):
    """
    Set up a QTableWidget with colour coded cells.

    Parameters:
        results (dict): Dictionary containing result values.
        result_type (str): Type of result.

    Returns:
        tuple: QTableWidget and a dictionary of QTableWidgetItem objects.
    """
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
    results_table.itemChanged.connect(handle_item_changed)
    results_table.setItemDelegate(colour_cell)

    return results_table, containers


def export_table_to_csv(table: QTableWidget):
    """
    Export the contents of a QTableWidget to a CSV file.

    Parameters:
        table (QTableWidget): The table to be exported.
    """
    path, ok = QFileDialog.getSaveFileName(None, "Save CSV", "", "CSV(*.csv)")
    if ok:
        columns = range(table.columnCount())
        header = [table.horizontalHeaderItem(column).text() for column in columns]
        with open(path, "w") as csvfile:
            writer = csv.writer(csvfile, dialect="excel", lineterminator="\n")
            writer.writerow(header)
            for row in range(table.rowCount()):
                writer.writerow(table.item(row, column).text() for column in columns)


def reset_value(value):
    """
    Reset the value to 0 if it's higher than 10 or not an integer.
    """
    try:
        int_value = int(value)
        if int_value > 10:
            return "0"
    except (ValueError, TypeError):
        return "0"
    return value


def handle_item_changed(item):
    """
    Resets the value to 0 if it's higher than 10 on the itemChanged signal.
    """
    if isinstance(item, QTableWidgetItem) and item.column() < 5:
        item.setText(reset_value(item.text()))
