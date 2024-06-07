import pygame  # Importing the Pygame module, allowing game creation and various visual options
import math  # Importing the Math module, which contains advanced mathematical functions

pygame.init()  # Initializing the Pygame environment

WIDTH, HEIGHT = 2570, 1980  # Height and width of the screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Creating a window with the specified size
pygame.display.set_caption("Planet Simulation")  # Setting a title for the window

# Constants representing colors in RGB
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GRAY = (80, 78, 81)
ORANGE = (255, 165, 0)
LIGHT_ORANGE = (255, 200, 100)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (25, 25, 112)
GRAY = (169, 169, 169)

# Variable containing a font for text in the window
FONT = pygame.font.SysFont("comicsans", 16)

# Definition of the Planet class representing planets and the sun
class Planet:
    AU = 149.6e6 * 1000  # Distance in meters of an asteroid from the sun
    G = 6.67428e-11  # Gravitational constant
    SCALE = 90 / AU  # Screen scale
    TIMESTEP = 3600 * 24  # Time for motion update

    def __init__(self, name, x, y, radius, color, mass):
        self.name = name  # Name of the planet
        self.x = x  # Initial point of the planet on the X-axis
        self.y = y  # Initial point of the planet on the Y-axis
        self.radius = radius  # Planet's radius
        self.color = color  # Planet's color
        self.mass = mass  # Planet's mass

        self.orbit = []  # Points with location data of the planet over time
        self.sun = False  # Boolean variable indicating whether the planet is the sun
        self.distance_to_sun = 0  # Distance of the planet from the sun

        self.x_vel = 0  # Velocity on the X-axis
        self.y_vel = 0  # Velocity on the Y-axis

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2  # Calculation of X value based on scaling
        y = self.y * self.SCALE + HEIGHT / 2  # Calculation of Y value based on scaling

        # Checking if the planet has orbit points
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                px, py = point
                px = px * self.SCALE + WIDTH / 2
                py = py * self.SCALE + HEIGHT / 2
                updated_points.append((px, py))

            pygame.draw.lines(win, self.color, False, updated_points, 2) # Drawing the planet's path in the window

        pygame.draw.circle(win, self.color, (x, y), self.radius)  # Drawing the planet in the window

        # Adding text to the planet - distance from the sun and the planet's name
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))
            name_text = FONT.render(self.name, 1, WHITE)
            win.blit(name_text, (x - name_text.get_width() / 2, y - name_text.get_height() / 2 + 20))

    def attraction(self, other):
        # Calculation of the forces affecting the planet from another planet
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def draw_saturn_rings(win, planet):
    # Drawing the rings of the planet Saturn
    x = planet.x * planet.SCALE + WIDTH / 2
    y = planet.y * planet.SCALE + HEIGHT / 2
    pygame.draw.ellipse(win, GRAY, (x - planet.radius * 3, y - planet.radius * 1.5, planet.radius * 6, planet.radius * 3), 1)
    pygame.draw.ellipse(win, GRAY, (x - planet.radius * 2.5, y - planet.radius * 1.25, planet.radius * 5, planet.radius * 2.5), 1)
    pygame.draw.ellipse(win, GRAY, (x - planet.radius * 2, y - planet.radius, planet.radius * 4, planet.radius * 2), 1)


def main():
    run = True
    clock = pygame.time.Clock()

    # Creating the planets with their properties
    sun = Planet("Sun", 0, 0, 28, YELLOW, 1.98892 * 10 ** 30)
    sun.sun = True

    earth = Planet("Earth", -1 * Planet.AU, 0, 14, BLUE, 5.9742 * 10 ** 24)
    earth.y_vel = 29.783 * 1000

    mars = Planet("Mars", -1.524 * Planet.AU, 0, 10, RED, 6.39 * 10 ** 23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet("Mercury", -0.387 * Planet.AU, 0, 8, DARK_GRAY, 3.30 * 10 ** 23)
    mercury.y_vel = 47.4 * 1000

    venus = Planet("Venus", -0.723 * Planet.AU, 0, 12, WHITE, 4.8685 * 10 ** 24)
    venus.y_vel = 35.02 * 1000

    jupiter = Planet("Jupiter", -5.2 * Planet.AU, 0, 22, ORANGE, 1.898 * 10 ** 27)
    jupiter.y_vel = 13.07 * 1000

    saturn = Planet("Saturn", -9.5 * Planet.AU, 0, 18, LIGHT_ORANGE, 5.683 * 10 ** 26)
    saturn.y_vel = 9.68 * 1000

    uranus = Planet("Uranus", -19.8 * Planet.AU, 0, 16, LIGHT_BLUE, 8.681 * 10 ** 25)
    uranus.y_vel = 6.80 * 1000

    neptune = Planet("Neptune", -30.1 * Planet.AU, 0, 16, DARK_BLUE, 1.024 * 10 ** 26)
    neptune.y_vel = 5.43 * 1000

    ceres = Planet("Ceres", -2.77 * Planet.AU, 0, 6, GRAY, 9.393 * 10 ** 20)
    ceres.y_vel = 17.882 * 1000

    # List of all planets
    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune, ceres]

    while run:
        clock.tick(60)  # Setting the display rate in frames per second
        WIN.fill((0, 0, 0))  # Filling the window with black color

        for event in pygame.event.get():  # Event loop for user actions
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:  # Updating the positions of the planets and drawing them
            planet.update_position(planets)
            planet.draw(WIN)
            if planet == saturn:  # Checking if the planet is Saturn
                draw_saturn_rings(WIN, planet)  # Drawing Saturn's rings

        pygame.display.update()  # Updating the display

    pygame.quit()  # Ending the program

main()  # Running the main function
