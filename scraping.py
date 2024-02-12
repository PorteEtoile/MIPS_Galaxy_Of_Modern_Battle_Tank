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
    if (tag.lower() == tr_tag.text.lower()) or (tag.lower() in tr_tag.text.lower()) :
        if tr_tag.find_next_sibling('td').find('a'):
            listElement = tr_tag.find_next_sibling('td').find_all('a')
            res = []
            for elementLI in listElement:
                res.append(elementLI.text)
            return res
        if tr_tag.find_next_sibling('td').find('ul'):
            listElement = tr_tag.find_next_sibling('td').find_all('li')
            res = []
            for elementLI in listElement:
                res.append(elementLI.text)
            return res
        elif tr_tag.find_next_sibling('td'):
            res = tr_tag.find_next_sibling('td').text
        
    return res

def getTank(linkTank):
    response = requests.get(linkTank)
    if response.status_code == 200:
        print("Access to the Tank's page")
        soupList = BeautifulSoup(response.text, 'html.parser')
        pageStuff = soupList.find("table",class_="infobox vcard")
        tr_tags = pageStuff.find_all('th',class_="infobox-label")
        for tr_tag in tr_tags:
            typeTank = getTankInfo(tr_tag,"Type")
            originTank = getTankInfo(tr_tag,"origin")
            crew = getTankInfo(tr_tag,"Crew")
            length = getTankInfo(tr_tag,"length")
            width = getTankInfo(tr_tag,"Width")
            height = getTankInfo(tr_tag,"Height")
            produced = getTankInfo(tr_tag,"produced")
            service = getTankInfo(tr_tag,"service")
            designer = getTankInfo(tr_tag,"Designer")
            manufacturer = getTankInfo(tr_tag,"Manufacturer")
            engine = getTankInfo(tr_tag,"Engine")
            mass = getTankInfo(tr_tag,"Mass")
            wars = getTankInfo(tr_tag,"Wars")
            secondaryArmament = getTankInfo(tr_tag,"Secondary")
            mainArmament = getTankInfo(tr_tag,"Main")
            suspension = getTankInfo(tr_tag,"suspension")
            operationnalRange = getTankInfo(tr_tag,"range")
            speed = getTankInfo(tr_tag,"speed")
            armor = getTankInfo(tr_tag,"armor")
            power = getTankInfo(tr_tag,"power")
            #print(typeTank)
            #print(originTank)
            #print(crew)
            #print(length)
            #print(width)
            #print(height)
            #print(produced)
            #print(service)
            #print(designer)
            #print(manufacturer)
            #print(engine)
            #print(mass)
            #print(wars)
            #print(secondaryArmament)
            #print(mainArmament)
            #print(suspension)
            #print(operationnalRange)
            #print(speed)
            #print(armor)
            #print(power)


#listTank = getListTank()
#for tankPage in listTank:
    #getTank(tankPage)
getTank("https://en.wikipedia.org/wiki/T-90")

