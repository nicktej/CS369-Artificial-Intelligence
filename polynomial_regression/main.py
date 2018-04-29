import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error


# generates data
def generate(n):
    coefficient = []
    data = []
    # generates the coefficients
    for i in range(5):
        coefficient.append(np.random.uniform(low=-0.5, high=0.5))
    for i in range(n):
        # generates the noise
        noise = np.random.normal(loc=0, scale=1, size=1)
        z = noise[0]
        x = np.random.uniform(low=-2.0, high=2.0)
        y = coefficient[0] * x ** 4 + coefficient[1] * x ** 3 + coefficient[2] * x ** 2 + coefficient[3] * x ** 1 + \
            coefficient[4]
        y_n = coefficient[0] * x ** 4 + coefficient[1] * x ** 3 + coefficient[2] * x ** 2 + coefficient[3] * x ** 1 + \
              coefficient[4] + z
        data.append([x, y, y_n])
    xs = [x[0] for x in data]
    ys = [x[1] for x in data]
    y_ns = [x[2] for x in data]
    xa = np.asarray(xs).reshape(n, -1)
    ya = np.asarray(ys).reshape(n, -1)
    yn = np.asarray(y_ns).reshape(n, -1)
    return xa, ya, yn


# graphs the single run
def graph():
    for n in (10, 100, 1000):
        x, y, yn = generate(n)
        # the points on the graph (with noise)
        plt.scatter(x, yn, s=2, c='m', label="Training Data")
        # the polynomial regression curves
        for style, width, degree, label in (
                ("g--", 1, 20, "20 Degrees"), ("b--", 1, 2, "2 Degrees"), ("r--", 1, 1, "1 Degrees"),
                ("y-", 1, 4, "True")):
            poly_features = PolynomialFeatures(degree=degree)
            X_poly = poly_features.fit_transform(x)
            lin_reg = LinearRegression()
            lin_reg.fit(X_poly, yn)
            X_new = np.linspace(-3, 3, 1000).reshape(1000, 1)
            X_new_poly = poly_features.transform(X_new)
            y_new = lin_reg.predict(X_new_poly)
            plt.plot(X_new, y_new, style, linewidth=width, label=label)
        plt.xlabel("$x_1$")
        plt.title("Graph of " + str(n) + " training points")
        plt.ylabel("$y$", rotation=0)
        plt.legend(loc="upper left")
        plt.ylim(-10, 10)
        plt.show()


# average mse
def amse():
    for points in (10, 100, 1000):
        ndeg = 21
        runs = 100
        train_mse = [0] * ndeg
        test_mse = [0] * ndeg
        for run in range(runs):
            creation = create(4)
            tx = 4 * np.random.random((points, 1)) - 2
            ty = np.array([creation(x) + np.random.normal() for x in tx])
            testx = np.linspace(-2, 2, 100)
            testy = np.array([creation(x) for x in testx])
            # fit the polynomial for degree 0
            fit = sum(ty) / len(ty)
            train_mse[0] = mean_squared_error(ty, [fit] * len(ty))
            test_mse[0] = mean_squared_error(testy, [fit] * len(testy))
            # fits for degrees 1 to 20
            for deg in range(1, ndeg):
                fit = fit_polynomial(tx, ty, deg)
                tfy = np.array([fit(x) for x in tx])
                testfy = np.array([fit(x) for x in testx])
                train_mse[deg] += mean_squared_error(ty, tfy) / runs
                test_mse[deg] += mean_squared_error(testy, testfy) / runs
        # plots the graph
        plt.plot(range(ndeg), train_mse, label="Training")
        plt.plot(range(ndeg), test_mse, color="red", label="Testing")
        plt.title("AMSE for " + str(points) + " Points")
        plt.xlabel("Degrees")
        plt.xticks(np.arange(0, ndeg, step=1))
        plt.ylabel("AMSE")
        plt.ylim(0, 10)
        plt.legend()
        plt.show()


# receives training data and the degree. returns a function.
def fit_polynomial(tx, ty, degree):
    if degree == 0:
        return lambda x: sum(ty) / len(ty)
    poly_features = PolynomialFeatures(degree=degree, include_bias=False)
    X_poly = poly_features.fit_transform(tx)
    lin_reg = LinearRegression()
    lin_reg.fit(X_poly, ty)
    coefficients = np.insert(lin_reg.coef_, 0, lin_reg.intercept_)
    return create(2, coefficients)


# creates a function
def create(degree, coefficients=np.zeros((1, 1))):
    if not coefficients.any():
        coefficients = np.random.random(degree) - 0.5
    return lambda x: sum([a * x ** i for i, a in enumerate(coefficients)])


# run
graph()
amse()
