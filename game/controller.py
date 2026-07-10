import pygame

from chess_types import Color, Coordinate, HighlightType
from game import Game
from renderer import Renderer

NORMAL_CURSOR = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
GRAB_CURSOR = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)


class GameController:
    def __init__(self, game: Game, renderer: Renderer) -> None:
        self.game = game
        self.renderer = renderer
        self.running = False
        self.clock = pygame.time.Clock()
        self.selected_square: Coordinate | None = None

    def start_game(self) -> None:
        self.game.initialize()

        self.game.state.clock.is_running = True
        self.running = True

        while self.running:
            self.handle_events()
            self.handle_hover()
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
        self.renderer.update_clock(
            self.game.state.clock.times[Color.WHITE],
            self.game.state.clock.times[Color.BLACK],
        )

        self.renderer.draw(self.game)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                square = self.renderer.mouse_to_square(pygame.mouse.get_pos())
                if square is None:
                    continue

                row, col = square

                if event.button == pygame.BUTTON_LEFT:
                    self._handle_square_click(row, col)

                elif event.button == pygame.BUTTON_RIGHT:
                    self.selected_square = None
                    self.renderer.highlight_square(row, col)

    def handle_hover(self) -> None:
        square = self.renderer.mouse_to_square(pygame.mouse.get_pos())
        hovering_piece = square is not None and self.game.board.has_piece(*square)

        pygame.mouse.set_cursor(GRAB_CURSOR if hovering_piece else NORMAL_CURSOR)

    def _handle_square_click(self, row: int, col: int) -> None:
        piece = self.game.board.get(row, col)
        self.renderer.clear_highlights(HighlightType.NORMAL)

        if self.selected_square is not None:
            to_row, to_col = row, col
            from_row, from_col = self.selected_square

            # Clicked the same square -> deselect
            if self.selected_square == (to_row, to_col):
                self._clear_selected_square()
                self.renderer.clear_highlights(HighlightType.SELECTED)
                return

            # Clicked a legal move: move
            legal_moves = self.game.legal_moves_from_square(from_row, from_col)
            legal_destinations = {move.end for move in legal_moves}

            if (to_row, to_col) in legal_destinations:
                self.game.move(from_row, from_col, to_row, to_col)
                self.renderer.highlight_move(from_row, from_col, to_row, to_col)
                self._clear_selected_square()
                return

            # Clicked another friendly piece: select that instead
            if piece and piece.color == self.game.state.current_color:
                self.selected_square = (to_row, to_col)
                self._render_selection_square(to_row, to_col)
                return

            # Invalid click: clear selection
            self._clear_selected_square()
            self.renderer.clear_highlights(HighlightType.SELECTED)

        else:
            # Nothing selected: select a piece
            if piece and piece.color == self.game.state.current_color:
                self.selected_square = (row, col)
                self._render_selection_square(row, col)

    def _render_legal_destinations(self, row: int, col: int) -> None:
        legal_moves = self.game.legal_moves_from_square(row, col)
        self.renderer.set_moves({move.end for move in legal_moves})

    def _render_selection_square(self, row: int, col: int) -> None:
        self._render_legal_destinations(row, col)
        self.renderer.highlight_selection(row, col)

    def _clear_selected_square(self) -> None:
        self.selected_square = None
        self.renderer.moves = set()
