from matplotlib import pyplot as plt

class FitnessPlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.avg_history = []
        self.best_history = []
        self.worst_history = []
        self.avg_line, = self.ax.plot([], [], label='Average Fitness')
        self.best_line, = self.ax.plot([], [], label='Best Fitness')
        self.worst_line, = self.ax.plot([], [], label='Worst Fitness')

    def init(self):
        plt.xlabel("Epoch")
        plt.ylabel("Fitness")
        plt.legend()
        plt.ion()


    def update(self, epoch, avg_fitness, best_fitness, worst_fitness):
        self.avg_history.append(avg_fitness)
        self.best_history.append(best_fitness)
        self.worst_history.append(worst_fitness)

        self.avg_line.set_data(range(len(self.avg_history)), self.avg_history)
        self.best_line.set_data(range(len(self.best_history)), self.best_history)
        self.worst_line.set_data(range(len(self.worst_history)), self.worst_history)

        self.ax.relim()
        self.ax.autoscale_view()

        plt.pause(0.05)

    def finalize(self):
        plt.ioff()
        plt.show()

class HitmapPlot:
    def __init__(self, title):
        self.data_list = []
        self.title = title

    def append(self, data):
        self.data_list.append(data)

    def show(self, color, has_colorbar=False, has_min_limit=False):
        plt.matshow(self.data_list, cmap=plt.get_cmap(color))
        if has_colorbar:
            plt.colorbar(shrink=0.8, aspect=10)
        if has_min_limit:
            plt.clim(vmin=0)
        plt.title(self.title)
        plt.savefig(f'{self.title}.png')