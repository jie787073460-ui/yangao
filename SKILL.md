---
name: yangao
description: Launch and use Yangao, a local browser-based UI fidelity inspection tool for designers. Use when the user wants to compare a design mockup with a frontend implementation screenshot, detect visible pixel differences, annotate the implementation with red boxes and arrows, review issues by severity, or export an annotated PNG and Markdown repair checklist. All image processing stays on the local device.
---

# yangao

Open the bundled local app for comparing one design image with one frontend implementation image. Keep all screenshots in browser memory and never upload them.

Before performing a direct image audit or changing the app's comparison contract, read `references/inspection-protocol.md` completely. Follow its category priority, objective-only rules, integer coordinate requirements, severity scale, and exact JSON schema. Do not invent font names, CSS values, or hidden-element properties that cannot be established from visible pixels.

## Launch

1. Run `python3 scripts/launch.py` from this skill directory.
2. Read the exact loopback URL printed by the script; do not assume a fixed port.
3. Open that URL in the in-app browser when the user asks to open, launch, use, or demo the tool.
4. Return the clickable local URL and mention that the local service must remain running.

If launch fails, inspect the reported port or permission error. Do not replace this workflow with a hosted service.

## Product behavior

- Accept PNG, JPEG, and WebP images for the design and implementation.
- Enable `一键走查` only after both images are loaded.
- Analyze differences locally with deterministic pixel-region comparison across all nine protocol categories: `颜色`, `尺寸`, `位置`, `文字`, `圆角`, `阴影`, `边框`, `图标`, and `布局`.
- Use fine, component, and layout-scale scans that combine color and edge-structure evidence; do not rely on one downsampled grid.
- Localize every annotation against the implementation image's visible edge bounds instead of exposing raw scan-cell bounds. Bridge very small horizontal gaps before creating text regions, absorb tiny detections that sit inside or immediately beside a confirmed text line, and do not label an isolated pixel fragment as a complete icon when its owning element cannot be established.
- Track significant-difference coverage and rescan uncovered regions instead of discarding results behind a fixed region or issue-count limit.
- Build an inferred comparison profile from screenshot dimensions: exact-pixel for matching widths, responsive normalization for compatible differing widths, and conservative comparison when scale or crop confidence is low. Surface the mode and confidence instead of inventing device metadata.
- For portrait mobile screenshots, exclude the inferred top system-status-bar band from difference masks and annotations; time, signal, Wi-Fi, battery, and transient status indicators are not fidelity issues. Apply a second mandatory result-level filter before grouping so status-bar-only regions cannot re-enter through responsive normalization or region merging. Exclude them from on-screen counts, canvas annotations, PNG, Markdown, and JSON.
- Treat text as fixed copy by default. Ignore a dynamic value's content only when an explicit page marker, comparison manifest, or user-defined region declares it dynamic; still inspect that region's typography, color, size, position, and container styling.
- Allow a changed region to produce both a color issue and one independently evidenced structural issue; never force every result into the color category.
- Consolidate spatially equivalent detections into one visible issue group across categories and scan scales. Treat nested boxes on the same text line or button as the same visual element even when their areas differ substantially, and merge tightly adjacent same-size glyph fragments into one text object. Treat a photo, illustration, product image, avatar, or large icon as one visual object: its internal color patches and contour fragments must be absorbed by the object's outer annotation instead of producing child boxes. Run the final grouping pass repeatedly until no text or image fragments can be merged further. One visual element must produce one canvas box and one group number; color, size, border, and other findings become sub-issues inside that group instead of additional annotations. Merge a main label with nearby same-row helper copy into one text group. Keep a leading icon and trailing action icon as separate visible groups, so a typical list row yields three clear annotations: left icon, title/helper copy, and right action. Require compatible vertical alignment, compact height, and a very tight gap for glyph merging so distant menu items or icons do not collapse together. Preserve every objective sub-issue inside the grouped export record.
- Describe grouped findings by inferred visible sub-element role (`左侧图标`, `主标题`, `辅助文字`, `右侧操作图标`, or `整行容器`) instead of generic machine regions. Convert size and position values into plain directional language such as `比设计稿窄 13px、矮 8px` or `比设计稿向左偏 11px、向下偏 11px`.
- Keep designer-facing copy in the page, annotated PNG, and Markdown direct and non-technical. Do not show terms such as `重心`, `轮廓密度`, `边界占比`, or `柔和外缘像素`; explain what is visibly wrong and how it differs from the design. Retain raw measurement terminology only in the protocol-compliant JSON for machine use.
- Provide three canvas comparison modes: annotated implementation, side-by-side design/implementation, and opacity overlay with an adjustable design-layer opacity.
- Keep issue annotations on the implementation image in every comparison mode. In PNG export, preserve the implementation image at its original pixel size and append a dedicated problem-list panel to its right.
- Show the implementation image on a Canvas with red boxes, arrows, and readable labels.
- Group issue groups as `严重`, `中等`, and `轻微`; selecting a group must focus its single annotation and expose its category sub-issues.
- Make PNG, Markdown, and JSON consume the same final filtered issue groups. Export only `严重` and `中等` groups; keep `轻微` findings available on screen but omit them from all export files. Export a readable review-board PNG with the original-size annotated implementation image on the left and a compact, matching group-ID problem list on the right. Include every exported `严重` and `中等` group in the PNG instead of capping the list, and keep the panel readable with severity sections, cards, and wrapped plain-language descriptions. Markdown must list each group once and keep its sub-issues beneath it. JSON must remain protocol-compliant and emit one record per visible group: use the highest-priority category in `type`, keep the group box in `bbox`, and combine all category-specific design values, implementation values, and plain-language findings into the existing string fields.
- Export a concise Markdown repair checklist grouped by severity.
- Export structured JSON that exactly follows `references/inspection-protocol.md`.
- Treat the analysis as a local visual-difference aid, not as a replacement for designer review.
- Ignore anti-aliasing-sized noise and very small isolated regions.
- Do not claim that the app invokes a cloud model or uploads images.

## Bundled resources

- `scripts/launch.py`: start a reusable loopback-only static server.
- `assets/app/index.html`: complete dependency-free interactive app.
- `references/inspection-protocol.md`: mandatory comparison priorities and JSON output contract.
