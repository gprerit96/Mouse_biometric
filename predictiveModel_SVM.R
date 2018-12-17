
#load libraries
library('e1071')
library('ROCR')
library('ggplot2')

cat("\014")
setwd("/Users/soumyamac/Documents/Projects/BTP WORK/BTP_Codes/features/")
combiSet <- read.csv("ProcessedFeatures.csv")

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
for (iteration in 1:count)
{
  #create train set and test set
  combiSet <- combiSet[sample(nrow(combiSet)),]   #randomize
  totalLength <- nrow(combiSet)
  testLength <- floor(totalLength / 5)
  testSet <- combiSet[1:testLength,]
  trainSet <- combiSet[(testLength+1):totalLength,]
  
  # fit <- svm(formula = User ~ f1 + f2 + f3 + f4 + f5 + f6 + f7 + f8 + f9 + f10,
  fit <- svm(formula = User ~ f7 + f8 + f9,
             data = trainSet, kernel = "radial", type = "C-classification", probability = T)
  
  # print(fit)
  # summary(fit)
  
  prediction <- predict(fit, testSet, decision.values = TRUE)
  prob <- prediction   #probability of class = 'originalUser'
  predictClass <- predict(fit, testSet)
  actual <- testSet[,1]
  prediction <- cbind(actual, predictClass)
  
  trueVal = 2
  falseVal = 1
  tp <- length(which(prediction[,1] == trueVal & prediction[,2] == trueVal))
  fp <- length(which(prediction[,1] == falseVal & prediction[,2] == trueVal))
  fn <- length(which(prediction[,1] == trueVal & prediction[,2] == falseVal))
  tn <- length(which(prediction[,1] == falseVal & prediction[,2] == falseVal))
  averageAccuracy = averageAccuracy + ((tp + tn) / (tp + fp + fn + tn))
  averageFRR = averageFRR + (fn / (fn + tp))
  averageFAR = averageFAR + (fp / (fp + tn))
  
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

