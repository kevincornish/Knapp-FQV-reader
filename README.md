# Knapp / FQV Reader

Knapp / FQV Reader is a Python application designed to analyze and compare pre-generated manual inspection FQV (Factor Quality Visual) and Knapp machine run (Factor Quality Automatic) files. This tool provides insights into the efficiency of inspections conducted by both manual operators and automated machines.

![GUI](/img/GUI.gif?raw=true "GUI")

## Knapp
The Knapp theory, developed by Dr. Julius Z. Knapp, provides a method for objectively comparing particulate inspection techniques. It recognizes the inherent probabilistic nature of inspections, influenced by factors like particle size and contrast. Widely accepted by pharmaceutical standards, Knapp's theory is crucial for assessing the efficiency of automatic inspection systems against manual visual inspection.

## FQV (Factor Quality Visual)
The FQV process involves the following steps:

1. **Container Identification:** Number containers from 1 to 250.
2. **Operator Selection:** Choose five operators with standard inspection capabilities.
3. **Inspection Process:** Each operator inspects the set ten times, totaling 50 inspections.
4. **Record Rejects:** After each inspection, record rejects.
5. **Calculate FQV:** After ten inspections, calculate FQV for each container using the formula: FQV = (n/N) * 10, where n is the number of rejections, and N is the total inspections.
    - Example: FQV (container 51) = (41/50) * 10 = 8.2.
6. Efficiency Emphasis: Efficiency calculations focus on containers 7 to 10. Categories 0 to 3 are good, 4 to 6 constitute a grey zone, ideally minimal.

## FQA (Factor Quality Automatic)
The FQA is defined by an automatic inspection system:

1. **Batch Loading:** Load 250 containers in subbatches based on the machine's spindles (e.g., 40 spindles load containers 1 to 40, 41 to 80, and so on).

2. **Run Inspection:** Perform machine inspection with typically 10 inspections per run.

## FQA vs FQV (Efficiency calculation)

1. **Calculate FQA Sum:** Sum FQA values for containers with automatic inspection categories between 7 and 10.
    - Formula: FQA(7,10) = Σ FQA_i, where i represents containers in the reject area (7 ≤ FQA ≤ 10).
    
2. **Calculate FQV Sum:** Sum FQV values for visually inspected containers with categories between 7 and 10.
    - Formula: FQV = Σ FQV_i, where i represents containers in the reject area (7 ≤ FQA ≤ 10).

2. **Efficiency Ratio:** Determine visual inspection efficiency related to automatic inspection results. If the ratio is less than 100%, visual inspection may miss some particles.
    - Formula: [FQV/FQA (7,10)] x 100.

## Installation

To run the Knapp / FQV Reader, you'll need Python 3. Create new Python env

```bash
python -m venv env
```

Activate env

Linux
```bash
source env/bin/activate
```

Windows
```ps1
.\env\Scripts\Activate.ps1
```

Install Requirements

```bash
pip install -r requirements.txt
```

## Usage

To use the Knapp / FQV Reader, run the `main.py` script in a terminal or command prompt and wait for the graphical user interface to load.

### Load FQV (Manual)

You can load an exisiting FQV file, either in .xml, .pkl or .csv formats, if a pickle file is loaded and contains multiple inspections per container, it will automatically perform the following sum to calculate the FQV per container ``` round((sum(value) / 50) * 10) ```

### Load FQA (Machine)

You can load an existing FQA file in .xml format, it will perform the following tree search to find the machine results for each container 
``` ParticlesInspection/Sample/TotReject ```

### Create FQV or Random FQV

When calling the function to create FQV, you have the option to open a small dialog to specify the number of containers you need. The application will create a table with 0s for the specified number of containers and fill the remaining ones up to 250 with -1.

### Create Manual Inspection Data

You can create manual inspection data using the CreateManualInspection interface. The table allows you to input inspection results for five inspectors across 250 containers. You can then use this to open in the FQV reader which wil automatically perform the sum required for FQV generation.

### Compare Results

The CompareResults interface allows you to compare manual and machine inspection results. It displays a table with two columns: one for manual results and one for machine results. The efficiency of the inspections is also calculated and displayed in a bar chart in the efficiency window comparing manual vs machine efficiency.