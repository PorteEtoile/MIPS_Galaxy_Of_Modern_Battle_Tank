# https://en.wikipedia.org/wiki/List_of_Russo-Ukrainian_War_military_equipment
# https://en.wikipedia.org/
# h4 = Tanks
# h2 =  Forces
import os
import requests
import scrapy
import re
from bs4 import BeautifulSoup

def getListLinkTank():
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

def getOperator(link:str, soupList):
    ## Il faudrait get le lien du td, pour être surs du bon id et que ce soit automatique !
    ## Faires opérateurs non-étatiques
    operators = soupList.find(id="Operators").parent.find_next_sibling('ul').find_all("li")
    listPaysOp = []
    for operatorsLi in operators:
        listPaysOp.append(operatorsLi.find("a").text)
    return listPaysOp

def traitementInfos(infos):
    res = str(infos).strip()
    if re.search(r'\[\d+\]', res):
        res = re.sub(r'\[\d+\]', '', res)
    if re.search(r'\xa0', res):
        res = re.sub(r'\xa0', ' ', res)
    res = res.strip()
    return res

def afficheInfosTank(tank):
    for info in tank:
        print(info," : ",tank[info])
        print("========")

def getTank(linkTank):
    response = requests.get(linkTank)
    if response.status_code == 200:
        print("Access to the Tank's page")
        soupList = BeautifulSoup(response.text, 'html.parser')
        # pageStuff = permet d'obtenir <table> du menu latéral des tanks
        pageStuff = soupList.find("table",class_="infobox vcard")
        # th_tags comporte tous les tags th du tableau
        th_tags = pageStuff.find_all('th',class_="infobox-label")
        infosTank = {}
        for th_tag in th_tags:
            infosTank[th_tag.text] = ""
            if "\n" in th_tag.find_next_sibling('td').text:
                listInfos = []
                infossep = th_tag.find_next_sibling('td').text.split("\n")
                for eltinfos in infossep:
                    listInfos.append(traitementInfos(eltinfos))
                infosTank[th_tag.text] = listInfos
            elif "," in th_tag.find_next_sibling('td').text:
                listInfos = []
                infossep = th_tag.find_next_sibling('td').text.split(",")
                for eltinfos in infossep:
                    listInfos.append(traitementInfos(eltinfos))
                infosTank[th_tag.text] = listInfos
            elif th_tag.find_next_sibling('td').findChildren('ul'):
                listInfos = []
                for eltUL in th_tag.find_next_sibling('td').findChildren('ul'):
                    for eltLI in eltUL.find_all('li'):
                        listInfos.append(traitementInfos(eltLI.text))
                infosTank[th_tag.text] = listInfos
            elif "<br/>" in th_tag.find_next_sibling('td').text:
                listInfos = []
                infossep = th_tag.find_next_sibling('td').text.split("<br/>")
                for eltinfos in infossep:
                    listInfos.append(traitementInfos(eltinfos))
                infosTank[th_tag.text] = listInfos
            elif "<br>" in th_tag.find_next_sibling('td').text:
                listInfos = []
                infossep = th_tag.find_next_sibling('td').text.split("<br>")
                for eltinfos in infossep:
                    listInfos.append(traitementInfos(eltinfos))
                infosTank[th_tag.text] = listInfos
            elif "See Operators" in th_tag.find_next_sibling('td').text or "See Operators" == th_tag.find_next_sibling('td').text:
                infosTank[th_tag.text] = getOperator(linkTank,soupList)
            else:
                infosTank[th_tag.text] = traitementInfos(th_tag.find_next_sibling('td').text)
        return infosTank

#listTank = []
#listLinkTank = getListLinkTank()
#for tankPage in listLinkTank:
    #listTank.append(getTank(tankPage))
#for tank in listTank:
    #afficheInfosTank(tank)
infosTank = getTank("https://en.wikipedia.org/wiki/T-90")
afficheInfosTank(infosTank)

