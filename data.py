import numpy as numpy
import pandas as pd
import numpy as np
import json 
from chembl_webresource_client.new_client import new_client
# Read data
raw_df = pd.read_csv('chembl_airflow/DAG/whole_record.csv')
with_NADPH_df = pd.read_csv('chembl_airflow/DAG/result_currated.csv')
filtered_df = pd.read_csv('chembl_airflow/DAG/result_without_filter.csv')
strict_df = pd.read_csv('chembl_airflow/DAG/rresult_strict.csv')

molecule_ids= list(with_NADPH_df['molecule_chembl_id'])
assay_ids= list(with_NADPH_df['assay_chembl_id'])
doc_ids= list(with_NADPH_df['assay_chembl_id'])

#define chembl api
molecule = new_client.molecule
mols = molecule.filter(molecule_chembl_id__in = molecule_ids).only(['molecule_properties'])
#feature for ml methods
chem_property=['full_molformula','full_mwt','psa','alogp']
results=[]
for mol in mols:
        results.append(list(mol[x] for x in chem_property))
chem_results=pd.DataFrame(np.array(results), columns=[['Formula','MW','PSA','AlogP']])

#assay record for further db set up
assay = new_client.assay
asys = pd.DataFrame(assay.filter(assay_chembl_id__in = assay_ids).only(['description']), columns='assay_description')
#record for further db set up
doc = new_client.document
docs = doc.filter(document_chembl_id__in = doc_ids).only(['joural_full_title','year','abstract','do1','pubmed_id'])
doc_results=pd.DataFrame(docs)

#col_1 & col_2 are training usage
col_1= with_NADPH_df['molecule_chembl_id','canonical_smiles']
col_2= with_NADPH_df['standard_type','standard_units','relation','standard_value']

final_df= pd.concat([col_1, col_2, chem_results, asys, doc_results], axis=1)
final_df.to_csv('hlm_dataset.csv', index=False)

asy_json= dict(zip(molecule_ids,(assay_ids,asys)))
ref_json= dict(zip(molecule_ids,docs))

with open("mol2assay.json", "w") as outfile1: 
        json.dump(asy_json, outfile1)
with open("mol2doc.json", "w") as outfile2: 
        json.dump(ref_json, outfile2)