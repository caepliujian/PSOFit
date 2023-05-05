# PSOFit
# Training:
- Step 1: Give a csv file for training or testing, containing the descriptor ('X') and the target property('Y').
- Step 2: Edit the form of equation ('F(x)'）.
- Step 3: Adjust the number of parameters ('ScaleFactors') and gives the initial values, which can be arbitrary.
- Step 4: Use command 'python PSOFit.py Train.csv Train' to run.

<em>The results are write to a parameter.txt including the values of automatic fitting parameters and a file named ‘Train_xx.csv’ including the evaluation index ($\text{R}^2$, MAE, RMSE) and the train results in the format of ‘ID, Y_Exp, Y_Pred’, as follows:

R2=0.8509	MAE=2.0	RMSE=2.6	

1-4-ETHYLPHENYL-2-4-ETHYLPHENYLETHANE	26.59	25.1

1-4-ETHYLPHENYL-2-PHENYLETHANE	23.79	22.02

......</em>


# Testing:
- Step 1: Give a csv file for training or testing, containing the descriptor ('X') and the target property('Y').
- Step 2: Put the parameter.txt obtained in the training process and the test file the same folder.
- Step 2: Use command 'python PSOFit.py Test.csv Test' to get test results.

</em>The results are write to a file named ‘Train_xx.csv’ including the evaluation index ($\text{R}^2$, MAE, RMSE) and the test results in the format of ‘ID, Y_Exp, Y_Pred’, as follows:

R2=0.7101	MAE=3.2	RMSE=3.9	

NITROMETHANE	11.92	12.5	0.58

NITROETHANE	13.38	12.56	-0.82</em>
