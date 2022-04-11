import random
import webbrowser
import pandas
import tkinter as tk
from tkinter import Menu, LabelFrame, DoubleVar, Scale
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo, showerror


# from tkinter import *

LARGEUR = 550
HAUTEUR = 550
LISTE_COLORS = ["black", "red", "green", "blue", "cyan", "yellow"]

rayon = 1
n = 100
c_ligne = "red"
c_figure = "blue"
mode = "OFF"
coords_x, coords_y = "", ""
csv_choisi = False
cercle = True
carre = False
droite = False

############################
# Fenêtre

root = tk.Tk()
root.title("Projet Statistique")
canvas = tk.Canvas(root, width=LARGEUR, height=HAUTEUR,
                   bg="white", borderwidth=0, highlightthickness=0)
canvas.grid(column=0, row=4, columnspan=3, padx=50, pady=5)


############################
# Fonctions

def cree_fichier_alea(nb, nomficher):
    """Crée un fichier avec le nom de fichier donné en argument
     contenenant un nombre 'nb' de chiffres de type flottants."""

    f = open(nomficher, "w")
    for _ in range(nb):

        f.write(str(random.uniform(0, 500)) + " " +
                str(random.uniform(0, 500)) + "\n")
    f.close()


def lit_fichier(nomfic):
    """Lit le fichier donné en argument et sépare
     en 2 listes X, Y les variables statistiques."""
    global listeX, listeY

    f = open(nomfic, "r")
    listeX, listeY = [], []
    for x in f:
        x = x.split()
        listeX.append(float(x[0]))
        listeY.append(float(x[1]))
    f.close()


def trace_nuage(nomf):
    """Trace les figures sur le canvas aux coordonnées de X et Y."""

    global n

    delete()

    if cercle:
        for i in range(len(listeX)):
            x, y = listeX[i], listeY[i]
            canvas.create_oval(x - rayon, HAUTEUR - y - rayon, x +
                               rayon, HAUTEUR - y + rayon, fill=c_figure,
                               width=0)
    if carre:
        for i in range(len(listeX)):
            x, y = listeX[i], listeY[i]
            canvas.create_rectangle(x - rayon, HAUTEUR - y - rayon, x +
                                    rayon, HAUTEUR - y + rayon, fill=c_figure,
                                    width=0)

    if forteCorrelation(listeX, listeY):
        l_forte_correlation.configure(text="Forte correlation: {}".format(
            forteCorrelation(listeX, listeY)),
            font=("product_sans", 12), fg="green")
    else:
        l_forte_correlation.configure(text="Forte correlation: {}".format(
            forteCorrelation(listeX, listeY)),
            font=("product_sans", 12), fg="red")

    l_nb_points.configure(text="Nombre de points: {}".format(
        n), font=("product_sans", 12))


def moyenne(serie):
    """Calcul la moyenne de la serie donné en argument."""
    moy = sum(serie) / len(serie)

    return moy


def variance(serie):
    """Calcul la variance de la serie donnée en argument"""

    var_list = []
    for i in range(len(serie)):
        var_list.append(((serie[i] - moyenne(serie))**2) / len(serie))

    return sum(var_list)


def covariance(serieX, serieY):
    """Calcul la covariance de la serieX et serieY données en argument."""

    cov_list = []
    for i in range(len(serieX)):
        cov_list.append(((serieX[i] - moyenne(serieX))
                        * (serieY[i] - moyenne(serieY))) / len(serieX))

    return sum(cov_list)


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


def trace_droite(a, b):
    """Trace une droite sur le canvas"""

    canvas.delete("line")

    x0 = 0
    y0 = HAUTEUR - b
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


def trace():
    """Calcul les coefficients et trace la droite
     en utilisant la fonction "trace_droite()"."""
    global droite

    if csv_choisi is False:
        showerror("Erreur", "Choisisez un fichier CSV avant !")
    else:
        droite = True
        a, b = droite_reg(listeX, listeY)
        trace_droite(a, b)


def couleur():
    """Choisit une couleur random d'une liste"""

    global c_ligne

    c_ligne = random.choice(LISTE_COLORS)
    if c_ligne == "black":
        b_couleur.configure(bg=c_ligne, fg="white")
    else:
        b_couleur.configure(bg=c_ligne, fg="black")


def activer():
    """Active le mode "Dessin" sur le canvas."""

    global des, mode
    if csv_choisi is False:
        showerror("Erreur", "Choisisez un fichier CSV avant !")
    else:
        des = True
        mode = "ON"
        l_dessin.configure(text="Mode dessin: {}".format(mode), fg="green")
        canvas.bind("<Button-1>", dessin)


def stop():
    """Désactive le mode "Dessin" sur le canvas."""

    global des, mode

    des = False
    mode = "OFF"
    l_dessin.configure(text="Mode dessin: {}".format(mode), fg="red")
    canvas.unbind("<Button-1>")


def dessin(event):
    """Lorsque le mode "Dessin" est activé cette fonction ajoute
    une figure aux coordonnées du clique souris sur le canvas."""

    global coords_x, coords_y, n, listeX, listeY

    if des:
        coords_x = (float(event.x))
        coords_y = (float(HAUTEUR - event.y))

        x = coords_x
        y = coords_y

        listeX.append(x)
        listeY.append(y)

        n += 1

        if cercle:
            canvas.create_oval(x - rayon, HAUTEUR - y - rayon, x +
                               rayon, HAUTEUR - y + rayon, fill=c_figure, width=0)

        else:
            canvas.create_rectangle(x - rayon, HAUTEUR - y - rayon, x +
                                    rayon, HAUTEUR - y + rayon, fill=c_figure, width=0)

        if forteCorrelation(listeX, listeY) == "True":
            l_forte_correlation.configure(text="Forte correlation: {}".format(
                forteCorrelation(listeX, listeY)),
                font=("product_sans", 12), fg="green")

        else:
            l_forte_correlation.configure(text="Forte correlation: {}".format(
                forteCorrelation(listeX, listeY)),
                font=("product_sans", 12), fg="red")

        l_nb_points.configure(text="Nombre de points: {}".format(
            n), font=("product_sans", 12))
        update_label()
        update_stats()


def options():
    """Crée une fenêtre option qui permet de changer 'TAILLE, FIGURE, COULEUR LIGNE, COULEUR FIGURE'"""

    global fenetre_options

    if csv_choisi is False:
        showerror("Erreur", "Choisisez un fichier CSV avant !")
    else:

        if "fenetre_options" in globals():
            fenetre_options.focus_force()
            return
        fenetre_options = tk.Toplevel(root)
        fenetre_options.title("Options")
        fenetre_options.resizable(False, False)
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
            5, 40, 25, 60, fill="red", outline="black", width=1)
        canvas_couleur_l.create_rectangle(
            35, 40, 55, 60, fill="green", outline="black", width=1)
        canvas_couleur_l.create_rectangle(
            65, 40, 85, 60, fill="blue", outline="black", width=1)
        canvas_couleur_l.create_rectangle(
            95, 40, 115, 60, fill="cyan", outline="black", width=1)
        canvas_couleur_l.create_rectangle(
            125, 40, 145, 60, fill="yellow", outline="black", width=1)
        canvas_couleur_l.create_rectangle(
            155, 40, 175, 60, fill="black", outline="black", width=1)

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
            5, 40, 25, 60, fill="red", outline="black", width=1)
        canvas_couleur_f.create_rectangle(
            35, 40, 55, 60, fill="green", outline="black", width=1)
        canvas_couleur_f.create_rectangle(
            65, 40, 85, 60, fill="blue", outline="black", width=1)
        canvas_couleur_f.create_rectangle(
            95, 40, 115, 60, fill="cyan", outline="black", width=1)
        canvas_couleur_f.create_rectangle(
            125, 40, 145, 60, fill="yellow", outline="black", width=1)
        canvas_couleur_f.create_rectangle(
            155, 40, 175, 60, fill="black", outline="black", width=1)

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
            global carre, cercle
            cercle, carre = False, True
            b_carre.configure(relief="sunken")
            b_cercle.configure(relief="raised")

        def figure_cercle():
            """Switch les bool carre et cercle"""
            global carre, cercle
            cercle, carre = True, False
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

    trace_nuage(filename)

    if c_ligne == "black":
        b_couleur.configure(bg=c_ligne, fg="white")
    else:
        b_couleur.configure(bg=c_ligne, fg="black")
    if droite:
        trace()


def valider():
    """Récupere la valeur de l'utilisateur"""
    global n, droite

    n = int(e_nb_de_points.get())

    if csv_choisi is False or f_chargé:
        showerror("Erreur", "Choisisez un fichier CSV avant !")
    else:
        csv(csv_name)
        update_label()
        droite = False


def sauvegarde():
    """Sauvegarde la configuration actuelle."""

    filepath = asksaveasfilename(title="Charger une configuration",
                                 filetypes=[(
                                     "Fichier texte", "*.txt")],
                                 defaultextension=[("Fichier texte", ".txt")])

    if filepath != "":
        f = open(filepath, "w")
        for i in range(len(listeX)):
            f.write(str(listeX[i]) + " " + str(listeY[i]) + "\n")
        showinfo("Sauvegarde", "La configuration a été sauvegardé avec succès")
        f.close()
    else:
        pass


def charger():
    """Charge une configuration choisit par l'utilisateur."""
    global filename, listeX, listeY, f_chargé, n

    f_chargé = True

    filename = askopenfilename(title="Charger une configuration", filetypes=[
                               ("Fichier .txt", ".txt")])

    # Retourne le nombre de ligne dans le fichier chargé.
    # Source: https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python)

    n = sum(1 for line in open(filename))

    main()


def quitter():
    """Ferme la fenêtre Tkinter et quitte l'application"""

    root.destroy()


def aide():
    """Renvoie vers le lien GitHub du projet"""

    webbrowser.open(
        "https://github.com/uvsq22005188/projet_statistiques/blob/main/README.md")


def villes_virgules():
    """Définit le mode csv."""
    global csv_name

    csv_name = "villes_virgule.csv"
    csv(csv_name)


def housing_california():
    """Définit le mode csv."""

    global csv_name

    csv_name = "housing_california.csv"
    csv(csv_name)


def csv(csv_name):
    """Lit le .csv et récupere les données necessaires dans un fichier .txt."""

    global csv_choisi, filename, n, f_chargé

    f_chargé = False

    if csv_name == "villes_virgule.csv":

        csv_choisi = True

        df = pandas.read_csv("villes_virgule.csv")
        nb_hab = df.loc[(df["nb_hab_2010"] <= 500) & (
            df["nb_hab_2012"] <= 500), ["nb_hab_2010", "nb_hab_2012"]]
        nb_2010, nb_2012 = nb_hab["nb_hab_2010"].tolist(
        ), nb_hab["nb_hab_2012"].tolist()
        f = open("villes_virgules_cleaned.txt", "w")
        if int(n) > len(nb_2010):
            showerror(
                "Erreur",
                "La valeur est supérieur au nombre d'éléments dans la liste.")
            n = 0
        else:
            for i in range(int(n)):
                f.write(str(nb_2010[i]) + " " + str(nb_2012[i]) + "\n")
            f.close()

        filename = "villes_virgules_cleaned.txt"

    if csv_name == "housing_california.csv":
        csv_choisi = True
        df = pandas.read_csv("housing_california.csv")
        med = df["median_income"].tolist()
        val = df["median_house_value"].tolist()
        f = open("housing_california_cleaned.txt", "w")
        if int(n) > len(med):
            showerror(
                "Erreur",
                "La valeur est supérieur au nombre d'éléments dans la liste.")
            n = 0
        else:
            for i in range(int(n)):
                f.write(str(med[i]*100) + " " + str(val[i]/1000) + "\n")
            f.close()

        filename = "housing_california_cleaned.txt"

    main()


def menu():
    """Crée un menu."""
    menubar = Menu(root)

    menu1 = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Fichier", menu=menu1)
    menu1.add_command(label="Sauvegarder", command=sauvegarde)
    menu1.add_command(label="Charger", command=charger)
    menu1.add_separator()
    menu1.add_command(label="Quitter", command=quitter)

    menu2 = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edition", menu=menu2)
    menu2.add_command(label="Options", command=options)
    menu2.add_separator()
    menu2.add_command(label="Statistiques", command=stats)
    menu2.add_separator()
    menu2.add_command(label="Activer mode dessin", command=activer)
    menu2.add_command(label="Désactiver mode dessin", command=stop)

    menu3 = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="CSV", menu=menu3)
    menu3.add_separator()
    menu3.add_command(label="villes_virgules.csv", command=villes_virgules)
    menu3.add_separator()
    menu3.add_command(label="housing_california.csv",
                      command=housing_california)
    menu3.add_separator()

    menu4 = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Aide", menu=menu4)
    menu4.add_command(label="Github", command=aide)

    root.config(menu=menubar)


def border():
    """Crée un bord autour du Canvas."""
    canvas.create_rectangle(0, 0, LARGEUR-1, HAUTEUR-1, width=3)


def boutons():
    """Crée les bouttons de la fenêtre principale."""
    global b_couleur

    b_tracer = tk.Button(root, text="Tracer la droite", command=trace, font=(
        "product_sans", 12), bg="gray", fg="white", width=14)
    b_couleur = tk.Button(root, text="Autre couleur", command=couleur, font=(
        "product_sans", 12), bg="gray", fg="white", width=14)
    b_valider = tk.Button(text="Valider", command=valider, font=(
        "product_sans", 12), bg="green", fg="white", width=14)

    b_tracer.grid(column=0, row=6)
    b_couleur.grid(column=0, row=7)
    b_valider.grid(column=2, row=7)


def stats():
    """Crée une fenêtre affichant les valeurs des statistiques."""
    global fenetre_stats, l_moyenne_x, l_moyenne_y
    global l_variance_x, l_variance_y, l_covariance, l_correlation

    if csv_choisi is False:
        showerror("Erreur", "Choisisez un fichier CSV avant !")
    else:
        if "fenetre_stats" in globals():
            fenetre_stats.focus_force()
            return

        fenetre_stats = tk.Toplevel(root)
        fenetre_stats.title("Statistiques")
        fenetre_stats.geometry("180x150")
        fenetre_stats.wm_protocol("WM_DELETE_WINDOW", del_fen_stats)

        l_moyenne_x = tk.Label(fenetre_stats, text="Moyenne X: {}".format(
            ""), font=("product_sans", 12))
        l_moyenne_y = tk.Label(fenetre_stats, text="Moyenne Y: {}".format(
            ""), font=("product_sans", 12))
        l_variance_x = tk.Label(fenetre_stats, text="Variance X: {}".format(
            ""), font=("product_sans", 12))
        l_variance_y = tk.Label(fenetre_stats, text="Variance Y: {}".format(
            ""), font=("product_sans", 12))
        l_covariance = tk.Label(fenetre_stats, text="Covariance: {}".format(
            ""), font=("product_sans", 12))
        l_correlation = tk.Label(
            fenetre_stats, text="Correlation: {}".format(""),
            font=("product_sans", 12))

        l_moyenne_x.grid(column=0, row=0)
        l_moyenne_y.grid(column=0, row=1)
        l_variance_x.grid(column=0, row=2)
        l_variance_y.grid(column=0, row=3)
        l_covariance.grid(column=0, row=4)
        l_correlation.grid(column=0, row=5)

        update_stats()


def del_fen_stats():
    """Ferme la fenêtre statistiques."""
    global fenetre_stats
    fenetre_stats.destroy()
    del fenetre_stats


def del_fen_options():
    """Ferme la fenêtre option."""
    global fenetre_options
    fenetre_options.destroy()
    del fenetre_options


def update_stats():
    """Met à jour l'affichage des statistiques sur la fenêtre statistique."""
    global l_moyenne_x, l_moyenne_y, l_variance_x
    global l_variance_y, l_covariance, l_correlation
    if "fenetre_stats" in globals():
        l_moyenne_x.configure(text="Moyenne X: {0:.3f}".format(
            moyenne(listeX)), font=("product_sans", 12))
        l_moyenne_y.configure(text="Moyenne Y: {0:.3f}".format(
            moyenne(listeY)), font=("product_sans", 12))
        l_variance_x.configure(text="Variance X: {0:.3f}".format(
            variance(listeX)), font=("product_sans", 12))
        l_variance_y.configure(text="Variance Y: {0:.3f}".format(
            variance(listeY)), font=("product_sans", 12))
        l_covariance.configure(text="Covariance: {0:.3f}".format(
            covariance(listeX, listeY)), font=("product_sans", 12))
        l_correlation.configure(text="Correlation: {0:.3f}".format(
            correlation(listeX, listeY)), font=("product_sans", 12))


def update_label():
    """Met à jour l'affichage du label et le nom de la fenêtre."""
    global l_titre
    l_titre.configure(text="Nuage de point du fichier: {}".format(
        filename), font=("product_sans", 12))

    root.title("Projet Statistiques - {}".format(filename))


def label():
    """Crée les labels de la fenêtre principale."""
    global l_nb_points, l_forte_correlation, l_dessin, l_titre

    l_nb_points = tk.Label(text="Nombre de points: {}".format(
        "__"), font=("product_sans", 12))
    l_forte_correlation = tk.Label(
        text="Forte correlation: {}".format("__"), font=("product_sans", 12))
    l_dessin = tk.Label(text="Mode dessin: {}".format(
        mode), fg="red", font=("product_sans", 12))
    l_titre = tk.Label(text="Nuage de point du fichier: {}".format(
        "__"), font=("product_sans", 12))

    l_titre.grid(column=0, row=3, columnspan=3)
    l_dessin.grid(column=1, row=0)
    l_nb_points.grid(column=1, row=6)
    l_forte_correlation.grid(column=1, row=7)


def entry():
    """Crée la case input pour l'utilisateur."""
    global e_nb_de_points

    e_text = tk.StringVar()
    e_nb_de_points = tk.Entry(textvariable=e_text, fg="black", font=(
        "product_sans", 12), width=14, bd=3)
    e_text.set(n)

    e_nb_de_points.grid(column=2, row=6)


def graduation():
    """Ajoute une graduation sur le canvas."""

    canvas.create_rectangle(0, 0, LARGEUR-1, HAUTEUR-1)
    for x in range(0, HAUTEUR, 50):
        canvas.create_line(x, 550, x, 540)
    for y in range(0, HAUTEUR, 50):
        canvas.create_line(0, y, 10, y)


def souris():
    """Affiche les coordonnées de la souris"""
    l_position = tk.Label(text="Position x: {}, y: {}".format(
        "", ""), font=("product_sans", 12), width=18)
    l_position.grid(column=1, row=2)
    canvas.bind("<Motion>", lambda event: l_position.configure(
        text="Position x: {}, y: {}".format(event.x, event.y)))


def delete():
    """Supprime tout les widget sur le Canvas principal et remet en place les bords et la graduation"""
    canvas.delete("all")
    graduation()
    border()


def initialisation():
    """Initalise tout les Widget au démarrage du programme."""
    global listeX, listeY
    root.focus_force()
    menu()
    border()
    graduation()
    boutons()
    entry()
    label()
    souris()

    listeX, listeY = [], []


def main():
    """Fonction principale"""
    delete()
    lit_fichier(filename)
    trace_nuage(filename)
    update_label()


initialisation()


############################
# Boucle principale

root.mainloop()
