import matplotlib.pyplot as plt # type: ignore
from math import*

"""
Simuler des orbites en 2D avec Velocity Verlet,
extraire automatiquement les paramètres orbitaux,
analyser l'énergie et comparer avec la théorie (lois de Kepler).
"""

# Constantes et paramètres de la simulation
GM = 3.986e14 # constante gravitationnelle de la Terre multipliée par sa masse en m^3/s^2
dt = 1 # pas de temps en secondes
duree = 5400 # durée de la simulation en secondes
r0 = 7000e3 # rayon Terre + altitude satellite = 6371 km + 629 km -> = 7000e3 m
facteur_vitesse = 0.8 # facteur pour ajuster la vitesse initiale et obtenir une orbite elliptique
nb_iterations = int(duree / dt)

def Verlet(dt, duree, r0, facteur_vitesse):
    # Conditions initiales
    x = r0
    y = 0
    v_circ = sqrt(GM / r0)
    vx = 0
    vy = facteur_vitesse * v_circ
    nb_iterations = int(duree / dt)

    #initialisation physique
    r  = sqrt(x**2 + y**2)
    ax = -GM * x / r**3
    ay = -GM * y / r**3

    #listes de stockage
    liste_x = []
    liste_y = []
    liste_v = []
    liste_r = []
    liste_energie = []
    liste_temps = []

    for i in range(nb_iterations):
        # Mettre à jour la position
        x += vx * dt + 0.5 * ax * dt**2
        y += vy * dt + 0.5 * ay * dt**2

        # Calculer nouvelle distance
        r = sqrt(x**2 + y**2)
        liste_r.append(r)

        # Calculer nouvelle accélération
        ax_new = -GM * x / r**3
        ay_new = -GM * y / r**3

        # Mettre à jour la vitesse
        vx += 0.5 * (ax + ax_new) * dt
        vy += 0.5 * (ay + ay_new) * dt

        # Mettre à jour l'accélération pour la prochaine itération
        ax = ax_new
        ay = ay_new

        # Stocker les données pour l'analyse
        liste_x.append(x)
        liste_y.append(y)
        v = sqrt(vx**2 + vy**2)
        liste_v.append(v)
        energie_cinetique = 0.5 * v**2
        energie_potentielle = -GM / r
        energie_totale = energie_cinetique + energie_potentielle
        liste_energie.append(energie_totale)
        liste_temps.append(i*dt)

    return liste_x, liste_y, liste_v, liste_r, liste_energie, liste_temps


# multi-simulation
def multi_simulation():
    facteurs_vitesse = [0.6, 0.8, 1.0, 1.2]

    # Résultats
    liste_facteurs = []
    excentricites = []
    energies = []
    demi_grands_axes = []
    types_orbites = []
    periodes = []
    kepler_constants = []

    for facteur in facteurs_vitesse:

        # Simulation
        liste_x, liste_y, liste_v, liste_r, liste_energie, liste_temps = Verlet(dt, duree, r0, facteur)

        # Paramètres orbitaux
        r_min = min(liste_r)
        r_max = max(liste_r)

        a = (r_min + r_max) / 2
        e = (r_max - r_min) / (r_max + r_min)

        # Energie
        E_moyenne = sum(liste_energie) / len(liste_energie)

        # Période orbitale
        # approximation : détecter passage proche du périhélie
        indices_peri = [i for i, r in enumerate(liste_r) if abs(r - r_min) < 1e3]

        if len(indices_peri) >= 2:
            T = (indices_peri[1] - indices_peri[0]) * dt
        else:
            T = None

        # Kepler
        if T is not None:
            kepler = T**2 / a**3
        else:
            kepler = None

        # Type d'orbite
        if E_moyenne < 0:
            type_orbite = "fermée (ellipse)"
        elif abs(E_moyenne) < 1e-3:
            type_orbite = "parabolique"
        else:
            type_orbite = "ouverte (hyperbole)"

        # Stockage
        liste_facteurs.append(facteur)
        excentricites.append(e)
        energies.append(E_moyenne)
        demi_grands_axes.append(a)
        types_orbites.append(type_orbite)
        periodes.append(T)
        kepler_constants.append(kepler)

    return (
        liste_facteurs,
        excentricites,
        energies,
        demi_grands_axes,
        types_orbites,
        periodes,
        kepler_constants,
    )

# Récupération des données multi-simulation
facteurs, excentricites, energies, a, types, periodes, kepler = multi_simulation()

# Filtrage des valeurs valides pour Kepler
a_valid = []
T_valid = []

for i in range(len(periodes)):
    if periodes[i] is not None:
        a_valid.append(a[i])
        T_valid.append(periodes[i])

# Création figure 2x2
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 7))
fig.canvas.manager.set_window_title('Simulation orbitale lvl4')

# ORBITE (simulation unique)

liste_x, liste_y, liste_v, liste_r, liste_energie, liste_temps = Verlet(dt, duree, r0, facteur_vitesse)

# périhélie / aphélie
i_peri = liste_r.index(min(liste_r))
i_aph = liste_r.index(max(liste_r))

x_peri, y_peri = liste_x[i_peri], liste_y[i_peri]
x_aph, y_aph = liste_x[i_aph], liste_y[i_aph]

ax1.plot(liste_x, liste_y, color='red', label='Orbite')
ax1.plot(0, 0, 'bo', markersize=10, label='Terre')
ax1.plot(x_peri, y_peri, 'go', markersize=8, label='Périhélie')
ax1.plot(x_aph, y_aph, 'mo', markersize=8, label='Aphélie')

ax1.set_title('Orbite')
ax1.set_xlabel('x (m)')
ax1.set_ylabel('y (m)')
ax1.axis('equal')
ax1.grid(True)
ax1.legend(loc='upper right', fontsize='small')

# ÉNERGIE

ax2.plot(liste_temps, liste_energie, color='green')
ax2.set_title('Énergie spécifique')
ax2.set_xlabel('Temps (s)')
ax2.set_ylabel('J/kg')
ax2.grid(True)

# EXCENTRICITÉ

ax3.plot(facteurs, excentricites, marker='o')
ax3.set_title("Excentricité vs vitesse initiale")
ax3.set_xlabel("Facteur de vitesse")
ax3.set_ylabel("Excentricité")
ax3.grid(True)

# LOI DE KEPLER

# Calcul a^3 et T^2
a_cube = [val**3 for val in a_valid]
T_carré = [val**2 for val in T_valid]

ax4.plot(a_cube, T_carré, marker='o')
ax4.set_title("Vérification de la 3e loi de Kepler")
ax4.set_xlabel("a^3 (m^3)")
ax4.set_ylabel("T^2 (s^2)")
ax4.grid(True)

plt.tight_layout()
plt.show()
