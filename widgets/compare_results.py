from utils import (
    export_table_to_csv,
    ColourCell,
)
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from constants import CONTAINER_START, CONTAINER_END


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
        self.setGeometry(600, 100, 700, 500)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.manual_containers = manual_results or {}
        self.machine_containers = machine_results or {}

        self.efficiency_canvas = FigureCanvas(Figure(figsize=(8, 6), dpi=100))

        self.save_chart_button = QPushButton("Save Chart", self)
        self.save_chart_button.clicked.connect(self.save_chart)
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)

        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.efficiency_canvas)
        self.central_layout.addWidget(self.save_chart_button)
        self.central_layout.addWidget(self.close_button)

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

    def save_chart(self):
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix("png")
        file_name, _ = file_dialog.getSaveFileName(
            self, "Save Chart as Image", "", "Images (*.png);;All Files (*)"
        )

        if file_name:
            self.efficiency_canvas.figure.savefig(file_name)
