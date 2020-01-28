---
layout: post
title:  "Tip: use 'ffmpeg-python' to create your movie"
categories: [Python]
---

[ffmpeg-python](https://github.com/kkroening/ffmpeg-python) is a great wrapper around *ffmpeg* to create your movie from Python.

Let us begin by setting up an environment that contains what we need: 

```
conda activate myenv
conda install -c conda-forge ffmpeg-python
conda install -c conda-forge matplotlib
```

(see [Conda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) on how to manage environments).

Then, we will create an animation as a batch of images:

```python
import matplotlib.pyplot as plt

filenames = []

for i in range(20):

    filename = 'image_{0:02d}.png'.format(i)
    filenames += [filename]

    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, i])
    ax.set_ylim([0, 20])
    plt.savefig(filename)
```

To convert this to a movie, we will use *ffmpeg-python*:

```python
import ffmpeg

(
    ffmpeg
    .input('image_%02d.png', framerate=2)
    .output('movie.mp4')
    .run()
)
```
