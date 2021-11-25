import matplotlib.pyplot as plt
import numpy as np


def normal_distribution(mu=0.5, sigma=0.1, nums=1000, print_graph=True):
    print(" normal distribution -  mu= " + str(mu) + " sigma= " + str(sigma) + " nums= " + str(nums))

    s = np.random.normal(mu, sigma, nums)
    if print_graph:
        print(s)
        # Create the bins and histogram
        count, bins, ignored = plt.hist(s, int(nums / 4), density=True)

        # Plot the distribution curve
        plt.plot(bins, 1 / (sigma * np.sqrt(2 * np.pi)) *
                 np.exp(- (bins - mu) ** 2 / (2 * sigma ** 2)), linewidth=3, color='y')
        plt.show()
    return s


def triangular_distribution(left=-3, mode=0, right=8, nums=100000, print_graph=True):
    print(" triangular distribution -  left= " + str(left) + " mode= " + str(mode) + " right= " + str(right) + " nums= " +\
          str(nums))
    s = np.random.triangular(left, mode, right, nums)

    if print_graph:
        print(s)
        count, bins, ignored = plt.hist(s, bins=200, density=True)
        plt.show()
    return s


def exponential_distribution(scale=1.0, nums=10000, print_graph=True):
    print(" exponential distribution -  scale= " + str(scale) + " nums= " + str(nums))
    s = np.random.exponential(scale, size=nums)
    if print_graph:
        print(s)
        count, bins, ignored = plt.hist(s, bins=200, density=True)
        plt.show()
    return s


def uniform_distribution(low=0.0, high=1.0, size=10000, print_graph=True):
    print(" uniform distribution -  low= " + str(low) + " high= " + str(high) + " size= " + str(size))
    s = np.random.uniform(low, high, size)
    if print_graph:
        print(s)
        count, bins, ignored = plt.hist(s, bins=200, density=True)
        plt.plot(bins, np.ones_like(bins), linewidth=2, color='r')
        plt.show()
    return s
# normal_distribution()
# triangular_distribution(180, 210, 230)
# exponential_distribution()

# uniform_distribution()
