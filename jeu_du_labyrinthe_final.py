"""Jeux du labyrinthe dans le cadre du MOOC "Apprendre à coder avec Python"
session printemps 2022
Date : 2022/04
Auteur : Moi (anonymisation pour évaluation)"""

import turtle
from CONFIGS import *

# # # Mes constantes et variables globales
# assignation des coorodnnées limites du labyrinthe sachant que : ZONE_PLAN_MINI(-240/-240) <-> ZONE_PLAN_MAXI(50/200)
x_zpmini, y_zpmini = ZONE_PLAN_MINI
x_zpmaxi, y_zpmaxi = ZONE_PLAN_MAXI
#création &co des curseurs dédiés
labyrinthe_turtle = turtle.Turtle() #curseur du labyrinthe
labyrinthe_turtle.hideturtle()
annonce_turtle = turtle.Turtle()
annonce_turtle.hideturtle()
inventaire_turtle = turtle.Turtle()
inventaire_turtle.hideturtle()
pion_turtle = turtle.Turtle("circle")
pion_turtle.color("red")
pion_turtle.shapesize(0.9, 0.9, 1)
#nbre cases de la matrice
ver_cases = None # verticalement
hor_cases = None # horizontalement
# taille des cases de la matrice
dim_case = None
#création des dictionnaires de la matrice
dico_cases = {} # de la matrice
dico_inventaire = {} # de l'inventaire
dico_portes = {} # des portes
#position du pion
position = None
#taille de la police
font_size = 10
#liste des objets collectés par pion
inventaire_liste=[]


### ### ### Création du labyrinthe - début
def lire_matrice(fichier):
    """Fonction permettant de créer et retourner une matrice à partir d'un fichier(fichier)"""
    with open (fichier, encoding='utf-8') as plan :
        # conversion du ficher texte en matrice
        labyrinthe_matrice=[[int(colonne) for colonne in ligne.split()] for ligne in plan]
    return (labyrinthe_matrice)

def calculer_pas(matrice) :
    """Fonction pour déterminer et retourner la longueur des côtés (taille d'une case et leur nombre)
       dans un espace pré-défini en fonction de la matrice(matrice) qu'elle reoit
       (/!\ les cases doivent être carrées)"""
    # détermination de la dimension du labyrinthe
    labyrinthe_nanboku = abs(y_zpmini)+abs(y_zpmaxi) #longueur sud-nord
    labyrinthe_tozai = abs(x_zpmini)+abs(x_zpmaxi) #longueur est-ouest
    # détermination du nombre de cases
    nanboku = len(matrice) #nombre de cases sud-nord
    for horizontal in matrice :
        tozai = len(horizontal) #nombre de cases est-ouest
    # determination de la longueur des cases
    case_cote_nanboku = labyrinthe_nanboku/nanboku
    case_cote_tozai = labyrinthe_tozai/tozai
    if case_cote_nanboku > case_cote_tozai :
        case_cote = case_cote_tozai
    else :
        case_cote = case_cote_nanboku
    return (nanboku, tozai, case_cote)
    
def coordonnees(case_ind, pas_coord) :
    """Fonction qui calcule et retourne les coordonnées turtle inférieures gauche de chaque case (case_ind)
       a partir des coordonnées turtle (position/clef) et la taille de la case (pas_case)"""
    i_case_nbre, j_case_nbre =list(case_ind)
    return [x_zpmini + (j_case_nbre*pas_coord), y_zpmini + ((ver_cases-1-i_case_nbre)*pas_coord)]

def tracer_carre(dimension_carre) :   
    """Fonction qui permet de tracer un carré de côté 'dimension'.
       Elle reçoit les dimensions de la case"""
    for i in range (4):
        labyrinthe_turtle.forward(dimension_carre)
        labyrinthe_turtle.left(90)
    return

def choix_couleurs (case_clr, i_clr) :
    """ Fonction qui détermine la couleur d'une case de coordonnées clé (i) dans le dictionnaire
        reçoit le contenu de la case(i_clr) dans le dictionnaire de la matrice du plan et sa clé (case_couleur)."""
    if case_clr[i_clr] == 0 :
        clr = COULEUR_COULOIR
    elif case_clr[i_clr] == 1 :
        clr = COULEUR_MUR
    elif case_clr[i_clr] ==2 :
        clr=COULEUR_OBJECTIF
    elif case_clr[i_clr] ==3 :
        clr=COULEUR_PORTE
    elif case_clr[i_clr] ==4 :
        clr= COULEUR_OBJET
    elif case_clr[i_clr] ==5 :
        clr= COULEUR_VUE
    return clr

def carre_setting (case, clef, pas) :
    """Fonction qui collecte les données et prépare les élèments nécessaires pour le tracé du carré :
       dictionnaire (case), coordonnées turtle type  (position/clef), taille de la case(pas))
       qu'elle lance par le biais de diverses fonctions."""
    coulr = choix_couleurs (case, clef) # launch fct de choix de couleur en croisant case et dictionnaire
    x, y = coordonnees (clef, pas) # launch fct de calcul de coord. case par case
    labyrinthe_turtle.hideturtle()
    labyrinthe_turtle.speed(0)
    labyrinthe_turtle.penup()
    labyrinthe_turtle.goto(x,y)
    labyrinthe_turtle.color(coulr)
    labyrinthe_turtle.pendown()
    labyrinthe_turtle.begin_fill()
    tracer_carre(pas)
    labyrinthe_turtle.end_fill()
    return

def tracer_case(case_tracer, pas_tracer) :
    """Fonction qui trace le plan en tant qu'agglomération de carrés
       reçoit le dictionnaire de la matrice du plan et les dimensions d'une case""" 
    for clef_tracer in case_tracer :
        carre_setting (case_tracer, clef_tracer, pas_tracer)     
 
def afficher_plan(matrice_afficher):
    """Fonction globale permettant de tracer le plan
       reçoit la matrice et crée son dictionnaire puis trace le plan"""
    global ver_cases
    global hor_cases
    global dim_case
    global dico_cases
    labyrinthe_turtle.screen.tracer(len(matrice_afficher[0])) # cadeau d'un évaluateur aucune idée de comment ça marche
    ver_cases, hor_cases, dim_case = calculer_pas(matrice_afficher) #launch fct de calcul du nbres de cases et de leur dimension
    dico_cases = {(v,h) : matrice_afficher[v][h] for h in range(hor_cases) for v in range(ver_cases)} #cree un dico d'indice des coord de plan haut-bas gauche-droite et de valeur couleur
    tracer_case(dico_cases, dim_case)
    return
### ### ### Création du labyrinthe - Fin

### ### ### Les annonces - début
# Panneau d'annonces : zonage POINT_AFFICHAGE_ANNONCES(-240/240) <-> (?/?)
def annonce() :
    """ fonction pour creer le panneau d'annonce"""
    annonce_turtle.penup()
    annonce_turtle.goto(POINT_AFFICHAGE_ANNONCES)
    annonce_turtle.write('Bonjour', font = ['arial', font_size, 'bold'])
    return
### ### ### Les annonces - Fin


### ### ### L'inventaire - début
# Création zone inventaire : zonage POINT_AFFICHAGE_INVENTAIRE (70/210) <-> (240/?)
def inventaire(fichier_inventaire) :
    """ fonction qui recoit le fichier des objets et lance la fonction de création du dictionnaire"""
    creer_dictionnaire_des_objets(fichier_inventaire)
    inventaire_turtle.penup()
    inventaire_turtle.goto(POINT_AFFICHAGE_INVENTAIRE)
    inventaire_turtle.write('Inventaire : ', font = ['arial', font_size, 'normal'])
    return

def creer_dictionnaire_des_objets(fichier_des_objets) :
    """Création du dictionnaire de l'inventaire en fonction d'un fichier
       recoit le fichier des objets"""
    with open (fichier_des_objets, encoding='utf-8') as liste_inventaire :
        global dico_inventaire
        for i_inventaire in liste_inventaire :
            element_inventaire=eval(i_inventaire)
            dico_inventaire[element_inventaire[0]]=element_inventaire[1]
    return dico_inventaire
        
def ramasser_objet (vertical_obj,horizontal_obj) :
    """ Fonction de gestion des objets trouvés en fonction de leur position (x,y)
        recoit la position de la case ou est l'objet"""
    objet = dico_inventaire[(vertical_obj,horizontal_obj)]
    # message d'annonce
    trouve = "Vous avez trouvé : "
    annonce_turtle.undo()
    annonce_turtle.write(trouve+objet, font = ['arial', font_size, 'normal'])
    # ajout à l'inventaire du pion
    global inventaire_liste
    inventaire_liste.append(objet)
    # ajout au listing du contenu de l'inventaire
    vertical_inventaire, horizontal_inventaire = POINT_AFFICHAGE_INVENTAIRE
    inventaire_turtle.goto (vertical_inventaire, horizontal_inventaire-((len(inventaire_liste)+1)*font_size*1.5))
    inventaire_turtle.write(objet, font = ['arial', font_size, 'normal'])
    return
### ### ### L'inventaire - Fin

### ### ### Les portes - début
def creer_dictionnaire_des_portes(fichier_des_portes) :
    """Création du dictionnaire des portes depuis un fichier
       recoit le fichier des portes"""
    with open (fichier_des_portes, encoding='utf-8') as liste_portes :
        global dico_portes
        for i_portes in liste_portes :
            element_portes=eval(i_portes)
            dico_portes[element_portes[0]]=element_portes[1]    
    return dico_portes

def poser_question (vertical_question,horizontal_question) :
    """Fonction pour interroger en vue d'obtenir l'ouverture de la porte de la case de coordonnées (x,y)
       recoit la position de la case ou est la porte"""
    i, j = dico_portes[(vertical_question,horizontal_question)]
    h = turtle.textinput("Question", i)
    turtle.listen() # réactivation de l'écoute du clavier
    if h == j :
        annonce_turtle.undo()
        annonce_turtle.write("La porte s'ouvre.", font = ['arial', font_size, 'normal'])
        return True
    else :
        annonce_turtle.undo()
        annonce_turtle.write("La porte n'est ni convaincue ni vaincue.", font = ['arial', font_size, 'normal'])
### ### ### Les portes - fin


### ### ### La sortie - début
def sortie() :
    """Fonction de validation de la sortie du labyrinthe"""
    liste_dico_inventaire = sorted(i for i in dico_inventaire.values())
    global inventaire_liste
    inventaire_liste = sorted(inventaire_liste)
    if inventaire_liste == liste_dico_inventaire :
        return True
    else :
        annonce_turtle.undo()
        annonce_turtle.write("Il va falloir rebrousser chemin. Il vous manque quelque chose.", font = ['arial', font_size, 'normal'])
        return False
### ### ### La sortie - fin


### ### ### Le pion - début
# Fonction de placement du pion
def positionnement(vertical_position, horizontal_position) :
    """positionne le pion au centre d'une case selon les coordonnées matricielles"""
    pion_turtle.penup()
    pion_turtle.goto (x_zpmini + (horizontal_position*dim_case)+dim_case/2, y_zpmini + ((ver_cases-1-vertical_position)*dim_case)+dim_case/2)
    global position
    position=(vertical_position,horizontal_position) # passe à la clé correspondant à la nouvelle position
    carre_setting (dico_cases, position, dim_case) # colorise la case ou le pion se trouve en visitée
    pion_turtle.dot(RATIO_PERSONNAGE, COULEUR_PERSONNAGE)
    # retour vers la fonction de gestion des déplacements avec le nouveau jeu de coordonnées de type clé
    return

# Fonction testant la nature de la case visée de coordonnées (x,y)
def test_case (vertical_test,horizontal_test) :
    """recoit la position de la case ou le pion veut aller et
       teste si le mouvement est possible"""
    if vertical_test in range (ver_cases) and horizontal_test in range (hor_cases) :
        if dico_cases[vertical_test,horizontal_test] == 0 or dico_cases[vertical_test,horizontal_test] == 5 : #action s'il s'agit d'une case couloir ou déjà visitée
            dico_cases[vertical_test,horizontal_test] = 5 # on change la valeur du dico_matrice en 5 
            return True
        elif dico_cases[vertical_test,horizontal_test] == 1 : #action s'il s'agit d'une case mur
            annonce_turtle.undo()
            annonce_turtle.write('Ouille, ça doit faire mal !', font = ['arial', font_size, 'normal'])
        elif dico_cases[vertical_test,horizontal_test] == 2 : #action s'il s'agit de la case sortie
            annonce_turtle.undo()
            annonce_turtle.write("On dirait bien la sortie. N'avez-vous rien oublié ? ", font = ['arial', font_size, 'normal'])
            if sortie() :
                pion_turtle.goto (x_zpmini + (horizontal_test*dim_case)+dim_case/2, y_zpmini + ((ver_cases-1-vertical_test)*dim_case)+dim_case/2)
                fin() # on fait qqc pour stopper le jeu
        elif dico_cases[vertical_test,horizontal_test] == 4 : #action s'il s'agit d'une case inventaire
            ramasser_objet (vertical_test,horizontal_test)
            dico_cases[vertical_test,horizontal_test] = 5 # on change la valeur du dico_matrice en 5
            return True
        elif dico_cases[vertical_test,horizontal_test] == 3 : #action s'il s'agit d'une case porte
            annonce_turtle.undo()
            annonce_turtle.write('Cette porte est fermée.', font = ['arial', font_size, 'normal'])
            if poser_question (vertical_test,horizontal_test) :
                dico_cases[vertical_test,horizontal_test] = 5 # on change la valeur du dico_matrice en 5 
                return True 
    else :
        annonce_turtle.undo()
        annonce_turtle.write('Hmm ?', font = ['arial', font_size, 'normal'])
 
#Fonctions de déplacement        
### à gauche
def deplacer_gauche() :
    """Fonction de déplacement : gauche"""
    turtle.onkeypress(None, "Left")   # Désactive la touche Left
    ver, hor = position #divise la clé de position en x et y pour tester les mouvements
    if test_case (ver, hor-1) : 
        positionnement(ver, hor-1)
    turtle.onkeypress(deplacer_gauche, "Left")   # Réassocie la touche Left à la fonction deplacer_gauche   
### à droite 
def deplacer_droite() :
    """Fonction de déplacement : droite"""
    turtle.onkeypress(None, "Right")   # Désactive la touche Right
    ver, hor = position #divise la clé de position en x et y pour tester les mouvements 
    if test_case (ver, hor+1) :
        positionnement(ver, hor+1)
    turtle.onkeypress(deplacer_droite, "Right")   # Réassocie la touche Right à la fonction deplacer_gauche
### en haut 
def deplacer_haut() :
    """Fonction de déplacement : haut"""
    turtle.onkeypress(None, "Up")   # Désactive la touche Up
    ver, hor = position #divise la clé de position en x et y pour tester les mouvements 
    if test_case (ver-1,hor):
        positionnement(ver-1, hor)
    turtle.onkeypress(deplacer_haut, "Up")   # Réassocie la touche Up à la fonction deplacer_gauche
### en bas
def deplacer_bas() :
    """Fonction de déplacement : bas"""
    turtle.onkeypress(None, "Down")   # Désactive la touche Down
    ver, hor = position #divise la clé de position en x et y pour tester les mouvements 
    if test_case (ver+1,hor):
        positionnement(ver+1, hor)
    turtle.onkeypress(deplacer_bas, "Down")   # Réassocie la touche Down à la fonction deplacer_gauche
        
 
def deplacer(position_deplacer) :
    """Fonction permettant de lancer le déplacement initial du pion vers la position initiale(position_deplacer)"""
    vertical_initial, horizontal_initial = position_deplacer
    positionnement(vertical_initial, horizontal_initial) 
### ### ### Le pion - fin
        

### ### ### Fin - début
def fin():
    """Fonction de clôture du jeu"""
    annonce_turtle.undo()
    annonce_turtle.write("Félicitations, brave paladin. \nLe château au sommet du Python des Neiges vous a livré ses secrets.", font = ['arial', font_size, 'normal'])
    e = turtle.textinput("Merlin", "Devrions laisser la neige le recouvrir ? (oui/non)")
    turtle.listen()
    if e == "oui" :
        turtle.clearscreen()
        return ('Fin')
    else :
        pass
### ### ### Fin - fin

    
### ### ### Code de lancement
labyrinthe_plan_matrice = lire_matrice(fichier_plan) # launch fct d'extraction de matrice d'un fichier
afficher_plan(labyrinthe_plan_matrice) # launch fct de dessin du plan selon la matrice
annonce ()
inventaire (fichier_objets)
creer_dictionnaire_des_portes(fichier_questions)
deplacer(POSITION_DEPART)
turtle.listen()    # Déclenche l’écoute du clavier
turtle.onkeypress(deplacer_gauche, "Left")   # Associe à la touche Left une fonction appelée deplacer_gauche
turtle.onkeypress(deplacer_droite, "Right") # Associe à la touche Left une fonction appelée deplacer_droite
turtle.onkeypress(deplacer_haut, "Up")  # Associe à la touche Left une fonction appelée deplacer_haut
turtle.onkeypress(deplacer_bas, "Down")  # Associe à la touche Left une fonction appelée deplacer_bas
    
turtle.mainloop()# Place le programme en position d’attente d’une action du joueur    
