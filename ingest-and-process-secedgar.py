#!/usr/bin/env python
# coding: utf-8

# [sec official endpoints](https://www.sec.gov/developer)
# 
# [sec edgar](https://www.sec.gov/edgar/)
# 
# [python tool](https://sec-edgar.github.io/sec-edgar/)

# # Ingest Data

# In[8]:


import nest_asyncio
nest_asyncio.apply()


# In[19]:


from secedgar.filings import Filing, FilingType

# 10Q filings for Apple (ticker "aapl")
from secedgar.filings import Filing, FilingType

my_filings = Filing(cik_lookup=['gme'],
                    filing_type=FilingType.FILING_10K,
                    count=1326380, # all avaliable gme reports
                   user_agent='deeptendies')

my_filings.save('filings')


# # Parse Data

# In[56]:


import glob
from secedgar.parser import MetaParser
from pathlib import Path

out_dir='parsed_filings'
Path(out_dir).mkdir(parents=True, exist_ok=True)

directory='filings'
for filepath in glob.iglob('filings/*/*/*.txt'):
    print(filepath)
    parser=MetaParser()
    parser.process(infile=filepath, out_dir=out_dir, create_subdir=True, rm_infile = False)


# # Extract Data
# extra data from a specific report type, and put them in a result list

# After parsing, the parsed data will be created at `out_dir='parsed_filings'`
# need to access the file like so:

# In[80]:


import json
import os
# os.walk(out_dir)
results = []
filings=[x[0] for x in os.walk(out_dir)]
for i in filings:
    meta=os.path.join(i, '*metadata.json')
    for filepath in glob.iglob(meta):
        print(filepath)
        with open(filepath) as file:
            data = json.load(file)
            for doc in data['documents']:
                if doc['type'] == '10-K':
                    print (doc['filename'])
                    filepaths2 = os.path.join(i, '*'+doc['filename'])
                    for filepath2 in glob.iglob(filepaths2):
                        with open(filepath2, 'r') as file2:
                            print (file2)
                            result = file2.read()
                            results.append(result)


# # What's left to do?
# Scrape & mine data
# 
# with the above code, all the 10-k filing reports's html are stored in the result list, use beautiful soup & data scraping techniques to extra the business information you're interested in. 
# 
# resources:
# https://realpython.com/beautiful-soup-web-scraper-python/

# In[79]:


result

