import pandas as pd
import matplotlib.pyplot as plt
import os
import json

OUT_PATH = "categorical"

if not os.path.exists(OUT_PATH):
    os.makedirs(OUT_PATH)


def plot_bin_graph(csv_file,
                   name,
                   show=False,
                   save=True,
                   exclude_all_zeros=True,
                   specify_order=None):

    df = pd.read_csv(csv_file,
                     usecols=lambda col: pd.notna(col) and not col.startswith(
                         'Unnamed')).dropna(how='all')

    valid_columns = [col for col in df.columns if col != 'Other']
    df = df[valid_columns]

    if exclude_all_zeros:
        df = df[(df != 0).any(axis=1)]

    activity_counts = df.sum()

    if specify_order and isinstance(specify_order, list):
        activity_counts = activity_counts.reindex(specify_order).dropna()
    else:
        activity_counts = activity_counts.sort_values(ascending=True)

    plt.figure(figsize=(14, 8))
    ax = activity_counts.plot(kind='barh',
                              color='#216477',
                              edgecolor='none',
                              alpha=0.8)

    def wrap_text(label, max_length=30):
        words = label.split()
        lines = []
        current_line = []
        current_length = 0
        for word in words:
            if current_length + len(word) + (
                    len(current_line) > 0) > max_length:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
            else:
                current_line.append(word)
                current_length += len(word) + 1
        if current_line:
            lines.append(" ".join(current_line))
        return "\n".join(lines)

    y_labels = [wrap_text(label) for label in activity_counts.index]

    ax.set_yticklabels(y_labels, fontsize=10, ha='right')
    ax.tick_params(axis='y', length=0)

    plt.subplots_adjust(left=0.3)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.xaxis.grid(True, linestyle='--', alpha=0.7)

    plt.title(label=name, fontsize=16)

    for index, value in enumerate(activity_counts.values):
        ax.text(value + 1, index, str(value), va='center', fontsize=10)

    if show:
        plt.show()
    if save:
        plt.savefig(os.path.join(OUT_PATH, f"{name}.png"))


if __name__ == "__main__":
    csv = ("C:/Users/willem.boone/Documents/projects/MARBEFES/analyse_survey/"
           "analyse/multi_choice_revision/split_activities.csv")

    plot_bin_graph(csv, name='Activities')
    # -------------------------------------------------------------------------
    csv = ("C:/Users/willem.boone/Documents/projects/MARBEFES/analyse_survey/"
           "analyse/multi_choice_revision/split_connection_type.csv")

    plot_bin_graph(csv, name='Coastal connection')
    # -------------------------------------------------------------------------
    csv = ("C:/Users/willem.boone/Documents/projects/MARBEFES/analyse_survey/"
           "analyse/multi_choice_revision/split_influence_experience.csv")

    plot_bin_graph(csv, name='Influencing factors')
    # -------------------------------------------------------------------------
    csv = ("C:/Users/willem.boone/Documents/projects/MARBEFES/analyse_survey/"
           "analyse/multi_choice_revision/split_motivation.csv")

    plot_bin_graph(csv, name='Motivation')
    # -------------------------------------------------------------------------
    csv = ("C:/Users/willem.boone/Documents/projects/MARBEFES/analyse_survey/"
           "analyse/multi_choice_revision/split_visit_frequency.csv")
    with open("mappings/frequency_values.json", "r", encoding="utf-8") as f:
        frequency_values = json.load(f)

    plot_bin_graph(csv,
                   name='Visit frequency',
                   exclude_all_zeros=True,
                   specify_order=list(reversed(frequency_values))
                   )

    # -------------------------------------------------------------------------
    csv = ("C:/Users/willem.boone/Documents/projects/MARBEFES/analyse_survey/"
           "analyse/multi_choice_revision/activity_nature_influences.csv")

    plot_bin_graph(csv, name='Influences on activity nature')

