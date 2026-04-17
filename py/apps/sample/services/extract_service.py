"""Extraction business logic — Azure Document Intelligence OCR + LLM text extraction."""

import asyncio
import base64
import logging
from functools import partial

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.identity import DefaultAzureCredential

logger = logging.getLogger(__name__)

_di_client: DocumentIntelligenceClient | None = None


def _get_di_client(endpoint: str) -> DocumentIntelligenceClient:
    """Return a cached Document Intelligence client using DefaultAzureCredential."""
    global _di_client
    if _di_client is None:
        credential = DefaultAzureCredential()
        _di_client = DocumentIntelligenceClient(endpoint, credential)
    return _di_client


def _sync_analyze(client: DocumentIntelligenceClient, image_bytes: bytes) -> str:
    """Run synchronous DI analysis — meant to be called in a thread pool."""
    poller = client.begin_analyze_document(
        "prebuilt-layout",
        AnalyzeDocumentRequest(bytes_source=image_bytes),
    )
    result = poller.result()

    parts: list[str] = []
    if result.content:
        parts.append(result.content)

    for table in result.tables or []:
        rows: dict[int, dict[int, str]] = {}
        for cell in table.cells:
            rows.setdefault(cell.row_index, {})[cell.column_index] = cell.content
        if rows:
            parts.append("\n[TABLE]")
            for ri in sorted(rows):
                cols = rows[ri]
                parts.append(" | ".join(cols.get(ci, "") for ci in sorted(cols)))
            parts.append("[/TABLE]")

    return "\n".join(parts)


async def extract_with_di(
    image_base64: str,
    di_endpoint: str,
) -> str:
    """Use Azure Document Intelligence to OCR an image and return extracted text."""
    image_bytes = base64.b64decode(image_base64)
    client = _get_di_client(di_endpoint)
    loop = asyncio.get_running_loop()
    text = await loop.run_in_executor(None, partial(_sync_analyze, client, image_bytes))
    return text
