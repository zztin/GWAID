import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import xmltodict
import json

# Import AID database (= db) from gwas catalog database
# def match(df):
#     for dz in aid:
#         po = df.loc[dz in df['DISEASE/TRAIT']]['DZ_ID'] = 1
#         df.loc[dz in df['DISEASE/TRAIT']]['DZ_CAT'] = dz
#
#         df[]

    # d_arr = df_ori['DISEASE/TRAIT'].values
    # d_list = d_arr.tolist()
    # d_list = []  # Disease/Trait name list
    # for dz in d_arr:
    #     if dz not in d_list:
    #         d_list.append(dz)
    #     else:
    #         pass
    #

    # Find all related phenotypes including the search terms in list aid (such as "Asthma related to air pollution" etc)
    #match_list = []
    #match_dic = {}



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


# Query imported GWAS_AID database
def phenotype_to_gene(df, disease):
    phenotype = df[df['DISEASE/TRAIT'] == disease]
    genes = phenotype['REPORTED GENE(S)']
    genes_and_id = phenotype[['REPORTED GENE(S)', 'SNP_GENE_IDS']]
    gene_id_up_sr = phenotype['UPSTREAM_GENE_ID']
    gene_id_dw_sr = phenotype['DOWNSTREAM_GENE_ID']
    gene_id_sr = phenotype['SNP_GENE_IDS']
    gene_id_input = gene_id_sr.tolist()
    # compare which is easier to use
    gene_list = genes.tolist()
    genes = []
    # print(gene_list)  # test
    for gene in gene_list:
        if gene == 'NR' or gene == 'intergenic':
            pass
        else:
            if gene not in genes:
                genes.append(gene)
    return (disease, genes)

def pmsearch_term_gen(disease, genes):
    pmterm_dic = {}
    pmterm_list = []
    for gene in genes:
        pubmed_term = disease + "[MeSH Term]" + disease + "[Title/Abstract]" + " AND " + gene + "[Title/Abstract]"
        pmterm_list.append(pubmed_term)
    pmterm_dic[gene] = pmterm_list
    return pmterm_dic

# Web query response check
def query_check(response):
    if response.ok:
        pass
    else:
        print('Something is wrong. Please check the query source website status.')
        print('Error code: ', response)



def search_lit(disease, genes):
    for gene in genes:
        pubmed_term = disease + "[MeSH Term]" + disease + "[Title/Abstract]" + " AND " + gene + "[Title/Abstract]"
        # search each search term formed by disease + gene from the list of the disease
        payload_eutils = {'db':'pubmed','term':pubmed_term,'usehistory':'y'}
        response_xml = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi", params = payload_eutils)
        query_check(response_xml)
        pmid_dic = xmltodict.parse(response_xml.text)
        # pmid_entry = pmid_dic['eSearchResult']['WebEnv'] # this is useful for retrieving this record of search history (not in use at the moment.)
        pmid_list = pmid_dic['eSearchResult']['IdList']['Id']
        return pmid_list

def pubtator_chemicals(pmid_list):
    pmid_input = ",".join(pmid_list)
    response_pubtator = requests.get('https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Chemical/'
                                     + pmid_input +'/JSON')
    text = response_pubtator.text  # {dic1,dic2,dic3,dic4,dic5,dic6} <--- structure is wrong. Is not a JSON structure.
    # Correct it to JSON format by string manipulation.
    text = text[1:-2]
    text = '[' + text + ']'
    text = '{"top":' + text + '}'
    # load json into python dictionary
    pubtator_dic = json.loads(text)
    chemicals = []
    for i in range(0,len(pubtator_dic['top'])):
        for j in range(0,len(pubtator_dic['top'][i]['denotations'])):
            chem = pubtator_dic['top'][i]['denotations'][j]['obj']
            if chem not in chemicals:
                chemicals.append(chem)
    print(chemicals)

