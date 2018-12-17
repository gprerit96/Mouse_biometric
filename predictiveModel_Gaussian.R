
#load libraries
library('ROCR')
library('ggplot2')

cat("\014")
setwd("/home/prerit/Documents/BTP/features/")
TruthSet <- read.csv("ProcessedFeatures.csv")
validLength = 38
totalLength = nrow(TruthSet)

#for (i in 2:11)
#{
#  pdfF11 <- density(TruthSet[1:validLength,i], kernel = 'gaussian')
#  plot(pdfF11, xlim = c(0, max(TruthSet[,i])), col = 'red', main = paste(c('Feature', i-1), collapse = " "))
#  pdfF10 <- density(TruthSet[(validLength + 1):totalLength,i], kernel = 'gaussian')
#  lines(pdfF10, xlim = c(0, 0.11), col = 'blue')
#}

validSet <- read.csv("ProcessedFeatures.csv")[1:validLength,]
invalidSet <- read.csv("ProcessedFeatures.csv")[(validLength + 1):totalLength,]

#threshold
epsilon = 5e-7

count = 1000
averageAccuracy = 0
averageFRR = 0
averageFAR = 0
averageAUC = 0
averageFPR <- vector(mode="numeric", length=3)
averageTPR <- vector(mode="numeric", length=3)
averagePrec <- vector(mode="numeric", length=3)
averageRec <- vector(mode="numeric", length=3)
averageSens <- vector(mode="numeric", length=3)
averageSpec <- vector(mode="numeric", length=3)
for(iteration in 1:count)
{
  #create train set and test set
  testLength = floor(nrow(TruthSet) / 20) * 4
  trainLength = nrow(validSet) - testLength / 2
  validSet <- validSet[sample(nrow(validSet)),]   #randomize
  invalidSet <- invalidSet[sample(nrow(invalidSet)),]   #randomize
  trainSet <- validSet[1:trainLength,]
  testSet <- rbind(validSet[(trainLength + 1):nrow(validSet),], invalidSet[1:(testLength / 2),])
  
  averageVal <- colSums(trainSet[,2:11]) / nrow(trainSet)
  stdVal <- apply(trainSet[,2:11], 2, sd )
  
  #Find the probability value for the test set
  prediction <- mat.or.vec(nr = nrow(testSet), nc = 3)
  trueVal = 2
  falseVal = 1
  for(i in 1:nrow(testSet))
  {
    prediction[i, 1] = testSet[i, 1]    #target class
    prediction[i, 3] = 1
    # for(j in 2:ncol(testSet))
    for(j in 2:11)
    {
      prediction[i, 3] = prediction[i, 3] * dnorm(testSet[i, j], averageVal[j-1], stdVal[j-1])
    }
    print(prediction[i,3])
    print(epsilon)
    if(prediction[i, 3] >= epsilon)
      prediction[i, 2] = trueVal
    else
      prediction[i, 2] = falseVal
  }

  tp <- length(which(prediction[,1] == trueVal & prediction[,2] == trueVal))
  fp <- length(which(prediction[,1] == falseVal & prediction[,2] == trueVal))
  fn <- length(which(prediction[,1] == trueVal & prediction[,2] == falseVal))
  tn <- length(which(prediction[,1] == falseVal & prediction[,2] == falseVal))
  averageAccuracy = averageAccuracy + ((tp + tn) / (tp + fp + fn + tn))
  averageFRR = averageFRR + (fn / (fn + tp))
  averageFAR = averageFAR + (fp / (fp + tn))
  
  
  prob <- prediction[, 3]   #probability of class = 'originalUser'
  pred <- prediction(prediction[,2], prediction[,1])    #prediction of Gaussian classifier for ROCR
  perf <- performance(pred, measure = "tpr", x.measure = "fpr")
  perf1 <- performance(pred, measure = "prec", x.measure = "rec")
  perf2 <- performance(pred, measure = "sens", x.measure = "spec")
  auc <- performance(pred, measure = "auc")
  averageAUC <- averageAUC + auc@y.values[[1]]
  averageFPR <- averageFPR + unlist(perf@x.values)
  averageTPR <- averageTPR + unlist(perf@y.values)
  averagePrec <- averagePrec + unlist(perf1@y.values)
  averageRec <- averageRec + unlist(perf1@x.values)
  averageSens <- averageSens + unlist(perf2@y.values)
  averageSpec <- averageSpec + unlist(perf2@x.values)
}

averageAccuracy = averageAccuracy / count * 100
averageFRR = averageFRR / count * 100
averageFAR = averageFAR / count * 100

print(averageAccuracy)
print(averageFRR)
print(averageFAR)

#ROC curve
averageFPR <- averageFPR / count
averageTPR <- averageTPR / count
averageAUC <- averageAUC / count
roc.data <- data.frame(FPR = averageFPR, TPR = averageTPR)
ggplot(roc.data, aes(x = FPR, ymin = 0, ymax = TPR)) + geom_ribbon(alpha = 0.2) + geom_line(aes(y = TPR)) + ggtitle(paste0("ROC Curve w/ AUC=", averageAUC))

#Precision-Recall plot
averagePrec <- averagePrec / count
averageRec <- averageRec / count
precRec.data <- data.frame(Precision = averagePrec, Recall = averageRec)
ggplot(precRec.data, aes(x = Precision, ymin = 0, ymax = Recall)) + geom_ribbon(alpha = 0.2) + geom_line(aes(y = Recall)) + ggtitle(paste0("Precision-Recall plot"))

#Sensitivity-Specificity plot
averageSens <- averageSens / count
averageSpec <- averageSpec / count
sensSpec.data <- data.frame(Sensitivity = averageSens, Specificity = averageSpec)
ggplot(sensSpec.data, aes(x = Sensitivity, ymin = 0, ymax = Specificity)) + geom_ribbon(alpha = 0.2) + geom_line(aes(y = Specificity)) + ggtitle(paste0("Sensitivity-Specificity plot"))

