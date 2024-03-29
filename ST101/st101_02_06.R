print.matrix <- function(m){
  write.table(format(m, justify="right"),
              row.names=T, col.names=T, quote=F)
}

p_loaded = 0.1
p_hfair = 0.5
p_hloaded = 0.9
cells <- c(4, 0,10, 0, 20, 0, 0, 5, 2, 3)
rnames <- c("# heads", "# tails")
# creates a list of in form ("#1", "#2", "#n"...) to n=number of trials
cnames <- c(paste("#", 1:(length(cells)/2), sep = "")) 
trials <- matrix(cells, nrow=2, ncol=5, byrow=FALSE, dimnames=list(rnames, cnames))
#print(trials)

# P(fair|flips) = (P(flips|fair) * P(fair))/ P(flips)

for (trial in 1:ncol(trials)) {
  # joint probablities for fair and loaded coins given observed results
  jp_fair = trials[1, trial] * p_hfair + trials[2, trial] * (1-p_hfair)
  jp_loaded = trials[1, trial] * p_hloaded + trials[2, trial] * (1-p_hloaded)
  if (jp_fair < jp_loaded) {
    print(paste("trial ", trial, " is < 0.5 probable for a fair coin!", sep=""))
  } 
}
