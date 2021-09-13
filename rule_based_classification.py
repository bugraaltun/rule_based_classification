############## RULE BASED CLASSIFICATION WITH PANDAS ##############
###################################################################


import pandas as pd


df = pd.read_csv("Datasets/persona.csv")
df.head()
df.shape


#Read the persona.csv file and show the general information about the dataset
def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


#How many unique sources are there and what are their frequencies

df["SOURCE"].nunique()
df["SOURCE"].value_counts()


#How many unique PRICEs are there?

df["PRICE"].nunique()


#How many sales were made from which price?

df["PRICE"].value_counts()



#How many sales were made from which country?

df["COUNTRY"].value_counts()


#How much was earned in total from sales by country?

df[["PRICE","COUNTRY"]].groupby("COUNTRY").agg("sum")


#What are the sales numbers by source types?

df["SOURCE"].value_counts()


#What are the price averages by country?

df[["COUNTRY", "PRICE"]].groupby("COUNTRY").agg("mean")


#What are the PRICE averages based on SOURCEs?

df[["SOURCE", "PRICE"]].groupby("SOURCE").agg("mean")


#What is the average price in the country-source breakdown?

df.pivot_table(values="PRICE", index="COUNTRY", columns="SOURCE")

#What are the average earnings in the breakdown of country, source, sex, age?

bg = df.groupby(["COUNTRY", "SOURCE","SEX","AGE"]).agg({"PRICE": "mean"})

#Sort the output by price.

agg_df = bg.sort_values(by="PRICE", ascending = False)

#Convert the names in the index to variable names.

agg_df.reset_index().head()
agg_df = agg_df.reset_index()

#Convert age variable to categorical variable.

df["AGE"].max()
bins = [0,18,23,30,40,66]
mylabels = ["0_18","19_23","24_30","31_40","41_66"]
agg_df["AGE_CAT"] =pd.cut(agg_df["AGE"],bins, labels=mylabels)
agg_df.head(20)

#Identify new level-based customers (personas).

agg_df.dtypes
agg_df["customer_level_based"] = [i[0].upper() + "_" + i[1].upper() + "_" +
                                  i[2].upper() + "_" +i[5].upper() for i in agg_df.values]

agg_df[["customer_level_based", "PRICE"]]
agg_df = agg_df[["customer_level_based", "PRICE"]]
agg_df.head(10)

agg_df["customer_level_based"].value_counts()

agg_df = agg_df.groupby("customer_level_based").agg({"PRICE" : "mean"})

agg_df = agg_df.reset_index()

#Segment new customers (personas).
#Classify new customers according to their segments and estimate how much revenue they can bring.
#▪Which segment does a 33-year-old Turkish woman using ANDROID belong to and how much income is expected to earn on average?
#▪In which segment and on average how much income would a 35-year-old French woman using IOS earn?

pd.qcut(agg_df["PRICE"], 4 , labels=["D","C","B","A"])

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4 , labels=["D","C","B","A"])

agg_df.groupby(["SEGMENT"]).agg({"PRICE": ["min", "max", "sum"]})
agg_df[agg_df["SEGMENT"] == "C"]

new_user = "TUR_ANDROID_FEMALE_30_40"
new_user2 = "FRA_IOS_FEMALE_30_40"

agg_df[agg_df["customer_level_based"] == new_user]

agg_df[agg_df["customer_level_based"] == new_user2]
