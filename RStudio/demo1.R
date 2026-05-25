library(ggplot2)
#library(rmarkdown)


movies = read.csv('../data/movieData.csv') # reading movieData.csv
movies

ggplot(movies, aes(y=CriticsRating, x=LevelOfViolence, color = factor(Watched))) +
  geom_point( size=3) + # using shape in geom_point parameter
  scale_color_manual(values = c("-1" = "red", "1" = "blue") , labels = c("Not Watched", "Watched")) +
  labs(title = "Decision Boundary of Perceptron", color = "Watch Status") +
  xlab('Critics Rating') +
  ylab('Level of Violence')


## the Viewer tab in the Output pane is used to display web content
## like `plotly`. Read: https://docs.posit.co/ide/user/ide/guide/ui/ui-panes.html
library(plotly)
plot_ly(x = 1:10, y = 1:10)