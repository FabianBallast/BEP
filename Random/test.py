from pylab import *
from tikzplotlib import save as tikz_save
x = linspace(0, 10, 101)
plot(x, sin(x))
xlabel('$x$-axis')
ylabel('$y$-axis')
tikz_save('fig.tikz')