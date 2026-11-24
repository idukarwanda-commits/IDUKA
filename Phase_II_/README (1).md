# IDUKA — Phase II: Data Sourcing, Normalization and Logical Design

## Deliverable status

This package contains the Phase II logical-design documents and a reproducible raw-data downloader.

**Important status:** The untouched UCI source archive is not bundled because the download could not be completed in the file-generation environment. `data/raw/` is intentionally empty. Run the downloader below and verify the resulting file before claiming Task 1 is complete.

## Dataset selected

UCI Machine Learning Repository — **Online Retail** (Dataset 352), a real retail transaction dataset with 541,909 reported invoice-line records and eight source fields. It is licensed under CC BY 4.0.

Official source: https://archive.ics.uci.edu/dataset/352/online+retail  
DOI: https://doi.org/10.24432/C5BW33

This is a historical UK retailer dataset used as a retail normalization case study. It is not data from an actual SMART IDUKA shop.

## Folder structure

```text
IDUKA/
├── README.md
├── data/
│   ├── raw/                         # Place untouched source archive here
│   └── dataset_card.md
├── docs/
│   └── design/
│       ├── normalization.md
│       ├── erd.png
│       └── data_dictionary.md
└── scripts/
    └── download_raw_dataset.py
```

## Download and preserve the raw source

From this project root, run:

```bash
python scripts/download_raw_dataset.py
```

It downloads the UCI archive to `data/raw/uci_online_retail_original.zip`, does not modify it, and prints a SHA-256 checksum. Keep the archive untouched. Extract a separate working copy only when performing the Phase II checks.

If your network blocks the script, download the archive from the official UCI dataset page and save it under `data/raw/`. Do not use a cleaned or transformed copy as the raw file.

## Phase II deliverables

| Requirement | File |
|---|---|
| Dataset source, licence, format and description | `data/dataset_card.md` |
| Quality-check profile and counts | `data/dataset_card.md` |
| UNF → 1NF → 2NF → 3NF explanation with example records | `docs/design/normalization.md` |
| Logical ERD, crow's-foot relationships | `docs/design/erd.png` |
| Keys, column meanings, required/unique status | `docs/design/data_dictionary.md` |
| Raw source downloader | `scripts/download_raw_dataset.py` |

## Important academic integrity notes

- The quality counts in the dataset card are preliminary figures reported by a published independent audit. Re-run the checks on your downloaded raw source and confirm them before final submission.
- The three normalization example rows are real example records reproduced in a published teaching extract of the UCI dataset.
- Do not claim missing-date counts, country spelling variants, or other unmeasured statistics. Compute them from the downloaded file.
- Do not clean the raw source in Phase II. Cleaning and type conversion belong to Phase IV.
- The selected source does not contain suppliers, purchases, payments, expenses or stock-on-hand. Those SMART IDUKA entities require another suitable dataset or clearly documented business requirements.

## Suggested 5-minute class demonstration

1. Open the untouched source workbook and show one invoice with multiple item rows.
2. Explain that the repeated item group becomes one row per item in 1NF.
3. Show the invoice header, product master and invoice line decomposition in 2NF.
4. Show how country values are moved to COUNTRY in 3NF.
5. Open `erd.png` and trace `INVOICE` to `INVOICE_LINE`, `PRODUCT`, `CUSTOMER` and `COUNTRY`.
6. Pick one raw record and map each of its eight source fields using the mapping table in `normalization.md`.

## Attribution

Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33. Licensed under CC BY 4.0.
