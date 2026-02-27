from google import genai
from google.genai import types
from decouple import config

# # pip install -U google-genai
def generate_kerala_diet_plan(goal="weight loss",age =None,weight=None,gender="male",target_weight=None,duration=None):
    
    # Initialize the new Client
    client = genai.Client(api_key=config('API_KEY'))
    
    # Extract user
   
    
    prompt = f"""Act as a Clinical Nutritionist.Create a Kerala-style {goal} diet plan.User: {gender}, {age}yrs, {weight}kg. Target: {target_weight}kg in {duration} months.
                Format the output strictly as a JSON object with these keys:
                - "daily_calories": (int)
                - "nutritional_advice": (string)
                - "weekly_plan": (list of 7 objects with keys: "day", "breakfast", "lunch", "snack", "dinner")
                - "kerala_tips": (list of strings)

                Use traditional Kerala foods (Matta rice, Thoran, Fish curry, etc.). 
                Ensure portions are specific (e.g., "1/2 cup Matta rice"). 
                Return ONLY the JSON. No preamble.
              """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a Kerala Nutritionist. Return ONLY JSON.",
                response_mime_type="application/json",
                # This schema ensures your frontend never breaks
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "daily_calories": {"type": "NUMBER"},
                        "diet_plan": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "day": {"type": "STRING"},
                                    "meals": {"type": "ARRAY", "items": {"type": "STRING"}}
                                }
                            }
                        }
                    }
                }
            )
        )
        return response.parsed 
    except Exception as e:
        return e

generate_kerala_diet_plan(goal="weight loss",age=32,weight=75,gender="male",target_weight=68,duration=4)




# prompt = f"""
#     Act as a Clinical Nutritionist. Create a Kerala-style weight loss diet plan.
#     User: {"male"}, {32}yrs, {64}kg. Target: {60}kg in 2 months.
    
#     Format the output strictly as a JSON object with these keys:
#     - "daily_calories": (int)
#     - "nutritional_advice": (string)
#     - "weekly_plan": (list of 7 objects with keys: "day", "breakfast", "lunch", "snack", "dinner")
#     - "kerala_tips": (list of strings)

#     Use traditional Kerala foods (Matta rice, Thoran, Fish curry, etc.). 
#     Ensure portions are specific (e.g., "1/2 cup Matta rice"). 
#     Return ONLY the JSON. No preamble.
#     """




