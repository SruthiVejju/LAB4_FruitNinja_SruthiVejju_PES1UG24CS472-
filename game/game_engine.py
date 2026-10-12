
import math
import array
import random
import pygame

from .fruit import Fruit


WHITE = (255, 255, 255)
BOMB_BLACK = (30, 30, 30)

FRUIT_COLORS = [
    (220, 60, 60),
    (230, 140, 40),
    (230, 200, 40),
    (90, 180, 90),
]


class GameEngine:
    DIFFICULTIES = {
        "Easy": {
            "spawn_interval": 75,
            "bomb_chance": 0.08,
            "speed_scale": 0.85,
        },
        "Medium": {
            "spawn_interval": 55,
            "bomb_chance": 0.15,
            "speed_scale": 1.0,
        },
        "Hard": {
            "spawn_interval": 38,
            "bomb_chance": 0.25,
            "speed_scale": 1.15,
        },
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("Arial", 28)
        self.title_font = pygame.font.SysFont(
            "Arial", 48, bold=True
        )
        self.button_font = pygame.font.SysFont("Arial", 25)

        self.sounds = {}
        self.audio_ready = False
        self._init_sounds()

        self.difficulty = "Medium"
        self.replay_requested = False
        self.exit_requested = False
        self._game_over_sound_played = False

        self._create_buttons()
        self.reset(self.difficulty)

    # --------------------------------------------------
    # SOUND EFFECTS
    # --------------------------------------------------

    def _make_tone(
        self,
        frequency,
        duration,
        volume=0.4,
        waveform="sine",
        falling=False,
    ):
        sample_rate = 22050
        total_samples = int(sample_rate * duration)
        samples = array.array("h")

        for i in range(total_samples):
            t = i / sample_rate
            progress = i / max(total_samples, 1)

            current_frequency = frequency
            if falling:
                current_frequency = frequency * (
                    1.0 - 0.75 * progress
                )

            phase = 2 * math.pi * current_frequency * t

            if waveform == "square":
                wave = (
                    1.0 if math.sin(phase) >= 0 else -1.0
                )
            elif waveform == "saw":
                wave = (
                    2.0 * ((phase / (2 * math.pi)) % 1.0)
                    - 1.0
                )
            else:
                wave = math.sin(phase)

            attack = min(1.0, i / 180)
            envelope = attack * (1.0 - progress) ** 1.5

            value = int(
                32767 * volume * envelope * wave
            )
            samples.append(value)

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def _make_game_over_sound(self):
        """Create a descending three-note ending melody."""
        sample_rate = 22050
        combined = array.array("h")

        notes = [
            (784, 0.22),
            (587, 0.28),
            (330, 0.65),
        ]

        for frequency, duration in notes:
            sound = self._make_tone(
                frequency,
                duration,
                volume=0.48,
                waveform="sine",
            )

            combined.extend(
                array.array("h", sound.get_raw())
            )

            # Short pause between the notes.
            combined.extend(
                array.array("h", [0] * 2200)
            )

        return pygame.mixer.Sound(
            buffer=combined.tobytes()
        )

    def _init_sounds(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(
                    frequency=22050,
                    size=-16,
                    channels=1,
                    buffer=512,
                )

            # Short, bright slicing pop.
            self.sounds["fruit"] = self._make_tone(
                1250,
                0.10,
                volume=0.35,
                waveform="sine",
            )

            # Low, rough, descending bomb buzz.
            self.sounds["bomb"] = self._make_tone(
                105,
                0.70,
                volume=0.60,
                waveform="saw",
                falling=True,
            )

            # Longer three-note Game Over melody.
            self.sounds["game_over"] = (
                self._make_game_over_sound()
            )

            self.audio_ready = True

        except (pygame.error, OSError):
            self.audio_ready = False

    def _play_sound(self, name):
        if not self.audio_ready:
            return

        try:
            self.sounds[name].play()
        except pygame.error:
            pass

    # --------------------------------------------------
    # GAME SETUP AND DIFFICULTY
    # --------------------------------------------------

    def _create_buttons(self):
        button_width = 150
        button_height = 48
        gap = 15

        total_width = (
            button_width * 4 + gap * 3
        )
        start_x = (self.width - total_width) // 2
        y = self.height // 2 + 105

        self.buttons = {}

        for i, label in enumerate(
            ["Easy", "Medium", "Hard", "Exit"]
        ):
            self.buttons[label] = pygame.Rect(
                start_x + i * (button_width + gap),
                y,
                button_width,
                button_height,
            )

    def reset(self, difficulty="Medium"):
        self.difficulty = difficulty
        settings = self.DIFFICULTIES[difficulty]

        self.fruits = []
        self.trail = []
        self.previous_mouse_pos = None

        self.spawn_interval = settings[
            "spawn_interval"
        ]
        self._spawn_timer = 0
        self.bomb_chance = settings["bomb_chance"]
        self.speed_scale = settings["speed_scale"]

        self.lives = 3
        self.score = 0
        self.game_over = False

        self.replay_requested = False
        self.exit_requested = False
        self._game_over_sound_played = False

    # --------------------------------------------------
    # FRUIT SPAWNING AND COLLISION DETECTION
    # --------------------------------------------------

    def spawn_fruit(self):
        x = random.randint(60, self.width - 60)
        vy = -random.uniform(13, 16) * self.speed_scale
        vx = random.uniform(-2, 2)

        kind = (
            "bomb"
            if random.random() < self.bomb_chance
            else "fruit"
        )

        fruit = Fruit(
            x,
            self.height + 30,
            vx,
            vy,
            0.35,
            kind=kind,
        )

        fruit.color = (
            BOMB_BLACK
            if kind == "bomb"
            else random.choice(FRUIT_COLORS)
        )

        self.fruits.append(fruit)

    def handle_event(self, event):
        if self.game_over:
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                for label, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        if label == "Exit":
                            self.exit_requested = True
                        else:
                            self.difficulty = label
                            self.replay_requested = True
                        return
            return

        if event.type == pygame.MOUSEMOTION:
            self._handle_motion(event.pos)

    def _handle_motion(self, pos):
        previous_pos = self.previous_mouse_pos
        x, y = pos

        for fruit in self.fruits:
            if fruit.sliced:
                continue

            if previous_pos is None:
                hit = fruit.contains_point(x, y)
            else:
                hit = fruit.intersects_segment(
                    previous_pos[0],
                    previous_pos[1],
                    x,
                    y,
                )

            if hit:
                self._slice(fruit)

        self.previous_mouse_pos = pos
        self.trail.append(pos)

        if len(self.trail) > 15:
            self.trail.pop(0)

    def _slice(self, fruit):
        if fruit.sliced:
            return

        fruit.sliced = True

        if fruit.kind == "bomb":
            self._play_sound("bomb")
            self.game_over = True
        else:
            self.score += 1
            self._play_sound("fruit")

    # --------------------------------------------------
    # GAME UPDATE
    # --------------------------------------------------

    def handle_input(self):
        pass

    def update(self):
        if self.game_over:
            return

        self._spawn_timer += 1

        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0
            self.spawn_fruit()

        remaining = []

        for fruit in self.fruits:
            fruit.update()

            if fruit.sliced:
                continue

            if fruit.off_screen(self.height):
                if fruit.kind == "fruit":
                    self.lives -= 1
                continue

            remaining.append(fruit)

        self.fruits = remaining

        if self.lives <= 0:
            self.game_over = True

    # --------------------------------------------------
    # RENDERING
    # --------------------------------------------------

    def render(self, screen):
        for fruit in self.fruits:
            pygame.draw.circle(
                screen,
                getattr(fruit, "color", WHITE),
                (int(fruit.x), int(fruit.y)),
                fruit.radius,
            )

        if len(self.trail) >= 2:
            pygame.draw.lines(
                screen,
                WHITE,
                False,
                self.trail,
                3,
            )

        score_text = self.font.render(
            f"Score: {self.score}", True, WHITE
        )
        lives_text = self.font.render(
            f"Lives: {self.lives}", True, WHITE
        )

        screen.blit(score_text, (10, 10))
        screen.blit(
            lives_text,
            (self.width - 130, 10),
        )

        if self.game_over:
            if not self._game_over_sound_played:
                self._play_sound("game_over")
                self._game_over_sound_played = True

            self._render_game_over(screen)

    def _render_game_over(self, screen):
        overlay = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA,
        )
        overlay.fill((0, 0, 0, 210))
        screen.blit(overlay, (0, 0))

        title = self.title_font.render(
            "GAME OVER", True, (255, 90, 90)
        )
        score = self.font.render(
            f"Final Score: {self.score}",
            True,
            WHITE,
        )
        prompt = self.font.render(
            "Choose a difficulty to play again",
            True,
            WHITE,
        )

        screen.blit(
            title,
            title.get_rect(
                center=(self.width // 2, 175)
            ),
        )
        screen.blit(
            score,
            score.get_rect(
                center=(self.width // 2, 235)
            ),
        )
        screen.blit(
            prompt,
            prompt.get_rect(
                center=(self.width // 2, 290)
            ),
        )

        colors = {
            "Easy": (50, 155, 75),
            "Medium": (45, 110, 200),
            "Hard": (205, 75, 55),
            "Exit": (90, 90, 90),
        }

        mouse_pos = pygame.mouse.get_pos()

        for label, rect in self.buttons.items():
            color = colors[label]

            if rect.collidepoint(mouse_pos):
                color = tuple(
                    min(c + 25, 255) for c in color
                )

            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=8,
            )

            text = self.button_font.render(
                label, True, WHITE
            )
            screen.blit(
                text,
                text.get_rect(center=rect.center),
            )
