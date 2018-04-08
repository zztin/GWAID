import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import xmltodict
import json
import time
import re

def gwas_import_aid():
    df_ori = pd.read_csv("./data/gwas_catalog_v1.0.1-associations_e91_r2018-02-13.tsv",sep='\t',low_memory=False)
    df = df_ori[['DISEASE/TRAIT', 'STRONGEST SNP-RISK ALLELE', "SNPS", "P-VALUE", 'REPORTED GENE(S)',
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
    df.drop(labels = df[df['DZ_ID'] == ''].index, inplace = True)  # Warning! copy version
    df.reset_index(inplace= True)
    # convert all values in p-value column to float : Warning! copy version
    #df = df.infer_objects()
    df['P-VALUE'] = df['P-VALUE'].apply(pd.to_numeric, downcast='float', errors='ignore')
    return df

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
                gene_pos.strip()
                if gene_pos not in genes:
                    genes.append(gene_pos)
        elif gene == 'NR' or gene == 'intergenic':
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
    pubtator_input_list = []
    pubtator_dic = {disease:[{}, {'gene amount':len(genes)}]}
    print(time.ctime()) #
    for gene in genes:
        pubtator_dic_gene = {gene:{'input':None,'chemicals':None, 'amount_chem':None}}
        pubtator_dic[disease][0].update(pubtator_dic_gene)
        #pubtator_dic[disease] = {gene: {}}
        #pubtator_dic[disease][gene] = {'length': []}
        #pubtator_dic[disease][gene]['length'] = len(genes)
        pubmed_term = disease + "[MeSH Term]" + " AND " + disease + "[Title/Abstract]" + " AND " + gene + "[Title/Abstract]"
        # search each search term formed by disease + gene from the list of the disease
        payload_eutils = {'db':'pubmed','term':pubmed_term,'usehistory':'y'}
        response_xml = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi", params = payload_eutils)
        query_check(response_xml)
        time.sleep(0.7)  # E-utilitz asked user not to send more than 3 url queries in 1 second. Sleep 0.7 second to delay the process
        pmid_dic = xmltodict.parse(response_xml.text)
        # pmid_entry = pmid_dic['eSearchResult']['WebEnv'] # this is useful for retrieving this record of search history (not in use at the moment.)
        try:
            pmid_list = pmid_dic['eSearchResult']['IdList']['Id']              # Raise TypeError when some key is absent
            pubtator_input = ",".join(pmid_list)
            pubtator_dic[disease][0][gene]['input'] = pubtator_input
            pubtator_input_list.append(pubtator_input)    # pubtator_input_list has the order according to the genes related to a disease
            response_pubtator = requests.get('https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Chemical/'
                                             + pubtator_input +'/JSON')
            query_check(response_xml)
            text = response_pubtator.text  # {dic1,dic2,dic3,dic4,dic5,dic6} <--- structure is wrong. Is not a JSON structure.
            # Correct it to JSON format by string manipulation.
            if 'Error' in text:
                continue
            text = text[1:-2]
            text = '[' + text + ']'
            text = '{"top":' + text + '}'
            # load json into python dictionary
            pub_json_load = json.loads(text)
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
            pubtator_dic[disease][gene]['amount_chem'] = len(chemicals)
            print(time.ctime())
        except TypeError:  # when search result is 0 hits:  'IdList' is NoneType
            pubtator_dic[disease][0][gene]['input'] = None
            pubtator_dic[disease][0][gene]['chemicals'] = None
            pubtator_dic[disease][0][gene]['amount_chem'] = 0
    print(pubtator_dic) #
    df_pubtator = pd.DataFrame.from_dict(pubtator_dic)  # NEW
    print(time.ctime())  #
    print(df_pubtator)
    return df_pubtator

df = gwas_import_aid()
disease, genes = disease_to_genes(df, 'Asthma')
df_pubtator = search_lit(disease, genes)