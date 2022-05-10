from windows.windows import window


def edge_collision(rect):
    left = window.room_rect.left < rect.left
    right = window.room_rect.right > rect.right
    top = window.room_rect.top < rect.top
    bottom = window.room_rect.bottom > rect.bottom

    if left and right and top and bottom:
        return False
    else:
        return True
