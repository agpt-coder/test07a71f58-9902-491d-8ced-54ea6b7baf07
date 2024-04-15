import logging
from contextlib import asynccontextmanager
from typing import List, Optional

import project.generate_qr_code_service
import project.submit_batch_request_service
import project.submit_data_for_qr_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="test",
    lifespan=lifespan,
    description="The project involves creating an API endpoint that accepts various forms of data, notably URLs, text, and contact information, for the purpose of QR code generation. The user prefers the encoded data to be in the form of a URL to facilitate directing users to specific webpages, aiming for efficient and user-friendly interactions. A significant requirement is the ability to customize the generated QR codes. Customization options include adjustments to the QR code's size, making it larger for enhanced readability, color modifications for improved contrast, and a higher error correction level to maintain scannability even when partially obscured or damaged. The output format for the generated QR code is specified as SVG, aligning with the user's needs for quality and scalability. The technical stack selected for this task consists of Python as the programming language, with FastAPI as the API framework, PostgreSQL for the database, and Prisma as the Object-Relational Mapping (ORM) system. This stack supports the development of efficient, scalable, and maintainable applications, fitting the project's requirements for a robust and responsive QR code generation service.",
)


@app.post(
    "/batchSubmit",
    response_model=project.submit_batch_request_service.BatchSubmitResponse,
)
async def api_post_submit_batch_request(
    items: List[project.submit_batch_request_service.QRCodeRequest],
) -> project.submit_batch_request_service.BatchSubmitResponse | Response:
    """
    Accepts and queues batch requests for QR code generation.
    """
    try:
        res = await project.submit_batch_request_service.submit_batch_request(items)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/submitData",
    response_model=project.submit_data_for_qr_service.QRCodeGenerationResponse,
)
async def api_post_submit_data_for_qr(
    data: str,
    size: Optional[int],
    color: Optional[str],
    error_correction_level: Optional[str],
    format: Optional[str],
) -> project.submit_data_for_qr_service.QRCodeGenerationResponse | Response:
    """
    Accepts data to be encoded in a QR code.
    """
    try:
        res = await project.submit_data_for_qr_service.submit_data_for_qr(
            data, size, color, error_correction_level, format
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/generateQR",
    response_model=project.generate_qr_code_service.QRCodeGenerationResponse,
)
async def api_post_generate_qr_code(
    color: str, errorCorrectionLevel: str, logo: Optional[str], data: str, size: int
) -> project.generate_qr_code_service.QRCodeGenerationResponse | Response:
    """
    Generates a customized QR code based on input data.
    """
    try:
        res = project.generate_qr_code_service.generate_qr_code(
            color, errorCorrectionLevel, logo, data, size
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
