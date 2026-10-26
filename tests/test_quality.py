import json
from PIL import Image
from factverse_manager.quality import validate_package

def test_valid_package_passes_with_human_review_flag(tmp_path):
    video=tmp_path/"clip.mp4"; video.write_bytes(b"fake mp4 bytes")
    thumb=tmp_path/"thumb.png"; Image.new("RGB",(720,1280)).save(thumb)
    metadata=tmp_path/"metadata.json"
    metadata.write_text(json.dumps({"title":"Fact","description":"A fact.","tags":["science"]}))
    result=validate_package(video,thumb,metadata)
    assert result["ok"]
    assert result["human_review_required"]

def test_empty_title_fails(tmp_path):
    video=tmp_path/"clip.mp4"; video.write_bytes(b"x")
    thumb=tmp_path/"thumb.png"; Image.new("RGB",(10,10)).save(thumb)
    metadata=tmp_path/"metadata.json"
    metadata.write_text(json.dumps({"title":" ","description":"Desc","tags":[]}))
    result=validate_package(video,thumb,metadata)
    assert not result["ok"]
    assert any("title" in issue.lower() for issue in result["issues"])
