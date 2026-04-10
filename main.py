from fastapi import FastAPI, HTTPException, Header
import pickle
import logging
   
# initialize app
app = FastAPI()

# setup logging
logging(level=logging.INFO) 
            
# API KEY (you can change this)
API_KEY = "mysecretkey"
     
# load trained model
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    logging.info("Model loaded successfully")
except Exception as e:
    logging.error(f"Error loading model: {str(e)}")
    model = None

# home route 
@app.get("/")
def home():                            
    return {"message": "ML API is running with authentication"}

# function to verify API key
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


# prediction route (secured)
@app.get("/predict")
def predict(area: float, x_api_key: str = Header(...)):
    try:
        # check API key
        verify_api_key(x_api_key)

        # check model
        if model is None:
            raise Exception("Model not loaded")

        # input validation
        if area <= 0:
            raise ValueError("Area must be greater")                                                                                       than 0")

        # prediction
        prediction = model.predict([[area]])

        logging.info(f"Prediction successful for input: {area}")

        return {"prediction": float(prediction[0])}

    except ValueError as ve:
        logging.error(f"Validation Error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))

    except HTTPException as he:
        raise he

    except Exception as e:
        logging.error(f"Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
