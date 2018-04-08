# Welcome user

def print_intro():
    print("An autoimmune disease is a condition in which your immune system mistakenly attacks your body. \n"
          "The immune system normally guards against germs like bacteria and viruses. When it senses these\n"
          "foreign invaders, it sends out an army of fighter cells to attack them. \n"
          "In an autoimmune disease, the immune system mistakes part of your body as foreign. It releases \n" 
          "proteins called auto-antibodies that attack healthy cells. Pathogenesis of autoimmune diseases \n"
          "involve both environmental and genetic factors. \n"
          "GWAS studies identified several genetic loci association with clinical menifestations and treatment \n"
          "outcome. In this program, 15 common autoimmune diseases are included. We provide 2 functions, \n"
          "one compare genetic background of various autoimmune diseases, the other allows deeper understanding \n"
          "to a certain disease by literature curation of related diseases and their treatments. ")

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


aid = ['Behcet\'s disease', 'Crohn\'s disease', 'Asthma', 'Atopic dermatitis', 'Primary sclerosing cholangitis',
       'Alopecia areata', 'Type 1 diabetes', 'Ankylosing spondylitis', 'Systemic sclerosis', 'Vitiligo',
       'Kawasaki disease', 'Psoriasis', 'Celiac disease', 'Systemic lupus erythematosus', 'Ulcerative colitis']


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
    return disease


# How to write a check program?
#  def check_input(user_input):
#       try:
#             user_input()
#

def again():
      again = input("Do you want to use other function of the program? (y/n) ")
      if again == 'y':
            return True
      else:
            return False

