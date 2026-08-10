def run_data_agent(area_m2, annual_kwh, annual_cost):
    errors = []
    if area_m2 <= 0:
        errors.append("Η επιφάνεια πρέπει να είναι θετική.")
    if annual_kwh <= 0:
        errors.append("Η ετήσια κατανάλωση πρέπει να είναι θετική.")
    if annual_cost <= 0:
        errors.append("Το ετήσιο κόστος πρέπει να είναι θετικό.")

    if errors:
        return {
            "status": "REJECTED",
            "errors": errors,
            "message": "Τα δεδομένα δεν πέρασαν τον αρχικό έλεγχο."
        }

    eui = annual_kwh / area_m2
    cost_intensity = annual_cost / area_m2
    effective_price = annual_cost / annual_kwh

    return {
        "status": "PASS",
        "area_m2": area_m2,
        "annual_kwh": annual_kwh,
        "annual_cost": annual_cost,
        "eui": eui,
        "cost_intensity": cost_intensity,
        "effective_price": effective_price,
        "message": "Τα δεδομένα επικυρώθηκαν και προωθήθηκαν στον Math Agent."
    }
