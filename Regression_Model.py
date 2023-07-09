from Statistical_Test import data
import statsmodels.formula.api as smf
import pandas as pd

# create dummy variable to represent gender where 1=Male, 0=Female
data['Male'] = pd.get_dummies(data['Gender'], drop_first=True)

# centering the age based on average age
data['C_Age'] = data['Age'] - data['Age'].mean()

# converting the salary into a unit of thousand of dollar to simplify/shorten the coef
data['Salary'] = data['Salary'] / 1000

data = data[['C_Age', 'Male', 'Education Level', 'Years of Experience', 'Salary']]
data.columns = ['C_Age', 'Male', 'Edu_Lvl', 'Years_Exp', 'Salary']
data = data.replace("Master's Degree", "Masters Degree").replace("Bachelor's Degree", "Bachelors Degree")
order = ['High School', 'Bachelors Degree', 'Masters Degree', 'PhD']
data['Edu_Lvl'] = pd.Categorical(data['Edu_Lvl'], ordered=True, categories=order)
data = data.sort_values(by="Edu_Lvl")

# regression model with interactions
model_age = smf.ols("Salary ~ C_Age * Male", data)
results_age = model_age.fit()

model_edu = smf.ols("Salary ~ Edu_Lvl * Male", data)
results_edu = model_edu.fit()

model_exp = smf.ols("Salary ~ Years_Exp * Male", data)
results_exp = model_exp.fit()

model_all = smf.ols("Salary ~ C_Age * Male + Years_Exp * Male + Edu_Lvl * Male", data)
results_all = model_all.fit()

rsquared_aic = pd.DataFrame({'Predictors': ['Age', 'Experience', 'Education', 'All'],
                             'Adjusted R-squared': [results_age.rsquared_adj, results_exp.rsquared_adj,
                                                    results_edu.rsquared_adj, results_all.rsquared_adj],
                             'AIC': [results_age.aic, results_exp.aic, results_edu.aic, results_all.aic]})

print(rsquared_aic)
