import matplotlib.pyplot as plt

def lire_et_afficher_fichier(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    blocs = contenu.strip().split("---\n")
    
    plt.figure(figsize=(8, 6))
    for index, bloc in enumerate(blocs):
        liste1, liste2 = [], []
        lignes = bloc.strip().split("\n")
        for ligne in lignes:
            if ", " in ligne:  # Vérifie que la ligne contient bien une virgule
                try:
                    elem1, elem2 = ligne.split(", ")
                    liste1.append(float(elem1))  # Convertir en float
                    liste2.append(float(elem2))  # Convertir en float
                except ValueError:
                    print(f"Ignoring malformed line: {ligne}")  # Debugging
    
        if liste1 and liste2:
            plt.plot(liste1, liste2, marker='o', linestyle='-', label=f"Série {index + 1}")

    plt.xlabel("X (Temps en sec ?)")
    plt.ylabel("Y (Valeur ?)")
    plt.legend()
    plt.title("Graphique des couples de listes")
    plt.grid()
    plt.show()

lire_et_afficher_fichier("result.txt")