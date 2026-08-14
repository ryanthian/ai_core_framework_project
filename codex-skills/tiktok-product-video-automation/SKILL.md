---
name: tiktok-product-video-automation
description: Use this skill when the user wants to create TikTok product video content from a product image and product details, including Bahasa Melayu scene overview, 8-second dialogue scripts, ultra-realistic image generation prompts, and Google Flow AI video prompts scene by scene.
---

# TikTok Product Video Automation

Use this workflow for Malay TikTok product videos built from a product image.

## Required Input

Ask for missing fields using this form:

```text
Nama produk:
Kelebihan utama produk:
Masalah yang produk selesaikan:
Sasaran pengguna:
Jumlah scene:
Tujuan video:
Watak:
Gaya bercakap:
Lokasi utama:
```

If a product image is required but not attached, ask the user to upload it.

## Global Rules

- 1 scene equals 8 seconds.
- Dialogue must be Bahasa Melayu only.
- Character speaks directly to camera.
- No narration.
- No subtitles.
- No watermark.
- No visible text in generated images.
- Dialogue must sound natural, like talking to a friend.
- Keep copy short, clear, and easy to understand.
- Generate only one scene at a time for images and video prompts unless the user asks for all.
- Keep character, lighting, color tone, framing, and emotional style consistent across scenes.

## Step 1: Overview and Script

Trigger phrases include:

- `GENERATE OVERVIEW`
- `buat overview`
- `generate skrip`
- `buat semua scene`

Create all scene overviews and scripts according to the requested number of scenes.

Use this exact format:

```text
Scene 1 (8 saat)
[Overview scene]
Dialog: "[Skrip dialog]"

Scene 2 (8 saat)
[Overview scene]
Dialog: "[Skrip dialog]"
```

Continue until complete. Then stop and wait for approval.

## Step 2: Ultra-Realistic Image Prompt

Trigger phrases include:

- `IMAGE SCENE 1`
- `gambar scene 1`
- `generate image scene 1`
- `NEXT SCENE` when the active mode is image generation

Generate one image prompt for the requested scene based on the approved overview and script.

Image prompt requirements:

- 9:16 vertical cinematic framing.
- Ultra-realistic, high detail, 4K cinematic look.
- Realistic skin texture, natural pores, no plastic effect.
- Professional lighting with soft key light and practical warm background light.
- Realistic depth of field, slightly blurred background.
- Natural color grading with slightly warm cinematic tone.
- 35mm film-style camera angle and shallow depth feel.
- Environment feels alive with real-world texture.
- Product is realistic, proportionate, and not oversized.
- Facial expression and emotion are clear.
- Framing is suitable for TikTok portrait video.
- No writing, no subtitle, no watermark, no visible text.

Output only the image prompt unless the user explicitly asks for explanation.

If the user asks to actually create the image, use the available image generation tool and generate the image directly.

## Step 3: Google Flow AI Video Prompt

Trigger phrases include:

- `VIDEO PROMPT SCENE 1`
- `Flow prompt scene 1`
- `prompt video scene 1`
- `NEXT SCENE` when the active mode is video prompt generation

Generate one Google Flow AI prompt for the requested scene based on the approved overview and script.

Rules:

- Environment description in English.
- Lighting and camera movement in English.
- Character action and facial expression in English.
- Dialogue in Bahasa Melayu only.
- No narration.
- No subtitles.
- Character speaks directly to camera.
- Dialogue must fit 8 seconds at natural pacing.
- Do not use labels such as `Malay dialogue:`.
- Do not add explanation outside the prompt.
- Output must be directly copy-paste ready for Google Flow AI.

Prompt structure:

```text
[Scene environment description in English.]
[Lighting and camera movement in English.]
[Character action and facial expression in English.]
"[Bahasa Melayu dialogue only.]"
```

## Scene Tracking

Remember the latest approved overview and script within the current conversation.

When the user says `NEXT SCENE`:

- If the previous output was an image prompt or generated image, continue to the next image scene.
- If the previous output was a Google Flow AI video prompt, continue to the next video prompt scene.
- Preserve visual and emotional consistency.

If there is no approved overview yet, generate or request approval for the overview before creating image or video prompts.

