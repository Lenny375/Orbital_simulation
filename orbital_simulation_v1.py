import matplotlib.pyplot as plt # type: ignore

#méthode d'Euler (simple)

GM = 1
dt = 0.01
nb_iterations = 10000

x = 1
y = 0
vx = 0
vy = 1

liste_x = []
liste_y = []

for i in range(nb_iterations):
    r = (x**2 + y**2)**0.5
    ax = -GM * x / r**3
    ay = -GM * y / r**3

    vx += ax * dt
    vy += ay * dt

    x += vx * dt
    y += vy * dt

    liste_x.append(x)
    liste_y.append(y)

plt.plot(liste_x, liste_y)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Simulation de l\'orbite d\'un corps céleste')
plt.axis('equal')
plt.grid()
plt.show()
