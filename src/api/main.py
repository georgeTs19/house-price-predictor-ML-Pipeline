from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from inference import predict_price, batch_predict
from schemas import HousePredictionRequest, PredictionResponse

# Initialize FastAPI app with metadata
app = FastAPI(
    title="House Price Prediction API",
    description=(
    "An API for predicting house prices based on various features. "
    "Authored by George Tsoupras. "
    "Disclaimer: This project is intended for educational purposes only and "
    "should not be used for real financial or investment decisions."
    ),
    version="1.0",
    contact={
        "name": "George Tsoupras",
        "email": "gtsoupras19@gmail.com",
    },

)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", response_model=dict)
async def health_check():
    return {"status": "healthy", "model_loaded": True}

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: HousePredictionRequest):
    return predict_price(request)

# Batch prediction endpoint
@app.post("/batch-predict", response_model=list)
async def batch_predict_endpoint(requests: list[HousePredictionRequest]):
    return batch_predict(requests)