from windows.windows import window
import pygame
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", 
        "resources", "cursors"
        )
    )

    
class NormalCursor:
    def __init__(self):
        # Image
        img = pygame.image.load(
            f"{resources_path}/normal_cursor.png")
        wd, ht = img.get_rect().size
        self.img = pygame.transform.scale(
            img, (wd * 2, ht * 2))

        # Rectangle
        self.rect = pygame.Rect(
            pygame.mouse.get_pos(),
            self.img.get_rect().size)

    def draw(self, display):
        if pygame.mouse.get_focused():  # checks if mouse is in the window
            display.blit(self.img, self.rect)
    
    def update(self):
        # Updates Cursor's Position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.x = (mouse_x / window.enlarge)
        self.rect.y = (mouse_y / window.enlarge)
