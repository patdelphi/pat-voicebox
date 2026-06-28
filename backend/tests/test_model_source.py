"""模型下载源切换的单元测试。

验证 HF / ModelScope 两种下载源会正确写入 HuggingFace Hub 使用的
endpoint 环境变量，避免设置页切换后仍访问旧源。
"""

import os

from backend.utils.model_source import (
    HF_ENDPOINT,
    MS_ENDPOINT,
    apply_model_download_source,
    get_current_model_download_source,
    normalize_model_download_source,
)


def test_apply_hf_source_sets_official_endpoint(monkeypatch):
    monkeypatch.delenv("HF_ENDPOINT", raising=False)

    source = apply_model_download_source("hf")

    assert source == "hf"
    assert get_current_model_download_source() == "hf"
    assert os.environ["HF_ENDPOINT"] == HF_ENDPOINT


def test_apply_ms_source_sets_modelscope_endpoint(monkeypatch):
    monkeypatch.delenv("HF_ENDPOINT", raising=False)

    source = apply_model_download_source("ms")

    assert source == "ms"
    assert get_current_model_download_source() == "ms"
    assert os.environ["HF_ENDPOINT"] == MS_ENDPOINT
    assert MS_ENDPOINT != HF_ENDPOINT


def test_empty_source_defaults_to_modelscope(monkeypatch):
    monkeypatch.delenv("HF_ENDPOINT", raising=False)

    source = apply_model_download_source(None)

    assert source == "ms"
    assert get_current_model_download_source() == "ms"
    assert os.environ["HF_ENDPOINT"] == MS_ENDPOINT


def test_invalid_source_is_rejected():
    try:
        normalize_model_download_source("bad")
    except ValueError as exc:
        assert "Unsupported model download source" in str(exc)
    else:
        raise AssertionError("invalid source should raise ValueError")
