"""模型下载源切换工具。

本模块集中管理 HuggingFace Hub 相关环境变量，避免各个模型后端重复处理
下载源选择。当前支持官方 HuggingFace（HF）和 ModelScope（MS）两个入口。
"""

from __future__ import annotations

import logging
import os
from typing import Literal

ModelDownloadSource = Literal["hf", "ms"]

HF_SOURCE: ModelDownloadSource = "hf"
MS_SOURCE: ModelDownloadSource = "ms"
DEFAULT_SOURCE: ModelDownloadSource = MS_SOURCE

HF_ENDPOINT = "https://huggingface.co"
MS_ENDPOINT = "https://www.modelscope.cn"

SOURCE_LABELS: dict[str, str] = {
    HF_SOURCE: "HuggingFace",
    MS_SOURCE: "ModelScope",
}

SOURCE_ENDPOINTS: dict[str, str] = {
    HF_SOURCE: HF_ENDPOINT,
    MS_SOURCE: MS_ENDPOINT,
}

logger = logging.getLogger(__name__)


def normalize_model_download_source(source: str | None) -> ModelDownloadSource:
    """把用户输入规整为受支持的下载源枚举。"""
    normalized = (source or DEFAULT_SOURCE).strip().lower()
    if normalized not in SOURCE_ENDPOINTS:
        raise ValueError(f"Unsupported model download source: {source}")
    return normalized  # type: ignore[return-value]


def get_model_download_source_label(source: str | None) -> str:
    """返回用于进度提示的下载源名称。"""
    return SOURCE_LABELS[normalize_model_download_source(source)]


def get_current_model_download_source() -> ModelDownloadSource:
    """根据当前环境变量推断正在使用的下载源。"""
    endpoint = os.environ.get("HF_ENDPOINT", MS_ENDPOINT).rstrip("/")
    for source, source_endpoint in SOURCE_ENDPOINTS.items():
        if endpoint == source_endpoint.rstrip("/"):
            return normalize_model_download_source(source)
    return DEFAULT_SOURCE


def get_current_model_download_source_label() -> str:
    """返回当前进程正在使用的下载源名称。"""
    return SOURCE_LABELS[get_current_model_download_source()]


def apply_model_download_source(source: str | None) -> ModelDownloadSource:
    """应用模型下载源到当前进程。

    HuggingFace Hub 在导入后会缓存部分常量，所以这里同时更新环境变量和
    已导入模块中的 endpoint 常量。这样后续 `from_pretrained` /
    `snapshot_download` 会尽量使用最新选择的源。
    """
    normalized = normalize_model_download_source(source)
    endpoint = SOURCE_ENDPOINTS[normalized]

    os.environ["HF_ENDPOINT"] = endpoint

    try:
        import huggingface_hub.constants as hf_constants

        if hasattr(hf_constants, "ENDPOINT"):
            hf_constants.ENDPOINT = endpoint
        if hasattr(hf_constants, "HUGGINGFACE_CO_URL_TEMPLATE"):
            hf_constants.HUGGINGFACE_CO_URL_TEMPLATE = (
                endpoint + "/{repo_id}/resolve/{revision}/{filename}"
            )
    except Exception as exc:
        logger.debug("Could not patch HuggingFace endpoint constants: %s", exc)

    logger.info("Model download source: %s (%s)", SOURCE_LABELS[normalized], endpoint)
    return normalized
