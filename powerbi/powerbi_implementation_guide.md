# Power BI Dashboard Implementation Guide
## Loan Default Risk Analysis

---

## Part 1: Data Model Setup

### Step 1: Import Tables
Import the following tables from `data/processed/`:
1. **loan_features.csv** - Core loan attributes
2. **risk_scored_loans.csv** - Model predictions and risk bands
3. **kpi_summary.csv** - Portfolio-level KPIs
4. **segment_default_rates.csv** - Segment analysis

### Step 2: Create Relationships
1. Set relationship between:
   - `loan_features[loan_id]` → `risk_scored_loans[loan_id]` (1:1, active)
2. Both tables should auto-relate to `segment_default_rates` via `segment` or `grade` dimension

### Step 3: Data Type Configuration
- Dates: `issue_month` → Date format (M/D/YYYY)
- Currency: `loan_amount` → Currency format ($)
- Percentages: `default_rate`, `interest_rate` → Percentage (2 decimals)
- IDs: `loan_id` → Text
- Flags: `default_flag`, `employment_length` → Text

---

## Part 2: DAX Measures

### Portfolio Metrics
```dax
// Total Active Loans
Total Loans = COUNTROWS(loan_features)

// Total Number of Defaults
Total Defaults = SUM(loan_features[default_flag])

// Overall Default Rate (%)
Default Rate % = 
    DIVIDE(
        SUM(loan_features[default_flag]), 
        COUNTROWS(loan_features), 
        0
    ) * 100

// Average Loan Amount
Avg Loan Amount = AVERAGE(loan_features[loan_amount])

// Average Interest Rate
Avg Interest Rate = AVERAGE(loan_features[interest_rate])

// Median Loan Amount
Median Loan Amount = MEDIAN(loan_features[loan_amount])

// Total Loan Exposure
Total Exposure = SUM(loan_features[loan_amount])
```

### Risk & Model Metrics
```dax
// Average Predicted Default Probability
Avg Predicted PD = AVERAGE(risk_scored_loans[pred_default_probability])

// High Risk Loans (PD > 0.5)
High Risk Loans = 
    CALCULATE(
        COUNTROWS(risk_scored_loans),
        risk_scored_loans[risk_band] = "High"
    )

// Medium Risk Loans
Medium Risk Loans = 
    CALCULATE(
        COUNTROWS(risk_scored_loans),
        risk_scored_loans[risk_band] = "Medium"
    )

// Low Risk Loans
Low Risk Loans = 
    CALCULATE(
        COUNTROWS(risk_scored_loans),
        risk_scored_loans[risk_band] = "Low"
    )

// Risk Distribution %
High Risk % = DIVIDE([High Risk Loans], [Total Loans], 0) * 100
Medium Risk % = DIVIDE([Medium Risk Loans], [Total Loans], 0) * 100
Low Risk % = DIVIDE([Low Risk Loans], [Total Loans], 0) * 100
```

### Business KPIs
```dax
// Non-Defaulted Loans
Performing Loans = [Total Loans] - [Total Defaults]

// Default Loss Exposure ($)
Potential Loss = 
    CALCULATE(
        SUM(loan_features[loan_amount]),
        loan_features[default_flag] = 1
    )

// Loss Rate by Exposure
Loss Rate % = DIVIDE([Potential Loss], [Total Exposure], 0) * 100

// YoY Default Rate Change (if year dimension exists)
// YoY Default Change = [Default Rate %] - CALCULATE([Default Rate %], DATEADD(Calendar[Date], -1, YEAR))
```

---

## Part 3: Report Pages

### PAGE 1: Portfolio Overview
**Purpose:** High-level summary of lending portfolio health

**Layout:**
- **Top Row (KPI Cards):**
  - Total Loans (format: #,##0)
  - Default Count (format: #,##0)
  - Default Rate % (format: 0.0%)
  - Total Exposure (format: $#,##0)

- **Visual 1 (Donut Chart - Top Left):**
  - Legend: Grade
  - Values: Count of Loans
  - Color: By Risk Level (Auto-generated)
  - Title: "Loan Distribution by Grade"

- **Visual 2 (Bar Chart - Top Right):**
  - X-Axis: State
  - Y-Axis: Default Rate %
  - Sort: Descending by Default Rate
  - Title: "Default Rate by State (Top 10)"
  - Limit: Top 10

- **Visual 3 (Card/Gauge - Bottom Left):**
  - Value: Avg Predicted PD
  - Format: 0.0%
  - Title: "Portfolio Average Risk Score"

- **Visual 4 (Stacked Bar - Bottom Right):**
  - X-Axis: Employment Length
  - Y-Axis: Default Rate %
  - Stacked by: Income Band
  - Title: "Default Rate by Employment & Income"

- **Slicers (Left Panel):**
  - Grade (buttons)
  - Purpose (dropdown)
  - State (dropdown)

---

### PAGE 2: Segment Risk Analysis
**Purpose:** Deep dive into risk by customer/loan segments

**Layout:**
- **Visual 1 (Matrix - Top Half):**
  - Rows: Grade
  - Columns: Purpose
  - Values: Count of Loans, Sum of Default Rate %
  - Title: "Default Rate by Grade × Purpose"
  - Conditional Formatting: Color scale (Red=High, Green=Low)

- **Visual 2 (Bar Chart - Bottom Left):**
  - X-Axis: Income Band
  - Y-Axis: Default Rate %
  - Series: Loan Term (24/36/60 months)
  - Title: "Risk Profile by Income & Loan Term"

- **Visual 3 (Treemap - Bottom Right):**
  - Group: Purpose
  - Values: Total Exposure
  - Color: Default Rate %
  - Title: "Loan Exposure & Risk by Purpose"

- **Slicers (Left Panel):**
  - Grade (buttons)
  - Home Ownership (dropdown)

---

### PAGE 3: Trend Analysis
**Purpose:** Monitor portfolio performance over time

**Layout:**
- **Visual 1 (Line Chart - Top):**
  - X-Axis: Issue Month (Date)
  - Y-Axis: Default Rate % (line), Count of Loans (column)
  - Dual Axis: Yes
  - Title: "Loan Issuance & Default Rate Trend"

- **Visual 2 (Combo Chart - Bottom Left):**
  - X-Axis: Issue Month
  - Y-Axis: Avg Loan Amount (bar), Avg Interest Rate % (line)
  - Title: "Pricing Trend: Loan Amount vs Interest Rate"

- **Visual 3 (Column Chart - Bottom Right):**
  - X-Axis: Issue Month
  - Y-Axis: Default Count
  - Color: Grade
  - Title: "Default Count Trend by Grade"

- **Slicers (Top Panel):**
  - Grade (buttons)
  - Purpose (dropdown)
  - State (dropdown)
  - Income Band (dropdown)

---

### PAGE 4: Model Insights
**Purpose:** Validate model performance and risk predictions

**Layout:**
- **Visual 1 (Histogram - Top Left):**
  - X-Axis: Pred Default Probability (bins of 0.1)
  - Y-Axis: Count
  - Title: "Distribution of Predicted Default Probability"
  - Format: Frequency chart

- **Visual 2 (Scatter - Top Right):**
  - X-Axis: Pred Default Probability
  - Y-Axis: Actual Default (0/1)
  - Size: Loan Amount
  - Color: Grade
  - Title: "Model Calibration: Predicted vs Actual Default"

- **Visual 3 (Bar Chart - Bottom):**
  - X-Axis: Risk Band
  - Y-Axis: Actual Default Rate %
  - Color: Risk Band
  - Title: "Model Performance: Actual Default Rate by Risk Band"
  - Data Labels: On

- **Key Metric Cards (Below):**
  - High Risk Loans (count)
  - Medium Risk Loans (count)
  - Low Risk Loans (count)

---

### PAGE 5: Executive Summary (Optional)
**Purpose:** One-page snapshot for executives

**Layout:**
- KPI cards with sparklines (if available)
- Key metrics from other pages
- Top risks and alerts
- Recommendation summary

---

## Part 4: Interactivity & Navigation

### Bookmark Navigation
Create bookmarks for:
1. "High Risk Focus" - Filter to High Risk Loans
2. "By State" - Switch to State view
3. "Trending Up" - Show increasing default rates

### Drill-Through
- From Grade card → Detail table of loans in that grade
- From State bar → Detailed loans for that state

### Dynamic Titles
Use formula titles that update with filters:
```dax
Title = "Portfolio Overview" & IF(HASONEVALUE(loan_features[grade]), " - " & VALUES(loan_features[grade]), " - All Grades")
```

---

## Part 5: Formatting & Design

### Color Scheme
- **Risk Levels:**
  - High Risk: Red (#E81123)
  - Medium Risk: Orange (#FFB900)
  - Low Risk: Green (#107C10)

- **Charts:**
  - Primary: Blue (#0078D4)
  - Secondary: Gray (#605E5C)

### Typography
- Title: Segoe UI, 14pt, Bold
- Labels: Segoe UI, 11pt
- Values: Segoe UI, 12pt, Bold

### Formatting Standards
- Numbers: 1000 separator (e.g., 1,234)
- Percentages: 0.0% format
- Currency: $#,##0
- Dates: MMM YYYY (e.g., Jan 2025)

---

## Part 6: Performance Optimization

### Tips for Large Datasets
1. **Use Direct Query** if dataset > 100M rows
2. **Create aggregations** for slow measures
3. **Index key columns:** loan_id, grade, state, issue_month
4. **Limit visuals** to top 5-10 items when possible
5. **Use slicer presets** for common filters

### Query Folding
- Filter at source (CSV) before import if possible
- Use native SQL query for preprocessing

---

## Part 7: Deployment & Sharing

### Publishing Steps
1. Save `.pbix` file locally
2. Publish to Power BI Service: File → Publish
3. Select workspace (My Workspace or Team)
4. Wait for data refresh
5. Configure refresh schedule (daily at 6 AM recommended)

### Access Control
- Viewer: Portfolio Overview + Trends
- Analyst: All pages
- Admin: Manage data refresh & parameters

### Data Refresh
- **Scheduled:** Daily at 6 AM EST
- **Manual:** Refresh button in Power BI Service
- **Incremental:** Implement if data grows beyond 1GB

---

## Part 8: Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing relationships | Check Data Model tab → Create inactive relationships |
| Blank slicers | Verify data loaded correctly → Refresh data |
| Slow performance | Reduce visuals per page, use aggregations |
| Incorrect totals | Check DAX syntax → Verify table joins |
| Date issues | Ensure date column recognized as Date type |

---

## Next Steps
1. Open Power BI Desktop
2. Import the four CSV files from `data/processed/`
3. Create relationships as outlined
4. Build DAX measures (copy-paste from Part 2)
5. Create visuals following Part 3 layouts
6. Apply formatting from Part 5
7. Publish to Power BI Service
