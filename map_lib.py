class AddFigures:
    def __init__(self, figures):
        self.figures = figures
    def circle(self, center, radius, color=(225, 225, 225)):
        circle_ = {
            'type': 'circle',
            'center': center,
            'radius': radius,
            'color': color
        }
        self.figures.append(circle_)

    def line(self, start, end, color=(225, 225, 225)):
        line_ = {
            'type': 'line',
            'start': start,
            'end': end,
            'color': color
        }
        self.figures.append(line_)
    def hide_box(self, points, connects, color=(225, 225, 225)):
        hide_box_ = {
            'type': 'hide_box',
            'points': points,
            'connects': connects,
            'color': color
        }
        self.figures.append(hide_box_)
    def figure(self, points, connects, color=(225, 225, 225)):
        figure_ = {
            'type': 'figure',
            'points': points,
            'connects': connects,
            'color': color
        }
        self.figures.append(figure_)

class Map:
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.figures = []

    def add(self):
        return AddFigures(self.figures)

