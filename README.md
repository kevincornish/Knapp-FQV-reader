# Knapp / FQV Reader

Knapp / FQV Reader is a python application that will open pre-generated FQV or Knapp machine run files. A comparison of the machine vs manual inspection can be viewed and a bar chart with the machine vs manual efficiency can be generated.

![GUI](/img/GUI.gif?raw=true "GUI")

## Knapp
The Knapp theory, introduced by Dr. Julius Z. Knapp over two decades ago, enables an objective comparison and validation of particulate inspection techniques. This theory is grounded in the understanding that particulate inspection, whether performed by humans or automated systems, is inherently probabilistic rather than deterministic. This probabilistic nature is attributed to factors such as the size, typology, and contrast of encountered particulates.

The primary objective of Knapp's theory is to establish a mathematical method for demonstrating the probability of detecting foreign particles in pharmaceutical products. It has found widespread use in assessing the efficiency of automatic inspection systems compared to traditional manual visual inspection. Recognized by the European Pharmacopoeia and the American PDA/FDA, this method serves as an effective means to calibrate fully automatic inspection systems, ensuring comparable inspection efficiency to manual systems in pharmaceutical companies.

The underlying principle focuses on statistically evaluating the efficiency of rejected containers that exhibit defects of a certain statistical value, considering particles of various dimensions and types.

## FQV (Factor Quality Visual)
The FQV process involves the following steps:

1. Number each container (from 1 to 250)
2. Record the identification number for the rejected containers
3. Select five operators with inspection capabilities equivalent to the factory's standard quality.
4. Each operator inspects the set ten times, totaling 50 inspections per batch.
5. After each inspection, record the rejects
6. After 10 inspections, record the FQV for each container
7. Calculate the number of times each container has been rejected by the five operators
8. Calculate the FQV for each container using the formula:

    FQV (container number. xxx) = (n/N) * 10

    n: Number of times the container has been rejected

    N: Total number of inspections

    Example:
    FQV (container number. 51) = (41/50) * 10 = 8.2

The Knapp method emphasizes containers 7 to 10 for efficiency calculations. Containers with FQV categories 0 to 3 are considered good, while categories 4 to 6 constitute a grey zone, indicating instability. Ideally, the grey zone should be minimal or nonexistent.

## FQA (Factor Quality Automatic)
The FQA is defined by an automatic inspection system:

1. Load the Knapp batch (250 containers) on the machine. The containers will be loaded in subbatches corresponding of the number of spindles, i.e. with 40 spindles machines the containers will be loaded in order starting from the position 1 to 40, than 41 to 80, and so on. 

2. Run inspection (usually 10 inspections per run).

## FQA vs FQV (Efficiency calculation)

The FQA categories included between 7 and 10 (by automatic inspection) are considered for the final calculation of rejection efficiency.

1. Calculate the sum of the FQA:

FQA(7,10) = sum FQA i

i=1

FQA = quality factor obtained by automatic inspection

i = containers included in the reject area (7 ≤ FQA ≤ 10)

2. Calculate the sum of the FQV:

FQV = Σ FQV i

i=1

FQV = quality factor obtained by traditional visual inspection

i = containers included in the reject area (7 ≤ FQA ≤ 10)

The ratio between the above sum totals determines the efficiency of the visual inspection related to the automatic inspection results: if this ratio is less than 100% the visual inspection values may contain some non-detected particles.

[FQV/FQA (7,10)] x 100


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