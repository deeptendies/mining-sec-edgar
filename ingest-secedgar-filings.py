#!/usr/bin/env python
# coding: utf-8

# [sec official endpoints](https://www.sec.gov/developer)
# 
# [sec edgar](https://www.sec.gov/edgar/)
# 
# [python tool](https://sec-edgar.github.io/sec-edgar/)

# In[8]:


import nest_asyncio
nest_asyncio.apply()


# In[19]:


from secedgar.filings import Filing, FilingType

# 10Q filings for Apple (ticker "aapl")
from secedgar.filings import Filing, FilingType

my_filings = Filing(cik_lookup=['gme'],
                    filing_type=FilingType.FILING_10K,
                    count=1326380,
                   user_agent='deeptendies')

my_filings.save('filings')


# In[ ]:




