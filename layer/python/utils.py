import base64
from io import BytesIO

import qrcode
import slack
from qrcode.image.styledpil import StyledPilImage

# from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer


def generate_qr_code(data):
    # Generate QR code
    qr = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=70,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image
    img = qr.make_image(
        image_factory=StyledPilImage,
        # module_drawer=RoundedModuleDrawer()
    )

    # Save the image to a BytesIO object
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Encode the image to base64
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return img_base64


class SlackManager:
    def __init__(self, channel, token):
        self.channel = channel
        self.slack_client = slack.WebClient(token)

    def post_message(self, message):
        self.slack_client.chat_postMessage(channel=self.channel, text=message)
