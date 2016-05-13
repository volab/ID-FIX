#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
#   Nom du fichier  : pillowSubstract.py
#   Autheur         : Poltergeist42
#   Version         : 2016.03.16
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


# import argparse
# import os.path
import PIL.Image as m_pilImg     # PIL.Image is a module not a class...
import numpy as i_np

def pilSubst():
    """Main function :
        pilSubst effectue une soustration entre deux images. Cette operation est effectuer
        32x en incrementant automatiquement le nom de chacune des images.
    """


    # PROCESS #################################################################
    v_photoVide = input("entrez le nom de la photo 'vide' : ")
    v_photoModel = input("Entrez le nom de la photo 'Model' : ")
    for v_photoCount in range(32):
        v_photoVideFinal = v_photoVide + "_{:03}.jpg".format(v_photoCount)
        v_photoModelFinal = v_photoModel + "_{:03}.jpg".format(v_photoCount)           
        i_np_ImgMask = i_np.array(m_pilImg.open(v_photoVideFinal))
        
        i_img = m_pilImg.open(v_photoModelFinal)

        i_np_img1 = i_np.array(i_img)
        # print(i_np_img1)
        i_np_ImgMask = i_np.clip(i_np_ImgMask, 0, i_np_img1)
            # i_np_ImgMask est contrain dans l'inverval 0 --> i_np_img1 de cette facon,
            # la soustraction ne peut pas repartir depuis 255 en cas de soustraction
            # negative.
        i_np_img = i_np_img1 - i_np_ImgMask
        print(i_np_img.shape)
        
        i_img = m_pilImg.fromarray(i_np_img)

        v_outputFilename = "out_" + v_photoModelFinal
        i_img.save(v_outputFilename)


if __name__ == '__main__':
    print("Attention, ce script doit etre executer en tan que root")
    pilSubst()