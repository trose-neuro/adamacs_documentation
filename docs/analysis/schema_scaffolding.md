# Schema Scaffolding for Missing Classes

`adamacs_analysis` includes a CLI to scaffold missing DataJoint classes.

This is useful when students need a clean starting point for project-specific computed/manual tables.

## CLI command

```bash
adamacs-analysis-generate \
  --schema-name adamacs_analysis \
  --output generated/my_analysis_schema.py \
  --class TrialLevelMetrics:Computed \
  --class SubjectSummary:Manual
```

## Overwrite existing output

```bash
adamacs-analysis-generate \
  --schema-name adamacs_analysis \
  --output generated/my_analysis_schema.py \
  --class TrialLevelMetrics:Computed \
  --overwrite
```

## Recommended usage pattern

1. Generate scaffolds into a `generated/` or `analysis_schema/` directory.
2. Rename classes to meaningful project names.
3. Add clear key dependencies and definitions.
4. Keep `make` methods small and testable.
5. Add unit tests or dry-run validation notebook.

## Design guidance

- prefer one class per biological/computational concept
- use stable primary keys that align with existing scan/session schema keys
- avoid embedding large blobs unless necessary
- keep intermediate outputs reproducible from upstream tables

## Example skeleton after generation

```python
@schema
class TrialLevelMetrics(dj.Computed):
    definition = """
    -> trial.Trial
    ---
    metric_value: float
    """

    def make(self, key):
        # query upstream
        # compute metric
        self.insert1({**key, 'metric_value': value})
```

## When to create new classes vs notebook-only analysis

Create new schema classes when:
- metric will be reused across projects
- computation is expensive and worth caching
- multiple notebooks depend on the same derived table

Stay notebook-only when:
- exploratory one-off analysis
- unstable metric definitions
- visualization-first iteration stage

