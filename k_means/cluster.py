import numpy as np
import matplotlib.pyplot as plt
import random

n = 4


def clust():
    x0 = random.random() * 10
    y0 = random.random() * 10
    return np.random.normal((x0, y0), 1, (300, 2))


def numclust(k):
    return np.concatenate([clust() for i in range(k)])


data = numclust(n)
rows = random.sample(range(data.shape[0]), n)
centroids = data[rows]


def plotting(data, centroids, clusters):
    clrs = ('r', 'm', 'black', 'blue')
    plt.scatter(data[:, 0], data[:, 1], c=[clrs[c] for c in clusters], s=5)
    plt.scatter(centroids[:, 0], centroids[:, 1], s=500, c=clrs, marker='*', edgecolors='c')
    plt.show()


def distances(data, centroids):
    sum = [np.sum(((data - centroid) ** 2), axis=1).reshape((-1, 1)) for centroid in centroids]
    return np.concatenate(sum, axis=1)


def smdist(distances):
    return distances.argmin(axis=1)


small = np.array([])

while True:
    prev = small.copy()
    small = smdist(distances(data, centroids))
    if np.all(prev == small):
        break

    for i in range(n):
        centroids[i] = np.average(data[small == i], axis=0)

    plotting(data, centroids, small)

# print(distances(data,centroids).shape)
