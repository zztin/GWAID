# plot overview for relationships between autoimmune diseases / p-value of snp variation / snp related genes
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd

def plot_overview(df):
    pt = df.pivot_table(index ="DZ_NAME", columns ="MAPPED_GENE", values ="P-VALUE")
    sns.heatmap(pt)
    plt.show()
    print("The overview figure is opened in another window. Please save the graph and close the window to continue.")
    sns.clustermap(pt)
    plt.show()
    print("The overview figure is opened in another window. Please save the graph and close the window to continue.")


# plot single disease comparison between gene name / publication amount / chemical amount
def plot_genes(df):
    print(df.head())  #########
    df.plot.bar(stacked = True)
    plt.show()
    print("The overview figure is opened in another window. Please save the graph and close the window to continue.")


    #
    # sns.set(style="whitegrid")
    # # Draw a nested barplot to show survival for class and sex
    # g = sns.factorplot(x="class", y="survived", hue="sex", data=titanic,
    #                    size=6, kind="bar", palette="muted")
    # g.despine(left=True)
    # g.set_ylabels("Genes")
    # plt.show()
    # print("The overview figure is opened in another window. Please save the graph and close the window to continue.")


