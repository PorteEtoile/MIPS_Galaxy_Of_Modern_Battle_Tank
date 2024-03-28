# MIPS_Galaxy_Of_Modern_Battle_Tank

Le but de ce projet est de créer une galaxie MISP contenant les informations de tous les chars ayant participé à la guerre en Ukraine (forces russes et ukrainiennes).

# Méthode de scrapping et fichiers
Nous avons rassemblés toutes nos fonctions de scraping dans un fichier écrit en Python nommé "scraping.py".
Le dossier "galaxies" contient le fichier JSON "galaxieTanks.json" modélisant notre galaxie MISP et le dossier "clusters" contient le fichier JSON "ClusterTanks.json" modélisant le cluster de données associé à cette galaxie.

## scraping.py
Dans notre fichier "scraping.py" nous avons tout d'abord : 
- Scraper la page https://en.wikipedia.org/wiki/List_of_Russo-Ukrainian_War_military_equipment contenant tous les équipements militaires utilisés dans la guerre russo-ukrainienne. Nous avons récupéré les liens wikipédias de tous les chars utilisés.
- Pour chaque lien wikipédia correspondant à un char, nous avons scrapés sa fiche d'information (la fiche d'information verticale à droite de chaque page wikipédia).
- Sur cette fiche d'information, nous avons scrapé toutes les informations en les réunissant dans un dictionnaire en python pour faire un couple de clé-valeurs.
	L'ensemble des dictionnaires sera stocké dans une liste python ce qui en résulte que chaque élément de cette liste est un dictionnaire contenant les informations d'un tank.
  Cette phase de scraping nous a demandé d'être assez généraliste et de prévoir l'ensemble des cas possibles de format de données, car d'une page wikipédia à une autre, les données ne sont pas présentées de la même façon au sein de la fiche.
  Réalisation d'un petit nettoyage de la présentation des données lorsqu'il y a des caractères qui ont été mal parsé.
- Dans le cas des opérateurs (les pays et organisations utilisant le tank) nous avons du distinguer deux cas :
	- Le premier cas c'est lorsque la liste des opérateurs se trouvent au sein de la même page wikipédia que la fiche d'information du tank. Nous avons récupéré l'id html de la liste puis parser la liste.
  - Le second cas c'est lorsque la liste se trouve sur une page wikipédia différente, nous avons du parser cette nouvelle page pour récupérer la liste
- Une fois les informations récupérées, nous avons sérialisé notre liste Python au format JSON que nous avons stocké dans un fichier. Nous avons fait cela pour une meilleure utilisation dans les clusters MISP.
- Nous avons ensuite créé une galaxie au format JSON.
- Enfin nous avons créé un cluster au format JSON, et nous avons remplis ce cluster grâce à notre fichier JSON de données de tanks.

## galaxieTanks.json
- Modélisation de la galaxie au format JSON
- Définition de :
	- Description de la galaxie
	- Les auteurs de la galaxie (ZANNIER Chloé et ZIMMERMANN Julien)
	- Le nom ainsi que le namespace de la galaxie
	- Son identifiant unique généré grâce au module "uuid" de python
	- Son numéro de version
  
## ClusterTanks.json
- Modélisation du cluster lié à la galaxie au format JSON.
- Définition de : 
	- Les auteurs du cluster (ZANNIER Chloé et ZIMMERMANN Julien)
  - Catégorie du cluster
  - Nom du cluster
  - Source du cluster
  - Type du cluster
	- L'identifiant unique du cluster généré grâce au module "uuid" de python
	- La liste des données des tanks

# Références
Pour scrapper et réaliser notre script, nous avons utilisé les modules python suivants :
- "BeautifulSoup" qui nous a permis de récupérer les informations isssues de la page Wikipédia suivante : https://en.wikipedia.org/wiki/List_of_Russo-Ukrainian_War_military_equipment
	Cette page wikipédia référence chaque équipement, arme, véhicule utilisé par les forces armées russes ou ukrénienne. Nous nous sommes concentrés sur la catégorie des véhicules "chars".
- "uuid" qui nous a permis de générer des identifiants aléatoires pour la galaxie, les clusters et les données du cluster.
- "json" pour la manipulation des fichiers JSON
- "re" pour la gestion des regex (utilisé pour réaliser des cleans dans les données récupérées par le scraping)
- "requests" pour réaliser des requêtes HTTP sur les pages wikipédia
- "os" pour la gestion des dossiers et des fichiers

# Axe d'améliorations et réalisations restantes
 - Séparation dans deux camps bien distincts les tanks utilisés par l'armée ukrainienne et ceux utilisés par l'armée russe.
 	Actuellement, nous récupérons tous les tanks utilisés pendant la guerre et nous listons seulement les opérateurs au niveau mondial.
- Correctement clean le parsage des données : Dû à la différence du format de données selon les pages wikipédia, nous avons pas prévu tous les cas possible.
- Récupérer lors du parsage, les différents types de variants de chaque type : ATTENTION, le parsage aura les même problèmes rencontrés lors du passage des opérateurs
- Intégration à MISP pour une réelle utilisation
 
 

Il existe d'autres sites qui référencent les chars par pays, comme [military factory](https://www.militaryfactory.com/).
