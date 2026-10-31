# Watercolor Diwali Market Short

A 20-second vertical 9:16 animated Diwali market scene built with Remotion and SVG artwork.

## Render locally
```bash
cd remotion
npm ci
npx remotion render src/index.ts DiwaliMarket out/diwali-watercolor-market.mp4
```

The GitHub Actions workflow renders this composition on every push that changes the Remotion project and uploads the MP4 as a downloadable workflow artifact. It uses no paid AI API; artwork is generated procedurally in code.
