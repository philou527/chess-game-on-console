# !Disclaimer! : Pour un meilleur visuel du code et de ses commentaires, changer la disposition des fenêtres en mettant la console en bas plutôt qu'à droite. 
# Pour ce qui est du test, nous vous conseillons de l'ouvrir en fichier.py directement avec python :) c'est bien plus agréable qu'ici sur pyzo
# Le code de notre jeu d'échec est atypique (pas de tableau à double entrée avec coord(x,y) etc), l'échiquier est une liste de 64 éléments connecté à une liste de coordonnées fixée.



# importation module système
import os
import sys
os.system("mode con cols=80 lines=15") # ajustement de la fenêtre si vous l'ouvrez directement sur la console python
clear = lambda: os.system('cls') # petite fonction pour clear l'écran (cela ne marche pas ici puisqu'elle n'est sans doute pas dans la library de pyzo)



# interface caché
coordonnees = [] #création d'une liste pour contenir les coordonnées de l'échiquier
letter = ["a","b","c","d","e","f","g","h"] # liste pour les colonnes
blanc = ["T","C","F","D","R","F","C","T","P"] # liste pour les pièces
noir = ["t","c","f","d","r","f","c","t","p"]
ScoreB = []
ScoreN = []
ListeMort = []
tourBlanc = True # une bool pour savoir qui joue



# mise en place des coordonnées sur l'échiquier
for i in range(1,9)[::-1]: # pour un range inversé (8 à 1)
    for j in letter:       # pour chaque lettre, nous allons le combiner avec un chiffre
        coordonnees.append(j+"{}".format(i))   # pour avoir ensuite des coordonnées



# interface montré
interface = [] # creation d'une 2eme liste pour l'interface visible
interface += coordonnees # nous allons le "lier" avec la liste coordonnées en y ajoutant ses éléments



def PlacementDebut(interface):
    """
        Placement des pièces au tout début.
    """
    ordre = 0 # compteur pour le placement des pièces de liste character
    for i in interface: # nous allons ici remplacer les coordonnées de l'interface visible par les différentes pieces
        pos = interface.index(i)
        if pos < 8 or pos > 55: # placement des 2 lignes de fond (interface.index(i) représente sa position dans la liste)
            interface[pos] = blanc[ordre] # on y ajoute dans l'ordre les pièces
            ordre +=1
        if ordre > 7:   # si ordre dépasser 7, on le remet à 0 pour refaire le placement pour la 2eme ligne de fond
            ordre = 0
        for j in i:     # placement des pions soldats
            if j == "7" or j=="2": # on se place sur les lignes 2 et 7
                interface[pos] = "P"

    for i in interface[:16]: # creation des pieces de bases blanches en noires
        interface[interface.index(i)] = chr((ord(i))+32)

    for i in interface: # on rempli les cases vides
        if (i in blanc) is False and (i in noir) is False: # test pour savoir si une case est occupée ou non
            interface[interface.index(i)] = "*"

    return ""




def MiseEnForme(interface, coordonnees):
    """
        Fonction pour mettre en forme l'échiquier.
        On affiche l'interface (la liste) par 8 pour avoir la forme d'un échiquier!   
    """
    l = 0                              
    r = 8                               
    for k in range(8):   # petit système d'incrémentation très simple
        print(" "*10,"  ".join(interface[l:r]), " "*5, " ".join(coordonnees[l:r])) # mise en forme + "beau" avec espace,etc
        l+=8
        r+=8



def Tour(interface,pos,coordonnees):
    """
        Fonction des mouvements possible de la Tour
    """
    mouvPossibleTour = []
    verticalB = pos     # 2 variables pour monter et descendre, vertical bas et vertical haut
    verticalH = pos     # on prend la position de notre piece qu'on veut déplacer
    for i in range(7):  # possibilité de déplacement de base à 8 cases en bas et en haut
        verticalH+=8    # il y aura forcément un surplus sur les extrémités (par exemple la tour "t" à gauche aura des valeurs négatives)
        verticalB-=8    
        mouvPossibleTour.append(verticalH)
        mouvPossibleTour.append(verticalB)
    horiz = coordonnees[pos][1] # on prend les coordonnées en y en utilisant la 1ere liste créée
    for j in coordonnees:
        if horiz in j: # on cherche la ligne avec l'indice y de notre piece
            mouvPossibleTour.append(coordonnees.index(j))
    for i in mouvPossibleTour: # on enlève ce surplus là en supprimant tout les éléments qui ne sont pas compris entre 0 et 64
        if i < 0 or i > 63:
            mouvPossibleTour.remove(i)
    mouvPossibleTour.remove(pos)
    
    return mouvPossibleTour




def Fou(interface, pos, coordonnees):
    """
        Fonction mouvements possibles pour le Fou
    """
    l = coordonnees[pos][0] # on prendre les coordonnées de la piece en x
    mouvPossibleFou = [[],[],[],[]] # 4 listes pour les 4 différents mouvements (hautG, hautD, basG, basD)
    diagH = pos
    diagB = pos
    diagH2 = pos
    diagB2 = pos
    for i in range(8):
        if l == "a": # colonne a (ici les mouvements sont bien plus restreints)
            diagH-=7 # pour se déplacer à droite en haut
            diagB+=9 # déplacer en bas à droite
            mouvPossibleFou[0].append(diagH)
            mouvPossibleFou[1].append(diagB)
              
        
        elif l == "h": # colonne h
            diagH2-=9 # se déplacer en haut à gauche
            diagB2+=7 # se déplacer en bas à gauche
            mouvPossibleFou[2].append(diagH2)
            mouvPossibleFou[3].append(diagB2)
        else:
            # si bug, il faudra reprendre code et vérifier si dans chaque ligne il y a que 2 positions possibles
            diagH-=7 # pour monter droite
            mouvPossibleFou[0].append(diagH)
            diagH2-=9 # monter gauche
            mouvPossibleFou[2].append(diagH2)
            #diagH+=2
            diagB+=9 # descendre gauche
            mouvPossibleFou[1].append(diagB)
            diagB2+=7 # descendre droite
            mouvPossibleFou[3].append(diagB2)
            #diagB-=2
            
    for i in mouvPossibleFou: # on enlève ici les surplus
        if i != []: # on vérifie si la liste n'est pas vide (sinon bug)
            for j in i:
                if j < 0 or j > 63:
                    mouvPossibleFou[mouvPossibleFou.index(i)].remove(j)
                    
    return mouvPossibleFou
 
 
 
 
def Cavalier(interface, pos, posD, coordonnees):
    """
        Fonctions mouvements posibles du cavalier
    """
    mouvPossibleCav = []
    fullZone = [18,19,20,21,26,27,28,29,34,35,36,37,42,43,44,45] # les coordonnées de la full zone (8cases) là où les déplacements sont maximaux
    demiZone = [[10,11,12,13],[17,25,33,41],[22,30,38,46],[50,51,52,53]] # coordonnées demi zone (6cases) soit 6 mouvements
    mPCfullZone = [pos+6,pos-6,pos+10,pos-10,pos+15,pos-15,pos+17,pos-17] # les mouv possible en full zone
    mPCdemiZone = [[pos-6,pos-10,pos+6,pos+10,pos+15,pos+17],[pos+6,pos+10,pos-6,pos-10,pos-15,pos-17],[pos-6,pos-15,pos-17,pos+10,pos+15,pos+17],[pos-10,pos-15,pos-17,pos+6,pos+15,pos+17]]

    if pos in fullZone: # on regarde d'abord la position de notre pièce 
        mouvPossibleCav += mPCfullZone # pour ensuite add les mouv possibles selon sa position
    else:
        for i in demiZone:
            if pos in i:
                mouvPossibleCav += mPCdemiZone[demiZone.index(i)] # en fonction de sa position on ajoute la liste de la liste mPCdemiZone
        if pos not in demiZone:
            mouvPossibleCav += mPCfullZone 
           
    for i in mouvPossibleCav: # on enleve les surplus dans les coins 
        if i < 0 or i > 63:
            mouvPossibleCav.remove(i)
    return mouvPossibleCav




def Pion(piece, interface, pos, posD, coordonnees, ennemi):
    mouvPossiblePion = []
    """
        Fonctions mouvements posibles pour pions
    """
    # les 2 pions blanc et noirs auront des mouv contraires, soit monter soit descendre
    if piece == "P": 
        if pos in [48,49,50,51,52,53,54,55,56]: # seulement sur cette ligne, ils peuvent avancer de 2 ou de 1
            mouvPossiblePion.append(pos-16)
            mouvPossiblePion.append(pos-8)
        else:                                   # sinon ils auront un mouv de base verti de +1
            mouvPossiblePion.append(pos-8)
            
        # on vérifie s'il y a des ennemis aux alentours
        if interface[pos-8] != "*" and interface[posD+8] in noir: 
            print("impossible de se déplacer ici!")
            Deplacement(interface, coordonnees, tourBlanc)
        # il peut manger en diagonale +1
        if interface[pos-7] in ennemi: # à droite
            mouvPossiblePion.append(pos-7)
        if interface[pos-9] in ennemi:  # à gauche
            mouvPossiblePion.append(pos-9)


    elif piece == "p": # on attribue les même caractéristiques que P en inversé
        if pos in [8,9,10,11,12,13,14,15,16]:
            mouvPossiblePion.append(pos+16)
            mouvPossiblePion.append(pos+8)
        else:
            mouvPossiblePion.append(pos+8)

        if interface[pos+8] != "*" and interface[posD-8] in blanc:
            print("impossible de se déplacer ici!")

        if interface[pos+7] in ennemi: 
            mouvPossiblePion.append(pos+7)
        if interface[pos+9] in ennemi: 
            mouvPossiblePion.append(pos+9)
            
    return mouvPossiblePion
        


 
# Vérifications des mouvements possibles dans les mouvements qu'on leur a crée (requis seulement pour tour et fou, car plus de situations possibles)
def FouCheck(mouvPossibleFou, posD, pos, interface, coordonnees):
    """
        Check pour les déplacements du fou
    """
    if posD in mouvPossibleFou[0]: # diagH
        check = ((interface[posD+7] == "*") and (interface[pos-7] == "*")) or (posD+7 == pos)
    elif posD in mouvPossibleFou[2]: # diagB
        check = ((interface[posD+9] == "*") and (interface[pos-9] == "*")) or (posD+9 == pos)
    elif posD in mouvPossibleFou[1]: # diagH2
        check = ((interface[posD-9] == "*") and (interface[pos+9] == "*")) or (posD-9 == pos)
    else: # diagB2
        check = ((interface[posD-7] == "*") and (interface[pos+7] == "*")) or (posD-7 == pos)

    return check
    
    
    
    

def TourCheck(interface,pos,posD,coordonnees):
    """
        Check pour les déplacements de la tour
        Cette fonction va scanner les cases entre la position de la piece et de la position demandée,
        il regarde ici s'il y a des pieces entre les 2 ou non.
        Ma méthode peut vous sembler fastidieuse mais je n'ai trouvé mieux sans trop modifier tout mon code
    """
    counter = pos
    if posD > pos: # tour veut descendre | posD représente la position du déplacement et pos la position de la piece choisie
        check = True  # on initialise une boolean à vrai et donc si on sort du scan sans probleme il reste à true
        if posD-pos == 8:  # ici il n'y a pas de case vide entre pos et posD 
            increm = 1
        else:
            increm = int((posD-pos)/8)-1 # le nombre d'espace entre pos et posD va être le nombre de scan et va regarder s'il y a des pieces entre les 2
        for i in range(increm):
            counter+=8 # pour scanner en vertical
            if interface[counter] != "*": # si il rencontre un objet
                if posD-8 == pos: # si c'est lui même il peut se déplacer, check reste à true
                    check = True
                else:
                    check = False # sinon valeur de check devient false

    else: # si plus grand : veut monter
        check = True
        if pos-posD == 8:
            increm = 1
        else:
            increm = int((pos-posD)/8)-1
        for i in range(increm):
            counter-=8
            if interface[counter] != "*":
                if posD+8 == pos:
                    check = True
                else:
                    check = False

    return check






def Contraintes(interface, pos, posD, coordonnees, ListeMort, ennemi):
    """
        Fonction contraintes pour finaliser la demande et l'action du déplacement.
        On ajoute ici aussi les pièces "mangées" dans la liste de score de chaque joueur.
        C'est en quelque sorte ici une fonction frontière où celui qui voudra se déplacer doit avoir tous ses documents)
        pos = position piece à deplacer | posD = position du déplacement
    """
    piece = interface[pos] # on relève la pièce choisie

    # contraintes tour
    if piece in "Tt":
        mouvPossibleTour = Tour(interface,pos,coordonnees) # ajoute dans une liste les déplacements en fonction de sa position
        if posD in mouvPossibleTour: 
            checkTour = TourCheck(interface,pos,posD,coordonnees) # vérification des possibilités de déplacements

            if checkTour is True:                                                                                                                                       
                ListeMort.append(interface[posD]) # celui qui a été mangé part dans liste des morts
                interface[posD] = interface[pos] # on prend la piece et on la déplace en fonction des positions relevées
                interface[pos] = "*" # on remplace l'ancienne case
            else:
                Impossible(interface, coordonnees,tourBlanc)

        else:
            Impossible(interface, coordonnees,tourBlanc)



    # contraintes fou
    elif piece in "fF":

        mouvPossibleFou = Fou(interface, pos, coordonnees)

        if posD in mouvPossibleFou[0] or posD in mouvPossibleFou[1] or posD in mouvPossibleFou[2] or posD in mouvPossibleFou[3]: # verification
            Check = FouCheck(mouvPossibleFou, posD, pos, interface, coordonnees)
        else:
            Impossible(interface, coordonnees,tourBlanc)



    
    # contraintes cavalier
    elif piece in "cC":
        
        mouvPossibleCav = Cavalier(interface, pos, posD, coordonnees)
        
        if posD in mouvPossibleCav:
            ListeMort.append(interface[posD])
            interface[posD] = interface[pos]
            interface[pos] = "*"
        else:
            Impossible(interface, coordonnees,tourBlanc)



    
    #contraintes dame
    elif piece in "dD":
        mouvDroit = Tour(interface,pos,coordonnees) # horizontal et vertical
        mouvDiag = Fou(interface, pos, coordonnees) # diagonales
        
        # même mécanisme que la tour et le fou
        if posD in mouvDroit:
            check = TourCheck(interface,pos,posD,coordonnees)

            if check is True:
                ListeMort.append(interface[posD])
                interface[posD] = interface[pos]
                interface[pos] = "*"
            else:
                Impossible(interface, coordonnees,tourBlanc)


        elif posD in mouvDiag[0] or posD in mouvDiag[1] or posD in mouvDiag[2] or posD in mouvDiag[3]:
            fouCheck = FouCheck(mouvDiag, posD, pos, interface, coordonnees)

            if fouCheck is True:
                ListeMort.append(interface[posD])
                interface[posD] = interface[pos]
                interface[pos] = "*"
            else:
                Impossible(interface, coordonnees,tourBlanc)
                
        else:
            Impossible(interface, coordonnees,tourBlanc)




    # contraintes pion
    elif piece in "pP":
        
        mouvPossiblePion = Pion(piece, interface, pos, posD, coordonnees, ennemi)

        if posD in mouvPossiblePion:

            ListeMort.append(interface[posD])
            interface[posD] = interface[pos]
            interface[pos] = "*"

            pos = posD # une fois le déplacement réussi on confirme que pos = posD
                       # pour que si la position du pion (qui vient d'être mise à jour) est dans le camp adverse, elle pourra se transformer
            if piece == "P" and pos in [0,1,2,3,4,5,6,7]: # pion blanc touche ligne de fond noire
                Mutation(piece, interface, pos)

            elif piece == "p" and pos in [56,57,58,59,60,61,62,63]: # pion noir touche ligne de fond blanche
                Mutation(piece, interface, pos)


        else:
            Impossible(interface, coordonnees,tourBlanc)



    # contraintes roi

    elif piece in "rR":
        
        mouvPossibleRoi = [pos+1,pos+7,pos+8,pos+9,pos-1,pos-7,pos-8,pos-9] # les mouvements à priori possibles du roi 
        
        # selon sa position aux extrémités on lui enlève des mouvements 
        if pos in interface[1:7]:  # en haut
            mouvPossibleRoi = [pos+1,pos+7,pos+8,pos+9,pos-1]
        elif pos in interface[57:63]: # en bas
            mouvPossibleRoi = [pos+1,pos-1,pos-7,pos-8,pos-9]
        elif coordonnees[pos][0] == "a": # à gauche
            mouvPossibleRoi = [pos+1,pos-7,pos-8,pos+9,pos+8]
        elif coordonnees[pos][0] == "h": # à droite
            mouvPossibleRoi = [pos-1,pos+7,pos+8,pos-9,pos-8]

        if posD in mouvPossibleRoi: #rappel: la vérif pour que si les pions autours sont ami ont été fait directement avant, dans Déplacement()
            ListeMort.append(interface[posD])
            interface[posD] = interface[pos] 
            interface[pos] = "*"
        
        else:
             Impossible(interface, coordonnees,tourBlanc)   
            
            
    else:
        Impossible(interface, coordonnees,tourBlanc)




def Echec(interface):
    """
        Fonction échec qui va vérifier avant chaque tour de jeu si un des rois est en échec ou non.
        Il va donc "scanner" les différentes pièces, leur simuler des mouvements possibles à chacuns et donc voir si 
        ces mouvements sont dans les mouvements possibles de rois.
        
    """
    for i in interface: # on cherche la position des 2 rois dans tout l'échiquier
        if i is "r":
            posroi = interface.index(i)
        elif i is "R":
            posRoi = interface.index(i)
    # ils auront les même mouvements mais à des endroits différents
    mouvPossibleroi = [posroi+1,posroi+7,posroi+8,posroi+9,posroi-1,posroi-7,posroi-8,posroi-9]
    mouvPossibleRoi = [posRoi+1,posRoi+7,posRoi+8,posRoi+9,posRoi-1,posRoi-7,posRoi-8,posRoi-9] # subtilité avec posRoi et posroi
    
    c = 0 # un incrémenteur qui représente ici une position dans l'échiquier
   
    while c<64: # j'utilise while car avec for il y aura des bugs puisque interface.index("p" ou "P") sera en plusieurs fois et ne pourra pas trouver sa position correctement
        pion = interface[c]  # on recupere la piece 
        
        # scan des pieces pions
        if pion in "pP": # ici je ne peux pas re-utiliser ma fonction Pion() pour avoir les cases possibles car celui ci ne marchent qu'avec une position
                         #demandée (en cours de jeu et non pas sur commande)
            if pion is "p":  # on simule les positions possibles
                mouv = [c+7,c+9] # je rappelle que "c" est la position de la pièce qu'on "scanne"
            elif pion is "P":
                mouv = [c-7,c-9]
            PosSuppr(interface,mouvPossibleRoi,mouvPossibleroi, mouv, posRoi, posroi, c) # -> est il dans les mouv possibles du roi ?
     
        # scan des pieces cavaliers
        elif pion in "cC":
            # positions possibles
            mouv = [c+6,c-6,c+10,c-10,c+15,c-15,c+17,c-17]
            for j in mouv: # on enleve le surplus
                if j < 0 or j > 64:
                    mouv.remove(j)
            PosSuppr(interface,mouvPossibleRoi,mouvPossibleroi, mouv, posRoi, posroi, c) # test de l'échec

        # scan des dames (la simulation des mouv possibles est procédée de la meme manière)    
        elif pion in "dD":
            mouvDroit = Tour(interface,c,coordonnees)
            mouvDiag = Fou(interface, c, coordonnees)
            mouvDiag = [j for i in mouvDiag for j in i]
            mouv = [] + mouvDroit + mouvDiag
            PosSuppr(interface,mouvPossibleRoi,mouvPossibleroi, mouv, posRoi, posroi, c)
            
        # scan des tours 
        elif pion in "tT":
            mouv = Tour(interface,c,coordonnees)
            
            PosSuppr(interface,mouvPossibleRoi,mouvPossibleroi, mouv, posRoi, posroi, c)

        # scan des fous            
        elif pion in "fF":
            mouv = Fou(interface,c,coordonnees)
            mouv = [j for i in mouv for j in i] # on rassemble les mouvs
            PosSuppr(interface,mouvPossibleRoi,mouvPossibleroi, mouv, posRoi, posroi, c)
                
        c+=1 # incrémentation pour parcourir toutes les pieces de l'échiquier
        
    Jeu = ChessnMat(mouvPossibleRoi,mouvPossibleroi) # on vérifie ensuite s'il y a échec et mat
    
    return Jeu
    
    
    
    
def PosSuppr(interface,mouvPossibleRoi,mouvPossibleroi, mouv, posRoi, posroi, c):
    """
        Fonction qui va vérifier si la liste mouv qui a été créé dans la "simulation" a des positions similaires
        dans la liste des mouvements des rois (si oui ne pourra pas se déplacer ou échec). 
    """

    for j in mouv: # on parcourt la liste des mouvements créés pour la piece en question qu'on est entrain de "scanner"
        if j<0 or j>64:
            mouv.remove(j)
        # si les mouvements coincident (j la position) :
        if j in mouvPossibleRoi and interface[c] in noir: # ceux qui peuvent mettre en échec "R" sont les noirs
            
            if interface[c] in "dt" and j in mouvPossibleRoi[6:]: # pour la tour et donc la dame, il faut checker les mouvements possibles
                mouvCheck = TourCheck(interface,c,j,coordonnees)  # sinon il le mettra en échec même avec un pion p devant
                
                if mouvCheck is False:
                    break # on sort de for (pas de mise en échec)
                    
            if interface[j] == "*": # s'il n'y a rien pour défendre le roi
                mouvPossibleRoi.remove(j) # on supprime le mouvement en question au roi
                print("Échec car",interface[c])
                
            elif j == posRoi: # s'il est dans le champ de vision direct du roi
                print("Échec car",interface[c]) 
              
        # même mécanisme pour les blancs        
        elif j in mouvPossibleroi and interface[c] in blanc:
            
            if interface[c] in "DT" and j in mouvPossibleroi[1:4]:
                mouvCheck = TourCheck(interface,c,j,coordonnees)
                
                if mouvCheck is False:
                    break
                    
            if interface[j] == "*": # sur le champ de vision du roi
                mouvPossibleroi.remove(j)
                print("échec car",interface[c])
                
            elif j == posroi: # direct sur le roi
                print("échec car",interface[c])
    
    return




def ChessnMat(mouvPossibleRoi,mouvPossibleroi):
    """
        Fonction Échec et Mat pour voir si les mouvements d'un des 2 rois sont nulles ou pas.
    """
    Jeu = True
    if mouvPossibleRoi == []:
        print("les noirs ont gagné !")
        Jeu = False
    
    elif mouvPossibleroi == []:
        print("les blancs ont gagné !")
        Jeu = False
        
    return Jeu


    
def Impossible(interface, coordonnees,tourBlanc):
    """
        Fonction pour répéter un déplacement impossible.
    """
    print("Déplacement impossible")
    Deplacement(interface, coordonnees, tourBlanc)



def EasterEgg(a,b,t,f):
    """
        Fonction caché (easter egg).
    """
    if a == "godmode" or b == "godmode":
        if f == blanc:
            for i in interface[48:56]:
                interface[interface.index(i)] = f[3]
        elif f == noir:
            for i in interface[8:16]:
                interface[interface.index(i)] = f[3]
        print("Il semblerait que le jeu a bugué...reprenons.")
    return
    



def Mutation(piece, interface, pos):
    """
        Fonction qui va transformer les pions p une fois avoir réussit à aller dans le camp adverse.
    """
    choix = input("Quel pièce voulez vous prendre ? (tour, cavalier, fou, dame) ")
    
    possibilite = ["tour", "cavalier", "fou", "dame"]

    if choix not in possibilite:
        print("Tappez correctement svp :)")
        Mutation(piece, interface, pos)
    else:
        if piece == "P":
            interface[pos] = chr(ord(choix[0])-32) # il faut basculer la piece choisie en majuscule
        elif piece == "p":
            interface[pos] = choix[0] # tandis qu'ici on peut le prendre directement

    return 




def Deplacement(interface, coordonnees, tourBlanc): # déplacement des pions
    """
        Fonction qui va gérer l'entrée des déplacements.
    """
    if tourBlanc is True:
        ami = blanc
        ennemi = noir
    else:
        ami = noir
        ennemi = blanc
        
    # vérification des positions des rois avant chaque coup
    EchecnMat = Echec(interface) 

    choixPiece = input("pièce à déplacer:  ")
    choixDeplac = input("Où voulez vous le déplacer :  ")
    
    coherence = (choixPiece in coordonnees) and (choixDeplac in coordonnees) and (interface[coordonnees.index(choixPiece)] in ami) # test pour savoir si la

    if coherence is False:                                                          # (ex: on regarde si c'était bien son tour)    # saisie est juste ou non
        print("Regardez le tableau à droite\nVous vous êtes sans doute tromper de pions...")
        EasterEgg(choixPiece, choixDeplac, tourBlanc, ami)
        Deplacement(interface, coordonnees, tourBlanc)
    else:
        position = coordonnees.index(choixPiece)  # on releve la position de la pièce à travers "coordonnees" (ex: "e8" = 4) pour "interface"
        positionDeplac = coordonnees.index(choixDeplac)  # on releve la position du deplacement

        if interface[positionDeplac] == "*" or (interface[positionDeplac] in ami) is False: # si la position du déplacement est vide ou pas dans les pieces amis
            Contraintes(interface, position, positionDeplac, coordonnees, ListeMort, ennemi) # on analyse les contraintes de la pièce
        else:
            print("\nVous ne pouvez pas vous placer sur une case déjà prise!\n")
            Deplacement(interface, coordonnees, tourBlanc)

    return EchecnMat # si il y a EchecnMat le jeu s'arrête




def Joueur1(ListeMort, ScoreB):
    """
        Fonction joueur 1: gestion du score
    """
    print("- Joueur n°1 -")
    for i in ListeMort:
        if ord(i) >= 97 and ord(i) <= 122: # si la piece mangée dans liste mort est en minuscule donc noire
            ScoreB.append(i)               # on ajoute à son score
            ListeMort.remove(i)
    print("score: ", ScoreB)




def Joueur2(ListMort, ScoreN):
    """
        Fonction joueur 2: gestion du score
    """
    print("- Joueur n°2 -")
    for i in ListeMort:
        if ord(i) >= 65 and ord(i) <= 90: # si la piece mangée dans liste mort est en minuscule donc blanche
            ScoreN.append(i)              # on ajoute à son score     
            ListeMort.remove(i)
    print("score: ", ScoreN)



# initialisation du programme : construction échiquier + sa mise en forme
print("-"*10,"Jeu d'Échec programmé par Philippe, Adam et Zineb","-"*10,"\n")
PlacementDebut(interface) # création des pièces
MiseEnForme(interface, coordonnees)
jeu = True 



# boucle du jeu
while jeu is True:
    if tourBlanc is True:
        Joueur1(ListeMort, ScoreB)
        jeu = Deplacement(interface, coordonnees, tourBlanc)
        clear()
        MiseEnForme(interface, coordonnees)
        tourBlanc = False
    else:
        Joueur2(ListeMort, ScoreN)
        jeu = Deplacement(interface, coordonnees, tourBlanc)
        clear()
        MiseEnForme(interface, coordonnees)
        tourBlanc = True
        
        
        
# fin    
print("-"*10,"Merci d'avoir joué :)","-"*10)
restart = input("Voulez vous rejouer ?(o/n)")
if restart == "o" or restart == "oui":
    os.execl(sys.executable, sys.executable, *sys.argv) # on force la relance du programme à l'aide de sys