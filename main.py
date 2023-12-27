import os
import pickle
import random
import sys
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QScrollArea,
    QLabel,
    QFileDialog,
    QSpinBox,
)
from PyQt5.QtCore import Qt, pyqtSlot


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Knapp / FQV Reader"
        self.width = 320
        self.height = 200
        self.MainWindowUI()

    def MainWindowUI(self):
        self.setWindowTitle(self.title)
        self.resize(400, 370)
        self.create_man_inspect_button = QPushButton(
            "Create Dummy Inspection Data", self
        )
        self.create_fqv_button = QPushButton("Create Dummy FQV", self)
        self.load_fqv = QPushButton("Load FQV", self)
        self.quit_button = QPushButton("Quit", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.create_man_inspect_button)
        layout.addWidget(self.create_fqv_button)
        layout.addWidget(self.load_fqv)
        layout.addWidget(self.quit_button)

        self.setLayout(layout)
        self.create_fqv_button.clicked.connect(self.dummy_fqv_button)
        self.create_man_inspect_button.clicked.connect(self.dummy_man_inspect_button)
        self.quit_button.clicked.connect(self.close)
        self.load_fqv.clicked.connect(self.LoadFQV)
        self.show()

    def LoadFQV(self):
        self.w = LoadFQV()
        self.w.show()

    @pyqtSlot()
    def dummy_fqv_button(self):
        inspectors = {}
        for number_of_inspectors in range(1, 6):
            inspections = 1
            number_of_inspections = 251
            while inspections < number_of_inspections:
                results = {
                    f"inspector{number_of_inspectors}_{inspections}": random.randint(
                        0, 10
                    )
                }
                inspectors.update(results)
                inspections += 1

        self.saveFileDialog()
        if self.fileName.endswith(".pkl"):
            with open(f"{self.fileName}", "wb") as fp:
                pickle.dump(inspectors, fp)
        else:
            with open(f"{self.fileName}.pkl", "wb") as fp:
                pickle.dump(inspectors, fp)

        print("FQV Data Saved")

    @pyqtSlot()
    def dummy_man_inspect_button(self):
        inspectors = {}
        for number_of_inspectors in range(1, 6):
            for number_of_runs in range(1, 11):
                inspections = 1
                number_of_inspections = 251
                while inspections < number_of_inspections:
                    results = {
                        f"inspector{number_of_inspectors}_{number_of_runs}_{inspections}": random.randint(
                            0, 10
                        )
                    }
                    inspectors.update(results)
                    inspections += 1

        self.saveFileDialog()
        if self.fileName.endswith(".pkl"):
            with open(f"{self.fileName}", "wb") as fp:
                pickle.dump(inspectors, fp)
        else:
            with open(f"{self.fileName}.pkl", "wb") as fp:
                pickle.dump(inspectors, fp)

        print("Random Inspection Data Saved")

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Save FQV or Machine results",
            "",
            "Pickle Files (*.pkl)",
            options=options,
        )


class LoadFQV(QMainWindow):
    def __init__(self):
        super().__init__()
        self.LoadFQVUI()

    def LoadFQVUI(self):
        self.scroll = QScrollArea()
        self.fqv_widget = QWidget()
        self.container_box = QVBoxLayout()
        l1 = QLabel()
        self.container_box.addWidget(l1)
        self.containers = {}
        for container in range(1, 251):
            self.containers[container] = QSpinBox()
            self.container_box.addWidget(QLabel(f"Container {container}"))
            self.container_box.addWidget(self.containers[container])
        self.fqv_widget.setLayout(self.container_box)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.fqv_widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 300, 600)
        self.setWindowTitle("FQV Results")
        self.openFileDialog()
        l1.setText(f"{self.results_title}")

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open FQV or Machine results",
            "",
            "All Files (*);;Pickle (*.pkl)",
            options=options,
        )
        if fileName:
            self.load_fqv(fileName)

    def load_fqv(self, fileName):
        self.results_title = os.path.basename(fileName)
        if fileName.endswith(".pkl"):
            try:
                with open(fileName, "rb") as fp:
                    self.fqv = pickle.load(fp)
                for container in range(1, 251):
                    self.containers[container].setValue(
                        self.fqv[f"inspector1_{container}"]
                        + self.fqv[f"inspector2_{container}"]
                        + self.fqv[f"inspector3_{container}"]
                        + self.fqv[f"inspector4_{container}"]
                        + self.fqv[f"inspector5_{container}"]
                    )
            except (pickle.UnpicklingError, KeyError):
                print("invalid FQV")
        elif fileName.endswith(".xml"):
            root = ET.parse(fileName).getroot()
            container_number = 0
            manual_results = {}
            for type_tag in root.findall("Sample/Manual"):
                container_number += 1
                manual_results[f"container_{container_number}"] = int(type_tag.text)
            for container in range(1, 251):
                self.containers[container].setValue(
                    manual_results[f"container_{container}"]
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())
