"""cortex-hit-encode instrument — encode, render, doctor, fetch.

Vendored from VideoCortex (https://github.com/sw30labs/videocortex)
so this experiment repo is self-contained at runtime. VideoCortex stays
an upstream *reference* only; nothing here imports a sibling checkout.

The command deck (``serve`` / web) is not vendored.
"""

__version__ = "0.1.0"
VENDOR_UPSTREAM = "https://github.com/sw30labs/videocortex"
VENDOR_COMMIT = "b34589552925338491cee8aee7087722be21c7d9"

from cortex_hit_encode.config import OverlayConfig, RenderConfig, RunConfig, VIEW_PRESETS
from cortex_hit_encode.device import describe_device, resolve_device, select_device

__all__ = [
    "__version__",
    "VENDOR_COMMIT",
    "VENDOR_UPSTREAM",
    "OverlayConfig",
    "RenderConfig",
    "RunConfig",
    "VIEW_PRESETS",
    "describe_device",
    "resolve_device",
    "select_device",
]
