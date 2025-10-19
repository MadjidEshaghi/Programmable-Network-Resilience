A Unifying Framework for Network Resilience based on Information Flow

This repository contains the official Python implementation and data for the paper: **"
A Unifying Framework for Network Resilience based on Information Flow
"**, submitted to *Nature*.

**Authors:** Madjid Eshaghi Gordji,
**Affiliation:** Department of Mathematics, Semnan University
**Preprint:** [Gordji
## 📝 Overview

This research introduces a novel mathematical framework for designing and analyzing programmable network resilience. We propose a calculus based on targeted edge rewiring that optimizes a network's structure against cascading failures while preserving its core functionalities. Our method allows for a precise trade-off between resilience enhancement and the economic cost of modifications.

The key findings demonstrate that our algorithm can significantly increase the resilience of critical infrastructures, such as power grids and communication networks, potentially preventing economic losses estimated at $150-200 billion annually in the U.S. alone from power outages.

This repository provides the source code to reproduce the simulations and figures presented in the paper.





.





## 🏛️ Repository Structure
Programmable-Network-Resilience/

│

├── 📜 README.md # You are here

├── ⚖️ LICENSE # MIT License

├── 📦 requirements.txt # Python dependencies

│

├── 📂 src/ # Main source code

│ ├── 🛠️ resilience_calculator.py # Core resilience algorithm and rewiring logic

│ ├── 📊 simulation_runner.py # Main script to run experiments

│ └── 🎨 plotting.py # Functions for generating plots

│

└── 📂 data/ # Network datasets used in the study

├── 🌐 power_grid.gml # U.S. Power Grid dataset

└── README.md # Data sources and descriptions

⚙️ Installation & Setup
To run the simulations, you need Python 3.8+ and the libraries listed in requirements.txt.

Clone the repository:

content_copy
bash
    git clone https://github.com/MadjidEshaghi/Programmable-Network-Resilience.git
    cd Programmable-Network-Resilience
Create a virtual environment (recommended):

content_copy
bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required packages:

content_copy
bash
    pip install -r requirements.txt
🚀 How to Run the Simulations
The main experiments can be reproduced by running the simulation_runner.py script from the src directory.

bash

cd src

python simulation_runner.py

This script will:

Load the network data from the /data directory.
Run the resilience optimization algorithm.
Perform cascading failure simulations on both the original and the rewired networks.
Save the results (e.g., plots and metrics) into a new results directory.
You can modify the parameters inside simulation_runner.py to experiment with different settings.

📚 Citation
If you use this code or the findings from our paper in your research, please cite us:

bibtex

@article{GordjiShahini2025Nature,

title = {A Calculus for Programmable Network Resilience},
.
