def run_math_agent(data_payload, target_percent):
    if data_payload.get("status") != "PASS":
        return {"status": "WAITING", "message": "Αναμονή έγκυρων δεδομένων από τον Data Agent."}

    c0 = data_payload["annual_cost"]
    required_saving = c0 * target_percent / 100
    target_cost = c0 - required_saving

    return {
        "status": "PASS",
        "baseline_cost": c0,
        "target_percent": target_percent,
        "required_saving": required_saving,
        "target_cost": target_cost,
        "message": "Ο επιχειρηματικός στόχος μετατράπηκε σε μαθηματικό KPI."
    }
