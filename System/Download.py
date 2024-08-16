from io import BytesIO
import requests,PIL

def Preview(Token):
    try:
        if Image := Token['Data'].get('Solana', {}).get('Metadata', {}).get('image'):
            Response = requests.get(Image)
            if Response.status_code == 200:
                ImageFile = PIL.Image.open(BytesIO(Response.content))
                ResizedImage = ImageFile.resize((1080, 1080))
                ResizedImage.save(f'Previews/{Token["Address"]}.png')
    except:pass