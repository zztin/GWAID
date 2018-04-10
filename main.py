# import local modules
import user_helper as uh
import dataprep_helper as dh
import plot_helper as ph
import warnings
import csv


"""
This main program serves as a controller. data are imported and transported between modules.
df = Autoimmune diseases related data extracted from gwas catelog
"""

# Load data.
print("Launching Autoimmune diseases exploration in Genome-wide association studies (GWAID)... Please wait...")
# A short introduction for user (if they like)
intro = input("Do you want to read some introduction? (y/n) ").lower()
if intro == 'y':
    uh.print_intro()
    print("\n\nPlease wait...")
else:
    print("\n\nPlease wait...")
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
        # By the time waiting for user input, convert data into designed format.
        if answer == 'a':
            ph.plot_overview(df)
            print("The overview figure is opened in another window. Please save the graph and close the window to continue.")
            again = uh.again()
            # Show heat map between Autoimmune diseases ( Gene hits )
            # overview.aid_compare()
        elif answer == 'b':
            index, disease = uh.aid_index_to_name()
            disease, genes = dh.disease_to_genes(df, disease)
            print('Query disease: '+ disease + '. Related gene amount found in GWAS database: '+  str(len(genes)) + '.')
            # generate pubmed key with disease name + 1 gene name from the list.
            pubtator_dic, df_pubtator = dh.search_lit(disease=disease, genes=genes)
            ph.plot_genes(df_pubtator) ##############
            dh.df_to_pickle(df_pubtator, disease)
            dh.dic_json(pubtator_dic, disease)
            dh.write_txt(pubtator_dic, disease)
            ph.plot_genes(df_pubtator)
#            chemicals = dh.pubtator_chemicals(pmid_list)
            again = uh.again()
        elif answer == 'c':
            print("Thank you for using this program. Goodbye. ")
            break
        else:
            print('This is an invalid input. Please try again using a,b,c: ')
# TBD: what errors exactly?
    except ValueError or TypeError:
        print("This is not a valid input. Please try again")

print("Thank you for using this program. Goodbye. ")