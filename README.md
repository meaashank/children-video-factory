# Children's Video Factory

A ₹0-first experiment for generating short children's storytelling videos with GitHub Actions and programmatically drawn scenes.

## First milestone

The workflow renders **Milo and the Moonflower** as a vertical MP4 using:
- Python + Pillow for illustrated scenes and captions
- espeak-ng for offline narration
- FFmpeg for gentle zoom motion and audio/video assembly
- GitHub Actions artifacts for downloading the result

The first voice is deliberately offline and synthetic. This keeps the pipeline independent of paid voice APIs; voice quality can be improved later.

## Run it

1. Open the **Actions** tab in this repository.
2. Select **Generate Children's Story Video**.
3. Click **Run workflow**.
4. Keep the default title for the first test, then start the workflow.
5. Open the completed run and download the `childrens-story-video` artifact.

The artifact is retained for 7 days. Download and extract the ZIP to view the MP4.

## Important notes

- This first version is a pipeline proof, not a finished studio-quality animation.
- GitHub-hosted runner availability and usage limits depend on repository and account settings.
- The workflow is manual-only for now. Scheduled generation will be added after the first successful render.
- The workflow does not publish anything to YouTube automatically.
- Use original stories and appropriately licensed assets/audio when expanding the project.

## Local prerequisites

Python 3.12, FFmpeg, espeak-ng, and the dependencies in `requirements.txt`.
