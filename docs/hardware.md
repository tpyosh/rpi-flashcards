# Hardware Strategy

## Target

- Raspberry Pi Zero 2 W
- 2.13-inch SPI e-paper module or HAT starter kit

## Uncertainty

Different starter kits may expose:

- different controller revisions
- different Waveshare-compatible Python modules
- slightly different initialization or refresh behavior

The repository therefore avoids binding application logic to a concrete driver name at this stage.

## Adapter Plan

1. keep frame preparation in `src/rpi_flashcards/display`
2. validate output on macOS by rendering PNG previews
3. add one Pi adapter inside `src/rpi_flashcards/display` or `src/rpi_flashcards/platform`
4. keep the adapter responsible for:
   - panel initialization
   - SPI/GPIO interaction
   - image buffer transfer
   - refresh policy

## Bring-up Order

1. run the terminal app on Raspberry Pi without display code
2. confirm packaged dictionary assets and timer behavior on-device
3. render PNG previews locally from the same dictionary data
4. wire one concrete e-paper driver after confirming panel identity
5. keep terminal fallback during hardware debugging

## Known Constraints

- e-paper refresh is slow, so updates should be explicit and infrequent
- full refresh is acceptable first; partial refresh optimization should wait
- ghosting behavior should be handled in the adapter, not in `core`
