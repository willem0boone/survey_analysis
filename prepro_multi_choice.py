import json
import os.path

import pandas as pd

PATH = "multi_choice"


def split_row(row, predefined_values):
    row_values = row.split(';')
    columns = {value: 0 for value in
               predefined_values}
    other = []
    for value in row_values:
        value = value.strip()
        if value in predefined_values:
            columns[value] = 1
        else:
            other.append(value)
    columns['Other'] = '; '.join(
        other)
    return pd.Series(columns)


def split_df(df, col, predefined_values):
    split_columns = df[col].apply(
        split_row,
        predefined_values=predefined_values
    )
    df = split_columns
    df.to_csv(os.path.join(PATH, f'split_{col}.csv'))


if __name__ == "__main__":

    if not os.path.exists(PATH):
        os.mkdir(PATH)

    csv_file = ("C:/Users/willem.boone/Documents/projects/MARBEFES/"
                "analyse_survey/survey_responses.csv")
    df = pd.read_csv(csv_file, sep=";", encoding='latin-1')

    # -------------------------------------------------------------------------
    with open("mappings/column_mapping.json", "r", encoding='utf-8') as f:
        column_mapping = json.load(f)
    df.rename(columns=column_mapping, inplace=True)

    # -------------------------------------------------------------------------
    with open("mappings/connection_values.json", "r", encoding="utf-8") as f:
        connections_values = json.load(f)
    df_ = df[["connection_type"]]
    split_df(df_, col="connection_type", predefined_values=connections_values)

    # -------------------------------------------------------------------------
    with open("mappings/frequency_values.json", "r", encoding="utf-8") as f:
        frequency_values = json.load(f)
    df_ = df[["visit_frequency"]]
    split_df(df_, col="visit_frequency", predefined_values=frequency_values)

    # -------------------------------------------------------------------------
    with open("mappings/activity_values.json", "r", encoding="utf-8") as f:
        activities_values = json.load(f)
    df_ = df[["activities"]]
    split_df(df_, col="activities", predefined_values=activities_values)

    # -------------------------------------------------------------------------
    with open("mappings/motivation_values.json", "r", encoding="utf-8") as f:
        motivation_values = json.load(f)
    df_ = df[["motivation"]]
    split_df(df_, col="motivation", predefined_values=motivation_values)

    # -------------------------------------------------------------------------
    with open("mappings/influence_values.json", "r", encoding="utf-8") as f:
        influence_values = json.load(f)
    df_ = df[["influence_experience"]]
    split_df(df_, col="influence_experience",
             predefined_values=influence_values)











