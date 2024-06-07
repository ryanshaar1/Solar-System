import pygame  # מייבא את מודול ה-Pygame, שמאפשר יצירת משחקים ואפשרויות ויזואליות רבות
import math  # מייבא את מודול ה-Math, שמכיל פונקציות מתמטיות מתקדמות

pygame.init()  # איתחול סביבת העבודה של Pygame

WIDTH, HEIGHT = 2570, 1980  # גובה ורוחב של המסך
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # יצירת חלון בגודל המצויין
pygame.display.set_caption("Planet Simulation")  # קביעת כותרת לחלון

# קבועים שמייצגים צבעים ב-RGB
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

# משתנה שמכיל פונט לטקסט בחלון
FONT = pygame.font.SysFont("comicsans", 16)

# הגדרת המחלקה Planet שמייצגת כוכבי לכת ואת השמש
class Planet:
    AU = 149.6e6 * 1000  # מרחק במטרים של אסטרואיד מהשמש
    G = 6.67428e-11  # הקבוע הגרביטצי
    SCALE = 90 / AU  # מידת הגודל של המסך
    TIMESTEP = 3600 * 24  # הזמן שבו מתבצעת העדכון של התנועה

    def __init__(self, name, x, y, radius, color, mass):
        self.name = name  # שם הכוכב
        self.x = x  # נקודת התחלה של הכוכב בציר ה-X
        self.y = y  # נקודת התחלה של הכוכב בציר ה-Y
        self.radius = radius  # רדיוס הכוכב
        self.color = color  # צבע הכוכב
        self.mass = mass  # המסה של הכוכב

        self.orbit = []  # נקודות עם נתוני המיקום של הכוכב במהלך הזמן
        self.sun = False  # משתנה בוליאני המציין האם הכוכב הוא השמש
        self.distance_to_sun = 0  # המרחק של הכוכב מהשמש

        self.x_vel = 0  # מהירות בציר ה-X
        self.y_vel = 0  # מהירות בציר ה-Y

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2  # חישוב ערך ה-X לפי מידת הגידול
        y = self.y * self.SCALE + HEIGHT / 2  # חישוב ערך ה-Y לפי מידת הגידול

        # בדיקה האם יש לכוכב נקודות למעקב
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                px, py = point
                px = px * self.SCALE + WIDTH / 2
                py = py * self.SCALE + HEIGHT / 2
                updated_points.append((px, py))

            pygame.draw.lines(win, self.color, False, updated_points, 2) #ציור המסלול של הכוכב בחלון

        pygame.draw.circle(win, self.color, (x, y), self.radius)  # ציור הכוכב בחלון

        # הוספת טקסט על הכוכב - מרחק מהשמש ושם הכוכב
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))
            name_text = FONT.render(self.name, 1, WHITE)
            win.blit(name_text, (x - name_text.get_width() / 2, y - name_text.get_height() / 2 + 20))

    def attraction(self, other):
        # חישוב הכוחות שמשפיעות על הכוכב מכוכב אחר
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
    # ציור הטבעות של כוכב הלכת שבתאי
    x = planet.x * planet.SCALE + WIDTH / 2
    y = planet.y * planet.SCALE + HEIGHT / 2
    pygame.draw.ellipse(win, GRAY, (x - planet.radius * 3, y - planet.radius * 1.5, planet.radius * 6, planet.radius * 3), 1)
    pygame.draw.ellipse(win, GRAY, (x - planet.radius * 2.5, y - planet.radius * 1.25, planet.radius * 5, planet.radius * 2.5), 1)
    pygame.draw.ellipse(win, GRAY, (x - planet.radius * 2, y - planet.radius, planet.radius * 4, planet.radius * 2), 1)


def main():
    run = True
    clock = pygame.time.Clock()

    # יצירת הכוכבים עם המאפיינים שלהם
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

    # רשימה של כל הכוכבים
    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune, ceres]

    while run:
        clock.tick(60)  # קביעת קצב התצוגה בפריים לשניה
        WIN.fill((0, 0, 0))  # מילוי החלון בצבע שחור

        for event in pygame.event.get():  # לולאת אירועים לקליטת פעולות מהמשתמש
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:  # עדכון מיקומי הכוכבים וציורם
            planet.update_position(planets)
            planet.draw(WIN)
            if planet == saturn:  # בדיקה האם הכוכב הוא שבתאי
                draw_saturn_rings(WIN, planet)  # ציור טבעות הכוכב

        pygame.display.update()  # עדכון התצוגה

    pygame.quit()  # סיום התוכנית

main()  # הפעלת הפונקציה הראשית
