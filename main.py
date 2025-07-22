import os
import base64
import io
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
import google.generativeai as genai_classic
from PIL import Image

app = FastAPI(title="Doodle to Art", version="1.0.0")

# Configure APIs
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY environment variable")

# Setup both API clients
genai_classic.configure(api_key=GEMINI_API_KEY)
recognition_model = genai_classic.GenerativeModel('gemini-2.0-flash-exp')

client = genai.Client(api_key=GEMINI_API_KEY)

# Create output directory
os.makedirs("generated_images", exist_ok=True)

class DrawingRequest(BaseModel):
    image: str

def process_image_data(image_data: str) -> Image.Image:
    """Convert base64 image data to PIL Image"""
    header, encoded = image_data.split(",", 1)
    image_bytes = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(image_bytes))
    return image

def recognize_doodle(image: Image.Image) -> str:
    """Use Gemini to recognize what the doodle represents"""
    recognition_prompt = """
    Look at this simple doodle/drawing and identify what object or thing it represents.
    Give a clear, simple description of what you see. Be specific but concise.
    If you're not sure, make your best guess based on the shapes and lines.
    Respond with just the name/description of the object, nothing else.
    Examples: "cat", "house", "tree", "car", "person", "flower"
    """
    
    try:
        response = recognition_model.generate_content([recognition_prompt, image])
        return response.text.strip()
    except Exception as e:
        print(f"Error in recognition: {e}")
        return "abstract drawing"

def create_enhanced_prompt(recognition: str) -> str:
    """Generate a bold, simple artistic prompt for Imagen"""
    # Choose a random bold artistic direction
    import random
    
    styles = [
        "stunning digital art",
        "beautiful oil painting", 
        "dreamy watercolor",
        "bold pop art style",
        "magical fantasy art",
        "vibrant cartoon style",
        "elegant minimalist art",
        "dramatic cinematic style"
    ]
    
    moods = [
        "magical and enchanting",
        "warm and cozy", 
        "bold and vibrant",
        "dreamy and ethereal",
        "dramatic and moody",
        "cheerful and bright",
        "mysterious and atmospheric",
        "elegant and sophisticated"
    ]
    
    style = random.choice(styles)
    mood = random.choice(moods)
    
    # Simple, direct prompt
    return f"A {recognition}, {style}, {mood}, professional quality, highly detailed"

def generate_image_with_imagen(prompt: str, reference_image: Image.Image = None) -> tuple[str, str]:
    """Generate image using Imagen with optional reference image"""
    try:
        # Prepare the request
        if reference_image:
            # Convert PIL image to bytes for Imagen
            img_bytes = io.BytesIO()
            reference_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            result = client.models.generate_images(
                model="models/imagen-4.0-generate-preview-06-06",
                prompt=prompt,
                reference_images=[{
                    'image': img_bytes.getvalue(),
                }],
                config=dict(
                    number_of_images=1,
                    output_mime_type="image/jpeg",
                    person_generation="ALLOW_ADULT",
                    aspect_ratio="1:1",
                ),
            )
        else:
            result = client.models.generate_images(
                model="models/imagen-4.0-generate-preview-06-06",
                prompt=prompt,
                config=dict(
                    number_of_images=1,
                    output_mime_type="image/jpeg",
                    person_generation="ALLOW_ADULT",
                    aspect_ratio="1:1",
                ),
            )

        if not result.generated_images:
            raise Exception("No images generated")

        if len(result.generated_images) != 1:
            raise Exception("Unexpected number of images generated")

        # Save the image locally
        generated_image = result.generated_images[0]
        image = Image.open(io.BytesIO(generated_image.image.image_bytes))
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"doodle_art_{timestamp}.jpg"
        filepath = os.path.join("generated_images", filename)
        
        # Save the image
        image.save(filepath, "JPEG", quality=95)
        
        return filepath, filename
        
    except Exception as e:
        print(f"Error generating image: {e}")
        raise Exception(f"Failed to generate image: {str(e)}")

@app.post("/generate")
async def generate_art(request: DrawingRequest) -> Dict[str, Any]:
    """Process doodle and generate beautiful art with Imagen"""
    try:
        # Process the doodle image
        image = process_image_data(request.image)
        
        # Step 1: Recognize what the doodle represents
        recognition = recognize_doodle(image)
        print(f"Recognized: {recognition}")
        
        # Step 2: Create elaborate prompt for Imagen
        enhanced_prompt = create_enhanced_prompt(recognition)
        print(f"Enhanced prompt: {enhanced_prompt}")
        
        # Step 3: Generate beautiful art with Imagen using the original doodle
        filepath, filename = generate_image_with_imagen(enhanced_prompt, image)
        
        # Create URL for the frontend to display the image
        image_url = f"/generated_images/{filename}"
        
        return {
            "recognition": recognition,
            "prompt": enhanced_prompt,
            "image_url": image_url,
            "filename": filename
        }
        
    except Exception as e:
        print(f"Error in generate_art: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating art: {str(e)}")

@app.get("/")
async def serve_index():
    """Serve the main HTML file"""
    return FileResponse("index.html")

# Serve generated images
app.mount("/generated_images", StaticFiles(directory="generated_images"), name="generated_images")

# Serve static files
app.mount("/static", StaticFiles(directory="."), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)