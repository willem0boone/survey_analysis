import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

csv_file = "C:/Users/willem.boone/Documents/projects/MARBEFES/analyse_survey/survey_responses.csv"
df = pd.read_csv(csv_file, sep=";", encoding='latin-1')
with open("column_mapping.json", "r", encoding='utf-8') as f:
    column_mapping = json.load(f)
df.rename(columns=column_mapping, inplace=True)


def plot_demographics(data, title="Demographic Distribution by Age and Gender"):
    age_gender_counts = data.groupby(["age", "gender"]).size().unstack(fill_value=0)
    vrouw_counts = age_gender_counts.get("Vrouw", pd.Series(dtype=int))
    man_counts = age_gender_counts.get("Man", pd.Series(dtype=int))
    all_age_categories = age_gender_counts.index
    vrouw_counts = vrouw_counts.reindex(all_age_categories, fill_value=0)
    man_counts = man_counts.reindex(all_age_categories, fill_value=0)
    plt.figure(figsize=(10, 6))
    bar_height = 1.0
    plt.barh(vrouw_counts.index, vrouw_counts.values, color='red',
             edgecolor='black', label='Female (Vrouw)', height=bar_height)
    plt.barh(man_counts.index, -man_counts.values, color='blue',
             edgecolor='black', label='Male (Man)', height=bar_height)
    plt.xlim(-100, 100)
    plt.xlabel('Number of Respondents')
    plt.ylabel('Age Category')
    plt.title(title)
    x_ticks = plt.xticks()[0]
    plt.xticks(x_ticks, [abs(int(tick)) for tick in x_ticks])
    plt.grid(axis='x', linestyle='--', alpha=0.7, linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_demographics(df, title=f"Demographic Distribution")

    municipalities = df['municipality'].unique()
    for municipality in municipalities:
        municipality_data = df[df['municipality'] == municipality]
        plot_demographics(municipality_data,
                          title=f"Demographic Distribution in {municipality}")
