import os
import xml.etree.ElementTree as ET
from utils import (
    setup_results_table,
)
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QFileDialog,
)
from constants import CONTAINER_END


class LoadMachineResults(QWidget):
    """
    Class for loading machine inspection results.
    """

    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 150, 600)
        self.setWindowTitle("Machine Results")
        self.machine_results = {f"container_{i}": -1 for i in range(1, CONTAINER_END + 1)}
        self.machine_containers = {}
        self.results_title = ""
        self.LoadMachineResultsUI()

    def LoadMachineResultsUI(self):
        """
        Setup the UI for loading machine results.
        """
        self.openFileDialog()
        self.machine_results_widget = QVBoxLayout()
        title_label = QLabel()
        self.machine_results_widget.addWidget(title_label)

        self.results_table, self.machine_containers = setup_results_table(
            self.machine_results, "Machine"
        )

        title_label.setText(f"{self.results_title}")
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.close_button)
        self.machine_results_widget.addWidget(self.results_table)
        self.machine_results_widget.addLayout(button_layout)
        self.setLayout(self.machine_results_widget)

    def openFileDialog(self):
        """
        Open a file dialog to choose the machine results file(s).
        """
        fileNames, _ = QFileDialog.getOpenFileNames(
            self,
            "Open FQV or Machine results",
            "",
            "All Files (*);;Pickle (*.pkl);;XML (*.xml)",
        )
        if fileNames:
            for fileName in fileNames:
                self.load_results(fileName)
                self.results_title += f"{os.path.basename(fileName)}\n"

    def load_results(self, fileName):
        """
        Load machine inspection results from xml files.

        Parameters:
            fileName (str): Path to the machine results file.
        """
        if fileName.endswith(".xml"):
            root = ET.parse(fileName).getroot()
            container_number = 0
            for run_number in range(1, 12):
                run_prefix = f"KnappRun_{run_number}_"
                if run_prefix in fileName:
                    container_number += (run_number - 1) * 24
                    for type_tag in root.findall(
                        "ParticlesInspection/Sample/TotReject"
                    ):
                        container_number += 1
                        if container_number > CONTAINER_END:
                            break
                        self.machine_results[f"container_{container_number}"] = int(
                            type_tag.text
                        )
        return self.machine_results
