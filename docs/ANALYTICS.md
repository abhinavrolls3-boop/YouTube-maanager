# Offline YouTube analytics

This tool reads a CSV export that you download yourself from YouTube Studio. It does not log in to YouTube, scrape private data, or upload the CSV anywhere.

## Use

1. In YouTube Studio, open Analytics and export a CSV report.
2. Put the CSV in the repository runtime (for local use) or include it in a manually dispatched workflow only if you understand that workflow artifacts may be visible to repository collaborators.
3. Run: `PYTHONPATH=src python -m factverse_manager.cli analytics path/to/report.csv`
4. Review totals, averages, top videos, and notes in `output/analytics.json`.

CSV headers differ between report types. Unsupported columns are skipped. CTR is summarized exactly as exported; confirm its units before comparing reports. A small export is descriptive, not proof of causation. Do not put personal information or private audience data in a public repository.
