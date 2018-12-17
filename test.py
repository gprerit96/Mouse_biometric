from EMD import EMD
import numpy  as np
import pylab as plt

# Define signal
t = np.linspace(0, 1, 200)

sin = lambda x,p: np.sin(2*np.pi*x*t+p)
S = 3*sin(18,0.2)*(t-0.2)**2
S += 5*sin(11,2.7)
S += 3*sin(14,1.6)
S += 1*np.sin(4*2*np.pi*(t-0.8)**2)
S += t**2.1 -t
s = S
# Execute EMD on signal
IMF = EMD().emd(s,t)
N = IMF.shape[0]+1
print IMF.shape
imf = sum(IMF)
print imf.shape
plt.figure(figsize=(12,9))
plt.subplot(N, 1, 1)
plt.plot(t, imf, 'r')
plt.show()


# Plot results
"""
plt.figure(figsize=(12,9))
plt.subplot(N, 1, 1)
plt.plot(t, s, 'r')

for n in range(N-1):
    plt.subplot(N, 1, n+2)
    plt.plot(t, IMF[n], 'g')
    plt.ylabel("IMF %i" %(n+1))
    plt.locator_params(axis='y', nbins=5)

plt.xlabel("Time [s]")
plt.tight_layout()
plt.savefig('simple_emd_1', dpi=120)
plt.show()
"""