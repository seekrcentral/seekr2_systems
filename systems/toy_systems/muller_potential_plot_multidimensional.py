import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seekr2.modules.common_base as base

import plotting

title = "Muller Potential System"
model_file = "/home/lvotapka/toy_seekr_systems/muller_potential_multi/model.xml"
model = base.load_model(model_file)
boundaries = np.array([[-1.75, 1.0], [-0.5, 2.0]])
toy_plot = plotting.Toy_plot(model, title, boundaries, stride=2)
milestone_cv_functions = ["x=value", "value"]
plotting.draw_linear_milestones(toy_plot, milestone_cv_functions)
#ani = toy_plot.animate_trajs(animating_anchor_indices=[19, 20, 30, 18, 31, 21, 8, 9, 29, 28, 17, 39, 40, 38, 37, 50, 48, 27, 36, 25, 35, 46, 49, 57, 58, 68, 45, 69, 80, 70, 81, 7, 32, 41, 26, 56, 92, 93, 24, 82, 51, 23, 13, 2, 3, 4, 1, 5, 16, 12, 22, 33, 14, 34, 44, 0, 6, 11, 55, 15])
plt.show()

#movie_filename = "muller_potential_milestones.gif" 
#writergif = animation.ImageMagickWriter(fps=30) 
#ani.save(movie_filename, writer=writergif)

#movie_filename = "muller_potential_milestones.mp4" 
#writervideo = animation.FFMpegWriter(fps=60) 
#ani.save(movie_filename, writer=writervideo)
