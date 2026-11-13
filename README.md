# ☕ Afficionado Coffee Roasters: Sales Trend & Time-Based Performance Dashboard

**A data-driven Streamlit analytics dashboard** analyzing temporal sales patterns across three specialty coffee locations.

This interactive dashboard reveals **when customers shop**, enabling data-driven decisions for staff scheduling, inventory management, and operational planning at Afficionado Coffee Roasters.

---

## 🎯 What This Dashboard Does

- 📊 **Visualizes 149,116 transactions** across 181 trading days (Jan–Jun 2025)
- 🏪 **Compares performance** across 3 locations: Astoria, Hell's Kitchen, Lower Manhattan
- ⏰ **Identifies peak hours** and demand patterns throughout the day
- 📈 **Tracks revenue trends** with interactive filtering and aggregations
- ✅ **Validates data quality** with automated checks and reconstruction details

---

## � Quick Start

### Local Setup (2 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

Open your browser to `http://localhost:8501`

### Deploy to Streamlit Cloud (Free, 3 clicks)

1. Push this repo to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Click **"New app"** → select your repo, branch, and `app.py`
4. Done! Your app is live at `https://your-app-name.streamlit.app`

---

## 📊 Dashboard Tabs

### 1️⃣ Overview
- Daily revenue trend with 7-day moving average
- Weekly trends by store
- Monthly total bar chart
- Key metrics: total revenue, transactions, units sold, average ticket

### 2️⃣ Day of Week
- Average daily revenue and transaction count by day
- Weekday vs. weekend comparison
- Statistical summary (best day, worst day, gap percentage)

### 3️⃣ Hourly Heatmaps
- Hour × Day of week heatmap (normalized by day count)
- Hourly bar chart showing peak transaction hours
- Peak hour identification (top 3 hours highlighted)

### 4️⃣ Location Comparison
- Hourly heatmap per store (side-by-side)
- Demand curve by store (normalized % of daily total)
- Time-bucket stacked bar chart (Morning, Afternoon, Evening)
- Peak hour table per store

### 5️⃣ Data Quality
- Validation checks: missing values, duplicates, invalid data
- Trading day reconstruction details
- Operating hours summary

---

## �️ Filter Controls (Sidebar)

| Control | Options |
|---------|---------|
| **Store Location** | All, or select specific stores |
| **Day of Week** | Mon–Sun (multi-select) |
| **Hour Range** | 0–23 (slider) |
| **Metric** | Revenue ($) or Quantity (units) |
| **First Trading Day** | Date picker (default: 1 Jan 2025) |

---

## 🔑 Key Findings

### Revenue & Volume
- **Growth:** +104% from Jan ($81.7k) to Jun ($166.5k)
- **Tickets:** Stable ~$4.70 average (growth driven by volume, not price)
- **Consistency:** Best vs. worst day only differs by 3.3% (no significant day-of-week effect)

### Hourly Demand
- **Peak Hour:** 10:00 AM (holds 36% of daily transactions)
- **Morning Rush:** 8:00–10:59 AM captures majority of sales
- **Midday Slump:** 11:00 AM–5:00 PM volume halves
- **Evening:** Recovery after 5:00 PM (varies by store)

### Store Differences
- **Hell's Kitchen** — Most morning-heavy; strong early customer base
- **Lower Manhattan** — Earliest start time; evening fade
- **Astoria** — Strongest evening trade; most balanced distribution

---

## 📁 Files in This Repository

```
.
├── app.py                                    # Main Streamlit app
├── requirements.txt                          # Dependencies
├── Afficionado_Coffee_Roasters_Cleaned.xlsx # Dataset (load in app)
└── README.md                                 # This file
```

---

## 📊 Dataset Details

**149,116 transactions** | **181 trading days** | **3 stores**

| Column | Description |
|--------|-------------|
| `transaction_id` | Unique transaction ID |
| `transaction_time` | Time of day (HH:MM:SS) |
| `transaction_qty` | Units purchased |
| `unit_price` | Price per unit ($) |
| `store_location` | Astoria, Hell's Kitchen, or Lower Manhattan |
| `product_category` | Product type (Espresso, Drip, Pastry, etc.) |
| `product_type` | Variant (Single Shot, Double, etc.) |
| `product_detail` | Flavor, blend, or special attributes |

**Important:** No explicit date column. Rows are chronological; time resets indicate new trading day. Dashboard reconstructs dates assuming start = 1 Jan 2025 (adjustable in sidebar).

---

## ⚙️ Feature Engineering

The app automatically creates:

- **`date`** — Reconstructed from time-of-day resets
- **`hour`** — Hour of day (0–23)
- **`day_of_week`** — Monday–Sunday
- **`revenue`** — `transaction_qty × unit_price`
- **`time_bucket`** — Morning (6–11), Afternoon (12–16), Evening (17–21), Late (22–5)
- **`week`** — Week start date for aggregation

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | Streamlit |
| **Language** | Python 3.8+ |
| **Data** | Pandas, NumPy |
| **Viz** | Plotly Express |
| **Excel** | Openpyxl |

---

## ✨ Features

✅ **Caching** — Fast data loads (loads once per app start)  
✅ **Responsive** — Handles 150K+ rows smoothly  
✅ **Flexible Filters** — Combine any store/day/hour filters  
✅ **Export-Ready** — All metrics can be screenshot/documented  
✅ **Mobile-Friendly** — Responsive design on mobile browsers  

---

## 💡 Business Applications

| Use Case | How to Use |
|----------|-----------|
| **Staff Scheduling** | Peak hours (8–11 AM) need more staff; 11 AM–5 PM can be lean |
| **Inventory** | Stock high-demand items for morning rush |
| **Marketing** | Promotions during 11 AM–5 PM slump to boost mid-day traffic |
| **Store Hours** | Consider opening 6 AM, closing 6 PM (covers 95% of demand) |
| **Store Comparison** | Hell's Kitchen early morning specialist; Astoria evening focus |

---

## ⚠️ Limitations

- **Date Reconstruction:** Assumes times logged chronologically; no external date validation
- **Time Gaps:** No data 22:00–05:59 (overnight closure)
- **Sample Size:** 6 months only (can't isolate seasonal vs. growth effects)
- **Missing Context:** No weather, events, staffing, or customer type data
- **Variable Pricing:** 15 products show 2 prices (~1% of rows); retained as-is

---

## 🧹 Data Cleaning

**What Was Cleaned:**
- 1,952 trailing spaces (product details) — trimmed
- No missing values, no duplicates, no invalid prices/quantities
- 13 bulk orders (6+ units) kept as plausible
- 15 variable prices kept (cause unknown; retained for transparency)

**Result:** 149,116 rows in → 149,116 rows out (zero deletions)

---

## 📖 How to Interpret Results

### Reading Charts

- **Daily Trend Graph:** Green = revenue, blue = 7-day average (smooths daily noise)
- **Heatmaps:** Dark orange = high activity; light = low activity
- **Stacked Charts:** Heights compare time buckets; width shows date progression

### Adjusting Filters

- **Single Store:** See location-specific patterns
- **Hour Range 6–12:** Isolate morning behavior
- **Weekdays Only:** Compare Mon–Fri patterns
- **Quantity vs. Revenue:** Volume trends vs. $ trends

---

## 📞 Support

**Data looks wrong?**
- Check the **Data Quality** tab for validation details
- Adjust **"First trading day"** if dates seem off
- Upload your own Excel file via sidebar to test different datasets

**App runs slowly?**
- Streamlit Cloud free tier has RAM limits
- Upgrade to Streamlit+ for better performance

---

## 📄 Related Deliverables

**Outside this repo:**
- `Afficionado_Research_Paper.docx` — Full EDA, recommendations, detailed analysis
- `Afficionado_Executive_Summary.docx` — One-page summary for stakeholders
- Cleaned dataset with data dictionary and cleaning log

---

## 🎓 Project Context

**Internship Project:** Unified Mentor – Data Analytics Track

**Skills Demonstrated:**
- Data cleaning & validation
- Time-series analysis
- Feature engineering
- Data visualization (Plotly)
- Interactive dashboard development (Streamlit)
- Business intelligence & insights

---

## 📝 License

This project is provided as-is for educational purposes.

---

**Ready to deploy?** Push to GitHub and connect to [Streamlit Cloud](https://streamlit.io/cloud) in 3 clicks! 🚀
