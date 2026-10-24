# Children's Video Factory

A ₹0-first experiment for generating original children's story shorts with GitHub Actions.

## Current prototype

The manual workflow renders **Milo and the Moonflower** as a 9:16 MP4. It uses:
- Python + Pillow to draw original forest backgrounds and characters frame by frame
- Small procedural movements, including Milo's movement, Pip appearing in later scenes, and a pulsing flower glow/sparkles
- espeak-ng for offline synthetic narration
- FFmpeg to assemble scene clips and audio
- GitHub Actions artifacts to deliver the finished MP4

This is an improvement over a still-image slideshow, but it is still a lightweight 2D prototype—not professional animation. Character motion is procedural and limited, and the voice is synthetic.

## Generate a video

1. Open the **Actions** tab.
2. Choose **Generate Children's Story Video**.
3. Click **Run workflow** and leave the default title for the first test.
4. Open the completed run and download the `childrens-story-video` artifact.
5. Extract the downloaded ZIP to find `childrens_story.mp4`.

Artifacts are retained for 7 days. This workflow is manual-only and does not publish to YouTube.

## Cost and limitations

- The workflow uses free/open-source tools and does not call paid AI APIs.
- GitHub-hosted runner availability and usage limits depend on repository/account settings.
- This version has a fixed sample story. The title changes, but the story dialogue does not yet generate dynamically.
- Original stories and properly licensed audio/assets should be used when expanding the project.

## Local prerequisites

Python 3.12, FFmpeg, espeak-ng, and the dependency in `requirements.txt`.
