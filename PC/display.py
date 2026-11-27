import pygame
import math


# Farben
BACKGROUND = (25, 25, 25)
CARD = (55, 55, 55)
PANEL = (23, 27, 37)
DARK_GREY = (55, 65, 80)
GREEN = (91, 165, 126)
GREEN_DARK = (55, 105, 77)
WHITE = (245, 245, 248)
GREY = (185, 190, 200)
RED = (190, 75, 75)


class BalanceDisplay:

    def __init__(self, screen):

        self.screen = screen
        self.width, self.height = screen.get_size()

        pygame.font.init()

        self.title_font = pygame.font.SysFont(
            "Arial", 25, bold=True
        )
        self.percent_font = pygame.font.SysFont(
            "Arial", 38, bold=True
        )
        self.normal_font = pygame.font.SysFont(
            "Arial", 20
        )
        self.info_font = pygame.font.SysFont(
            "Arial", 17
        )
        self.small_font = pygame.font.SysFont(
            "Arial", 13
        )
        self.timer_font = pygame.font.SysFont(
            "Arial", 30, bold=True
        )
        self.button_font = pygame.font.SysFont(
            "Arial", 18, bold=True
        )

        # Buttonpositionen
        self.abort_button = pygame.Rect(370, 550, 160, 42)
        self.restart_button = pygame.Rect(350, 550, 200, 42)
        self.start_button = pygame.Rect(350, 550, 200, 42)
    # --------------------------------
    # Text zeichnen
    # --------------------------------

    def draw_text(self, text, font, color, x, y):

        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    # --------------------------------
    # Hauptanzeige
    # --------------------------------

    def draw(self, left, right, progress, elapsed,
             duration, state):

        self.screen.fill(BACKGROUND)

        # Äußerer Rahmen
        pygame.draw.rect(
            self.screen,
            CARD,
            (15, 15, self.width - 30, self.height - 30),
            border_radius=18
        )

        # Überschrift
        self.draw_text(
            "LEVEL 1 - BALANCE HOLD",
            self.title_font,
            WHITE,
            self.width // 2,
            48

        )
        # Hauptpanel
        pygame.draw.rect(
            self.screen,
            PANEL,
            (30, 115, self.width - 60, 410),
            border_radius=20
        )

        self.draw_text(
            "HALTE DAS GLEICHGEWICHT",
            self.title_font,
            WHITE,
            self.width // 2,
            150
        )

        # Linke und rechte Belastungsanzeige
        self.draw_side(
            90, 220, 180, 145, left, "LINKS"
        )

        self.draw_side(
            630, 220, 180, 145, right, "RECHTS"
        )

        # Runde Uhr in der Mitte
        self.draw_clock(
            self.width // 2,
            290,
            50,
            progress
        )

        # Aktuelle Sekunde unter der Uhr
        current_second = min(int(elapsed), duration)

        self.draw_text(
            str(current_second),
            self.timer_font,
            GREEN,
            self.width // 2,
            405
        )

        self.draw_text(
            "SEKUNDEN",
            self.small_font,
            GREY,
            self.width // 2,
            430
        )

        self.draw_text(
            "Zielbereich: 45–55 %       |       Haltezeit: 10 Sekunden",
            self.info_font,
            GREY,
            self.width // 2,
            485
        )

        # Spielzustand und Buttons
        if state == "WAITING":

            self.draw_button(
                self.start_button,
                "STARTEN",
                GREEN_DARK
            )


        elif state == "RUNNING":

            self.draw_button(
                self.abort_button,
                "ABBRECHEN",
                RED
            )

        elif state == "SUCCESS":

            self.draw_text(
                "LEVEL GESCHAFFT!",
                self.title_font,
                GREEN,
                self.width // 2,
                185
            )

            self.draw_button(
                self.restart_button,
                "NEUSTART",
                GREEN_DARK
            )

        pygame.display.flip()

    # --------------------------------
    # Belastungsanzeigen
    # --------------------------------

    def draw_side(self, x, y, width, height, value, label):

        pygame.draw.rect(
            self.screen,
            DARK_GREY,
            (x, y, width, height),
            border_radius=15
        )

        # Prozentzahl
        self.draw_text(
            f"{value:.0f} %",
            self.percent_font,
            WHITE,
            x + width // 2,
            y + 40
        )

        # Balkenhintergrund
        bar_y = y + 75
        bar_height = 55

        pygame.draw.rect(
            self.screen,
            GREEN_DARK,
            (x + 15, bar_y, width - 30, bar_height),
            border_radius=8
        )

        # Balkenfüllung
        fill_width = int(
            (width - 30) * max(0, min(value / 100, 1))
        )

        if fill_width > 0:

            pygame.draw.rect(
                self.screen,
                GREEN,
                (x + 15, bar_y, fill_width, bar_height),
                border_radius=8
            )

        # Beschriftung
        self.draw_text(
            label,
            self.normal_font,
            GREY,
            x + width // 2,
            y + height + 20
        )

    # --------------------------------
    # Runde Stoppuhr
    # --------------------------------

    def draw_clock(self, center_x, center_y, radius, progress):

        center = (center_x, center_y)

        # Äußerer Kreis
        pygame.draw.circle(
            self.screen,
            DARK_GREY,
            center,
            radius
        )

        pygame.draw.circle(
            self.screen,
            GREEN,
            center,
            radius,
            4
        )

        # Markierungen für die 10 Sekunden
        for i in range(10):

            angle = -math.pi / 2 + i * (2 * math.pi / 10)

            x1 = center_x + math.cos(angle) * (radius - 10)
            y1 = center_y + math.sin(angle) * (radius - 10)

            x2 = center_x + math.cos(angle) * (radius - 19)
            y2 = center_y + math.sin(angle) * (radius - 19)

            pygame.draw.line(
                self.screen,
                WHITE,
                (x1, y1),
                (x2, y2),
                3
            )

        # Zeiger
        angle = -math.pi / 2 + progress * 2 * math.pi

        hand_length = radius - 27

        hand_x = center_x + math.cos(angle) * hand_length
        hand_y = center_y + math.sin(angle) * hand_length

        pygame.draw.line(
            self.screen,
            GREEN,
            center,
            (hand_x, hand_y),
            5
        )

        pygame.draw.circle(
            self.screen,
            WHITE,
            center,
            6
        )

    # --------------------------------
    # Buttons
    # --------------------------------

    def draw_button(self, rect, text, color):

        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius=10
        )

        self.draw_text(
            text,
            self.button_font,
            WHITE,
            rect.centerx,
            rect.centery
        )
