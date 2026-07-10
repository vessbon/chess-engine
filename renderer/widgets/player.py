import pygame


class PlayerWidget:
    def __init__(
        self,
        position: tuple[int, int],
        font_path: str,
        username: str,
        anchor: str = "topright",
    ) -> None:
        self.position = position
        self.anchor = anchor
        self.font = pygame.font.Font(font_path, 24)
        self.username = username

        self.surface = pygame.Surface((110, 32))

    def draw(self, screen: pygame.Surface):
        rect = self.surface.get_rect()
        setattr(rect, self.anchor, self.position)

        self.surface.fill((64, 64, 64))

        text = self.font.render(self.username, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.surface.get_rect().center))

        self.surface.blit(text, text_rect)
        screen.blit(self.surface, rect)
