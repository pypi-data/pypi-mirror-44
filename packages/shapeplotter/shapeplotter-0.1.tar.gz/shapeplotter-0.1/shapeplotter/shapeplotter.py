import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, grid=(1, 1, 1)):
        self.grid = grid
        self.wire = []
        self.fig = 0
        self.ax = 0

    @staticmethod
    def __restartplot(self):
        plt.clf()
        plt.cla()
        plt.close()

    def addwire(self, geom):
        print(geom.geom_type)
        if geom.geom_type == "Point":
            raise Exception('Cannot wire plot a Point')
        elif geom.geom_type == "LineString":
            x = []
            y = []
            for points in list(geom.coords):
                x.append(points[0])
                y.append(points[1])
            self.wire.append([x, y])
        elif geom.geom_type == "LinearRing":
            x = []
            y = []
            for points in list(geom.coords):
                x.append(points[0])
                y.append(points[1])
            self.wire.append([x, y])
        elif geom.geom_type == "Polygon":
            x, y = geom.exterior.xy
            self.wire.append([x, y])
        else:
            for g in geom:
                self.addwire(g)

    def plot(self, restart=True):
        if restart:
            self.__restartplot(self)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(*self.grid)
        for element in self.wire:
            self.ax.plot(element[0], element[1])
        plt.show()
        if restart:
            self.__restartplot(self)

