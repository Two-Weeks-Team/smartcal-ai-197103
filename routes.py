from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Any, Dict

from models import SessionLocal, User, MealPlan, Meal, FoodItem, SmartPlateEntry, AIPrediction
from ai_service import call_inference

router = APIRouter()

# Dependency to provide a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Simple placeholder endpoint for contract demonstration
@router.get("/items", tags=["Demo"])
async def get_items():
    return {"items": ["demo1", "demo2", "demo3"]}

class MealPlanRequest(BaseModel):
    user_id: str = Field(..., description="ID of the user requesting a plan")
    preferences: Dict[str, Any] = Field(..., description="User dietary preferences and goals")

class MealPlanResponse(BaseModel):
    meal_plan: Dict[str, Any]

@router.post("/generate-meal-plan", response_model=MealPlanResponse, tags=["AI"])
async def generate_meal_plan(request: MealPlanRequest, db: SessionLocal = Depends(get_db)):
    # Verify user exists (minimal check)
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    system_msg = "You are a helpful nutrition AI that creates a 7‑day meal plan based on the provided user preferences. Return a JSON object with days as keys and an array of meals (name, calories, protein, carbs, fat)."
    user_msg = f"Preferences: {request.preferences}"
    ai_result = await call_inference(messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}])

    # Store prediction for auditability
    pred = AIPrediction(
        user_id=request.user_id,
        type="meal_plan",
        prediction=ai_result,
        confidence=None,
    )
    db.add(pred)
    db.commit()

    return MealPlanResponse(meal_plan=ai_result)

class FoodRecognitionResponse(BaseModel):
    food_item: Dict[str, Any]

@router.post("/recognize-food", response_model=FoodRecognitionResponse, tags=["AI"])
async def recognize_food(image: UploadFile = File(...), request: Request = None, db: SessionLocal = Depends(get_db)):
    # Read image bytes (in a real implementation you'd send the bytes or a URL to the model)
    image_bytes = await image.read()
    # For the demo we just describe the image as base64 string placeholder
    import base64
    b64_image = base64.b64encode(image_bytes).decode('utf-8')
    system_msg = "You are a vision model that identifies food items in an image. Return a JSON object with the most likely food name and estimated calories."
    user_msg = f"Image (base64): {b64_image[:100]}..."
    ai_result = await call_inference(messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}])

    # Store smart plate entry (image_path omitted for demo)
    entry = SmartPlateEntry(
        user_id="unknown",  # In a real flow, extract from auth context
        image_path=None,
        ai_prediction=ai_result,
    )
    db.add(entry)
    db.commit()

    return FoodRecognitionResponse(food_item=ai_result)
