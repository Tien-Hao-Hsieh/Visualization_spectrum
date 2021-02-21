#! bin/python
from numpy import *
from astropy.constants import c, k_B, h
#from pylab import *

c=c.cgs.value
k_B=k_B.cgs.value
h=h.cgs.value
Tbg=2.73

HFS=rot90(loadtxt('Functions/nh3_hfs_Pagani07'))[::-1]
RestFre=HFS[0][0]		# in GHz (shall be insert in Image.py when doing clean
print 'nu=',RestFre
HFS_v=HFS[:,1:]	# in cgs (cm/s)

nu=RestFre*10**9	# in Hz

def Gaussian(x,vlsr,sig):
#        sig=delV/(2*(2*log(2))**0.5)
        G=e**(-(x-vlsr)**2/(2*sig**2))
        return G

def J(Tex):
	J=(h*nu)/k_B * 1/(exp( h*nu/(k_B*Tex) )-1)
	return J

def Tmb(Tex,tau):
	T = ( J(Tex)-J(Tbg) ) * (1-exp(-tau))
	return T

def Tmb_all(v,Tex,tau,vlsr,sig):
	tau_v=zeros(len(v))
	for i in arange(len(HFS_v[0])):
		v_km=HFS_v[0][i]	# To km/s
		com=HFS_v[1][i]		
		tau_v += tau*com*Gaussian(v,vlsr+v_km,sig)  # tau normalize to the first (lowest) component, might change if edit hfs file
	out=Tmb(Tex,tau_v)
	return out
#v=arange(-20,20,0.1)
#plot(v,Tmb_all(v,5,0.5,0,0.1))
#show()
