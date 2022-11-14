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
If you don't wish to create your own dataset, but just visualize, you just need to use the RiskVisualizer. You will have access to premade simulations of up to 50vs50.
The basic usage is to first install the requirements (PyPlot), and then just use the program:
```
pip install -R requirements.txt
python RiskVisualizer.py
```
After that, the program will ask of what you want to simulate, which should be pretty straight forward!
Good luck!

## Graph composition
So, the graph made basically shows the probability of win for either side, and having atleast x troops remaining (negative values for defender). The p in the legend is the probability of attacker victory.
![obraz](https://user-images.githubusercontent.com/13346371/201528487-ef03a409-b316-43e3-b05b-ae04df4c93c3.png)
For exmaple in the example here, there's a fight of 2 attacker troops vs 1 defender troop, with a 75,41% chance of the attacker winning. There's a 75,41% chance of the attacker having atleast one troop remaining, and about 60% chance of him having 2 troops remaining.

## Fun statistics
Having that in mind, we can make some interesting statistics

### Equal amounts of attackers and defenders
![obraz](https://user-images.githubusercontent.com/13346371/201557616-ca6ec418-061b-4ea9-8d97-e185e9df1dab.png)
As we see here, with an equal amount of attackers and defenders, the defender has an advantage up until 5v5, where the probability of the attacker winning is 50,83%.

### Defender advantage - 1 troop
![obraz](https://user-images.githubusercontent.com/13346371/201557682-decac747-982c-4b72-8940-32ffb2751076.png)

Here, the defender has one more troop than the attacker. We see the attacker having a quite low win probability up until 11v12, where he will win 50,54% of the time.

### Defender advantage - 2 troops
![obraz](https://user-images.githubusercontent.com/13346371/201557708-092629f9-ab75-4d7d-af03-59f762f8eca4.png)

The same trend can be observed here, up until 17 vs 19

### Defender advantage - 3 troops
![obraz](https://user-images.githubusercontent.com/13346371/201557805-57ce810e-f05a-4812-b3e4-69f2e9201784.png)

Same here, up until 23vs26.

### Attacker advantage
![obraz](https://user-images.githubusercontent.com/13346371/201557852-a9b4ea18-34cf-4577-a299-ffc73c391026.png)
As we see, with the attacker having one troop advantage, he willbasically always have the odds on his side.
