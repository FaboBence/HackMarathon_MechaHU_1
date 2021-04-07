import pandas as pd
import numpy as np

def voting(time_matrix, values_array):
    time_matrix = np.array(time_matrix)
    col_sum = time_matrix.sum(axis=0) # Sum of votes for every option
    mult = np.multiply(col_sum, np.asarray(values_array)) # Weighing votes
    Avg = mult.sum()/col_sum.sum() # Average = weighted votes / sum of all the votes
    # Returning the closest value from values_array
    idx = (np.abs(values_array-Avg)).argmin()
    lunch_time = values_array[idx]
    return values_array[idx]

def ranking_algorithm(price_matrix,food_matrix,filename="database.csv"):
    # Reading requisite files
    database = pd.read_csv(filename, index_col = 0, sep=';') # Restaurant data
    to_matrix=database.drop(["Name"],1)
    restaurant_matrix=to_matrix.to_numpy()
    price_matrix=np.array(price_matrix)
    food_matrix=np.array(food_matrix)

    #manipulating food_matrix
    fm_sum=food_matrix.sum(axis=1)
    food_matrix_norm=[]
    for i,row in enumerate(food_matrix):
        food_matrix_norm.append(row/fm_sum[i])
    food_matrix_norm=np.array(food_matrix_norm)

    #manipulating price_matrix:
    pm_sum=price_matrix.sum(axis=1)*2+2
    price_matrix_norm=[]
    coefficients=[]
    for row in price_matrix:
        tmp=0
        tmp_row=[]
        print(row)
        for i,elem in enumerate(row):
           if row[i]==1:
               tmp+=2
           else:
                if i==0:
                    if row[i+1]==1:
                        tmp+=1
                elif i==len(row)-1:
                    if row[i-1]==1:
                        tmp+=1
                else:
                    if (row[i-1]==1 or row[i+1]==1):
                        tmp+=1
        for i,elem in enumerate(row):
             if row[i]==1:
                tmp_row.append(2*1/tmp)
             else:
                if i==0:
                    if row[i+1]==1:
                        tmp_row.append(1/tmp)
                    else:
                        tmp_row.append(0)
                
                elif i==len(row)-1:
                    if row[i-1]==1:
                        tmp_row.append(1/tmp)
                    else:
                        tmp_row.append(0)
                else:
                    if (row[i-1]==1 or row[i+1]==1):
                        tmp_row.append(1/tmp)
                    else:
                        tmp_row.append(0)
        price_matrix_norm.append(tmp_row)
    price_matrix_norm=np.array(price_matrix_norm)

    #matrix multiplication (algorithm core)
    participant_matrix_norm=np.concatenate((price_matrix_norm,food_matrix_norm),axis=1)
    result=np.matmul(participant_matrix_norm,np.transpose(restaurant_matrix))

    #sort, list ranked restaurants:
    ranking=result.sum(axis=0)
    database.insert(0,"Ranking",ranking)
    database=database.sort_values(by=["Ranking"], ascending=False)
    print(database)
    ranked_restaurant=database["Name"].to_list()

    return ranked_restaurant # Its a list of restaurant names from best to worst