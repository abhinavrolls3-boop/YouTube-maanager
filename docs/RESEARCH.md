# Open-source choices and cost assumptions

## Selected first-stage stack
- **Python + Pillow**: draw text, cards, and simple animated scene elements.
- **imageio + imageio-ffmpeg**: encode frames into MP4 without a system-level FFmpeg install step in common CI environments.
- **Official YouTube Data API client**: optional authorized upload; OAuth and quota are required.
- **GitHub Actions**: build/test workflow plus best-effort daily preparation schedule. Runner availability and free usage are not guaranteed; publishing stays manual.

## Why not install a giant animation framework first?
The user needs a phone-controlled, ₹0 workflow. A small renderer is easier to debug and test than a large dependency stack. This output is simple motion graphics, not full rigged 2D character animation. A separate motion-control engine is a later research milestone and may exceed free CPU quotas.

## Cost statement
Code and open-source packages have no license fee for this use, but remote compute, network TTS, model inference, and YouTube API quotas have their own availability and limits. This project assumes no paid services and has no guaranteed free always-on runtime. OmniRoute can be added only after its currently available free quota and endpoint are confirmed.

## YouTube policy risk controls

The tool intentionally avoids mass public uploads. Every package is marked for human review; the uploader requires explicit human-review and originality checklist approvals, source URLs, non-public visibility, and a default limit of one upload per UTC day. Exact file hashes are checked against a best-effort local history. These checks reduce avoidable risks but cannot guarantee policy compliance or prevent a platform enforcement action. A person must ensure each video adds original educational value, verifies claims, uses licensed/original assets, and follows current YouTube monetization and spam policies.
