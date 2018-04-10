# plot overview for relationships between autoimmune diseases / p-value of snp variation / snp related genes
import seaborn as sns
from matplotlib import pyplot as plt

def plot_overview(df):
    pt = df.pivot_table(index ="DZ_NAME", columns ="MAPPED_GENE", values ="P-VALUE")
    sns.heatmap(pt)
    plt.show()

# plot single disease comparison between gene name / publication amount / chemical amount
def plot_genes(df):
    print(df.head())  #########
    titanic = sns.load_dataset("titanic")

    sns.set(style="whitegrid")
    # Draw a nested barplot to show survival for class and sex
    g = sns.factorplot(x="class", y="survived", hue="sex", data=titanic,
                       size=6, kind="bar", palette="muted")
    g.despine(left=True)
    g.set_ylabels("Genes")
    plt.show()

