import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import xmltodict
import json
import time
import re
import csv
import math


import user_helper as uh

def gwas_import_aid():
    df = pd.read_csv("./data/gwas_catalog_v1.0.1-associations_e91_r2018-02-13.tsv",sep='\t',low_memory=False)
    df = df[['DISEASE/TRAIT', 'STRONGEST SNP-RISK ALLELE', "SNPS", "P-VALUE", 'REPORTED GENE(S)',
                  'MAPPED_GENE', 'UPSTREAM_GENE_ID', 'DOWNSTREAM_GENE_ID', 'SNP_GENE_IDS', 'MAPPED_TRAIT',
                  'MAPPED_TRAIT_URI', 'PUBMEDID', 'FIRST AUTHOR', 'DATE', 'JOURNAL']]
    df.insert(loc=1, column="DZ_NAME", value="")
    df.insert(loc=1, column="DZ_ID", value="")
    aid = ['Behcet\'s disease', 'Crohn\'s disease', 'Asthma', 'Atopic dermatitis',
                'Primary sclerosing cholangitis', 'Alopecia areata', 'Type 1 diabetes', 'Ankylosing spondylitis',
                'Systemic sclerosis', 'Vitiligo', 'Kawasaki disease', 'Psoriasis', 'Celiac disease',
                'Systemic lupus erythematosus', 'Ulcerative colitis']
    i = 0
    for dz in aid:
        i += 1
        df_temp = df[df['DISEASE/TRAIT'].str.contains(dz)]['DZ_NAME'].apply(lambda x: dz)
        df_temp2 = df[df['DISEASE/TRAIT'].str.contains(dz)]['DZ_ID'].apply(lambda x: i)
        df.update(df_temp)
        df.update(df_temp2)
    df.drop(labels = df[df['DZ_ID'] == ''].index, inplace = True)
    df.reset_index(inplace= True)
    # convert all values in p-value column to float : Warning! copy version
    #df = df.infer_objects()
    df['P-VALUE'] = df['P-VALUE'].apply(pd.to_numeric, errors='raise')
    df.drop(df[df['P-VALUE'] <= 0].index, inplace = True
    df['P-VALUE log10-n'] = df['P-VALUE']
    df['P-VALUE log10-n'] = df['P-VALUE log10-n'].apply(lambda x: -math.log10(float(x)))
    print(df['P-VALUE log10-n'])
    return df



def log_p(x):
    result = -(math.log10(x))
    return result


# Web query response check.
def query_check(response):
    if response.ok:
        pass
    else:
        print('Something is wrong. Please check the query source website status.')
        print('Error code: ', response)


# Query imported GWAS_AID database
def disease_to_genes(df, disease):
    # Select a series of GENES where DZ_NAME is the same as disease
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


# redundant
# def pmsearch_term_gen(disease, genes):
#     pmterm_dic = {}
#     for gene in genes:
#         pubmed_term = disease + "[MeSH Term]" + " AND " + disease + "[Title/Abstract]" + " AND " + gene + "[Title/Abstract]"
#         pmterm_dic[gene] = pubmed_term
#     return pmterm_dic


def search_lit(disease, genes):
    start_time = time.ctime()   ###########################
    #pubtator_input_list = []
    pubtator_dic = {disease:{}}
    counter = 0
    for gene in genes:
        pubtator_dic_tmp1 = {gene:{}}
        pubtator_dic[disease].update(pubtator_dic_tmp1)
        counter += 1
        pubmed_term = disease + "[MeSH Term]" + " AND " + disease + "[Title/Abstract]" + " AND " + gene + "[Title/Abstract]"
        # search each search term formed by disease + gene from the list of the disease
        payload_eutils = {'db':'pubmed','term':pubmed_term,'usehistory':'y'}
        print(time.ctime() + " Querying gene " + str(counter) + ", " + str(gene))  #######################################################
        response_xml = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi", params = payload_eutils)
        query_check(response_xml)
        pm_search = response_xml.text
        time.sleep(0.5)  # E-utilitz asked user not to send more than 3 url queries in 1 second. Sleep 0.5 second to delay the process
        try:
            pmid_dic = xmltodict.parse(pm_search)
            pmid_entry = pmid_dic['eSearchResult']['WebEnv'] # this is useful for retrieving this record of search history (not in use at the moment.)
            pubtator_dic[disease][gene]['pmid_entry'] = pmid_entry
            pmid_list = pmid_dic['eSearchResult']['IdList']['Id']
            # Raise TypeError when returning no search results. When search result is 0 hits:  'IdList' is NoneType
            pubtator_dic[disease][gene]['pmid_list'] = pmid_list
            pubtator_dic[disease][gene]['Disease-Gene related literature amount'] = len(pmid_list)
        except TypeError:
            pmid_list = ''
            pubtator_dic[disease][gene]['pmid_list'] = []
            pubtator_dic[disease][gene]['pmid_entry'] = None
        except Exception as err:
            pmid_list = ''
            print(err)             ##########
        try:
            if pmid_list == '':
                raise Exception
            elif isinstance(pmid_list, list) == True:
                pubtator_input = ",".join(pmid_list)  # if pubtator_input = None--> stop trying to query
            #pubtator_input_list.append(pubtator_input)    # pubtator_input_list has the order according to the genes related to a disease
            elif isinstance(pmid_list, str) == True:
                pass
            else:
                raise Exception
            response_pubtator = requests.get('https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Chemical/'
                                             + pubtator_input +'/JSON')
            query_check(response_xml)
            text_pubtator = response_pubtator.text  # {dic1,dic2,dic3,dic4,dic5,dic6} <--- structure is wrong. Is not a JSON structure.
            # Correct it to JSON format by string manipulation.
            if '[Error] :' in text_pubtator:
                print(gene, 'Error message presented. Skip PubTator querying.')
                continue
            text_pubtator = text_pubtator[1:-2]
            text_pubtator = '[' + text_pubtator + ']'
            text_pubtator = '{"top":' + text_pubtator + '}'
            # load json into python dictionary
            pub_json_load = json.loads(text_pubtator)
            chemicals = []
            for i in range(0,len(pub_json_load['top'])):
                for j in range(0,len(pub_json_load['top'][i]['denotations'])): # Raise TypeError when some key is absent
                    chem = pub_json_load['top'][i]['denotations'][j]['obj']    # Raise TypeError when some key is absent
                    # format of "chem" is "Chemical : chemical_ID (starts from CHEBI:, C, D)
                    # Retrieve the last part of the string after ":" as chem id
                    chem_id = chem.split(':')[-1]
                    if chem_id not in chemicals:
                        if chem_id != '':
                            chemicals.append(chem_id)
            pubtator_dic[disease][gene]['chemicals'] = chemicals             # REWRITE! DID NOT CONTAIN THE DATA BEFORE
            pubtator_dic[disease][gene]['Gene related chemical counts'] = len(chemicals)
        except Exception as err:  # when search result is 0 hits:  'IdList' is NoneType
            pubtator_dic[disease][gene]['chemicals'] = None
            pubtator_dic[disease][gene]['Disease-Gene related chemical counts'] = 0
    # pubtator_dic contains all useful information extracted from the query. (Further save as json for future use.)
    print(pubtator_dic) ##########
    # extract the information for plotting barchart comparison between gene (major output)
    df_pubtator = pd.DataFrame.from_dict(pubtator_dic[disease],orient = 'index')
    print("END")                             #########################
    print("Total querying time from \n" + start_time+ '\n' + time.ctime())  #########################
    return pubtator_dic, df_pubtator


# def dic_to_json(pubtator_dic, filename):
#     pubtator_json = json.dumps(pubtator_dic)
#     f = open(filename, 'w')
#     f.write(pubtator_json)
#     f.close

# save result df to pickle file
def df_to_pickle(df, filename):
    print('Pickle file saved. ')
    df.to_pickle('./data/' + filename)


def write_txt(dic, filename):
    print('.txt file saved. ')
    with open('./data/'+ filename, 'w') as file:
        file.write(str(dic))

def dic_json(dic, filename):
    print('json file saved. ')
    with open('./data/' + filename + '.txt', 'w') as outfile:
        json.dump(dic, outfile)


# read df as a pickle file for further analysis
def read_pickle_df(filepath):
    df = pd.read_pickle(filepath)
    return df

# read in json file to a dic
def read_json(filepath):
    dic = json.load(filepath)
    return dic

gwas_import_aid()