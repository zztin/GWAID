# Welcome user
import unicodedata
import re

# A introduction paragraph for user to read and understand what is autoimmune diseases.
def print_intro():
    intro = input("Do you want to read some introduction? (y/n) ").lower()
    if intro == 'y':
        print("\nAn autoimmune disease is a condition in which your immune system mistakenly attacks your body. \n"
              "The immune system normally guards against germs like bacteria and viruses. When it senses these\n"
              "foreign invaders, it sends out an army of fighter cells to attack them. \n"
              "In an autoimmune disease, the immune system mistakes part of your body as foreign. It releases \n"
              "proteins called auto-antibodies that attack healthy cells. Pathogenesis of autoimmune diseases \n"
              "involve both environmental and genetic factors. \n"
              "GWAS studies identified several genetic loci association with clinical manifestations and treatment \n"
              "outcome. In this program, 15 common autoimmune diseases are included. We provide 2 functions, \n"
              "one compare genetic background of various autoimmune diseases, the other allows deeper understanding \n"
              "to a certain disease by literature curation of related diseases and their treatments. ")
        print("\n\nPlease wait...")
    else:
        print("\n\nPlease wait...")

# A list for printing. User can choose from the index for each autoimmune disease.
aid_list = "1. Behcet's disease \n" \
           "2. Crohn's disease \n" \
           "3. Asthma \n" \
           "4. Atopic dermatitis \n" \
           "5. Primary sclerosing cholangitis \n" \
           "6. Alopecia areata \n" \
           "7. Type 1 diabetes \n" \
           "8. Ankylosing spondylitis \n" \
           "9. Systemic sclerosis \n" \
           "10. Vitiligo \n" \
           "11. Kawasaki disease \n" \
           "12. Psoriasis \n" \
           "13. Celiac disease \n" \
           "14. Systemic lupus erythematosus \n" \
           "15. Ulcerative colitis \n" \

# The list in python list format. indexing is correlated to the user selected index.
aid = ['Behcet\'s disease', 'Crohn\'s disease', 'Asthma', 'Atopic dermatitis', 'Primary sclerosing cholangitis',
       'Alopecia areata', 'Type 1 diabetes', 'Ankylosing spondylitis', 'Systemic sclerosis', 'Vitiligo',
       'Kawasaki disease', 'Psoriasis', 'Celiac disease', 'Systemic lupus erythematosus', 'Ulcerative colitis']


# convert the user selected index into disease name to further manipulate the dataframe.
def aid_index_to_name():
    wrong_input = True
    while wrong_input == True:
        try:
            index = int(input('Please select a disease from the following list : \n'
                                      + aid_list +'\n (Enter 1-15): \n'))
            disease = aid[index - 1]
            print("Your choice is: " + disease)
            wrong_input = False
        except (ValueError, IndexError):
            print("Warning! Please enter a number to choose the correlated disease! ")
            wrong_input = True
    return index, disease

def set_pvalue():
    reassign = ''
    while reassign != 'y' and reassign != 'n':
        reassign = input("The Default for the significance of genes related to the disease is set by P-Value < 1 x 10^ -6."
                    " \n Do you want to set a different P-Value (y)? (y/n) \n")
        if reassign == 'n':
            logpvalue = 6
        elif reassign == 'y':
            print("Please enter a cut-off P-value 'N' for the significance of genes "
                  "related to the disease.\n"
                  "Higher N results in more specific relationship and less genes. \n")
            while True:
                try:
                    logpvalue = int(input("P-Value < 1 x 10^ -N \nN = "))
                    if logpvalue > 300 or logpvalue < 6:
                        raise Exception
                    print("You've chose a P-Value < 1 x 10^ -" + str(logpvalue)+ '.')
                    break
                except Exception:
                    print('N should be an integer between 8 and 300\n')
        else:
            print('This is not a valid input. select y or n.\n')
    return logpvalue

def confirm_pvalue():
    while True:
        confirm = input("(Tip: Querying speed: 30 genes / minute. "
                        "A smaller P-Value results in less genes to search.)\n\n"
                        "Press 'y' to preceed with the search. Press 'n' to select a new P-Value. (y/n)\n")
        if confirm == 'y' or confirm == 'n':
            return confirm
        else:
            print('This is not a valid input. Press y or n.\n')


def filename_convert(value):
    """
    removes non-alpha or non-number characters, and converts underscores, hyphens and spaces to a single underscore.

    Adapt from stackoverflow according to https://www.djangoproject.com/
    The function is called by fill_filename() function in this user_helper program.
    """
    # delete all non-word, non-whitespace, and not _ or - characters.
    value = re.sub('[^\w\s_-]', '', value).strip()
    # convert all -, _, whitespace characters into one single underscore.
    value = re.sub('[-_\s]+', '_', value)
    return value


def fill_filename(disease, logpvalue):
    """
    Generate a default valid filename for user to choose from. User can also enter filename on their own.
    :param disease: The disease the user has queried.
    :return: a valid filename
    """
    filename = None
    while filename == None:
        # generate default filename
        default = input("The Default filename is : GWAID_" + filename_convert(disease) + "_P_value_" + str(logpvalue)
                        + "\nDo you want to save with this filename? (y/n) ")
        if default == 'y':
            # save with default filename.
            filename = filename_convert("GWAID_" + disease + "_P_value_" + str(logpvalue))
        elif default == 'n':
            # user does not want to use the default filename.
            confirm = 'n'
            while confirm != 'y':
                try:
                    # formatted the user input filename into a valid standardized filename.
                    filename = filename_convert(input("Please choose a new filename: "))
                    # Ask user to confirm if they want to use the converted valid filename.
                    confirm = input("New filename = "+ filename + " : Confirm? (y/n) ")
                    # if not, continue to ask user to input a new filename.
                except Exception:
                    print("Please enter a valid filename. ")
        else:
            print("Please enter y or n.\n")
    return filename


def again():
    """
    Ask user if they want to continue to use other function of the program.

    :return:
    """
    again = input("\nDo you want to leave the program? (y/n) \n")
    if again != 'y':
        return True
    else:
        return False