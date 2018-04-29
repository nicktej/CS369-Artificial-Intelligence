from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cmx


# Load the data
def load():
    info = []
    with open('wine.data.txt') as input_file:
        for line in input_file:
            line = line.strip('\n')
            info.append(line.split(','))
        results = [list(map(float, lst)) for lst in info]
    return results


# Plot
def plot(results, x, y, z, w, colorsMap):
    attributes = ['type', 'alcohol', 'malic acid', 'ash', 'alcalinity of ash', 'magnesium', 'total phenols',
                  'flavanoids', 'phenols', 'proanthocyanins', 'color', 'hue', 'OD280/OD315', 'proline']
    cm = plt.get_cmap(colorsMap)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    a = []
    b = []
    c = []
    d = []
    length = len(results)
    for i in range(length):
        a.append(results[i][x])
        b.append(results[i][y])
        c.append(results[i][z])
        d.append(results[i][w])
    c_norm = matplotlib.colors.Normalize(vmin=min(d), vmax=max(d))
    scalar_map = cmx.ScalarMappable(norm=c_norm, cmap=cm)
    ax.set_xlabel(attributes[x])
    ax.set_ylabel(attributes[y])
    ax.set_zlabel(attributes[z])
    ax.set_title('3D Scatterplot on Wine')
    # ax = Axes3D(fig)
    ax.scatter(a, b, c, marker='o', c=scalar_map.to_rgba(d))
    scalar_map.set_array(w)
    fig.colorbar(scalar_map).set_label(attributes[w])
    plt.show()


if __name__ == '__main__':
    print('1:alcohol 2:malic acid 3:ash 4:alcalinity of ash 5:magnesium 6:total phenols 7:flavanoids 8:phenols '
          '9:proanthocyanins 10:color 11:hue 12:OD280/OD315 13:proline')
    while True:
        a = input('Enter 1st number (1-13, this is the x-axis): ')
        b = input('Enter 2nd number (1-13, this is the y-axis): ')
        c = input('Enter 3rd number (1-13, this is the z-axis): ')
        d = input('Enter 4th number (1-13, this is the color): ')
        flag = 0
        try:
            val = int(a)
            val = int(b)
            val = int(c)
            val = int(d)
            a = int(a)
            b = int(b)
            c = int(c)
            d = int(d)
            if 0 < a < 14 and 0 < b < 14 and 0 < c < 14 and 0 < d < 14:
                flag = 1
                break
        except ValueError:
            print("Incorrect entry, try again")
        if flag == 1:
            break
    result = load()
    plot(result, a, b, c, d, 'jet')
