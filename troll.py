# coding: utf8
#!/usr/bin/env python
# ------------------------------------------------------------------------
# Jeu du troll
# Implémentation de AZZIZ Otman
#
# Projet MIF26 - Master 1 - Année 2020/2021
# ------------------------------------------------------------------------
import numpy as np

# nombre de pierres
N = 15
# nombre de cases du chemin (doit être impair)
M = 5
# debug
VERBOSE = True

class Player:
    ''' Classe représentant un joueur '''

    def __init__(self, name):
        '''
        @summary: Création d'un joueur
        @param name: Nom du joueur
        @type name: str
        '''
        self.name = name
        self.n = N
        self.coordinate = None

    # --------------------------------------------------------------------

    def getName(self):
        '''
        @summary: Retourne le nom du joueur
        '''
        return self.name

    # --------------------------------------------------------------------

    def getN(self):
        '''
        @summary: Retourne le nombre de pierres restantes
        '''
        return self.n

    def dropStones(self, n):
        '''
        @summary: Retire le nombre de pierres donné en paramètres
        @param n: Nombre de pierres jetées durant le tour (supérieur à 0)
        @type n: int
        '''
        if n > self.n:
            self.n = 0
        else:
            self.n -= n

    def isOutOfStone(self):
        '''
        @summary: Vérifie si le joueur n'a plus de pierres
        '''
        return self.n == 0

    # --------------------------------------------------------------------

    def getCoordinate(self):
        '''
        @summary: Retourne la coordonnée du joueur
        '''
        return self.coordinate

    def setCoordinate(self, x):
        '''
        @summary: Définit une coordonnée au joueur
        @param x: Coordonnée donnée
        @type x: int
        '''
        self.coordinate = x

    # --------------------------------------------------------------------

    def toString(self):
        '''
        @summary: Retourne les informations sur le joueur 
        '''
        return [self.name, self.n, self.coordinate]

class Troll:
    ''' Classe représentant un troll '''

    def __init__(self):
        '''
        @summary: Création du troll
        '''
        self.coordinate = 0

    # --------------------------------------------------------------------

    def getCoordinate(self):
        '''
        @summary: Retourne la coordonnée du troll
        '''
        return self.coordinate

    def moveTroll(self, n1, n2):
        '''
        @summary: Fait déplacer le troll à des nouvelles coordonnées selon le nombre de pierres jetés par les 2 joueurs
        @param n1: Nombre de pierres jetés par le joueur 1
        @type n1: int
        @param n2: Nombre de pierres jetés par le joueur 2
        @type n2: int
        '''
        if n1 > n2:
            self.coordinate += 1
        elif n1 < n2:
            self.coordinate -= 1

    # --------------------------------------------------------------------

    def toString(self):
        '''
        @summary: Retourne les informations sur le troll 
        '''
        return ["Le troll", self.coordinate]

class Game:
    ''' Classe représentant une partie de jeu '''

    def __init__(self, player1, troll, player2):
        '''
        @summary: Création de la partie
        @param player1: Joueur 1 de la partie
        @type player1: Player class
        @param player1: Joueur 2 de la partie
        @type player1: Player class
        @param troll: Troll désigné pour détruire un royaume
        @type troll: Troll class
        '''
        self.player1 = player1
        self.troll = troll
        self.player2 = player2
        # déclaration des coordonnées pour chaque joueur
        player1.setCoordinate(-(M // 2))
        player2.setCoordinate(M // 2)

    # --------------------------------------------------------------------

    def isOver(self):
        '''
        @summary: Vérifie si la partie est terminée
        '''

        # le troll a atteint le royaume du joueur 1
        if self.troll.getCoordinate() == self.player1.getCoordinate():
            print("Le Troll à atteint le royaume de " + self.player1.getName() + "(J1)")
            return True

        # le troll a atteint le royaume du joueur 2
        if self.troll.getCoordinate() == self.player2.getCoordinate():
            print("Le Troll à atteint le royaume de " + self.player2.getName() + "(J2)")
            return True

        # les 2 joueurs n'ont plus aucune pierre à jeter
        if self.player1.isOutOfStone() and self.player2.isOutOfStone():
            
            # on regarde ou est la coordonnée du troll
            if self.troll.getCoordinate() == 0:
                print("Les 2 joueurs n'ont plus aucune pierre à jeter: le Troll est au milieu. Egalité parfaite")
            elif self.troll.getCoordinate() < 0:
                print("Les 2 joueurs n'ont plus aucune pierre à jeter: le Troll est proche du royaume de " + self.player1.getName() + "(J1)")
            else:
                print("Les 2 joueurs n'ont plus aucune pierre à jeter: le Troll est proche du royaume de " + self.player2.getName() + "(J2)")

            return True

        return False

    # --------------------------------------------------------------------

    def startRound(self):
        '''
        @summary: Lance la manche avec vérification de contraintes avant de sélectionner des stratégies
        '''
        # on vérifie si l'un des 2 joueurs n'a plus de pierre: si oui, le jeu se termine automatiquement
        if self.player1.isOutOfStone():
            # le joueur 1 n'a plus de pierres
            stone1 = 0
            stone2 = 1
            print(self.player1.getName() + "(J1) n'a plus de pierres: " + self.player2.getName() + "(J2) va donc jeter 1 pierre")
        elif self.player2.isOutOfStone():
            # le joueur 2 n'a plus de pierres
            stone1 = 1
            stone2 = 0
            print(self.player2.getName() + "(J2) n'a plus de pierres: " + self.player1.getName() + "(J1) va donc jeter 1 pierre")
        else:
            # chacun des joueurs choisit sa stratégie

            ''' cette partie de choisir le nombre de pierres est a modifier par des stratégies '''
            while True:
                stone1 = int(input("Combien de pierres voulez-vous jeter (J1)? "))
                if stone1 > 0:
                    break

            while True:
                stone2 = int(input("Combien de pierres voulez-vous jeter (J2)? "))
                if stone2 > 0:
                    break

            print(self.player1.getName() + "(J1) a décidé ce tour-ci de jeter " + str(stone1) + " pierres contre " + self.player2.getName() + "(J2) qui compte jeter " + str(stone2) + " pierres")
             
        self.player1.dropStones(stone1)
        self.player2.dropStones(stone2)
        self.troll.moveTroll(stone1, stone2)

    # --------------------------------------------------------------------

    def gainStrategies(self, n1, n2, t):
        '''
        @summary: Création d'une matrice de stratégies et trouver le gain optimal
        @param n1: Nombre de pierres du joueur 1
        @type n1: int
        @param n2: Nombre de pierres du joueur 2
        @type n2: int
        @param t: Coordonnée du troll
        @type t: int
        '''
        difference = n1 - n2

        gainArray = n1 * [0]
        for i in range(n1):
            gainArray[i] = n2 * [0]
            for j in range(n2):
                x = n1 - i - 1
                y = n2 - j - 1
                localDifference = x - y
                if localDifference == difference:
                    localT = t
                elif localDifference > difference:
                    localT = t - 1
                else:
                    localT = t + 1

                gainArray[i][j] = [x, y, localT, getGain(x, y, localT)]

        
        #print(gainArray)
        matrix = np.array(gainArray)
        #print(np.reshape(matrix, (n1, n2, 4)))
        print(matrix)


    # --------------------------------------------------------------------

    def toString(self):
        '''
        @summary: Retourne les informations sur la partie 
        '''
        return [self.player1.toString(), self.troll.toString(), self.player2.toString()]

    def stats(self):
        '''
        @summary: Retourne les statistiques sous forme (nbPierresJ1, nbPierresJ2, coordonnéeTroll) 
        '''
        return [self.player1.getN(), self.player2.getN(), self.troll.getCoordinate()]

# ------------------------------------------------------------------------

def getGain(x, y, t):
    '''
    @summary: Retourne le gain de la configuration donné en paramètre
    @param n1: Nombre de pierres du joueur actuel
    @type n1: int
    @param n2: Nombre de pierres du joueur opposé
    @type n2: int
    @param t: Coordonnée du troll
    @type t: int
    '''
    return None


# ------------------------------------------------------------------------
def main():

    # vérification des bons paramètres de départ (configuration convenable)
    if M % 2 == 0 or M <= 4:
        print("Il faut que le nombre de cases soit impair et supérieur à 4 pour que la partie soit plus intéressante")
        exit()
    if (N <= 0):
        print("Il faut que le nombre de pierres à jeter soit supérieur à 0 pour que la partie soit plus intéressante")
        exit()

    # création des joueurs
    p1 = Player("Robert")
    p2 = Player("Roger")

    # création du troll
    troll = Troll()

    # création de la partie
    game = Game(p1, troll, p2)

    print(game.stats())

    '''
    # début de la partie
    while not game.isOver():
        game.startRound()
        print(game.stats())
    '''

    # DEBUG
    if VERBOSE:
        # création d'une matrice de stratégies 
        game.gainStrategies(5, 4, -1)
        print(game.toString())
        print(game.stats())



if __name__ == '__main__':
    main()