import matplotlib.pyplot as plt # type: ignore
from math import*

"""
Simuler une orbite elliptique autour de la Terre
avec la méthode de Velocity Verlet
et vérifier la conservation de l'énergie
"""

# Constantes et paramètres de la simulation
GM = 3.986e14 # constante gravitationnelle de la Terre multipliée par sa masse en m^3/s^2
dt = 1 # pas de temps en secondes
duree = 5400 # durée de la simulation en secondes
nb_iterations = int(duree / dt)

# Conditions initiales pour une orbite elliptique
x = 7000e3 # rayon Terre + altitude satellite = 6371 km + 629 km -> = 7000e3 m
y = 0

#Calculer vitesse circulaire
v_circ = sqrt(GM / x)

#Modifier la vitesse pour obtenir une orbite elliptique
vy = 0.8 * v_circ
vx = 0

#affichage de la vitesse en km/h
print(f"Vitesse initiale : {vy*3.6:.2f} km/h")

#calcul initial de l'accélération
r = sqrt(x**2 + y**2)
ax = -GM * x / r**3
ay = -GM * y / r**3

# Listes pour stocker les positions et l'énergie
liste_x = []
liste_y = []
liste_energie = []
liste_distance = []

for i in range(nb_iterations):
    # Mettre à jour la position
    x += vx * dt + 0.5 * ax * dt**2
    y += vy * dt + 0.5 * ay * dt**2

    # Calculer nouvelle distance
    r = sqrt(x**2 + y**2)
    liste_distance.append(r)

    # Calculer nouvelle accélération
    ax_new = -GM * x / r**3
    ay_new = -GM * y / r**3

    # Mettre à jour la vitesse
    vx += 0.5 * (ax + ax_new) * dt
    vy += 0.5 * (ay + ay_new) * dt

    # Mettre à jour l'accélération pour la prochaine itération
    ax = ax_new
    ay = ay_new

    # Stocker les positions
    liste_x.append(x)
    liste_y.append(y)

    # Calculer et stocker l'énergie totale (cinétique + potentielle)
    v = sqrt(vx**2 + vy**2)
    E = 0.5*v**2 - GM / r
    liste_energie.append(E)


print(f"Vitesse finale : {sqrt(vx**2 + vy**2)*3.6:.2f} km/h")

# Indices de périhélie et aphélie
i_perihelie = liste_distance.index(min(liste_distance))
i_aphelie = liste_distance.index(max(liste_distance))

# Coordonnées
x_perihelie, y_perihelie = liste_x[i_perihelie], liste_y[i_perihelie]
x_aphelie, y_aphelie = liste_x[i_aphelie], liste_y[i_aphelie]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.canvas.manager.set_window_title('Simulation orbitale')
ax1.plot(liste_x, liste_y, color='red', label='Orbite')
ax1.plot(0, 0, 'bo', markersize=10, label='Terre')
ax1.plot(x_perihelie, y_perihelie, 'go', markersize=8, label='Périhélie')
ax1.plot(x_aphelie, y_aphelie, 'mo', markersize=8, label='Aphélie')
ax1.set_title('Orbite')
ax1.set_xlabel('x (m)')
ax1.set_ylabel('y (m)')
ax1.axis('equal')
ax1.grid(True)
ax1.legend(loc='upper right', fontsize='small')

ax2.plot(liste_energie, color='green')
ax2.set_title('Énergie spécifique')
ax2.set_xlabel('Pas de temps')
ax2.set_ylabel('J/kg')
ax2.grid(True)

plt.tight_layout()
plt.show()
