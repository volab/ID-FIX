#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
#   Nom du fichier  : mainPi.py
#   Autheur         : Poltergeist42
#   Version         : 2016.03.08
###

###
#   [ lexique ]
#
#   v_              : variable
#   l_              : list
#   t_              : tuple
#   d_              : dictionnaire
#   f_              : fonction
#   C_              : Class
#   i_              : Instance
#   m_              : Module

#################### Taille maximum des commentaires (80 caracteres)######################

###

import time, os
import picamera
import moteurPap

class C_ScanPi(object) :
    """
    Class permettant de cree une instance de l'objet 'C_Scanpi'
    
        [ Liste de methode]
            def __init__(self):
    ""
        Declaration des variables propre a l'instance de l'objet
        
        self.v_nbPhoto
            # Cette valeur correspond au nombre de photos a prendre

        self.coef
            # Cette valeur correspond au rapport entre le pignon et la roue
            # la roue comprte 63 dents et le pignon 21
            # soit un rapport de 1 pour 3
                       
        self.v_totalStep
            # Cette valeur correspond 
            # au nombre de Pas Total en sortie d'arbre
            
        self.v_totalStepCoef
            # Cette valeur correspond
            # au nombre de Pas Total pour effectuer une revolution complete
            # au niveau du plateau
        
        self.v_stepCoef
            # Cette valeur correspond au veritable nombre de pas
            # a parcourir entre les cliche pour que la piece sur le plateau
            # effectue un tour complet
            
            # self.v_totalStepCoef % self.v_nbPhoto doit etre egale a 0
            # les valeurs dispo sont donc
            #
            # self.v_stepCoef   |   self.v_nbPhoto
            #       12288       |       1
            #       6144        |       2
            #       4096        |       3
            #       3072        |       4
            #       2048        |       6
            #       1536        |       8
            #       1024        |       12
            #       768         |       16
            #       512         |       24
            #       384         |       32
            #       256         |       48
            #       192         |       64
            #       128         |       96
            
    ""
    self.v_nbPhoto = 24
    self.v_coef = 3
    self.v_totalStep = 4096
    self.v_totalStepCoef = self.v_totalStep * self.v_coef
    self.v_stepCoef = int(self.v_totalStepCoef//self.v_nbPhoto)
    

def f_prev(self):
    ""
        Cette methode permet de previsualiser la piece sur le plateau
        
        N.B : l'image restera afficher jusqu'a ce que l'on appuie sur la touche 'entree'
    ""
    i_Camera.start_preview()
    input("Appuyer sur la touche 'entree' pour sortir du mode 'Previsualisation'")
    i_Camera.stop_preview()

def f_prevScan(self):
    ""
        Cette methode lance la sequence de prise de vue sans creer les photos associes
    ""
    i_Camera.resolution = (1024, 768)
    for v_photoCount in range(self.v_nbPhoto):
        i_Camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        i_Pap.f_moveStep(self.v_stepCoef)
    
    i_Camera.stop_preview()

def f_scan(self):
    ""
        Cette methode lance la sequence de prise de vue
        Le nom de l'image doit etre renseigne en début de sequence
    ""
    v_photoName = input("entrez le nom de la photo : ")
    i_Camera.resolution = (1024, 768)
    for v_photoCount in range(self.v_nbPhoto):
        v_photoNameFinal = v_photoName + "{:03}.jpg".format(v_photoCount)
        i_Camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        i_Camera.capture(v_photoNameFinal)
        i_Pap.f_moveStep(self.v_stepCoef)

    i_Camera.stop_preview()

    
def f_destructor(self):
    ""
        Methode permettant de terminer proprement les objet 'i_Camera' et 'i_Pap'
    ""
    i_Camera.close()
    i_Pap.f_gpioDestructor()

    """

    def __init__(self):
        """
            Declaration des variables propre a l'instance de l'objet
            
            self.v_nbPhoto
                # Cette valeur correspond au nombre de photos a prendre

            self.coef
                # Cette valeur correspond au rapport entre le pignon et la roue
                # la roue comprte 63 dents et le pignon 21
                # soit un rapport de 1 pour 3
                           
            self.v_totalStep
                # Cette valeur correspond 
                # au nombre de Pas Total en sortie d'arbre
                
            self.v_totalStepCoef
                # Cette valeur correspond
                # au nombre de Pas Total pour effectuer une revolution complete
                # au niveau du plateau
            
            self.v_stepCoef
                # Cette valeur correspond au veritable nombre de pas
                # a parcourir entre les cliche pour que la piece sur le plateau
                # effectue un tour complet
                
                # self.v_totalStepCoef % self.v_nbPhoto doit etre egale a 0
                # les valeurs dispo sont donc
                #
                # self.v_stepCoef   |   self.v_nbPhoto
                #       12288       |       1
                #       6144        |       2
                #       4096        |       3
                #       3072        |       4
                #       2048        |       6
                #       1536        |       8
                #       1024        |       12
                #       768         |       16
                #       512         |       24
                #       384         |       32
                #       256         |       48
                #       192         |       64
                #       128         |       96
                
        """
        self.v_nbPhoto = 32
        self.v_coef = 3
        self.v_totalStep = 4096
        self.v_totalStepCoef = self.v_totalStep * self.v_coef
        self.v_stepCoef = int(self.v_totalStepCoef//self.v_nbPhoto)
        
        self.v_long = 1152  #1024
        self.v_larg = 864  #768
        
    def f_initObj(self) :
        """
            Cette methode permet de creer les objets 'i_Camera' et 'i_Pap'
        """ 
        # Creation et configuration de l'instance de l'objet 'camera'
        self.i_Camera = picamera.PiCamera()
        self.i_Camera.resolution = (self.v_long, self.v_larg)
        self.i_Camera.vflip = True
        self.i_Camera.hflip = True
        self.i_Camera.framerate = 30
        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Now fix the values
        self.i_Camera.shutter_speed = self.i_Camera.exposure_speed
        self.i_Camera.exposure_mode = 'off'
        v_g = self.i_Camera.awb_gains
        self.i_Camera.awb_mode = 'off'
        self.i_Camera.awb_gains = v_g

        # i_Camera.brightness = 63
        # i_Camera.contrast = 52
        
        # Creation de l'instance de l'objet 'moteurPap'
        self.i_Pap = moteurPap.C_MoteurPap()
        self.i_Pap.f_gpioInit()

    
    def f_prev(self):
        """
            Cette methode permet de previsualiser la piece sur le plateau
            
            N.B : l'image restera afficher jusqu'a ce que l'on appuie sur la touche 'entree'
        """
        self.i_Camera.resolution = (self.v_long, self.v_larg)
        self.i_Camera.start_preview()
        input("Appuyer sur la touche 'entree' pour sortir du mode 'Previsualisation'")
        self.i_Camera.stop_preview()

    def f_prevScan(self):
        """
            Cette methode lance la sequence de prise de vue sans creer les photos associes
        """
        # i_Camera.resolution = (self.v_long, self.v_larg)
        self.i_Camera.start_preview()
        for v_photoCount in range(self.v_nbPhoto):
            # Camera warm-up time
            #time.sleep(2)
            self.i_Pap.f_moveStep(self.v_stepCoef)
        
        self.i_Camera.stop_preview()

    def f_scan(self):
        """
            Cette methode lance la sequence de prise de vue
            Le nom de l'image doit etre renseigne en début de sequence
        """
        v_photoName = input("entrez le nom de la photo : ")
        # self.i_Camera.resolution = (self.v_long, self.v_larg)
        self.i_Camera.start_preview()
        for v_photoCount in range(self.v_nbPhoto):
            v_photoNameFinal = v_photoName + "_{:03}.jpg".format(v_photoCount)
            # Camera warm-up time
            time.sleep(2)
            self.i_Camera.capture(v_photoNameFinal)
            time.sleep(0.5)
            self.i_Pap.f_moveStep(self.v_stepCoef)

        self.i_Camera.stop_preview()

        
    def f_destructor(self):
        """
            Methode permettant de terminer proprement les objet 'i_Camera' et 'i_Pap'
        """
        self.i_Camera.close()
        self.i_Pap.f_gpioDestructor()
        
    def f_videoSequence(self):
        """
            Methode permettant de creer une sequence video
        """
        self.i_Camera.start_recording('my_video.h264')
        self.f_prevScan()
        self.i_Camera.stop_recording()
        
    def f_test(self) :
        """
            Methode permettant d'implementer de nouvelles methodes à tester
        """
        
        
def main():
    
    # creation de l'instance de l'objet 'scanPi'
    i_Scan = C_ScanPi()
    i_Scan.f_initObj()
    v_chkMenu = True
    while v_chkMenu :
    
        os.system('clear')

        print("\n\n\n\n")
        print(
                "\t\t\t                  ____   ____      _____          _       ______                     \n",
                "\t\t\t                 |_  _| |_  _|    |_   _|        / \     |_   _ \                    \n",
                "\t\t\t ______  ______    \ \   / / .--.   | |         / _ \      | |_) |   ______  ______  \n",
                "\t\t\t|______||______|    \ \ / // .'`\ \ | |   _    / ___ \     |  __'.  |______||______| \n",
                "\t\t\t                     \ ' / | \__. |_| |__/ | _/ /   \ \_  _| |__) |                  \n",
                "\t\t\t                      \_/   '.__.'|________||____| |____||_______/                   \n\n\n",
                "\t\t\t                     _____  ______          ________  _                              \n",
                "\t\t\t                    |_   _||_   _ `.       |_   __  |(_)                             \n",
                "\t\t\t                      | |    | | `. \ ______ | |_ \_|__   _   __                     \n",
                "\t\t\t                      | |    | |  | ||______||  _|  [  | [ \ [  ]                    \n",
                "\t\t\t                     _| |_  _| |_.' /       _| |_    | |  > '  <                     \n",
                "\t\t\t                    |_____||______.'       |_____|  [___][__]`\_]                    \n\n\n\n"
              )

        print("\tMenu :\n\n",
               "\t\t1 - Previsualisation\n\n",
               "\t\t2 - Previsualisation de la sequence\n\n",
               "\t\t3 - Enregistremant d'une video de la sequence\n\n",
               "\t\t4 - Numerisation\n\n",
               "\t\tT - Test\n\n",
               "\t\tQ - Quitter\n\n")

        v_inputMenu = input("\tvotre choix : ").upper()
    
        if v_inputMenu == "1" : i_Scan.f_prev()
        if v_inputMenu == "2" : i_Scan.f_prevScan()
        if v_inputMenu == "3" : i_Scan.f_videoSequence()
        if v_inputMenu == "4" : i_Scan.f_scan()
        
        
        if v_inputMenu == "T" : i_Scan.f_test()
        if v_inputMenu == "Q" : v_chkMenu = False
        
            
    i_Scan.f_destructor()
    
if __name__ == '__main__':
    main()
