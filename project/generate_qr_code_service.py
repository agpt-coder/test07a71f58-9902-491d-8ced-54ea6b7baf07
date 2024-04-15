from typing import Optional

import qrcode
from pydantic import BaseModel
from qrcode.image.pil import PilImage


class QRCodeGenerationResponse(BaseModel):
    """
    Response model for the QR code generation request. Contains the generated QR code in the specified format and any relevant metadata.
    """

    qr_code: str
    data: str
    size: int
    color: str
    errorCorrectionLevel: str
    logo: Optional[str] = None


def _embed_logo(qr_img: PilImage, logo: str, qr_size: int) -> PilImage:
    """
    Embeds a logo image at the center of the QR code.

    Args:
        qr_img (PilImage): The PIL image object of the generated QR code.
        logo (str): The path to the logo image to embed.
        qr_size (int): The size of the QR code image.

    Returns:
        PilImage: The QR code image with the logo embedded.
    """
    from PIL import Image

    logo_img = Image.open(logo)
    logo_img = logo_img.resize((qr_size // 5, qr_size // 5))
    qr_img.paste(
        logo_img,
        ((qr_size - logo_img.size[0]) // 2, (qr_size - logo_img.size[1]) // 2),
        logo_img,
    )
    return qr_img


def generate_qr_code(
    color: str, errorCorrectionLevel: str, logo: Optional[str], data: str, size: int
) -> QRCodeGenerationResponse:
    """
    Generates a customized QR code based on input data.

    Args:
        color (str): The color of the QR code. This is typically in hex format.
        errorCorrectionLevel (str): The error correction level of the QR code, affecting its resilience to errors.
                                    Values can be 'L', 'M', 'Q', 'H'.
        logo (Optional[str]): An optional logo to embed in the center of the QR code. Provide a URL or path to the image.
        data (str): The data to be encoded into the QR code. This could be a URL, text, or contact information.
        size (int): The desired size of the QR code in pixels.

    Returns:
        QRCodeGenerationResponse: Response model for the QR code generation request. Contains the generated QR code
                                  in the specified format and any relevant metadata.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=getattr(
            qrcode.constants, f"ERROR_CORRECT_{errorCorrectionLevel}"
        ),
        box_size=size // 30,
        border=4,
    )  # TODO(autogpt): "QRCode" is not a known member of module "qrcode". reportAttributeAccessIssue
    #   Found documentation for the module:
    #    To fix the error """"QRCode" is not a known member of module "qrcode". reportAttributeAccessIssue""", you need to ensure you are importing `QRCode` correctly from the `qrcode` module. The correct import statement is:
    #
    #   ```python
    #   import qrcode
    #   ```
    #
    #   And to create a QRCode object, use:
    #
    #   ```python
    #   qr = qrcode.QRCode(
    #       version=1,
    #       error_correction=qrcode.constants.ERROR_CORRECT_L,
    #       box_size=10,
    #       border=4,
    #   )
    #   ```
    #
    #   Make sure you are using `qrcode` in a manner consistent with its documentation, such as initializing a QRCode object with its options like version, error_correction, box_size, and border, then adding data and generating an image with those specifications.
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=color, back_color="white").convert("RGB")
    if logo:
        qr_img = _embed_logo(qr_img, logo, size)
    from io import BytesIO

    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    img_str = buffer.getvalue()
    response = QRCodeGenerationResponse(
        qr_code=img_str,
        data=data,
        size=size,
        color=color,
        errorCorrectionLevel=errorCorrectionLevel,
        logo=logo,
    )
    return response
