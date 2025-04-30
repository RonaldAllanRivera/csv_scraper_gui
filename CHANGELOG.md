# Changelog

All notable changes to this project will be documented in this file.

## [1.4.0] - 2025-04-28

### Added

- `set_button_states()` now disables buttons dynamically to prevent user actions during scraping.
- Clear progress updates shown in the UI during scraping.
- Status label for "Saving file..." after scraping completes.

### Changed

- `human_think_time()` duration increased to 0.8–1.2s to mimic human behavior more effectively.
- `human_scroll_page()` and `human_move_mouse()` timings adjusted to reduce bot-like behavior.
- More consistent UI button logic (Import, Start, Pause, Continue, Stop) to avoid conflicting actions.
- Increased robustness when running long scraping tasks.

### Fixed

- Prevented multiple button actions during scraping state transitions.
- Resolved UI responsiveness lag during scraping.

## [1.3.0] - 2025-04-26

### Added

- Treeview row update while scraping (live UI sync).
- Pause and Resume functionality.
- Color-coded progress bar and row backgrounds (dark theme).

## [1.2.0] - 2025-04-25

### Added

- Progress percentage label.
- CSV output file generation with timestamp.
- User-Agent rotation from `user_agents.txt`.

## [1.0.0] - 2025-04-24

### Initial release

- GUI for importing CSVs and scraping AI tool listings from `theresanaiforthat.com`.
- Output saved to new CSV with Title, Content, and Category fields.
