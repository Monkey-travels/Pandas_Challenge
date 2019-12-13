#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)
purchase_data.head()


# ## Player Count

# * Display the total number of players
# 

# In[16]:


#Calcuate the Number of Unique Players
player_demographics = purchase_data.loc[:, ["Gender", "SN", "Age"]]
player_demographics = player_demographics.drop_duplicates()
num_players = player_demographics.count()[0]
num_players
pd.DataFrame({"Total Players": [num_players]})


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[20]:


#Run calcuation to obtain number of unique iterms average praice, etc.
average_item_price = purchase_data["Price"].mean()
total_purchase_value = purchase_data["Price"].sum()
purchase_count = purchase_data["Price"].count()
item_count = len(purchase_data["Item ID"].unique())

#Create a DataFrame to hold results
summary_table = pd.DataFrame({ 
                            "Number of Unique Items" : item_count,
                            "Total Revenue": [total_purchase_value],
                            "Number of Purchases": [purchase_count],
                            "Average Price": [average_item_price]
                            })

#Minor Data Munging
#summary_table.head()
summary_table = summary_table.round(2)
summary_table["Average Price"] = summary_table["Average Price"].map("${:,.2f}".format)
summary_table["Number of Purchases"] = summary_table["Number of Purchases"].map("{:,}".format)
summary_table["Total Revenue"] = summary_table["Total Revenue"].map("${:,.2f}".format)
summary_table = summary_table.loc[:, ["Number of Unique Items", "Average Price", "Number of Purchases", "Total Revenue"]]

summary_table


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[28]:


#Calcuate the Number of % by Gender
gender_demographics_total = player_demographics["Gender"].value_counts()
gender_demographics_percent = gender_demographics_total / num_players
gender_demographics = pd.DataFrame({
                                    "Total Count": gender_demographics_total,
                                    "Percentage of Players": gender_demographics_percent
                                   })
#Minor data cleaning
gender_demographics["Percentage of Players"] = gender_demographics["Percentage of Players"].map("{:,.2%}".format)

gender_demographics


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[38]:


#Run calcuations
gender_purchase_total = purchase_data.groupby(["Gender"]).sum()["Price"].rename("Total Purchase Value")
#gender_purchase_total
gender_average = purchase_data.groupby(["Gender"]).mean()["Price"].rename("Average Purchase Price")
#gender_average
gender_count = purchase_data.groupby(["Gender"]).count()["Price"].rename("Purchase Count")
#gender_count

#Calcuate normalized purchasing
normalized_total = gender_purchase_total / gender_demographics["Total Count"]

#Convert to DataFrame
gender_data = pd.DataFrame({
                            "Purchase Count": gender_count,
                            "Average Purchase Price": gender_average,
                            "Total Purchase Value": gender_purchase_total,
                            "Normalized Totals": normalized_total
                           })

#Cleaning process
gender_data["Average Purchase Price"] = gender_data["Average Purchase Price"].map("${:,.2f}".format)
gender_data["Total Purchase Value"] = gender_data["Total Purchase Value"].map("${:,.2f}".format)
gender_data["Purchase Count"] = gender_data["Purchase Count"].map("${:,.2f}".format)
gender_data["Avg Total Purchase per Person"] = gender_data["Normalized Totals"].map("${:,.2f}".format)
gender_data[["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Avg Total Purchase per Person"]]


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[44]:


#Establish bins for ages
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_name = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"] 

#Categorize the exising players using age bins
player_demographics["Age Ranges"] = pd.cut(player_demographics["Age"], 
                                           age_bins, labels=group_name)

age_demographics_total = player_demographics["Age Ranges"].value_counts()
age_demographics_percents = age_demographics_total / num_players
age_demographics = pd.DataFrame({"Total Count": age_demographics_total, 
                                 "Percentage of Players": age_demographics_percents})

#Clean
age_demographics["Percentage of Players"] = age_demographics["Percentage of Players"].map("{:,.2%}".format)

#Display aget demographics table
age_demographics = age_demographics.sort_index()
age_demographics


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[52]:


#Bin the purchasing data
purchase_data["Age Ranges"] = pd.cut(purchase_data["Age"], age_bins, labels=group_name)

#calculate
age_purchase_total = purchase_data.groupby(["Age Ranges"]).sum()["Price"].rename("Total Purchase Value")
age_average = purchase_data.groupby(["Age Ranges"]).mean()["Price"].rename("Average Purchase Price")
age_count = purchase_data.groupby(["Age Ranges"]).count()["Price"].rename("Purchase Count")

#normalize the total
normalized_total = age_purchase_total / age_demographics["Total Count"]
#normalized_total

#Convert to DataFrame
age_data = pd.DataFrame({
                        "Purchase Count": age_count,
                        "Average Purchase Price": age_average,
                        "Total Purchase Value": age_purchase_total,
                        "Normalized Totals": normalized_total
                        })

age_data["Average Purchase Price"] = age_data["Average Purchase Price"].map("${:,.2f}".format)
age_data["Total Purchase Value"] = age_data["Total Purchase Value"].map("${:,.2f}".format)
age_data["Purchase Count"] = age_data["Purchase Count"].map("${:,}".format)
age_data["Avg Total Purchase per Person"] = age_data["Normalized Totals"].map("${:,.2f}".format)

age_data[["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Avg Total Purchase per Person"]]


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[54]:


user_total = purchase_data.groupby(["SN"]).sum()["Price"].rename("Total Purchase Value")
user_average = purchase_data.groupby(["SN"]).mean()["Price"].rename("Average Purchase Price")
user_count = purchase_data.groupby(["SN"]).count()["Price"].rename("Purchase Count")

user_data = pd.DataFrame({
                        "Total Purchase Value": user_total,
                        "Average Purchase Price": user_average,
                        "Purchase Count": user_count
                        })

user_sorted = user_data.sort_values("Total Purchase Value", ascending=False)

user_sorted["Average Purchase Price"] = user_sorted["Average Purchase Price"].map("${:,.2f}".format)
user_sorted["Total Purchase Value"] = user_sorted["Total Purchase Value"].map("${:,.2f}".format)


user_sorted[["Purchase Count", "Average Purchase Price", "Total Purchase Value"]].head(5)


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[58]:


item_data = purchase_data[["Item ID", "Item Name", "Price"]]

#Calculation
total_item_purchase = item_data.groupby(["Item ID", "Item Name"]).sum()["Price"].rename("Total Purchse Price")
average_item_purchase = item_data.groupby(["Item ID", "Item Name"]).mean()["Price"]
item_count = item_data.groupby(["Item ID", "Item Name"]).count()["Price"].rename("Purchase Count")

#Create DataFrame
item_data_pd = pd.DataFrame({
                            "Total Purchase Value": total_item_purchase,
                            "Item Price": average_item_purchase,
                            "Purchase Count": item_count
                            })

#Sort Values
item_data_count_sorted = item_data_pd.sort_values("Purchase Count", ascending=False)

#Cleaning
item_data_count_sorted["Item Price"] = item_data_count_sorted["Item Price"].map("${:,.2f}".format)
item_data_count_sorted["Purchase Count"] = item_data_count_sorted["Purchase Count"].map("${:,}".format)
item_data_count_sorted["Total Purchase Value"] = item_data_count_sorted["Total Purchase Value"].map("${:,.2f}".format)

item_data_count_sorted[["Purchase Count", "Item Price", "Total Purchase Value"]].head()


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[59]:


#Item table
item_total_purchase = item_data_pd.sort_values("Total Purchase Value", ascending=False)

item_total_purchase["Item Price"] = item_total_purchase["Item Price"].map("${:,.2f}".format)
item_total_purchase["Purchase Count"] = item_total_purchase["Purchase Count"].map("{:,}".format)
item_total_purchase["Total Purchase Value"] = item_total_purchase["Total Purchase Value"].map("${:,.2f}".format)

item_total_purchase[["Purchase Count", "Item Price", "Total Purchase Value"]].head(5)


# In[ ]:

#Observations:
#This game is most popular for men at the age of between 15 and 24.
#However, the players with the most purchasing power are the players between age 35 and 39.
#The most popular item (Oathbreaker, Last Hope of the Breaking Storm) is also the most profitable item.



