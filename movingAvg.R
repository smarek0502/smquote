library(plyr)
library(dplyr)
library(ggplot2)

quotes <- lapply(Sys.glob('data/*csv'),read.table,header=T,sep=",")

quotesdf <- rbind.fill(quotes) %>%
     mutate(closeunder=Close<Open) %>%
     #group_by(Name) %>%

# TODO calcuate 20 window
