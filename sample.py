from EMD import EMD
import numpy  as np
import scipy.io
from scipy import interpolate
import pylab as plt
import math
from sequence import Point, dist, Sequence

User1_path = "data/anil/log1.txt"
User2_path = "/home/prerit/Documents/BTP/data/arvind/log1.txt"
f1 = open(User1_path,'r')
f2 = open(User2_path,'r')

t_prev = 0
s1 = Sequence()
for value in f2.readlines()[11971:12050]:
	v = value.split(", ")
	if int(v[3]) is not 0:
		s1.add_p(Point(int(v[1]),int(v[2])),t_prev)
		print Point(int(v[1]),int(v[2])).x , Point(int(v[1]),int(v[2])).y
		t_prev = t_prev+int(v[3])

[s,t] = s1.get_sig()
s = np.array(s,np.float)
t = np.array(t,np.float)
print type(s),type(t)
#for z in zip(s,t):
#	print z
#data2 = f2.readlines()[10:69]
#scipy.io.savemat('user1.mat', dict(x=x, y=y))

plt.figure()
[p,t1] = s1.get_p()
x = [pp.x for pp in p]
y = [pp.y for pp in p]
plt.plot(x,y,'b',label ="Actual Trajectory")
plt.plot([x[0],x[-1]],[y[0],y[-1]],'go')
plt.plot([x[0],x[-1]],[y[0],y[-1]],'r--',label="Shortest Path")
plt.text(x[0],y[0], "(%i,%i) Start" %(int(x[0]),int(y[0])))
plt.text(x[-1],y[-1], "(%i,%i) End" %(int(x[-1]),int(y[-1])))
plt.xlabel("X-axis on screen")
plt.ylabel("Y-axis on screen")
#plt.title("Mouse_movement sequence")
#plt.title("User 2 : mouse signal trajectory")
plt.legend(loc='upper right')
plt.show()

# Execute EMD on signal
S = s
print type(S)
eIMFs = EMD().emd(S, t)
nIMFs = eIMFs.shape[0]
print eIMFs.shape
print s

"""
##### Retrieval #############
p1 = s1.get_start()
p2 = s1.get_end()
slope = (p2.y - p1.y)/(p2.x - p1.x)
cosx = -(p2.x - p1.x)/dist(p2,p1)
sinx = (p2.y - p1.y)/dist(p2,p1)
ret = eIMFs[1:].sum(axis=0)
print "Retrieved"
print ret
[val,t1] = s1.get_p()

for i in range(len(val)):
    val[i].x = val[i].x - eIMFs[0][i]*cosx
    val[i].y = val[i].y - eIMFs[0][i]*sinx

plt.figure()
x = [pp.x for pp in val]
y = [pp.y for pp in val]
plt.plot(x,y,'b',label ="Actual Trajectory")
plt.plot([x[0],x[-1]],[y[0],y[-1]],'go')
plt.plot([x[0],x[-1]],[y[0],y[-1]],'r--',label="Shortest Path")
#plt.text(x[0],y[0], "(%i,%i) Start" %(int(x[0]),int(y[0])))
#plt.text(x[-1],y[-1], "(%i,%i) End" %(int(x[-1]),int(y[-1])))
plt.xlabel("X-axis on screen")
plt.ylabel("Y-axis on screen")
plt.title("User 2 : mouse signal trajectory")
plt.legend(loc='upper right')
plt.show()
"""

"""
# Plot results
plt.figure(figsize=(12,9))
plt.subplot(nIMFs+1, 1, 1)
plt.plot(t, S, 'r')
plt.title("User 1 : Emperical Mode Decomposition")
plt.ylabel("Signal")
for n in range(nIMFs):
    plt.subplot(nIMFs+1, 1, n+2)
    plt.plot(t, eIMFs[n], 'g')
    if n == (nIMFs - 1):
    	plt.ylabel("Residue")
    else:
    	plt.ylabel("eIMF %i" %(n+1))
    plt.locator_params(axis='y', nbins=5)

plt.xlabel("Time [ms]")
plt.tight_layout()
plt.show()
"""
#e = eIMFs[2]



mean = np.zeros(nIMFs-1)
var = np.zeros(nIMFs-1)
entropy = np.zeros(nIMFs-1)

for i in range(nIMFs - 1):
    """
    e = eIMFs[i]
    flinear = interpolate.interp1d(t1, e)
    fcubic = interpolate.interp1d(t1, e, kind='cubic')

    xnew = np.linspace(t1[0], t1[-1], 40)
    x_normal = np.linspace(0,1,40)
    ylinear = flinear(xnew)
    ycubic = fcubic(xnew)

    """
    """
    plt.plot(t1, e, 'X', label = "Non-uniform sampled signal")
    plt.plot(xnew, ycubic, 'o', label = "Sampled points after interpolation")
    plt.title("eIMF2 : Sampling after cubic spline interpolation")
    plt.legend(loc = "upper right")
    plt.xlabel("t (in ms)")
    plt.ylabel("IMF value")
    plt.show()

    plt.plot(x_normal, ycubic, 'o', label = "Sampled points")
    plt.title("eIMF2 : Signal with normalized range")
    plt.legend(loc = "upper right")
    plt.xlabel("t (in ms)")
    plt.ylabel("IMF value")
    plt.show()
    """
    """
    y = ycubic
    x = x_normal
    
    #print y.shape,x.shape
    #print np.sum(y)
    mean[i] = np.sum(y)/len(y)
    #print mean.shape
    y_sq = np.sum([y_*y_ for y_ in y])
    var[i] = y_sq/len(y) - mean[i]*mean[i]
    ent = 0
    for j in range(len(y)):
        quo = (y[j]*y[j])/y_sq
        ent = ent + quo*math.log(quo)/math.log(10)
    entropy[i] = -ent/(math.log(len(y))/math.log(10))
    #print mean[0][i],var[0][i],entropy[0][i]
    print "Mean = %0.3f Var = %0.3f Entropy = %0.3f"%(float(mean[i]),float(var[i]),float(entropy[i]))
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    """

