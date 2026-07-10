import pygame


def draw_smooth_circle(
    surface: pygame.Surface,
    center: tuple[int, int],
    radius: int,
    color: pygame.Color | tuple[int, int, int] | tuple[int, int, int, int],
    width: int = 0,
):
    """Draws a perfectly anti-aliased circle or ring using supersampling."""
    if radius <= 0:
        return

    scale = 4
    target_size = radius * 2
    temp_size = target_size * scale

    temp_surf = pygame.Surface((temp_size, temp_size), pygame.SRCALPHA)

    high_res_center = (temp_size // 2, temp_size // 2)
    high_res_radius = radius * scale
    high_res_width = width * scale

    pygame.draw.circle(
        temp_surf, color, high_res_center, high_res_radius, high_res_width
    )

    smooth_surf = pygame.transform.smoothscale(temp_surf, (target_size, target_size))

    top_left = (center[0] - radius, center[1] - radius)
    surface.blit(smooth_surf, top_left)
