import os.path
import re
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

OUT_PATH = "participants_profile"


def demographics(data, title, save, show):
    age_gender_counts = (
        data.groupby(["age", "gender"]).size().unstack(fill_value=0))
    vrouw_counts = age_gender_counts.get("Vrouw", pd.Series(dtype=int))
    man_counts = age_gender_counts.get("Man", pd.Series(dtype=int))
    all_age_categories = age_gender_counts.index

    vrouw_counts = vrouw_counts.reindex(all_age_categories, fill_value=0)
    man_counts = man_counts.reindex(all_age_categories, fill_value=0)

    plt.figure(figsize=(10, 6))
    bar_height = 1.0

    plt.barh(vrouw_counts.index,
             vrouw_counts.values,
             color='red',
             edgecolor='black',
             label='Female (Vrouw)',
             height=bar_height)

    plt.barh(man_counts.index,
             -man_counts.values,
             color='blue',
             edgecolor='black',
             label='Male (Man)',
             height=bar_height)

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

    if save:
        plt.savefig(os.path.join(OUT_PATH, f"{title}.png"))

    if show:
        plt.show()


def clean_column_names(columns):
    return [re.sub(r'[^a-zA-Z0-9]', '_', col) for col in columns]


def map_visits_to_matrix(df):
    home_col = "municipality"
    visit_col = "visit_municipalities"

    if home_col not in df.columns or visit_col not in df.columns:
        raise ValueError(f"The DataFrame must contain '{home_col}' and "
                         f"'{visit_col}' columns.")

    # Define the municipalities order
    municipalities = [
        'De Panne',
        'Koksijde',
        'Nieuwpoort',
        'Middelkerke',
        'Oostende',
        'Bredene',
        'De Haan',
        'Blankenberge',
        'Zeebrugge',
        'Knokke-Heist',
        'Andere gemeente in West-Vlaanderen',
        'Andere gemeente in België'
    ]

    home_count = df[home_col].value_counts()

    home_count = home_count.reindex(index=municipalities,
                                    fill_value=0
                                    )

    visit_matrix = pd.DataFrame(data=0,
                                index=municipalities,
                                columns=municipalities
                                )

    for home in municipalities:
        df_home = df[df[home_col] == home]

        locations_series = (
            df_home[visit_col]
            .str.split(';')
            .explode()
            .loc[lambda x: x != '']
        )

        location_counts = locations_series.value_counts()
        for visit, count in location_counts.items():
            if visit in visit_matrix.columns:
                visit_matrix.loc[home, visit] += count

    combined_matrix = visit_matrix.copy()
    combined_matrix.insert(0, "responses", home_count)
    combined_matrix.index.name = "municipalities"

    return combined_matrix


def plot_cumulative_responses(df, show, save):
    date_column = "completion_time"
    df[date_column] = pd.to_datetime(df[date_column], format='%d-%m-%Y %H:%M')

    df = df.sort_values(by=date_column)
    df['cumulative_responses'] = range(1, len(df) + 1)
    df['week'] = df[date_column].dt.to_period('W').dt.start_time
    weekly_counts = df.groupby('week').size()

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(df[date_column],
             df['cumulative_responses'],
             label='Cumulative Responses',
             color='b')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Cumulative Responses',
                   color='b')
    ax1.tick_params(axis='y',
                    labelcolor='b')
    mondays = weekly_counts.index

    ax1.set_xticks(mondays)
    ax1.xaxis.set_major_formatter(
        plt.matplotlib.dates.DateFormatter('%Y-%b-%d'))

    for monday in mondays:
        ax1.axvline(x=monday,
                    color='gray',
                    linestyle='--',
                    alpha=0.7)

    ax1.set_xticklabels(mondays.strftime('%d %b %Y'), rotation=45, ha="right")
    ax1.set_ylim(0, None)

    ax2 = ax1.twinx()
    for start_date, count in weekly_counts.items():
        ax2.bar(start_date,
                count,
                width=7,
                alpha=0.5,
                color='green',
                align='edge',
                label='Responses per Week' if start_date == weekly_counts.
                index[0] else "")

    ax2.set_ylabel('Responses per Week', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
    plt.title('Cumulative Responses and Weekly Response Counts')
    plt.tight_layout()
    if save:
        plt.savefig(os.path.join(OUT_PATH, "response_rate.png"))
    if show:
        plt.show()


def plot_score(df, col, name, show, save):
    plt.figure(figsize=(8, 6))
    sns.boxplot(y=df[col], color='skyblue')

    # Calculate statistics
    mean = df[col].mean()
    median = df[col].median()

    # Add horizontal lines for mean and median
    plt.axhline(mean, color='red', linestyle='--', linewidth=1,
                label=f'Mean: {mean:.2f}')
    plt.axhline(median, color='green', linestyle='-', linewidth=1,
                label=f'Median: {median:.2f}')

    # Add labels, legend, and title
    plt.title(name, fontsize=16)
    plt.ylabel(col, fontsize=14)
    plt.legend(loc='upper right', fontsize=12)

    # Show the plot
    plt.tight_layout()

    if show:
        plt.show()
    if save:
        plt.savefig(os.path.join(OUT_PATH, f"{name}.png"))


if __name__ == "__main__":

    if not os.path.exists(OUT_PATH):
        os.mkdir(OUT_PATH)

    csv_file = ("C:/Users/willem.boone/Documents/projects/MARBEFES/"
                "analyse_survey/survey_responses.csv")

    df = pd.read_csv(csv_file, sep=";", encoding='latin-1')
    with open("mappings/column_mapping.json", "r", encoding='utf-8') as f:
        column_mapping = json.load(f)
    df.rename(columns=column_mapping, inplace=True)

    # -------------------------------------------------------------------------
    # demographics
    demographics(df,
                 title=f"Demographic Distribution",
                 show=False,
                 save=True
                 )

    # demographics per municipality
    municipalities = df['municipality'].unique()

    for municipality in municipalities:
        municipality_data = df[df['municipality'] == municipality]
        demographics(municipality_data,
                     title=f"Demographic Distribution in {municipality}",
                     show=False,
                     save=True
                     )
    # -------------------------------------------------------------------------
    # response over time
    plot_cumulative_responses(df, show=False, save=True)

    # -------------------------------------------------------------------------
    # scores
    plot_score(df,
               col="env_state",
               name="env_state",
               save=True,
               show=False
               )

    plot_score(df,
               col="env_importance",
               name="env_importance",
               save=True,
               show=False
               )

    # -------------------------------------------------------------------------
    # fluxes
    visit_matrix = map_visits_to_matrix(df=df)
    visit_matrix.to_csv(os.path.join(OUT_PATH, 'matrix.csv'))


