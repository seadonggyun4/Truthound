# Truthound 3.1.8 릴리스 노트

## 핵심 변경

Truthound 3.1.8은 Data Docs 보고서를 한국 공공기관/연구용 A4 보고서 스타일로
승격합니다. HTML과 PDF-ready 산출물은 A4 페이지 크기, 한국어 폰트 stack,
조밀한 표, 요약 박스, 캡션, 인쇄 break 제어를 공유하는 보고서 레이아웃 체계를
사용합니다.

이번 릴리스에서는 공개 built-in theme도 `light`, `dark`, `minimal` 3개로
정리했습니다. `light`는 기본 A4 보고서 스타일이고, `dark`는 같은 정보 구조를
저휘도 palette로 표현하며, `minimal`은 흑백/저채도 중심의 간결한 공문서형
스타일을 제공합니다.

## Theme 호환성

공개 theme 목록에는 다음 3개만 노출됩니다.

- `light`
- `dark`
- `minimal`

`default`는 기존 사용자 호환성을 위해 숨겨진 `light` alias로 유지됩니다.
`professional`, `modern`은 한 릴리스 동안 deprecated alias로 유지되며 사용할 때
warning을 발생시킵니다. Custom YAML, JSON, dictionary theme loader 동작은
변경하지 않았습니다.

## A4 보고서 산출물

Data Docs renderer는 browser HTML과 PDF-ready HTML 모두에 공유 A4 보고서
stylesheet를 제공합니다.

- mm/pt 단위 기반 A4 portrait page shell
- `맑은 고딕`, `Malgun Gothic`, `돋움`, `sans-serif` 순서의 한국어 우선 font stack
- 네이비 계열 보고서 제목과 표 header
- 얇은 선과 조밀한 cell padding을 사용하는 collapsed report table
- 재사용 가능한 summary box와 figure caption
- print/PDF를 위한 `@page`, page-break, table, figure, summary break 제어

Validation runtime, `th.check()` 결과 모델, profiler, drift, anomaly, 데이터 품질
계산 의미는 변경하지 않았습니다.

## Visual/PDF Smoke Coverage

Data Docs는 모든 공개 theme에 대해 deterministic visual smoke fixture를 갖습니다.
테스트는 깨지기 쉬운 binary golden image 대신 안정적인 structural marker를
검증하므로, 스냅샷 관리 비용 없이 레이아웃 회귀를 잡을 수 있습니다.

WeasyPrint와 시스템 라이브러리를 사용할 수 있는 환경에서는 PDF smoke test가
실제 PDF를 생성하고 PDF header, 최소 파일 크기, 텍스트 추출을 검증합니다.
Poppler가 있으면 첫 페이지를 PNG로 렌더링하는 smoke도 수행할 수 있습니다.

PDF coverage가 skip되면 안 되는 CI 환경에서는 다음 flag를 설정합니다.

```bash
TRUTHOUND_DATADOCS_REQUIRE_PDF_SMOKE=1
TRUTHOUND_DATADOCS_REQUIRE_PDF_RENDER=1
```

## 소비자 업그레이드 Gate

소비자는 공개 배포된 3.1.8 wheel을 설치하고 `truthound.__version__`을 확인한 뒤
대표 Data Docs HTML/PDF 보고서를 다시 생성해야 합니다. 또한 공개 theme 목록이
`light`, `dark`, `minimal`만 포함하는지 확인해야 합니다. Source checkout이나
배포되지 않은 wheel은 소비자 인증 증거가 아닙니다.
