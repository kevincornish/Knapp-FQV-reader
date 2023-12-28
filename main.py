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
    QLabel,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QStyledItemDelegate,
)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QPalette
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MainApp(QWidget):
    """
    Main application window for the Knapp/FQV Reader.
    """

    def __init__(self):
        super().__init__()
        self.setGeometry(600, 400, 200, 200)
        self.setWindowTitle("Knapp / FQV Reader")
        self.MainWindowUI()

    def MainWindowUI(self):
        """
        Create the main window UI layout.
        """
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
        confirmation = QMessageBox.question(
            self,
            "Confirmation",
            "Show FQV?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation == QMessageBox.Yes:
            self.fqv_window.show()

    def LoadMachineResults(self):
        self.machine_window = LoadMachineResults()
        confirmation = QMessageBox.question(
            self,
            "Confirmation",
            "Show Machine Results?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation == QMessageBox.Yes:
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
        l1 = QLabel()
        self.fqv_widget.addWidget(l1)
        table = QTableWidget()
        table.setRowCount(250)
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["Manual"])
        for container in range(1, 251):
            self.fqv_containers[container] = QTableWidgetItem(
                str(self.manual_results.get(f"container_{container}", 0))
            )
            table.setItem(container - 1, 0, self.fqv_containers[container])
            self.fqv_containers[container].setFlags(
                self.fqv_containers[container].flags() & ~Qt.ItemIsEditable
            )
            if int(self.fqv_containers[container].text()) > 7:
                self.fqv_containers[container].setData(Qt.UserRole, "high_value")

        colourCell = ColourCell()
        table.setItemDelegate(colourCell)
        l1.setText(f"{self.results_title}")
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.close_button)
        self.fqv_widget.addWidget(table)
        self.fqv_widget.addLayout(button_layout)
        self.compare_window = CompareResults(self.manual_results)
        self.setLayout(self.fqv_widget)

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
        return self.manual_results


class LoadMachineResults(QWidget):
    """
    Class for loading machine inspection results.
    """

    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 150, 600)
        self.setWindowTitle("Machine Results")
        self.machine_results = {}
        self.machine_containers = {}
        self.LoadMachineResultsUI()

    def LoadMachineResultsUI(self):
        """
        Setup the UI for loading machine results.
        """
        self.openFileDialog()
        self.machine_results_widget = QVBoxLayout()
        l1 = QLabel()
        self.machine_results_widget.addWidget(l1)
        table = QTableWidget()
        table.setRowCount(250)
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["Machine"])
        for container in range(1, 251):
            self.machine_containers[container] = QTableWidgetItem(
                str(self.machine_results.get(f"container_{container}", 0))
            )
            table.setItem(container - 1, 0, self.machine_containers[container])
            self.machine_containers[container].setFlags(
                self.machine_containers[container].flags() & ~Qt.ItemIsEditable
            )
            if int(self.machine_containers[container].text()) > 7:
                self.machine_containers[container].setData(Qt.UserRole, "high_value")

        colourCell = ColourCell()
        table.setItemDelegate(colourCell)
        l1.setText(f"{self.results_title}")
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.close_button)
        self.machine_results_widget.addWidget(table)
        self.machine_results_widget.addLayout(button_layout)
        self.setLayout(self.machine_results_widget)

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
            if "KnappRun_2_" in fileName:
                container_number = 24
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
            if "KnappRun_3_" in fileName:
                container_number = 48
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
            if "KnappRun_4_" in fileName:
                container_number = 72
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
            if "KnappRun_5_" in fileName:
                container_number = 96
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
            if "KnappRun_6_" in fileName:
                container_number = 120
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
            if "KnappRun_7_" in fileName:
                container_number = 144
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
            if "KnappRun_8_" in fileName:
                container_number = 168
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
            if "KnappRun_9_" in fileName:
                container_number = 192
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
            if "KnappRun_10_" in fileName:
                container_number = 216
                for type_tag in root.findall("ParticlesInspection/Sample/TotReject"):
                    container_number += 1
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
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
        return self.machine_results


class CompareResults(QWidget):
    """
    Class for comparing manual and machine inspection results.
    """

    def __init__(self, manual_results=None, machine_results=None):
        super().__init__()
        self.manual_results = manual_results or {}
        self.machine_results = machine_results or {}
        self.efficiency_window = None
        self.CompareResultsUI()

    def CompareResultsUI(self):
        """
        Setup the UI for comparing manual and machine inspection results.
        """
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

            self.manual_containers[f"container_{container}"] = int(manual_item.text())
            self.machine_containers[f"container_{container}"] = int(machine_item.text())

        colourCell = ColourCell()
        table.setItemDelegate(colourCell)
        self.show_efficiency_button = QPushButton("Calculate efficiency", self)
        self.show_efficiency_button.clicked.connect(self.show_efficiency)
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.show_efficiency_button)
        button_layout.addWidget(self.close_button)
        self.compare_results_widget.addWidget(table)
        self.compare_results_widget.addLayout(button_layout)
        self.setLayout(self.compare_results_widget)

    def show_efficiency(self):
        if self.efficiency_window is not None:
            self.efficiency_window.showNormal()
            self.efficiency_window.activateWindow()
        else:
            self.efficiency_window = EfficiencyWindow(
                self.manual_containers, self.machine_containers
            )
            self.efficiency_window.show()


class ColourCell(QStyledItemDelegate):
    """
    Custom delegate class for coloring cells based on their values.
    """

    def initStyleOption(self, option, index):
        """
        Initialize style options for the delegate to customize cell appearance.
        """
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


class EfficiencyWindow(QMainWindow):
    """
    Class for displaying a bar chart comparing manual and machine efficiency.
    """

    def __init__(self, manual_results=None, machine_results=None):
        super().__init__()

        self.setWindowTitle("Machine vs Manual")
        self.setGeometry(600, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.manual_containers = manual_results or {}
        self.machine_containers = machine_results or {}

        self.efficiency_canvas = FigureCanvas(Figure(figsize=(8, 6), dpi=100))
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.efficiency_canvas)

        self.plot_bar_chart()

    def plot_bar_chart(self):
        """
        Plot a bar chart comparing manual and machine efficiency.
        """
        ax = self.efficiency_canvas.figure.add_subplot(111)

        if not self.manual_containers or not self.machine_containers:
            ax.text(
                0.5,
                0.5,
                "No data to plot",
                ha="center",
                va="center",
                fontsize=12,
                color="gray",
            )
        else:
            values = list(range(11))
            manual_counts = [
                list(self.manual_containers.values()).count(value) for value in values
            ]
            machine_counts = [
                list(self.machine_containers.values()).count(value) for value in values
            ]

            bar_width = 0.35
            index = range(len(values))

            for i, count in enumerate(manual_counts):
                ax.bar(
                    i, count, bar_width, color="blue", label="Manual" if i == 0 else ""
                )
                ax.text(
                    i,
                    count,
                    str(count),
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    color="black",
                )

            for i, count in enumerate(machine_counts):
                ax.bar(
                    i + bar_width,
                    count,
                    bar_width,
                    color="orange",
                    label="Machine" if i == 0 else "",
                )
                ax.text(
                    i + bar_width,
                    count,
                    str(count),
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    color="black",
                )

            ax.set_xlabel("No. rejected by operators and machine")
            ax.set_ylabel("Times Rejected")
            ax.set_title("FQV/A graphical distribution")
            ax.set_xticks([i + bar_width / 2 for i in index])
            ax.set_xticklabels(values)

            # Calculate efficiency only for values 7 or above
            total_manual = sum(manual_counts[7:])
            total_machine = sum(machine_counts[7:])
            efficacy_manual_to_machine = (
                total_manual / total_machine * 100 if total_machine > 0 else 0
            )
            efficacy_machine_to_manual = (
                total_machine / total_manual * 100 if total_manual > 0 else 0
            )

            text_manual_vs_machine = (
                f"Manual vs Machine Efficiency: {efficacy_manual_to_machine:.2f}%"
            )
            text_machine_vs_manual = (
                f"Machine vs Manual Efficiency: {efficacy_machine_to_manual:.2f}%"
            )

            ax.annotate(
                text_manual_vs_machine,
                xy=(0.5, 0.95),
                xycoords="axes fraction",
                ha="center",
                va="center",
                fontsize=10,
                color="blue",
            )
            ax.annotate(
                text_machine_vs_manual,
                xy=(0.5, 0.90),
                xycoords="axes fraction",
                ha="center",
                va="center",
                fontsize=10,
                color="orange",
            )

            ax.legend()

        self.efficiency_canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())
