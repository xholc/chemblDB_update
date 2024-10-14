import re
from chembl_webresource_client.new_client import new_client
import pandas as pd

activity = new_client.activity
res= activity.filter(description__icontains="human liver microsome")
res= res.filter(target_organism='Homo sapiens')
res= res.filter(standard_type='T1/2')
res= res.filter(standard_units='hr')
res2= res.only(['assay_chembl_id','assay_description','assay_type','bao_format','canonical_smiles','document_chembl_id','molecule_chembl_id','relation','standard_type','standard_units','standard_value','target_chembl_id','target_organism'])

df_raw= pd.DataFrame(res)
df= pd.DataFrame(res2)
key_words_pattern = r'\b(?:pH\s*7|NADPH)\b'
ng_words_pattern = r'\b(?:inhibitor|UDPGA|supersomes)\b'

# Function to check if a string contains a match for a given pattern
def contains_pattern(text, pattern):
    return bool(re.search(pattern, text, re.IGNORECASE))

# Create a new dataframe with rows containing key words
df_key_words = df[df['assay_description'].apply(lambda x: contains_pattern(x, key_words_pattern))]

# Remove rows containing NG words from the original dataframe
df_without_ng = df[~df['assay_description'].apply(lambda x: contains_pattern(x, ng_words_pattern))]

# strict
df_strict = df_key_words[~df_key_words['assay_description'].apply(lambda x: contains_pattern(x, ng_words_pattern))]

df_raw.to_csv('whole_record.csv', index=False)
df_key_words.to_csv('result_currated.csv', index=False)
df_without_ng.to_csv('result_without_filter.csv', index=False)
df_strict.to_csv('result_strict.csv', index=False)
