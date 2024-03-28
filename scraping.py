# Script réalisé par ZANNIER Chloé et ZIMMERMANN Julien
# Réalisé pour l'option "Threat Intelligence" de la formation M2 SIS de l'UFR MIM de Metz
# Ce script consiste en la réalisation d'une galaxie MISP modélisant l'ensemble de tous les tanks ayant participé à la guerre en Ukraine
# Nous avons scrapé la page wikipédia https://en.wikipedia.org/wiki/List_of_Russo-Ukrainian_War_military_equipment pour récupérer la liste des tanks
# Puis nous avons scrapé chaque page wikipédia de chaque tanks pour récupérer les données de sa fiche d'information (l'encadré à droite au début de chaque page wikipédia)
import os
import requests
import re
import json
import uuid
from bs4 import BeautifulSoup

# Récupère la liste des pages HTTP wikipedia de tous les tanks ayant participé à la guerre en Ukraine
def getListLinkTank():
    listTank = []
    # Définition des liens http utiles à la récupération de la liste des tanks
    # linkList est la page wikipédia comportant la liste de tous les équipements militaire ayant servit durant le conflit
    # genericLink est le lien de la page d'accueil de wikipedia 
    genericLink = "https://en.wikipedia.org/"
    linkList = "https://en.wikipedia.org/wiki/List_of_Russo-Ukrainian_War_military_equipment"
    response = requests.get(linkList)
    # Si code 200 alors la requête http à la page des équipements militaire a réussie
    if response.status_code == 200:
        # Dans cette page, les titres des équipements militaires sont disposés par des balises HTML <h4>
        # Avec beautifulSoup on récupère la page de contenu HTML et on parse toutes les balises <h4>
        soupList = BeautifulSoup(response.text, 'html.parser')
        pageStuff = soupList.find("div",class_="mw-content-ltr mw-parser-output")
        h4_tags = pageStuff.find_all('h4')
        for h4_tag in h4_tags:
            # Balise <h4> correspondant aux Tanks
            if h4_tag.text == "Tanks[edit]":
                # Récupération de la liste de place de tous les tanks
                # On récupère le lien href menant à la page wikipédia de chaque Tank
                # Puis on concatène ce morceau de lien avec le lien générique wikipédia pour avoir le lien HTTP complet
                next_ul = h4_tag.find_next_sibling('ul')
                if next_ul :
                    li_tags = next_ul.find_all('li')
                    for li_tag in li_tags:
                        linkTank = li_tag.find('a')
                        linkTank = genericLink+ str(linkTank['href'])
                        listTank.append(linkTank)
    return listTank

# Récupération de la liste des opérateurs (pays / organisateurs qui sont utilisateurs) pour un tank
# 2 possibilités pour récupérer la liste : 
# - Soit la liste est présente dans la page wikipédia du tank (lien interne)
# - Soit la liste est accessible sur une page wikipédia différente de celle du tank (lien externe)
def getOperator(link:str, soupList,th_tag):
    ## Il faudrait get le lien du td, pour être surs du bon id et que ce soit automatique !
    ## Faire opérateurs non-étatiques

    # Réutilisation du lien générique pour concaténer le lien href menant à la liste des opérateurs avec le lien wikipédia
    genericLink = "https://en.wikipedia.org/"
    listPaysOp = []
    # Vérification que la balise <th> correspond bien à celle des opérateurs
    if "Used" in th_tag.text and "by" in th_tag.text:
        tdfilsOperateur = th_tag.find_next_sibling('td')
        # Vérification que la liste des opérateurs est dans un lien interne
        if re.search(r'^#',tdfilsOperateur.findChildren('a')[0]['href']):
            # On est dans le cas d'un lien interne
            # On va alors récupère l'élément HTML ayant l'ID du lien interne, puis parcourir la liste <ul>
            # Pour chaque élément <li> de la liste <ul>, on récupère le texte qui sera le nom de l'opérateur
            lienInterne = str(tdfilsOperateur.findChildren('a')[0]['href'].split("#")[1])
            operators = soupList.find(id=lienInterne).parent.find_next_sibling('ul').find_all("li")
            for operatorsLi in operators:
                listPaysOp.append(operatorsLi.find("a").text)
        else:
            # On est dans le cas d'un lien externe
            # On récupère le lien de la page wikipédia comportant la liste des opérateurs
            linkOperateur = genericLink+ str(tdfilsOperateur.findChildren('a')[0]['href'])
            responseLinkOperator = requests.get(linkOperateur)
            # Si code 200 alors la requête HTTP a réussie
            if responseLinkOperator.status_code == 200:
                # On parse la page HTML avec BeautifulSoup et on récupère les titres H2
                # Si un titre <h2> comporte le mot clé "operators" alors on a la liste des opérateurs
                # On parcourt ensuite chaque élement <li> de la liste <ul> et on récupère le texte qui sera le nom de l'opérateur
                soupOperator = BeautifulSoup(responseLinkOperator.text, 'html.parser')
                h2Operator_tags = soupOperator.find_all('h2')
                for h2Operator_tag in h2Operator_tags:
                    if "operators" in h2Operator_tag.text.lower():
                        listOperator = h2Operator_tag.find_next_sibling('ul').find_all("li")
                        for operator in listOperator:
                            if operator.findChildren('a')[0].text != "":
                                listPaysOp.append(operator.findChildren('a')[0].text)
    return listPaysOp

# Récupération de la liste des variants de chaque tank
# CETTE FONCTION N'EST PAS TERMINÉE , NOUS NE RÉCUPÉRONS AUCUN VARIANTS POUR L'INSTANT
# Il faut faire le même type de traitement qu'avec la fonction getOperator
# Nous avons repéré qu'il faut faire des distinctions entre les liens internes et les liens externes comme dans la fonction getOperator
def getVariants(link:str, soupList,th_tag):
    genericLink = "https://en.wikipedia.org/"
    listVariants = []
    if "Variants" in th_tag.text:
        tdfilsVariants = th_tag.find_next_sibling('td')
        if re.search(r'^#',tdfilsVariants.findChildren('a')[0]['href']):
            lienInterne = str(tdfilsVariants.findChildren('a')[0]['href'].split("#")[1])
    return listVariants


# Lors de la récupération de l'information d'un tank, on procède à un nettoyage du texte
# S'il y a la chaine \xa0  qui est l'équivalent en python du "&nbsp;" en HTML, on le remplace par un espace
def traitementInfos(infos):
    res = str(infos).strip()
    if re.search(r'\[\d+\]', res):
        res = re.sub(r'\[\d+\]', '', res)
    if re.search(r'\xa0', res):
        res = re.sub(r'\xa0', ' ', res)
    res = res.strip()
    return res


# Affiche sur la console les informations du tank
# Les informations du tank sont stockés dans un dictionnaire avec :
# Clé = Nom / Titre de l'information | Valeur = Valeur de l'information
def afficheInfosTank(tank):
    for info in tank:
        print(info," : ",tank[info])
        print("========")

# Affiche sur la console les informations de tous les tanks faisant partie de la liste
# Les informations du tank sont stockés dans un dictionnaire avec :
# Clé = Nom / Titre de l'information | Valeur = Valeur de l'information
def afficheInfosListTank(listTank):
    for tank in listTank:
        afficheInfosTank(tank)

# Récupère toutes les informations d'un tank selon sa page wikipédia
# Les informations récupérées proviennent de la carte d'information à droite de la page
def getTank(linkTank):
    genericLink = "https://en.wikipedia.org/"
    response = requests.get(linkTank)
    # Si code 200 alors la requête HTTP a réussie
    if response.status_code == 200:
        soupList = BeautifulSoup(response.text, 'html.parser')
        # pageStuff = permet d'obtenir <table> du menu latéral des tanks
        pageStuff = soupList.find("table",class_="infobox vcard")
        # th_tags comporte tous les tags th du tableau
        th_tags = pageStuff.find_all('th',class_="infobox-label")
        # Création d'un dictionnaire qui va comporter toutes les informations du tank selon le concept clé / valeur avec : 
        # Clé = Nom / Titre de l'information | Valeur = Valeur de l'information
        infosTank = {}
        infosTank["Name"] = pageStuff.find('th',class_="infobox-above hproduct").findChildren('span')[0].text.strip()
        # On parcourt toutes les balises <th> de la carte d'information du tank
        # Chaque balise <th> contient le titre d'une information
        # Chaque balise <th> possède une balise soeur <td> auquel on va récupérer le texte pour avoir la valeur de l'information
        # Il faut prévoir tous les cas possibles de formats de données
        for th_tag in th_tags:
            infosTank[th_tag.text] = ""
            # S'il y a des retours à la ligne dans le texte, on stocke dans une liste chaque lignes composant le texte
            if "\n" in th_tag.find_next_sibling('td').text:
                listInfos = []
                infossep = th_tag.find_next_sibling('td').text.split("\n")
                for eltinfos in infossep:
                    listInfos.append(traitementInfos(eltinfos))
                infosTank[th_tag.text] = listInfos
            # S'il y a des virgules dans le texte, on stocke dans une liste chaque morceaux du texte séparé par une virgule
            # Cela peut paraitre étrange au premier abord, mais nous avons rencontré dans certains cas que dans certaines fiches d'informations,
            #   certaines informations importantes à visualiser séparemment comme les différents armements étaient juste séparé par une virgule
            elif "," in th_tag.find_next_sibling('td').text:
                listInfos = []
                infossep = th_tag.find_next_sibling('td').text.split(",")
                for eltinfos in infossep:
                    listInfos.append(traitementInfos(eltinfos))
                infosTank[th_tag.text] = listInfos
            # S'il y a une liste non ordonnée dans le texte, nous parcourons le texte de chacun des élements de la liste
            elif th_tag.find_next_sibling('td').findChildren('ul'):
                listInfos = []
                for eltUL in th_tag.find_next_sibling('td').findChildren('ul'):
                    for eltLI in eltUL.find_all('li'):
                        listInfos.append(traitementInfos(eltLI.text))
                infosTank[th_tag.text] = listInfos
            # S'il y a des retours à la ligne dans le texte, on stocke dans une liste chaque lignes composant le texte
            elif "<br/>" in th_tag.find_next_sibling('td').text:
                listInfos = []
                infossep = th_tag.find_next_sibling('td').text.split("<br/>")
                for eltinfos in infossep:
                    listInfos.append(traitementInfos(eltinfos))
                infosTank[th_tag.text] = listInfos
            # S'il y a des retours à la ligne dans le texte, on stocke dans une liste chaque lignes composant le texte
            elif "<br>" in th_tag.find_next_sibling('td').text:
                listInfos = []
                infossep = th_tag.find_next_sibling('td').text.split("<br>")
                for eltinfos in infossep:
                    listInfos.append(traitementInfos(eltinfos))
                infosTank[th_tag.text] = listInfos
            # Cas spécifique pour récupérer la liste des opérateurs (utilisateurs) d'un tank
            elif "Used" in th_tag.text and "by" in th_tag.text:
                infosTank[th_tag.text] = getOperator(linkTank,soupList,th_tag)
            # Cas spécifique pour récupérer les variants d'un tank
            elif "Variants" in th_tag.text:
                infosTank[th_tag.text] = getVariants(linkTank,soupList,th_tag)
            # Le cas par défaut si nous ne rentrons pas dans les conditions précédentes
            else:
                infosTank[th_tag.text] = traitementInfos(th_tag.find_next_sibling('td').text)
        return infosTank


# Permet de créer un fichier JSON contenant l'ensemble des informations de chaque Tank
# Le fichier JSON contient une liste, et un objet JSON par Tank
# Ce fichier JSON sera stocké dans le dossier racine du projet
def CreerJSONTanks(listTank,nomFichier):
    jsonTanks = json.dumps(listTank, indent=4)
    with open(nomFichier, 'w') as fichier:
        fichier.write(jsonTanks)

# Permet de créer une galaxie MISP et de stocker cette galaxie dans un fichier JSON
# Cette galaxie sera stockée dans le dossier "galaxies"
def CreerGalaxie(nomFichier,description,icon,authors,name,namespace,type,uuid,version):
    json_galaxie = {
        "description" : description,
        "icon" : icon,
        "authors" : authors,
        "name" : name,
        "namespace" : namespace,
        "type" : type,
        "uuid" : uuid,
        "version" : version
    }
    chemin_galaxies = os.path.join(os.getcwd(), "galaxies")
    chemin_fichier_json = os.path.join(chemin_galaxies, nomFichier)
    with open(chemin_fichier_json, 'w') as fichier:
        json.dump(json_galaxie, fichier, indent=4)

# Permet de créer un cluster lié à une Galaxie pour remplir la galaxie de nos données de Tank
# Les données des Tanks seront lu à partir du fichier de la fonction CreerJSONTanks seront stocké dans la liste de la clé "values" puis dans l'objet ayant la clé "meta"
# Ce cluster sera stocké dans le dossier "clusters"
# Les données des tanks viennent du fichier JSON créé avec la fonction CreerJSONTanks
def CreerCluster(nomFichier,authors,category,name,source,typeCluster,uuidCluster,fichierData):
    chemin_clusters = os.path.join(os.getcwd(), "clusters")
    chemin_clusters_json = os.path.join(chemin_clusters, nomFichier)
    json_clusters = {
        "authors" : authors,
        "category" : category,
        "name" : name,
        "source" : source,
        "type" : typeCluster,
        "uuid" : uuidCluster
    }
    listMeta = []
    with open(fichierData, 'r') as fichier:
        listTanks = json.load(fichier)
        for tank in listTanks:
            uuidMeta = str(uuid.uuid4())
            meta = {
                "meta" : tank,
                "uuid" :uuidMeta,
                "value" : tank["Name"]
            }
            listMeta.append(meta)
    json_clusters["values"] = listMeta
    with open(chemin_clusters_json, 'w') as fichier:
        json.dump(json_clusters, fichier, indent=4)

# Définition d'une fonction main pour une exécution simple de notre script :
# On récupère dans une liste, la liste de tous les liens wikipédias de chaque tanks ayant participé à la guerre russo-ukrainienne
# On ajoute dans une seconde liste, tous les dictionnaires de données de chaque tanks
# On créé le fichier JSON contenant toutes les données des tanks
# On créé notre galaxie
# On créé notre cluster et on le remplis avec les données du fichier JSON des tanks
def main():
    listTank = []
    listLinkTank = getListLinkTank()
    for tankPage in listLinkTank:
        listTank.append(getTank(tankPage))
    CreerJSONTanks(listTank,"tanks.json")
    auteurs = ["ZANNIER Chloé","ZIMMERMANN Julien"]
    CreerGalaxie("galaxieTanks.json","Une galaxie de tank","Tank",auteurs,"Tanks","Tanks","tanksList",str(uuid.uuid4()),1)
    CreerCluster("ClusterTanks.json",auteurs,"Tanks","Tanks","https://en.wikipedia.org/wiki/List_of_Russo-Ukrainian_War_military_equipment"
                 ,"Tanks",str(uuid.uuid4()),"tanks.json")
    #afficheInfosListTank(listTank)  

if __name__ == "__main__":
    main()


