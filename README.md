# Setup
https://github.com/sec-edgar/sec-edgar
```shell
pip install nest-asyncio
pip install secedgar
```

to convert your notebook
```
ipython nbconvert --to python *.ipynb
```

to ingest filings, run file https://github.com/stancsz/dt-secedgar-filings/blob/master/ingest-secedgar-filings.py
specifics, refer to this doc
https://sec-edgar.github.io/sec-edgar/


# What's done
for the most interesting data: financial reports, the reports is already avaliable at:
```
parsed_filings/0000950123-10-030164/0.Financial_Report.xls

parsed_filings/0001326380-18-000033/0.Financial_Report.xlsx

```

# What's left to do
feel free to write codes to load & combine them
suggestions:
https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html


# Noice to haves
Would be nice to have if we can periodically generate some reports and update our stakeholders at wsb
https://www.reddit.com/r/wallstreetbets/
