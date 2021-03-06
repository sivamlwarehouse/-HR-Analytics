# -*- coding: utf-8 -*-
"""prod_funct.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12p3TG6q2axPj7lF9TmhfU5Tz7qk89yuy
"""

def load_data(filepath):
    import pandas as pd
    import numpy as np
    data=pd.read_csv(filepath)
    return data

#missingvalues_analysis
def mis_val(data):
    mis_val=data.isnull().sum()
    return(mis_val)

##def change_datatypes(bank_data):
##  lis = []
##  for i in range(0, bank_data.shape[1]):
##      #print(i)
##      if(bank_data.iloc[:,i].dtypes == 'object'):
##          bank_data.iloc[:,i] = pd.Categorical(bank_data.iloc[:,i])
##          #print(marketing_train[[i]])
##          bank_data.iloc[:,i] = bank_data.iloc[:,i].cat.codes 
##          bank_data.iloc[:,i] = bank_data.iloc[:,i].astype('object')
##          
##          lis.append(bank_data.columns[i])
##    return data

#FINDING highly correlated variables
def corr_matrix(data):
  #extract numeric data
  num_data=data.select_dtypes('float64').copy()
  # Create correlation matrix
  corr_matrix = num_data.corr().abs()
  # Select upper triangle of correlation matrix
  corr_mat= corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
  upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
  # Find index of feature columns with correlation greater than 0.95
  to_drop = [column for column in num_data.columns if any(upper[column] > 0.95)]
  sns.heatmap(corr_mat,cmap="Spectral")
 
  return num_data

def feature_scaling(num_data):

  sc=StandardScaler()
  num_data_scaled=sc.fit_transform(num_data)
  return num_data_scaled

def train_test_slpit(X,y):
   X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
   return X_train,X_test,y_train,y_test

#Decision Tree Clssification
from sklearn.tree import DecisionTreeClassifier

def DecisionTreeClassifier(X_train,y_train):
  dc_tree=DecisionTreeClassifier()
  dc_tree.fit(X_train,y_train)
  #y_predict=dc_tree.predict(X_test)
  return y_predict

#Randoforest classifier
def random_forest(X_train,y_train):
  rf_cls=RandomForestClassifier()
  rf_cls.fit(X_train,y_train)
  #y_predict=rf_cls.predict(X_test)
  return y_predict

#Gradienboosting classifier
def gradientboost_classification(X_train,y_train,X_test):
  #creating scroring parameter:
  scoring={'accuracy':make_scorer(accuracy_score),
          'precision':make_scorer(precision_score),'recall':make_scorer(recall_score)}
  #A sample parameter
  parameters = {
      "loss":["deviance"],
      "learning_rate": [0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2],
      "min_samples_split": np.linspace(0.1, 0.5, 12),
      "min_samples_leaf": np.linspace(0.1, 0.5, 12),
      "max_depth":[3,5,8],
      "max_features":["log2","sqrt"],
      "criterion": ["friedman_mse",  "mae"],
      "subsample":[0.5, 0.618, 0.8, 0.85, 0.9, 0.95, 1.0],
      "n_estimators":[10]
      }       
  #passing the scorng function in the GridSearchCV
  clf=GridSearchCV(GradientBoostingClassifier(),parameters,scoring=scoring,refit=False,cv=4, n_jobs=-1)
  clf.fit(X_train,y_train)
  return clf


  
##  y_predict=clf.predict(X_test)
##  #converting the clf.cv_results to dataframe
##  df=pd.DataFrame.from_dict(clf.cv_results_)
##  #here Possible inputs for cross validation is cv=2, there two split split0 and split1
##  df[['split0_test_accuracy','split1_test_accuracy','split0_test_precision','split1_test_precision','split0_test_recall','split1_test_recall']]
##  return y_predict,clf.summary,df
##




#predicting probabilities
def metrics_classification(y_test,y_predict):
  cm=confusion_matrix(y_test,y_predict)
  probs=dc_tree.predict_proba(X_test)
  predcs=probs[:,1]
  fpr,tpr,threshold=metrics.roc_curve(y_test,predcs)
  roc_auc=metrics.auc(fpr,tpr)
  print (classification_report(y_test,y_predict))
  plt.title('Receiver Operating Characteristic')
  plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
  plt.legend(loc = 'lower right')
  plt.plot([0, 1], [0, 1],'r--')
  plt.xlim([0, 1])
  plt.ylim([0, 1])
  plt.ylabel('True Positive Rate')
  plt.xlabel('False Positive Rate')
  plt.show()
  return  classification_report(y_test,y_predict),fpr,tpr



