import os
import pickle
import random
import sys
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QScrollArea,
    QLabel,
    QFileDialog,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QStyledItemDelegate,
)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QPalette


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle = "Knapp / FQV Reader"
        self.MainWindowUI()

    def MainWindowUI(self):
        self.resize(200, 200)
        self.create_man_inspect_button = QPushButton(
            "Create Dummy Inspection Data", self
        )
        self.create_fqv_button = QPushButton("Create Dummy FQV", self)
        self.load_fqv = QPushButton("Load FQV", self)
        self.load_machine_results = QPushButton("Load Machine Results (Particle)", self)
        self.compare_results = QPushButton("Compare Results", self)
        self.compare_results.setEnabled(False)
        self.quit_button = QPushButton("Quit", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.create_man_inspect_button)
        layout.addWidget(self.create_fqv_button)
        layout.addWidget(self.load_fqv)
        layout.addWidget(self.load_machine_results)
        layout.addWidget(self.compare_results)
        layout.addWidget(self.quit_button)

        self.setLayout(layout)
        self.create_fqv_button.clicked.connect(self.dummy_fqv_button)
        self.create_man_inspect_button.clicked.connect(self.dummy_man_inspect_button)
        self.load_fqv.clicked.connect(self.LoadFQV)
        self.load_machine_results.clicked.connect(self.LoadMachineResults)
        self.compare_results.clicked.connect(self.CompareResults)
        self.quit_button.clicked.connect(self.close)
        self.show()

    def LoadFQV(self):
        self.fqv_window = LoadFQV()
        self.fqv_window.show()

    def LoadMachineResults(self):
        self.machine_window = LoadMachineResults()
        self.machine_window.show()
        self.compare_results.setEnabled(True)

    def CompareResults(self):
        self.compare_window = CompareResults(
            self.fqv_window.manual_results, self.machine_window.machine_results
        )
        self.compare_window.show()

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
        if self.fileName != "":
            if self.fileName.endswith(".pkl"):
                with open(f"{self.fileName}", "wb") as fp:
                    pickle.dump(inspectors, fp)
            else:
                with open(f"{self.fileName}.pkl", "wb") as fp:
                    pickle.dump(inspectors, fp)

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
        if self.fileName != "":
            if self.fileName.endswith(".pkl"):
                with open(f"{self.fileName}", "wb") as fp:
                    pickle.dump(inspectors, fp)
            else:
                with open(f"{self.fileName}.pkl", "wb") as fp:
                    pickle.dump(inspectors, fp)

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
        self.setGeometry(600, 100, 300, 600)
        self.setWindowTitle("FQV Results")
        self.manual_results = {}
        self.LoadFQVUI()

    def LoadFQVUI(self):
        self.scroll = QScrollArea()
        self.fqv_widget = QWidget()
        self.container_box = QVBoxLayout()
        l1 = QLabel()
        self.container_box.addWidget(l1)
        self.fqv_containers = {}
        for container in range(1, 251):
            self.fqv_containers[container] = QSpinBox()
            self.container_box.addWidget(QLabel(f"Container {container}"))
            self.container_box.addWidget(self.fqv_containers[container])
        self.fqv_widget.setLayout(self.container_box)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.fqv_widget)
        self.setCentralWidget(self.scroll)
        self.openFileDialog()
        l1.setText(f"{self.results_title}")
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        self.close_button.move(80, 0)
        self.compare_window = CompareResults(self.manual_results)

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open FQV or Machine results",
            "",
            "All Files (*);;Pickle (*.pkl);;XML (*.xml)",
            options=options,
        )

        self.results_title = ""
        if fileName:
            self.load_fqv(fileName)
            self.results_title = os.path.basename(fileName)

    def load_fqv(self, fileName):
        self.results_title = os.path.basename(fileName)
        if fileName.endswith(".pkl"):
            try:
                with open(fileName, "rb") as fp:
                    self.fqv = pickle.load(fp)
                for container in range(1, 251):
                    self.manual_results[f"container_{container}"] = round(
                        (
                            self.fqv[f"inspector1_{container}"]
                            + self.fqv[f"inspector2_{container}"]
                            + self.fqv[f"inspector3_{container}"]
                            + self.fqv[f"inspector4_{container}"]
                            + self.fqv[f"inspector5_{container}"]
                        )
                        / 50
                        * 10
                    )
                    self.fqv_containers[container].setValue(
                        self.manual_results[f"container_{container}"]
                    )

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
                for container in range(1, 251):
                    self.fqv_containers[container].setValue(
                        self.manual_results[f"container_{container}"]
                    )
            except KeyError:
                pass
        return self.manual_results


class LoadMachineResults(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 300, 600)
        self.setWindowTitle("Machine Results")
        self.machine_results = {}
        self.LoadMachineResultsUI()

    def LoadMachineResultsUI(self):
        self.scroll = QScrollArea()
        self.machine_results_widget = QWidget()
        self.container_box = QVBoxLayout()
        l1 = QLabel()
        self.container_box.addWidget(l1)
        self.machine_containers = {}
        for container in range(1, 251):
            self.machine_containers[container] = QSpinBox()
            self.container_box.addWidget(QLabel(f"Container {container}"))
            self.container_box.addWidget(self.machine_containers[container])
        self.machine_results_widget.setLayout(self.container_box)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.machine_results_widget)

        self.setCentralWidget(self.scroll)

        self.openFileDialog()
        l1.setText(f"{self.results_title}")
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        self.close_button.move(80, 0)

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(
            self,
            "Open FQV or Machine results",
            "",
            "All Files (*);;Pickle (*.pkl);;XML (*.xml)",
            options=options,
        )
        self.results_title = ""
        if fileNames:
            for fileName in fileNames:
                self.load_results(fileName)
                self.results_title += f"{os.path.basename(fileName)}\n"

    def load_results(self, fileName):
        if fileName.endswith(".xml"):
            root = ET.parse(fileName).getroot()
            if "KnappRun_1_" in fileName:
                container_number = 0
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
                    self.machine_containers[container_number].setValue(
                        self.machine_results[f"container_{container_number}"]
                    )
            if "KnappRun_2_" in fileName:
                container_number = 24
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
                    self.machine_containers[container_number].setValue(
                        self.machine_results[f"container_{container_number}"]
                    )
            if "KnappRun_3_" in fileName:
                container_number = 48
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
                    self.machine_containers[container_number].setValue(
                        self.machine_results[f"container_{container_number}"]
                    )
            if "KnappRun_4_" in fileName:
                container_number = 72
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
                    self.machine_containers[container_number].setValue(
                        self.machine_results[f"container_{container_number}"]
                    )
            if "KnappRun_5_" in fileName:
                container_number = 96
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
                    self.machine_containers[container_number].setValue(
                        self.machine_results[f"container_{container_number}"]
                    )
            if "KnappRun_6_" in fileName:
                container_number = 120
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
                    self.machine_containers[container_number].setValue(
                        self.machine_results[f"container_{container_number}"]
                    )
            if "KnappRun_7_" in fileName:
                container_number = 144
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
                    self.machine_containers[container_number].setValue(
                        self.machine_results[f"container_{container_number}"]
                    )
            if "KnappRun_8_" in fileName:
                container_number = 168
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
                    self.machine_containers[container_number].setValue(
                        self.machine_results[f"container_{container_number}"]
                    )
            if "KnappRun_9_" in fileName:
                container_number = 192
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
                    self.machine_containers[container_number].setValue(
                        self.machine_results[f"container_{container_number}"]
                    )
            if "KnappRun_10_" in fileName:
                container_number = 216
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
                    self.machine_containers[container_number].setValue(
                        self.machine_results[f"container_{container_number}"]
                    )
            if "KnappRun_11_" in fileName:
                container_number = 240
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    if container_number > 250:
                        break
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
                    self.machine_containers[container_number].setValue(
                        self.machine_results[f"container_{container_number}"]
                    )
        return self.machine_results


class CompareResults(QWidget):
    def __init__(self, manual_results=None, machine_results=None):
        super().__init__()
        self.manual_results = manual_results or {}
        self.machine_results = machine_results or {}
        self.CompareResultsUI()

    def CompareResultsUI(self):
        self.compare_results_widget = QVBoxLayout()
        self.setGeometry(600, 100, 300, 600)
        self.setWindowTitle("FQV vs Machine Results")
        self.manual_containers = {}
        self.machine_containers = {}
        table = QTableWidget()
        table.setRowCount(250)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Manual", "Machine"])

        for container in range(1, 251):
            manual_item = QTableWidgetItem(
                str(self.manual_results.get(f"container_{container}", 0))
            )
            machine_item = QTableWidgetItem(
                str(self.machine_results.get(f"container_{container}", 0))
            )

            manual_item.setFlags(manual_item.flags() & ~Qt.ItemIsEditable)
            machine_item.setFlags(machine_item.flags() & ~Qt.ItemIsEditable)

            table.setItem(container - 1, 0, manual_item)
            table.setItem(container - 1, 1, machine_item)

            if int(manual_item.text()) > 7:
                manual_item.setData(Qt.UserRole, "high_value")
            if int(machine_item.text()) > 7:
                machine_item.setData(Qt.UserRole, "high_value")

        colourCell = ColourCell()
        table.setItemDelegate(colourCell)
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.close_button)
        self.compare_results_widget.addWidget(table)
        self.compare_results_widget.addLayout(button_layout)
        self.setLayout(self.compare_results_widget)


class ColourCell(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(ColourCell, self).initStyleOption(option, index)

        value = int(index.data(Qt.DisplayRole))

        if 0 <= value <= 3:
            option.backgroundBrush = QBrush(QColor(0, 150, 0))
            palette = option.palette
            palette.setColor(QPalette.Text, Qt.black)
            option.palette = palette
        elif 4 <= value <= 6:
            option.backgroundBrush = QBrush(QColor(255, 165, 0))
            palette = option.palette
            palette.setColor(QPalette.Text, Qt.black)
            option.palette = palette
        elif value >= 7:
            option.backgroundBrush = QBrush(QColor(255, 0, 0))
            palette = option.palette
            palette.setColor(QPalette.Text, Qt.white)
            option.palette = palette


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())
