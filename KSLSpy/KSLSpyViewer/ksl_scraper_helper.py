############################################# spoof user agent
import random

possible_headers = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30",
]

def get_random_header():
    random_index = random.randint(0, len(possible_headers) - 1)
    return possible_headers[random_index]
################################################################################ end spoof user agent
import json
from bs4 import BeautifulSoup
import requests

def get_query_results(query_json_object):
    query_dict = json.loads(query_json_object)

    keywords = ""
    category = ""
    lower_price = ""
    higher_price = ""
    zipcode = ""
    distance_from_zip = ""
    seller_type = ""
    listing_type = ""
    has_photos = ""
    time_since_posted = ""

    # keywords = "i5 computer"
    # keywords = keywords.split(" ")
    # keywords = [x+"%20" for x in keywords]
    # keywords = "".join(keywords)
    # category = "Computers"
    # #print keywords
    # lower_price = "100"
    # higher_price = "500"
    # zipcode = "84339"
    # distance_from_zip = "50"
    # seller_type = "Private"
    # listing_type = "Sale"
    # has_photos = "Has Photos"
    # time_since_posted = "30DAYS"


    #must handle missing query fields -keys will be present with no value
    if 'keywords' in query_dict:
        keywords = query_dict['keywords']
        keywords = keywords.split(" ")
        keywords = [x+"%20" for x in keywords]
        keywords = "".join(keywords)
    #print keywords
    if 'category' in query_dict:
        category = query_dict['category']
    if 'lower_price' in query_dict:
        lower_price = query_dict['lower_price']
        higher_price = query_dict['higher_price']
        zipcode = query_dict['zipcode']
        distance_from_zip = query_dict['distance_from_zip']
        seller_type = query_dict['seller_type']
        listing_type = query_dict['listing_type']
        has_photos = query_dict['has_photos']
        time_since_posted = query_dict['time_since_posted']

    print query_dict

    # In[57]:


    url = "https://www.ksl.com/classifieds/search?category[]="+category+"&subCategory[]=&keyword="+keywords+"&priceFrom=%24"+lower_price+"&priceTo=%24"+higher_price+"&zip="+zipcode+"&miles="+distance_from_zip+"&sellerType[]="+seller_type+"&marketType[]="+listing_type+"&hasPhotos[]="+has_photos+"&postedTimeFQ[]="+time_since_posted
    print url
    #url = "https://www.ksl.com/classifieds/search?category[]=Computers&subCategory[]=&keyword=i5%20computer&priceFrom=%24100&priceTo=%24500&zip=84339&miles=50&sellerType[]=Private&marketType[]=Sale&hasPhotos[]=Has%20Photos&postedTimeFQ[]=30DAYS"
    #print url

    headers = {'User-Agent': get_random_header()}
    #print headers
    downloaded_html = ""
    downloaded_html = requests.get(url, headers=headers)
    downloaded_html = downloaded_html.text.encode('utf-8')
    # with open("test.html", "r") as file:
    # 	downloaded_html = file.read()
    soup = BeautifulSoup(downloaded_html, 'html.parser')


    # In[58]:


    container_div = soup.find("div", { "class" : "listing-group" })
    #print container_div
    if container_div is None:#no listings under query
        import sys
        sys.exit()


    # In[59]:


    listings = container_div.find_all("div", { "class" : "listing" })
    #print listings[7]


    # In[60]:

    for element in listings:
        results_json = {}##each result will be yielded one by one as a json object. The Results DB will have a list of results, identifiable by Query id

        title = element.find("a", { "class" : "link" }).next.strip()
        results_json['title'] = title
        #print title
        description = element.find("div", { "class" : "description-text ellipsis" }).next.strip()
        results_json['description'] = description
        #print description
        price = element.find("h3", { "class" : "price listing-detail-line" }).next.strip()
        results_json['price'] = price
        #print price
        image_link = element.find("div", { "class" : "photo" }).find("img")['src']
        image_link = "https:"+image_link
        results_json['image_link'] = image_link
        #print image_link
        time_on_site = element.find("span", { "class" : "timeOnSite" }).next.strip("|").strip()
        results_json['time_on_site'] = time_on_site
        #print time_on_site
        address = element.find("span", { "class" : "address" }).next.strip()
        results_json['address'] = address
        #print address
        views = element.find("span", { "class" : "text" }).next.strip()
        results_json['views'] = views
        #print views
        likes = element.find("span", { "class" : "favorite-number text" }).next.strip()
        results_json['likes'] = likes
        #print likes

        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        print results_json
        yield json.dumps(results_json)
