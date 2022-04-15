import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seekr2.modules.common_base as base

import plotting

title = "Muller Potential System"
model_file = "/home/lvotapka/toy_seekr_systems/muller_potential_multi/model.xml"
model = base.load_model(model_file)
boundaries = np.array([[-1.75, 1.0], [-0.5, 2.0]])
toy_plot = plotting.Toy_plot(model, title, boundaries, stride=10)
milestone_cv_functions = ["x=value", "value"]
plotting.draw_linear_milestones(toy_plot, milestone_cv_functions)
ani = toy_plot.animate_trajs(animating_anchor_indices=[19, 20, 30, 31, 29, 18, 40, 39, 38, 28, 27, 37, 26, 17, 48, 49, 50, 47, 58, 46, 69, 57, 68, 80, 81, 70, 45, 56, 36, 35, 34, 25, 24, 23, 22, 33, 44, 82, 93, 92, 55, 66, 67, 77, 78, 79, 88, 89, 90, 91, 100, 99, 101, 102, 103, 104, 16, 15, 14, 13, 12, 11, 2, 3, 4, 5, 6, 7, 8, 1, 0, 51, 21, 32, 105, 94])
plt.show()

#movie_filename = "muller_potential_milestones.gif" 
#writergif = animation.ImageMagickWriter(fps=30) 
#ani.save(movie_filename, writer=writergif)

#movie_filename = "muller_potential_milestones.mp4" 
#writervideo = animation.FFMpegWriter(fps=60) 
#ani.save(movie_filename, writer=writervideo)
