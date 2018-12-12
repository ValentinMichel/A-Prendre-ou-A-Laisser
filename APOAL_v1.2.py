#!/usr/bin/python3
import random
import sys
import time
import os
import platform
#import pygame

def clean():
    '''
    Nettoyage de la console au coups par coups du joueur.
    Equivalant à CTRL+L et fonctionne sous Linux, macOS et Windows.
    '''
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("clear")

# Print iterations progress
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '\033[35m█\033[0m'):
    """
    Fonction qui une fois lancée crée une progressBar
    Liste des paramètes de la fonction :
    @params:
        iteration   - Required  : current iteration (Int) (Le nombre de fois déjà effectué)
        total       - Required  : total iterations (Int) (Nombre de fois que le programme tourne)
        prefix      - Optional  : prefix string (Str) (Ajoute un prefixn ex: Progression)
        suffix      - Optional  : suffix string (Str) (Ajoute un suffix, ex: Terminée)
        decimals    - Optional  : positive number of decimals in percent complete (Int) (Decimal des %)
        length      - Optional  : character length of bar (Int) (Longueur)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s \033[35m|\033[0m%s\033[35m|\033[0m %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def rules():
    print("\n\n\t\tRègles d'A Prendre ou A Laisser")
    print("\nLes règles sont les suivantes :")
    print("\t1. 16 candidats sont présents par Région")
    print("\t2. Une boîte est associée à chaque candidat en début de partie.")
    print("\t3. Une des régions est sélectionnée au Tirage au sort aléatoire indépendant.")
    print("\t4. Le candidat correspondant à cette région devra inscrire son nom, et pourra débuter la partie.")
    print("\t5. Le but du joueur sera alors d'ouvrir coups par coups les boîtes des autres candidats.")
    print("\t6. Chaque boîte ouverte révèle la somme d'argent caché, et l'élimine du gain possible.")
    print("\t7. Durant la partie, le banquier fera une intervention lorsqu'il restera un nombre précis de boîte à ouvrir.")
    print("\t\t7.1. Le banquier peut proposer un échange de boîte, si vous acceptez, vous choisissez la boîte de la région que vous voulez.")
    print("\t\t7.2. Le banquier peut proposer une somme d'argent, que vous pouvez accepter ou refuser.\n\t\t     Attention, la somme d'argent est là pour inspirer le doute.")
    print("\t8. La partie se termine lorsqu'il ne reste plus aucune boîte à ouvrir chez les Régions, vous allez découvrir la vôtre.")
    print("\t9. La partie se termine si vous acceptez la somme d'argent du banquier. Toutes les boîtes y compris la vôtre se dévoilent.")

def init():
    global player, region_Select, argent, candidats, candidat_Select, somme_Actuelle, initialisation, boxOpen, candidats_Exc, somme_OwnBox, money_Deal
    player = ''
    initialisation = True
    money_Deal = False
    somme_OwnBox = 0
    region_Select = ''
    boxOpen = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    argent = [0.01 , 5, 20, 100, 250, 500, 5000, 10000, 20000, 25000, 30000, 50000, 75000, 100000, 150000, 250000, 500000]
    random.shuffle(argent)
    #print(argent) #Check le mélange de la liste argent
    candidats = {'Auvergne-Rhône-Alpes' : argent[0],'Bourgogne-Franche-Comté' : argent[1],'Bretagne' : argent[2],'Centre-Val de Loire' : argent[3],'Corse' : argent[4],'Grand Est' : argent[5],'Hauts de France' : argent[6],'Île de France' : argent[7],'Normandie' : argent[8],'Nouvelle Aquitaine' : argent[9],'Occitanie' : argent[10],'Pays de la Loire' : argent[11],'Provence-Alpes-Côte d\'Azur' : argent[12],'Guyane' : argent[13],'Mayotte' : argent[14],'Guadeloupe' : argent[15]}
    candidats_Exc = {'Auvergne-Rhône-Alpes' : argent[0],'Bourgogne-Franche-Comté' : argent[1],'Bretagne' : argent[2],'Centre-Val de Loire' : argent[3],'Corse' : argent[4],'Grand Est' : argent[5],'Hauts de France' : argent[6],'Île de France' : argent[7],'Normandie' : argent[8],'Nouvelle Aquitaine' : argent[9],'Occitanie' : argent[10],'Pays de la Loire' : argent[11],'Provence-Alpes-Côte d\'Azur' : argent[12],'Guyane' : argent[13],'Mayotte' : argent[14],'Guadeloupe' : argent[15]}
    '''
    for nom, info in candidats.items():
        print(nom,info)
    #Check que chaque candidat de région dispose d'une boîte avec une valeur unique provenant de la liste argent
    '''
    candidat_Select = random.randint(0,15)
    compt = 0
    for region, somme in candidats.items():
        if compt == candidat_Select:
            region_Select = region
            somme_Actuelle = somme
            del candidats[region]
            del candidats_Exc[region]
            break
        compt += 1
    print('Le candidat sélectionné pour cette partie appartient à la région\033[36m',region_Select,'\033[0m')

def end():
    global initialisation, boxOpen
    if money_Deal:
        #-----------------------------------------------------------------------------------------------------------------
        # A List of Items
        items = list(range(0, 57))
        l = len(items)
        # Initial call to print 0% progress
        printProgressBar(0, l, prefix = 'Formulation de l\'offre:', suffix = 'Terminée', length = 50)
        for i, item in enumerate(items):
            # Do stuff...
            time.sleep(0.1)
            # Update Progress Bar
            printProgressBar(i + 1, l, prefix = 'Ouverture de toutes les boîtes:', suffix = 'Terminée', length = 50)
        #-----------------------------------------------------------------------------------------------------------------
        numR = 1
        for region,somme in candidats.items():
            print("\033[35m",end='')
            print(somme,"\033[0m  |   ","(",numR,")",region)
            numR += 1
        print("La somme de votre boîte est de :", end='')
        if somme_OwnBox > somme_Actuelle:
            print("\033[31m",somme_OwnBox,"€\033[0m")
        elif somme_OwnBox < somme_Actuelle:
            print("\033[32m",somme_OwnBox,"€\033[0m")
        print("Vous avez gagné",somme_Actuelle,"€")
        if somme_OwnBox > somme_Actuelle:
            print("\033[31mDommage !\033[0m")
        else:
            print("\033[31mBien joué, vous avez gagné plus d'argent que votre boîte actuel.")
    if len(boxOpen) == 15:
        print("Vous avez ouvert toutes les boîtes, vous avez gagné un total de ",somme_Actuelle,"€")
    initialisation = False

def name():
    global player,region_Select
    print("Candidat de la région\033[36m",region_Select,"\033[0m, veuillez inscrire votre nom :\033[36m",end=" ")
    player = input("")
    print(end="\033[0m")

def banquier():
    global somme_Actuelle, candidats, somme_OwnBox, money_Deal
    print("\n\n\033[36mIntervention du Banquier !\033[0m")
    offre_Banque = ['Argent','Echange','Echange','Argent','Echange','Argent','Argent','Echange']
    select_Offre = 0
    #-----------------------------------------------------------------------------------------------------------------
    # A List of Items
    items = list(range(0, 57))
    l = len(items)
    # Initial call to print 0% progress
    printProgressBar(0, l, prefix = 'Formulation de l\'offre:', suffix = 'Terminée', length = 50)
    for i, item in enumerate(items):
        # Do stuff...
        time.sleep(0.1)
        # Update Progress Bar
        printProgressBar(i + 1, l, prefix = 'Formulation de l\'offre:', suffix = 'Terminée', length = 50)
    #-----------------------------------------------------------------------------------------------------------------
    select_Offre = random.randint(0,7)
    print("\033[32m")
    print(offre_Banque[select_Offre],"\033[0m")
    if offre_Banque[select_Offre] == 'Argent':
        print("Le banquier vous offre une somme d'argent.")
        if somme_Actuelle >= 250000:
            pourcentage_Interet_Inferieur = 35/100
            pourcentage_Interet_Superieur = 5/100
        elif somme_Actuelle < 250000 and somme_Actuelle >= 50000:
            pourcentage_Interet_Inferieur = 30/100
            pourcentage_Interet_Superieur = 10/100
        elif somme_Actuelle < 50000 and somme_Actuelle > 10000:
            pourcentage_Interet_Inferieur = 25/100
            pourcentage_Interet_Superieur = 15/100
        else:
            pourcentage_Interet_Inferieur = 20/100
            pourcentage_Interet_Superieur = 25/100
        minimum = somme_Actuelle*(1-pourcentage_Interet_Inferieur)
        maximum = somme_Actuelle*(1+pourcentage_Interet_Superieur)
        minimum = int(minimum)
        maximum = int(maximum)
        somme_Banque = random.randint(minimum,maximum)
        print("L'offre du banquier s'élève à\033[32m",somme_Banque,"€\033[0m")
        choix = ''
        while choix != 'oui' and choix != 'non':
            print("\nVoulez-vous accepter l'offre du banquier ?\nChoix (oui ou non) : ",end='')
            choix = input("")
            if choix != 'oui' and choix != 'non':
                print("\033[33mVotre réponse doit être 'oui' ou 'non'.\033[0m")
        if choix == 'oui':
            somme_OwnBox = somme_Actuelle
            somme_Actuelle = somme_Banque
            #end()
            print("Vous avez accepté une somme d'argent du banquier de",somme_Actuelle,"€")
            money_Deal = True
        else:
            print("\033[36mVous avez refusé l'offre du banquier, vous pouvez jouer le prochain coups.\033[0m")
    elif offre_Banque[select_Offre] == 'Echange':
        print("Le banquier vous propose un échange.")
        choix = ''
        while choix != 'oui' and choix != 'non':
            print("\nVoulez-vous accepter l'offre du banquier ?\nChoix (oui ou non) : ",end='')
            choix = input("")
            if choix != 'oui' and choix != 'non':
                print("\033[33mVotre réponse doit être 'oui' ou 'non'.\033[0m")
        if choix == 'oui':
            count = 1
            for region in candidats_Exc.keys():
                print(count,"-",region)
                count += 1
            print("Vous devez choisir la boîte de la région avec qui vous souhaitez échanger votre boîte.")
            select_Region = -1
            while select_Region<1 or select_Region>len(candidats_Exc):
                select_Region = int(input("Entrer le numéro de la région avec qui échanger votre boîte : "))
                if select_Region<1 or select_Region>len(candidats_Exc):
                    print("\033[31mEntrer un identifiant valide du classement des régions ci-dessus.\033[0m")
            count = 1
            '''
            for region, somme in candidats_Exc.items():
                print(region, somme)
            print("-------------------------------------------------------------------------------------")
            #Check time : vérification avant échange des box et leur valeur
            '''
            for region, somme in candidats_Exc.items():
                if count == select_Region:
                    '''
                    Check time :
                    print("somme actu : ", somme_Actuelle)
                    print("somme de la région : ",somme)
                    '''
                    somme_Temp = somme_Actuelle
                    somme_Actuelle = somme
                    candidats[region] = somme_Temp
                    region_Exc = region
                    #Check time :
                    #print("somme actu après échange :",somme_Actuelle)
                count += 1
            print("Vous avez échangé votre boîte avec la région\033[36m",region_Exc,"\033[0m")
            '''
            #Affichage temporaire : vérification que la valeur de somme_Actuelle a été transféré
            for region, somme in candidats.items():
                print(region, somme)
            '''


def jouer():
    global player,region_Select,somme_Actuelle,candidats, boxOpen
    select_Box = -1
    '''
    Inclure une boucle qui interdit à l'utilisateur de donner le numéro d'une boîte déjà ouverte
    '''
    while (select_Box<0 or select_Box>14) or select_Box in boxOpen:
        select_Box = int(input("Sélectionner la boîte d'une des régions à ouvrir : "))
        if select_Box<0 or select_Box>14:
            print("\033[31mVeuillez insérer un numéro compris entre 0 et 14 inclus.\033[0m")
        if select_Box in boxOpen:
            print("\033[31mVous avez déjà ouvert cette boîte, ouvrez en une autre !\033[0m")
    boxOpen.append(select_Box)
    numB = 0
    for region, somme in candidats.items():
        if numB == select_Box:
            print("Vous avez ouvert la boîte de la région\033[36m",region,"\033[0mqui contenait le gain suivant :\033[34m",somme,"€\033[0m")
            del candidats_Exc[region]
            break
        numB += 1
    if len(boxOpen) == 15:
        end()
    banque_Intervention = len(boxOpen)
    if banque_Intervention == 3 or banque_Intervention == 6 or banque_Intervention == 7 or banque_Intervention == 9 or banque_Intervention == 11 or banque_Intervention == 12:
        banquier()



def display_Box():
    global candidats
    numR = 0
    for region, somme in candidats.items():
        if numR in boxOpen:
            print("\033[35m",end='')
            print(somme,"\033[0m  |   ","(",numR,")",region)
        else:
            print("XXXXXX   |  ","(",numR,")",region)
        numR += 1

def menu():
    global money_Deal, initialisation
    print("\n\n\n\tBienvenue sur le jeu \033[32mA Prendre ou A Laisser\033[0m")
    print("\t\t\tVersion Programme : \033[33m1.1.3\033[0m")
    print("\n\n")
    choix = ''
    while choix != 'Q':
        if initialisation:
            if money_Deal:
                end()
        print("\n\n")
        print("MENU DU JEU :")
        if not initialisation:
            print("1. Initialiser une partie")
            print("2. Règles du jeu")
            print("Q. Quitter")
        else:
            print("1. Jouer")
            print("2. Règles du jeu")
            print("Q. Quitter")
        print("\n\033[33mInsérer ci-dessous votre choix, en indiquant le chiffre ou la lettre prédéfinie.\033[0m")
        choix = input("Votre choix : \033[32m")
        print("\033[0m")
        clean()
        if not initialisation:
            if choix == '1':
                init()
                name()
            elif choix == '2':
                rules()
            elif choix == 'Q':
                print("Vous allez quitter le jeu.")
                print("Fermeture du processus ...")
                time.sleep(3)
                print("A bientôt !")
                sys.exit(0)
        else:
            if choix == '1':
                    display_Box()
                    jouer()
            elif choix == '2':
                rules()
            elif choix == 'Q':
                print("Vous allez quitter le jeu.")
                print("Fermeture du processus ...")
                time.sleep(3)
                print("A bientôt !")
                sys.exit(0)

global initialisation
initialisation = False
menu()
