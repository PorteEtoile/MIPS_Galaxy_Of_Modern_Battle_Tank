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

def getTankInfo(th_tag,tag):
    res = ""
    if (tag.lower() == th_tag) or (tag.lower() in th_tag) :
        if (th_tag.find_next_sibling('td')):
            res = th_tag.find_next_sibling('td').text
    #     if th_tag.find_next_sibling('td').find('a'):

    #         listElement = th_tag.find_next_sibling('td').find_all('a')
    #         res = []
    #         for elementLI in listElement:
    #             res.append(elementLI.text)
    #         return res
    #     if th_tag.find_next_sibling('td').find('ul'):
    #         listElement = th_tag.find_next_sibling('td').find_all('li')
    #         res = []
    #         for elementLI in listElement:
    #             res.append(elementLI.text)
    #         return res
    #     elif th_tag.find_next_sibling('td'):
    #         res = th_tag.find_next_sibling('td').text
        
    return res 

def getOperator(link:str, soupList):
    ## Il faudrait get le lien du td, pour être surs du bon id et que ce soit automatique !
    ## Faires opérateurs non-étatiques
    operators = soupList.find(id=link).parent.find_next_sibling('ul').find_all("li")
    listPaysOp = []
    for operatorsLi in operators:
        listPaysOp.append(operatorsLi.find("a").text)
    
    return listPaysOp

def getTank(linkTank):
    response = requests.get(linkTank)
    if response.status_code == 200:
        print("Access to the Tank's page")
        soupList = BeautifulSoup(response.text, 'html.parser')

        # pageStuff = permet d'obtenir <table> du menu latéral des tanks
        pageStuff = soupList.find("table",class_="infobox vcard")
        # th_tags comporte tous les tags th du tableau
        th_tags = pageStuff.find_all('th',class_="infobox-label")

        # # tr_tags comporte tous les tags <tr> du tableau
        # tr_tags = pageStuff.find_all("tr")
        # # il faut garder uniquement les tr où on a un couple <th>, <td>+
        # for tr_tag in tr_tags:
        #     if (tr_tag.find("td")):     ## peut-être inutile
        #             print(tr_tag.find("th", class_="infobox-label"))
        #         #print(getTankInfo(tr_tag.find("th").text.lower(),"Type"))
                
        #         #print(getTankInfo(tr_tag.find("th"),"Type"))



        for th_tag in th_tags:
            #print(th_tag)
            print(th_tag.text)
            #print(th_tag.find_next_sibling('td'))
            print(th_tag.find_next_sibling('td').text)
            print("========")
            
            #print("============")
#listTank = getListTank()
#for tankPage in listTank:
    #getTank(tankPage)
getTank("https://en.wikipedia.org/wiki/T-90")

