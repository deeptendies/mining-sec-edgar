import re
import requests
import unicodedata
from bs4 import BeautifulSoup

def restore_windows_1252_characters(restore_string):
    """
        Replace C1 control characters in the Unicode string s by the
        characters at the corresponding code points in Windows-1252,
        where possible.
    """

    def to_windows_1252(match):
        try:
            return bytes([ord(match.group(0))]).decode('windows-1252')
        except UnicodeDecodeError:
            # No character at the corresponding code point: remove it.
            return ''

    return re.sub(r'[\u0080-\u0099]', to_windows_1252, restore_string)


def scrape_table_dictionary(table_dictionary):
    # initalize a new dicitonary that'll house all your results
    new_table_dictionary = {}
    if len(table_dictionary) != 0:
        # loop through the dictionary
        for table_id in table_dictionary:
            # grab the table
            table_html = table_dictionary[table_id]

            # grab all the rows.
            table_rows = table_html.find_all('tr')

            # parse the table, first loop through the rows, then each element, and then parse each element.
            parsed_table = [
                [element.get_text(strip=True) for element in row.find_all('td')]
                for row in table_rows
            ]

            # keep the original just to be safe.
            new_table_dictionary[table_id]['original_table'] = table_html

            # add the new parsed table.
            new_table_dictionary[table_id]['parsed_table'] = parsed_table
            # here some additional steps you can take to clean up the data - Removing '$'.
            parsed_table_cleaned = [
                [element for element in row if element != '$']
                for row in parsed_table
            ]
            # here some additional steps you can take to clean up the data - Removing Blanks.
            parsed_table_cleaned = [
                [element for element in row if element != None]
                for row in parsed_table_cleaned
            ]
    else:
        # if there are no tables then just have the id equal NONE
        new_table_dictionary[1]['original_table'] = None
        new_table_dictionary[1]['parsed_table'] = None
    return new_table_dictionary
######################################################################################################
new_html_text = r"https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/0000320193-18-000145.txt"
response = requests.get(new_html_text)
soup = BeautifulSoup(response.content, 'lxml')
master_filings_dict = {}
company = 'AAPL'
master_filings_dict[company] = {}

# initalize the dictionary that will house all of our documents
master_document_dict = {}

# find all the documents in the filing.
for filing_document in soup.find_all('document'):
    # define the document type, found under the <type> tag, this will serve as our key for the dictionary.
    document_id = filing_document.type.find(text=True, recursive=False).strip()
    if document_id != "10-K":
        print('not 10-K')
        break
    # here are the other parts if you want them.
    document_sequence = filing_document.sequence.find(text=True, recursive=False).strip()
    document_filename = filing_document.filename.find(text=True, recursive=False).strip()
    document_description = filing_document.description.find(text=True, recursive=False).strip()
    #print(document_id, document_description, document_sequence, document_filename)
    # initalize our document dictionary
    master_document_dict[document_id] = {}

    # add the different parts, we parsed up above.
    master_document_dict[document_id]['document_sequence'] = document_sequence
    master_document_dict[document_id]['document_filename'] = document_filename
    master_document_dict[document_id]['document_description'] = document_description

    # store the document itself, this portion extracts the HTML code. We will have to reparse it later.
    master_document_dict[document_id]['document_code'] = filing_document.extract()
    #print(master_document_dict[document_id]['document_code'])
    # grab the text portion of the document, this will be used to split the document into pages.
    filing_doc_text = filing_document.find('text').extract()
    #print(filing_doc_text)
    all_thematic_breaks = filing_doc_text.find_all('hr')
    #print(all_thematic_breaks)
    # convert all thematic breaks to a string so it can be used for parsing
    all_thematic_breaks = [str(thematic_break) for thematic_break in all_thematic_breaks]
    #print(all_thematic_breaks)
    # prep the document text for splitting, this means converting it to a string.
    filing_doc_string = str(filing_doc_text)

    # handle the case where there are thematic breaks.
    if len(all_thematic_breaks) > 0:

        # define the regex delimiter pattern, this would just be all of our thematic breaks.
        regex_delimiter_pattern = '|'.join(map(re.escape, all_thematic_breaks))

        # split the document along each thematic break.
        split_filing_string = re.split(regex_delimiter_pattern, filing_doc_string)

        # store the document itself
        master_document_dict[document_id]['pages_code'] = split_filing_string

    # handle the case where there are no thematic breaks.
    elif len(all_thematic_breaks) == 0:

        # handles so it will display correctly.
        split_filing_string = all_thematic_breaks

        # store the document as is, since there are no thematic breaks. In other words, no splitting.
        master_document_dict[document_id]['pages_code'] = [filing_doc_string]

    #print(master_document_dict[document_id]['pages_code'])
    # display some information to the user.
    #print('-' * 80)
    #print('The document {} was parsed.'.format(document_id))
    #print('There was {} thematic breaks(s) found.'.format(len(all_thematic_breaks)))
    # only do 10-K
    break
master_filings_dict[company]['filing_documents'] = master_document_dict
# first grab all the documents
#################################################################################################
filing_documents = master_filings_dict[company]['filing_documents']

# try2
htmll = r'https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/a10-k20189292018.htm'
rrr = requests.get(htmll).text
soup = BeautifulSoup(rrr, 'lxml')
tbl = soup.find_all("table")
headings = []
for td in tbl:
    headings.append(td.b.text.replace('\n', ' '))
print(headings)
