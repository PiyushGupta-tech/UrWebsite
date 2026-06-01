"""Dashboard preview data for hero section — Urbanrupee merchant dashboard."""

DASHBOARD_DEMO = {
    "title": "Payin Analytics(May 2026)",
    "periods": ["Today", "Yesterday", "This Week", "This Month", "This Year", "All"],
    "default_period": "This Month",
    "rotate_interval_ms": 5000,
    "period_titles": {
        "Today": "Payin Analytics (Today)",
        "Yesterday": "Payin Analytics (Yesterday)",
        "This Week": "Payin Analytics (This Week)",
        "This Month": "Payin Analytics(May 2026)",
        "This Year": "Payin Analytics (This Year)",
        "All": "Payin Analytics (All Time)",
    },
    "period_snapshots": {
        "Today": {
            "success_rate": 70.53,
            "stats": [
                {
                    "label": "All Transactions",
                    "value": "₹8,42,156.20",
                    "sub": "38 transactions",
                    "variant": "navy",
                },
                {
                    "label": "Successful",
                    "value": "₹5,98,364.26",
                    "sub": "27 transactions",
                    "variant": "blue",
                },
                {
                    "label": "Success Rate",
                    "value": "70.53%",
                    "sub": "27 of 38 payins",
                    "variant": "cyan",
                },
            ],
            "status_distribution": [
                {"label": "Successful", "percent": 71, "color": "#22c55e"},
                {"label": "Pending", "percent": 19, "color": "#eab308"},
                {"label": "Failed", "percent": 10, "color": "#ef4444"},
            ],
        },
        "Yesterday": {
            "success_rate": 73.17,
            "stats": [
                {
                    "label": "All Transactions",
                    "value": "₹9,18,420.50",
                    "sub": "41 transactions",
                    "variant": "navy",
                },
                {
                    "label": "Successful",
                    "value": "₹6,71,771.10",
                    "sub": "30 transactions",
                    "variant": "blue",
                },
                {
                    "label": "Success Rate",
                    "value": "73.17%",
                    "sub": "30 of 41 payins",
                    "variant": "cyan",
                },
            ],
            "status_distribution": [
                {"label": "Successful", "percent": 73, "color": "#22c55e"},
                {"label": "Pending", "percent": 17, "color": "#eab308"},
                {"label": "Failed", "percent": 10, "color": "#ef4444"},
            ],
        },
        "This Week": {
            "success_rate": 75.0,
            "stats": [
                {
                    "label": "All Transactions",
                    "value": "₹72,48,920.00",
                    "sub": "248 transactions",
                    "variant": "navy",
                },
                {
                    "label": "Successful",
                    "value": "₹54,36,690.00",
                    "sub": "186 transactions",
                    "variant": "blue",
                },
                {
                    "label": "Success Rate",
                    "value": "75.00%",
                    "sub": "186 of 248 payins",
                    "variant": "cyan",
                },
            ],
            "status_distribution": [
                {"label": "Successful", "percent": 75, "color": "#22c55e"},
                {"label": "Pending", "percent": 15, "color": "#eab308"},
                {"label": "Failed", "percent": 10, "color": "#ef4444"},
            ],
        },
        "This Month": {
            "success_rate": 76.21,
            "stats": [
                {
                    "label": "All Transactions",
                    "value": "₹31,757,676.59",
                    "sub": "1,114 transactions",
                    "variant": "navy",
                },
                {
                    "label": "Successful",
                    "value": "₹2,41,92,847.66",
                    "sub": "849 transactions",
                    "variant": "blue",
                },
                {
                    "label": "Success Rate",
                    "value": "76.21%",
                    "sub": "849 of 1,114 payins",
                    "variant": "cyan",
                },
            ],
            "status_distribution": [
                {"label": "Successful", "percent": 76, "color": "#22c55e"},
                {"label": "Pending", "percent": 16, "color": "#eab308"},
                {"label": "Failed", "percent": 8, "color": "#ef4444"},
            ],
        },
        "This Year": {
            "success_rate": 77.12,
            "stats": [
                {
                    "label": "All Transactions",
                    "value": "₹2,84,12,800.00",
                    "sub": "9,842 transactions",
                    "variant": "navy",
                },
                {
                    "label": "Successful",
                    "value": "₹2,19,11,234.18",
                    "sub": "7,590 transactions",
                    "variant": "blue",
                },
                {
                    "label": "Success Rate",
                    "value": "77.12%",
                    "sub": "7,590 of 9,842 payins",
                    "variant": "cyan",
                },
            ],
            "status_distribution": [
                {"label": "Successful", "percent": 77, "color": "#22c55e"},
                {"label": "Pending", "percent": 15, "color": "#eab308"},
                {"label": "Failed", "percent": 8, "color": "#ef4444"},
            ],
        },
        "All": {
            "success_rate": 78.0,
            "stats": [
                {
                    "label": "All Transactions",
                    "value": "₹1,24,80,500.00",
                    "sub": "4,280 transactions",
                    "variant": "navy",
                },
                {
                    "label": "Successful",
                    "value": "₹97,34,216.12",
                    "sub": "3,338 transactions",
                    "variant": "blue",
                },
                {
                    "label": "Success Rate",
                    "value": "78.00%",
                    "sub": "3,338 of 4,280 payins",
                    "variant": "cyan",
                },
            ],
            "status_distribution": [
                {"label": "Successful", "percent": 78, "color": "#22c55e"},
                {"label": "Pending", "percent": 14, "color": "#eab308"},
                {"label": "Failed", "percent": 8, "color": "#ef4444"},
            ],
        },
    },
    "stats": [
        {
            "label": "All Transactions",
            "value": "₹31,757,676.59",
            "sub": "1,114 transactions",
            "variant": "navy",
        },
        {
            "label": "Successful",
            "value": "₹2,41,92,847.66",
            "sub": "849 transactions",
            "variant": "blue",
        },
        {
            "label": "Success Rate",
            "value": "76.21%",
            "sub": "849 of 1,114 payins",
            "variant": "cyan",
        },
    ],
    "chart_views": ["Line", "Bar", "Histogram"],
    "status_distribution": [
        {"label": "Successful", "percent": 76, "color": "#22c55e"},
        {"label": "Pending", "percent": 16, "color": "#eab308"},
        {"label": "Failed", "percent": 8, "color": "#ef4444"},
    ],
    "sidebar": [
        {"section": None, "items": [{"label": "Dashboard", "icon": "home", "active": False}]},
        {
            "section": "PROVIDERS",
            "items": [{"label": "All Providers", "icon": "grid", "active": False}],
        },
        {
            "section": "STATEMENT",
            "items": [
                {"label": "In Ledger", "icon": "ledger", "active": True},
                {"label": "Out Ledger", "icon": "ledger", "active": False},
            ],
        },
        {
            "section": "USERS AREA",
            "items": [
                {"label": "Add User", "icon": "user", "active": False},
                {"label": "User List", "icon": "list", "active": False},
                {"label": "Referral Partners", "icon": "users", "active": False},
            ],
        },
    ],
}
