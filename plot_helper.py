# plot overview for relationships between autoimmune diseases / p-value of snp variation / snp related genes
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# import dataprep_helper as dh
# df = dh.read_pickle_df("data/GWASCatelog")

def plot_overview(df):
    """
    Plot overview graphs to show the similarities of genetics backgrounds for different autoimmune diseases.
    <>< <>< <>< <>< <><
    Two matrix plots containing the information of diseases/ genes / and P-Value of the mutations on certain genes
    are presented. The brighter the color represents the gene is more likely to be causal to the diseases.

    :param df: The csv file downloaded from gwascatelog
    :return: a heatmap and a clustermap open in another pop up window. Users have to save it themselves.
    """
    # Collect the genes that has more than 7 occurrence.
    top = df['MAPPED_GENE'].value_counts() >= 7
    top_gene_list = []
    for gene in top.keys():
        if top[gene] == True:
            top_gene_list.append(gene)
    # Create a dataframe containing only the rows with top occurrence genes.
    df_top = df[df['MAPPED_GENE'].isin(top_gene_list)].copy()
    # transform the dataframe into a pivot table containing three columns for plotting the matrix plots.
    pt = df_top.pivot_table(index ="DZ_NAME", columns ="MAPPED_GENE", values="P-VALUE log10-n",fill_value=1, aggfunc=np.max, figsize=(8, 6))
    # plot a heatmap with title and label
    sns.heatmap(pt).set_title('SNPs P-Values for Genes of Autoimmune Diseases')
    # Give users a hint to save the file and close the window in prompt lines.
    print("The overview heatmap figure will open in another window. Please save the graph and close the window to continue.")
    # Show the graph in another window
    plt.show()
    # plot a cluster map
    sns.clustermap(pt)
    # Give users a hint to save the file and close the window in prompt lines.
    print("The overview cluster figure will open in another window. Please save the graph and close the window to continue.")
    # Show the graph in another window
    plt.show()


def plot_genes(df, disease):
    """
    Plot single disease comparison between gene name / publication amount / chemical amount.
    <>< <>< <>< <>< <><
    By the visualization, it is possible to infer that
    1. which genes are investigated more intensively for the certain disease.
    2. which disease-genes combination are linked to more chemicals (drugs) which could be potential treatment.
    3. if there are genes that are significantly less ingestigated and may be a future potential therapy aim.

    :param df: dataframe generated from literature curation for a certain disease.
    :param disease: a certain disease out of the 15 autoimmune disease selected by users.
    :return: a bar chart representing the literature and the chemicals related to genes related to a certain diseases.
    """
    # Give users a hint to save the file and close the window in prompt lines.
    print("The figure is opened in another window. Please save the graph and close the window to continue.")
    # set default palette to seaborn colors.
    sns.set()
    df = df[df['Disease-Gene related literature amount'] > 0].copy()
    # plot the barchart by pandas function
    ax = df.plot.barh(stacked = True, figsize=(8, 6), title = "Genes and potential therapies (chemicals) related to " + disease)
    ax.set(xlabel="literature / chemical counts", ylabel="genes")
    plt.show()


def plot_pvalue(df, disease):
    # Give users a hint to save the file and close the window in prompt lines.
    print("A figure showing genes amount for each cut-off P-Value is presented. \n"
          "Use the information to decide which cut-off P-Value. \n"
          "The figure is opened in another window. Please close the window to continue.")
    sns.set()
    p_value_series = df[df['DZ_NAME'] == disease]['P-VALUE log10-n']
    ax = p_value_series.plot.hist(bins = 60, cumulative= -1, figsize=(8, 6))
    ax.set_xlabel('N, (P-Value = 1 x 10 -N)')
    ax.set_ylabel('Gene amount for set P-Value')
    ax.set_title("P-Value Ranges for Genes related to "+ disease)
    plt.show()

