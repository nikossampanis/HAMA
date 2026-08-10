def run_business_agent(audit_payload, target_percent, max_budget=None):
    if audit_payload.get("status") != "PASS":
        return {
            "status": "WAITING",
            "message": "Δεν μπορεί να ληφθεί επιχειρηματική απόφαση πριν περάσει το Audit."
        }

    feasible = []
    for item in audit_payload["results"]:
        meets_target = item["reduction_percent"] >= target_percent
        within_budget = True if max_budget is None else item["investment_cost"] <= max_budget
        if meets_target and within_budget:
            feasible.append(item)

    if not feasible:
        return {
            "status": "REJECTED",
            "message": "Κανένα σενάριο δεν ικανοποιεί ταυτόχρονα στόχο και διαθέσιμο budget.",
            "selected": None
        }

    # Ισορροπημένη επιλογή: ελάχιστος χρόνος αποπληρωμής,
    # με δεύτερο κριτήριο τη μεγαλύτερη ετήσια εξοικονόμηση.
    selected = sorted(
        feasible,
        key=lambda x: (x["payback_years"], -x["expected_saving"])
    )[0]

    return {
        "status": "PASS",
        "selected": selected,
        "feasible_count": len(feasible),
        "message": "Επιλέχθηκε το οικονομικά αποδοτικότερο σενάριο μεταξύ όσων περνούν τους περιορισμούς."
    }
