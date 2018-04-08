# import local modules
import user_helper as uh
import dataprep_helper as dh
import plot_helper as ph

"""
This main program serves as a controller. data are imported and transported between modules.
df = Autoimmune diseases related data extracted from gwas catelog
"""

# Load data.
print("Launching Autoimmune diseases exploration in Genome-wide association studies (GWAID)... Please wait...")
# A short introduction for user (if they like)
intro = input("Do you want to read some introduction? (y/n)").lower
if intro == 'y':
    uh.print_intro()
else:
    pass
try:
    df = dh.gwas_import()
except Exception:
    print("The program package is not complete. Some data is lost. End program. ")
# HOW to end program ???

# Welcome the user
print("Welcome to Autoimmune disease exploration in Genome-wide association studies (GWAS) program.")
# Ask what the user what to do.
again = True
while again == True:
    try:
        answer = input('Please select a function: '
                       'a. Overview of all Autoimmune diseases.\n'
                       'b. Select a particular disease of interest: \n'
                       'c. End program. \n').lower()
        # By the time waiting for user input, convert data into designed format.
        if answer == 'a':
            ph.plot_overview(df)
            again = uh.again()
            # Show heat map between Autoimmune diseases ( Gene hits )
            # overview.aid_compare()
        elif answer == 'b':
            disease_index = input('Please select a disease from the following list (enter 1-15): \n' + uh.aid_list)
            disease = uh.aid_index_name(disease_index)
            disease, genes = dh.phenotype_to_gene(df,disease)
            # generate pubmed key with disease name + 1 gene name from the list.
            pmid_list = dh.search_lit(disease=disease, genes=genes)
            chemicals = dh.pubtator_chemicals(pmid_list)
            again = uh.again()
        elif answer == 'c':
            print("Thank you for using this program. Goodbye. ")
            break
        else:
            print('This is an invalid input. Please try again using a,b,c: ')
# TBD: what errors exactly?
    except ValueError or TypeError:
        print("This is not a valid input. Please try again")
