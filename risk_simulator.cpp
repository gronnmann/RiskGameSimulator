#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <vector>
#include <fstream>
#include <string>

using namespace std;

int rollDice(){
    return rand() % 6 + 1;
}
// returns 0 for attacker victory, 1 for tie, 2 for defender victory
// returns [attackerLost, defenderLost]
vector<int> simulateSingleAttack(int attackerDices, int defenderDices){
    vector<int> attacker, defender;

    for (int i = 0; i < attackerDices; i++){
        attacker.emplace_back(rollDice());
    }

    for (int i = 0; i < defenderDices; i++){
        defender.emplace_back(rollDice());
    }

    std::sort(attacker.begin(), attacker.end());
    std::sort(defender.begin(), defender.end());

    std::reverse(attacker.begin(), attacker.end());
    std::reverse(defender.begin(), defender.end());

    int attackerPoints = 0, defenderPoints = 0;

    int rolledDices = (attackerDices > defenderDices) ? defenderDices : attackerDices;


    for (int i = 0; i < rolledDices; i++){
        int attackerRoll = attacker.at(i);
        int defenderRoll = defender.at(i);

        if (attackerRoll > defenderRoll){
            attackerPoints++;
//            cout << attackerRoll << " - " << defenderRoll << " : ATTACKER VICTORY\n";
        }
        else{
            defenderPoints++;
//            cout << attackerRoll << " - " << defenderRoll << " : DEFENDER VICTORY\n";
        }
    }


    vector<int> results;
    results.emplace_back(defenderPoints);
    results.emplace_back(attackerPoints);

    return results;
}


//void simulateForVariables(int n_runs, int attackerDices, int defenderDices){
//
//    int results[3] = {0, 0, 0};
//
//
//    for (int i = 0; i < n_runs; i++){
//        results[simulateSingleAttack(attackerDices, defenderDices)] += 1;
//    }
//
//    float resultChances[3];
//    for (int i = 0; i < 3; i++){
//        resultChances[i] = float(results[i]) / float(n_runs);
//    }
//
//    printf("\n");
//    printf("Attack with %i attacker, %i defender, n_runs = %i\n", attackerDices, defenderDices, n_runs);
//    printf("Attacker victory: %i (chance %f)\n", results[0], resultChances[0]);
//    printf("Tie: %i (chance %f)\n", results[1], resultChances[1]);
//    printf("Defender victory: %i (chance %f)\n", results[2], resultChances[2]);
//    printf("\n");
//}

// Returns vector<int> with [attackerWon, attackerRemainingPieces, defenderRemainingPieces]
vector<int> simulateAttack(int attackerPieces, int defenderPieces){
    while (true){
        int attackerUsed = attackerPieces > 3 ? 3 : attackerPieces;
        int defenderUsed = defenderPieces > 2 ? 2 : defenderPieces;

        vector<int> attackResult = simulateSingleAttack(attackerUsed, defenderUsed);

        attackerPieces -= attackResult.at(0);
        defenderPieces -= attackResult.at(1);

        if (attackerPieces == 0 || defenderPieces == 0){
            int attackerWon = (attackerPieces == 0) ? 0 : 1;

            vector<int> simulationResults;
            simulationResults.emplace_back(attackerWon);
            simulationResults.emplace_back((attackerPieces == 0) ? defenderPieces : attackerPieces);
            return simulationResults;
        }
    }
}

void simulateFightOdds(int attackerPieces, int defenderPieces, int n_runs, string savedFolder){

    int attackerWon[attackerPieces];
    int defenderWon[defenderPieces];
    int attacksWon = 0, defensesWon = 0;



    for (int i = 0; i < attackerPieces; i++){
        attackerWon[i] = 0;
    }

    for (int i = 0; i < defenderPieces; i++){
        defenderWon[i] = 0;
    }

    defenderWon[1] ++;

    for (int i = 0; i < n_runs; i++){
        vector<int> attack = simulateAttack(attackerPieces, defenderPieces);

        int attackerWonResult = attack.at(0);
        int remainingPieces = attack.at(1);

        if (attackerWonResult == 1){
            // -1 because will be added 1 later
            attackerWon[remainingPieces-1] += 1;
            attacksWon++;
        }else{
            defenderWon[remainingPieces-1] += 1;
            defensesWon++;
        }
    }

    float attackerOdds = float(attacksWon) / float(n_runs);
    float defenderOdds = float(defensesWon) / float(n_runs);

    printf("\n");
    printf("Attacker victory: (odds: %f)\n", attackerOdds);

    ofstream oddsFile(savedFolder + "/odds_" + to_string(attackerPieces) + "_" + to_string(defenderPieces) + ".csv");

    for (int i = 0; i < attackerPieces; i++){
        int runsWithXRemaining = attackerWon[i];

        float chance = float(runsWithXRemaining) / float(n_runs);

        printf("ATTACKER WON: %i pieces remaining: %i (chance: %f)\n", i+1, runsWithXRemaining, chance);

        oddsFile << i+1 << "," << chance << "\n";
    }

    printf("\nDefender victory: (odds: %f)\n", defenderOdds);
    for (int i = 0; i < defenderPieces; i++){
        int runsWithXRemaining = defenderWon[i];

        float chance = float(runsWithXRemaining) / float(n_runs);

        printf("DEFENDER WON: %i pieces remaining: %i (chance: %f)\n", i+1, runsWithXRemaining, chance);

        oddsFile << -1*(i+1) << "," << chance << "\n";
    }

    printf("\n");

    oddsFile.close();
}



int main(int argc, char *args[]) {
    bool useDefault = false;
    int args_n_runs = 0, args_max_attackers = 0, args_max_defenders = 0;
    string args_output_folder = "";
    if (argc < 3){
        printf("Using default (args_max_attackers = 50, args_max_defenders = 50, args_n_runs = 500000) as no arguments specified.\n");
        printf("Usage with arguments: ./RiskSimulator.exe {args_output_folder} {args_max_attackers} {args_max_defenders} {args_n_runs}\n");
        useDefault = true;
    }
    else{
        args_n_runs = atoi(args[4]);
        args_max_attackers = atoi(args[2]);
        args_max_defenders = atoi(args[3]);
        args_output_folder = args[1];

        //Erorr or 0 value which doesnt make sense
        if (args_n_runs == 0 || args_max_attackers == 0 || args_max_defenders == 0){
            printf("Error: One of number arguments was either not number or 0.\n");
            printf("Output folder: %s, args_max_attackers: %i, args_max_defenders: %i, args_n_runs: %i\n", args_output_folder.c_str(), args_max_attackers, args_max_defenders, args_n_runs);
            printf("Returning to defaults...");
            useDefault = true;
        }
    }

    int n_runs = useDefault ? 500000 :  args_n_runs;
    int max_attackers = useDefault ? 50 : args_max_attackers;
    int max_defenders = useDefault ? 50: args_max_defenders;
    string output_folder = useDefault ? "../simulation_data" : args_output_folder;


    for (int i = 1; i <= max_attackers; i++){
        for (int j = 1; j <= max_defenders; j++){
            printf("Simulating fight with attackers = %i, defenders = %i", i, j);
            simulateFightOdds(i, j, n_runs, output_folder);
        }
    }

    return 0;
}
