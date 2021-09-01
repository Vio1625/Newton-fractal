import imageio as io
from PIL import Image 
from random import randrange
from cmath import pi,exp,log
import numpy as np



def calcul_racines(n):  
    '''Fonction calculant les racines du polynôme z**n-1 pour un n donné'''
    ens_racines=[]                  # liste vide qui contiendra l'ensemble des racines
    for k in range(n):              # il y a n racines en tout pour un polynôme de la forme z**n-1 
        racine=exp(2*1j*k*pi/n)     # les racines sont exp(2*i*k*pi/n) avec k allant de 0 à n-1
        ens_racines+=[racine] 
    return(ens_racines)





def racine_couleur(n,ens_racines):
    ''' Fonction qui choisit des couleurs et les associe à des racines'''
    ens_racine_couleur=[]           # liste qui contiendra un ensemble de tuples avec comme premier élément la racine et deuxième sa couleur
    h=int(255/n)                    # variable choisie pour établir une formule
    k=0
    for racine in ens_racines:
        couleur_1=255-k*h           # le rouge diminue au fur et à mesure que k augmente
        if k%3==0:                  
            couleur_2=2*k*h         # la composante verte augmente avec des k divisible par 3
            couleur_3=0             # aucune composante bleue avec un k divisible par 3
        elif k%3==1:
            couleur_2=0             # aucune composante verte si le reste de k par 3 vaut 1
            couleur_3=2*k*h         # la composante bleue augmente pour un reste égal à 1 (div eucl de k par 3)
        else:
            couleur_2=2*k*h         # les composantes vertes et bleues augmentent avec un reste valant 2
            couleur_3=2*k*h 
        k+=1
        couleur=(couleur_1,couleur_2,couleur_3)
        racine_couleur=[(racine,couleur)]
        ens_racine_couleur+=racine_couleur
    return(ens_racine_couleur)



def calculCouleur(n,valeur,eps_calcul,ens_racine_couleur):
    ''' Fonction qui regarde vers quelle racine converge un z donné et qui l'associe à la couleur de cette racine '''
    for k in ens_racine_couleur:
        if abs(k[0]-valeur)<eps_calcul:   
            return (k[1])
    return (0,0,0) 



eps_calcul=1e-5                     # valeur de comparaison utilisée pour voir si une différence tend vers 0

#menu
print("1) Réglage par défaut")
menu=int(input("2) Réglages \n"))
if menu==1:                         # version préréglée sur l'exmple du sujet
    xmin=-1
    xmax=-0.25
    ymin=0.25
    ymax=1
    eps_x=1e-3                      # pas entre deux abscisses consécutives
    N_x=int(abs(xmax-xmin)/eps_x)   # nombre de pixels en longueur
    eps_y=1e-3                      # pas entre deux ordonées consécutives
    N_y=int(abs(ymax-ymin)/eps_y)   # nombre de pixels en largeur
    m=1
    h=1
    n=4
    S=np.array([1,-1,2])            # source lumineuse
    P=lambda z:z**4-1
    dP=lambda z:4*z**3
    dP2=lambda z:12*z**2
    ens_racines=calcul_racines(4)   # ensemble des racines
    
    def newton1(P,dP,z0,eps):       # uniquement pour la version par défaut (n=4)
        z=z0
        old=z0+1
        N=0                         # nombre d'itérations
        Nmax=50
        while abs(old-z)>=eps and N<=Nmax:
            old=z
            z=0.75*z+z**(-3)/4      # on calcule zn+1
            N+=1
        return([z,N])
    
    def newton2(P,dP,dP2,z0,eps,ens_racines):   # uniquement pour la version par défaut (n=4)
        '''Fonction qui renvoie la racine z vers laquelle z0 converge et la profondeur Z'''
        for z in ens_racines:
            if abs(z0-z)<=1e-10:                # si z0 est déjà une racine
                return(0,0)
        z=z0
        dz0=1
        Pz=P(z0)
        dz=dP(z0)
        d=eps+1                                 # pour pouvoir entrer dans la boucle lors de la première itération
        N=0
        Nmax=50
        while d>eps and N<=Nmax:
            zn=z                                # pour mémoriser la valeur de z à l'itération précédente
            dzn=dz                              # pour mémoriser la valeur de dz à l'itération précédente
            z=0.75*z+z**(-3)/4                  # on calcule zn+1
            dz=dz*0.75*(1-zn**-4)               # on calcule dzn+1
            d=abs(zn-z)
            N+=1
        D=abs(dzn-dz)
        E=(d*abs(log(d)))/D
        Z=(exp(-E)-1)/(exp(-E)+1)
        return(z,Z)                             

else:
    xmin=float(input("abscisse minimum  "))
    xmax=float(input("abscisse maximum  "))
    ymin=float(input("ordonnée minimum  "))
    ymax=float(input("ordonnée maximum  "))
    N_x=int(input("nombre de pixels en longueur  "))
    N_y=int(input("nombre de pixels en largeur  "))
    eps_x=abs(xmax-xmin)/N_x                        # pas entre deux abscisses consécutives
    eps_y=abs(ymax-ymin)/N_y                        # pas entre deux ordonnées consécutives
    print("deux paramètres réels positifs pour la version en profondeur :")  
    m=float(input("m="))
    h=float(input("h="))
    print("coordonées de la source lumineuse :")
    S=[float(input("abscisse  "))]
    S+=[float(input("ordonée  "))]
    S+=[float(input("côte  "))]
    print("1) Polynôme de la forme z^n-1")
    f=int(input("2) autre polynôme \n"))
    if f==1:
        n=int(input("Polynôme de la forme z^n-1 avec n="))
        P=lambda z:z**n -1
        dP=lambda z:n*z**(n-1)
        dP2=lambda z:n*(n-1)*z**(n-2)
        ens_racines=calcul_racines(n)
        
        def newton1(P,dP,z0,eps):  # simplifiée pour les polynômes de la forme z**n-1
            z=z0
            old=z0+1
            N=0
            Nmax=50
            while abs(old-z)>=eps and N<=Nmax:
                old=z
                z=(1-1/n)*z+z**(1-n)/n      # on calcule zn+1
                N+=1
            return([z,N])
            
        def newton2(P,dP,dP2,z0,eps,ens_racines):       # simplifiée pour les pôlynômes de la forme z**n-1
            '''Fonction qui renvoie la racine vers laquelle z0 et converge et la profondeur'''
            for z in ens_racines:
                if abs(z0-z)<=1e-10:             # si z0 est déjà une racine
                    return(0,0)
            z=z0
            dz0=1
            Pz=P(z0)
            dz=dP(z0)
            d=eps+1                              # pour pouvoir entrer dans la boucle lors de la première itération
            N=0
            Nmax=50
            
            while d>eps and N<=Nmax:
                zn=z                            # pour mémoriser la valeur de z à l'itération précédente
                dzn=dz                          # pour mémoriser la valeur de dz à l'itération précédente
                z=(1-1/n)*z+z**(1-n)/n          # calcul de zn+1
                dz=dz*(1-1/n)*(1-zn**-n)        # calcul dzn+1
                d=abs(zn-z)
                N+=1
            D=abs(dzn-dz)
            E=(m*d*abs(log(d)))/D
            Z=h*((exp(-E)-1)/(exp(-E)+1))
            return(z,Z)
    
    
    
    else:                               # pour tous les polynômes
        n=int(input("degré du polynôme  "))
        liste_coef=[float(input("coefficient dominant  "))]
        for i in range(n-1,-1,-1):
            print("coefficient de z^",i," ")
            liste_coef+=[float(input())]
        P=np.poly1d(liste_coef)         # création du polynôme demandé
        dP=P.deriv()                    # calcul de la dérivée
        dP2=dP.deriv()                  # calcul de la dérivée seconde
        ens_racines=P.roots             # calcul des racines
        
        def newton1(P,dP,z0,eps): 
            z=z0
            Pz=P(z0)
            N=0                             # nombre d'itérations
            Nmax=50
            while abs(Pz)>=eps and N<=Nmax:
                z=z-P(z)/dP(z)              # calcul de zn+1
                Pz=P(z)                     
                N+=1
            return([z,N])
            
        def newton2(P,dP,dP2,z0,eps,ens_racines):
            '''Fonction qui renvoie la racine vers laquelle z0 et converge et la profondeur'''
            for z in ens_racines:
                if abs(z0-z)<=1e-10:            # si z0 est déjà une racine
                    return(0,0)
            z=z0
            dz0=1
            Pz=P(z0)
            dz=dP(z0)
            d=eps+1                             # pour pouvoir entrer dans la boucle lors de la première itération
            N=0
            Nmax=50
            while d>eps and N<=Nmax:
                zn=z                            # on mémorise le z de l'itération précédente
                dzn=dz                          # on mémorise le dz de l'itération précédente
                z=z-P(z)/dP(z)                          # calcul de zn+1
                dz=dz*(P(zn)*dP2(zn))/(dP(zn)**2)       # calcul de dzn+1
                d=abs(zn-z)                              
                N+=1
            D=abs(dzn-dz)
            E=(m*d*abs(log(d)))/D
            Z=h*((exp(-E)-1)/(exp(-E)+1))
            return(z,Z)



def Fract_Newt(n,P,dP,eps_x,eps_y):
    ''' Fonction qui affiche la fractale version plate associée à un polynôme donné'''
    ens_racine_couleur=racine_couleur(n,ens_racines)    # liste de tuples associant racines et couleurs
    Nmax=50
    inv_eps_x=int(1 / eps_x) 
    inv_eps_y=int(1/eps_y)    
    diff_x=-xmin                    # pour effectuer les conversions entre les abscisses des pixels et les abscices des points
    diff_y=ymax                     # pour effectuer les conversions entre les ordonées des pixels et les ordonées des points 

    im = Image.new("RGB",(int(N_x),int(N_y)))  # création d'une image
    x=xmin
    y=ymax                          # y va décroître
    while x < xmax:
        
        while y > ymin:
            if abs(x)<1e-10 and abs(y)<1e-10:  # si x et y sont trop proches de 0
                im.putpixel((int((diff_x+x)*inv_eps_x),int((diff_y-y)*inv_eps_y)), (0,0,0))  
            else:
                z0=complex(x,y) 
                valeur=newton1(P,dP,z0,eps_calcul)
                couleur=calculCouleur(n,valeur[0],eps_calcul,ens_racine_couleur)
                couleur1=(couleur[0]*(1-valeur[1]/Nmax))        # composante rouge
                couleur2=(couleur[1]*(1-valeur[1]/Nmax))        # composante verte
                couleur3=(couleur[2]*(1-valeur[1]/Nmax))        # composante bleue
                couleur=(int(couleur1),int(couleur2),int(couleur3))     # couleur du z0
                im.putpixel((int((diff_x+x)*inv_eps_x),int((diff_y-y)*inv_eps_y)), couleur)  # x et y (du plan) sont convertis en leur equivalent en pixel
            y-=eps_y
        y=ymax   
        x+=eps_x
    im.show()



def Frac_Newt_Relief(P,dP,eps_x,eps_y):
    '''Fonction qui affiche la fractale en relief associée à un polynôme donné'''
    ens_racine_couleur=racine_couleur(n,ens_racines)    # liste de tuples associant une racine à sa couleur
    Nmax=50
    inv_eps_x=int(1 / eps_x)            # pour la conversion entre les abscisses des pixels et les abscisses des points
    inv_eps_y=int(1/eps_y)              # pour la conversion entre les ordonnées des pixels et les ordonnées des points
    diff_x=-xmin                   
    diff_y=ymax                  
    im = Image.new("RGB",(int(N_x),int(N_y)))   # création de l'image
    x=xmin
    y=ymax                                      # pour pouvoir faire décroitre les ordonnées 
    Nmax=50
    while x < xmax:
        z,ZA=newton2(P,dP,dP2,complex(x,y+eps_y),eps_calcul,ens_racines)  # calcul de la profondeur du point C qui se trouve hors de l'image (pas déjà calculé en un point A)
        list_coteB=[]
        list_convergB=[]                # liste des racines vers lesquelles les points B convergent
        while y > ymin:
            ZC=ZA                       # le point C se situe à la même position que le point A de l'itération précédente
            zA=complex(x,y)
            if abs(zA)<=1e-10:          # si zA est déjà une racine
                im.putpixel((x_pixel,y_pixel), (0,0,0)) 
            x_pixel=int((diff_x+x)*inv_eps_x)           # conversion des abscisses
            y_pixel=int((diff_y-y)*inv_eps_y)           # conversion des ordonnées
            if x==xmin:
                z,ZA=newton2(P,dP,dP2,zA,eps_calcul,ens_racines)        # calcul de la profondeur du point A qui se trouve sur la première ligne (pas déjà calculé en un point B)
            else:
                z=list_convergA[y_pixel]
                ZA=list_coteA[y_pixel]
            zB=complex(x+eps_x,y)
            b,ZB=newton2(P,dP,dP2,zB,eps_calcul,ens_racines)
            list_coteB+=[ZB]                # mémoïsation des valeurs de B car le point A se retrouvera à la même abscisse plus tard
            list_convergB+=[b]
            AB=np.array([eps_x,0,(ZB-ZA).real])             # vecteurs AB et AC
            AC=np.array([0,eps_y,(ZC-ZA).real])
            N=np.cross(AB,AC)                               # produit vectoriel entre AB et AC
            N=N/(np.linalg.norm(N))                         # on normalise le vecteur N
            U=np.array([S[0]-x,S[1]-y,S[2]-(ZA).real])      # création du vecteur N
            U=U/(np.linalg.norm(U))                         # on normalise le vecteur U
            couleur=calculCouleur(n,z,eps_calcul,ens_racine_couleur)
            if np.isnan(np.inner(N,U)):     # cas où le produit vectoriel, le produit scalaire ou la normalisation a effectué une division par 0 (si python veut afficher "not a number")
                im.putpixel((x_pixel,y_pixel), (0,0,0)) 
            else:
                couleur1=couleur[0]*np.inner(N,U)           # on multiplie par le produit scalaire entre N et U la composante rouge
                couleur2=couleur[1]*np.inner(N,U)           # on multiplie par le produit scalaire entre N et U la composante verte
                couleur3=couleur[2]*np.inner(N,U)           # on multiplie par le produit scalaire entre N et U la composante bleue
                couleur=(int(couleur1),int(couleur2),int(couleur3))    
                im.putpixel((x_pixel,y_pixel), couleur) 
            y-=eps_y                                        # on parcourt dans le sens décroissant 
        list_coteA=np.copy(list_coteB)                      # on copie les valeurs de B afin de les réutiliser pour A
        list_convergA=np.copy(list_convergB)
        y=ymax  
        x+=eps_x                                
    im.show()

  
    
# menu

print("1) Version plate")
menu=int(input(("2) Version en relief\n")))
if menu==1:
    Fract_Newt(n,P,dP,eps_x,eps_y)
else :
    Frac_Newt_Relief(P,dP,eps_x,eps_y)