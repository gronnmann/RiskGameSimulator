import csv
import matplotlib.pyplot as plt
import matplotlib
import os


def addAllValuesBelow(items):
    print(f"Items: {items}")

    fixed_pairs = []

    sorted_current = (sorted(items, key=lambda x: x[0]))

    # return sorted_current
    print(sorted_current)

    x_list = [x[0] for x in sorted_current]
    y_list = [x[1] for x in sorted_current]

    for i, x in enumerate(sorted_current):
        print(f"current: {i} : {y_list[-(i+1)]}")

        if x_list[0] < 0:
            fixed_pairs.append(
                (
                    x_list[i],
                    sum(y_list[0:(i+1)])
                )
            )
        else:
            fixed_pairs.append(
                (
                    x_list[i],
                    sum(y_list[i:])
                )
            )
        # print(f"{i}: {x} : {fixed_pairs} : {sorted_current}")

    # print(new_list)

    return fixed_pairs


def plotPlotWith(attacker: int, defender: int, plot):
    plot_file_name = f"simulation_data/odds_{attacker}_{defender}.csv"

    if not os.path.exists(plot_file_name):
        return False

    with open(plot_file_name) as data_file:
        csv_file = csv.reader(data_file, delimiter=",")

        attackerChance = 0.0

        value_pairs_positive = []
        value_pairs_negative = []

        for row in csv_file:
            # print(row)
            if int(row[0]) > 0:
                attackerChance += float(row[1])
                value_pairs_positive.append((int(row[0]), 100 * float(row[1])))
            else:
                value_pairs_negative.append((int(row[0]), 100 * float(row[1])))

        y_positive_corrected = value_pairs_positive
        if len(value_pairs_positive) > 1:
            y_positive_corrected = addAllValuesBelow(value_pairs_positive)
        y_negative_corrected = value_pairs_negative
        if len(value_pairs_negative) > 1:
            y_negative_corrected = addAllValuesBelow(value_pairs_negative)

        # y_negative_corrected.reverse()

        total_graph = y_negative_corrected + y_positive_corrected
        # print(y_total_fixed)

        # print(plt_x)
        # print(plt_y)
        #
        plot.plot([x[0] for x in total_graph], [y[1] for y in total_graph], 'o-',
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

        plt.xticks(range(-1 * int(advantage_range[1]), int(advantage_range[1]) + 1, 1))

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
