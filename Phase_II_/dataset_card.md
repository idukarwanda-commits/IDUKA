# Dataset Card — UCI Online Retail

## Dataset identity
- **Dataset name:** Online Retail
- **Publisher:** UCI Machine Learning Repository
- **Creator:** Daqing Chen
- **Dataset ID:** 352
- **DOI:** https://doi.org/10.24432/C5BW33
- **Official source page:** https://archive.ics.uci.edu/dataset/352/online+retail
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Original published format:** Excel workbook (`Online Retail.xlsx`); UCI distributes it in a ZIP archive.
- **Expected source size:** approximately 22.6 MB for the workbook (UCI catalogue listing).
- **Reported records:** 541,909 transaction-line records.
- **Collection period represented:** 1 December 2010 to 9 December 2011.
- **Date collected for this project:** 24 November 2026 (project preparation date; download must be run locally to record the actual retrieval timestamp and SHA-256).

## What one record represents
One record represents **one product line on an invoice**: an invoice identifier, product code and description, quantity, invoice timestamp, unit price, customer identifier (when available), and customer country.

## Privacy and anonymisation
The published dataset contains customer identifiers, not customer names, phone numbers or government ID numbers. `CustomerID` is a pseudonymous numeric identifier in the source. This project does not attempt to re-identify customers. Treat customer identifiers as pseudonymous personal data and restrict unnecessary disclosure. No names, phone numbers or national ID numbers are present in the documented source fields.

## Raw-data preservation
The untouched source archive belongs in `data/raw/uci_online_retail_original.zip`. Run:

```bash
python scripts/download_raw_dataset.py
```

The script saves the downloaded archive without transforming its contents and prints its SHA-256 checksum. Extract a separate working copy for inspection; **never clean, rename columns, remove duplicates, fill nulls or otherwise modify the file in `data/raw/`**.

> **Delivery note:** The source archive could not be transferred into this generated package in this session. The `data/raw/` folder is therefore intentionally empty until the downloader is run. Do not claim the raw-file requirement is complete until the archive is present and its checksum is recorded.

## Preliminary data-quality profile
The following counts are reported by an independent published audit of the UCI source file. They are provided as preliminary reference figures, **not as a fresh local execution of the quality checks**. Re-run the checks against the downloaded raw file and update this card if the counts differ.

| Check | Reported count | Interpretation |
|---|---:|---|
| Total records | 541,909 | Source transaction-line rows |
| Missing `CustomerID` | 135,080 | Customer cannot be linked for these rows |
| Missing `Description` | 1,454 | Product description absent |
| Exact duplicate rows | 5,268 | Duplicate full source records |
| Negative `Quantity` | 10,624 | Includes returns/corrections; investigate, do not delete in Phase II |
| `UnitPrice` less than or equal to zero | 2,517 | Includes zero/negative price records |
| Invoice numbers beginning with `C` | 9,288 | Cancellation/credit-note indicator |

**Unmeasured in this preliminary report:** number of missing dates, country spelling variants, invalid date strings, non-numeric price strings in an exported CSV, customer-to-country conflicts, and duplicate invoice/product combinations. These must be computed from the downloaded source; no counts are invented here.

## Known source-field profile
- `InvoiceNo`: invoice identifier; a leading `C` indicates cancellation.
- `StockCode`: product identifier; preserve as text so formatting is not lost.
- `Description`: product description.
- `Quantity`: line quantity; negative values can occur.
- `InvoiceDate`: invoice date and time.
- `UnitPrice`: unit price in pounds sterling (GBP).
- `CustomerID`: customer identifier; missing for some rows.
- `Country`: country associated with the customer.

## Attribution
Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33. Licensed under CC BY 4.0.

Independent audit reference for preliminary quality counts: https://github.com/Ozas007/online-retail-data-cleaning (counts must be independently rechecked against the raw download).
