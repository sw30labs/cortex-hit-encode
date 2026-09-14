import pytest

from cortex_hit_encode.cli import build_parser


def test_render_requires_a_stimulus():
    with pytest.raises(SystemExit):
        build_parser().parse_args(["render"])


def test_render_rejects_two_stimuli():
    with pytest.raises(SystemExit):
        build_parser().parse_args(["render", "--video", "a.mp4", "--text", "b.txt"])


def test_render_defaults_are_laptop_shaped():
    a = build_parser().parse_args(["render", "--video", "clip.mp4"])
    # Upstream ships batch_size=8 / num_workers=20, tuned for a Slurm node.
    assert a.batch_size == 1
    assert a.num_workers == 0
    assert a.device == "auto"
    assert a.views == "standard"
    # slots dataclass trap: RunConfig.checkpoint is a member_descriptor.
    assert a.checkpoint == "facebook/tribev2"
    assert isinstance(a.checkpoint, str)
    # Feature cache is resolved at run time from env / ./.che-cache
    assert a.cache_dir is None


def test_render_accepts_audio_primary():
    a = build_parser().parse_args(["render", "--audio", "track.wav"])
    assert a.audio.name == "track.wav"
    assert a.video is None


def test_draw_needs_no_model_arguments():
    a = build_parser().parse_args(["draw", "runs/clip/predictions.npy", "--views", "full"])
    assert a.command == "draw"
    assert a.views == "full"
    assert not hasattr(a, "device")


def test_doctor_offline_flag():
    assert build_parser().parse_args(["doctor", "--offline"]).offline is True


def test_doctor_renderer_flag():
    a = build_parser().parse_args(["doctor", "--renderer"])
    assert a.renderer is True
    assert a.offline is False


def test_overlay_requires_run():
    with pytest.raises(SystemExit):
        build_parser().parse_args(["overlay"])


def test_overlay_defaults_match_the_spec():
    a = build_parser().parse_args(["overlay", "--run", "runs/clip"])
    assert a.command == "overlay"
    assert a.position == "top-right"
    assert a.lag_mode == "stimulus"
    assert a.label == "time"
    assert a.size == 0.24
    assert a.views == "standard"
    assert a.stride == 1
    assert not a.fast
    assert not a.spin
    assert a.dps == 24.0


def test_overlay_spin_flag():
    a = build_parser().parse_args(["overlay", "--run", "runs/clip", "--spin", "--dps", "18"])
    assert a.spin is True
    assert a.dps == 18.0
    assert a.fps == 24.0
    assert a.az_step == 2


def test_no_serve_command():
    with pytest.raises(SystemExit):
        build_parser().parse_args(["serve"])


def test_prog_is_che():
    assert build_parser().prog == "che"
