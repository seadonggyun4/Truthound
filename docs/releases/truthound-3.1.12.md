# Truthound 3.1.12 Release Notes

## Highlights

Truthound 3.1.12 fixes automatic schema caching for lazy dataframe inputs.
Distinct lazy schemas now receive distinct cache identities, preventing a
schema learned for one dataset from being reused for another dataset.

## Validation

- Preserves the existing `th.check()` API and `ValidationRunResult` contract.
- Keeps automatic schema learning enabled for zero-configuration validation.
- Derives lazy-input cache identity from discovered column names and data
  types without materializing rows.
- Prevents cross-dataset missing/extra-column findings caused solely by cache
  collisions.

## Compatibility

The change is backward compatible. DataFrame, mapping, and file-backed cache
identities retain their existing behavior. Applications using lazy dataframe
inputs should upgrade when multiple schemas are validated in the same runtime.
