def calc_positions():
    positions = []
    for i in range(7):
        sx, sy = 23, 133
        h, w = 69, 169
        for j in range(3):
            x1 = sx
            y1 = sy
            x2 = x1 + w
            y2 = y1 + h

            positions.append((x1, y1, x2, y2))
            # for the next cell to the right
            sx = sx + 180

        sy = sy + 100
    
    return positions

# Example usage:
calculated_positions = calc_positions()
print(calculated_positions)
