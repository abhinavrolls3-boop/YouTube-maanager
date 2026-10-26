"""Build a sample video and metadata bundle."""
import json
from pathlib import Path
from .content import SAMPLE_FACT, make_metadata
from .render import render_video

def main():
    metadata=make_metadata(SAMPLE_FACT)
    video, thumbnail=render_video(SAMPLE_FACT.title,SAMPLE_FACT.explanation)
    Path("output/metadata.json").write_text(json.dumps(metadata,indent=2),encoding="utf-8")
    print(json.dumps({"video":video,"thumbnail":thumbnail,"metadata":"output/metadata.json"},indent=2))

if __name__ == "__main__": main()