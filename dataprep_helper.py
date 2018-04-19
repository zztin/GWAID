import pandas as pd
import requests
import xmltodict
import json
import time
import math


def gwas_import_aid():
    """
    Transform downloaded csv file into pandas dataframe for further analysis.
    :return:  a dataframe containing all important information related.
    """
    # read in file
    df = pd.read_csv("./data/gwas_catalog_v1.0.1-associations_e91_r2018-02-13.tsv",sep='\t',low_memory=False)
    # select informative columns
    df = df[['DISEASE/TRAIT', 'STRONGEST SNP-RISK ALLELE', "SNPS", "P-VALUE", 'REPORTED GENE(S)',
                  'MAPPED_GENE', 'UPSTREAM_GENE_ID', 'DOWNSTREAM_GENE_ID', 'SNP_GENE_IDS', 'MAPPED_TRAIT',
                  'MAPPED_TRAIT_URI', 'PUBMEDID', 'FIRST AUTHOR', 'DATE', 'JOURNAL']]
    # Select the row of autoimmune diseases and assign grouped name and id
    df.insert(loc=1, column="DZ_NAME", value="")
    df.insert(loc=1, column="DZ_ID", value="")
    aid = ['Behcet\'s disease', 'Crohn\'s disease', 'Asthma', 'Atopic dermatitis',
                'Primary sclerosing cholangitis', 'Alopecia areata', 'Type 1 diabetes', 'Ankylosing spondylitis',
                'Systemic sclerosis', 'Vitiligo', 'Kawasaki disease', 'Psoriasis', 'Celiac disease',
                'Systemic lupus erythematosus', 'Ulcerative colitis']
    i = 0
    for dz in aid:
        i += 1
        # select the rows with the autoimmune diseases name contained in the column 'DISEASE/TRAIT'
        df_temp = df[df['DISEASE/TRAIT'].str.contains(dz)]['DZ_NAME'].apply(lambda x: dz)
        df_temp2 = df[df['DISEASE/TRAIT'].str.contains(dz)]['DZ_ID'].apply(lambda x: i)
        df.update(df_temp)
        df.update(df_temp2)
    # drop the rows which are not autoimmune diseases. New df only contains autoimmune diseases.
    df.drop(labels = df[df['DZ_ID'] == ''].index, inplace = True)
    # reset index for aid.
    df.reset_index(inplace= True)
    # convert the dtype of column P-Value ("1.35e-23" string format ---> into numeric format.)
    df['P-VALUE'] = df['P-VALUE'].apply(pd.to_numeric, errors='raise')
    # P-Values should be always > 0.
    # However, while converting, some columns has very small value (3.0* 10^-235) are deemed as zero. This will raise
    # problem in the next step when transforming the float into log10 format. Therefore drop the rows that has P-value = 0
    df.drop(df[df['P-VALUE'] <= 0].index, inplace = True)
    # copy a column P-VALUE
    df['P-VALUE log10-n'] = df['P-VALUE']
    # transform into log10-n format
    df['P-VALUE log10-n'] = df['P-VALUE log10-n'].apply(lambda x: -math.log10(float(x)))
    return df



# Web query response check.
def query_check(response):
    if response.ok:
        return True
    else:
        print('Something is wrong. Please check the query source website status.')
        print('Error code: ', response)
        return False



# Query imported GWAS_AID database
def disease_to_genes(df, disease, logpvalue=6):
    # Select a series of GENES where DZ_NAME is the same as disease
    df = df[df['P-VALUE log10-n'] > logpvalue ]
    genes = df[df['DZ_NAME'] == disease]['REPORTED GENE(S)']
    gene_list = genes.tolist()
    genes = []
    for gene in gene_list:
        if ',' in gene:
            gene_possibilities = gene.split(',')
            for gene_pos in gene_possibilities:
                gene_pos = gene_pos.strip()
                if gene_pos not in genes:
                    genes.append(gene_pos)
        elif gene == 'NR' or gene == 'intergenic' or gene == 'Intergenic':
            pass
        else:
             if gene not in genes:
                genes.append(gene)
             else:
                 pass
    return disease, genes


def search_lit(disease, genes):
    # Create a dictionary for a certain disease to collect query data from pubtator (pubmed).
    pubtator_dic = {disease:{}}
    ##############
    ##STEP 1: Query pubmed for " disease + each gene from the GWAS result"
    ##############
    start_time = time.ctime()
    counter = 0
    for gene in genes:
        # create a part of the dictionary for each gene to update the main dictionary (for disease) each time.
        pubtator_dic_tmp1 = {gene:{}}
        pubtator_dic[disease].update(pubtator_dic_tmp1)
        counter += 1
        # create pubmed search term formed by disease + gene from the list of the disease
        pubmed_term = disease + "[MeSH Term]" + " AND " + disease + "[Title/Abstract]" + " AND " + gene + "[Title/Abstract]"
        # create payload for querying.
        payload_eutils = {'db':'pubmed','term':pubmed_term,'usehistory':'y'}
        # inform user which gene the computer is currently querying and what time when the query starts.
        print(time.ctime() + " Querying gene " + str(counter) + ", " + str(gene))
        # REST-FUL API access
        response_xml = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi", params = payload_eutils)
        # check response
        if query_check(response_xml) != True:
            raise Exception
        time.sleep(0.4)  # E-utilitz asked user not to send more than 3 url queries in 1 second. Sleep 0.4 second to delay the process
        try:
            # transform the xml result from the first query into dictionary format. Find useful information ( pubmed id)
            # and further analysis if there are chemicals (drugs) presented in the abstracts of these papers.
            pmid_dic = xmltodict.parse(response_xml.text)
            pmid_entry = pmid_dic['eSearchResult']['WebEnv'] # this is useful for retrieving this record of search history (not in use at the moment.)
            pubtator_dic[disease][gene]['pmid_entry'] = pmid_entry
            pmid_list = pmid_dic['eSearchResult']['IdList']['Id']  # when search result is 0 hits:  'IdList' is NoneType (TypeError)
            # pmid_list is to be used in the next pubtator query.
            pubtator_dic[disease][gene]['pmid_list'] = pmid_list
            # Calculate the amount of literature
            pubtator_dic[disease][gene]['Disease-Gene related literature amount'] = len(pmid_list)
        except TypeError:
            # if there are no related disease - gene papers, assign the following params as '', [], and None.
            pmid_list = ''
            pubtator_dic[disease][gene]['pmid_list'] = []
            pubtator_dic[disease][gene]['pmid_entry'] = None
        except Exception as err:
            # catch other unexpected errors and keep the program running
            pmid_list = ''
            print(err)
        ##############
        ##STEP 2: Literature curation via pubtator web-service for chemicals in the abstract of related literature.
        ##############
        try:
            if pmid_list == '':
                # if pmid_list is empty string, skip the next pubtator query step.
                raise Exception
            elif isinstance(pmid_list, list) == True:
                # if pmid is a list, join the ids into a string (to become a valid format for next querying step.)
                pubtator_input = ",".join(pmid_list)
            elif isinstance(pmid_list, str) == True:
                # if the pmid_list contain only 1 pumbed entry, it will be a string instead of a list. Use the string
                # in next querying step directly.
                pass
            else:
                # catch other errors.
                raise Exception
            # query the pubtator to acquire related chemicals names and amount.
            response_pubtator = requests.get('https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Chemical/'
                                             + pubtator_input +'/JSON')
            if query_check(response_xml) != True:
                raise Exception
            text_pubtator = response_pubtator.text
            # The returned structure has two formats, error or success. Both are not JSON structures.
            # 1. Error messages starts with [Error] :
            if '[Error] :' in text_pubtator:
                print(gene, 'Error message presented. Skip PubTator querying step.')
                continue
            # 2. Successful query: format: {dic1, dic2, dic3, dic4, dic5, dic6} <-- not a json format. (Not {key: value})
            # Correct it to JSON format by string manipulation.
            text_pubtator = text_pubtator[1:-2]
            text_pubtator = '[' + text_pubtator + ']'
            text_pubtator = '{"top":' + text_pubtator + '}'
            # load the corrected json into python dictionary
            pub_json_load = json.loads(text_pubtator)
            # Collect the chemicals information from the json transformed dictionary.
            chemicals = []
            for i in range(0,len(pub_json_load['top'])):
                for j in range(0,len(pub_json_load['top'][i]['denotations'])): # raise TypeError when some key is absent
                    chem = pub_json_load['top'][i]['denotations'][j]['obj']    # raise TypeError when some key is absent
                    # "chem" has a string format:  "Chemical:xxxxxxxx (three types: 1. CHEBI:xxxxx, 2. Cxxxxxx, 3.  Dxxxxxx)
                    # Retrieve the last part of the string after ":" as chem id for further use.
                    chem_id = chem.split(':')[-1]
                    # collect the not repeated occurrence.
                    if chem_id not in chemicals:
                        if chem_id != '':
                            chemicals.append(chem_id)
            pubtator_dic[disease][gene]['chemicals'] = chemicals
            pubtator_dic[disease][gene]['Gene related chemical counts'] = len(chemicals)
        except Exception as err:  # when search result is 0 hits.
            pubtator_dic[disease][gene]['chemicals'] = None
            pubtator_dic[disease][gene]['Gene related chemical counts'] = 0
    # pubtator_dic contains all useful information extracted from the query. (Further save as json for future use.)
    # extract the information for plotting barchart comparison between gene (major output) and save as dataframe (df_pubtator)
    df_pubtator = pd.DataFrame.from_dict(pubtator_dic[disease],orient = 'index')
    print("End query.")
    # inform the user the total query time.
    print("Total querying time from \n" + start_time+ '\n' + time.ctime())
    return pubtator_dic, df_pubtator

# save result df to pickle file
def df_to_pickle(df, filename):
    print('Pickle file saved. ')
    df.to_pickle('./data/' + filename)


def write_txt(dic, filename):
    print('.txt file saved. ')
    with open('./data/'+ filename + ".txt", 'w') as file:
        file.write(str(dic))

def dic_json(dic, filename):
    print('json file saved. ')
    with open('./data/' + filename + '_json.txt', 'w') as outfile:
        json.dump(dic, outfile)


# read df as a pickle file for further analysis ( not included in the moment)
def read_pickle_df(filepath):
    df = pd.read_pickle(filepath)
    return df

# read in json file to a dic ( not included in the moment)
def read_json(filepath):
    dic = json.load(filepath)
    return dic

