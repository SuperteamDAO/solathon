import qrcode
from PIL import Image, ImageDraw
from io import BytesIO


def create_qr(link: str, size: int = 10, background: str = 'white', color: str = 'black') -> BytesIO:
    qr = qrcode.QRCode(
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color=color, back_color=background)

    img_pil = Image.new("RGB", img.size, background)
    img_pil.paste(img)

    img_bytes_io = BytesIO()
    img_pil.save(img_bytes_io, format='PNG')
    img_bytes_io.seek(0)
    
    return img_bytes_io