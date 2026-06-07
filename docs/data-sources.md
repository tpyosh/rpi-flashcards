# Data Sources

## Current State

The repository currently ships a tiny manual seed dataset under
`data/raw/manual_seed/seed_dictionary.json`. It was created for the initial flashcard PoC and still
uses English definition-oriented fields.

The roadmap now targets an English/Japanese word-pair dictionary display. The next data work should
reshape the sample asset before importing or generating a larger dictionary.

## Target Sample Asset

Phase 1 and Phase 2 should use a small sample dictionary that is easy to inspect and commit.

Required fields:

- `entry_id`
- `word`
- `japanese`

Likely optional fields:

- `part_of_speech`
- `tags`
- `source`

Example:

```json
{
  "entry_id": "sample-001",
  "word": "careful",
  "japanese": "注意深い",
  "part_of_speech": "adjective",
  "tags": ["sample"],
  "source": "manual_sample"
}
```

## Planned Real Sources

The real dictionary can come from one or more offline-friendly sources, as long as the resulting
artifact is converted into the finalized English/Japanese word-pair format.

First candidate:

- EJDict-hand
  - URL: https://github.com/kujirahand/EJDict
  - expected fit: English word to Japanese meaning
  - expected format: tab-separated text-like dictionary rows
  - license stated by the project: Public Domain / CC0

Other candidates to reconsider only if EJDict-hand does not fit:

- JMdict or EDICT-derived data
  - strong dictionary quality, but primarily Japanese-to-English and likely heavier to invert
  - license and attribution requirements must be checked before use
- Wiktionary-derived dictionaries such as WikDict
  - broad coverage, but larger format and share-alike licensing may add project overhead
- Tatoeba
  - useful later for example sentences, but it is sentence-pair data rather than word-pair data

Phase 3 should not pick a final conversion strategy from documentation alone. Download the actual
source first, inspect representative raw rows, then decide parser and filtering rules from the
observed file shape.

ChatGPT-assisted work is appropriate for:

- comparing candidate sources
- summarizing license notes for human review
- inspecting raw samples
- proposing parser rules
- finding long translations, symbols, duplicate words, and unsuitable entries
- generating tests for the chosen conversion rules

Human review is still required for:

- accepting license terms
- deciding whether Japanese translations are good enough
- excluding words or meanings that are unsuitable for a passive display
- judging whether entries fit the small e-paper screen

The project should not require network access at runtime.

## Phase 3 Download-and-Inspect Spike

The first real-dictionary task should produce evidence, not a polished importer.

Expected steps:

1. download EJDict-hand into `data/raw/` or a documented local-only raw path
2. record the download URL, date, version or commit, and license note
3. inspect file names, size, line count, encoding, delimiter, and 50-100 representative rows
4. classify source patterns:
   - normal one-word rows
   - rows with multiple English spellings
   - rows with multiple Japanese meanings
   - rows with part-of-speech markers
   - rows with usage labels, slang, rare words, or sensitive labels
   - rows too long for terminal or e-paper display
5. propose a minimal conversion rule for `entry_id`, `word`, and `japanese`
6. generate a small curated subset for UI testing before importing the whole dictionary
7. update parser tests based on real examples from the source

## Transformation Stages

1. `data/raw/`
   source-shaped files, untouched except for storage
2. `data/normalized/`
   validated English/Japanese word-pair records
3. generated runtime dictionary asset
   compact snapshot used by terminal and e-paper display modes
4. `state/`
   reserved for later display history or learning state; not required for Phase 1

## Rebuild Flow

The existing commands are placeholders from the initial PoC:

```bash
make normalize-data
make build-deck
```

They should be adjusted during Phase 2 so rebuilding produces the finalized dictionary-display
asset rather than a quiz or review deck.

## Assumptions

- early development should prefer a small deterministic sample dictionary
- runtime display should be fully offline
- dictionary format work should happen before importing or generating a larger dictionary
- quiz and review metadata should not be required for the first e-paper display
