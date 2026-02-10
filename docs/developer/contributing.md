# Contributing

This page defines a pragmatic contribution workflow for ADAMACS code and docs.

## Branching

- create focused branches per topic
- keep ingest and analysis changes separated unless unavoidable

## Pull request scope

Good PR characteristics:
- one clear objective
- small, reviewable diff
- tests or validation evidence attached
- explicit migration/impact notes if behavior changes

## Minimum PR checklist

- [ ] code lints pass
- [ ] tests pass (or explain why not)
- [ ] docs updated for user-visible behavior changes
- [ ] no secrets/config credentials committed
- [ ] notebook outputs cleared or intentionally curated

## Review focus by repo

Ingest repo reviews should prioritize:
- operational safety
- backward compatibility for GUI/task staging
- worker interaction correctness
- permissions/ownership implications

Analysis repo reviews should prioritize:
- query correctness and key restrictions
- reproducibility metadata
- helper API clarity
- notebook maintainability

## Testing guidance

### Ingest-side

Validate on minimal session/scan key before broad rollout.
Confirm:
- metadata insert correctness
- task insertion correctness
- worker pickup behavior

### Analysis-side

Validate:
- keyset restrictions
- table joins and row counts
- expected output shapes and units

## Documentation expectation

Every operational change should include doc updates in this repository (or linked docs source).
At minimum, update one of:
- ingest workflow pages
- worker ownership page
- troubleshooting page

## Security expectations

Never commit:
- `dj_local_conf.json`
- API keys (RSpace, PyRAT, webhooks)
- private credentials in notebooks/scripts

