import json
from google import genai
from google.genai import types

from decouple import config

def analyze_food(image):
  
    food_image = image
    if not food_image:
        return {"error": "No image provided"}

    # 2. Initialize the New Client
    # Replace with your actual API key or use an environment variable
    client = genai.Client(api_key=config('API_KEY'))

    # 3. Read image bytes
    image_bytes = food_image.read()

    # 4. Define the Prompt & Schema
    prompt = """
                Act as a professional Clinical Dietitian and Computer Vision expert. 
                Analyze the attached image of food and provide a high-precision nutritional breakdown.

                1. **Identification**: Identify the specific dish (e.g., "Chicken Mandi/Kuzhimanthi").
                2. **Component Analysis**: Estimate the weight (in grams) for each individual element (Rice, Protein, Sauces).
                3. **Caloric Range**: Provide a 'calorie_low' (standard portion) and 'calorie_high' (restaurant portion with hidden fats).
                4. **Note**: Include a brief expert insight on the macronutrient profile.

                Output the result strictly in JSON format with these keys: 
                "food_name", "calorie_low", "calorie_high".

             """

    try:
        # Using the new SDK's generate_content
        response = client.models.generate_content(
            model="gemini-2.5-flash", # or gemini-1.5-flash
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=food_image.content_type
                )
            ],
            config=types.GenerateContentConfig(
                system_instruction="You are a clinical nutritionist. Return ONLY JSON.",
                response_mime_type="application/json",
                # Explicit schema ensures the JSON structure is 100% consistent
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "food_name": {"type": "STRING"},
                        "average_calorie": {"type": "NUMBER"},
                        # "calorie_high": {"type": "NUMBER"} # Changed to NUMBER for easier math later
                    },
                    "required": ["food_name", "average_calorie"]
                }
            )
        )

        # 5. Access the parsed JSON directly
        # The new SDK automatically parses JSON if response_mime_type is set
     
        return response.parsed

    except Exception as e:
        return {"error": str(e)}