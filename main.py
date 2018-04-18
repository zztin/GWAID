# import local modules
import user_helper as uh
import dataprep_helper as dh
import plot_helper as ph
import sys

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
    print("The program package is not complete. Some data is lost. End program. ")
    sys.exit()

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
            ph.plot_pvalue(df, disease)
            # Query the disease in GWAS catelog and return the number of related genes.
            confirm = 'n'
            while confirm == 'n':
                logpvalue = uh.set_pvalue()
                disease, genes = dh.disease_to_genes(df, disease, logpvalue)
                print('Query disease: '+ disease + '. Related gene amount found in GWAS database: '+  str(len(genes)) + '\n')
                confirm = uh.confirm_pvalue()
            # Query pubmed for each gene related to the disease.
            print('Starting Pubmed literature search.\n')
            print('\nIf you would like to halt the query, press ctrl + C. However, the results will not be saved.\n')
            pubtator_dic, df_pubtator = dh.search_lit(disease=disease, genes=genes)
            # Plot the result genes and chemicals related to the disease.
            ph.plot_genes(df_pubtator, disease)
            # Ask user to select a filename to save file.
            filename = uh.fill_filename(disease)
            try:
                # Save files in different formats.
                dh.df_to_pickle(df_pubtator, filename)
                dh.dic_json(pubtator_dic, filename)
                dh.write_txt(pubtator_dic, filename)
            except SystemError as err:
                print(err)
                print("Unable to save the query data files. It could be the process exceed the memory of your computer.")
            again = uh.again()
        elif answer == 'c':
            break
        else:
            print('This is an invalid input. Please try again using a,b,c: ')
    except ValueError or TypeError:
        print("This is not a valid input. Please try again")
    except KeyboardInterrupt:
        print("You have forced stopped the querying process.")
        again = uh.again()

# End program message.
print("Thank you for using this program. Goodbye. ")