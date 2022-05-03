import numpy as np
import matplotlib.pyplot as plt
import seekr2.modules.common_base as base
import matplotlib.animation as animation

import plotting

title = "Entropy Barrier System"
model_file = "/home/lvotapka/toy_seekr_systems/entropy_barrier/model.xml"
model = base.load_model(model_file)
boundaries = np.array([[-1.0, 1.0], [-1.0, 1.0]])
toy_plot = plotting.Toy_plot(model, title, boundaries)
milestone_cv_functions = ["value"]

plotting.draw_linear_milestones(toy_plot, milestone_cv_functions)
ani = toy_plot.animate_trajs(animating_anchor_indices=[0, 1, 2, 3, 4, 5, 6])
#plt.show()

movie_filename = "entropy_barrier.mp4" 
writervideo = animation.FFMpegWriter(fps=60) 
ani.save(movie_filename, writer=writervideo)
