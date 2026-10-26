from factverse_manager.manifest import create_manifest, verify_manifest

def test_manifest_verifies_files(tmp_path):
    video = tmp_path / "sample.mp4"
    video.write_bytes(b"video bytes")
    manifest = tmp_path / "manifest.json"
    create_manifest([str(video)], manifest)
    assert verify_manifest(manifest)["ok"] is True

def test_manifest_detects_modified_file(tmp_path):
    video = tmp_path / "sample.mp4"
    video.write_bytes(b"first")
    manifest = tmp_path / "manifest.json"
    create_manifest([str(video)], manifest)
    video.write_bytes(b"changed")
    result = verify_manifest(manifest)
    assert result["ok"] is False
    assert "Hash mismatch" in result["issues"][0]
