# Script to run BFAST on a Sentinel-1 timeseries

#install packages
#install.packages("remotes")
library(remotes)
#install_github("bfast2/bfast")

#load packages
#library('zoo')
#library(lubridate)
library('bfast')
#library(plyr)


# load the data
filename <- 'data/bfastInput.csv'
s1data <- read.table(file=filename, sep=",", header=TRUE, fill=TRUE, check.names =FALSE)

# run BFAST
nBreaks=3
ts <-bfastts(s1data[,2],s1data[,1], type="irregular")
fit <-bfastlite(ts, breaks=nBreaks)

# print out the date
for( n in 1:nBreaks){
  index=fit$breakpoints$breakpoints[n]
  print('Breakpoint found on')
  print(s1data[index,1])
}

