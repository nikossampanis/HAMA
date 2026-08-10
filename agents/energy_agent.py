def evaluate_scenarios(baseline_cost, scenarios, inject_error=False):
    results = []
    for idx, item in enumerate(scenarios):
        reduction = item["reduction_percent"] / 100
        saving = baseline_cost * reduction

        # Προαιρετικό σκόπιμο σφάλμα για το εκπαιδευτικό demo του Audit Agent.
        reported_saving = saving
        if inject_error and idx == 1:
            reported_saving = saving + 1000

        new_cost = baseline_cost - reported_saving
        payback = item["investment_cost"] / saving if saving > 0 else None

        results.append({
            **item,
            "true_saving": saving,
            "reported_saving": reported_saving,
            "reported_new_cost": new_cost,
            "payback_years": payback
        })

    return {
        "status": "PASS",
        "results": results,
        "message": "Τα ενεργειακά σενάρια υπολογίστηκαν και στάλθηκαν για ανεξάρτητο audit."
    }
