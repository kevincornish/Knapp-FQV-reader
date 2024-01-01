import xml.etree.ElementTree as ET
from utils import (
    write_pickle_file,
    read_pickle_file,
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
from constants import CONTAINER_START, CONTAINER_END


class CreateFQV(QWidget):
    """
    Class for creating FQV results.
    """

    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 150, 600)
        self.setWindowTitle("Create FQV Results")
        self.manual_results = {}
        self.fqv_containers = {}
        self.CreateFQVUI()

    def CreateFQVUI(self):
        """
        Setup the UI for creating FQV results.
        """
        self.fqv_widget = QVBoxLayout()

        self.setup_table()

        title = QLabel("Create FQV Results")
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_fqv_results)

        self.open_button = QPushButton("Open", self)
        self.open_button.clicked.connect(self.open_file)

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)

        self.fqv_widget.addWidget(title)
        self.fqv_widget.addWidget(self.fqv_results_table)
        self.fqv_widget.addWidget(self.save_button)
        self.fqv_widget.addWidget(self.open_button)
        self.fqv_widget.addWidget(self.close_button)

        self.setLayout(self.fqv_widget)

    def setup_table(self):
        """
        Setup the table for displaying FQV results.
        """
        self.fqv_results_table = QTableWidget()
        self.fqv_results_table.setRowCount(CONTAINER_END)
        self.fqv_results_table.setColumnCount(1)
        self.fqv_results_table.setHorizontalHeaderLabels(["Manual"])

        for container in range(CONTAINER_START, CONTAINER_END + 1):
            self.fqv_containers[container] = QTableWidgetItem("0")
            self.fqv_results_table.setItem(
                container - 1, 0, self.fqv_containers[container]
            )

        self.fqv_results_table.setItemDelegate(ColourCell())

    def save_fqv_results(self):
        """
        Save the created FQV results to a pickle file.
        """
        for container in range(CONTAINER_START, CONTAINER_END + 1):
            self.manual_results[f"container_{container}"] = int(
                self.fqv_containers[container].text()
            )
        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Save FQV Results",
            "",
            "Pickle Files (*.pkl)",
        )

        if fileName and write_pickle_file(fileName, self.manual_results):
            self.close()

    def open_file(self):
        """
        Open a file dialog to load existing FQV data.
        """
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open FQV Data",
            "",
            "All Files (*);;Pickle Files (*.pkl);;XML Files (*.xml)",
        )

        if fileName:
            if fileName.endswith(".pkl"):
                pre_made_results = read_pickle_file(fileName)
                for container in range(CONTAINER_START, CONTAINER_END + 1):
                    result = pre_made_results.get(f"container_{container}", 0)
                    self.fqv_containers[container].setText(str(result))
            elif fileName.endswith(".xml"):
                try:
                    root = ET.parse(fileName).getroot()
                    container_number = 0
                    for type_tag in root.findall("Sample/Manual"):
                        container_number += 1
                        self.fqv_containers[container_number].setText(
                            str(type_tag.text)
                        )
                except KeyError:
                    pass
