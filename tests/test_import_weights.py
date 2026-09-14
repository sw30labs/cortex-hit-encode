import os
import stat
import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "import-weights.sh"

REQUIRED = [
    "facebook/tribev2",
    "facebook/w2v-bert-2.0",
    "facebook/dinov2-large",
    "meta-llama/Llama-3.2-3B",
    "facebook/vjepa2-vitg-fpc64-256",
]


def hub_name(repo: str) -> str:
    return "models--" + repo.replace("/", "--")


def make_fake_hub(root: Path) -> Path:
    hub = root / "hub"
    for repo in REQUIRED:
        d = hub / hub_name(repo)
        d.mkdir(parents=True)
        (d / "probe.json").write_text('{"ok": true}\n')
    return hub


def test_script_is_executable():
    assert SCRIPT.is_file()
    mode = SCRIPT.stat().st_mode
    assert mode & stat.S_IXUSR


def test_help_exits_zero():
    out = subprocess.run(
        ["bash", str(SCRIPT), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0
    assert "Never calls HuggingFace" in out.stdout


def test_refuses_when_sources_missing(tmp_path):
    out = subprocess.run(
        ["bash", str(SCRIPT), "--from", str(tmp_path / "empty")],
        check=False,
        capture_output=True,
        text=True,
    )
    assert out.returncode == 1
    assert "does not download" in out.stderr or "no HF hub" in out.stderr


def test_dry_run_does_not_write(tmp_path):
    src = make_fake_hub(tmp_path / "src")
    dest = tmp_path / "dest-hub"
    out = subprocess.run(
        [
            "bash",
            str(SCRIPT),
            "--hf-src",
            str(src),
            "--hf-dest",
            str(dest),
            "--dry-run",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0, out.stderr
    assert "dry-run" in out.stdout
    assert not dest.exists() or not any(dest.iterdir())


def test_copies_required_dirs(tmp_path):
    src = make_fake_hub(tmp_path / "src")
    dest = tmp_path / "private" / "hub"
    feat_src = tmp_path / "src" / ".videocortex-cache"
    feat_src.mkdir()
    (feat_src / "features.bin").write_bytes(b"x" * 32)
    feat_dest = tmp_path / "private" / ".che-cache"

    env = os.environ.copy()
    env["HF_HOME"] = str(tmp_path / "should-not-use")
    env["CORTEX_HIT_ENCODE_CACHE"] = str(tmp_path / "should-not-use-feat")

    out = subprocess.run(
        [
            "bash",
            str(SCRIPT),
            "--hf-src",
            str(src),
            "--hf-dest",
            str(dest),
            "--feature-src",
            str(feat_src),
            "--feature-dest",
            str(feat_dest),
        ],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert out.returncode == 0, out.stderr + out.stdout
    for repo in REQUIRED:
        probe = dest / hub_name(repo) / "probe.json"
        assert probe.is_file(), repo
    assert (feat_dest / "features.bin").is_file()
    assert "never downloads" in out.stdout.lower() or "Never downloads" in out.stdout


def test_from_discovers_hub_and_feature_cache(tmp_path):
    tree = tmp_path / "videocortex-ref"
    hub = make_fake_hub(tree)
    # nest as --from/hub/...
    feat = tree / ".videocortex-cache"
    feat.mkdir()
    (feat / "x").write_text("1")
    dest = tmp_path / "hf-dest"
    feat_dest = tmp_path / "che-cache"
    out = subprocess.run(
        [
            "bash",
            str(SCRIPT),
            "--from",
            str(tree),
            "--hf-dest",
            str(dest),
            "--feature-dest",
            str(feat_dest),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0, out.stderr + out.stdout
    assert (dest / hub_name("facebook/tribev2") / "probe.json").is_file()
    assert (feat_dest / "x").is_file()
    # sanity: we discovered the nested hub
    assert str(hub) in out.stdout


def test_refuses_videocortex_named_dest(tmp_path):
    src = make_fake_hub(tmp_path / "src")
    dest = tmp_path / "videocortex" / "hub"
    out = subprocess.run(
        [
            "bash",
            str(SCRIPT),
            "--hf-src",
            str(src),
            "--hf-dest",
            str(dest),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert out.returncode == 1
    assert "VideoCortex" in out.stderr
