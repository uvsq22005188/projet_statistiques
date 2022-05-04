############################
# Groupe : MI TD03
# Kaan Doyurur
# Younous Soussi
# Haled Issouf
# Tri Nghiem
# https://github.com/uvsq22005188/projet_statistiques
############################
# Import des librairies

import time
import random
import os
import webbrowser
import pandas
import tkinter as tk
from tkinter import Menu, LabelFrame, DoubleVar, Scale
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo, showerror

############################
# Constantes

LARGEUR = 500
HAUTEUR = 500
LISTE_COLORS = ["red", "green", "blue", "cyan", "yellow"]

############################
# Variables globales

temp = "tmp"

c_figure = "blue"
c_ligne = "red"

rayon = 1

option_cercle = True
option_carre = False

n = 0

############################
# Fonctions OUTILS


def cree_fichier_alea(n, nomficher):
    """Crée un fichier avec le nom de fichier donné en argument
     contenenant un nombre 'nb' de chiffres de type flottants."""

    with open(nomficher, "w") as f:
        for i in range(n):
            f.write("{} {}\n".format(random.uniform(
                0, 500), random.uniform(0, 500)))

    listeX, listeY = lit_fichier(nomficher)
    copy_tmp(listeX, listeY)
    trace_nuage("aleatoire.txt")

    l_nb_points.configure(text=f"Nombre de points : {n}")


def lit_fichier(nom):
    """Lit le fichier donné en argument et sépare
     en 2 listes X, Y les variables statistiques."""

    with open(nom, "r") as f:
        liste = f.readlines()
        listeX, listeY = [], []
        for i in liste:
            i = i.split()
            listeX.append(float(i[0]))
            listeY.append(float(i[1]))

    return listeX, listeY


def trace_nuage(nom):
    """Trace les figures sur le canvas aux coordonnées de X et Y."""

    delete()

    listeX, listeY = lit_fichier(nom)

    if option_cercle:
        for elem in enumerate(listeX):
            x, y = elem[1], listeY[elem[0]]
            canvas.create_oval(x - rayon, HAUTEUR - y - rayon, x +
                               rayon, HAUTEUR - y + rayon, fill=c_figure,
                               width=0)
    if option_carre:
        for elem in enumerate(listeX):
            x, y = elem[1], listeY[elem[0]]
            canvas.create_rectangle(x - rayon, HAUTEUR - y - rayon, x +
                                    rayon, HAUTEUR - y + rayon, fill=c_figure,
                                    width=0)
    if -0.8 < forteCorrelation(listeX, listeY) < 0.8:
        l_correlation.configure(
            text=f"Forte correlation : False", fg="red")
    else:
        l_correlation.configure(
            text=f"Forte correlation : True", fg="green")

    return len(listeX)


def trace_droite(a, b):
    """Trace une droite sur le canvas"""

    canvas.delete("line")

    x0 = 0
    y0 = HAUTEUR - b  # ne pas oublier d'inverser l'axe y
    x1 = LARGEUR
    if a == 1:
        canvas.create_line(x0, y0, x1, -b, fill=c_ligne, width=3, tags="line")
    if a == -1:
        canvas.create_line(x0, y0, x1, -a * LARGEUR,
                           fill=c_ligne, width=3, tags="line")
    if -1 < a < 1:
        canvas.create_line(x0, y0, x1, (1 - a) * LARGEUR - b,
                           fill=c_ligne, width=3, tags="line")
    else:
        canvas.create_line(x0, y0, x1, -(a - 1) * LARGEUR - b,
                           fill=c_ligne, width=3, tags="line")


############################
# Fonctions CALCULS STATISTIQUES


def moyenne(serie):
    """Calcul la moyenne de la serie donné en argument."""
    moy = sum(serie) / len(serie)

    return moy


def variance(serie):
    """Calcul la variance de la serie donnée en argument"""
    moyenne_serie = moyenne(serie)

    var = sum(((elem - moyenne_serie)**2)
              for elem in serie) / len(serie)

    return var


def covariance(serieX, serieY):
    """Calcul la covariance de la serieX et serieY données en argument."""

    moyenne_serieX = moyenne(serieX)
    moyenne_serieY = moyenne(serieY)

    cov = sum(((elem[1] - moyenne_serieX) * (serieY[elem[0]] - moyenne_serieY))
              for elem in enumerate(serieX)) / len(serieX)
    return cov


def correlation(serieX, serieY):
    """Calcul le coefficient de correlation entre
     la serieX et serieY données en argument."""

    cor = covariance(serieX, serieY) / \
        (variance(serieX) * variance(serieY)) ** 0.5

    return cor


def forteCorrelation(serieX, serieY):
    """Détermine si la correlation entre la serieX et la serieY
     est forte. (-0.8 < correlation < 0.8)"""

    if -0.8 < correlation(serieX, serieY) < 0.8:
        return False
    else:
        return True


def droite_reg(serieX, serieY):
    """Détermine a le coefficient directeur et b l'ordonnée à l'origine."""
    a = covariance(serieX, serieY) / variance(serieX)
    b = moyenne(serieY) - a * moyenne(serieX)
    return (a, b)


############################
# Fonctions FICHIER


def sauvegarde():
    """Sauvegarde la configuration actuelle."""
    listeX, listeY = lit_fichier(temp)
    filepath = asksaveasfilename(title="Sauvegarder une configuration",
                                 filetypes=[(
                                     "Fichier texte", "*.txt")],
                                 defaultextension=[("Fichier texte", ".txt")])

    with open(filepath, "w") as f:
        for elem in enumerate(listeX):
            f.write("{} {}\n".format(elem[1], listeY[elem[0]]))
        showinfo("Sauvegarde", "La configuration a été sauvegardé avec succès")


def charger():
    """Charge une configuration choisit par l'utilisateur."""

    global n, loaded_name

    loaded_name = askopenfilename(title="Charger une configuration", filetypes=[
        ("Fichier .txt", ".txt")])

    n = trace_nuage(loaded_name)

    listeX, listeY = lit_fichier(loaded_name)
    copy_tmp(listeX, listeY)

    l_nb_points.configure(text=f"Nombre de points: {n}")

    showinfo("Charger", "La configuration a été chargé avec succès")


def copy_tmp(listeX, listeY):
    """"""
    with open(temp, "w") as f:
        for i in range(n):
            f.write("{} {}\n".format(listeX[i], listeY[i]))


def reset():
    """"""
    global n

    with open(temp, "w") as f:
        f.write("")
    n = trace_nuage(temp)
    l_nb_points.configure(text=f"Nombre de points: {n}")


def quitter():
    """Quitte le programme."""
    root.destroy()


############################
# Fonction EDITION


def activer_mode_dessin():
    """"""
    global mode_dessin

    mode_dessin = True
    l_dessin.configure(text="Mode dessin: ON", fg="green")
    canvas.bind("<Button-1>", dessin)


def desactiver_mode_dessin():
    """"""
    global mode_dessin

    mode_dessin = False
    l_dessin.configure(text="Mode dessin: OFF", fg="red")
    dessin(None)
    canvas.unbind("<Button-1>")


def dessin(event):
    """"""

    global n

    if mode_dessin:
        x = (float(event.x))
        y = (float(HAUTEUR - event.y))

        canvas.create_rectangle(x - rayon, HAUTEUR - y - rayon, x +
                                rayon, HAUTEUR - y + rayon, fill=c_figure, width=0)

        with open(temp, "a") as f:
            f.write("{} {}\n".format(x, y))

        n += 1

        l_nb_points.configure(text=f"Nombre de points: {n}")


############################
# Fonctions BOUTONS


def trace():
    """Calcul les coefficients et trace la droite
     en utilisant la fonction "trace_droite()"."""

    listeX, listeY = lit_fichier(temp)
    a, b = droite_reg(listeX, listeY)
    trace_droite(a, b)


def couleur():
    """Choisit une couleur random d'une liste"""
    global c_ligne

    c_ligne = random.choice(LISTE_COLORS)
    b_couleur.configure(bg=c_ligne)


def valider():
    """Récupere la valeur de l'utilisateur"""

    global n

    n = int(e_nb_de_points.get())

    listeX, listeY = lit_fichier(loaded_name)
    copy_tmp(listeX, listeY)
    trace_nuage(temp)

    l_nb_points.configure(text=f"Nombre de points: {n}")


############################
# Fonction CSV


def villes_virgule():
    """"""
    clean("villes_virgule.csv")


def housing_california():
    """"""
    clean("housing_california.csv")


def clean(csv_name):
    """"""

    if csv_name == "villes_virgule.csv":
        df = pandas.read_csv("CSV\\villes_virgule.csv")
        nb_hab = df.loc[(df["nb_hab_2010"] <= 500) & (
            df["nb_hab_2012"] <= 500), ["nb_hab_2010", "nb_hab_2012"]]  # garde seulement les villes avec moins de 500 habitants
        nb_2010, nb_2012 = nb_hab["nb_hab_2010"].tolist(
        ), nb_hab["nb_hab_2012"].tolist()  # crée 2 liste avec les valeurs du dataset.
        with open("CONFIGURATIONS\\villes_virgule_c.txt", "w") as f:
            for elem in enumerate(nb_2010):
                f.write(str(elem[1]) + " " + str(nb_2012[elem[0]]) + "\n")

    if csv_name == "housing_california.csv":
        df = pandas.read_csv("CSV\\housing_california.csv")
        med, val = df["median_income"].tolist(
        ), df["median_house_value"].tolist()
        with open("CONFIGURATIONS\\housing_california_c.txt", "w") as f:
            for elem in enumerate(med):
                f.write(str(elem[1]*100) + " " + str(val[elem[0]]/1000) + "\n")


############################
# Fonctions CANVAS

def border():
    """Crée un bord autour du Canvas."""
    canvas.create_rectangle(0, 0, LARGEUR-1, HAUTEUR-1, width=3)


def graduation():
    """Ajoute une graduation sur le canvas."""

    canvas.create_rectangle(0, 0, LARGEUR-1, HAUTEUR-1)
    for x in range(0, HAUTEUR, 50):
        canvas.create_line(x, 550, x, 540)
    for y in range(0, HAUTEUR, 50):
        canvas.create_line(0, y, 10, y)


def delete():
    """Supprime tout les widget sur le Canvas principal et remet en place les bords et la graduation"""
    canvas.delete("all")
    graduation()
    border()

############################
# Fonction AIDE


def aide():
    """Ouvre la page README du projet sur GitHub."""
    webbrowser.open("https://github.com/uvsq22005188/projet_statistiques")


############################
# Fonctions FENÊTRES


def fenetre_statistiques():
    """Crée une fenêtre affichant les valeurs des statistiques."""

    global fenetre_stats

    listeX, listeY = lit_fichier(temp)

    if "fenetre_stats" in globals():
        fenetre_stats.focus_force()
        return
    else:
        fenetre_stats = tk.Toplevel(root)
        fenetre_stats.title("Statistiques")
        fenetre_stats.geometry("180x150")
        fenetre_stats.wm_protocol("WM_DELETE_WINDOW", del_fen_stats)

        l_moyenne_x = tk.Label(
            fenetre_stats, text=f"Moyenne X: {moyenne(listeX):.3f}", font=("product_sans", 12))
        l_moyenne_y = tk.Label(
            fenetre_stats, text=f"Moyenne Y: {moyenne(listeY):.3f}", font=("product_sans", 12))
        l_variance_x = tk.Label(
            fenetre_stats, text=f"Variance X: {variance(listeX):.3f}", font=("product_sans", 12))
        l_variance_y = tk.Label(
            fenetre_stats, text=f"Variance Y: {variance(listeY):.3f}", font=("product_sans", 12))
        l_covariance = tk.Label(
            fenetre_stats, text=f"Covariance: {covariance(listeX, listeY):.3f}", font=("product_sans", 12))
        l_correlation = tk.Label(
            fenetre_stats, text=f"Correlation: {correlation(listeX, listeY):.3f}", font=("product_sans", 12))

        l_moyenne_x.grid(column=0, row=0)
        l_moyenne_y.grid(column=0, row=1)
        l_variance_x.grid(column=0, row=2)
        l_variance_y.grid(column=0, row=3)
        l_covariance.grid(column=0, row=4)
        l_correlation.grid(column=0, row=5)


def del_fen_stats():
    """Ferme la fenêtre statistiques."""

    global fenetre_stats

    fenetre_stats.destroy()
    del fenetre_stats


def fenetre_parametres():
    """Crée une fenêtre option qui permet de changer 'TAILLE, FIGURE, COULEUR LIGNE, COULEUR FIGURE"""

    global fenetre_options

    if "fenetre_options" in globals():
        fenetre_options.focus_force()  # Pour eviter d'ouvrir plusieurs fois la même fenêtre
        return
    fenetre_options = tk.Toplevel(root)
    fenetre_options.title("Options")
    fenetre_options.resizable(False, False)
    # Lorsque l'on quitte la fenêtre, la variable est supprimé de globals()
    fenetre_options.wm_protocol("WM_DELETE_WINDOW", del_fen_options)
    b_valider_option = tk.Button(
        fenetre_options, text="Appliquer", command=valider_option)
    b_valider_option.grid(column=1, row=2, columnspan=3)
    frame1 = LabelFrame(fenetre_options, text="Couleur ligne",
                        bg="white", fg="black", padx=15, pady=15)
    frame2 = LabelFrame(fenetre_options, text="Couleur figures",
                        bg="white", fg="black", padx=15, pady=15)
    frame3 = LabelFrame(fenetre_options, text="Figures",
                        bg="white", fg="black", padx=15, pady=15)
    frame4 = LabelFrame(fenetre_options, text="Taille figures",
                        bg="white", fg="black", padx=15, pady=15)
    frame1.grid(column=0, row=0)
    frame2.grid(column=0, row=1)
    frame3.grid(column=1, row=0)
    frame4.grid(column=1, row=1)
    ############################
    # Couleur ligne

    canvas_couleur_l = tk.Canvas(
        frame1, width=180, height=100, highlightthickness=0)
    canvas_couleur_l.grid(column=0, row=1)

    canvas_couleur_l.create_rectangle(
        20, 40, 40, 60, fill="red", outline="black", width=1)
    canvas_couleur_l.create_rectangle(
        50, 40, 70, 60, fill="green", outline="black", width=1)
    canvas_couleur_l.create_rectangle(
        80, 40, 100, 60, fill="blue", outline="black", width=1)
    canvas_couleur_l.create_rectangle(
        110, 40, 130, 60, fill="cyan", outline="black", width=1)
    canvas_couleur_l.create_rectangle(
        140, 40, 160, 60, fill="yellow", outline="black", width=1)

    def changer_couleur_ligne(event):
        """Change la couleur de la ligne lorsque l'on clique sur un carré de couleur"""
        global c_ligne, b_couleur
        i = canvas_couleur_l.find_withtag("current")
        c_ligne = canvas_couleur_l.itemcget(i, "fill")
        for x in range(7):
            canvas_couleur_l.itemconfigure(x, width=1, outline="black")
        canvas_couleur_l.itemconfigure(i, width=5, outline="gray")

    canvas_couleur_l.bind("<Button-1>", changer_couleur_ligne)

    ############################
    # Couleur figure
    canvas_couleur_f = tk.Canvas(
        frame2, width=180, height=100, highlightthickness=0)
    canvas_couleur_f.grid(column=0, row=0)

    canvas_couleur_f.create_rectangle(
        20, 40, 40, 60, fill="red", outline="black", width=1)
    canvas_couleur_f.create_rectangle(
        50, 40, 70, 60, fill="green", outline="black", width=1)
    canvas_couleur_f.create_rectangle(
        80, 40, 100, 60, fill="blue", outline="black", width=1)
    canvas_couleur_f.create_rectangle(
        110, 40, 130, 60, fill="cyan", outline="black", width=1)
    canvas_couleur_f.create_rectangle(
        140, 40, 160, 60, fill="yellow", outline="black", width=1)

    def changer_couleur_figure(event):
        """Change la couleur de la figure lorsque l'on clique sur un carré de couleur"""
        global c_figure
        i = canvas_couleur_f.find_withtag("current")
        c_figure = canvas_couleur_f.itemcget(i, "fill")
        for x in range(7):
            canvas_couleur_f.itemconfigure(x, width=1, outline="black")
        canvas_couleur_f.itemconfigure(i, width=5, outline="gray")

    canvas_couleur_f.bind("<Button-1>", changer_couleur_figure)

    ############################
    # Figure

    canvas_figure = tk.Canvas(
        frame3, width=180, height=74, highlightthickness=0)
    canvas_figure.grid(column=0, row=0, columnspan=2)

    canvas_figure.create_rectangle(30, 30, 60, 60, fill="black")
    canvas_figure.create_oval(120, 30, 150, 60, fill="black")

    def figure_carre():
        """Switch les bool carre et cercle"""
        global option_carre, option_cercle
        option_cercle, option_carre = False, True
        b_carre.configure(relief="sunken")
        b_cercle.configure(relief="raised")

    def figure_cercle():
        """Switch les bool carre et cercle"""
        global option_carre, option_cercle
        option_cercle, option_carre = True, False
        b_carre.configure(relief="raised")
        b_cercle.configure(relief="sunken")

    b_carre = tk.Button(frame3, text="Carrés",
                        command=figure_carre)
    b_cercle = tk.Button(
        frame3, text="Cercles", command=figure_cercle, relief="sunken")

    b_carre.grid(column=0, row=1)
    b_cercle.grid(column=1, row=1)

    ############################
    # Taille figure

    canvas_taille = tk.Canvas(
        frame4, width=180, height=58, highlightthickness=0)
    canvas_taille.grid(column=1, row=0)

    valeur = DoubleVar()
    scale = Scale(frame4, orient="horizontal", from_=0, to=10,
                  resolution=0.5, length=175, variable=valeur)
    scale.grid(column=1, row=1, columnspan=3)
    canvas_taille.create_rectangle(
        180//2 - rayon, 60//2 - rayon, 180//2
        + rayon, 60//2 + rayon, fill=c_figure)
    valeur.set(rayon)

    def afficher_taille(event):
        """Affiche une représentation de la taille de la figure sur le Canvas."""
        global rayon
        rayon = valeur.get()
        canvas_taille.delete("all")
        canvas_taille.create_rectangle(
            180//2 - rayon, 60//2 - rayon, 180//2
            + rayon, 60//2 + rayon, fill="black")

    scale.bind("<ButtonRelease-1>", afficher_taille)


def valider_option():
    """Applique tout les changement faits dans la fenêtre option et met à jour l'affichage sur le Canvas princapal."""

    trace_nuage(temp)


def del_fen_options():
    """Ferme la fenêtre option."""
    global fenetre_options
    fenetre_options.destroy()
    del fenetre_options


def fenetre_aleatoire():
    """"""
    global n, fenetre_alea

    if "fenetre_alea" in globals():
        fenetre_alea.focus_force()
        return
    else:
        fenetre_alea = tk.Toplevel(root)
        fenetre_alea.title("Statistiques")
        fenetre_alea.geometry("400x60")
        fenetre_alea.wm_protocol("WM_DELETE_WINDOW", del_fen_alea)

        nb_points = tk.Label(
            fenetre_alea, text="Nombre de points pour le fichier aléatoire: ", font=("product_sans", 12))

        e_txt = tk.StringVar()
        e_nb = tk.Entry(fenetre_alea, textvariable=e_txt, fg="black", font=(
            "product_sans", 12), width=14, bd=3)
        e_txt.set(n)

        nb_points.grid(column=0, row=0)
        e_nb.grid(column=1, row=0)

        b_valider_points = tk.Button(
            fenetre_alea, text="Valider", font=("product_sans", 12), command=lambda: cree_fichier_alea(int(e_nb.get()), "aleatoire.txt"))

        b_valider_points.grid(column=1, row=1)


def del_fen_alea():
    """Ferme la fenêtre option."""
    global fenetre_alea
    fenetre_alea.destroy()
    del fenetre_alea

############################
# Programme principal
############################
# Création de la fenêtre principale


root = tk.Tk()
root.title("Projet Statistique")
canvas = tk.Canvas(root, width=LARGEUR, height=HAUTEUR,
                   bg="white", borderwidth=0, highlightthickness=0)
canvas.grid(column=0, row=4, columnspan=3, padx=50, pady=5)
border()
graduation()

############################
# Boutons

b_tracer = tk.Button(root, text="Tracer la droite", command=trace, font=(
    "product_sans", 12), bg="gray", fg="white", width=14)
b_couleur = tk.Button(root, text="Autre couleur", command=couleur, font=(
    "product_sans", 12), bg="gray", fg="white", width=14)
b_valider = tk.Button(text="Valider", command=valider, font=(
    "product_sans", 12), bg="green", fg="white", width=14)

b_tracer.grid(column=0, row=6)
b_couleur.grid(column=0, row=7)
b_valider.grid(column=2, row=7)

############################
# Entry

e_text = tk.StringVar()
e_nb_de_points = tk.Entry(textvariable=e_text, fg="black", font=(
    "product_sans", 12), width=14, bd=3)
e_text.set(n)

e_nb_de_points.grid(column=2, row=6)

############################
# Menu

menubar = Menu(root)

menu1 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Fichier", menu=menu1)
menu1.add_command(label="Sauvegarder", command=sauvegarde)
menu1.add_command(label="Charger", command=charger)
menu1.add_separator()
menu1.add_command(label="Configuration Aléatoire",
                  command=fenetre_aleatoire)
menu1.add_separator()
menu1.add_command(label="Reinitialiser", command=reset)
menu1.add_separator()
menu1.add_command(label="Quitter", command=quitter)

menu2 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edition", menu=menu2)
menu2.add_command(label="Options", command=fenetre_parametres)
menu2.add_separator()
menu2.add_command(label="Statistiques", command=fenetre_statistiques)
menu2.add_separator()
menu2.add_command(label="Activer mode dessin", command=activer_mode_dessin)
menu2.add_command(label="Désactiver mode dessin",
                  command=desactiver_mode_dessin)

menu3 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="CSV", menu=menu3)
menu3.add_separator()
menu3.add_command(label="villes_virgules.csv", command=villes_virgule)
menu3.add_separator()
menu3.add_command(label="housing_california.csv",
                  command=housing_california)
menu3.add_separator()

menu4 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Aide", menu=menu4)
menu4.add_command(label="Github", command=aide)

root.config(menu=menubar)

############################
# Labels

l_nb_points = tk.Label(
    text=f"Nombre de points: {n}", font=("product_sans", 12))
l_dessin = tk.Label(text="Mode dessin: OFF", fg="red",
                    font=("product_sans", 12))
l_correlation = tk.Label(text="Forte corrélation: __",
                         font=("product_sans", 12))


l_dessin.grid(column=1, row=0)
l_nb_points.grid(column=1, row=6)
l_correlation.grid(column=1, row=7)

############################
# Création du fichier tmp

with open("tmp", "w") as f:
    f.write("")

############################
# Boucle principale
root.mainloop()
