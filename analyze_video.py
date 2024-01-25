import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import skvideo.io
import sys, os


def find_length_per_pixel(video):
    fig, ax = plt.subplots()
    fig.suptitle("Right and Left click on the uppermost and lowermost major divisions to set the scale of the video.")

    first_image = next(video)
    ax.imshow(first_image)
    top_line, = ax.plot([0, first_image.shape[1] - 1], [0, 0], linewidth=1)
    top_height = 0
    bottom_line, = ax.plot([0, first_image.shape[1] - 1], [0, 0], linewidth=1)
    bottom_height = 0

    def on_click(event):
        nonlocal top_height, bottom_height
        if event.button is MouseButton.LEFT:
            top_height = event.ydata
            top_line.set(ydata=[top_height, top_height])
        elif event.button is MouseButton.RIGHT:
            bottom_height = event.ydata
            bottom_line.set(ydata=[bottom_height, bottom_height])
        else:
            return
        fig.canvas.draw()

    binding_id = plt.connect('button_press_event', on_click)

    plt.show()

    plt.disconnect(binding_id)
    return 3e-3 / abs(top_height - bottom_height)


def get_blobs(image, threshold=0.5):
    return None

if __name__ == "__main__":
    path = sys.argv[1]
    video = skvideo.io.vreader(path)

    length_per_pixel = find_length_per_pixel(video)
    print(f"{length_per_pixel:.7f}")

    # blobs = []
    # video = skvideo.io.vreader(path)
    # for image in video:
    #     blobs.append(get_blobs(image))
