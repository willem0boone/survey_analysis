import pandas as pd
import matplotlib.pyplot as plt


def plot_counts(data, save, show, name):
    df = pd.DataFrame(data)

    # Drop the "Other" column as it's not needed for counting
    df_counts = df.drop(columns=["Other"])

    # Sum the counts for each category
    category_counts = df_counts.sum()

    # Plot the counts as a bar graph
    plt.figure(figsize=(10, 6))
    category_counts.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title(f"{name} frequency graph", fontsize=16)
    plt.ylabel("Count", fontsize=14)
    plt.xlabel("Category", fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    if save:
        plt.savefig(f"{name}.png")
    if show:
        plt.show()
