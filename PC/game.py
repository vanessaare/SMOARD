import pygame
from display import BalanceDisplay


class Game:

    def __init__(self):

        pygame.init()

        self.width = 900
        self.height = 620

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption(
            "Balance Board - Level 1"
        )

        self.clock = pygame.time.Clock()
        self.display = BalanceDisplay(self.screen)

        # Spielparameter
        self.target_min = 45
        self.target_max = 55
        self.duration = 10

        # Testwerte
        self.left = 50
        self.right = 50

        # Spielzustand
        self.state = "WAITING"
        self.elapsed = 0

        self.running = True

    # --------------------------------
    # Sensordaten
    # --------------------------------

    def update_sensors(self):

        # Vorerst simulierte Werte
        self.right = 100 - self.left

        # Später kommen hier die FSR-Werte hinein.

    # --------------------------------
    # Balance überprüfen
    # --------------------------------

    def check_balance(self):

        return (
            self.target_min <= self.left <= self.target_max
            and
            self.target_min <= self.right <= self.target_max
        )

    # --------------------------------
    # Messung starten
    # --------------------------------

    def start_game(self):

        self.elapsed = 0
        self.state = "RUNNING"

    # --------------------------------
    # Messung abbrechen
    # --------------------------------

    def abort_game(self):

        self.elapsed = 0
        self.state = "WAITING"

    # --------------------------------
    # Neustart
    # --------------------------------

    def restart_game(self):

        self.elapsed = 0
        self.left = 50
        self.right = 50
        self.state = "WAITING"

    # --------------------------------
    # Spiellogik
    # --------------------------------

    def update_game(self, dt):

        if self.state != "RUNNING":
            return

        if self.check_balance():

            self.elapsed += dt

        else:

            self.elapsed = 0

        if self.elapsed >= self.duration:

            self.elapsed = self.duration
            self.state = "SUCCESS"

    # --------------------------------
    # Eingaben
    # --------------------------------

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_SPACE:

                    if self.state == "WAITING":
                        self.start_game()

                    elif self.state == "RUNNING":
                        self.abort_game()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if (
                    self.state == "WAITING"
                    and self.display.start_button.collidepoint(event.pos)
                ):
                    self.start_game()
                    
                elif (
                    self.state == "RUNNING"
                    and self.display.abort_button.collidepoint(event.pos)
                ):
                    self.abort_game()

                elif (
                    self.state == "SUCCESS"
                    and self.display.restart_button.collidepoint(event.pos)
                ):
                    self.restart_game()

    # --------------------------------
    # Hauptschleife
    # --------------------------------

    def run(self):

        while self.running:

            dt = self.clock.tick(60) / 1000

            self.handle_events()

            self.update_sensors()

            self.update_game(dt)

            progress = self.elapsed / self.duration

            self.display.draw(
                self.left,
                self.right,
                progress,
                self.elapsed,
                self.duration,
                self.state
            )

        pygame.quit()
