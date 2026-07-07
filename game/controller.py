import pygame

from game import Game
from renderer import Renderer


class GameController:
    def __init__(self, game: Game, renderer: Renderer) -> None:
        self.game = game
        self.renderer = renderer
        self.running = False
        self.clock = pygame.time.Clock()

    def start_game(self) -> None:
        self.game.initialize()

        self.game.state.clock.is_running = True
        self.running = True

        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(60)

        pygame.quit()

    def update(self) -> None:
        dt = self.clock.get_time() / 1000

        active_color = self.game.state.current_color
        self.game.state.clock.tick(active_color, dt)

        if self.game.state.clock.has_flagged(active_color):
            print(f"Game Over! {active_color.opposite.value} wins on time.")
            self.running = False
            return

    def draw(self) -> None:
        self.renderer.draw(self.game)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
