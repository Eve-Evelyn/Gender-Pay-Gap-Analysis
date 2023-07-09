import numpy as np
import matplotlib.pyplot as plt
from Regression_Model import *


def print_coef_std_err(mod_results):
    """
    Function to combine estimated coefficients and standard error in one DataFrame
    """
    coef = mod_results.params
    std_err = mod_results.bse

    df = pd.DataFrame(data=np.transpose([coef, std_err]),
                      index=coef.index,
                      columns=["coef", "std err"])
    return df


def create_graph_num(mod_res, pred, interaction):
    """
    Create fitted line graph for x-axis with numerical value
    """
    # Extract the Coefficient and Standard Error to DataFrame
    results_dataframe = print_coef_std_err(mod_results=mod_res)

    # plot C_Age vs Salary
    predictors = [pred, "Male", interaction]
    outcome = "Salary"
    data_1 = data.copy()
    results_ = results_dataframe.copy()
    linestyles = {0: "--", 1: "-"}
    c = {0: "r", 1: "b"}
    markers = {0: "x", 1: "."}

    # Plot the data
    for i in range(2):
        plt.scatter(data_1[data_1[predictors[1]] == i][predictors[0]], data_1[data_1[predictors[1]] == i][outcome],
                    color=c[i], marker=markers[i])

    beta0_hat = results_.loc["Intercept"]["coef"]
    beta1_hat = results_.loc[predictors[0]]["coef"]
    beta2_hat = results_.loc[predictors[1]]["coef"]
    beta3_hat = results_.loc[predictors[2]]["coef"]

    x_domain = np.linspace(np.min(data[predictors[0]]), np.max(data[predictors[0]]), 100)
    fitted_values = [beta0_hat + beta1_hat * x_domain + beta2_hat * i + beta3_hat * i * x_domain for i in range(2)]

    # Plot two fitted line
    for i in range(2):
        plt.plot(x_domain, fitted_values[i], c=c[i], label=f"Fitted line (Male={i})", linestyle=linestyles[i])

    # Add a legend and labels
    plt.legend()
    plt.ylabel(f"{outcome}", fontsize=12)
    plt.xlabel(f"{predictors[0]}", fontsize=12)
    plt.show()


# create_graph_num(results_exp, "Years_Exp", "Years_Exp:Male")

def create_graph_cat():
    """
    Create fitted line graph for x-axis with categorical value
    """
    linestyles = {0: "--", 1: "-"}
    c = {0: "r", 1: "b"}
    markers = {0: "x", 1: "."}

    # Plot the data
    for i in range(2):
        plt.scatter(data[data['Male'] == i]['Edu_Lvl'], data[data['Male'] == i]['Salary'],
                    color=c[i], marker=markers[i])

    # Extract the Coefficient and Standard Error to DataFrame
    results_ = print_coef_std_err(mod_results=results_edu)

    beta0_hat = results_.loc["Intercept"]["coef"]
    beta1_hat = results_.loc['Edu_Lvl[T.Bachelors Degree]']["coef"]
    beta2_hat = results_.loc['Edu_Lvl[T.Masters Degree]']["coef"]
    beta3_hat = results_.loc['Edu_Lvl[T.PhD]']["coef"]
    beta4_hat = results_.loc['Male']["coef"]
    beta5_hat = results_.loc['Edu_Lvl[T.Bachelors Degree]:Male']["coef"]
    beta6_hat = results_.loc['Edu_Lvl[T.Masters Degree]:Male']["coef"]
    beta7_hat = results_.loc['Edu_Lvl[T.PhD]:Male']["coef"]

    x_domain = ['High School', 'Bachelors Degree', 'Masters Degree', 'PhD']

    # Calculate the fitted value for each category
    def fitted_val(n=0):
        fitted_val_var = [0, beta1_hat + beta5_hat * n, beta2_hat + beta6_hat * n, beta3_hat + beta7_hat * n]
        return fitted_val_var + beta0_hat + beta4_hat * n

    # Plot two fitted line
    for i in range(2):
        plt.plot(x_domain, fitted_val(n=i), c=c[i], label=f"Fitted line (Male={i})", linestyle=linestyles[i])

    plt.legend()
    plt.ylabel("Salary", fontsize=12)
    plt.xlabel("Education Level", fontsize=12)
    plt.show()


# create_graph_cat()
