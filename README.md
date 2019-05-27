# SeedTerminalVelocity_RaspberryPi_MEE

### About this repository

Code associated with our paper introducing a device to measure samara terminal velocity based on a Raspberry Pi.  If using this code, please cite the paper as follows:

Wyse, S.V., Hulme, P.E., & Holland, E.P. (2019) Partitioning intraspecific variaton in seed dispersal potential using a low-cost method for rapid estimation of samara terminal velocity. *Methods in Ecology and Evolution.* https://doi.org/10.1111/2041-1210X.13202

This repository contains the following scripts:

- **MeasureSeedTerminalVelocity_RaspberryPi.py**

   This Python script is run on the Raspberry Pi.  It is used to control the camera module and calculate the terminal velocity of seeds when dropped in the device.

- **CalculateSamaraDimensions.py**

   This Python script is used to calculate the area and dimensions of samaras from scanned images.

- **WaldModel_AreaUnderCurve.R**

   This R script is used to predict likely seed dispersal kernels using the Wald model.

### Licensing

The scripts provided in this repository are licensed according to the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode "Creative Commons License Information").
