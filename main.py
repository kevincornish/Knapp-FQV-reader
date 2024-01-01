import random
import sys
from utils import (
    show_confirmation,
    write_pickle_file,
)
from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QTabWidget,
)
from PyQt6.QtCore import pyqtSlot
from widgets.compare_results import CompareResults
from widgets.create_fqv import CreateFQV
from widgets.load_fqv import LoadFQV
from widgets.create_manual_inspection import CreateManualInspection
from widgets.load_manual_inspection import LoadManualInspection
from widgets.load_machine_results import LoadMachineResults
from constants import CONTAINER_START, CONTAINER_END


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec())
