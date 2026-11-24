# SMART IDUKA — Phase II Normalization (UNF → 3NF)

## 1. Source and scope

This design uses the UCI Online Retail transaction-line dataset as a real retail dataset for demonstrating relational normalization. It is historical UK online-retail data, not actual SMART IDUKA customer/business data. It contains invoice lines, products, customers and countries. The source has no supplier, purchase-cost, expense, payment-method or stock-on-hand fields; those must not be fabricated into this Phase II schema.

A raw record represents one product line on an invoice. The original source fields are:

`InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country`

The dataset card records source provenance, licence and preliminary quality counts. The raw source archive must be downloaded into `data/raw/` and preserved unchanged before final submission.

## 2. UNF — Unnormalized form

At the conceptual UNF level, one invoice header contains a repeating collection of invoice items:

| InvoiceNo | InvoiceDate | CustomerID | Country | Items (repeating group) |
|---|---|---|---|---|
| 574021 | 2011-11-02 12:18:00 | 14434 | United Kingdom | (23301, GARDENERS KNEELING PAD KEEP CALM, 48, 1.45); (23355, HOT WATER BOTTLE KEEP CALM, 24, 4.15); (23284, DOORMAT KEEP CALM AND COME IN, 20, 7.08) |

**Problem:** `Items` is a repeating group containing multiple product facts in one invoice record. It is not atomic and cannot be reliably queried or constrained as a relational row.

## 3. 1NF — First Normal Form

Remove the repeating group so that each row contains exactly one invoice line and each field contains one atomic value.

The following three real invoice-line examples are reproduced in a published teaching extract of the UCI dataset. All three belong to invoice `574021`, dated `2011-11-02 12:18:00`, customer `14434`, country `United Kingdom`.

| InvoiceNo | StockCode | Description | Quantity | InvoiceDate | UnitPrice | CustomerID | Country |
|---|---|---|---:|---|---:|---:|---|
| 574021 | 23301 | GARDENERS KNEELING PAD KEEP CALM | 48 | 2011-11-02 12:18:00 | 1.45 | 14434 | United Kingdom |
| 574021 | 23355 | HOT WATER BOTTLE KEEP CALM | 24 | 2011-11-02 12:18:00 | 4.15 | 14434 | United Kingdom |
| 574021 | 23284 | DOORMAT KEEP CALM AND COME IN | 20 | 2011-11-02 12:18:00 | 7.08 | 14434 | United Kingdom |

**Dependency removed:** the repeating `Items` group is removed by storing one product line per row, making each attribute atomic.

**Key caution:** `(InvoiceNo, StockCode)` is often suggested as a line key, but the raw dataset reports exact duplicate rows. Do not assume that this pair is unique. The target design therefore introduces a generated `INVOICE_LINE_ID` surrogate primary key and preserves every source row during staging.

## 4. 2NF — Second Normal Form

For the 1NF staging relation, consider the natural composite business identifier `(InvoiceNo, StockCode)` as a provisional key only (subject to uniqueness validation). The functional dependencies visible in the business meaning are:

- `InvoiceNo → InvoiceDate, CustomerID, Country`
- `StockCode → Description`
- `(InvoiceNo, StockCode) → Quantity, UnitPrice` (provisional; duplicate invoice/product lines require a surrogate line identifier in the final implementation).

Move invoice-header facts into `INVOICE`, and product-master facts into `PRODUCT`. Keep the transaction-specific quantity and unit price in `INVOICE_LINE`.

### 2NF decomposition using the same three records

**INVOICE**

| InvoiceNo | InvoiceDate | CustomerID | Country |
|---|---|---|---|
| 574021 | 2011-11-02 12:18:00 | 14434 | United Kingdom |

**PRODUCT**

| StockCode | Description |
|---|---|
| 23301 | GARDENERS KNEELING PAD KEEP CALM |
| 23355 | HOT WATER BOTTLE KEEP CALM |
| 23284 | DOORMAT KEEP CALM AND COME IN |

**INVOICE_LINE (illustrative rows)**

| InvoiceNo | StockCode | Quantity | UnitPrice |
|---|---|---:|---:|
| 574021 | 23301 | 48 | 1.45 |
| 574021 | 23355 | 24 | 4.15 |
| 574021 | 23284 | 20 | 7.08 |

**Dependency removed:** invoice date/customer/country depend on `InvoiceNo` alone, and product description depends on `StockCode` alone, so those partial dependencies are moved out of the line relation into their respective parent relations.

## 5. 3NF — Third Normal Form

The invoice header still contains a country description. Country is a repeated reference value and should be represented once in a country lookup relation. Store `COUNTRY_ID` in `INVOICE` and the country name in `COUNTRY`.

The customer identifier is separated into `CUSTOMER`; the invoice references a customer where the source identifier is present. The source country is retained on `INVOICE` rather than assumed to be a permanent customer attribute, because customer-country consistency has not yet been measured.

### Final 3NF relations

1. **COUNTRY** (`COUNTRY_ID` PK, `COUNTRY_NAME` UQ)
2. **CUSTOMER** (`CUSTOMER_ID` PK)
3. **PRODUCT** (`PRODUCT_CODE` PK, `DESCRIPTION`)
4. **INVOICE** (`INVOICE_NO` PK, `INVOICE_DATETIME`, `CUSTOMER_ID` FK nullable, `COUNTRY_ID` FK)
5. **INVOICE_LINE** (`INVOICE_LINE_ID` PK, `INVOICE_NO` FK, `PRODUCT_CODE` FK, `QUANTITY`, `UNIT_PRICE`)

**Dependency removed:** `COUNTRY_NAME` is stored once in `COUNTRY` and referenced by `COUNTRY_ID`, removing the repeated country-description dependency from invoice records.

### Final functional dependencies

- `COUNTRY_ID → COUNTRY_NAME`
- `CUSTOMER_ID → (no additional customer attributes exist in this source)`
- `PRODUCT_CODE → DESCRIPTION`
- `INVOICE_NO → INVOICE_DATETIME, CUSTOMER_ID, COUNTRY_ID`
- `INVOICE_LINE_ID → INVOICE_NO, PRODUCT_CODE, QUANTITY, UNIT_PRICE`

Each non-key attribute in each final relation depends on the key, the whole key, and nothing but the key.

## 6. Raw-field-to-target mapping

| Raw field | Target table.column | Required transformation / handling |
|---|---|---|
| `InvoiceNo` | `INVOICE.INVOICE_NO`; `INVOICE_LINE.INVOICE_NO` | Preserve as text; retain leading `C` cancellation prefix; trim only in Phase IV after documenting raw value. |
| `StockCode` | `PRODUCT.PRODUCT_CODE`; `INVOICE_LINE.PRODUCT_CODE` | Preserve as text; do not cast to a number because codes are identifiers and may contain letters/leading zeroes. |
| `Description` | `PRODUCT.DESCRIPTION` | Text; source has missing descriptions. Keep nullable until Phase IV policy is approved; do not invent product names. |
| `Quantity` | `INVOICE_LINE.QUANTITY` | Convert to integer/number; retain negative quantities as source facts for returns/corrections. |
| `InvoiceDate` | `INVOICE.INVOICE_DATETIME` | Parse source date/time to a date-time value; record invalid/missing counts during Phase IV. |
| `UnitPrice` | `INVOICE_LINE.UNIT_PRICE` | Convert to exact decimal; source currency is GBP. Do not use binary floating-point for monetary calculations. |
| `CustomerID` | `CUSTOMER.CUSTOMER_ID`; `INVOICE.CUSTOMER_ID` | Preserve as text identifier; source is missing for many rows, so invoice FK is nullable. Do not create fake customer identities. |
| `Country` | `COUNTRY.COUNTRY_NAME`; `INVOICE.COUNTRY_ID` | Standardize and map distinct raw labels to country keys in Phase IV; retain original raw values for audit. |

No raw field is dropped. The `INVOICE_LINE_ID` is a generated surrogate key, not a source field.

## 7. Quality checks still required against the downloaded raw file

Do not clean the source in Phase II. Before finalizing, run and record:
- Missing counts for every source column, especially `InvoiceDate`, `CustomerID`, `Description`.
- Exact duplicate-row count.
- Duplicate `(InvoiceNo, StockCode)` count and maximum repeated occurrences.
- Distinct country labels and possible spelling/case/whitespace variants.
- Distinct descriptions per `StockCode` and distinct countries per `CustomerID`.
- Data-type anomalies in exported CSVs, invalid dates, non-numeric quantity/price values.
- Counts of negative/zero quantities and negative/zero prices.
- Cancellation invoice count (`InvoiceNo` begins with `C`).

The published preliminary counts are listed in `data/dataset_card.md`; they must be verified locally.

## 8. Design assumptions and limitations

- `INVOICE_NO` is treated as the source invoice identifier. Confirm it is unique at invoice-header level after raw profiling.
- Every source row is retained as a separate invoice line using a generated surrogate key. This protects duplicate source lines from being collapsed.
- `CUSTOMER_ID` is nullable because source rows can lack a customer identifier.
- `COUNTRY` is associated with the invoice/source row, not permanently assigned to a customer, until customer-country consistency is validated.
- This dataset does not contain supplier, purchase, inventory balance, expenses, payment, tax or cost-of-goods-sold data. Those are SMART IDUKA domain requirements and should be designed as additional entities when suitable source data or explicit business requirements are supplied.
- The 3NF design is a logical blueprint. Oracle data types, lengths, constraints, indexes and physical implementation are Phase IV work.

## References

- Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33
- UCI dataset page: https://archive.ics.uci.edu/dataset/352/online+retail
- Published teaching extract containing the three invoice-line examples: https://dbdmg.polito.it/dbdmg_web/wp-content/uploads/2025/11/DS_MLL_Lab_07__Frequent_Pattern_Mining_.pdf
- Independent published quality audit (preliminary counts; re-verify): https://github.com/Ozas007/online-retail-data-cleaning
