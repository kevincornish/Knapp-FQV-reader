import csv
import os
import pickle
from utils import (
    read_pickle_file,
    export_table_to_csv,
    ColourCell,
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


class LoadManualInspection(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 500, 600)
        self.setWindowTitle("Manual Inspection Data")
        self.manual_inspection_results = {}
        self.manual_inspection_containers = {}
        self.table = QTableWidget()
        self.results_title = ""
        self.LoadManualInspectionUI()

    def LoadManualInspectionUI(self):
        self.manual_inspection_widget = QVBoxLayout()

        self.openFileDialog()
        title_label = QLabel()
        self.manual_inspection_widget.addWidget(title_label)
        self.table.setRowCount(CONTAINER_END - CONTAINER_START + 1)
        self.table.setColumnCount(5)  # One column for each inspector
        self.table.setHorizontalHeaderLabels(
            ["Inspector 1", "Inspector 2", "Inspector 3", "Inspector 4", "Inspector 5"]
        )

        for container in range(CONTAINER_START, CONTAINER_END + 1):
            inspector_results = self.manual_inspection_results.get(
                f"container_{container}", [0, 0, 0, 0, 0]
            )
            self.manual_inspection_containers[container] = [
                QTableWidgetItem(str(result)) for result in inspector_results
            ]

            for i in range(5):
                self.table.setItem(
                    container - 1, i, self.manual_inspection_containers[container][i]
                )

                self.manual_inspection_containers[container][i].setFlags(
                    self.manual_inspection_containers[container][i].flags()
                    & ~Qt.ItemFlag.ItemIsEditable
                )

        self.table.setItemDelegate(ColourCell())
        title_label.setText(f"{self.results_title}")
        self.export_button = QPushButton("Export (csv)")
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        self.export_button.clicked.connect(self.export_manual_inspection_data)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.close_button)
        self.manual_inspection_widget.addWidget(self.table)
        self.manual_inspection_widget.addLayout(button_layout)
        self.table.resizeColumnsToContents()
        self.setLayout(self.manual_inspection_widget)

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
            self.load_manual_inspection_data(fileName)
            self.results_title = os.path.basename(fileName)

    def load_manual_inspection_data(self, fileName):
        """
        Load manual inspection data from a pickle or csv file.

        Parameters:
            fileName (str): Path to the manual inspection data file.
        """
        self.results_title = os.path.basename(fileName)
        if fileName.endswith(".pkl"):
            try:
                self.manual_inspection_results = read_pickle_file(fileName)
                for container_key, values in self.manual_inspection_results.items():
                    if not isinstance(values, list):
                        self.manual_inspection_results[container_key] = [values] * 5
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
                    inspector_results = [int(value) for value in values]
                    self.manual_inspection_results[container_key] = inspector_results
                    for column, value in enumerate(values):
                        item = QTableWidgetItem(value)
                        self.table.setItem(row, column, item)
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

    def export_manual_inspection_data(self):
        """
        Export the manual inspection data to a CSV file.
        """
        export_table_to_csv(self.table)
