from __future__ import annotations

from typing import Dict, Any
import pandas as pd


def validate_credit_risk_df(df: pd.DataFrame) -> Dict[str, Any]:
    results = {
        "success": True,
        "checks": [],
        "failed_checks": [],
        "summary": {},
    }

    expected_columns = [
        "Unnamed: 0",
        "Age",
        "Sex",
        "Job",
        "Housing",
        "Saving accounts",
        "Checking account",
        "Credit amount",
        "Duration",
        "Purpose",
    ]

    missing_cols = [c for c in expected_columns if c not in df.columns]
    col_check = {
        "check": "expected_columns_present",
        "passed": len(missing_cols) == 0,
        "missing_columns": missing_cols,
    }
    results["checks"].append(col_check)
    if not col_check["passed"]:
        results["failed_checks"].append(col_check)

    if missing_cols:
        results["success"] = False
        results["summary"] = {
            "rows": int(df.shape[0]),
            "cols": int(df.shape[1]),
            "reason": "missing required columns",
        }
        return results

    row_check = {
        "check": "row_count_gt_0",
        "passed": len(df) > 0,
        "row_count": int(len(df)),
    }
    results["checks"].append(row_check)
    if not row_check["passed"]:
        results["failed_checks"].append(row_check)

    null_thresholds = {
        "Age": 0.00,
        "Sex": 0.00,
        "Job": 0.00,
        "Housing": 0.00,
        "Saving accounts": 0.60,
        "Checking account": 0.60,
        "Credit amount": 0.00,
        "Duration": 0.00,
        "Purpose": 0.00,
    }

    for col, threshold in null_thresholds.items():
        null_rate = float(df[col].isna().mean())
        check = {
            "check": f"null_rate_{col}",
            "passed": null_rate <= threshold,
            "column": col,
            "null_rate": null_rate,
            "threshold": threshold,
        }
        results["checks"].append(check)
        if not check["passed"]:
            results["failed_checks"].append(check)

    numeric_rules = {
        "Age": (18, 100),
        "Job": (0, 10),
        "Credit amount": (1, 1000000),
        "Duration": (1, 120),
    }

    for col, (min_val, max_val) in numeric_rules.items():
        series = pd.to_numeric(df[col], errors="coerce")
        invalid = int(((series < min_val) | (series > max_val) | (series.isna())).sum())
        check = {
            "check": f"range_{col}",
            "passed": invalid == 0,
            "column": col,
            "min": min_val,
            "max": max_val,
            "invalid_count": invalid,
        }
        results["checks"].append(check)
        if not check["passed"]:
            results["failed_checks"].append(check)

    allowed_categories = {
        "Sex": {"male", "female"},
        "Housing": {"own", "rent", "free"},
    }

    for col, allowed in allowed_categories.items():
        actual = set(df[col].dropna().astype(str).str.lower().unique())
        unexpected = sorted(actual - allowed)
        check = {
            "check": f"allowed_values_{col}",
            "passed": len(unexpected) == 0,
            "column": col,
            "unexpected_values": unexpected,
        }
        results["checks"].append(check)
        if not check["passed"]:
            results["failed_checks"].append(check)

    for col in ["Age", "Job", "Credit amount", "Duration"]:
        coerced = pd.to_numeric(df[col], errors="coerce")
        check = {
            "check": f"numeric_type_{col}",
            "passed": int(coerced.isna().sum()) == 0,
            "column": col,
        }
        results["checks"].append(check)
        if not check["passed"]:
            results["failed_checks"].append(check)

    results["success"] = len(results["failed_checks"]) == 0
    results["summary"] = {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "total_checks": len(results["checks"]),
        "failed_checks": len(results["failed_checks"]),
    }

    return results