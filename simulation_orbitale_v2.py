import matplotlib.pyplot as plt # type: ignore
from math import*


#méthode d'Euler améliorée (simulation de l'orbite de l'ISS)

GM = 3.986e14 # constante gravitationnelle de la Terre multipliée par sa masse en m^3/s^2
dt = 1 # pas de temps en secondes
nb_iterations = int(5600 / dt) #une orbite de l'ISS dure environ 90 minutes

x = 6771e3 # rayon Terre + altitude satellite = 6371 km + 400 km -> x = 6771e3 m
y = 0
vx = 0
vy = sqrt(GM / x) # vitesse orbitale pour une orbite circulaire à cette altitude

liste_x = []
liste_y = []

for i in range(nb_iterations):
    # Calcul de la distance au centre de la Terre
    r_actuel = max((x**2 + y**2)**0.5, 1e-10)  # epsilon pour éviter division par zéro

    # Accélération gravitationnelle
    ax = -GM * x / r_actuel**3
    ay = -GM * y / r_actuel**3

    # Mise à jour de la vitesse (Euler)
    vx += ax * dt
    vy += ay * dt

    # Mise à jour de la position (Euler)
    x += vx * dt
    y += vy * dt

    # Stockage des positions
    liste_x.append(x)
    liste_y.append(y)


plt.plot(liste_x, liste_y, 'r' , label='Trajectoire ISS') 
# Ajouter la Terre au centre
plt.plot(0, 0, 'bo', markersize=15, label='Terre')  # point jaune pour la Terre
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Simulation de l\'orbite de l\'ISS')
plt.axis('equal')  # garder les proportions correctes
plt.grid(True)
plt.legend(loc ='upper right', fontsize = 'small')

# Affichage
plt.show()
