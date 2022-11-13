import csv
import matplotlib.pyplot as plt
import matplotlib
import os


def addAllValuesBelow(items):
    new_list = []

    sorted_current = None
    if items[1] > 0:
        sorted_current = sorted(items, reverse=True)
    else:
        sorted_current = sorted(items)

    print(sorted_current)
    for i, x in enumerate(sorted_current):
        sliced_array = sorted_current[i:]

        print(f"{i}: {x} : {sum(sliced_array)} : {sliced_array} : {sorted_current}")

        new_list.append(sum(sliced_array))

    # print(new_list)

    return new_list


def plotPlotWith(attacker: int, defender: int, plot):
    plot_file_name = f"simulation_data/odds_{attacker}_{defender}.csv"

    if not os.path.exists(plot_file_name):
        return False

    with open(plot_file_name) as data_file:
        csv_file = csv.reader(data_file, delimiter=",")

        plt_x = []
        plt_y = []
        # print(f"{attacker} attackers, {defender} defendeers")

        attackerChance = 0.0

        y_positive = []
        y_negative = []

        for row in csv_file:
            # print(row)
            plt_x.append(int(row[0]))
            if int(row[0]) > 0:
                attackerChance += float(row[1])
                y_positive.append(100 * float(row[1]))
            else:
                y_negative.append(100 * float(row[1]))

            plt_y.append(100 * float(row[1]))

        # plt_x.reverse()
        # plt_y.reverse()

        y_positive_corrected = y_positive
        if len(y_positive) > 1:
            y_positive_corrected = addAllValuesBelow(y_positive)
        y_negative_corrected = y_negative
        if len(y_negative) > 1:
            y_negative_corrected = addAllValuesBelow(y_negative)

        y_negative_corrected.reverse()

        y_total_fixed = y_negative_corrected + y_positive_corrected
        # print(y_total_fixed)

        # print(plt_x)
        # print(plt_y)
        #
        plot.plot(sorted(plt_x), y_total_fixed, 'o-',
                  label=f"{attacker} attackers, {defender} defenders, p={attackerChance:.4f}")

        return True


# for i in attack:
#     for d in defense:
#         plotPlotWith(i, d)

def main():
    print("""Viewing Risk statistics. Modes:
    1 - Range
    2 - Specific scenarioes
    3 - Attacker/defender n advantage""")

    matplotlib.use('TkAgg')
    fig = plt.figure()
    fig_ax = fig.add_subplot(1, 1, 1)

    mode = input("Please specify mode: ")
    if mode == "1":
        attacker_range = input("Please specify attacker range (start-end): ").split("-")
        defender_range = input("Please specify defender range (start-end): ").split("-")

        attack_range = range(int(attacker_range[0]), int(attacker_range[1]) + 1, 1)
        defense_range = range(int(defender_range[0]), int(defender_range[1]) + 1, 1)

        print(f"{attack_range} : {defense_range}")
        for a in attack_range:
            for d in defense_range:
                succ = plotPlotWith(a, d, fig_ax)
                if not succ:
                    print(f"Found no data for attacker: {a}, defender: {d}. Exiting.")
                    exit(0)

                plt.xticks(range(max(defense_range) * -1, max(attack_range) + 1, 1))

    elif mode == "2":
        scenarioes = input("Please specify scenarioes attackers:defenders, separated by comma: ").split(",")

        min_def = 100000
        max_att = -10000
        for scenario in scenarioes:
            scenario_split = scenario.split(":")
            a, d = int(scenario_split[0]), int(scenario_split[1])

            if -d < min_def:
                min_def = -d
            if a > max_att:
                max_att = a

            succ = plotPlotWith(a, d, fig_ax)
            if not succ:
                print(f"Found no data for attacker: {a}, defender: {d}. Exiting.")
                exit(0)
        plt.xticks(range(min_def, max_att + 1, 1))
    elif mode == "3":
        advantage = input("Please specify defender advantage (use negative numbers for defender): and range for "
                          "attacker numbers (for example 1|1:20): ").split("|")
        advantage_range = advantage[1].split(":")

        for a in range(int(advantage_range[0]), int(advantage_range[1])):
            d = a + int(advantage[0])

            succ = plotPlotWith(a, d, fig_ax)

            if not succ:
                print(f"Found no data for attacker: {a}, defender: {d}. Exiting.")
                exit(0)

        plt.xticks(range(-1*int(advantage_range[1]), int(advantage_range[1]) + 1, 1))

    else:
        print("Wrong mode entered. Exiting...")

    plt.legend(loc="upper right", prop={'size': 6})
    plt.title("Risk simulation")
    plt.xlabel("Troops remaining. Negative values = defense won")
    plt.ylabel("Probability")
    plt.yticks(range(0, 105, 5))

    plt.axvline(x=0, linewidth=5, c="black")

    plt.show()


main()
