import pandas as pd
import bokeh
import numpy as np
from bokeh.plotting import figure, show, output_file
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
import matplotlib

image_path = "/home/maarten/Downloads/img_align_celeba/"
identity_path = "identities.txt"

df = pd.read_csv(identity_path, header=None, sep=" ")
df.columns = ["image", "identity"]
identities = df["identity"].unique()


class GUI():
    def __init__(self):
        self.n_same = 2
        self.n_columns = 6
        self.n_rows = 3
        self.n_frames = int(self.n_columns*self.n_rows)
        self.figure_i = [None]*self.n_frames
        self.files = None
        self.fig, self.ax = plt.subplots(self.n_rows, self.n_columns, figsize=(15,15))
        self.ax_list = []
        self.n_correct = 0
        self.first_time = True
        
    def draw_images(self):
        n_pictures = self.n_frames
        n_same = self.n_same
        to_draw = n_pictures - n_same
    
        # def draw
        # Get duplicate
        found = False
        while not found:
            duplicate = np.random.choice(identities, 1)[0]
            if df[df["identity"] == duplicate].shape[0] > self.n_same:
                found = True
                
        others = np.random.choice(identities, to_draw).tolist()
    
        # Get IDs
        correct_answers = df[df["identity"] == duplicate]["image"].sample(2).values.tolist()
        wrong_answers = []
        for p in others:
            file = df[df["identity"] == p]["image"].sample(1).values[0]
            wrong_answers += [file]
        all_answers = wrong_answers + correct_answers
        random.shuffle(all_answers)
        
        # Answers
        self.answer_indices = []
        for c in correct_answers:
            self.answer_indices += [all_answers.index(c) + 1]
        print(self.answer_indices)
        
        self.fig.suptitle(f"First answer: {self.answer_indices[0]}")
        # Get answers
        self.files = ["/home/maarten/Downloads/img_align_celeba/" + f for f in all_answers]
        
    def paint_images(self):
        im = 1
        for i in range(1, self.n_rows + 1):
            for j in range(1, self.n_columns + 1):
                # From 0,1,...,24
                # Create new axes
                if self.first_time:
                    ax = self.fig.add_subplot(self.n_rows, self.n_columns, im)
                    self.ax_list += [ax]
                else:
                    ax = self.ax_list[im - 1]
                    

                img = mpimg.imread(self.files[im - 1])
                ax.imshow(img)
                # ax.axes.get_yaxis().set_visible(False)
                # ax.axes.get_xaxis().set_visible(False)
                plt.text(0, 0, im)

                ax.set_xticks([])
                ax.set_yticks([])

                self.fig.canvas.draw()

                im += 1

        self.first_time = False
        
    def callback(self, event):
        if event.inaxes is not None:
            c = 1
            for ax in ax_list:
                if event.inaxes == ax:
                    print("answer: " ,c)
                    # We've got the picture number. Check if correct. If so, paint green.
                    if c in self.answer_indices:
                        self.answer_indices.remove(c)
                        self.n_correct += 1
                        print("correct")
                        if self.n_correct == self.n_same:
                            print("draw new")
                            # self.fig.clf()
                            self.draw_images()
                            self.paint_images()
                            self.fig.canvas.draw()
                            self.n_correct = 0
                            plt.axis("off")
                c += 1

    def run(self):
        self.fig.canvas.mpl_connect('button_press_event', self.callback)
        plt.show()

gui = GUI()
gui.draw_images()
gui.paint_images()
ax_list = gui.ax_list

# Run
gui.run()



