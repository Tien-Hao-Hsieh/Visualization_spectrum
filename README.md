# Visualization_spectrum

A data cube examing tool. Input the sky image and data cubes (i.e., spectrum) you want to exam, and >> python Plot_comparison.py.
Moving the cursor to see the spectra at the given position in the image.

#### Requirments:
* Numpy
* Matplotlib
* Astropy
* Scipy

### Example of visualization N2H+ and NH3 spectra at a positon in the infrared iamge
* Infrared images (Hsieh et al. 2017)
* IRAM 30m: N<sub>2</sub>H<sup>+</sup> J=1-0 (Tobin et al. 2013)
* GBT NH<sub>3</sub> (1,1) Survey: [Archived data](https://dataverse.harvard.edu/dataverse/GAS_Project) (Friesen et al. 2017)

The top right and bottom panels show the N<sub>2</sub>H<sup>+</sup> J=1-0 and NH<sub>3</sub> (1,1), respectively.
The red lines show the best-fit to the hyperfine structures, and the best-fit parameters were labeled in the upper right corner. To include the fitting results, you need to run the hyperfine fitting (e.g., Fitting_N2Hp.py in Functions/) and includes the results in Plot_comparison.py.

![image](https://github.com/tienhaohsieh/Visualization_spectrum/blob/main/demo.gif)

