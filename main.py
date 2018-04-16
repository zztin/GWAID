# import local modules
import user_helper as uh
import dataprep_helper as dh
import plot_helper as ph
import warnings
import csv


"""
This main program serves as a controller. data are imported and transported between modules.
"""

print("Launching Autoimmune diseases exploration in Genome-wide association studies (GWAID).")
# A short introduction for user (if they like)
intro = input("Do you want to read some introduction? (y/n) ").lower()
if intro == 'y':
    uh.print_intro()
    print("\n\nPlease wait...")
else:
    print("\n\nPlease wait...")
# Load data.
try:
    df = dh.gwas_import_aid()
except Exception:
    pass
    print("The program package is not complete. Some data is lost. End program. ")
# HOW to end program ???

# Welcome the user
print("Welcome to Autoimmune disease exploration in Genome-wide association studies (GWAS) program.")
# Ask what the user what to do.
again = True
while again == True:
    try:
        answer = input('Please select a function: \n'
                       'a. Overview of all Autoimmune diseases.\n'
                       'b. Select a particular disease of interest. \n'
                       'c. End program. \n'
                       'Enter ( a / b / c ) : ').lower()
        if answer == 'a':
            # Show heatmap and clustermap between Autoimmune diseases.
            ph.plot_overview(df)
            again = uh.again()
        elif answer == 'b':
            # Ask user which particular disease they would like to query from a list.
            index, disease = uh.aid_index_to_name()
            # Query the disease in GWAS catelog and return the number of related genes.
            disease, genes = dh.disease_to_genes(df, disease)
            print('Query disease: '+ disease + '. Related gene amount found in GWAS database: '+  str(len(genes)))
            # Query pubmed for each gene related to the disease.
            pubtator_dic, df_pubtator = dh.search_lit(disease=disease, genes=genes)
            # Plot the result genes and chemicals related to the disease.
            ph.plot_genes(df_pubtator, disease)
            # Ask user to select a filename to save file.
            filename = uh.fill_filename(disease)
            # Save files in different formats.
            dh.df_to_pickle(df_pubtator, filename)
            dh.dic_json(pubtator_dic, filename)
            dh.write_txt(pubtator_dic, filename)
            again = uh.again()
        elif answer == 'c':
            break
        else:
            print('This is an invalid input. Please try again using a,b,c: ')
    except ValueError or TypeError:
        print("This is not a valid input. Please try again")

# End program message.
print("Thank you for using this program. Goodbye. ")