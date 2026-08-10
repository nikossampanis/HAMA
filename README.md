# HAMA — Human–AI Master Agent School Energy Startup Lab

Διαδραστική εφαρμογή Streamlit για εκπαιδευτικό σενάριο μαθητικής επιχειρηματικότητας.

## Τι κάνει
- Demo School ή εισαγωγή πραγματικών σχολικών δεδομένων.
- Data Agent: έλεγχος και κανονικοποίηση δεδομένων.
- Math Agent: KPI στόχου εξοικονόμησης.
- Energy Agent: αξιολόγηση επενδυτικών σεναρίων.
- Audit Agent: ανεξάρτητη επαλήθευση και δυνατότητα REJECT.
- Business Agent: επιλογή εφικτής επιχειρηματικής πρότασης.
- Master Coordinator: τελική απόφαση SUCCESS / FAILED.
- Export αποτελεσμάτων σε CSV και JSON.

## Εκτέλεση τοπικά
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud
1. Ανέβασε όλο τον φάκελο σε GitHub repository.
2. Στο Streamlit Community Cloud επίλεξε το repository.
3. Main file: `app.py`
4. Deploy.

## Σημαντικό
Η εφαρμογή είναι αυτοτελής και δεν χρειάζεται API key. Οι "agents" εδώ είναι
δομημένοι ψηφιακοί ρόλοι με τυποποιημένα handoffs και verification loop.
Αυτό κάνει το demo αναπαραγώγιμο και ασφαλές για συνέδριο/τάξη.
