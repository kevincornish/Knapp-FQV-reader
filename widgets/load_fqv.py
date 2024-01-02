import csv
import os
import pickle
import xml.etree.ElementTree as ET
from utils import (
    read_pickle_file,
    setup_results_table,
)
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QFileDialog,
)
from widgets.compare_results import CompareResults
from constants import CONTAINER_START, CONTAINER_END


class LoadFQV(QWidget):
    """
    Class for loading FQV results.
    """

    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 150, 600)
        self.setWindowTitle("FQV Results")
        self.manual_results = {}
        self.fqv_containers = {}
        self.LoadFQVUI()

    def LoadFQVUI(self):
        """
        Setup the UI for loading FQV results.
        """
        self.openFileDialog()
        self.fqv_widget = QVBoxLayout()
        title_label = QLabel()
        self.fqv_widget.addWidget(title_label)

        self.results_table, self.fqv_containers = setup_results_table(
            self.manual_results, "Manual"
        )

        title_label.setText(f"{self.results_title}")
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.close_button)
        self.fqv_widget.addWidget(self.results_table)
        self.fqv_widget.addLayout(button_layout)
        self.compare_window = CompareResults(self.manual_results)
        self.setLayout(self.fqv_widget)

    def openFileDialog(self):
        """
        Open a file dialog to choose the FQV results file.
        """
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open FQV or Machine results",
            "",
            "All Files (*);;Pickle (*.pkl);;XML (*.xml);;CSV (*.csv)",
        )

        self.results_title = ""
        if fileName:
            self.load_fqv(fileName)
            self.results_title = os.path.basename(fileName)

    def load_fqv(self, fileName):
        """
        Load FQV results from a pickle, csv or xml file.

        Parameters:
            fileName (str): Path to the FQV results file.
        """
        self.results_title = os.path.basename(fileName)
        if fileName.endswith(".pkl"):
            try:
                self.fqv = read_pickle_file(fileName)
                for container in range(CONTAINER_START, CONTAINER_END + 1):
                    key = f"container_{container}"
                    value = self.fqv.get(key, None)
                    if value is not None:
                        if isinstance(value, list):
                            avg_value = round((sum(value) / 50) * 10)
                            self.manual_results[key] = avg_value
                        else:
                            self.manual_results[key] = value
            except (pickle.UnpicklingError, KeyError):
                pass
        elif fileName.endswith(".xml"):
            try:
                root = ET.parse(fileName).getroot()
                container_number = 0
                for type_tag in root.findall("Sample/Manual"):
                    container_number += 1
                    self.manual_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
            except KeyError:
                pass
        elif fileName.endswith(".csv"):
            self.manual_results = {}
            with open(fileName, "rt") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row, values in enumerate(reader):
                    container_key = f"container_{row + 1}"
                    inspector_results = []
                    for value in values:
                        try:
                            inspector_results.append(int(value))
                        except ValueError:
                            inspector_results.append(0)

                    avg_value = round((sum(inspector_results) / 5))
                    self.manual_results[container_key] = avg_value
        return self.manual_results
