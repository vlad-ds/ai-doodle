# ✨ Doodle to Art

A minimal web app where users draw simple doodles, AI identifies what they drew, creates an elaborate artistic prompt, and generates beautiful images using Google Imagen.

## How it Works

1. **Draw**: User creates a simple doodle on the canvas
2. **Recognize**: Gemini Flash 2.5 identifies what the doodle represents
3. **Enhance**: AI creates an elaborate, detailed artistic prompt
4. **Generate**: Google Imagen 4.0 creates beautiful artwork
5. **Save**: Images are automatically saved locally with timestamps

## Features

- **Minimal Interface**: Clean, focused design
- **Smart Recognition**: AI understands even simple sketches
- **Elaborate Prompts**: Transforms simple concepts into rich artistic descriptions
- **Professional Art**: High-quality images generated with Imagen 4.0
- **Local Storage**: All generated images saved in `generated_images/` folder
- **Mobile Friendly**: Works on touch devices

## Tech Stack

- **Frontend**: HTML5 Canvas, Vanilla JavaScript, CSS
- **Backend**: FastAPI (Python)
- **AI Recognition**: Google Gemini Flash 2.5
- **Image Generation**: Google Imagen 4.0
- **Dependencies**: google-genai, google-generativeai, Pillow, FastAPI

## Setup Instructions

1. **Navigate to project**:
   ```bash
   cd ai_doodle
   ```

2. **Set up virtual environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   uv pip install fastapi uvicorn google-genai google-generativeai pillow python-multipart
   ```

4. **Set up Gemini API**:
   - Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Set the environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

5. **Run the server**:
   ```bash
   python main.py
   ```

6. **Open your browser**:
   Navigate to `http://localhost:8000`

## Usage

1. **Draw** a simple doodle (cat, house, tree, etc.)
2. **Click "Generate Art"** to process your drawing
3. **View** the AI's recognition and enhanced prompt
4. **See** the beautiful generated artwork
5. **Find** saved images in the `generated_images/` folder

## Example Workflow

**User draws**: Simple cat sketch
**AI recognizes**: "cat"
**Enhanced prompt**: "A majestic cat with piercing emerald eyes, sitting gracefully on a vintage wooden windowsill. Soft golden hour sunlight streams through lace curtains, creating warm shadows across its silky fur..."
**Result**: Professional-quality artistic image of a cat

## Cost Information

- **Gemini Flash 2.5**: Very low cost for recognition and prompt enhancement
- **Imagen 4.0**: Reasonable cost per image generation
- Total cost per generation: Typically under $0.10

## File Structure

```
ai_doodle/
├── main.py              # FastAPI backend with Imagen integration
├── index.html           # Minimal frontend interface
├── generated_images/    # Directory for saved images
└── README.md           # This file
```

## API Endpoints

- `GET /`: Serves the main HTML interface
- `POST /generate`: Processes doodle and generates art
- `GET /generated_images/{filename}`: Serves generated images

## Requirements

- Python 3.8+
- Google AI Studio API key
- Internet connection for API calls

## Troubleshooting

1. **"Please set GEMINI_API_KEY environment variable"**
   - Make sure you've set your Gemini API key

2. **Image generation fails**
   - Check your API key has Imagen access enabled
   - Ensure you have sufficient API credits

3. **No images appear**
   - Check the `generated_images/` folder was created
   - Verify file permissions

## Generated Images

All images are saved as:
- **Format**: JPEG (high quality)
- **Naming**: `doodle_art_YYYYMMDD_HHMMSS.jpg`
- **Location**: `./generated_images/`
- **Size**: 1024x1024 pixels (1:1 aspect ratio)