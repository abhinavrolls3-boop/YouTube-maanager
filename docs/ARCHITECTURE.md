# Architecture

## Pipeline
1. Deterministic starter facts so the first render does not require a model API.
2. Validate script fields before rendering.
3. Pillow draws lightweight animated cards/shapes; imageio-ffmpeg encodes MP4. This is motion graphics, not advanced character animation or motion-control generation.
4. Generate thumbnail and metadata sidecar.
5. Optional official YouTube Data API upload using OAuth; disabled by default.
6. Log each run and prevent duplicate uploads before public scheduling.

## Free-tier reality
No free cloud runner is guaranteed. GitHub Actions is a manual proof-of-concept until this repository's runner access and repeated runs are verified. No 24/7 compute is required, but scheduled execution is best-effort.

## OmniRoute
Integrate only after confirming its exact endpoint format, supported model, free quota, and terms. The renderer must work without model API access. Never put keys in source code.

## Future
Keep scripts, rendering, upload, analytics, and scheduling separate. Use official/permitted data sources and never automate fake engagement.