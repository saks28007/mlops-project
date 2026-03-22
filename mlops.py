import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# dummy data
data = pd.DataFrame({
    "area": [1000, 1500, 2000],
    "price": [10, 15, 20]
})

X = data[["area"]]
y = data["price"]

model = LinearRegression()
model.fit(X, y)

# save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# test loading
with open("model.pkl", "rb") as f:
    loaded_model = pickle.load(f)

print(loaded_model.predict([[1200]]))