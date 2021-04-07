import pandas as pd
import numpy as np

# Reading requisite files + Global variables
filename="database.csv"
database = pd.read_csv(filename, index_col = 0, sep=';') # Restaurant data
to_matrix=database.drop(["Name"],1)
restaurant_matrix=to_matrix.to_numpy()
#csak a futtatáshoz kellennek:
price_matrix=np.array([[0,1,0,0],[0,1,0,0],[1,0,0,0],[0,0,1,0]])
food_matrix=np.array([[0,0,0,0,0,0,1,0,0,0,0,0],[1,0,1,0,0,0,1,0,0,0,0,0],[1,1,1,1,1,1,0,0,0,0,0,0],[0,0,0,1,0,0,1,0,1,0,0,0]])

#manipulating food_matrix
fm_sum=food_matrix.sum(axis=1)
food_matrix_norm=[]
for i,row in enumerate(food_matrix):
    food_matrix_norm.append(row/fm_sum[i])
food_matrix_norm=np.array(food_matrix_norm)

#manipulating price_matrix:
pm_sum=price_matrix.sum(axis=1)*2+2; 
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

#mtrix multiplication (algorithm core)
participant_matrix_norm=np.concatenate((price_matrix_norm,food_matrix_norm),axis=1)
result=np.matmul(participant_matrix_norm,np.transpose(restaurant_matrix))

#sort, list ranked restaurants:
ranking=result.sum(axis=0)
database.insert(0,"Ranking",ranking)
database=database.sort_values(by=["Ranking"], ascending=False)
print(database)
ranked_restaurant=database["Name"]
print("\nRestaurant recommendation:")
print()
print(ranked_restaurant)