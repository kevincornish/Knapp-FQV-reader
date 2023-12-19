import pickle
import random
import sys
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QWidget,
    QLabel,
    QFileDialog,
    QSpinBox,
)
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot


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
            "QFileDialog.getSaveFileName()",
            "",
            "Pickle Files (*.pkl)",
            options=options,
        )
        if self.fileName:
            print(self.fileName)


class LoadFQV(QWidget):
    def __init__(self):
        super().__init__()
        self.LoadFQVUI()

    def LoadFQVUI(self):
        layout = QGridLayout(self)
        self.container_1 = QSpinBox()
        self.container_2 = QSpinBox()
        layout.addWidget(QLabel("container_1"))
        layout.addWidget(self.container_1)
        layout.addWidget(QLabel("container_2"))
        layout.addWidget(self.container_2)
        self.openFileDialog()

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "",
            "All Files (*);;Pickle (*.pkl)",
            options=options,
        )
        if fileName:
            self.load_fqv(fileName)

    def load_fqv(self, fileName):
        if fileName.endswith(".pkl"):
            try:
                with open(fileName, "rb") as fp:
                    self.fqv = pickle.load(fp)
                    print(f"File: {fileName} loaded!")
                self.container_1.setValue(
                    self.fqv["inspector1_1"]
                    + self.fqv["inspector2_1"]
                    + self.fqv["inspector3_1"]
                    + self.fqv["inspector4_1"]
                    + self.fqv["inspector5_1"]
                )
                self.container_2.setValue(
                    self.fqv["inspector1_2"]
                    + self.fqv["inspector2_2"]
                    + self.fqv["inspector3_2"]
                    + self.fqv["inspector4_2"]
                    + self.fqv["inspector5_2"]
                )
            except (pickle.UnpicklingError, KeyError):
                print("invalid FQV")
                pass
        elif fileName.endswith(".xml"):
            root = ET.parse(fileName).getroot()
            container_number = 0
            for type_tag in root.findall("Sample/Manual"):
                container_number += 1
                print(type_tag.text, container_number)
        else:
            print("invalid FQV")
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())
