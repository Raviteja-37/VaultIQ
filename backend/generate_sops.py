import os

SOPS = {
    "KYC_Policy_v2.1.txt": """
KYC POLICY — Standard Operating Procedure v2.1
Department: Compliance | Updated: January 2025

1. CUSTOMER IDENTIFICATION
All new customers must provide valid government-issued photo ID.
Accepted: Aadhaar Card, PAN Card, Passport, Voter ID, Driving License.
Foreign nationals: Passport + Visa copy mandatory.

2. ADDRESS VERIFICATION
Proof of address required within 30 days of account opening.
Accepted: Utility bill, Bank statement, Rental agreement (not older than 3 months).
Digital copies accepted if attested by a gazetted officer.

3. RISK CATEGORIZATION
Low Risk: Salaried individuals, government employees.
Medium Risk: Self-employed, small business owners.
High Risk: PEPs (Politically Exposed Persons), foreign nationals, cash-heavy businesses.

4. EXCEPTION HANDLING
If customer cannot provide standard KYC documents:
- Escalate to Branch Manager immediately.
- Branch Manager may approve alternative docs on case-by-case basis.
- Log exception in CRM with reason code EXC-KYC-01.
- Report to Compliance team within 24 hours.

5. KYC RENEWAL
Regular customers: Every 5 years.
Medium risk customers: Every 3 years.
High risk customers: Annually.
Failure to renew: Account flagged, transactions restricted after 30-day notice.

6. DIGITAL KYC (VIDEO KYC)
Permitted for savings accounts below Rs. 2 lakhs.
Customer must appear live on video with original documents.
Agent must record session and store for 5 years.
""",

    "NACH_Mandate_SOP_v1.8.txt": """
NACH MANDATE PROCESSING — SOP v1.8
Department: Operations | Updated: February 2025

1. WHAT IS NACH
National Automated Clearing House (NACH) is an electronic payment system
for recurring transactions like loan EMIs, insurance premiums, SIPs.

2. MANDATE REGISTRATION
Customer submits physical mandate form or e-mandate via net banking.
Verification: Bank verifies signature against records within 3 working days.
Activation: NPCI activates mandate within 10 working days of submission.

3. MANDATE FAILURE REASONS
Technical failure: System downtime at customer bank.
Insufficient funds: Balance below EMI amount on due date.
Account closed: Customer account no longer active.
Signature mismatch: Physical mandate rejected by destination bank.
Mandate expired: Mandate validity period has elapsed.

4. EXCEPTION HANDLING FOR MANDATE FAILURE
Step 1: System auto-retries after 24 hours (once).
Step 2: If retry fails, ops team notified via system alert.
Step 3: Customer notified via SMS and email within 2 hours.
Step 4: Ops executive contacts customer within 1 business day.
Step 5: If no response in 3 days, escalate to Collections team.
Reason code for CRM: EXC-NACH-01 (technical), EXC-NACH-02 (insufficient funds).

5. MANDATE CANCELLATION
Customer request: Process within 2 working days.
Bank-initiated: Only for account closure or court order.
Notify NPCI within 1 business day of cancellation.
""",

    "Loan_Processing_SOP_v3.2.txt": """
RETAIL LOAN PROCESSING — SOP v3.2
Department: Loans | Updated: December 2024

1. LOAN APPLICATION INTAKE
Accepted channels: Branch, website, mobile app, DSA (Direct Sales Agent).
Required documents: KYC docs, income proof, 6-month bank statement, ITR (2 years).
Property loans: Additional property documents, valuation report required.

2. CREDIT ASSESSMENT
Bureau check: CIBIL score minimum 700 for personal loans, 650 for home loans.
Income assessment: EMI/NMI ratio must not exceed 50%.
Employment verification: Minimum 2 years employment for salaried, 3 years for self-employed.

3. LOAN APPROVAL MATRIX
Up to Rs. 5 lakhs: Branch Manager approval.
Rs. 5–25 lakhs: Regional Credit Manager approval.
Rs. 25 lakhs–1 crore: Credit Committee approval.
Above Rs. 1 crore: Executive Credit Committee + Board approval.

4. LOAN DISBURSEMENT
Approval to disbursement: Maximum 7 working days for personal loans.
Home loans: Maximum 15 working days after property verification.
Disbursement only to borrower's own account — no third party.

5. RESTRUCTURING REQUESTS
Eligible after: Minimum 12 EMIs paid.
Reasons accepted: Job loss, medical emergency, natural disaster.
Customer submits: Written request + supporting documents.
Processing time: 15 working days.
Approval authority: Credit restructuring committee.

6. NPA (NON-PERFORMING ASSET) CLASSIFICATION
Special Mention Account (SMA-0): Overdue 1-30 days.
SMA-1: Overdue 31-60 days — relationship manager to contact customer.
SMA-2: Overdue 61-90 days — escalate to collections.
NPA: Overdue 90+ days — legal team notified.
""",

    "Customer_Grievance_SOP_v2.0.txt": """
CUSTOMER GRIEVANCE REDRESSAL — SOP v2.0
Department: Customer Service | Updated: November 2024

1. GRIEVANCE CHANNELS
Branch: Customer submits written complaint at branch.
Phone: Call center logs complaint, issues reference number.
Email: complaints@bank.com — acknowledged within 4 hours.
Online: Website grievance portal — auto-acknowledged instantly.
Regulator: RBI Banking Ombudsman for escalated complaints.

2. TAT (TURNAROUND TIME) STANDARDS
Account-related: 3 working days.
Transaction disputes: 7 working days.
Loan complaints: 10 working days.
Fraud complaints: 24 hours for blocking, 7 days for resolution.
All others: 14 working days maximum.

3. COMPLAINT CATEGORIES
L1 (Frontline): Simple queries, balance disputes — branch resolves.
L2 (Operations): Transaction errors, failed payments — ops team resolves.
L3 (Management): Unresolved L2, policy complaints — branch manager resolves.
L4 (Regulator): Unresolved within 30 days — RBI Ombudsman.

4. FRAUD COMPLAINT HANDLING
Immediate: Block card/account within 30 minutes of complaint.
Register FIR: Customer advised to file police complaint.
Investigation: Fraud team investigates within 3 days.
Provisional credit: For debit card fraud, provisional credit within 10 days.
Zero liability: If fraud reported within 3 days of occurrence.

5. COMPENSATION POLICY
Delays beyond TAT: Rs. 100 per day compensation to customer.
Wrongful charges: Full refund + 10% additional as goodwill.
Service failure: As per RBI compensation framework.
""",

    "AML_Compliance_Policy_v4.0.txt": """
ANTI-MONEY LAUNDERING POLICY — v4.0
Department: Compliance | Updated: January 2025

1. OVERVIEW
The bank is committed to full compliance with the Prevention of Money
Laundering Act (PMLA) 2002 and RBI AML guidelines. All staff must complete
AML training annually.

2. SUSPICIOUS TRANSACTION INDICATORS
Large cash transactions above Rs. 10 lakhs.
Multiple transactions just below reporting threshold (structuring).
Sudden increase in account activity inconsistent with customer profile.
Transactions with high-risk countries (FATF blacklist).
Frequent international wire transfers to unknown beneficiaries.

3. TRANSACTION MONITORING
System auto-flags transactions above Rs. 10 lakhs for CTR filing.
Suspicious transactions flagged by system or staff — STR filing required.
CTR filing: Within 7 days of transaction.
STR filing: Within 7 days of suspicion being established.
Reports filed with FIU-IND (Financial Intelligence Unit — India).

4. CUSTOMER DUE DILIGENCE (CDD)
Standard CDD: All customers at onboarding.
Enhanced CDD: PEPs, high-risk countries, unusual transaction patterns.
Simplified CDD: Low-risk products (basic savings below Rs. 50,000).

5. RECORD KEEPING
All KYC records: Minimum 5 years after account closure.
Transaction records: Minimum 5 years from date of transaction.
STR/CTR copies: Minimum 10 years.

6. STAFF RESPONSIBILITIES
All staff must report suspicious activity to Compliance Officer immediately.
Tipping off customers about AML investigation strictly prohibited.
Violation of AML policy: Disciplinary action up to termination.
""",

    "HR_Leave_Policy_v1.5.txt": """
HR LEAVE POLICY — v1.5
Department: Human Resources | Updated: March 2025

1. LEAVE ENTITLEMENTS (Annual)
Casual Leave (CL): 12 days per year. Cannot be carried forward.
Sick Leave (SL): 12 days per year. Requires medical certificate above 2 days.
Earned Leave (EL): 30 days per year. Can be carried forward up to 90 days.
Maternity Leave: 26 weeks (first 2 children). 12 weeks thereafter.
Paternity Leave: 5 days within 6 months of child birth.
Bereavement Leave: 3 days for immediate family.

2. LEAVE APPLICATION PROCESS
CL/EL: Apply minimum 3 days in advance through HR portal.
Sick Leave: Inform reporting manager by 10 AM on the day.
Emergency: Verbal approval from manager, formal application within 24 hours.

3. APPROVAL AUTHORITY
Up to 3 days: Reporting Manager.
4–7 days: Department Head.
Above 7 days: HR + Department Head joint approval.

4. LEAVE WITHOUT PAY (LWP)
After all leaves exhausted.
Maximum 30 days per year.
Requires HR Head approval.
Salary deducted proportionally.

5. HOLIDAY LIST 2025
National Holidays: Republic Day (Jan 26), Independence Day (Aug 15), Gandhi Jayanti (Oct 2).
Bank Holidays: As per RBI circular for respective state.
Festivals: 3 optional festival leaves from approved list per employee.
""",

    "IT_Security_Policy_v2.3.txt": """
IT SECURITY POLICY — v2.3
Department: IT & Cybersecurity | Updated: January 2025

1. PASSWORD POLICY
Minimum length: 12 characters.
Complexity: Uppercase, lowercase, number, special character required.
Expiry: Every 90 days.
Reuse: Last 10 passwords cannot be reused.
Failed attempts: Account locked after 5 failed attempts.

2. DATA CLASSIFICATION
Public: Marketing materials, published annual reports.
Internal: Operational documents, SOPs, policies.
Confidential: Customer data, financial data, audit reports.
Restricted: Board minutes, M&A information, salary data.

3. ACCESS CONTROL
Principle of least privilege: Staff get minimum access needed for job.
Access review: Quarterly review of all system access.
Privileged access: Dual approval required for admin-level access.
Remote access: VPN mandatory for all remote work.

4. INCIDENT RESPONSE
Detection to containment: Within 1 hour.
Notify CISO: Within 2 hours of confirmed incident.
Customer notification: Within 72 hours if customer data compromised.
RBI reporting: Within 6 hours for critical cybersecurity incidents.

5. ACCEPTABLE USE
Bank systems for official use only.
No unauthorized software installation.
USB devices prohibited on bank workstations.
Personal email on bank systems strictly prohibited.

6. DATA BACKUP
Critical systems: Real-time replication.
All systems: Daily backup, weekly offsite backup.
Recovery time objective (RTO): 4 hours for critical systems.
Recovery point objective (RPO): 1 hour for critical systems.
""",

    "Product_Guide_FD_v1.2.txt": """
FIXED DEPOSIT PRODUCT GUIDE — v1.2
Department: Products | Updated: February 2025

1. PRODUCT OVERVIEW
Fixed Deposits (FD) offer guaranteed returns at a fixed interest rate
for a predetermined tenure. Principal is protected. Interest is assured.

2. ELIGIBILITY
Resident individuals (single or joint).
HUF (Hindu Undivided Family).
Companies, trusts, associations.
NRIs: NRE/NRO fixed deposits available.

3. TENURE OPTIONS
Minimum: 7 days.
Maximum: 10 years.
Short term (7 days – 1 year): Ideal for parking surplus funds.
Long term (1–10 years): Higher interest rates, tax benefits under 80C (5 year lock-in).

4. INTEREST RATES (Indicative — check current rates)
7–45 days: 4.00% p.a.
46–179 days: 5.50% p.a.
180–364 days: 6.00% p.a.
1–2 years: 6.75% p.a.
2–5 years: 7.00% p.a.
5–10 years: 7.25% p.a.
Senior citizens: Additional 0.50% on all tenures.

5. PREMATURE WITHDRAWAL
Allowed with penalty: 1% deduction from applicable rate.
No premature withdrawal: Tax-saving FD (5-year lock-in).
Partial withdrawal: Not allowed. Must break entire FD.

6. NOMINATION
Nomination mandatory for all individual FDs.
Up to 4 nominees allowed.
Nominee receives proceeds in case of depositor's death.

7. RENEWAL
Auto-renewal: Default option, same tenure, prevailing rate at maturity.
Manual renewal: Customer must visit branch or use net banking within 30 days.
Maturity proceeds: Credited to linked savings account if not renewed.
"""
}

def generate():
    os.makedirs("data/documents", exist_ok=True)
    for filename, content in SOPS.items():
        path = f"data/documents/{filename}"
        with open(path, "w") as f:
            f.write(content.strip())
        print(f"✅ Created: {filename}")
    print(f"\n🎉 Generated {len(SOPS)} SOP documents in data/documents/")

if __name__ == "__main__":
    generate()