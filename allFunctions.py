import random


def generate_colors(nb_colors):
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
              for i in range(nb_colors)]
    return colors
