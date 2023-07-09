import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

data = pd.read_csv('Salary_Data.csv')
data = data.dropna()

# Check what are the unique data in the Gender column and the count
# print(data['Gender'].value_counts())
# There are 14 rows where Gender = Other, let's drop this
data = data.drop(data.loc[data['Gender'] == 'Other'].index, inplace=False)
data = data.reset_index()

# Check what are the unique data in the Education Level column and the count
# print(data['Education Level'].value_counts())
# There are inconsistency in how some category is written, let's standardize them
data = data.replace("Bachelor's", "Bachelor's Degree").replace("Master's", "Master's Degree").replace("phD", "PhD")

# Visualize the salary distribution between male and female using histogram for 3000 random sample of each gender
plt.hist(data[data['Gender'] == 'Male']['Salary'].sample(3000), bins=list(range(0, 290000, 10000)), color='blue', label='Male', alpha=0.5)
plt.hist(data[data['Gender'] == 'Female']['Salary'].sample(3000), bins=list(range(0, 290000, 10000)), color='red', label='Female', alpha=0.5)
plt.legend()
plt.xlabel('Salary', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.show()


# Do statistical test to check if female and male average salary is equal
# start by doing F-test to check if we should use T-test with equal or unequal variance
data_female = data[data['Gender'] == 'Female']
data_male = data[data['Gender'] == 'Male']
fem_sal = np.array(data_female['Salary'])
male_sal = np.array(data_male['Salary'])

f = np.var(fem_sal, ddof=1) / np.var(male_sal, ddof=1)
dfn = fem_sal.size - 1
dfd = male_sal.size - 1
p = 1 - stats.f.cdf(f, dfn, dfd)
if p < 0.05:
    var_equality = False
else:
    var_equality = True
print(f"p-value of F-test is {p}, variance equality is {var_equality}")

# continue doing two-sided T-test with equal variance
result = stats.ttest_ind(a=data_female['Salary'],
                         b=data_male['Salary'],
                         equal_var=var_equality,
                         alternative="two-sided")
print(f"p-value of t_test is {result.pvalue}")
if result.pvalue < 0.05:
    print("Null hypothesis rejected, average salary of female and male"
          " is unequal")
else:
    print("Fail to reject null hypothesis, average salary of female and"
          " male is equal")
# now we know that average salary of female and male is unequal, so gender need to be included as predictor
