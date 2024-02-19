import pandas as pd
from surprise import Dataset, Reader, NMF, SVD, KNNBasic
from surprise.model_selection import cross_validate, train_test_split, GridSearchCV

# Load data
prodDf = pd.read_excel("Makeup_Products_Metadata.xlsx")
userRatingsDf = pd.read_excel("User_review_data.xlsx").sort_values(by=["User"])


# Transform data into the correct format with the appropriate reader
surpriseData = {
    "user": userRatingsDf["User"].to_list() * 566,
    "item": userRatingsDf.drop("User", axis=1).columns.values.tolist() * 600,
    "rating": userRatingsDf.drop("User", axis=1).values.flatten()
    }

df = pd.DataFrame(surpriseData)
reader = Reader(rating_scale=(0, 5))

data = Dataset.load_from_df(df[["user", "item", "rating"]], reader)

# Cross validate several algorithms to check different accuracies
# SVD

algo = SVD()

cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

# KNNBasic

algo = KNNBasic()

cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

# NMF

algo = NMF()

cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)


# Use gridSearch to find the best parameters for the SVD algorithm and fit the data

trainSet, testSet = train_test_split(data, test_size=0.25)

paramGrid = {'n_factors': [100,150],
              'n_epochs': [20,25,30],
              'lr_all':[0.005,0.01,0.1],
              'reg_all':[0.02,0.05,0.1]}
gridSearch = GridSearchCV(SVD, paramGrid, measures=['rmse','mae'], cv=3)
gridSearch.fit(data)  


algo = gridSearch.best_estimator['rmse']

cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)


algo.fit(trainSet)

# Make predictions and check the top 10 reccomendations

predictions = algo.test(testSet)

predDf = pd.DataFrame(predictions)
predDf.sort_values(by=['est'],inplace=True,ascending = False)
print(predDf.head(10))