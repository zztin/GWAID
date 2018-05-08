# Project GWAID 

<>< An Automated Literature Curation Program for Discovering Potential Therapies  
in Genome-Wide Association Studies on Autoimmune Diseases <><

The GWAID project is a data exploration tool focusing on genetic information of autoimmune diseases from
genome wide association studies written in Python programming language. 
The project is a final assignment of the course Computational Thinking, Applied Data Science Profile, Utrecht University. This project focus on the implementation of using API tools and software structural design. Relevance in life science needed to be ingestigated and refined. 

## A quick start:

<>< Configuration requirement
1. Download Anaconda Python 3.6 Distribution according to your OS(MacOS, Linux, or Windows). Available at:
https://www.anaconda.com/download/
2. (Optional) Create a virtual environment for running the program. Instruction check (step 1-4):
https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/

3. install additional Python packages to the virtual environment or to root python installation.
Type these following line into terminal:

pip install xmltodict

<>< Operating instructions

1. Create a folder named data. Download GWAS Catelog all association v1.0.1 Available at:
http://www.ebi.ac.uk/gwas/docs/file-downloads

2. Compare the filename is it is the same with the first file in the list (see below)

2. Open the terminal, go to the directory containing all files

3. run "python main.py "

## Expected Outcomes:

1. Individual Autoimmune disease function: A barchart of literature counts and related chemicals appeared in literature in every genes related to the disease above user-defined cut-off P-Value. As a review of interests of further investigation of disease related genes discovered in GWA studies.

2. Overview function: Return a heatmap and a clustered heatmap for Autoimmune diseases and mutated genes based on P-Value of SNP located in the genes.

3. Figures and details please refer to this PDF document in the link: http://bit.ly/gwaid_project_report


##  List of files included:

1. data/gwas_catalog_v1.0.1-associations_e91_r2018-02-13.tsv
2. data/GWASCatelog
3. dataprep_helper.py
4. main.py
5. plot_helper.py
6. user_helper.py
7. README.TXT


## Copyright and licensing:BSD 3-Clause License

Copyright (c) 2018, zztin
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## Author Contact information:
zzzstop@gmail.com

## References:
#### GWAS data retrieved from GWAS Catelog:

* Burdett T (EBI), Hall PN (NHGRI), Hastings E (EBI), Hindorff LA (NHGRI), Junkins HA (NHGRI), Klemm AK (NHGRI), MacArthur J (EBI), Manolio TA (NHGRI), Morales J (EBI), Parkinson H (EBI) and Welter D (EBI). The NHGRI-EBI Catalog of published genome-wide association studies. Available at: www.ebi.ac.uk/gwas. Accessed 03-05-2018, version v.1.0.1.

#### Web services used in this program:
PubMed E-utilities:

* Sayers E. E-utilities Quick Start. 2008 Dec 12 [Updated 2017 Nov 1]. In: Entrez Programming Utilities Help [Internet]. Bethesda (MD): National Center for Biotechnology Information (US); 2010-.Available from: https://www.ncbi.nlm.nih.gov/books/NBK25500/

PubTator:

* Wei CH et. al., PubTator: A Web-based text mining tool for assisting Biocuration, Nucleic acids research, 2013, 41 (W1): W518-W522

* Wei CH et. al., Accelerating literature curation with text-mining tools: a case study of using PubTator to curate genes in PubMed abstracts, Database (Oxford), 2012, bas041

* Wei CH et. al., PubTator: A PubMed-like interactive curation system for document triage and literature curation,in Proceedings of BioCreative 2012 workshop, Washington DC, USA, 145-150, 2012
