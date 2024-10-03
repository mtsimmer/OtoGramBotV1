"""
Checks meshumashot database
"""
import re
from requests import request
from datetime import datetime
from collections.abc import Iterable
from bs4 import BeautifulSoup, NavigableString, Tag
from config import MESHUMASHOT_HOST, MESHUMASHOT_ENDPOINTS, MESHUMASHOT_REQUEST_TYPE
#curl "https://meshumeshet.com/c/18734101" ^
#  -H "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7" ^
#  -H "accept-language: en-US,en;q=0.9,he-IL;q=0.8,he;q=0.7,fr;q=0.6" ^
#  -H ^"cookie: FCNEC=^%^5B^%^5B^%^22AKsRol8uVF-nn-OXZB8rs9dO7Z685yFJJxcHW20gQ-DMb-UCMMNTLOAvIbqnnSbUDGjkF2-481exZasmiDRn7HbEy2EuodGKw4n4l4lQ7BU34CNCo9rADzUC38EzOKZEOCp6W4PkQDFCYPVeOjVDb-VR2JThjL5tEg^%^3D^%^3D^%^22^%^5D^%^5D; __gads=ID=726a191be147d93d:T=1723318965:RT=1726773561:S=ALNI_MaNOunfkPnfcY-PjuXdY4JZsa3eSA; __gpi=UID=00000ec1d30c00b5:T=1723318965:RT=1726773561:S=ALNI_MbikOLeF4_aKloPnhmBgFifltJGNQ; __eoi=ID=c3c43e1e750aebf9:T=1723318965:RT=1726773561:S=AA-AfjZyzSEzMZG2TFhssBJsYbQf; _ga=GA1.2.1743351088.1723318957; _ga_9DSVX2ELG4=GS1.1.1726773553.2.1.1726774064.60.0.0; PHPSESSID=uig9snqsjjcn9p0nfk6vugtvg4^" ^
#  -H "dnt: 1" ^
#  -H "priority: u=0, i" ^
#  -H "referer: https://meshumeshet.com/" ^
#  -H ^"sec-ch-ua: ^\^"Google Chrome^\^";v=^\^"129^\^", ^\^"Not=A?Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"129^\^"^" ^
#  -H "sec-ch-ua-mobile: ?0" ^
#  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
#  -H "sec-fetch-dest: document" ^
#  -H "sec-fetch-mode: navigate" ^
#  -H "sec-fetch-site: same-origin" ^
#  -H "sec-fetch-user: ?1" ^
#  -H "upgrade-insecure-requests: 1" ^
#  -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"

class Owner:
    """
    A class that represents past owners from meshumashot
    """
    def __init__(self, ownership_date, owner_type):
        self.owner_type = owner_type
        regex_pattern = r'^(0[1-9]|1[0-2])/\d{4}$'
        if not re.match(regex_pattern, ownership_date):
            raise ValueError("Date string must be in the format 'MM/YYYY' with valid month.")
        try:
            self.ownership_date = datetime.strptime(ownership_date, "%m/%Y")
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

    def __repr__(self):
        return "owner:" + self.owner_type + "-" + self.ownership_date.strftime("%m/%Y")

    def __str__(self):
        return "owner:" + self.owner_type + "-" + self.ownership_date.strftime("%m/%Y")

class Comment:
    def __init__(self, mileage_update = None, general_info = None, image_links = None):
        self.general_info = general_info
        self.image_links = image_links
    def __repr__(self):
        return f"general_info={self.general_info}"
    def __str__(self):
        return f"general_info - {self.general_info}"

class Mileage_update:
    def __init__(self,mileage, date):
        self.mileage = mileage
        self.date = datetime.strptime(date, "%m/%Y")
    def __repr__(self):
        return f"{self.date}, mileage_update={self.mileage}"
    def __str__(self):
        return self.date.strftime("%m/%Y")+ f" - {self.mileage}km"

def query(plate):
    url = MESHUMASHOT_HOST + MESHUMASHOT_ENDPOINTS['SEARCH'] + plate
    result = request(MESHUMASHOT_REQUEST_TYPE, url)
    soup = BeautifulSoup(result.content, 'html.parser')
    try:
        owners = extract_past_ownership(soup)
    except LookupError as E:
        owners = "No Owners could be retrieved (Probably too old)"
    mileage_updates,reports = extract_comments(soup)
    return owners,mileage_updates,reports,url

def pretty_query(plate):
    owners, mileage_updates, reports, url = query(plate)
    pretty_string = "according to meshumashot : \n"
    if isinstance(owners, Iterable):
        for owner in owners:
            pretty_string += str(owner) + '\n'
    else:
        pretty_string += 'no owners data :( ' + '\n'
    for report in reports:
        pretty_string += str(report) + '\n'
    for mileague in mileage_updates:
        pretty_string += str(mileague) + '\n'
    pretty_string += '\n for more info: \n' + url
    return pretty_string


# Main function to extract all comments
def extract_comments(soup):
    comments = []
    comments.append(soup.find('section', id='comments'))
    mileage_extraction = comments[0]
    comments_extraction = comments[0]
    mileage_updates = extract_miles_from_comment_row(mileage_extraction)
    comments = extract_raw_comments(comments_extraction)
    return mileage_updates,comments

def extract_miles_from_comment_row(comment_row):
    #row_contents = comment_row.find_all(lambda el: el.tag == "div" and "col-md-12" == el["class"])
    mileage_tags = comment_row.find_all(mile_update_filter)
    #print(mileage_tags)
    return(extract_miles(mileage_tags))

def mile_update_filter(tag):
    if tag.name == "div" and tag.has_attr('class') and tag.attrs['class'] == ['col-md-12'] and tag.next_element.name == "label":
        #ipdb.set_trace()
        return True
    return False

def extract_miles(mileage_tags):
    mileage_updates = []
    for i in range(0,len(mileage_tags),2):
        #print(mileage_tags[i].contents[-1].strip(),mileage_tags[i+1].contents[-1].strip())
        mileage_updates.append(Mileage_update(mileage_tags[i].contents[-1].strip(),mileage_tags[i+1].contents[-1].strip()))
    return(mileage_updates)

def extract_raw_comments(commets_bs):
    comments_tags = commets_bs.find_all(comment_filter)
    #ipdb.set_trace()
    comments = []
    for comment_tag in comments_tags:
        comments.append(Comment(general_info=comment_tag.contents[-1].strip()))
    return comments

#def extract_raw_comment(comments_tags):

def comment_filter(tag):
    if tag.name == "div" and tag.has_attr('class') and tag.attrs['class'] == ['col-md-12'] and tag.parent.has_attr('class') and tag.parent.attrs['class'] == ['row'] and tag.parent.parent.has_attr('class') and tag.parent.parent.attrs['class'] == ['col-md-12', 'col-sm-12'] and tag.next_sibling == None :  
        #ipdb.set_trace()
        return True
    return False

def _is_general_data(contents):
    lbls = contents.find_all('label')
    if lbls == None:
        return contents

def extract_reports(soup):
    """
    Expects a bs4 objects and returs a list of reports
    """
    reports = soup.find('section', id='comments')
    return reports


def extract_past_ownership(soup):
    """
    Expects a bs4 object and returns all past owners according to a table on the site
    """
    try:
        table = soup.find('table')
        ownership_table_header = table.find('th', 'ודש-שנה תחילת בעלות')
        owners = []
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            regex_pattern = r'^(0[1-9]|1[0-2])/\d{4}$'
            if not re.match(regex_pattern, cols[0].text):
                return None
            owners.append(Owner(cols[0].text,cols[2].text))
        return owners
    except AttributeError as E:
        raise LookupError("Unable to parse ownership table section in HTML probably no past owners table")




