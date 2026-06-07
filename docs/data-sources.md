# Data Sources

## Current State

The repository currently ships a tiny manual seed dataset under `data/raw/manual_seed/seed_dictionary.json`. It exists to validate:

- schema design
- normalization
- deck generation filters
- terminal UX

This keeps bootstrap small and fully offline.

## Planned Free Sources

Primary target:

- Open English WordNet or another redistributable English lexical source

Supplementary metadata:

- word frequency data from an open source such as `wordfreq`

## Target Normalized Fields

- `entry_id`
- `lemma`
- `part_of_speech`
- `definition`
- `example` (optional)
- `difficulty`
- `frequency_per_million`
- `tags`
- `source`

## Transformation Stages

1. `data/raw/`
   source-shaped files, untouched except for storage
2. `data/normalized/`
   cleaned JSONL entries with stable field names
3. `data/decks/`
   generated deck snapshots from machine-readable deck configs
4. `state/`
   user progress and review events

## Rebuild Flow

```bash
make normalize-data
make build-deck
```

Changing deck size, difficulty buckets, or part-of-speech filters only requires editing `configs/decks/*.toml` and rebuilding.

## Assumptions

- early development should prefer a small deterministic subset
- runtime should not require network access
- later larger sources should fit the same normalized schema

