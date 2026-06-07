# Roadmap

The project goal is a Raspberry Pi dictionary display that periodically shows an English word
and its Japanese translation on an e-paper panel. Early phases stay terminal-first so the data
format and viewing experience can be checked before hardware work starts.

Quiz, rating, reveal, and spaced-review behavior are not part of the current roadmap. They can
be reconsidered after the dictionary display works on e-paper.

## Phase 1: Sample Dictionary UI Check

Done condition:

- `make run-demo` runs a terminal display on macOS
- the UI shows one English word and one Japanese translation at a time
- development mode advances automatically every 5 seconds
- displayed entries are selected randomly from the sample dictionary
- the terminal app can be stopped with a simple quit path such as `q` or Ctrl-C
- no quiz input, rating, reveal step, progress state, GPIO, or e-paper dependency is required

## Phase 2: Sample Dictionary Format Finalization

Done condition:

- the sample dictionary has a stable machine-readable format
- required fields for the first display use case are fixed
- the format clearly represents an English word and its Japanese translation
- optional metadata fields are documented without making the first UI harder to run
- tests cover loading, validation, and deterministic sample behavior

Likely first fields:

- `entry_id`
- `word`
- `japanese`
- `part_of_speech` optional
- `tags` optional
- `source` optional

## Phase 3: Real Dictionary Formation

Approach:

- use a freely downloadable English/Japanese dictionary as the primary source
- start with EJDict-hand as the first candidate because it is English-to-Japanese, simple to parse,
  and published as Public Domain / CC0
- download the real source and inspect the actual raw files before finalizing conversion rules
- use ChatGPT-assisted analysis for source comparison, raw-data inspection, parser planning, and
  outlier detection
- keep human review for license acceptance, Japanese quality, and display suitability

Done condition:

- a source download URL, license, and local raw-data path are documented
- raw source samples are inspected before parser rules are finalized
- a larger real dictionary can be generated or imported into the finalized format
- the source, license notes, filtering rules, and generation process are documented
- generated dictionary artifacts are reproducible enough for local development
- runtime display still works offline from committed or locally generated assets
- sample data remains available for small, fast UI checks

## Phase 4: Raspberry Pi Port and SSH Check

Done condition:

- the terminal display runs on Raspberry Pi without e-paper-specific code
- setup steps are documented for Raspberry Pi OS
- the app can be launched over SSH from a Mac
- dictionary asset paths and Python environment setup work on-device
- the same terminal behavior can be compared between macOS and Raspberry Pi

## Phase 5: E-paper Operation Test

Done condition:

- the exact e-paper panel and driver path are confirmed
- a minimal hardware test can clear the panel and draw known text or an image
- SPI/GPIO setup is documented separately from app logic
- display refresh constraints are observed before wiring the dictionary UI
- terminal mode remains available while hardware is being tested

## Phase 6: Dictionary Display on E-paper

Done condition:

- English word and Japanese translation pairs are rendered on the e-paper panel
- display updates follow the configured timer interval
- random selection uses the same dictionary assets validated in earlier phases
- the display layer handles panel-specific rendering without changing dictionary data logic
- the app can run as a practical Raspberry Pi dictionary display

## Later Candidates

- physical buttons for pause, next, or shutdown
- boot-to-app startup flow
- display history or duplicate avoidance
- quiz mode
- lightweight learning or review state
