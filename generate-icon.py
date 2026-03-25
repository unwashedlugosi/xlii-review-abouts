import google.genai as genai
from google.genai import types
import base64, sys

client = genai.Client(api_key="REDACTED_GEMINI_KEY")

prompt = """Generate a square app icon (1024x1024). The icon should be:
- A vintage clipboard or editor's notepad with a red pencil or pen marking up text
- The text should look like typed show notes or reviews being edited
- Small red checkmarks and strikethroughs on the page suggesting editorial review
- Warm aged paper color, dark background (near black)
- Gold and cream and red accent color palette
- Clean, modern icon style — no words readable, just the impression of text being reviewed
- The image must fill the entire square with NO rounded corners, NO border, NO margin
- Photorealistic style with slight retro warmth, like a music journalist's desk"""

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"]
    )
)

for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data') and part.inline_data:
        raw = part.inline_data.data
        if isinstance(raw, bytes):
            img_data = raw
        else:
            img_data = base64.b64decode(raw)
        
        with open("icon-1024.png", "wb") as f:
            f.write(img_data)
        
        from PIL import Image
        img = Image.open("icon-1024.png")
        print(f"Icon saved: {img.size}, {img.mode}, {img.format}")
        img.resize((180, 180), Image.LANCZOS).save("icon-180.png")
        img.resize((32, 32), Image.LANCZOS).save("favicon.png")
        print("All sizes generated")
        sys.exit(0)

print("No image generated")
sys.exit(1)
