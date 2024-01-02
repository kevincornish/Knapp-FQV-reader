import csv
import pickle
from utils import (
    write_pickle_file,
    read_pickle_file,
    ColourCell,
    handle_item_changed,
)
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt6.QtCore import Qt
from constants import CONTAINER_START, CONTAINER_END


class CreateManualInspection(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 500, 600)
        self.setWindowTitle("Create Manual Inspection Data")
        self.inspection_results = {}
        self.inspection_containers = {}
        self.CreateManualInspectionUI()

    def CreateManualInspectionUI(self):
        """
        Setup the UI for creating manual inspection data.
        """
        self.inspection_widget = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(CONTAINER_END)
        self.table.setColumnCount(5)  # One column for each inspector
        self.table.setHorizontalHeaderLabels(
            ["Inspector 1", "Inspector 2", "Inspector 3", "Inspector 4", "Inspector 5"]
        )

        for container in range(CONTAINER_START, CONTAINER_END + 1):
            self.inspection_containers[container] = [
                QTableWidgetItem("0") for _ in range(5)
            ]

            for i in range(5):
                self.table.setItem(
                    container - 1, i, self.inspection_containers[container][i]
                )
        self.table.itemChanged.connect(handle_item_changed)
        self.table.setItemDelegate(ColourCell())

        title_label = QLabel()
        title_label.setText("Create Manual Inspection Data")
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_inspection_results)

        self.open_button = QPushButton("Open", self)
        self.open_button.clicked.connect(self.openFileDialog)

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)

        self.inspection_widget.addWidget(title_label)
        self.inspection_widget.addWidget(self.table)
        self.inspection_widget.addWidget(self.save_button)
        self.inspection_widget.addWidget(self.open_button)
        self.inspection_widget.addWidget(self.close_button)

        self.setLayout(self.inspection_widget)

    def openFileDialog(self):
        """
        Open a file dialog to choose the manual inspection data file.
        """
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open Manual Inspection Data",
            "",
            "All Files (*);;Pickle (*.pkl);;XML (*.xml)",
        )

        if fileName:
            self.open_file(fileName)

    def open_file(self, fileName):
        """
        Open a file dialog to load existing manual inspection data.
        """
        if fileName.endswith(".pkl"):
            try:
                manual_results = read_pickle_file(fileName)
                for container in range(CONTAINER_START, CONTAINER_END + 1):
                    inspector_results = manual_results.get(
                        f"container_{container}", [0, 0, 0, 0, 0]
                    )
                    for i in range(5):
                        item = QTableWidgetItem(str(inspector_results[i]))
                        self.table.setItem(container - 1, i, item)
            except (pickle.UnpicklingError, KeyError):
                pass
        elif fileName.endswith(".csv"):
            self.table.clearContents()
            self.table.setRowCount(0)
            self.manual_inspection_results = {}
            with open(fileName, "rt") as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)
                self.table.setColumnCount(len(header))
                self.table.setHorizontalHeaderLabels(header)
                for row, values in enumerate(reader):
                    self.table.insertRow(row)
                    container_key = f"container_{row + 1}"
                    inspector_results = []
                    for value in values:
                        try:
                            inspector_results.append(int(value))
                        except ValueError:
                            inspector_results.append(0)

                    self.manual_inspection_results[container_key] = inspector_results
                    for column, value in enumerate(values):
                        item = QTableWidgetItem(str(value))
                        self.table.setItem(row, column, item)
            self.table.itemChanged.disconnect(handle_item_changed)
            self.table.itemChanged.connect(handle_item_changed)

    def save_inspection_results(self):
        """
        Save the created manual inspection results to a pickle file.
        """
        for container in range(CONTAINER_START, CONTAINER_END + 1):
            inspector_results = [
                int(self.table.item(container - 1, i).text()) for i in range(5)
            ]
            self.inspection_results[f"container_{container}"] = inspector_results

        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Save Manual Inspection Results",
            "",
            "Pickle Files (*.pkl)",
        )

        if fileName and write_pickle_file(fileName, self.inspection_results):
            self.close()
