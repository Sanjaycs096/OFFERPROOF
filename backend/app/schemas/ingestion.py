from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class UrlMetadata(BaseModel):
    submitted_url: str = Field(..., description="The original submitted URL")
    hostname: Optional[str] = Field(None, description="Extracted domain/hostname")
    scheme: Optional[str] = Field(None, description="URL protocol (http/https)")
    path: Optional[str] = Field(None, description="URL path component")


class TextIngestRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=50000, description="Raw opportunity description or message")
    url: Optional[str] = Field(None, description="Optional application or listing URL reference")
    category_hint: Optional[str] = Field("job", description="User-selected category hint: job, internship, scholarship")


class DocumentMetadata(BaseModel):
    filename: str = Field(..., description="Original filename of the document")
    file_size_bytes: int = Field(..., description="File size in bytes")
    page_count: int = Field(..., description="Total pages in document")
    title: Optional[str] = Field(None, description="Embedded document title")
    author: Optional[str] = Field(None, description="Embedded document author")


class IngestResponse(BaseModel):
    success: bool = Field(True, description="Ingestion operation success indicator")
    source_type: str = Field(..., description="Source medium: text, pdf, url_reference")
    content: str = Field(..., description="Sanitized extracted text content")
    content_length: int = Field(..., description="Length of extracted text in characters")
    url_metadata: Optional[UrlMetadata] = Field(None, description="Parsed URL components if URL provided")
    document_metadata: Optional[DocumentMetadata] = Field(None, description="Document metadata if PDF uploaded")
    message: Optional[str] = Field(None, description="Operational status or informational message")
