import pandas as pd
from sklearn.model_selection import train_test_split

clean_data = pd.read_csv("mclean_glassdoors_dataset.csv")

print(clean_data.columns)

# get the most important features for modeling
data = clean_data[["average_income","Rating","Size","Type of ownership","Industry","Sector","Revenue","Competitors_Number","Hourly","Employer_Provided_Salary","State","location_job","Company_Age","Python","Spark","AWS","Excel","Jobs_Rephrases","Seniority","L_Job_Description"]]
data.to_csv("model_data.csv", index = False)

data=pd.read_csv('model_data.csv')

print(data.head())

print(data.columns)

print(len(data.columns))

final_data = pd.get_dummies(data)

print(final_data.head())

print(final_data.columns)

print(len(final_data.columns))



X = final_data.drop("average_income", axis = 1)              # independent features
y = final_data["average_income"].values                           # output label

print(X.shape)

print(y.shape)

# train test split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state = 42)

print(X_train.shape)

print(y_train.shape)

print(X_test.shape)

print(y_test.shape)

from sklearn.linear_model import LinearRegression

linear_regressor = LinearRegression()                                      # Model Initialization
linear_regressor.fit(X_train,y_train)

from sklearn.model_selection import cross_val_score

score=cross_val_score(linear_regressor,X_train, y_train, scoring = "neg_mean_absolute_error",cv = 3)

import numpy as np

validation_score=np.mean(score)

print(validation_score)

from sklearn.linear_model import Lasso

import matplotlib.pyplot as plt

# Hyperparameter Optimization using elbow method
alpha,error=[],[]
for parameter in range(1,100):
    alpha.append(parameter/100)
    lasso = Lasso(alpha=(parameter/100))
    error.append(np.mean(cross_val_score(lasso,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3)))
plt.plot(alpha,error)
plt.ylabel('ERROR')
plt.xlabel('alpha')
plt.title('Hyperparameter Optimization')

errors = tuple(zip(alpha,error))
all_errors = pd.DataFrame(errors, columns = ['alpha','error'])
print(all_errors[all_errors["error"] == max(all_errors["error"])])               # lowest error

### from the above elbow method we can tell that, for alpha~0.13 we are getting lowest error

lasso_regressor = Lasso(alpha=.14)                                   # Model Initialization
lasso_regressor.fit(X_train,y_train)

lasso_score=cross_val_score(lasso_regressor,X_train, y_train, scoring = "neg_mean_absolute_error",cv = 3)

lasso_validation_score=np.mean(lasso_score)

print(lasso_validation_score)

## Random Forest

from sklearn.ensemble import RandomForestRegressor

random_forest = RandomForestRegressor()                              # Model Initialization

random_forest_score=cross_val_score(random_forest,X_train,y_train,scoring = 'neg_mean_absolute_error', cv= 3)

random_forest_validation_score=np.mean(random_forest_score)

print(random_forest_validation_score)

# Hyper parameter optimization
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(0,250,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}

model = GridSearchCV(random_forest,parameters,scoring='neg_mean_absolute_error',cv=3)
model.fit(X_train,y_train)

print(model.best_score_)

print(model.best_estimator_)

pred_by_linearRegressor = linear_regressor.predict(X_test)
pred_by_lassoRegressor = lasso_regressor.predict(X_test)
pred_by_RandomForestRegressor = model.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
print("Mean Absolute Errors of the above models:")
print("predictions by Linear Regressor: ",mean_absolute_error(y_test,pred_by_linearRegressor))
print("predictions by Lasso Regression: ",mean_absolute_error(y_test,pred_by_lassoRegressor))
print("predictions by Random Forest Regressor",mean_absolute_error(y_test,pred_by_RandomForestRegressor))

import pickle

pickle_file = {'model': model.best_estimator_}
pickle.dump( pickle_file, open( 'optimized_model' + ".pickle", "wb" ) )


file_name = "optimized_model.pickle"
with open(file_name, 'rb') as output:
    data = pickle.load(output)
    loaded_model=data['model']

print(loaded_model.predict(np.array(list(X_test.iloc[1,:])).reshape(1,-1))[0])


### for the above employee the average salary is 52k $ approx