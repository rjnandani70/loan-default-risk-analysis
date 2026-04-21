# Power BI DAX Quick Reference
## Loan Default Risk Analysis Dashboard

---

## Quick Copy-Paste DAX Formulas

### Top KPIs (Copy to Measure grid)

```dax
Portfolio KPIs =
VAR TotalLoans = COUNTROWS(loan_features)
VAR TotalDefaults = SUM(loan_features[default_flag])
VAR DefaultRate = DIVIDE(TotalDefaults, TotalLoans, 0)
VAR TotalExposure = SUM(loan_features[loan_amount])
RETURN
IF(
    SELECTEDVALUE(KPI_Selection[Measure]) = "Total Loans", TotalLoans,
    IF(SELECTEDVALUE(KPI_Selection[Measure]) = "Defaults", TotalDefaults,
    IF(SELECTEDVALUE(KPI_Selection[Measure]) = "Default Rate", DefaultRate,
    IF(SELECTEDVALUE(KPI_Selection[Measure]) = "Total Exposure", TotalExposure,
    BLANK()))))
```

### Count Measures

```dax
Total Loans = COUNTROWS(loan_features)

Total Defaults = SUM(loan_features[default_flag])

Performing Loans = [Total Loans] - [Total Defaults]

High Risk Loans = CALCULATE(COUNTROWS(risk_scored_loans), risk_scored_loans[risk_band]="High")

Medium Risk Loans = CALCULATE(COUNTROWS(risk_scored_loans), risk_scored_loans[risk_band]="Medium")

Low Risk Loans = CALCULATE(COUNTROWS(risk_scored_loans), risk_scored_loans[risk_band]="Low")
```

### Percentage Measures

```dax
Default Rate % = DIVIDE([Total Defaults], [Total Loans], 0) * 100

High Risk % = DIVIDE([High Risk Loans], [Total Loans], 0) * 100

Medium Risk % = DIVIDE([Medium Risk Loans], [Total Loans], 0) * 100

Low Risk % = DIVIDE([Low Risk Loans], [Total Loans], 0) * 100

Loss Rate % = DIVIDE([Potential Loss], [Total Exposure], 0) * 100
```

### Average Measures

```dax
Avg Loan Amount = AVERAGE(loan_features[loan_amount])

Avg Interest Rate % = AVERAGE(loan_features[interest_rate])

Avg Predicted PD = AVERAGE(risk_scored_loans[pred_default_probability])

Median Loan Amount = MEDIAN(loan_features[loan_amount])
```

### Sum Measures

```dax
Total Exposure = SUM(loan_features[loan_amount])

Potential Loss = CALCULATE(SUM(loan_features[loan_amount]), loan_features[default_flag]=1)

Total Interest Income = SUM(loan_features[interest_income])
```

### Calculated Columns (Add to loan_features table)

```dax
Risk Score Decile = 
    IF(
        risk_scored_loans[pred_default_probability] >= 0.9, "Top 10% Risk",
        IF(risk_scored_loans[pred_default_probability] >= 0.8, "80-90%",
        IF(risk_scored_loans[pred_default_probability] >= 0.7, "70-80%",
        IF(risk_scored_loans[pred_default_probability] >= 0.6, "60-70%",
        IF(risk_scored_loans[pred_default_probability] >= 0.5, "50-60%",
        IF(risk_scored_loans[pred_default_probability] >= 0.4, "40-50%",
        IF(risk_scored_loans[pred_default_probability] >= 0.3, "30-40%",
        IF(risk_scored_loans[pred_default_probability] >= 0.2, "20-30%",
        IF(risk_scored_loans[pred_default_probability] >= 0.1, "10-20%",
        "Bottom 10%")))))))))

Risk Exposure Bucket =
    IF(loan_features[loan_amount] >= 25000, "Large (≥$25K)",
    IF(loan_features[loan_amount] >= 15000, "Medium ($15K-$25K)",
    "Small (<$15K)"))

Experience Level =
    IF(loan_features[employment_length] >= 10, "10+ Years",
    IF(loan_features[employment_length] >= 5, "5-10 Years",
    IF(loan_features[employment_length] >= 2, "2-5 Years",
    IF(loan_features[employment_length] >= 1, "1-2 Years",
    "<1 Year"))))
```

### Advanced Measures (Optional)

```dax
// Running Total of Defaults by Issue Month
Running Default Total = 
    CALCULATE(
        SUM(loan_features[default_flag]),
        FILTER(
            ALL(loan_features[issue_month]),
            loan_features[issue_month] <= MAX(loan_features[issue_month])
        )
    )

// Year-over-Year Default Rate (if date hierarchy exists)
YoY Default Rate = 
    VAR CurrentYear = [Default Rate %]
    VAR PriorYear = CALCULATE([Default Rate %], DATEADD(loan_features[issue_month], -1, YEAR))
    RETURN
    IFERROR(DIVIDE(CurrentYear - PriorYear, PriorYear, 0), 0)

// Loan Amount Percentile Rank
Loan Amount Percentile = 
    PERCENTILE.INC(
        VALUES(loan_features[loan_amount]),
        0.75
    )

// Risk Concentration Index (Herfindahl)
Concentration Index =
    SUMPRODUCT(
        DIVIDE([Total Exposure by Purpose], [Total Exposure], 0) ^ 2
    )
```

---

## Common Visual Configurations

### Slicer Settings
```
Display Options:
- List or Buttons (prefer Buttons for ≤5 items)
- Single Select or Multi-Select (recommend Multi)
- Show "All" option: Yes
- Formatting: Font Size 11, Color #0078D4

Sync Slicers across pages: Yes (Slicers pane → Sync)
```

### Conditional Formatting (Colors)

```
Data Bars:
- Green (#107C10) for good (Low Risk, ↑ performance)
- Red (#E81123) for bad (High Risk, ↓ performance)
- Orange (#FFB900) for warning (Medium Risk, ⚠)

Background Colors:
Minimum: Green, Middle: Yellow, Maximum: Red
Field: [Default Rate %] or [Risk Band]
```

### Number Formatting

```
Loan Amount: $#,##0 (Currency, 0 decimals)
Default Rate: 0.00% (Percentage, 2 decimals)
Count: #,##0 (Whole numbers, thousands separator)
Probability: 0.00% (Percentage, 2 decimals)
Interest Rate: 0.00% (Percentage, 2 decimals)
```

---

## Filter Context Examples

### Bookmark Filters

**"High Risk Dashboard"**
```
Filter: risk_scored_loans[risk_band] = "High"
Hide: Tabs for "Segment Risk" and "Trend Analysis" (less relevant)
Highlight: Loans with PD > 0.7
```

**"State Deep Dive"**
```
Filter: loan_features[state] = Selected State
Drill-Down: County / City (if available)
Show: Comparative metrics vs. national average
```

**"YTD Performance"**
```
Filter: loan_features[issue_month] >= TODAY()-365
Show: Default trend sparkline
Show: YoY comparison
```

---

## Slicer Configuration Checklist

- [ ] **Grade Slicer:** Buttons, Multi-select
- [ ] **Purpose Slicer:** Dropdown, Multi-select
- [ ] **State Slicer:** Dropdown, Multi-select, Searchable
- [ ] **Income Band Slicer:** Buttons or Dropdown
- [ ] **Risk Band Slicer:** Buttons (Low, Medium, High)
- [ ] **Issue Month Slicer:** Range slider, format as "MMM YYYY"
- [ ] **Home Ownership Slicer:** Buttons
- [ ] **Loan Term Slicer:** Buttons (24/36/60)

All slicers should be **synced** across related pages (Portfolio, Segment, Trends)

---

## Performance Tuning Tips

1. **Reduce cardinality:**
   - Bin continuous variables (loan_amount → buckets)
   - Use lookup tables for repeated dimensions

2. **Optimize DAX:**
   - Avoid nested IFs → Use SWITCH()
   - Cache with variables (VAR)
   - Pre-calculate aggregations

3. **Visual optimization:**
   - Limit visuals to Top 10-15 items
   - Use aggregated tables for summaries
   - Disable visual interactions if not needed

4. **Example Optimized Measure:**
   ```dax
   Default Rate Optimized = 
       VAR Cache = VALUES(loan_features[grade])
       RETURN
       CALCULATE(
           DIVIDE(SUM(loan_features[default_flag]), COUNTROWS(loan_features), 0),
           Cache
       )
   ```

---

## Testing Checklist

- [ ] All measures display correct values
- [ ] Filters work across all pages
- [ ] Drill-throughs navigate correctly
- [ ] Bookmarks load expected states
- [ ] Performance acceptable (<2sec refresh)
- [ ] Mobile layout readable (if applicable)
- [ ] Print layout has proper spacing
- [ ] Data refresh completes successfully

---