import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Retrieve Data

prodDf = pd.read_excel("Makeup_Products_Metadata.xlsx")

#  Pre-process data

prodDf.at[462, "Product Description"] = ""
prodDf["Product Description"] = prodDf["Product Description"].map(lambda x: x.split("Explore the entire range")[0])
prodDf["Product Description"] = prodDf["Product Description"].map(lambda x: x.split("Shop more")[0])
prodDf["Product Description"].replace("", np.nan, inplace=True)
prodDf["Product Description"] = np.where(pd.isnull(prodDf["Product Description"]), prodDf["Product Name"], prodDf["Product Description"])
prodDf["Product Tags"] = np.where(pd.isnull(prodDf["Product Tags"]), prodDf["Product Category"], prodDf["Product Tags"])

# Assign weights to different variables
w_desc = 3
w_cat = 3
w_tags = 1
w_brand = 1
w_name = 2
w_price = 1

# Create new column to use for training

prodDf["TrainData"] = prodDf["Product Description"] * w_desc + " " + \
                        prodDf["Product Category"] * w_cat + " " + \
                        prodDf["Product Tags"] * w_tags + " " + \
                        prodDf["Product Brand"] * w_brand + " " + \
                        prodDf["Product Name"] * w_name + " " + \
                        str(prodDf["Product Price [SEK]"]) * w_price

#  Create the similarity matrix for the given weights

vect = CountVectorizer(stop_words='english')

vect_matrix = vect.fit_transform(prodDf["TrainData"])

cosine_similarity_matrix = cosine_similarity(vect_matrix, vect_matrix)

# Select a random product and check the top 5 reccomendations for that product,
# removing the product itself from the list

randProd = prodDf.sample().index

scores = cosine_similarity_matrix[randProd]
np.delete(scores, randProd[0])

sortedScores = np.argpartition(scores, -5)[-5:][0]

originalProd = prodDf.iloc[randProd[0]]
reccommendsProds = prodDf.iloc[sortedScores[-5:]]

