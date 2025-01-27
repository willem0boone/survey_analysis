import json
import pandas as pd


# Function to split into columns
def split_row(row, predefined_values):
    row_values = row.split(';')  # Split by semicolon
    columns = {value: 0 for value in
               predefined_values}  # Initialize all predefined values to 0
    other = []  # To capture other unrecognized values

    for value in row_values:
        value = value.strip()  # Remove leading/trailing whitespace
        if value in predefined_values:
            columns[value] = 1  # Mark the value as present
        else:
            other.append(value)  # Add to "Other" if not in predefined values

    columns['Other'] = '; '.join(
        other)  # Join unrecognized values into the "Other" column
    return pd.Series(columns)


def split_df(df, col, predefined_values):

    # Apply function to split into multiple columns
    split_columns = df[col].apply(
        split_row,
        predefined_values=predefined_values
    )
    df = pd.concat([df, split_columns], axis=1)
    df.to_csv(f'intermediate/splitted_{col}.csv')


if __name__ == "__main__":

    csv_file = ("C:/Users/willem.boone/Documents/projects/MARBEFES/"
                "analyse_survey/survey_responses.csv")

    df = pd.read_csv(csv_file, sep=";", encoding='latin-1')

    with open("column_mapping.json", "r", encoding='utf-8') as f:
        column_mapping = json.load(f)
    df.rename(columns=column_mapping, inplace=True)

    # -------------------------------------------------------------------------
    connections_values = [
        "Als toerist (recreatief)",
        "Als Lokale bewoner",
        "Verbonden via cultuur en tradities",
        "Verbonden via industrie of economie",
        "Verbonden via visserij",
        "Als werknemer bij een publieke dienst (gemeentelijk, gewestelijk, veiligheidsdiensten... )",
        "Verbonden als onderzoeker",
        "Verbonden via milieu-en of of klimaatorganisatie."
    ]

    df_ = df[["connection_type"]]

    split_df(df_, col="connection_type", predefined_values=connections_values)

    # -------------------------------------------------------------------------
    frequency_values = [
        "Dagelijks",
        "Minstens 1 keer per week",
        "Minstens 1 keer per maand",
        "Minstens 1 keer per jaar",
        "Minder dan 1 keer per jaar"
    ]

    df_ = df[["visit_frequency"]]

    split_df(df_, col="visit_frequency", predefined_values=frequency_values)

    # -------------------------------------------------------------------------
    activities_values = [
        "Wandelen",
        "Fietsen",
        "Huisdieren uitlaten",
        "Ontspanning",
        "Zwemmen",
        "Lopen of joggen",
        "Fotografie",
        "Genieten van het uitzicht",
        "Eet-en of of drinkgelegenheid",
        "Watersport (zeilen, surfen, kajakken, kiten etc.)",
        "Tijd in de natuur doorbrengen",
    ]

    df_ = df[["activities"]]

    split_df(df_, col="activities", predefined_values=activities_values)

    # -------------------------------------------------------------------------
    motivation_values = [
        "Contact met de natuur",
        "Beleven van tradities",
        "Educatieve verrijking",
        "Stimulans voor mentale gezondheid",
        "Mogelijkheid tot ontspanning",
        "Sportgelegenheid",
        "Culturele beleving",
        "Toeristische faciliteiten (bv. Horeca)",
        "Binding met gemeenschap of woonplaats",
    ]

    df_ = df[["motivation"]]

    split_df(df_, col="motivation", predefined_values=motivation_values)

    # -------------------------------------------------------------------------
    influence_values = [
        "Geen invloed",
        "Biodiversiteit verandering",
        "Klimaatverandering",
        "Kust erosie",
        "Overstroming",
        "Vervuiling",
        "Toename toerisme",
        "Zeespiegelstijging",
        "Aanleg windmolenparken",
    ]

    df_ = df[["influence_experience"]]

    split_df(df_, col="influence_experience",
             predefined_values=influence_values)











