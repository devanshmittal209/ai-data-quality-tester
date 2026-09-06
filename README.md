# DataGuard AI

**AI-assisted data quality testing and dataset inspection tool built with Python and Streamlit.**

[Live Demo](https://ai-data-quality-tester-u3hykngv4de8f3xy8ppnhb.streamlit.app/)

---

## Overview

DataGuard AI is a lightweight data quality testing tool that helps identify common problems in CSV datasets and provides AI-assisted insights into the detected issues.

The application combines deterministic data quality checks using **Pandas and NumPy** with optional **Google Gemini-powered analysis** to explain potential data-quality risks and suggest practical next steps.

The goal is to make dataset inspection faster, more transparent, and easier to understand.

---

## Features

- Upload and inspect CSV datasets
- Dataset overview:
  - Number of rows and columns
  - Missing values
  - Duplicate records
- Automated data quality checks:
  - Missing values
  - Duplicate rows
  - Negative numeric values
  - Potential statistical outliers using IQR
  - Whitespace inconsistencies in categorical/text columns
- Overall data quality score
- Issue severity classification:
  - High
  - Medium
  - Low
- View affected records for individual issues
- Optional Gemini-powered analysis of detected issues
- Interactive AI assistant for questions about the detected issues
- Persistent analysis state within the Streamlit session
- Dark-themed dataset inspection interface

---

## How It Works

```text
CSV Dataset
     |
     v
Dataset Profiling
     |
     v
Data Quality Engine
     |
     +-- Missing Values
     +-- Duplicates
     +-- Negative Values
     +-- Outliers
     +-- Text Inconsistencies
     |
     v
Quality Score + Issue Severity
     |
     +-------------------+
     |                   |
     v                   v
Affected Records     AI Analysis
                         |
                         v
                  Recommendations


The core quality checks are performed deterministically rather than relying on an AI model.
Gemini is used as an additional interpretation layer to explain the detected issues and provide recommendations.
```

---

## Data Quality Checks

- Missing Values: Identifies columns containing null or missing values and reports the number and percentage of affected records.
-Duplicate Records: Detects duplicate rows that may indicate repeated or incorrectly ingested records.
-Negative Numeric Values: Flags negative values in numeric columns where they may indicate invalid data.
-Potential Outliers: Uses the Interquartile Range (IQR) method to identify statistically unusual numeric values.
-Whitespace Inconsistency: Detects leading or trailing whitespace in categorical/text fields that can create inconsistent values during analysis.

---

## AI-Assisted Analysis

After running the deterministic quality checks, users can optionally generate AI insights using Google Gemini.

The AI receives a structured summary of the detected quality issues rather than the entire dataset. This keeps the AI layer focused on interpreting the results produced by the quality engine.

Users can also ask questions about the detected issues and possible corrective actions.

For example:

Should I remove the sales_amount outliers?

The AI provides contextual explanations and practical recommendations based on the detected quality issues.

---

## Tech Stack

-Python
-Streamlit — web application and interface
-Pandas — data processing and analysis
-NumPy — numerical analysis
-Google Gemini API — AI-assisted insights and Q&A
-python-dotenv — local environment variable management

---

## Deployment

DataGuard AI is deployed using Streamlit Community Cloud.

The Gemini API key is stored securely as a deployment secret and is not included in the GitHub repository.

Live Application:
https://ai-data-quality-tester-u3hykngv4de8f3xy8ppnhb.streamlit.app/

---

## Why I Built This

Data quality is often the first step before meaningful analytics, reporting, or machine learning workflows.

I built DataGuard AI to explore how an automated data-quality layer can identify common dataset problems while using AI to make those findings easier to interpret and act on.

The project gave me hands-on experience with data validation, statistical analysis, stateful Streamlit applications, API integration, environment-based secrets, and cloud deployment.

---

## Future Improvements

-Additional schema and data-type validation
-Configurable data-quality rules
-Custom validation thresholds
-Data-quality trend tracking across dataset versions
-Exportable quality reports
-Additional data profiling metrics
---