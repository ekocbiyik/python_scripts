import requests
from bs4 import BeautifulSoup, NavigableString
import concurrent.futures
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}


def getUrlList(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    url_list = []

    if response.status_code != 200:
        return url_list

    links = soup.find_all("a", target="_self")
    for link in links:
        url_list.append(link.get("href"))

    return url_list


def getContent(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    data = {
        "facilityName": getFacilityName(soup),
        "address": getAddress(soup),
        "contactName": getContactName(soup),
        "jobTitle": getJobTitle(soup),
        "phone": getPhone(soup),
        "fax": getFax(soup),
        "webUrl": getWebUrl(soup),
        "facilityType": getFacilityType(soup),
        "licensedBeds": getLicensedBeds(soup),
    }
    
    return data


def getFacilityName(soup):
    main_div = soup.find(
        "div", {"id": "main", "class": "full_width ill_directory_is_member"}
    )
    element = main_div.find("h1")

    if element:
        return element.get_text(strip=True)

    return ""


def getAddress(soup):
    main_div = soup.find(
        "div", {"id": "main", "class": "full_width ill_directory_is_member"}
    )
    element = main_div.find("p")

    if element and element.contents.__len__() > 0:
        return (
            "".join(map(str, element.contents))
            .replace("<br/>", " ")
            .replace("<b>", "")
            .replace("</b>", "")
            .replace("\n", "")
        )

    return ""


def getContactName(soup):
    main_div = soup.find(
        "div", {"id": "main", "class": "full_width ill_directory_is_member"}
    )
    element = main_div.find("p", {"class": "ill_directory_item_contact_info"})

    if element and element.contents.__len__() > 0:
        return element.contents[0].get_text(strip=True)

    return ""


def getJobTitle(soup):
    main_div = soup.find(
        "div", {"id": "main", "class": "full_width ill_directory_is_member"}
    )
    element = main_div.find("p", {"class": "ill_directory_item_contact_info"})

    if element and element.contents.__len__() > 0:
        if element.contents[1].__len__() > 0:
            if isinstance(element.contents[1].contents[0], NavigableString):
                return element.contents[1].contents[0]

    return ""


def getPhone(soup):
    main_div = soup.find(
        "div", {"id": "main", "class": "full_width ill_directory_is_member"}
    )
    element = main_div.find("p", {"class": "ill_directory_item_contact_info"})

    if element.find("span", {"class": "ill_directory_phone"}):
        return element.find("span", {"class": "ill_directory_phone"}).contents[0]

    return ""


def getFax(soup):
    main_div = soup.find(
        "div", {"id": "main", "class": "full_width ill_directory_is_member"}
    )
    element = main_div.find("p", {"class": "ill_directory_item_contact_info"})

    if element.find("span", {"class": "ill_directory_fax"}):
        return element.find("span", {"class": "ill_directory_fax"}).contents[0]

    return ""


def getWebUrl(soup):
    main_div = soup.find(
        "div", {"id": "main", "class": "full_width ill_directory_is_member"}
    )
    element = main_div.find("p", {"class": "ill_directory_item_contact_info"})

    if element.find("a", {"class": "ill_directory_web_url"}):
        return element.find("a", {"class": "ill_directory_web_url"}).contents[0]

    return ""


def getFacilityType(soup):
    main_div = soup.find("div", {"class": "ill_directory_category_facility-type"})

    if main_div.find("a"):
        return main_div.find("a").get_text()

    return ""


def getLicensedBeds(soup):
    main_div = soup.find("p", {"class": "licensedbeds"})

    if main_div:
        if main_div.find("b"):
            return (
                "".join(map(str, main_div.contents))
                .replace("<br/>", "")
                .replace("<b>", "")
                .replace("</b>", "")
                .replace("\n", "")
                .replace("Licensed Beds: ", "")
            )

    return ""


def printData(data_list):

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    
    df = pd.DataFrame(data_list)
    df.to_csv('veri.csv', sep='\t', index=False, header=True)
    

def main():
    url_list = getUrlList("https://www.whca.org/facility-finder/")
    if url_list.__len__ == 0:
        return

    data_list = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(getContent, url) for url in url_list]
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            data_list.append(data)
            printData(data_list)
    
    printData(data_list)


if __name__ == "__main__":
    main()
