from EMD import EMD
import numpy  as np
import os,math
from scipy import interpolate
import pylab as plt
from sequence import Point, dist, Sequence

#allUsers = ['arvind', 'vikrant', 'anil', 'bishal', 'vishnu', 'pawan', 'pandu']
allUsers = ['bishal', 'vishnu', 'pawan', 'pandu']

def getNthVal(line, n):
	return int(line.split(", ")[n])

path1 = "data/"
path2 = "data2/"

for user in allUsers:
	u_path1 = path1 + user
	u_path2 = path2 + user
	for file in os.listdir(u_path1):
		f_path1 = u_path1 + '/' + file
		f_path2 = u_path2 + '/' + file
		print f_path2
		f1 = open(f_path1,'r')
		f2 = open(f_path2,'w')
		lines = f1.readlines()
		for line in lines[:9]:
			f2.write(line)
		flag = 1
		for line in lines[9:]:
			v = line.split(", ")
			if(v[0] == "MM"):
				if(flag):
					if int(v[3]) is not 0:
						s1 = Sequence([],[])
						#[s,t] = s1.get_sig()
						#print t
						t_prev = 0
						s1.add_p(Point(int(v[1]),int(v[2])),t_prev)
						flag = 0
						print(1)
				else:
					if int(v[3]) is not 0:
						t_prev = t_prev + int(v[3])
						s1.add_p(Point(int(v[1]),int(v[2])),t_prev)
						print(2)

			elif(v[0] == "MP" and flag == 0):
				print(3)
				flag = 1
				if(s1.get_size()>10):
					[s,t] = s1.get_sig()
					if (not s==[]):		
						s = np.array(s,np.float)
						t = np.array(t,np.float)
						print type(s),type(t)
						S = s
						print type(S)
						print S
						print t
						print len(S),len(t)
						eIMFs = EMD().emd(S, t)
						nIMFs = eIMFs.shape[0]
						print eIMFs.shape
						
						mean = np.zeros(nIMFs-1)
						var = np.zeros(nIMFs-1)
						entropy = np.zeros(nIMFs-1)

						for i in range(nIMFs - 1):
							e = eIMFs[i]
							#flinear = interpolate.interp1d(t1, e)
							fcubic = interpolate.interp1d(t, e, kind='cubic')
							xnew = np.linspace(t[0], t[-1], 40)
							x_normal = np.linspace(0,1,40)
							#ylinear = flinear(xnew)
							ycubic = fcubic(xnew)
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
							    quo = (y[i]*y[i])/y_sq
							    ent = ent + quo*math.log(quo)/math.log(10)
							entropy[i] = -ent
							#print mean[0][i],var[0][i],entropy[0][i]
							print "Mean = %0.3f Var = %0.3f Entropy = %0.3f"%(float(mean[i]),float(var[i]),float(entropy[i]))


						p1 = s1.get_start()
						p2 = s1.get_end()
						if((p2.x - p1.x) == 0):
							slope = 10000000
						else:
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
							if (i==0):
								f2.write("MM, "+"%0.3f"%(val[i].x)+", "+"%0.3f"%(val[i].y)+", "+str(t1[i])+"\n")
							else:
								f2.write("MM, "+"%0.3f"%(val[i].x)+", "+"%0.3f"%(val[i].y)+", "+str(t1[i]-t1[i-1])+"\n")
						print [(val[i].x,val[i].y) for i in range(len(val))]
				f2.write(line)
				del s1
				#print "Size of s1: %d"%(len(s1)) 

			else:
				f2.write(line)
				print(4)