# SMART IDUKA — Business Process Model (BPMN 2.0)

**Project:** SMART IDUKA  
**Document:** Business Process Diagram README  
**Diagram file:** `SMART_IDUKA_Business_Process.bpmn`  
**Modeling standard:** BPMN 2.0  
**Process style:** Owner-centric shop management workflow

## 1. Project overview

SMART IDUKA is a shop management and automated accounting system designed to help a shop owner manage day-to-day business operations from one platform.

The owner enters business information—such as products, purchases, sales, payments and expenses—while the system organizes the records, updates stock and balances, performs accounting calculations, and produces reports.

The process is designed around one primary business user: **the shop owner**. It does not require separate actors such as an accountant, cashier or inventory manager for the core workflow.

**Tagline:** *Your Business. Your Numbers. Your Control.*

## 2. Purpose of the BPMN diagram

The BPMN 2.0 diagram describes the main business process and shows:
- Where the shop-management process starts and ends.
- The activities the owner performs.
- The decisions that affect the next process step.
- The automated operations performed by SMART IDUKA.
- How purchasing, inventory, sales, payments, expenses and reporting connect.

This is a business-process model for explaining the intended workflow. It is **not** an executable application or a deployment-ready process-engine definition.

## 3. Main process workflow

1. **Start the process** — the owner opens SMART IDUKA.
2. **Set up the shop** — enter the shop profile and business settings.
3. **Register the catalog** — add products, categories and suppliers.
4. **Choose an operation** — the owner selects the business activity to perform.

The workflow then follows the relevant path:

### A. Purchasing and restocking

1. Record the supplier purchase and invoice.
2. Calculate acquisition cost, including applicable landed costs.
3. Update inventory and retain stock-movement history.
4. Calculate or recommend selling prices.
5. Return to the shop operations selection.

### B. Sales

1. Record the sale and its items.
2. Check whether sufficient stock is available.
3. If stock is insufficient, show a low-stock alert and recommend replenishment.
4. If stock is available, determine whether payment was received in full.
5. Record the payment, or register the unpaid amount as customer credit/receivable.
6. Update inventory, balances and accounting records.
7. Return to the shop operations selection.

### C. Expenses

1. Record the business expense.
2. Post the expense to the accounting records.
3. Return to the shop operations selection.

### D. Reports and business review

1. Generate the dashboard and financial reports.
2. Review profit, cash, debts and stock performance.
3. Decide whether to continue managing the shop.
4. If yes, return to the operations selection. If no, end the session.

## . SMART IDUKA automated capabilities

| Capability | What SMART IDUKA is intended to do |
|---|---|
| Inventory management | Update stock and maintain stock movement history. |
| Acquisition costing | Calculate product acquisition cost and applicable landed costs. |
| Smart pricing | Recommend selling prices using configured pricing rules. |
| Sales management | Record sales and check stock availability. |
| Payment and credit tracking | Record payments and track unpaid customer balances. |
| Automated accounting | Update relevant accounting records from business transactions. |
| Expense management | Record expenses and reflect them in accounting records. |
| Reporting and analytics | Present business performance and financial reports. |
| Alerts | Notify the owner about low stock and relevant business conditions. |

## . Important business and accounting rules

- Use decimal-safe monetary calculations (for example, Java `BigDecimal`).
- Keep purchase costs and stock-movement history; do not overwrite historical transaction costs when a product's current cost changes.
- Define and consistently apply an inventory costing method, such as FIFO or weighted average.
- Record every stock increase or decrease with a traceable stock movement.
- Distinguish sales revenue, cash received, customer receivables, expenses, gross profit and net profit.
- Ensure every posted double-entry journal entry balances: total debits must equal total credits.
- Preserve posted financial history. Correct posted transactions using controlled reversals or adjustment entries rather than silently deleting them.

The BPMN diagram describes the business flow; detailed accounting rules must also be enforced in the application and database.


## . How to open and edit the BPMN file

1. Install **Camunda Modeler** from its official download page: https://camunda.com/download/modeler/
2. Launch Camunda Modeler.
3. Choose **File → Open File**.
4. Select `SMART_IDUKA_Business_Process.bpmn`.
5. Review the diagram and adjust element positions or labels if required.
6. Save the file after making changes.

You can also open the file in another BPMN 2.0-compatible modeler.
## . Scope and limitations of this version
This model presents the main owner-centric business workflow. It is a high-level process model and does not yet detail every exception or sub-process, including:
- Supplier payment and supplier payable settlement.
- Purchase returns and customer sales returns.
- Partial payments and debt collection.
- Stock adjustments, damaged goods and stock counts.
- Expiry-date handling.
- Multi-branch transfers and employee permissions.
- Detailed journal-entry posting rules and period closing.

These can be added as separate BPMN sub-processes as the project requirements become more detailed.

## . Expected business value

SMART IDUKA is intended to reduce manual record-keeping, improve stock visibility, make customer debts easier to track, reduce calculation errors, organize financial records and help the owner make better-informed business decisions.

**Core principle:** The owner enters business information; SMART IDUKA organizes, calculates, tracks and reports it.
