#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


data1=pd.read_csv(r"C:\Users\Vatsal_Fast\Desktop\DataSciencePractice\keithgaliElectronicRetailAnalysis\data\Sales_December_2019.csv")
data1


# In[3]:


import os

#for loop that could create a list by iterating over the directory file list
files=[file for file in os.listdir(r"C:\Users\Vatsal_Fast\Desktop\DataSciencePractice\keithgaliElectronicRetailAnalysis\data")]
files


# In[4]:


year_data=pd.DataFrame()

for file in files:
#     month_data=pd.read_csv(r"H:\IT Cources\Data_science\keithgaillypython\Pandas\analysis\data\"+file)
    month_data=pd.read_csv("C:\\Users\\Vatsal_Fast\\Desktop\\DataSciencePractice\\keithgaliElectronicRetailAnalysis\\data\\"+file)
#     year_data=pd.concat[year_data,month_data]
    year_data=pd.concat([year_data,month_data])

    
# net records should be around 186850
print(year_data)
# year_data=pd.to_csv(r"H:\IT Cources\Data_science\keithgaillypython\Pandas\analysis\data\Sales_2019.csv")
year_data.to_csv(r"C:\Users\Vatsal_Fast\Desktop\DataSciencePractice\keithgaliElectronicRetailAnalysis\Agregateddata\Sales_2019.csv",index=False)


# In[6]:


data=pd.read_csv(r"C:\Users\Vatsal_Fast\Desktop\DataSciencePractice\keithgaliElectronicRetailAnalysis\Agregateddata\Sales_2019.csv")
print(data.head())


# # Finding the best month for sales

# In[7]:


data['Month']=data['Order Date'].str[0:2]
data.head()


# In[8]:


# data['Month']=data['Month'].astypr('int16')    
#error hence data cleaning


# In[9]:


# print(data[data['Month']=='NaN'])??????????????????????????

data=data.dropna(how='all')
data.head()


# In[10]:


# data['Month']=data['Month'].astype('int16')
#further cleaning required


# In[11]:


print(data[data['Month']=='Or'])
data=data[data['Month']!='Or']
print(data[data['Month']=='Or'])


# In[12]:


data['Month']=data['Month'].astype('int16')
print(data.head())
#success finally


# In[13]:


data['Net_price']=data['Quantity Ordered']*data['Price Each']
#further data cleaning required


# In[14]:


# data['Quantity Ordered']=data['Quantity Ordered'].astype('int32')
# data['Price Each']=data['Price Each'].astype('float')

#or

data['Quantity Ordered']=pd.to_numeric(data['Quantity Ordered'])
data['Price Each']=pd.to_numeric(data['Price Each'])


# In[15]:


data['Net_price']=data['Quantity Ordered']*data['Price Each']
print(data.head())

print(data.groupby('Month').sum().sort_values(by=['Net_price'],ascending=False))


# In[16]:


monthly_sale=data.groupby('Month').sum()['Net_price']

# months=arange(1,13)
months=range(1,13)
print(months)

plt.xlabel('Month of the year 2019')
plt.ylabel('Net Sale of the Month (in USD)')
plt.xticks(months)

plt.bar(months,monthly_sale)

plt.show()


# # Finding the City with Highest Sale

# In[17]:


data

# data['Purchase Address'].apply(lambda x: x.split(','))[1]
data['Purchase Address'].apply(lambda x: x.split(',')[1])

data['City']=data['Purchase Address'].apply(lambda x: x.split(',')[1])


print(data)


# In[18]:


data.groupby('City').sum()

city_sale=data.groupby('City').sum()['Net_price']


# city=pd.distinct[data['City']] #no
# city=data['City'].unique()                                        #with chance of error
#or
# city=[city for city in data.groupby('City')] #no
city=[city for city,data in data.groupby('City')]


plt.xlabel('City Name')
plt.ylabel('Net Sale from City (in USD)')
# plt.xticks(city)??????????????????????????????????????????????????????????????????????????
plt.xticks(rotation='vertical',size=8)

# y=float(range(1,5))?????????????????????????????????????????????????????????????????????????????????
# yticks=y*0.4

plt.yticks([0,4000000,8000000,12000000,16000000])

plt.bar(city,city_sale)

plt.show()
data.groupby('City').sum()


# In[19]:


data['City'].unique()


# In[20]:


#there could be multiple cities with same name hence state is also important

def getcity(x):
    return x.split(',')[1]

def getstate(x):
    y=x.split(',')[2]
    return y.split(' ')[1]

def getpin(x):
    y=x.split(',')[2]
    return y.split(' ')[2]

# data['CitywithState']=f"{getcity(data['Purchase Address'])} {getstate(data['Purchase Address'])}"
data['CitywithState']=data['Purchase Address'].apply(lambda x: f"{getcity(x)} ({getstate(x)})")

data['City Pin']=data['Purchase Address'].apply(lambda x: f"{getpin(x)}")

print(data)
data.groupby('CitywithState').sum()
# data.groupby('City').sum()
# data.groupby('City Pin').sum()


# In[21]:


city_sale=data.groupby('CitywithState').sum()['Net_price']


city=data['CitywithState'].unique()                                        #with chance of error


plt.xlabel('City Name')
plt.ylabel('Net Sale from City (in USD)')
plt.xticks(rotation='vertical',size=8)

plt.yticks([0,4000000,8000000,12000000,16000000])

plt.bar(city,city_sale)

plt.show()
data.groupby('CitywithState').sum()


# ### here is a great error of respectiveness of city name list and group by sales sum list

# In[22]:


#hence used sort by clause

city_sale=data.groupby('CitywithState').sum().sort_values(by=['CitywithState'],ascending=False)['Net_price']


# city=data['CitywithState'].sort_values(by=['CitywithState'],ascending=False).unique()       
city=data['CitywithState'].sort_values(ascending=False).unique()      


plt.xlabel('City Name')
plt.ylabel('Net Sale from City (in USD)')
plt.xticks(rotation='vertical',size=8)

plt.yticks([0,4000000,8000000,12000000,16000000])

plt.bar(city,city_sale)

plt.show()
data.groupby('CitywithState').sum()


# # Finding the Best time for advertisement

# In[23]:


data


# In[24]:


# data['Order Date'].split(' ').split(':')[0]
data['Order Time']=data['Order Date'].apply(lambda x: (x.split(' ')[1]).split(':')[0])

#OR
#data['Order Date']=pd.to_datetime(data['Order Date'])

# data['Hour']=data['Order Date'].dt.hour
# data['Minutes']=data['Order Date'].dt.minute


data.head()


# In[25]:


print(data.groupby('Order Time').sum().sort_values(by='Net_price',ascending=False))
# print(data.groupby('Order Time').sum().sort_values(by='Quantity Ordered',ascending=False))


print(data.groupby('Order Time').count())


# In[26]:


hours=[hour for hour,df in data.groupby('Order Time')]

order_count_hour=data.groupby('Order Time').count()

plt.figure(figsize=(8,5),dpi=100)

plt.ylabel("Number of Orders")
plt.xlabel("Hour of the day")
# plt.xticks(hours)

plt.grid()

plt.plot(hours,order_count_hour)

plt.show()


# ## Finding the products sold together

# In[27]:


data.columns
data2=data[['Order ID', 'Product', 'Quantity Ordered', 'Price Each', 'Order Date', 'Month','CitywithState',
       'Net_price']]
data2

data2['Grouped']=data2.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
print(data2.head())


# In[28]:


data2.groupby('Grouped').count()


# In[29]:


#these have some duplication errors so restart with elimination of duplicates


# In[30]:


# data3=data[['Order ID', 'Product', 'Quantity Ordered', 'Price Each', 'Order Date', 'Month','CitywithState',
#        'Net_price']]
# data3.head()

data3=data[data['Order ID'].duplicated(keep=False)]      
#did it to only consider the record which are having double Order id
#that the products which are going to be sold/ordered together are going to have same order id
#hence only those records will be necessary for analysis of this question 

data3.head(30)


# In[31]:


data3['Grouped']=data3.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
print(data3.head())


# In[32]:


data4=data3[['Order ID','Grouped']].drop_duplicates()
data4


# In[33]:


data4.groupby('Grouped').count()


# # imp to do library

# In[34]:


from collections import Counter
from itertools import combinations

count=Counter()

for r in data4['Grouped']:
    row_list=r.split(',')
    count.update(Counter(combinations(row_list,2)))
    

count

count.most_common(10)

for k,v in count.most_common(10):
    print(k," :    ",v)





# ## Finding the product Sold the most and why

# In[35]:


product_count=data.groupby('Product').sum()['Quantity Ordered']
products=[prod for prod,df in data.groupby('Product')]

plt.figure(figsize=(8,5),dpi=100)

plt.xlabel('Product Name')
plt.ylabel('Units sold in 2019')
plt.xticks(rotation='vertical')

plt.bar(products,product_count)
plt.show()


# In[39]:


# price_each=[price for price, df in data.groupby('Product').mean()]
# price_each=[price for price, df in data.groupby('Price Each').mean()]
#price_each=[price for price in data.groupby('Product').mean()['Price Each']]
price_each = [df['Price Each'].mean() for _, df in data.groupby('Product')]

products=[prod for prod,df in data.groupby('Product')]

plt.figure(figsize=(8,5),dpi=100)

plt.xlabel('Product Name')
plt.ylabel('Price of Product')
plt.xticks(rotation='vertical')

plt.plot(products,price_each)
plt.show()


# In[41]:


products=[prod for prod,df in data.groupby('Product')]

product_count=data.groupby('Product').sum()['Quantity Ordered']

#price_each=[price for price in data.groupby('Product').mean()['Price Each']]
price_each = [data.groupby('Product')['Price Each'].mean().loc[prod] for prod in data['Product'].unique()]


#plt.figure(figsize=(8,5),dpi=100)??????????????????????????????????????????


fig,ax1=plt.subplots()


ax2=ax1.twinx()

ax1.bar(products,product_count,color='g')
ax2.plot(products,price_each,'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Units sold in 2019')
ax2.set_ylabel('Price of Product')
# ax1.set_xticks(rotation='vertical',size=8)
ax1.set_xticklabels(products,rotation='vertical',size=8)


plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




