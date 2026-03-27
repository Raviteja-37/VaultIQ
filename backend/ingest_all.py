from app.ingestion.pipeline import ingest_document
import os

DOCUMENTS = [
    # Format: (filename, namespace, version)
    ("KYC_Policy_v2.1.txt",           "sop",        "v2.1"),
    ("NACH_Mandate_SOP_v1.8.txt",     "sop",        "v1.8"),
    ("Loan_Processing_SOP_v3.2.txt",  "sop",        "v3.2"),
    ("Customer_Grievance_SOP_v2.0.txt","sop",       "v2.0"),
    ("AML_Compliance_Policy_v4.0.txt","compliance", "v4.0"),
    ("HR_Leave_Policy_v1.5.txt",      "hr",         "v1.5"),
    ("IT_Security_Policy_v2.3.txt",   "internal",   "v2.3"),
    ("Product_Guide_FD_v1.2.txt",     "public",     "v1.2"),
]

def ingest_all():
    base = "data/documents"
    success, failed = 0, 0
    for filename, namespace, version in DOCUMENTS:
        path = os.path.join(base, filename)
        if not os.path.exists(path):
            print(f"⚠️  Skipping {filename} — file not found")
            failed += 1
            continue
        try:
            result = ingest_document(path, namespace, version)
            print(f"✅ {filename} → {namespace} ({result['chunks']} chunks)")
            success += 1
        except Exception as e:
            print(f"❌ Failed: {filename} — {e}")
            failed += 1

    print(f"\n🎉 Done! {success} ingested, {failed} failed.")

if __name__ == "__main__":
    ingest_all()