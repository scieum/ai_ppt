# 플립북 설명 에셋

2026-10-28 · NotionTalk 웨비나 · 주황 #FF9228

## 파일

- `flipbook-illustration.png`: built-in `image_gen`으로 생성한 투명 배경 플립북 개념 삽화. 1536×1024 RGBA 원본을 그대로 복사했다. 실제 촬영물이나 정확한 프레임 분해도는 아니다.
- `flipbook-motion.gif`: 자체 좌표로 만든 46프레임 반복 GIF. 720×495. 앞으로 이동한 뒤 되돌아오는 루프이며 각 프레임은 기본 80ms, 양 끝은 240ms다.
- `frame-01.svg`~`frame-06.svg`: 공의 색·크기는 유지하고 위치를 조금씩 바꾼 여섯 벡터 그림.
- 같은 이름 PNG: 각 SVG에 대응하는 720×495 래스터 그림.
- `six-frame-strip.svg`: 여섯 장을 나란히 놓은 벡터 그림.
- `frames.json`: 프레임 크기·좌표·재생 시간.
- `build_frames.py`: 생성 삽화를 편집하지 않고, 별도의 자체 도형으로 프레임과 GIF를 만드는 재현 코드.

PPT의 아래 여섯 프레임은 각각 편집 가능한 종이·선·공 도형이다. 오른쪽 반복 재생은 GIF를 외부 링크 없이 PPT에 내장했다. PDF에는 첫 정지 프레임이 표시된다.

## 설명 범위

플립북은 조금씩 다른 그림을 이어 보여 주는 비유다. 모션 그래픽의 모든 프레임을 손으로 그려야 한다는 뜻은 아니다. 코드·키프레임·도구가 중간 상태를 계산할 수 있다. 특정 프레임 수나 재생 속도를 모든 영상의 필수 조건으로 설명하지 않는다.

근거: [Adobe 플립북 애니메이션](https://www.adobe.com/uk/creativecloud/animation/discover/flipbook-animation.html), [Adobe Fresco 프레임 애니메이션](https://helpx.adobe.com/ae_en/fresco/desktop/draw-paint-animate-and-share/apply-motion-to-artwork.html). 원문 이미지·예제 영상은 복사하지 않았다. 기존 G10 권리 검토 상태를 자동 통과시키지 않는다.

## 생성 기록

삽화 생성 방식: built-in `image_gen` 도구, `transparent_background=true`. CLI·외부 생성 서비스는 사용하지 않았다. 생성 원본 파일명은 `exec-ecffe9cc-d86d-4f20-8396-93f01efc6483.png`다. 프로젝트의 `assets/flipbook/20261028/flipbook-illustration.png`로 복사했고 원본을 보존했다. 연속 그림·GIF는 생성 삽화와 별개의 코드 기반 다이어그램이다.

최종 이미지 생성 프롬프트:

```text
Create a single polished 3D educational illustration asset of a physical FLIPBOOK, isolated on a genuinely transparent background, no text, no letters, no watermark, no people, no hands. A small horizontal stack of thick white paper cards held along the left edge by a subtle dark charcoal binding, shown in three-quarter isometric view, with several pages gently fanning upward as if being flipped. The pages show the SAME simple vivid orange ball (#FF9228) at slightly shifted horizontal positions, suggesting sequential drawings. Clean rounded forms, realistic paper thickness and soft subtle shadows, premium friendly 3D illustration, restrained white/charcoal/orange palette, crisp silhouette. The open pages and orange ball must be the dominant readable subject. NOT a laptop, NOT a spiral notebook, NOT a book with writing. Composition centered, landscape-ish compact object with generous transparent margin, suitable as a large cutout asset on a black Korean lecture slide. This is an illustrative physical flipbook; the precise frame sequence will be drawn separately in editable vectors.
```
