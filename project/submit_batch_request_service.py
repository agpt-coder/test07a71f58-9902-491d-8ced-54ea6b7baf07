import asyncio
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class QRCodeRequest(BaseModel):
    """
    Data for generating a single QR code in a batch process, including any customization options.
    """

    data: str
    size: int
    color: str
    error_correction_level: prisma.enums.ErrorCorrectionLevel
    format: prisma.enums.QRCodeFormat


class BatchSubmitResponse(BaseModel):
    """
    Response model for when a batch submission request is successfully accepted.
    """

    batch_id: str
    message: str


async def submit_batch_request(items: List[QRCodeRequest]) -> BatchSubmitResponse:
    """
    Accepts and queues batch requests for QR code generation.

    Args:
    items (List[QRCodeRequest]): A list of data for QR code generation, including customization options.

    Returns:
    BatchSubmitResponse: Response model for when a batch submission request is successfully accepted.
    """
    batch_process = await prisma.models.BatchProcess.prisma().create(
        data={"status": "queued"}
    )
    tasks = []
    for item in items:
        task = prisma.models.QRCode.prisma().create(
            data={
                "data": item.data,
                "size": item.size,
                "color": item.color,
                "errorCorrectionLevel": item.error_correction_level,
                "format": item.format,
                "batchProcessId": batch_process.id,
            }
        )
        tasks.append(task)
    await asyncio.gather(*tasks)
    return BatchSubmitResponse(
        batch_id=batch_process.id,
        message="Your batch request has been queued for processing.",
    )
