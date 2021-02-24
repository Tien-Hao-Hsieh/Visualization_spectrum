#! bin/python
from numpy import *
from pylab import *
from astropy.io import fits as pyfits
import sys
sys.path.append('Functions/')
import Radiative_n2hp as n2hp_fun
import Radiative_nh3 as nh3_fun
from header import *
from astropy.constants import c
c=c.to('km/s').value

fac=2*(2*log(2.))**0.5
class Cursor():
    def __init__(self, ax):
        self.ax = ax
    def mouse_move(self, event):
        if not event.inaxes:
            return
        ra, dec = event.xdata, event.ydata

	x=argmin(abs(ra-ra_nh3))
	y=argmin(abs(dec-dec_nh3))
	ax2=axes([0.55,0.09,0.43,0.38])
	ax2.cla()
	spe=data[:,int(y),int(x)]
	ax2.step(Vel_li_nh3,spe,c='#8E8E8E',lw=2,where='mid')
	popt2=Fit_result[int(y),int(x)]
	error2=Fit_result_err[int(y),int(x)]
	ax2.plot(v_li,nh3_fun.Tmb_all(v_li,popt2[0],popt2[1],popt2[2],popt2[3]),c='r',lw=1)

	x=argmin(abs(ra-ra_n2hp))
	y=argmin(abs(dec-dec_n2hp))
	ax3=axes([0.55,0.59,0.43,0.38])
	ax3.cla()
	spe=data2[:,int(y),int(x)]
	ax3.step(Vel_li_n2hp,spe,c='b',lw=2,where='mid')
	popt3=Fit_result2[int(y),int(x)]
	error3=Fit_result_err2[int(y),int(x)]
	ax3.plot(v_li,n2hp_fun.Tmb_all(v_li,popt3[0],popt3[1],popt3[2],popt3[3]),c='r',lw=1)
	for ax in [ax2,ax3]:
		ax.set_ylabel('T (K)')
		ax.set_xlim(-10,25)
		ax.set_xlabel(r'V (km s$^{-1}$)')
	for ax,popt,error in zip([ax2,ax3],[popt2,popt3],[error2,error3]):
		ax.annotate(r'$T_{\rm ex}$  $=$'+'%.1f'%popt[0]+'$\pm$'+'%.1f'%error[0]+r' K',xycoords='axes fraction',xy=(0.05,0.92),fontsize=10)
		ax.annotate(r'$\tau$     $=$'+'%.2f'%popt[1]+'$\pm$'+'%.2f'%error[1],xycoords='axes fraction',xy=(0.05,0.85),fontsize=10)
		ax.annotate(r'$V_{\rm LSR}=$'+'%.2f'%popt[2]+'$\pm$'+'%.2f'%error[2]+r' km s$^{-1}$',xycoords='axes fraction',xy=(0.05,0.78),fontsize=10)
		ax.annotate(r'$\Delta V$  $=$'+'%.2f'%(popt[3]*fac)+'$\pm$'+'%.2f'%(error[3]*fac)+r' km s$^{-1}$',xycoords='axes fraction',xy=(0.05,0.71),fontsize=10)

        plt.draw()

############################################### NH3 ########################################
FITS='Data/NH3/GBT_Friesen/To_brightness_temperature/GBT100m.Tbrightness.fits'
fits=pyfits.open(FITS)
data=fits[0].data
ra_nh3,dec_nh3=read_wcs_coord2(fits[0].header)
Fre_li,chan,Vel_li_nh3=read_wave(fits[0].header)

Fit_result=load('Data/NH3/GBT_Friesen/HFS_fitting/Output_HFSfitting.npy')
Fit_result_err=load('Data/NH3/GBT_Friesen/HFS_fitting/Output_HFSfitting_err.npy')
############################################### NH3 #########################################
 
                                                                          
############################################### N2H ########################################
FITS='Data/N2H+/Tobin_IRAS16253_data/To_brightness_temperature/IRAM30m.Tbrightness.fits'
fits2=pyfits.open(FITS)
data2=fits2[0].data[0]
ra_n2hp,dec_n2hp=read_wcs_coord2(fits2[0].header)
Fre_li,chan,Vel_li_n2hp=read_wave(fits2[0].header)

Fit_result2=load('Data/N2H+/Tobin_IRAS16253_data/HFS_fitting/Output_HFSfitting.npy')
Fit_result_err2=load('Data/N2H+/Tobin_IRAS16253_data/HFS_fitting/Output_HFSfitting_err.npy')
############################################### N2H #########################################
 
image=imread('Data/IR_images/IRAS16253_IR.png')

v_li=arange(-30,30,0.005)                                    
fig=figure(figsize=(10,5))                                                 
ax=axes([0.01,0.05,0.55,0.9])
ax.imshow(image,interpolation=None,extent=(247.11717,247.06250,-24.65000,-24.58333),aspect='equal')
ax.tick_params(labelleft=False,labelbottom=False,direction='in')

cursor = Cursor(ax)
connect('motion_notify_event', cursor.mouse_move)
show()

