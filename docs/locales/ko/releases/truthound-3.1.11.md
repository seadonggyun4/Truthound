# Truthound 3.1.11 릴리스 노트

## 핵심 변경

Truthound 3.1.11은 PyPI의 3.1.10 릴리스 슬롯이 이미 사용된 상태에서, 한국형
A4 Data Docs 보고서 엔진 변경분을 새 패키지 버전으로 배포하기 위한 릴리스입니다.
검증 런타임의 계산 의미는 유지하면서, HTML/PDF 보고서 산출물을 공공기관 및
연구용 데이터 품질 검토에 더 적합한 형태로 정리했습니다.

## Data Docs 보고서

- 공개 보고서 테마는 `light`, `dark`, `minimal` 세 가지만 유지합니다.
- `default`는 `light`의 숨김 alias로 보존하고, `professional`과 `modern`은
  호환성을 위한 deprecated alias로 유지합니다.
- 표지 메타데이터, 요약문, 표가 아닌 목차, 장/절 번호, 부록, 표, 그림, 캡션,
  방법론 메모, 품질 차원 해석을 포함하는 구조화된 보고서 렌더링을 제공합니다.
- 내장 보고서 UI와 라벨은 한국어로 렌더링하면서, 사용자가 전달한 제목, 데이터
  출처, 원본 컬럼명은 그대로 보존합니다.

## 검증과 패키징

- 테마 정책, 한국어 보고서 구조, 시각 marker, PDF export smoke, 샘플 bundle
  계약, 패키지 artifact 포함 여부를 릴리스 준비 검증에 포함합니다.
- 새 보고서 엔진 모듈이 wheel과 source distribution에 포함되는지 확인합니다.
- `th.check()`, `ValidationRunResult`, profile, drift, anomaly, 데이터 품질 계산
  의미는 변경하지 않습니다.

## 사용법

```python
from truthound.datadocs import generate_html_report, export_to_pdf

generate_html_report(profile, title="데이터 품질 분석 보고서", theme="light", language="ko")
export_to_pdf(profile, "report-ko.pdf", title="데이터 품질 분석 보고서", language="ko")
```

같은 보고서 구조를 어두운 팔레트로 보려면 `theme="dark"`를, 흑백/저채도 공문서형
스타일로 보려면 `theme="minimal"`을 사용합니다.
