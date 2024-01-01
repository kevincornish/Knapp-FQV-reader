import csv
import os
import pickle
import random
import sys
import xml.etree.ElementTree as ET
from utils import (
    show_confirmation,
    write_pickle_file,
    read_pickle_file,
    setup_results_table,
    export_table_to_csv,
    ColourCell,
)
from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QLabel,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
)
from PyQt6.QtCore import Qt, pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


CONTAINER_START = 1
CONTAINER_END = 250


class MainApp(QWidget):
    """
    Main application window for the Knapp/FQV Reader.
    """

    def __init__(self):
        super().__init__()
        self.setGeometry(600, 400, 450, 350)
        self.setWindowTitle("Knapp / FQV Reader")
        self.MainWindowUI()

    def MainWindowUI(self):
        """
        Create the main window UI layout.
        """
        self.main_ui = QTabWidget()
        self.knapp_tab = QWidget()
        self.create_data_tab = QWidget()
        self.manual_inspection_tab = QWidget()
        self.main_ui.addTab(self.knapp_tab, "Knapp")
        self.main_ui.addTab(self.create_data_tab, "Create Knapp Data")
        self.main_ui.addTab(self.manual_inspection_tab, "Manual Inspection")
        self.setup_knapp_tab_layout()
        self.setup_create_data_tab_layout()
        self.setup_manual_inspection_tab_layout()
        self.quit_button = QPushButton("Quit", self)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.main_ui)
        main_layout.addWidget(self.quit_button)

        self.setLayout(main_layout)

        self.create_random_fqv_button.clicked.connect(self.random_fqv_button)
        self.create_random_man_inspect_button.clicked.connect(
            self.random_man_inspect_button
        )
        self.create_fqv_button.clicked.connect(self.create_fqv_window)
        self.create_man_inspect_button.clicked.connect(
            self.create_manual_inspection_window
        )
        self.load_manual_inspection.clicked.connect(self.LoadManualInspection)
        self.load_fqv.clicked.connect(self.LoadFQV)
        self.load_machine_results.clicked.connect(self.LoadMachineResults)
        self.compare_results.clicked.connect(self.CompareResults)
        self.quit_button.clicked.connect(self.close)
        self.show()

    def setup_knapp_tab_layout(self):
        """
        Set up the layout for the Main tab.
        """
        self.load_fqv = QPushButton("Load FQV (Manual)", self)
        self.load_machine_results = QPushButton("Load FQA (Machine)", self)
        self.compare_results = QPushButton("Compare Results", self)
        self.compare_results.setEnabled(False)

        main_layout = QVBoxLayout(self.knapp_tab)
        main_layout.addWidget(self.load_fqv)
        main_layout.addWidget(self.load_machine_results)
        main_layout.addWidget(self.compare_results)

    def setup_create_data_tab_layout(self):
        """
        Set up the layout for the create data tab.
        """
        self.create_fqv_button = QPushButton("Create FQV", self)
        self.create_random_fqv_button = QPushButton("Create Random FQV", self)

        create_data_layout = QVBoxLayout(self.create_data_tab)
        create_data_layout.addWidget(self.create_fqv_button)
        create_data_layout.addWidget(self.create_random_fqv_button)

    def setup_manual_inspection_tab_layout(self):
        self.create_man_inspect_button = QPushButton(
            "Create Manual Inspection Data", self
        )
        self.create_random_man_inspect_button = QPushButton(
            "Create Random Inspection Data", self
        )
        self.load_manual_inspection = QPushButton("Load Manual Inspection Data", self)
        manual_inspection_tab_layout = QVBoxLayout(self.manual_inspection_tab)
        manual_inspection_tab_layout.addWidget(self.create_man_inspect_button)
        manual_inspection_tab_layout.addWidget(self.create_random_man_inspect_button)
        manual_inspection_tab_layout.addWidget(self.load_manual_inspection)

    def LoadManualInspection(self):
        self.manual_inspection_window = LoadManualInspection()
        if show_confirmation(self, "Show Manual Inspection Data?"):
            self.manual_inspection_window.show()

    def LoadFQV(self):
        self.fqv_window = LoadFQV()
        if show_confirmation(self, "Show FQV?"):
            self.fqv_window.show()

    def LoadMachineResults(self):
        self.machine_window = LoadMachineResults()
        if show_confirmation(self, "Show Machine Results?"):
            self.machine_window.show()
        self.compare_results.setEnabled(True)

    def CompareResults(self):
        self.compare_window = CompareResults(
            self.fqv_window.manual_results, self.machine_window.machine_results
        )
        self.compare_window.show()

    def create_fqv_window(self):
        self.create_fqv_window = CreateFQV()
        self.create_fqv_window.show()

    def create_manual_inspection_window(self):
        self.create_manual_inspection_window = CreateManualInspection()
        self.create_manual_inspection_window.show()

    @pyqtSlot()
    def random_fqv_button(self):
        inspectors = {}
        for container in range(CONTAINER_START, CONTAINER_END + 1):
            results = {f"container_{container}": random.randint(0, 10)}
            inspectors.update(results)

        self.saveFileDialog()
        if self.fileName != "":
            write_pickle_file(self.fileName, inspectors)

    @pyqtSlot()
    def random_man_inspect_button(self):
        inspectors = {}
        for container in range(CONTAINER_START, CONTAINER_END + 1):
            results = {
                f"container_{container}": [random.randint(0, 10) for _ in range(5)]
            }
            inspectors.update(results)

        self.saveFileDialog()
        if self.fileName != "":
            write_pickle_file(self.fileName, inspectors)

    def saveFileDialog(self):
        self.fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Save FQV or Machine results",
            "",
            "Pickle Files (*.pkl)",
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
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open FQV or Machine results",
            "",
            "All Files (*);;Pickle (*.pkl);;XML (*.xml)",
        )

        self.results_title = ""
        if fileName:
            self.load_fqv(fileName)
            self.results_title = os.path.basename(fileName)

    def load_fqv(self, fileName):
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
            self.manual_results = {}  # Clear existing results
            with open(fileName, "rt") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row, values in enumerate(reader):
                    container_key = f"container_{row + 1}"
                    inspector_results = [int(value) for value in values]
                    avg_value = round((sum(inspector_results) / 5))
                    self.manual_results[container_key] = avg_value
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
                    if container_number > CONTAINER_END:
                        break
                    self.machine_results[f"container_{container_number}"] = int(
                        type_tag.text
                    )
        return self.machine_results


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
        export_table_to_csv(self.table)


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
        self.table = QTableWidget()
        self.table.setRowCount(CONTAINER_END)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Manual", "Machine"])

        for container in range(CONTAINER_START, CONTAINER_END + 1):
            manual_item = QTableWidgetItem(
                str(self.manual_results.get(f"container_{container}", 0))
            )
            machine_item = QTableWidgetItem(
                str(self.machine_results.get(f"container_{container}", 0))
            )

            manual_item.setFlags(manual_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            machine_item.setFlags(machine_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.table.setItem(container - 1, 0, manual_item)
            self.table.setItem(container - 1, 1, machine_item)

            if int(manual_item.text()) > 7:
                manual_item.setData(Qt.ItemDataRole.UserRole, "high_value")
            if int(machine_item.text()) > 7:
                machine_item.setData(Qt.ItemDataRole.UserRole, "high_value")

            self.manual_containers[f"container_{container}"] = int(manual_item.text())
            self.machine_containers[f"container_{container}"] = int(machine_item.text())

        self.table.setItemDelegate(ColourCell())
        self.show_efficiency_button = QPushButton("Calculate efficiency", self)
        self.show_efficiency_button.clicked.connect(self.show_efficiency)
        self.export_button = QPushButton("Export (csv)", self)
        self.export_button.clicked.connect(self.export_compare_results_data)
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.show_efficiency_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.close_button)
        self.compare_results_widget.addWidget(self.table)
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

    def export_compare_results_data(self):
        export_table_to_csv(self.table)


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


class CreateManualInspection(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 500, 600)
        self.setWindowTitle("Create Manual Inspection Data")
        self.inspection_results = {}
        self.inspection_containers = {}
        self.CreateManualInspectionUI()

    def CreateManualInspectionUI(self):
        self.inspection_widget = QVBoxLayout()

        table = QTableWidget()
        table.setRowCount(CONTAINER_END)
        table.setColumnCount(5)  # One column for each inspector
        table.setHorizontalHeaderLabels(
            ["Inspector 1", "Inspector 2", "Inspector 3", "Inspector 4", "Inspector 5"]
        )

        for container in range(CONTAINER_START, CONTAINER_END + 1):
            self.inspection_containers[container] = [
                QTableWidgetItem("0") for _ in range(5)
            ]

            for i in range(5):
                table.setItem(
                    container - 1, i, self.inspection_containers[container][i]
                )

        table.setItemDelegate(ColourCell())

        title_label = QLabel()
        title_label.setText("Create Manual Inspection Data")
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_inspection_results)

        self.open_button = QPushButton("Open", self)
        self.open_button.clicked.connect(self.open_file)

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)

        self.inspection_widget.addWidget(title_label)
        self.inspection_widget.addWidget(table)
        self.inspection_widget.addWidget(self.save_button)
        self.inspection_widget.addWidget(self.open_button)
        self.inspection_widget.addWidget(self.close_button)

        self.setLayout(self.inspection_widget)

    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open Manual Inspection Data",
            "",
            "Pickle Files (*.pkl)",
        )

        if fileName:
            try:
                manual_results = read_pickle_file(fileName)
                for container in range(CONTAINER_START, CONTAINER_END + 1):
                    inspector_results = manual_results.get(
                        f"container_{container}", [0, 0, 0, 0, 0]
                    )
                    for i in range(5):
                        self.inspection_containers[container][i].setText(
                            str(inspector_results[i])
                        )
            except (pickle.UnpicklingError, KeyError):
                pass

    def save_inspection_results(self):
        for container in range(CONTAINER_START, CONTAINER_END + 1):
            inspector_results = [
                int(self.inspection_containers[container][i].text()) for i in range(5)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec())
