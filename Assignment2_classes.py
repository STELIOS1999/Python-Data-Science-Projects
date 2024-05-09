import pandas as pd
import numpy as np

def matrix_multiplication(size):
    intA = np.random.randint(-500,50000, (size,size))
    flA = np.random.rand(size,size)
    A = intA + flA
    b = np.random.randint(-10,100,size)
    return(A@b)

def int_sorting(size):

    array = np.random.randint(-500,50000, (size))#random array
    
    for i in range(len(array)-1):
        
        min_value=array[i]#min value as the first element of searching
        
        change=False
        
        for j in range(i+1,len(array)):#checking the next integers of the list to find the minimum       
            
            if array[j]<=min_value:
                min_value=array[j]#new minimum value
                index=j#saving the index to change numbers
                change=True
                
        if change:
            
            #replacing values 
            temp=array[index]
            array[index]=array[i]
            array[i]=temp
            
    return array  

def subset_string(string,substring):
    
    index=0#initialise index
    
    for i in range(len(string)):
        
        condition=False #initialising, assuming false
        
        if string[i]==substring[0]:#if the first element of the substring match for any element for the string
            
            for j in range(1,len(substring)):#checking remaining elements
                
                if i+j<=len(string)-1: # loop until the end of the substring, unless end of string is reached
                    
                    if string[i+j]!=substring[j]:#if j element for substring doesn't match, break
                        break
                        
                    else:
                        if j==len(substring)-1:#if reached end of substring, condition is satisfied
                            condition=True
                else:
                    break
                
            if condition:
                index=i #index that match starts 
                break
                
    if condition==False:
        return 'Second string is no substring of the first'
    
    else:       
        return 'There is a match at index'+" "+"{}".format(index)
        
class Data_Cleaning:
    def __init__(self,df):
        self.df=df#initialising dataframe
        
    def missing_values(self):
        for i in range(len(self.df)):
            
            #substituting missing values with the mean of their respective level
            
            if np.isnan(self.df['T4'].iloc[i]):
                self.df['T4'].iloc[i]=self.df[self.df['Level']==self.df['Level'].iloc[i]]['T4'].mean()
            if np.isnan(self.df['T3'].iloc[i]):
                self.df['T3'].iloc[i]=self.df[self.df['Level']==self.df['Level'].iloc[i]]['T3'].mean() 
            if np.isnan(self.df['T3adjusted'].iloc[i]):
                self.df['T3adjusted'].iloc[i]=self.df[self.df['Level']==self.df['Level'].iloc[i]]['T3adjusted'].mean()
            if np.isnan(self.df['T4adjusted'].iloc[i]):
                self.df['T4adjusted'].iloc[i]=self.df[self.df['Level']==self.df['Level'].iloc[i]]['T4adjusted'].mean()
        return self.df
    
    
    def removing_rows(self):
        
        array=np.asarray([])
        for i in range(len(self.df)): 
            
            if self.df['T4'].iloc[i]==0 or self.df['T3'].iloc[i]==0:#if T3=0 or T4=0 ignore as the ratio is meaningless
                continue
                
            elif (self.df['T4'].iloc[i]/self.df['T3'].iloc[i])>=3 or (self.df['T3'].iloc[i]/self.df['T4'].iloc[i])>=3:#criterio used to exclude data that are extreme outliers within the best fit line and they don't make sense
        
                array=np.append(array,[i],axis=0)
            else:
                if np.sign(self.df['T4'].iloc[i])!=np.sign(self.df['T3'].iloc[i]):#if T3 and T4 have different sign they are again excluded as extreme outliers
                    array=np.append(array,[i],axis=0)
                else:
                    continue
        self.df=self.df.drop(array)
        return self.df
    
    def table_statistics(self):
        #creating sorted arrays for each field
        Level=np.asarray(self.df['Level'])
        Level=np.sort(Level)
        T4=np.asarray(self.df['T4'])
        T4=np.sort(T4)
        T3=np.asarray(self.df['T3'])
        T3=np.sort(T3)
        T3adjusted=np.asarray(self.df['T3adjusted'])
        T3adjusted=np.sort(T3adjusted)
        T4adjusted=np.asarray(self.df['T4adjusted'])
        T4adjusted=np.sort(T4adjusted)
        
        #creating 2 dimensional array that each column is sorted
        dataframe_array=np.asarray([Level,T4,T3,T3adjusted,T4adjusted]).T
     
    
        describe_array=np.zeros((8,5))#array with zeros to be filled with table statistics values
        columns=np.asarray(self.df.columns)#array with columns for table dataframe
        
    
       #filling count values in describe_array
        for i in range(dataframe_array.shape[0]):
            for j in range(len(columns)):
                if np.isnan(dataframe_array[i,j]):
                    continue
                else:
                    describe_array[0,j]+=1  
        #calculate mean values in describe_array            
        for k in range(len(columns)):
            describe_array[1,k]=self.df[[columns[k]]].sum()
        describe_array[1,:]=describe_array[1,:]/describe_array[0,:]            
                    
       #calculation of std values in describe_array
        for i in range(dataframe_array.shape[0]):
             for j in range(len(columns)):
                if np.isnan(dataframe_array[i,j]):
                    continue
                else:
                    describe_array[2,j]+=(dataframe_array[i,j]-describe_array[1,j])**2
        describe_array[2,:]=(describe_array[2,:]/(describe_array[0,:]-1))**(0.5)
    
        
        for j in range(len(columns)):
              describe_array[3,j]=dataframe_array[:,j][~np.isnan(dataframe_array[:,j])][0]#take the first value in the sorted array with no nan values as the min
              describe_array[7,j]=dataframe_array[:,j][~np.isnan(dataframe_array[:,j])][len(dataframe_array[:,j][~np.isnan(dataframe_array[:,j])])-1]#take the last value in the sorted array with no nan values as the max
            
              if describe_array[0,j]%2==1:#if count is not even
                      describe_array[5,j]=dataframe_array[int(describe_array[0,j]//2+1),j]#substitute median
                        
                      if (describe_array[0,j]//2)%2==1:
                        
                           #if 25% and 75% lie on singular values
                           describe_array[4,j]=dataframe_array[int(describe_array[0,j]//2//2+1),j]
                        
                           describe_array[6,j]=dataframe_array[int(describe_array[0,j]//2+1+describe_array[0,j]//2//2+1),j]
                            
                      else:
                        
                        #if 25% and 75% lie on 2 values, the average is taken
                        
                           describe_array[4,j]=(dataframe_array[int(describe_array[0,j]//2//2),j]+dataframe_array[int(describe_array[0,j]//2//2+1),j])/2
                            
                           describe_array[6,j]=(dataframe_array[int(describe_array[0,j]//2+1+describe_array[0,j]//2//2),j]+dataframe_array[int(describe_array[0,j]//2+1+describe_array[0,j]//2//2+1),j])/2
                        
              else:#if count is even
                
                #average between the 2 values is taken for the median
                
                     describe_array[5,j]=(dataframe_array[int(describe_array[0,j]//2),j]+dataframe_array[int(describe_array[0,j]//2+1),j])/2
                    
                     if (describe_array[0,j]//2)%2==1:
                     #if 25% and 75% lie on singular values       
                           describe_array[4,j]=dataframe_array[int(describe_array[0,j]//2//2+1),j]
                           describe_array[6,j]=dataframe_array[int(describe_array[0,j]//2+describe_array[0,j]//2//2+1),j]
                            
                     else:
                        
                        #if 25% and 75% lie on 2 values, the average is taken
                           describe_array[4,j]=(dataframe_array[int(describe_array[0,j]//2//2),j]+dataframe_array[int(describe_array[0,j]//2//2+1),j])/2
                            
                           describe_array[6,j]=(dataframe_array[int(describe_array[0,j]//2+describe_array[0,j]//2//2),j]+dataframe_array[int(describe_array[0,j]//2+describe_array[0,j]//2//2+1),j])/2
        


        
        index=np.array(['count','mean','std','min','25%','50%',"75%",'max'])#array with index for dataframe
        lf = pd.DataFrame(data=describe_array, index=index, columns=columns)#creating the table dataframe
        return lf
        
        
    def repeated_rows(self):
        array=[]
        for i in range(len(self.df)):
            for j in range(i+1,len(self.df)):
                if all(np.asarray(self.df.iloc[i])==np.asarray(self.df.iloc[j])):#if all values are the same append
                    array.append([i,j])
        if array:
            return(array)
        else:
            return('There are no repeated rows')

