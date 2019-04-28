#-------------------------------------------------------------------------------------
#Code to produce dispersal kernels for seeds for the range of terminal velocities 
#measured in our study for Pinus radiata, under "average" set of conditions (Fig. 5a)
#The script produces a heat plot of the integral of these kernels, with contours
#showing the locations of the 50% (median), 95%, and 99% quantiles

# LICENSING
#This code is licensed according to the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
#International License.
#-------------------------------------------------------------------------------------

#Function to calculate the dispersal kernel, using the WALD model, with parameters other
#than terminal velocity defaulting to those used in Fig. 5a.
P.x = function(x, term.vel, Ubar = 1.87, H.release = 23.5, H.canopy = 10, sigma.w = 0.6, K = 0.4){
  mu = (Ubar*H.release)/term.vel
  gamma = (Ubar*H.release^2)/(2*K*H.canopy*sigma.w)
  
  px = sqrt(gamma/(2*pi*(x^3)))*exp(-1*((gamma*((x-mu)^2))/(2*x*(mu^2))))
  
  return(px)
  
}

#----------------------------------------------------------------------------------------

#sequence of terminal velocity values
tvs = seq(0.63, 1.44, by = 0.01)

#Sequence of distances
dists = seq(1,250, by = 1)

#create an empty matrix with rows the distances and columns the terminal velocities  
px.mat = matrix(ncol = length(tvs), nrow = length(dists))
colnames(px.mat) = tvs
rownames(px.mat) = dists

#for each row and column, calculate the area under the dispersal kernel from 0 metres to
# 'r' metres, for samaras of terminal velocity 'c' and fill in the appropriate cell in the
#matrix
for(r in 1:nrow(px.mat)){
  for(c in 1:ncol(px.mat)){
    
    px.mat[r,c] = as.numeric(integrate(P.x, lower = 0, upper = as.numeric(rownames(px.mat)[r]), term.vel = as.numeric(colnames(px.mat)[c]))[1])
  }
}
  
#plot the heatplot of the matrix (remember that image plots a 90 degree anti-clockwise
#rotation of the printed layout of the input matrix

par(mar = c(5,5,1,1))
image(dists, tvs, px.mat, col = heat.colors(50), xlab = "Dispersal distance (m)", ylab = expression(paste("Terminal velocity (m ", s^-1, ")")))

#add contours
contour(dists, tvs, px.mat, add = T, labcex = par('cex'), levels = c(0.5, 0.95, 0.99))

#add a nice box around the plot
rect(par('usr')[1], par('usr')[3], par('usr')[2], par('usr')[4])

