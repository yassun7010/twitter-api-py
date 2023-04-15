from typing import Literal

MediaField = Literal[
    "duration_ms",
    "height",
    "media_key",
    "preview_image_url",
    "type",
    "url",
    "width",
    "public_metrics",
    "non_public_metrics",
    "organic_metrics",
    "promoted_metrics",
    "alt_text",
    "variants",
]

ALL_MEDIA_FIELDS: list[MediaField] = [
    "duration_ms",
    "height",
    "media_key",
    "preview_image_url",
    "type",
    "url",
    "width",
    "public_metrics",
    "non_public_metrics",
    "organic_metrics",
    "promoted_metrics",
    "alt_text",
    "variants",
]
