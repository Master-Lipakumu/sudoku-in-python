#-*- coding: utf-8 -*-
from tkinter import *
from copy import deepcopy
from random import randrange
import os

def imprime_chiffre(chiffre):
    """"Inprime un chiffre sélectionné dans le menu popup dans la matrice de jeu."""
    
    # en mode jeu : la matrice de jeu est une copie de la grille choisie dans la liste (= matrice mère)
    # on ne peut pas imprimer un chiffre dans la matrice de jeu si son emplacement dans la matrice mère est différent de zéro
    if not modeEdition:
        if choixMatrice[(coordSouris_Y - margeHaut) // hauteurSprite][(coordSouris_X - margeGauche) // largeurSprite] == 0:
            matriceJeu[(coordSouris_Y - margeHaut) // hauteurSprite][(coordSouris_X - margeGauche) // largeurSprite] = chiffre
            # après chaque ajout de chiffre, on vérifie si le sodoku est achevé
            if not verif_sudoku():
                # dans la négative on verifie si le chiffre est déjà présent en ligne, colonne ou en ensemble3x3                
                verif_chiffre_deja_present()        
                affichage()            

    # en mode édition : par principe on peut écrire partout
    else:
        matriceJeu[(coordSouris_Y - margeHaut) // hauteurSprite][(coordSouris_X - margeGauche) // largeurSprite] = chiffre
        # on peut tout de même faire un petit test de présence de chiffres redondants pour éviter les erreurs d'édition
        verif_chiffre_deja_present()        
        affichage()
          
        
def affichage():
    """M�thode de r�affichage de la matrice de jeu."""
    global tabChiffresDejaPresents 

    # on efface tout � chaque fois
    can.delete(ALL)

    # chaque emplacement de la matrice est converti en coordonn�es
    for indiceLigne in range(0,len(matriceJeu)):
        for indiceColonne in range(0,len(matriceJeu[0])):
            coordX = margeGauche+(indiceColonne*largeurSprite)
            coordY = margeHaut+(indiceLigne*hauteurSprite)

            # en fonction de la valeur de l'emplacement courant une image est choisie
            if matriceJeu[indiceLigne][indiceColonne] == 1:
                can.create_image(coordX,coordY,image=imageChiffreUn,anchor=NW)
            elif matriceJeu[indiceLigne][indiceColonne] == 2:
                can.create_image(coordX,coordY,image=imageChiffreDeux,anchor=NW)
            elif matriceJeu[indiceLigne][indiceColonne] == 3:
                can.create_image(coordX,coordY,image=imageChiffreTrois,anchor=NW)
            elif matriceJeu[indiceLigne][indiceColonne] == 4:
                can.create_image(coordX,coordY,image=imageChiffreQuatre,anchor=NW)
            elif matriceJeu[indiceLigne][indiceColonne] == 5:
                can.create_image(coordX,coordY,image=imageChiffreCinq,anchor=NW)
            elif matriceJeu[indiceLigne][indiceColonne] == 6:
                can.create_image(coordX,coordY,image=imageChiffreSix,anchor=NW)
            elif matriceJeu[indiceLigne][indiceColonne] == 7:
                can.create_image(coordX,coordY,image=imageChiffreSept,anchor=NW)
            elif matriceJeu[indiceLigne][indiceColonne] == 8:
                can.create_image(coordX,coordY,image=imageChiffreHuit,anchor=NW)
            elif matriceJeu[indiceLigne][indiceColonne] == 9:
                can.create_image(coordX,coordY,image=imageChiffreNeuf,anchor=NW)

            couleur = ''
            if not modeEdition:
                # le coloriage de la case ne doit pas affecter les cases de la matrice m�re               
                if choixMatrice[indiceLigne][indiceColonne] == 0 and matriceJeu[indiceLigne][indiceColonne] != 0:
                    # si l'emplacement courant contient un chiffre d�termin� comme d�ja pr�sent, on colorie la case en rouge
                    if [indiceLigne,indiceColonne] in tabChiffresDejaPresents:
                        couleur = 'red'
                    # sinon si le sudoku n'est pas achev� et qu'on est pas en mode �dition, on colorie la case en orange
                    elif not sudokuComplet :
                        couleur = 'orange'
                    # si le sudoku est achev�, on colorie la case en vert
                    elif sudokuComplet:
                        couleur = 'light green'
            else:
                if [indiceLigne,indiceColonne] in tabChiffresDejaPresents:
                    couleur = 'red'                    

            rectangle = can.create_rectangle(coordX,coordY,coordX+largeurSprite,coordY+hauteurSprite,fill=couleur)
            can.lower(rectangle)
                
    #tabChiffresDejaPresents = []
    grille_jeu()

def grille_jeu():
    """M�thode affichant la grille de jeu."""
    
    for coordY_ligne in range(margeHaut,(9*hauteurSprite)+margeHaut+1,40):
        if (coordY_ligne-margeHaut)%120 == 0:
            epaisseur = 5
        else:
            epaisseur = 1
        
        can.create_line(margeGauche,coordY_ligne,(largeurSprite*9)+margeGauche,coordY_ligne,width=epaisseur)

    for coordX_colonne in range(margeGauche,(9*largeurSprite)+margeGauche+1,40):
        if (coordX_colonne-margeGauche)%120 == 0:
            epaisseur = 5
        else:
            epaisseur = 1
        
        can.create_line(coordX_colonne,margeHaut,coordX_colonne,(hauteurSprite*9)+margeHaut,width=epaisseur)

def verif_chiffre_deja_present():
    """M�thode d�terminant si des chiffres sont pr�sents plus d'une fois en ligne, colonne, ou ensemble3x3."""
    global tabChiffresDejaPresents

    # liste contenant toutes les coordonn�es matricielles des chiffres d�ja pr�sents en ligne, colonne, ou ensemble3x3
    tabChiffresDejaPresents = []
    # liste d'�num�ration
    listeChiffres = [1,2,3,4,5,6,7,8,9]

    #--- Recherche en ligne
    for indiceLigne in range(len(matriceJeu)):
        for chiffre in listeChiffres:
            # si pour un indice ligne donn�, un chiffre est pr�sent plus d'une fois
            if matriceJeu[indiceLigne].count(chiffre) > 1:
                # on boucle depuis le debut de la colonne
                for indiceColonne in range(len(matriceJeu[indiceLigne])):
                    # et pour chaque colonne contenant ce chiffre
                    if matriceJeu[indiceLigne][indiceColonne] == chiffre:
                        # on remplie 'tabChiffresDejaPresents' du couple form� de l'indice ligne et colonne courant ( = coordonn�es matricielles du chiffre)
                        tabChiffresDejaPresents.append([indiceLigne,indiceColonne])
    
    #--- Recherche en colonne
    for indiceColonne in range(len(matriceJeu[0])):
        # liste contenant tous les chiffres d'une colonne donn�e    
        colonne = []
        for indiceLigne in range(len(matriceJeu)):
            colonne.append(matriceJeu[indiceLigne][indiceColonne])
        for chiffre in listeChiffres:
            # si pour un indice colonne donn�, un chiffre est pr�sent plus d'une fois
            if colonne.count(chiffre) > 1:
                # on boucle depuis le debut en ligne
                for indiceLigne in range(len(colonne)):
                    # et pour chaque ligne contenant ce chiffre
                    if colonne[indiceLigne] == chiffre:
                        # on remplie 'tabChiffresDejaPresents' du couple form� de l'indice ligne et colonne courant ( = coordonn�es matricielles du chiffre)                        
                        tabChiffresDejaPresents.append([indiceLigne,indiceColonne])

    #--- Recherche en ensemble3x3
    # arbitrairement on se d�placera de 3 lignes en 3 lignes pour un ensemble de 3 colonnes donn�
    for decalColonne in range(0,9,3):
        for decalLigne in range(0,9,3):
            # liste contenant tous les chiffres d'un ensemble3x3 donn�
            ensemble3x3 = []
            for indiceLigne in range(decalLigne,3+decalLigne):
                for indiceColonne in range(decalColonne,3+decalColonne):
                    ensemble3x3.append(matriceJeu[indiceLigne][indiceColonne])
            for chiffre in listeChiffres:
                # si pour un ensemble3x3 donn�, un chiffre est pr�sent plus d'une fois
                if ensemble3x3.count(chiffre) > 1:
                    # on boucle en ligne et en colonne dans cet ensemble3x3
                    for indiceLigne in range(3):
                        for indiceColonne in range(3):
                            # on remplie 'tabChiffresDejaPresents' du couple form� de l'indice ligne et colonne courant ( = coordonn�es matricielles du chiffre)
                            # auxquels on ajoute les d�calages de matrice en cours
                            if matriceJeu[indiceLigne+decalLigne][indiceColonne+decalColonne] == chiffre:
                                tabChiffresDejaPresents.append([indiceLigne+decalLigne,indiceColonne+decalColonne])

    
def verif_sudoku():
    """Fonction d�terminant si le sudoku est achev�."""
    global sudokuComplet

    sudokuComplet = False

    # Conditions d'ach�vement du sudoku :
    #           - la somme des lignes est �gale � 45
    #           - la somme des colonnes est �gale � 45
    #           - la somme des ensemble3x3 est �gale � 45
    
    # somme des lignes
    for ligne in matriceJeu:
        if sum(ligne) != 45:
            return False

    # somme des colonnes
    somme = 0
    for indiceColonne in range(len(matriceJeu[0])):
        for indiceLigne in range(len(matriceJeu)):
            somme += matriceJeu[indiceLigne][indiceColonne]
        if somme != 45:
            return False
        else:
            somme = 0

    # somme des ensemble3x3
    somme = 0
    for decalColonne in range(0,9,3):
        for decalLigne in range(0,9,3):
            somme = 0
            for indiceLigne in range(decalLigne,3+decalLigne):        
                for indiceColonne in range(decalColonne,3+decalColonne):
                    somme += matriceJeu[indiceLigne][indiceColonne]
            if somme != 45:
                return False

    # si les 3 conditions sont r�unies la m�thode n'a jamais retourn� 'False'
    sudokuComplet = True
    affichage()

#------------   Fonctions du menu Popup -------------
def menu_contextuel(event):
    """M�thode faisant appara�tre le menu popup sous la souris."""
    global coordSouris_X,coordSouris_Y

    if event.x > margeGauche and event.x < margeGauche+(largeurSprite*9) and event.y > margeHaut and event.y < margeHaut+(hauteurSprite*9):
        coordSouris_X = event.x
        coordSouris_Y = event.y
    
        menuPopup.post(event.x_root,event.y_root)

def chiffre_un():
    """M�thode correspondant � l'option du menu popup permettant l'�criture du chiffre '1' dans la matrice de jeu."""
    
    imprime_chiffre(1)

def chiffre_deux():
    """M�thode correspondant � l'option du menu popup permettant l'�criture du chiffre '2' dans la matrice de jeu."""
    
    imprime_chiffre(2)

def chiffre_trois():
    """M�thode correspondant � l'option du menu popup permettant l'�criture du chiffre '3' dans la matrice de jeu."""
    
    imprime_chiffre(3)

def chiffre_quatre():
    """M�thode correspondant � l'option du menu popup permettant l'�criture du chiffre '4' dans la matrice de jeu."""
    
    imprime_chiffre(4)

def chiffre_cinq():
    """M�thode correspondant � l'option du menu popup permettant l'�criture du chiffre '5' dans la matrice de jeu."""
    
    imprime_chiffre(5)

def chiffre_six():
    """M�thode correspondant � l'option du menu popup permettant l'�criture du chiffre '6' dans la matrice de jeu."""
    
    imprime_chiffre(6)

def chiffre_sept():
    """M�thode correspondant � l'option du menu popup permettant l'�criture du chiffre '7' dans la matrice de jeu."""
    
    imprime_chiffre(7)

def chiffre_huit():
    """M�thode correspondant � l'option du menu popup permettant l'�criture du chiffre '8' dans la matrice de jeu."""
    
    imprime_chiffre(8)

def chiffre_neuf():
    """M�thode correspondant � l'option du menu popup permettant l'�criture du chiffre '9' dans la matrice de jeu."""
    
    imprime_chiffre(9)    
    
def effacer_chiffre():
    """M�thode correspondant � l'option du menu popup permettant l'�criture du chiffre '0' dans la matrice de jeu."""
    
    imprime_chiffre(0)

#-------------- Fonctions de l'option 'Nouvelle Partie' de la barre des Menu -----------------
def mode_facile():
    """Fonction chargeant les grilles faciles de jeu en mode Jouable."""
    global listeGrilles, choixMatrice, matriceJeu, modeEdition, numGrilleCourante
    
    menuBarre.entryconfig(2, state=ACTIVE)
    menuBarre.entryconfig(3, state=ACTIVE)
    menuEdition.entryconfig(1, state=DISABLED)

    modeEdition = False
    sudokuComplet = False

    try:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'grillesFaciles.txt')
        with open(file_path, 'r') as fichier:
            listeGrilles = eval(fichier.read())
    except FileNotFoundError:
        print("Le fichier grillesFaciles.txt est introuvable.")
        return

    hazard = randrange(0, len(listeGrilles))
    choixMatrice = listeGrilles[hazard]
    matriceJeu = deepcopy(choixMatrice)

    numeroGrille.set(str(hazard + 1))
    numGrilleCourante = numeroGrille.get()
    textNbrGrilles.configure(text=' / ' + str(len(listeGrilles)) + "   Grille facile")

    affichage()

    fenetre.bind('<Button-3>', menu_contextuel)
       

def mode_moyen():
    """Fonction chargeant les grilles moyennes de jeu en mode Jouable."""
    global listeGrilles, choixMatrice, matriceJeu, modeEdition, numGrilleCourante

    menuBarre.entryconfig(2, state=ACTIVE)
    menuBarre.entryconfig(3, state=ACTIVE)
    menuEdition.entryconfig(1, state=DISABLED)

    modeEdition = False
    sudokuComplet = False

    try:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'grillesMoyennes.txt')
        with open(file_path, 'r') as fichier:
            listeGrilles = eval(fichier.read())
    except FileNotFoundError:
        print("Le fichier grillesMoyennes.txt est introuvable.")
        return

    hazard = randrange(0, len(listeGrilles))
    choixMatrice = listeGrilles[hazard]
    matriceJeu = deepcopy(choixMatrice)

    numeroGrille.set(str(hazard + 1))
    numGrilleCourante = numeroGrille.get()
    textNbrGrilles.configure(text=' / ' + str(len(listeGrilles)) + "   Grille moyenne")

    affichage()

    fenetre.bind('<Button-3>', menu_contextuel)       


def mode_difficile():
    """Fonction chargeant les grilles difficiles de jeu en mode Jouable."""
    global listeGrilles, choixMatrice, matriceJeu, modeEdition, numGrilleCourante

    menuBarre.entryconfig(2, state=ACTIVE)
    menuBarre.entryconfig(3, state=ACTIVE)
    menuEdition.entryconfig(1, state=DISABLED)

    modeEdition = False
    sudokuComplet = False

    try:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'grillesDifficiles.txt')
        with open(file_path, 'r') as fichier:
            listeGrilles = eval(fichier.read())
    except FileNotFoundError:
        print("Le fichier grillesDifficiles.txt est introuvable.")
        return

    hazard = randrange(0, len(listeGrilles))
    choixMatrice = listeGrilles[hazard]
    matriceJeu = deepcopy(choixMatrice)

    numeroGrille.set(str(hazard + 1))
    numGrilleCourante = numeroGrille.get()
    textNbrGrilles.configure(text=' / ' + str(len(listeGrilles)) + "   Grille difficile")

    affichage()

    fenetre.bind('<Button-3>', menu_contextuel)

def mode_diabolique():
    """Fonction chargeant les grilles diaboliques de jeu en mode Jouable."""
    global listeGrilles, choixMatrice, matriceJeu, modeEdition, numGrilleCourante

    menuBarre.entryconfig(2, state=ACTIVE)
    menuBarre.entryconfig(3, state=ACTIVE)
    menuEdition.entryconfig(1, state=DISABLED)

    modeEdition = False
    sudokuComplet = False

    try:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'grillesDiaboliques.txt')
        with open(file_path, 'r') as fichier:
            listeGrilles = eval(fichier.read())
    except FileNotFoundError:
        print("Le fichier grillesDiaboliques.txt est introuvable.")
        return

    hazard = randrange(0, len(listeGrilles))
    choixMatrice = listeGrilles[hazard]
    matriceJeu = deepcopy(choixMatrice)

    numeroGrille.set(str(hazard + 1))
    numGrilleCourante = numeroGrille.get()
    textNbrGrilles.configure(text=' / ' + str(len(listeGrilles)) + "   Grille diabolique")

    affichage()

    fenetre.bind('<Button-3>', menu_contextuel)       

#-------------- Fonctions de l'option 'Edition' de la barre des Menu -----------------
def ajout_facile():
    """Fonction chargeant les grilles faciles de jeu en mode Edition."""
    global modeEdition,nomFichierEdition,listeGrilles,matriceJeu,choixMatrice,numGrilleCourante

    modeEdition = True

    menuEdition.entryconfig(1,state=ACTIVE)
    menuBarre.entryconfig(2,state=ACTIVE)
    menuBarre.entryconfig(3,state=ACTIVE)
    menuBarre.entryconfig(0,state=DISABLED)
    menuEdition.entryconfig(0,state=DISABLED)

    try:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'grillesFaciles.txt')
        with open(file_path, 'r') as fichier:
            listeGrilles = eval(fichier.read())
    except FileNotFoundError:
        print("Le fichier grillesFaciles.txt est introuvable.")
        return

    # une matrice vide est cr��e et ajout�e � la liste des grilles charg�e
    matriceJeu = []
    for i in range(9):
        matriceJeu.append([0,0,0,0,0,0,0,0,0])

    listeGrilles.append(matriceJeu)

    choixMatrice = deepcopy(matriceJeu)

    # mis � jour des widget entry et label
    indexGrille = len(listeGrilles)-1
    numeroGrille.set(str(len(listeGrilles)))
    numGrilleCourante = numeroGrille.get()
    textNbrGrilles.configure(text=' / '+ str(len(listeGrilles))+ "   Edition grilles faciles")

    verif_chiffre_deja_present()
    affichage()

    fenetre.bind('<Button-3>',menu_contextuel)    

def ajout_moyen():
    """Fonction chargeant les grilles moyennes de jeu en mode Edition."""
    global modeEdition,nomFichierEdition,listeGrilles,matriceJeu,choixMatrice,numGrilleCourante

    modeEdition = True

    menuEdition.entryconfig(1,state=ACTIVE)
    menuBarre.entryconfig(2,state=ACTIVE)
    menuBarre.entryconfig(3,state=ACTIVE)
    menuBarre.entryconfig(0,state=DISABLED)
    menuEdition.entryconfig(0,state=DISABLED)    

    try:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'grillesMoyennes.txt')
        with open(file_path, 'r') as fichier:
            listeGrilles = eval(fichier.read())
    except FileNotFoundError:
        print("Le fichier grillesMoyennes.txt est introuvable.")
        return

    matriceJeu = []
    for i in range(9):
        matriceJeu.append([0,0,0,0,0,0,0,0,0])

    listeGrilles.append(matriceJeu)
    
    choixMatrice = deepcopy(matriceJeu)

    indexGrille = len(listeGrilles)-1
    numeroGrille.set(str(len(listeGrilles)))
    numGrilleCourante = numeroGrille.get()
    textNbrGrilles.configure(text=' / '+ str(len(listeGrilles))+ "   Edition grilles moyennes")    

    verif_chiffre_deja_present()
    affichage()

    fenetre.bind('<Button-3>',menu_contextuel)    

def ajout_difficile():
    """Fonction chargeant les grilles difficiles de jeu en mode Edition."""
    global modeEdition,nomFichierEdition,listeGrilles,matriceJeu,choixMatrice,numGrilleCourante

    modeEdition = True

    menuEdition.entryconfig(1,state=ACTIVE)
    menuBarre.entryconfig(2,state=ACTIVE)
    menuBarre.entryconfig(3,state=ACTIVE)
    menuBarre.entryconfig(0,state=DISABLED)
    menuEdition.entryconfig(0,state=DISABLED)  


    try:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'grillesDifficiles.txt')
        with open(file_path, 'r') as fichier:
            listeGrilles = eval(fichier.read())
    except FileNotFoundError:
        print("Le fichier grillesDifficiles.txt est introuvable.")
        return  

    matriceJeu = []
    for i in range(9):
        matriceJeu.append([0,0,0,0,0,0,0,0,0])

    listeGrilles.append(matriceJeu)

    choixMatrice = deepcopy(matriceJeu)
    
    indexGrille = len(listeGrilles)-1    
    numeroGrille.set(str(len(listeGrilles)))
    numGrilleCourante = numeroGrille.get()
    textNbrGrilles.configure(text=' / '+ str(len(listeGrilles))+ "   Edition grilles difficiles")    

    verif_chiffre_deja_present()
    affichage()

    fenetre.bind('<Button-3>',menu_contextuel)    

def ajout_diabolique():
    """Fonction chargeant les grilles diaboliques de jeu en mode Edition."""
    global modeEdition,nomFichierEdition,listeGrilles,matriceJeu,choixMatrice,numGrilleCourante

    modeEdition = True

    menuEdition.entryconfig(1,state=ACTIVE)
    menuBarre.entryconfig(2,state=ACTIVE)
    menuBarre.entryconfig(3,state=ACTIVE)
    menuBarre.entryconfig(0,state=DISABLED)
    menuEdition.entryconfig(0,state=DISABLED)  


    try:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'grillesDiaboliques.txt')
        with open(file_path, 'r') as fichier:
            listeGrilles = eval(fichier.read())
    except FileNotFoundError:
        print("Le fichier grillesDiaboliques.txt est introuvable.")
        return    

    matriceJeu = []
    for i in range(9):
        matriceJeu.append([0,0,0,0,0,0,0,0,0])

    listeGrilles.append(matriceJeu)

    choixMatrice = deepcopy(matriceJeu)

    indexGrille = len(listeGrilles)-1
    numeroGrille.set(str(len(listeGrilles)))
    numGrilleCourante = numeroGrille.get()
    textNbrGrilles.configure(text=' / '+ str(len(listeGrilles))+ "   Edition grilles diaboliques ")    

    verif_chiffre_deja_present()
    affichage()

    fenetre.bind('<Button-3>',menu_contextuel)        

def sauver_sudoku():
    """Fonction sauvegardant la grille courante éditée."""
    global nomFichierEdition  # Déclare la variable globale

    menuBarre.entryconfig(0, state=ACTIVE)
    menuEdition.entryconfig(1, state=DISABLED)
    menuBarre.entryconfig(2, state=DISABLED)
    menuBarre.entryconfig(3, state=DISABLED)
    menuEdition.entryconfig(0, state=ACTIVE)

    # Si la grille éditée ne contient aucun chiffre, on la supprime de sa liste avant de sauvegarder cette dernière
    matriceVide = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
                   
    for grille in listeGrilles:
        if grille == matriceVide:
            listeGrilles.remove(grille)
            
    with open(nomFichierEdition, 'w') as fichier:
        fichier.write(str(listeGrilles))

    fenetre.unbind('<Button-3>')

def grille_precedente():
    """Permet de se d�placer en arri�re dans la liste de grilles choisie."""
    global matriceJeu,choixMatrice,numGrilleCourante

    numeroGrille.set(numGrilleCourante)

    indiceTableauCourant = int(numeroGrille.get())-1
    indiceTableauCourant -= 1

    if indiceTableauCourant < 0:
        indiceTableauCourant = len(listeGrilles)-1

    choixMatrice = listeGrilles[indiceTableauCourant]
    matriceJeu = deepcopy(choixMatrice)

    numeroGrille.set(str(indiceTableauCourant+1))
    numGrilleCourante = numeroGrille.get()

    affichage()
    
def grille_suivante():
    """Permet de se d�placer en avant dans la liste de grilles choisie."""
    global matriceJeu,choixMatrice,numGrilleCourante

    numeroGrille.set(numGrilleCourante)

    indiceTableauCourant = int(numeroGrille.get())-1
    indiceTableauCourant += 1

    if indiceTableauCourant > len(listeGrilles)-1:
        indiceTableauCourant = 0
    
    choixMatrice = listeGrilles[indiceTableauCourant]
    matriceJeu = deepcopy(choixMatrice)

    numeroGrille.set(str(indiceTableauCourant+1))
    numGrilleCourante = numeroGrille.get()

    affichage()

def recupere_tableau_choisi(event):
    """Permet de r�cup�rer le num�ro de tableau d�sir� par l'utilisateur."""
    global matriceJeu,choixMatrice,numGrilleCourante

    choixGrille = numeroGrille.get()
    if choixGrille.isdigit():
        if int(numeroGrille.get()) > 0 and int(numeroGrille.get()) <= len(listeGrilles) and numeroGrille.get()[0] != '0':
            choixMatrice = listeGrilles[int(numeroGrille.get())-1]
            matriceJeu = deepcopy(choixMatrice)
            numGrilleCourante = numeroGrille.get()
            affichage()            
        else:
            numeroGrille.set(numGrilleCourante)
            affichage()
    else:
        numeroGrille.set(numGrilleCourante)

def quitter():
    """Quitte l'application."""

    fenetre.quit()       
    fenetre.destroy()
try:
    modeEdition = True
    if modeEdition: nomFichierEdition = './grillesFaciles.txt'
    elif modeEdition: nomFichierEdition = './grillesMoyennes.txt'
    elif modeEdition: nomFichierEdition = './grillesDificiles.txt'
    elif modeEdition: nomFichierEdition = './grillesDiaboliques.txt'
    else: nomFichierEdition = './grillesFaciles.txt'
    with open(nomFichierEdition, 'r') as fichier:
        listeGrilles = eval(fichier.read())
        nomFichierEdition = './grillesFaciles.txt'
        nomFichierEdition = './grillesMoyennes.txt'
        nomFichierEdition = './grillesDificiles.txt'
        nomFichierEdition = './grillesDiaboliques.txt'
except FileNotFoundError:  print("Le fichier grille.txt est introuvable.")

#-------------------   Entrée principale du programme ------------------------
if __name__ == '__main__':
    #--- Fenêtre Principale ---
    fenetre = Tk()
    fenetre.configure(bg='light blue')
    fenetre.title("Mona Technology Sudoku")
    fenetre.iconbitmap('./favicon.ico')
    fenetre.resizable(0,0)
    fenetre.update_idletasks()  # Assurez-vous que les dimensions sont mises à jour
    hauteurEcran = fenetre.winfo_height()
    largeurEcran = fenetre.winfo_width()
    pos_x = int((fenetre.winfo_screenwidth() - largeurEcran) / 2 - 300)
    pos_y = int((fenetre.winfo_screenheight() - hauteurEcran) / 2 - 300)
    pos = f'+{pos_x}+{pos_y}'
    fenetre.geometry(pos)

    #--- Frame pour afficher le tableau courant et le nombre total ---
    frameInfo = Frame(fenetre,bg='light blue')
    frameInfo.pack()

    numeroGrille = StringVar()
    entreeGrille = Entry(frameInfo, textvariable=numeroGrille, width=2, font="Century 8 normal bold")
    entreeGrille.pack(side=LEFT)
    numeroGrille.set('')
    numGrilleCourante = numeroGrille.get()
    listeGrilles = []
    choixMatrice = []
    matriceJeu = []
    textNbrGrilles = Label(frameInfo, text=" / 0", bg='light blue', font="Century 14 normal bold")
    textNbrGrilles.pack(side=RIGHT)

    #--- Canevas Principal ---
    margeGauche, margeHaut = 20, 20
    can = Canvas(fenetre, bg='ivory', width=360 + margeGauche * 2, height=360 + margeHaut * 2)
    can.pack(side=BOTTOM)

    #--- Menu Principal ---
    menuBarre = Menu(fenetre, tearoff=0)
    menuNllePartie = Menu(menuBarre, tearoff=0)    
    menuEdition = Menu(menuBarre, tearoff=0)

    menuBarre.add_cascade(label='Nouvelle Partie', menu=menuNllePartie)
    menuNllePartie.add_radiobutton(label='Facile', command=mode_facile)
    menuNllePartie.add_radiobutton(label='Moyen', command=mode_moyen)
    menuNllePartie.add_radiobutton(label='Difficile', command=mode_difficile)
    menuNllePartie.add_radiobutton(label='Diabolique', command=mode_diabolique)
    menuNllePartie.add_separator()
    menuNllePartie.add_command(label='Quitter', command=quitter)

    menuBarre.add_cascade(label='Edition', menu=menuEdition)
    menuAjout = Menu(menuEdition)    
    menuEdition.add_cascade(label='Ajouter sudoku', menu=menuAjout)
    menuAjout.add_radiobutton(label='Facile ', command=ajout_facile)
    menuAjout.add_radiobutton(label='Moyen ', command=ajout_moyen)
    menuAjout.add_radiobutton(label='Difficile ', command=ajout_difficile)
    menuAjout.add_radiobutton(label='Diabolique ', command=ajout_diabolique)    

    menuEdition.add_command(label='Sauvegarder', command=sauver_sudoku, state=DISABLED)
    fenetre.config(menu=menuBarre)

    menuBarre.add_command(label='<-', command=grille_precedente, state=DISABLED)
    menuBarre.add_command(label='->', command=grille_suivante, state=DISABLED)

    #--- Menu Popup ---
    menuPopup = Menu(fenetre, tearoff=0)
    menuPopup.add_command(label='1', command=chiffre_un)
    menuPopup.add_command(label='2', command=chiffre_deux)
    menuPopup.add_command(label='3', command=chiffre_trois)
    menuPopup.add_command(label='4', command=chiffre_quatre)
    menuPopup.add_command(label='5', command=chiffre_cinq)
    menuPopup.add_command(label='6', command=chiffre_six)
    menuPopup.add_command(label='7', command=chiffre_sept)
    menuPopup.add_command(label='8', command=chiffre_huit)
    menuPopup.add_command(label='9', command=chiffre_neuf)
    menuPopup.add_separator()
    menuPopup.add_command(label='Effacer', command=effacer_chiffre)

    #--- chargement des images ---
    script_dir = os.path.dirname(__file__)  # Répertoire du script actuel
    imageChiffreUn = PhotoImage(file=os.path.join(script_dir, "chiffre1.gif"))
    imageChiffreDeux = PhotoImage(file=os.path.join(script_dir, "chiffre2.gif"))
    imageChiffreTrois = PhotoImage(file=os.path.join(script_dir, "chiffre3.gif"))
    imageChiffreQuatre = PhotoImage(file=os.path.join(script_dir, "chiffre4.gif"))
    imageChiffreCinq = PhotoImage(file=os.path.join(script_dir, "chiffre5.gif"))
    imageChiffreSix = PhotoImage(file=os.path.join(script_dir, "chiffre6.gif"))
    imageChiffreSept = PhotoImage(file=os.path.join(script_dir, "chiffre7.gif"))
    imageChiffreHuit = PhotoImage(file=os.path.join(script_dir, "chiffre8.gif"))
    imageChiffreNeuf = PhotoImage(file=os.path.join(script_dir, "chiffre9.gif"))
    largeurSprite = imageChiffreUn.width()
    hauteurSprite = imageChiffreUn.height()

    fenetre.bind('<Return>', recupere_tableau_choisi)
    grille_jeu()

    fenetre.mainloop()