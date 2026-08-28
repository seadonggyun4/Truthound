# truthound docs themes

사용 가능한 보고서 테마를 표시합니다.

## Synopsis

```bash
truthound docs themes
```

## Description

`docs themes` 명령은 공개 Data Docs 보고서 테마만 표시합니다. Truthound의 공개 built-in 테마는 다음 세 가지입니다.

| Theme | 설명 | 적합한 용도 |
|-------|------|-------------|
| `light` | 한국 공공기관/연구용 A4 보고서 스타일이며 기본 테마 | 인쇄 보고서, 공식 검토, 연구 산출물 |
| `dark` | 같은 A4 정보 구조를 유지하는 다크 보고서 스타일 | 어두운 환경의 화면 검토 |
| `minimal` | 흑백/저채도 중심의 간결한 A4 보고서 스타일 | 내부 보고서, 흑백 인쇄 |

`default`는 `light`로 매핑되는 hidden compatibility alias입니다. `professional`과 `modern`은 한 릴리스 동안 `light`로 매핑되는 deprecated alias이며 공개 테마 목록에는 표시하지 않습니다.

## Examples

### 테마 목록 확인

```bash
truthound docs themes
```

Output:

```text
Available report themes:

  light          - Korean public/research A4 report style (default)
  dark           - Dark report style with the same A4 structure
  minimal        - Low-chroma formal A4 report style
```

### 보고서 생성

```bash
truthound docs generate profile.json -o report.html --theme light
truthound docs generate profile.json -o report-dark.html --theme dark
truthound docs generate profile.json -o report-minimal.html --theme minimal
```

## Exit Codes

| Code | 조건 |
|------|------|
| 0 | 성공 |

## Related Commands

- [`docs generate`](generate.md) - 테마를 적용해 HTML 또는 PDF 보고서 생성
