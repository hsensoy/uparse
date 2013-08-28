library(sqldf)
library(fpc)
TOPN = 80000
german_embeddings <- read.delim("~/uparse/german.embeddings", nrows= TOPN,header=F,col.names=c("word","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15","f16","f17","f18","f19","f20","f21","f22","f23","f24","f25"),sep='\t',blank.lines.skip=TRUE,quote = "",colClasses=c("character",rep("numeric",25)))
german_embeddings_features = subset(german_embeddings, select=c("f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15","f16","f17","f18","f19","f20","f21","f22","f23","f24","f25"))

#german.embeddings.matrix = scale(german.embeddings)

# DBSCAN Algorithm
d = dist(german_embeddings_features)
ds <- dbscan(d, 0.4, MinPts=8,showplot=FALSE,method="dist")
ncluster = max(ds$cluster)
german_embeddings$cluster = predict(ds, german_embeddings_features, german_embeddings_features)
german_embeddings_filtered= sqldf("select word,cluster from german_embeddings where cluster != 0 order by cluster, word")

MinPts = 24
init = c(0.4)

optimDBSCAN <- function (eps) {
  ds <- dbscan(german_embeddings_features, eps, MinPts,showplot=FALSE)
  ncluster = max(ds$cluster)
  s <- summary(silhouette(ds$cluster,d))[4]
  #message(ncluster, " for eps=",eps, " and MinPts=",MinPts, ". Silhouette is ",  s)
  
  (s$avg.width*-1.)
}

nopt = which.max(silresult)
cl <- kmeans(german.embeddings.matrix,centers=nopt,iter.max=300,nstart=1000)
s <- silhouette(cl$cluster,d)
#plot(s)
cl


wssplot <- function(data, nc=50, seed=1234){
  wss <- (nrow(data)-1)*sum(apply(data,2,var))
  for (i in 2:nc){
    set.seed(seed)
    wss[i] <- sum(kmeans(data, centers=i,iter.max = 20)$withinss)}
  
  plot(1:nc, wss, type="b", xlab="Number of Clusters",
       ylab="Within groups sum of squares",)
}

#german_embeddings$cluster = predict(ds, german_embeddings_features, german_embeddings_features)
#german_embeddings_filtered= sqldf("select word,cluster from german_embeddings where cluster != 0 order by cluster, word")

#cl <- kmeans(german.embeddings.matrix,centers=nopt,iter.max=300,nstart=1000)
#s <- silhouette(cl$cluster,d)
#plot(s)
