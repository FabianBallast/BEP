import numpy as np
import matplotlib.pyplot as plt

a = 220
b = 675
c = 101
d = 5

plt.plot([5, 6], [0, 0], color='g')
plt.plot([6, 7], [0, 2*a], color='g')
plt.plot([7, 8], [2*a, (b+c)/2], color='g')
plt.plot([8, 9], [(b+c)/2, 2*d], color='g')
plt.plot([9, 10],[2*d, 0], color='g')

#plt.show()

data = [6.5]*a + [7.5]*b + [8.5]*c + [9.5]*d


from scipy.stats import norm

mu, std = norm.fit(data)

# Plot the histogram.
plt.hist(data, bins=5, range=[5, 10], density=False, alpha=0.6, color='g')


# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std) * 1000
plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
plt.title(title)

plt.show()





x = 7.95

print(1 - norm.cdf(x, mu, std))

tot = sum([a,b,c,d])

#boven 8
upwards = d+c


interp = (x-7) / 1 *((b+c)/2 - (2*a))  + a*2

print('interp', interp)
lastpart = (1-(x-7)) * (interp + (b+c)/2)/2
print('lastpart', lastpart)

tot_upwards = upwards+lastpart

print("linear:", tot_upwards/tot)