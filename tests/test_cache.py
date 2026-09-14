from pathlib import Path

from cortex_hit_encode.config import (
    FEATURE_CACHE_ENV,
    default_feature_cache,
    default_hf_hub_cache,
    hf_hub_dirname,
    local_hf_repo_dir,
)


def test_feature_cache_defaults_to_dot_che_cache(monkeypatch):
    monkeypatch.delenv(FEATURE_CACHE_ENV, raising=False)
    assert default_feature_cache() == Path(".che-cache")


def test_feature_cache_honors_env(monkeypatch, tmp_path):
    monkeypatch.setenv(FEATURE_CACHE_ENV, str(tmp_path / "mine"))
    assert default_feature_cache() == tmp_path / "mine"


def test_hf_hub_cache_honors_huggingface_hub_cache(monkeypatch, tmp_path):
    monkeypatch.setenv("HUGGINGFACE_HUB_CACHE", str(tmp_path / "hub"))
    monkeypatch.setenv("HF_HOME", str(tmp_path / "ignored"))
    assert default_hf_hub_cache() == tmp_path / "hub"


def test_hf_hub_cache_honors_hf_home(monkeypatch, tmp_path):
    monkeypatch.delenv("HUGGINGFACE_HUB_CACHE", raising=False)
    monkeypatch.setenv("HF_HOME", str(tmp_path / "hf"))
    assert default_hf_hub_cache() == tmp_path / "hf" / "hub"


def test_hf_hub_dirname():
    assert hf_hub_dirname("facebook/tribev2") == "models--facebook--tribev2"
    assert hf_hub_dirname("meta-llama/Llama-3.2-3B") == "models--meta-llama--Llama-3.2-3B"


def test_local_hf_repo_dir_requires_nonempty(tmp_path):
    empty = tmp_path / "models--facebook--tribev2"
    empty.mkdir()
    assert local_hf_repo_dir("facebook/tribev2", tmp_path) is None
    (empty / "config.yaml").write_text("ok")
    assert local_hf_repo_dir("facebook/tribev2", tmp_path) == empty
