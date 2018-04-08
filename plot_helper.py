# plot overview for relationships between autoimmune diseases / p-value of snp variation / snp related genes
import seaborn as sns
from matplotlib import pyplot as plt

# For developing use. Delete afterward!!!!!!
import dataprep_helper as dh
df = dh.gwas_import_aid()
# For developing use. Delete afterward!!!!!!



def plot_overview(df):
    pt = df.pivot_table(index ="DZ_NAME", columns ="MAPPED_GENE", values ="P-VALUE")
    sns.heatmap(pt)
    plt.show()
