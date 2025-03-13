import pandas as pd
import json


def translate_row(row, lookup_dict):
    return row.map(lambda x: ';'.join([lookup_dict.get(activity.strip(), activity.strip()) for activity in x.split(';')]))


def translate(df, col, lookup_dict):
    """

    :param df_in:
    :param l_out:
    :return:
    """

    df[col] = df[col].apply(lambda x: ';'.join(
        [lookup_dict.get(activity.strip(), activity.strip()) for activity in
         x.split(';')]))

    return df


if __name__ == "__main__":
    raw_eng = (
        "responses/Socio-cultural valuation of the Belgian Coast and North "
        "Sea - Marbefes project.csv")

    raw_nl = (
        "responses/Sociaal-culturele waardering van de Belgische Kust en"
        " Noordzee - Marbefes project.csv")

    raw_eng = pd.read_csv(raw_eng, encoding="utf-8", sep=",")
    raw_nl = pd.read_csv(raw_nl, encoding="utf-8", sep=",")

    with open("mapping/column_mapping_NL.json", "r", encoding='utf-8') as f:
        column_mapping = json.load(f)
    df_nl = raw_nl.rename(columns=column_mapping)

    with open("mapping/activity_v.json", "r", encoding='utf-8') as f:
        activity_mapping = json.load(f)
    df_nl = translate(df_nl, col="activities", lookup_dict=activity_mapping)

    with open("mapping/connection_v.json", "r", encoding='utf-8') as f:
        connection_mapping = json.load(f)
    df_nl = translate(df_nl, col="connection_type", lookup_dict=connection_mapping)

    with open("mapping/frequency_v.json", "r", encoding='utf-8') as f:
        frequency_mapping = json.load(f)
    df_nl = translate(df_nl, col="visit_frequency", lookup_dict=frequency_mapping)

    with open("mapping/influence_v.json", "r", encoding='utf-8') as f:
        influence_mapping = json.load(f)
    df_nl = translate(df_nl, col="influence_experience", lookup_dict=influence_mapping)

    with open("mapping/motivation_v.json", "r", encoding='utf-8') as f:
        motivation_mapping = json.load(f)
    df_nl = translate(df_nl, col="motivation", lookup_dict=motivation_mapping)

    with open("mapping/municip_v.json", "r", encoding='utf-8') as f:
        municip_mapping = json.load(f)
    df_nl = translate(df_nl, col="municipality", lookup_dict=municip_mapping)

    with open("mapping/gender_v.json", "r", encoding='utf-8') as f:
        gender_mapping = json.load(f)
    df_nl = translate(df_nl, col="gender", lookup_dict=gender_mapping)

    with open("mapping/column_mapping_ENG.json", "r", encoding='utf-8') as f:
        column_mapping = json.load(f)
    raw_eng.rename(columns=column_mapping, inplace=True)

    df_merged = pd.concat([df_nl, raw_eng])

    reverse_column_mapping = {v: k for k, v in column_mapping.items()}
    df_merged = df_merged.rename(columns=reverse_column_mapping)

    df_merged.to_csv('translation.csv')



















