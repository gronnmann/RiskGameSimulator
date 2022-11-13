# RiskGameSimulator
Simulator to find probability of victory in the board game Risk

It uses C++ to simulate and therefore generate odds for different outcomes.
Pre-generated data has been made in ```simulation_data```, generating upto 50 attacking troops vs 50 defending tropps, and with n_runs at 500 000.
## RiskSimulator
The general usage for the RiskSimulator that generates the dataset is:
```
RiskSimulator.exe {output folder} {max attackers to simulate} {max defenders to simulate} {n_runs}
```
Please make sure the {output_folder} exists, or the program won't run.

## Risk Visualizer
If you don't wish to create your own dataset, but just visualize, you just need to use the RiskVisualizer.
The basic usage is to first install the requirements (PyPlot), and then just use the program:
```
pip install -R requirements.txt
python RiskVisualizer.py
```
After that, the program will ask of what you want to simulate, which should be pretty straight forward!
Good luck!
