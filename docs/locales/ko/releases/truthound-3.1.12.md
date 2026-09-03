# Truthound 3.1.12 릴리스 노트

## 핵심 변경

Truthound 3.1.12는 Lazy DataFrame 입력의 자동 스키마 캐시를 수정합니다.
서로 다른 lazy schema에 서로 다른 캐시 identity를 부여하여 한 데이터셋에서
학습한 스키마가 다른 데이터셋에 재사용되지 않도록 합니다.

## 검증

- 기존 `th.check()` API와 `ValidationRunResult` 계약을 유지합니다.
- zero-configuration 검증의 자동 스키마 학습을 계속 지원합니다.
- 행을 materialize하지 않고 발견된 컬럼명과 데이터 타입으로 lazy 입력의 캐시
  identity를 생성합니다.
- 캐시 충돌만으로 발생하던 데이터셋 간 missing/extra-column 판정을 차단합니다.

## 호환성

이 변경은 하위 호환됩니다. DataFrame, mapping, 파일 기반 캐시 identity의 기존
동작은 유지됩니다. 하나의 런타임에서 서로 다른 여러 lazy schema를 검증하는
애플리케이션은 이 버전으로 업그레이드해야 합니다.
