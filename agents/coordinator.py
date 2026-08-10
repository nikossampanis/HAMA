def run_coordinator(data_payload, math_payload, audit_payload, business_payload):
    statuses = {
        "DATA": data_payload.get("status", "WAITING"),
        "MATH": math_payload.get("status", "WAITING"),
        "AUDIT": audit_payload.get("status", "WAITING"),
        "BUSINESS": business_payload.get("status", "WAITING"),
    }

    if not all(v == "PASS" for v in statuses.values()):
        return {
            "status": "MISSION NOT COMPLETE",
            "statuses": statuses,
            "message": "Ο Master Coordinator δεν εγκρίνει την αποστολή ακόμη."
        }

    selected = business_payload["selected"]
    achieved = selected["reduction_percent"] >= math_payload["target_percent"]

    return {
        "status": "MISSION ACCOMPLISHED" if achieved else "MISSION FAILED",
        "statuses": statuses,
        "selected": selected,
        "message": (
            "Ο HAMA πέτυχε τον επιχειρηματικό στόχο."
            if achieved
            else "Ο HAMA δεν πέτυχε τον αρχικό στόχο."
        )
    }
