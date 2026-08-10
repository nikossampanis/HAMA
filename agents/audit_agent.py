def run_audit_agent(baseline_cost, energy_payload, tolerance=1e-9):
    audited = []
    all_pass = True

    for item in energy_payload["results"]:
        expected_saving = baseline_cost * item["reduction_percent"] / 100
        error = abs(item["reported_saving"] - expected_saving)
        passed = error <= tolerance
        all_pass = all_pass and passed

        audited.append({
            **item,
            "expected_saving": expected_saving,
            "audit_error": error,
            "audit_status": "PASS" if passed else "REJECTED"
        })

    return {
        "status": "PASS" if all_pass else "REJECTED",
        "results": audited,
        "message": (
            "Όλοι οι υπολογισμοί επαληθεύτηκαν."
            if all_pass
            else "Εντοπίστηκε ασυνέπεια. Το αποτέλεσμα επιστρέφει στον Energy Agent."
        )
    }
