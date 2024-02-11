# https://en.wikipedia.org/wiki/List_of_Russo-Ukrainian_War_military_equipment
# https://en.wikipedia.org/
# h4 = Tanks
# h2 =  Forces
import os
import requests
import scrapy
import re
from bs4 import BeautifulSoup

def getListTank():
    listTank = []
    genericLink = "https://en.wikipedia.org/"
    linkList = "https://en.wikipedia.org/wiki/List_of_Russo-Ukrainian_War_military_equipment"
    response = requests.get(linkList)
    if response.status_code == 200:
        print("Access to the Tank's list")
        soupList = BeautifulSoup(response.text, 'html.parser')
        pageStuff = soupList.find("div",class_="mw-content-ltr mw-parser-output")
        h4_tags = pageStuff.find_all('h4')
        for h4_tag in h4_tags:
            if h4_tag.text == "Tanks[edit]":
                next_ul = h4_tag.find_next_sibling('ul')
                if next_ul :
                    li_tags = next_ul.find_all('li')
                    for li_tag in li_tags:
                        linkTank = li_tag.find('a')
                        linkTank = genericLink+ str(linkTank['href'])
                        listTank.append(linkTank)
    return listTank

def getTankInfo(tr_tag,tag):
    res = ""
    if tag.lower() in tr_tag.text.lower():
        res = tr_tag.find_next_sibling('td').find('a').text
    return res

def getTankInfoTwoTag(tr_tag,tag,tag1):
    res = ""
    if tag.lower() in tr_tag.text.lower() or tag1.lower() in tr_tag.text.lower():
        res = tr_tag.find_next_sibling('td').find('a').text
    return res

def getTank(linkTank):
    response = requests.get(linkTank)
    if response.status_code == 200:
        typeTank = ""
        print("Access to the Tank's page")
        soupList = BeautifulSoup(response.text, 'html.parser')
        pageStuff = soupList.find("table",class_="infobox vcard")
        tr_tags = pageStuff.find_all('th',class_="infobox-label")
        for tr_tag in tr_tags:
            typeTank = getTankInfo(tr_tag,"Type")
            originTank = getTankInfoTwoTag(tr_tag,"place","origin")
            print(typeTank)
            print(originTank)


#listTank = getListTank()
#for tankPage in listTank:
    #getTank(tankPage)
getTank("https://en.wikipedia.org/wiki/T-90")

