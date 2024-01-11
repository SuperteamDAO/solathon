import qrcode
from io import BytesIO
from PIL import Image
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
import os

def create_qr(link: str, size: int = 10, background: str = 'white', color: str = 'black', border: int = 2, logo_path: str = "qr-logo.png") -> BytesIO:
    """
    Creates a QR code with the given link and returns it as a BytesIO object.

    Args:
        link (str): The link to be encoded in the QR code.
        size (int): The size of the QR code.
        background (str): The background color of the QR code.
        color (str): The color of the QR code.
        border (int): The border of the QR code.
        logo_path (str): The path to the logo image.

    """
    qr = qrcode.QRCode(
        box_size=size,
        border=border,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color=color, back_color=background, module_drawer=RoundedModuleDrawer()).convert('RGB')

    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)

    logo = Image.open(logo_path)
    logo_size_percent = 20
    logo_width = int(img.width * (logo_size_percent / 100))
    logo = logo.resize((logo_width, int(logo.size[1] * (logo_width / logo.size[0]))))

    pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
    img.paste(logo, pos)

    img_pil = Image.new("RGB", img.size, background)
    img_pil.paste(img)

    img_bytes_io = BytesIO()
    img_pil.save(img_bytes_io, format='PNG')
    img_bytes_io.seek(0)

    return img_bytes_io
