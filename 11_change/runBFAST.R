# Script to run BFAST on a Sentinel-1 timeseries

#install packages
#install.packages("remotes")
library(remotes)
install_github("bfast2/bfast")

#load packages
#library('zoo')
#library(lubridate)
#library('bfast')
#library(plyr)


# load the data
filename <- 'data/ee-chart.csv'
vh <- read.table(file=filename, sep=",", header=TRUE, fill=TRUE, check.names =FALSE)

# run BFAST

