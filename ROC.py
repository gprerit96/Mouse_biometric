print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

from sklearn.metrics import roc_curve, auc
"""
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
"""
#fpr = [1,0.073,0.052,0.049,0.048,0.043,0.028,0.026,0.024,0.011,0.006,0.002,0]
#tpr = [1,0.985,0.973,0.961,0.9503,0.944,0.938,0.934,0.927,0.922,0.89,0.86,0]

fpr = [1,0.257,0.124,0.114,0.0932,0.0703,0.0633,0.0521,0.0433,0.0213,0.0117,0]
tpr = [1,0.831,0.820,0.814,0.795,0.783,0.7623,0.732,0.712,0.695,0.664,0]

eer = 0.17621
plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw ,label='ROC curve (area = %0.3f)' % auc(fpr,tpr))
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
#plt.plot([0, 1], [1, 0], color='navy', lw=lw, linestyle='--')
plt.plot([eer],[1-eer],'ro')
plt.text(eer,1-eer-0.06,'EER (%0.2f,%0.2f)' %(eer,1-eer))
#plt.xlim([0.0, 1.0])
#plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Reciever Operating Characterstics')
plt.legend(loc="lower right")
plt.show()

tnr = [1-ele for ele in fpr]

plt.figure()
lw = 2
plt.plot(tnr, tpr, color='darkorange',
         lw=lw )
#plt.xlim([0.0, 1.0])
#plt.ylim([0.0, 1.05])
plt.xlabel('Sensitivity')
plt.ylabel('Specificity')
plt.title('Sensitivity-Specificity Characterstics')
plt.legend(loc="lower right")
plt.show()

