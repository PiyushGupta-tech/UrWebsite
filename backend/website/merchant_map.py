"""Merchant locations for the India map — one company per pointer.

Positions use state_id + offset_x/offset_y from SVG-calibrated anchors (viewBox 612×696).
Validated with browser isPointInFill against @svg-maps/india paths.
"""

MERCHANT_MAP = {
    "tag": "Pan-India presence",
    "locations": [
        {"id": "ludhiana", "state_id": "pb", "company": "SparkMudra", "offset_x": 0, "offset_y": 0},
        {"id": "chandigarh", "state_id": "ch", "company": "Revopay", "offset_x": 0, "offset_y": 0},
        {"id": "kurukshetra", "state_id": "hr", "company": "BingoPay", "offset_x": 0, "offset_y": 0},
        {"id": "gurugram", "state_id": "hr", "company": "Ambel Trade", "offset_x": 16, "offset_y": -28},
        {"id": "delhi-shadval", "state_id": "dl", "company": "Shadval Pay", "offset_x": 0, "offset_y": 0},
        {"id": "delhi-mobitm", "state_id": "dl", "company": "Mobitm Solutions", "offset_x": -4, "offset_y": -4},
        {"id": "delhi-evelocy", "state_id": "dl", "company": "E Velocy", "offset_x": 0, "offset_y": 4},
        {
            "id": "rajgarh-greenweb",
            "state_id": "mp",
            "company": "Green Web Solution",
            "offset_x": 0,
            "offset_y": 0,
        },
        {"id": "pune", "state_id": "mh", "company": "Dreamnexus Tech", "offset_x": 0, "offset_y": 0},
        {
            "id": "bengaluru-quickwave",
            "state_id": "ka",
            "company": "Quickwave Technologies",
            "offset_x": 0,
            "offset_y": 0,
        },
        {
            "id": "bengaluru-vyaptrix",
            "state_id": "ka",
            "company": "Vyaptrix Infotech",
            "offset_x": 0,
            "offset_y": -32,
        },
        {"id": "bengaluru-aai", "state_id": "ka", "company": "AAI Wallet", "offset_x": -32, "offset_y": 0},
        {
            "id": "ka-syllogi",
            "state_id": "ka",
            "company": "Syllogi Software Pvt Ltd",
            "offset_x": 0,
            "offset_y": 32,
        },
        {
            "id": "hyderabad-indyapay",
            "state_id": "tg",
            "company": "Indyapay (Mobifintree Services Pvt Ltd)",
            "offset_x": 0,
            "offset_y": 0,
        },
        {
            "id": "hyderabad-skriptonic",
            "state_id": "tg",
            "company": "Skriptonic Software Pvt Ltd",
            "offset_x": 0,
            "offset_y": -32,
        },
        {"id": "indore", "state_id": "mp", "company": "Barbari Pay", "offset_x": 0, "offset_y": -32},
        {"id": "tn-kuberan", "state_id": "tn", "company": "Kuberan Pay", "offset_x": 0, "offset_y": 0},
        {
            "id": "tn-unibeck",
            "state_id": "tn",
            "company": "UnibeckTech Service Pvt Ltd",
            "offset_x": 0,
            "offset_y": -32,
        },
        {
            "id": "rajasthan-groots",
            "state_id": "rj",
            "company": "Groots Technology Pvt Ltd",
            "offset_x": 0,
            "offset_y": 0,
        },
        {
            "id": "mp-greenweb-bhopal",
            "state_id": "mp",
            "company": "Green Web Software Pvt Ltd",
            "offset_x": -32,
            "offset_y": 0,
        },
        {"id": "gujarat-ojct", "state_id": "gj", "company": "Ojct Digicom Pvt Ltd", "offset_x": 0, "offset_y": 0},
        {"id": "gujarat-luxpay", "state_id": "gj", "company": "Luxpay", "offset_x": 0, "offset_y": -32},
    ],
}
