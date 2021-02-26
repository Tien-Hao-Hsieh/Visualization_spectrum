#bin/python
import pyfits
from numpy import *
from pylab import *
from astropy.constants import c
from Radiative_n2hp import *
from scipy.optimize import curve_fit


mom0=nan_to_num(pyfits.getdata('../Moment0/IRAS16253_mom0.fits')[0][0])
noi=loadtxt('../Moment0/Noise/Noise_table',usecols=[1])
SN=7
Mask=ones(shape(mom0));Mask[mom0<SN*noi]=0
#imshow(mom0,interpolation=None)
#contour(Mask,levels=[0.5])
#show()

FITS='../To_brightness_temperature/IRAM30m.Tbrightness.fits'
fits=pyfits.open(FITS)
data=fits[0].data[0]
header=fits[0].header


#BMAJ=header['BMAJ']*60*60
#BMIM=header['BMIN']*60*60
#BPA=header['BPA'] #from north to west (clockwise)
#RestFre=header['RESTFRQ']
RestFre=HFS[0][4]*10**9
RefFre=header['CRVAL3']
CDELT_F=header['CDELT3']
RefPix=header['CRPIX3']
N_Fre=header['NAXIS3']

#Fre_li=arange(RefFre-CDELT_F*(RefPix-1),RefFre+CDELT_F*(-RefPix+N_Fre+0.5),CDELT_F)
#Vel_li=( RestFre-Fre_li )/RestFre*(c/10**5)
Vel_li=arange(RefFre-CDELT_F*(RefPix-1),RefFre+CDELT_F*(-RefPix+N_Fre+0.5),CDELT_F)/10**3	# m to km/s

sh=shape(data)
output=nan*ones((sh[1],sh[2],4))
output2=nan*ones((sh[1],sh[2],4))
Chi_output=nan*ones((sh[1],sh[2]))

#data=data*Mask

print 'Start Fitting'
for y in arange(sh[2]):
   print '%.0f'%(float(y)/sh[2]*100),'%'
   for x in arange(sh[1]):
	if Mask[y][x]==0:continue
	spe=data[:,y,x]
	spe=nan_to_num(spe)
	
	p0=[6.0,0.55,4.0,0.11]
	popt, pcov = curve_fit(Tmb_all, Vel_li, spe, p0=p0,maxfev=5000)


#	Tex=[popt[0], sqrt(diagonal(pcov)[0])]
#	Tau=[popt[1], sqrt(diagonal(pcov)[1])]
#	Vlsr=[popt[2], sqrt(diagonal(pcov)[2])]
#	delV=[popt[3], sqrt(diagonal(pcov)[3])]

	step(Vel_li,spe,c='#8E8E8E',lw=2,where='mid')
	v_li=arange(Vel_li[0],Vel_li[-1],0.005)
	plot(v_li,Tmb_all(v_li,popt[0],popt[1],popt[2],popt[3]),c='r',lw=1)
	xlim(-10,15);xlabel(r'$V_{\rm LSR}\rm (km~s^{-1})$')
#	show()
#	close()
	chi=sum( (spe-Tmb_all(Vel_li,popt[0],popt[1],popt[2],popt[3]))**2 )
	Chi_output[y][x]=chi

	
	output[y][x]=popt
	output2[y][x]=sqrt(diagonal(pcov))
save('Chi2',Chi_output)
output=asarray(output)
save('Output_HFSfitting',output)
output2=asarray(output2)
save('Output_HFSfitting_err',output2)

#show()
