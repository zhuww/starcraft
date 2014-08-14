import matplotlib
import matplotlib.pyplot as plt
from numpy import array
N = lambda t:6 + int(t/17)
Ni = lambda t:6 + (t/17.)
m = lambda t:N(t) * (5 * int(t/7.7)) + 50 - 50*(N(t) - 5)
t = array(range(1500))/10.
#plt.plot([Ni(x) for x in t], [m(x) for x in t])
#plt.show()
Mrate = lambda N: N*5/7.7*60
print Mrate(15)
print Mrate(16)
