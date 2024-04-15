from typing import Optional

from pydantic import BaseModel


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


async def submit_data_for_qr(
    data: str,
    size: Optional[int] = None,
    color: Optional[str] = None,
    error_correction_level: Optional[str] = None,
    format: Optional[str] = None,
) -> QRCodeGenerationResponse:
    """
    Accepts data to be encoded in a QR code.

    This functionality has been designed assuming integration with a QR code generation service or library
    that supports the required features. Since the use of external libraries (like qrcode) or services is not allowed
    in this context, this function will return a mocked response demonstrating how you would structure the response
    based on function inputs.

    Args:
        data (str): The data to be encoded into the QR code. This could be a URL, text, or contact information.
        size (Optional[int]): Optional. The desired size of the QR code (in pixels).
        color (Optional[str]): Optional. The desired color of the QR code. Should be specified in hex format.
        error_correction_level (Optional[str]): Optional. The desired error correction level for the QR code.
                                                Valid values are L, M, Q, and H.
        format (Optional[str]): Optional. The desired output format for the QR code. Valid values are PNG and SVG.

    Returns:
        QRCodeGenerationResponse: Response model for the QR code generation request. Contains the generated QR code
                                  in the specified format and any relevant metadata.
    """
    mock_qr_code = "base64-encoded-image-string-goes-here"
    size = size if size is not None else 200
    color = color if color is not None else "#000000"
    error_correction_level = (
        error_correction_level if error_correction_level is not None else "M"
    )
    format = format if format is not None else "SVG"
    response = QRCodeGenerationResponse(
        qr_code=mock_qr_code,
        data=data,
        size=size,
        color=color,
        errorCorrectionLevel=error_correction_level,
        logo=None,
    )
    return response
