#!/usr/bin/env python3
"""Generate synthetic orchestration test data (130 goals) and test detection + server."""

import json
import sys
from pathlib import Path

app_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(app_dir.parent.parent.parent))  # noqa: TID251
sys.path.insert(0, str(app_dir))  # noqa: TID251

from services.template_executor import detect_template  # noqa: E402

# ── 1. Template Wording Variants (70 goals — 10 per template) ─────────

TEMPLATE_VARIANTS = [
    # ── churn_risk_analysis (10) ──
    {"goal": "We need to check if our clients are at risk of churning before the quarter ends", "expected_template": "churn_risk_analysis"},
    {"goal": "Can you evaluate the churn probability for our top-tier enterprise accounts?", "expected_template": "churn_risk_analysis"},
    {"goal": "The quarterly review showed high churn — analyze risk for the portfolio", "expected_template": "churn_risk_analysis"},
    {"goal": "Figure out which accounts have declining usage and flag them for retention", "expected_template": "churn_risk_analysis"},
    {"goal": "Our customer attrition rate spiked last month, run a deep analysis", "expected_template": "churn_risk_analysis"},
    {"goal": "Several key accounts are disengaging from our platform, investigate immediately", "expected_template": "churn_risk_analysis"},
    {"goal": "Are any of our enterprise clients about to cancel their subscriptions?", "expected_template": "churn_risk_analysis"},
    {"goal": "Management wants a churn risk report by EOD — check all accounts", "expected_template": "churn_risk_analysis"},
    {"goal": "Identify accounts that might cancel and notify the retention leads", "expected_template": "churn_risk_analysis"},
    {"goal": "Look at recent risk metrics and retention trends across all segments", "expected_template": "churn_risk_analysis"},

    # ── contract_renewal (10) ──
    {"goal": "Handle the account situation for ACC-1234 — their contract is up for renewal", "expected_template": "contract_renewal"},
    {"goal": "The agreement with our biggest client expires in two weeks, start the extension process", "expected_template": "contract_renewal"},
    {"goal": "We need to renew the subscription for Acme Corp (ACC-5555) ASAP", "expected_template": "contract_renewal"},
    {"goal": "Process renewal paperwork and apply the negotiated discount for ACC-7777", "expected_template": "contract_renewal"},
    {"goal": "Can you kick off the contract renewal workflow? The customer wants to continue", "expected_template": "contract_renewal"},
    {"goal": "Their license is expiring next month — start the renewal and get finance approval", "expected_template": "contract_renewal"},
    {"goal": "Extend the service contract for another year and send the updated quote", "expected_template": "contract_renewal"},
    {"goal": "The client asked about contract extension options — begin the renewal process", "expected_template": "contract_renewal"},
    {"goal": "Subscription for ACC-3210 is about to expire, handle the renewal end to end", "expected_template": "contract_renewal"},
    {"goal": "Prepare the renewal offer with appropriate pricing and submit for approval", "expected_template": "contract_renewal"},

    # ── incident_response (10) ──
    {"goal": "We have a production outage affecting multiple customers — activate response plan", "expected_template": "incident_response"},
    {"goal": "Critical incident: servers down in EU region, need immediate escalation", "expected_template": "incident_response"},
    {"goal": "Something is broken with the inventory system — respond to this incident now", "expected_template": "incident_response"},
    {"goal": "High severity incident reported: notify on-call engineers and begin triage", "expected_template": "incident_response"},
    {"goal": "Emergency malfunction at the warehouse — equipment failure needs response", "expected_template": "incident_response"},
    {"goal": "There's an outage in our payment processing system — escalate immediately", "expected_template": "incident_response"},
    {"goal": "Respond to the critical incident and notify all affected stakeholders", "expected_template": "incident_response"},
    {"goal": "The monitoring system triggered alerts — investigate and respond to this incident", "expected_template": "incident_response"},
    {"goal": "Major incident in progress: coordinate response and notify management", "expected_template": "incident_response"},
    {"goal": "Warehouse emergency: equipment malfunction in APAC-SOUTH, respond urgently", "expected_template": "incident_response"},

    # ── inventory_restock (10) ──
    {"goal": "Can you check inventory levels across all warehouses and flag low stock?", "expected_template": "inventory_restock"},
    {"goal": "Restock low-inventory items before the holiday rush hits", "expected_template": "inventory_restock"},
    {"goal": "We're running low on supplies in the EU warehouse — check and reorder", "expected_template": "inventory_restock"},
    {"goal": "Run a stock audit and trigger purchase orders for anything below threshold", "expected_template": "inventory_restock"},
    {"goal": "Check warehouse supply levels and replenish anything that's running low", "expected_template": "inventory_restock"},
    {"goal": "Make sure all distribution centers have adequate inventory for next month", "expected_template": "inventory_restock"},
    {"goal": "Our stock of Filter-H800 might be depleted — verify and restock across warehouses", "expected_template": "inventory_restock"},
    {"goal": "Review current inventory positions and place orders where supply is low", "expected_template": "inventory_restock"},
    {"goal": "Ensure supply chain readiness — check stock levels and restock as needed", "expected_template": "inventory_restock"},
    {"goal": "The warehouse manager reported low stock — verify availability and reorder", "expected_template": "inventory_restock"},

    # ── meeting_scheduler (10) ──
    {"goal": "Set up a product demo meeting with the client for next Tuesday", "expected_template": "meeting_scheduler"},
    {"goal": "Can we schedule a call with their team to discuss the integration?", "expected_template": "meeting_scheduler"},
    {"goal": "Book a meeting with the account manager to review Q3 performance", "expected_template": "meeting_scheduler"},
    {"goal": "Find a time slot and schedule an introductory session with the new client", "expected_template": "meeting_scheduler"},
    {"goal": "Arrange a conference call between our engineering leads and the customer", "expected_template": "meeting_scheduler"},
    {"goal": "Please schedule a kickoff meeting for the project with all stakeholders", "expected_template": "meeting_scheduler"},
    {"goal": "We need to book a time with the client's CTO for a technical deep-dive", "expected_template": "meeting_scheduler"},
    {"goal": "Coordinate a presentation meeting with the sales team and the prospect", "expected_template": "meeting_scheduler"},
    {"goal": "Set up a call with the customer to walk through the new features", "expected_template": "meeting_scheduler"},
    {"goal": "Schedule a quarterly review meeting between the CSM and account ACC-4567", "expected_template": "meeting_scheduler"},

    # ── onboarding_workflow (10) ──
    {"goal": "We just closed the deal — start the onboarding for Contoso (ACC-9999)", "expected_template": "onboarding_workflow"},
    {"goal": "New client signed yesterday — run the complete onboarding workflow", "expected_template": "onboarding_workflow"},
    {"goal": "Onboard Northwind Traders (ACC-2020) and assign CSM-15 as their success manager", "expected_template": "onboarding_workflow"},
    {"goal": "Begin the new customer activation process including welcome emails and kickoff", "expected_template": "onboarding_workflow"},
    {"goal": "A new enterprise account just signed up — set up everything for the new account to get started", "expected_template": "onboarding_workflow"},
    {"goal": "Process the onboarding for the new account and schedule the kickoff call", "expected_template": "onboarding_workflow"},
    {"goal": "We need to welcome the new customer and provision their services", "expected_template": "onboarding_workflow"},
    {"goal": "The sales team signed a new account ACC-6060 — start onboarding immediately", "expected_template": "onboarding_workflow"},
    {"goal": "Set up the new client with CRM entry, welcome package, and intro meeting", "expected_template": "onboarding_workflow"},
    {"goal": "Kick off the onboard process for our newest enterprise customer", "expected_template": "onboarding_workflow"},

    # ── re_engagement_campaign (10) ──
    {"goal": "Run a win-back campaign for customers who stopped using our platform", "expected_template": "re_engagement_campaign"},
    {"goal": "We have dormant accounts that haven't logged in — send them outreach emails", "expected_template": "re_engagement_campaign"},
    {"goal": "Launch the re-engagement email series for inactive customers from last quarter", "expected_template": "re_engagement_campaign"},
    {"goal": "Target lapsed users who haven't been contacted in 120+ days with a campaign", "expected_template": "re_engagement_campaign"},
    {"goal": "Send re-engage emails to accounts showing no activity in the past 3 months", "expected_template": "re_engagement_campaign"},
    {"goal": "Our inactive account list is growing — run re-engagement outreach (max 5)", "expected_template": "re_engagement_campaign"},
    {"goal": "Nudge dormant accounts back to the platform with personalized offers", "expected_template": "re_engagement_campaign"},
    {"goal": "We need to win back customers who haven't interacted in 60+ days", "expected_template": "re_engagement_campaign"},
    {"goal": "Execute the reengagement workflow for accounts with zero activity this quarter", "expected_template": "re_engagement_campaign"},
    {"goal": "Reach out to lapsed customers with a promotional campaign to re-engage them", "expected_template": "re_engagement_campaign"},
]

# ── 2. Unknown/New Template Goals (30 goals) ─────────────────────────

UNKNOWN_GOALS = [
    {"goal": "Compile a customer satisfaction report from survey responses", "expected_template": None},
    {"goal": "Process refund requests for flagged transactions", "expected_template": None},
    {"goal": "Generate compliance audit trail for Q4", "expected_template": None},
    {"goal": "Update pricing tiers based on usage analytics", "expected_template": None},
    {"goal": "Migrate customer data between CRM systems", "expected_template": None},
    {"goal": "Set up automated billing for new enterprise contracts", "expected_template": None},
    {"goal": "Run A/B test analysis on email campaign variants", "expected_template": None},
    {"goal": "Process employee PTO requests and update calendars", "expected_template": None},
    {"goal": "Generate quarterly board presentation with KPI dashboards", "expected_template": None},
    {"goal": "Reconcile vendor invoices against purchase orders for this month", "expected_template": None},
    {"goal": "Create user access review report for SOC2 compliance", "expected_template": None},
    {"goal": "Build a training curriculum for the new support team members", "expected_template": None},
    {"goal": "Archive old project files and update the knowledge base", "expected_template": None},
    {"goal": "Calculate sales commissions for the international team", "expected_template": None},
    {"goal": "Prepare tax documentation for the upcoming filing deadline", "expected_template": None},
    {"goal": "Analyze website traffic patterns and optimize landing pages", "expected_template": None},
    {"goal": "Deploy the latest microservice build to staging environment", "expected_template": None},
    {"goal": "Review and merge pending pull requests in the main repository", "expected_template": None},
    {"goal": "Set up disaster recovery failover procedures", "expected_template": None},
    {"goal": "Run performance benchmarks on the new database cluster", "expected_template": None},
    {"goal": "Draft an RFP response for the government procurement opportunity", "expected_template": None},
    {"goal": "Process insurance claims for damaged shipments from last week", "expected_template": None},
    {"goal": "Generate employee performance reviews for the engineering department", "expected_template": None},
    {"goal": "Coordinate the office relocation logistics and vendor bookings", "expected_template": None},
    {"goal": "Set up single sign-on integration with the customer's identity provider", "expected_template": None},
    {"goal": "Produce a competitive analysis report comparing our features to rivals", "expected_template": None},
    {"goal": "Schedule the annual company retreat and send invitations", "expected_template": None},
    {"goal": "Automate the data pipeline for daily ETL from partner APIs", "expected_template": None},
    {"goal": "Update the product roadmap based on recent customer feedback", "expected_template": None},
    {"goal": "Create a budget forecast for the next fiscal year", "expected_template": None},
    {"goal": "Rotate API keys and update secrets in the vault", "expected_template": None},
]

# ── 3. Edge Cases Within Known Templates (30 scenarios) ───────────────

EDGE_CASES = [
    # Churn edge cases
    {"goal": "Analyze churn risk for our enterprise customer portfolio",
     "expected_template": "churn_risk_analysis",
     "edge_case": "all_low_risk", "description": "All accounts have >90 days to renewal — no notifications should be sent"},
    {"goal": "Run churn prediction — we believe all accounts are healthy",
     "expected_template": "churn_risk_analysis",
     "edge_case": "empty_results", "description": "CRM search returns zero declining-usage accounts"},
    {"goal": "Check churn risk for a single account with declining usage",
     "expected_template": "churn_risk_analysis",
     "edge_case": "single_account", "description": "Only one account returned from CRM search"},

    # Contract renewal edge cases
    {"goal": "Process the contract renewal for ACC-0000 which doesn't exist in our CRM",
     "expected_template": "contract_renewal",
     "edge_case": "nonexistent_account", "description": "Account ID doesn't exist — crm_get_account returns error/empty"},
    {"goal": "Renew the contract for ACC-1234 — they have very low usage",
     "expected_template": "contract_renewal",
     "edge_case": "zero_discount", "description": "Low usage → 0% discount → no approval needed"},
    {"goal": "Handle the renewal for ACC-8888 — they're our highest-usage enterprise customer",
     "expected_template": "contract_renewal",
     "edge_case": "max_discount", "description": "High usage → 15% discount → needs finance approval"},
    {"goal": "Renew the contract but the subscription check shows it's already cancelled for ACC-4444",
     "expected_template": "contract_renewal",
     "edge_case": "cancelled_subscription", "description": "Subscription status is cancelled during renewal"},

    # Incident response edge cases
    {"goal": "Respond to the low severity incident affecting Widget-A100 in US-EAST",
     "expected_template": "incident_response",
     "edge_case": "low_severity", "description": "Low severity → no escalation to engineering_manager"},
    {"goal": "Respond to the medium severity incident affecting Sensor-B200 in EU-CENTRAL, APAC-SOUTH",
     "expected_template": "incident_response",
     "edge_case": "medium_severity", "description": "Medium severity → no escalation, still notifies oncall"},
    {"goal": "Handle the critical incident but we don't know which warehouses are affected",
     "expected_template": "incident_response",
     "edge_case": "no_warehouses", "description": "No warehouses extractable → empty inventory queries"},
    {"goal": "Respond to the critical incident affecting AllProducts in WH-1, WH-2, WH-3, WH-4, WH-5",
     "expected_template": "incident_response",
     "edge_case": "many_warehouses", "description": "Five warehouses → five inventory queries"},

    # Inventory restock edge cases
    {"goal": "Check inventory levels for Filter-H800 in APAC-SOUTH, US-EAST and alert if below 25 units",
     "expected_template": "inventory_restock",
     "edge_case": "all_stocked", "description": "All warehouses fully stocked → no notifications sent"},
    {"goal": "Check inventory for Widget-X in EU-CENTRAL — threshold below 100 units",
     "expected_template": "inventory_restock",
     "edge_case": "high_threshold", "description": "Very high threshold — most warehouses likely low"},
    {"goal": "Verify inventory for Gadget-Z in a single warehouse US-WEST",
     "expected_template": "inventory_restock",
     "edge_case": "single_warehouse", "description": "Only one warehouse to check"},
    {"goal": "Check inventory but no specific product is mentioned across warehouses",
     "expected_template": "inventory_restock",
     "edge_case": "no_sku", "description": "No SKU extractable — empty string for sku parameter"},

    # Meeting scheduler edge cases
    {"goal": "Schedule a demo meeting for FreeUser Corp (ACC-7070) with REP-01",
     "expected_template": "meeting_scheduler",
     "edge_case": "free_tier", "description": "Account is free tier → meeting blocked, notify rep"},
    {"goal": "Schedule a strategy meeting for Premium Inc (ACC-8080) with REP-02 but calendar is full",
     "expected_template": "meeting_scheduler",
     "edge_case": "no_slots", "description": "All time slots taken → meeting blocked"},
    {"goal": "Schedule a meeting for a premium client (ACC-9090) with REP-03",
     "expected_template": "meeting_scheduler",
     "edge_case": "happy_path", "description": "Premium account with available slots → meeting scheduled"},
    {"goal": "Schedule a review meeting for ACC-1111 but account is missing from CRM with REP-04",
     "expected_template": "meeting_scheduler",
     "edge_case": "missing_account", "description": "CRM returns error for account lookup"},

    # Onboarding edge cases
    {"goal": "Onboard new account Cancelled Corp (ACC-5050) assigned to CSM-10",
     "expected_template": "onboarding_workflow",
     "edge_case": "cancelled_subscription", "description": "Subscription status cancelled → onboarding blocked"},
    {"goal": "Start onboarding for PendingCo (ACC-6060) assigned to CSM-11",
     "expected_template": "onboarding_workflow",
     "edge_case": "pending_subscription", "description": "Subscription status pending → onboarding blocked"},
    {"goal": "Onboard new customer ActiveCo (ACC-7070) with CSM-12",
     "expected_template": "onboarding_workflow",
     "edge_case": "happy_path", "description": "Active subscription → full onboarding flow"},
    {"goal": "Run the onboarding workflow but the CRM has no record of ACC-0001 with CSM-13",
     "expected_template": "onboarding_workflow",
     "edge_case": "missing_account", "description": "Account not found in CRM"},

    # Re-engagement edge cases
    {"goal": "Re-engage inactive customers not contacted in 90 days (max 0)",
     "expected_template": "re_engagement_campaign",
     "edge_case": "max_zero_emails", "description": "max_emails=0 → no emails sent at all"},
    {"goal": "Run re-engagement campaign for dormant accounts not contacted in 30 days (max 1)",
     "expected_template": "re_engagement_campaign",
     "edge_case": "max_one_email", "description": "max_emails=1 → only one email sent"},
    {"goal": "Launch re-engagement for accounts not contacted in 365 days — long dormancy",
     "expected_template": "re_engagement_campaign",
     "edge_case": "long_dormancy", "description": "365 days dormancy filter → possibly zero results"},
    {"goal": "Run reengagement campaign but all found accounts have cancelled subscriptions",
     "expected_template": "re_engagement_campaign",
     "edge_case": "all_cancelled", "description": "No eligible accounts after subscription check"},
    {"goal": "Re-engage inactive accounts not contacted in 60 days (max 100)",
     "expected_template": "re_engagement_campaign",
     "edge_case": "high_max_emails", "description": "Very high max → sends to all eligible"},
    {"goal": "Win back dormant accounts with zero activity — we have no CRM data",
     "expected_template": "re_engagement_campaign",
     "edge_case": "empty_crm", "description": "CRM search returns zero accounts"},
]

# ── Combine all scenarios ─────────────────────────────────────────────

ALL_GOALS = TEMPLATE_VARIANTS + UNKNOWN_GOALS + EDGE_CASES


def run_detection_test(goals: list[dict]) -> tuple[int, int, list[dict]]:
    """Run detect_template against all goals. Returns (correct, total, misses)."""
    correct = 0
    total = len(goals)
    misses = []

    for g in goals:
        detected = detect_template(g["goal"])
        expected = g.get("expected_template")
        if detected == expected:
            correct += 1
        else:
            misses.append({
                "goal": g["goal"][:80],
                "detected": detected,
                "expected": expected,
                "edge_case": g.get("edge_case", ""),
            })

    return correct, total, misses


def main():
    # Save the dataset
    out_path = Path(__file__).parent / "orchestrate_v2.json"
    with open(out_path, "w") as f:
        json.dump(ALL_GOALS, f, indent=2)
    print(f"Saved {len(ALL_GOALS)} scenarios to {out_path.name}")

    # Run detection tests
    print("\n" + "=" * 72)
    print("TEMPLATE DETECTION ACCURACY REPORT")
    print("=" * 72)

    # Test category 1: Template wording variants
    c1, t1, m1 = run_detection_test(TEMPLATE_VARIANTS)
    print(f"\n  Template Wording Variants:  {c1}/{t1}  ({c1/t1*100:.1f}%)")

    # Test by individual template
    templates = [
        "churn_risk_analysis", "contract_renewal", "incident_response",
        "inventory_restock", "meeting_scheduler", "onboarding_workflow",
        "re_engagement_campaign",
    ]
    for tmpl in templates:
        subset = [g for g in TEMPLATE_VARIANTS if g["expected_template"] == tmpl]
        c, t, _ = run_detection_test(subset)
        status = "✓" if c == t else "✗"
        print(f"    {status} {tmpl:30s}  {c}/{t}")

    # Test category 2: Unknown goals
    c2, t2, m2 = run_detection_test(UNKNOWN_GOALS)
    print(f"\n  Unknown/New Template Goals:  {c2}/{t2}  ({c2/t2*100:.1f}%)")

    # Test category 3: Edge cases
    c3, t3, m3 = run_detection_test(EDGE_CASES)
    print(f"\n  Edge Cases (detection):     {c3}/{t3}  ({c3/t3*100:.1f}%)")

    # Overall
    total_correct = c1 + c2 + c3
    total_all = t1 + t2 + t3
    print(f"\n  OVERALL DETECTION:          {total_correct}/{total_all}  ({total_correct/total_all*100:.1f}%)")

    # Print all misses
    all_misses = m1 + m2 + m3
    if all_misses:
        print(f"\n{'=' * 72}")
        print(f"DETECTION MISSES ({len(all_misses)})")
        print("=" * 72)
        for m in all_misses:
            ec = f" [{m['edge_case']}]" if m['edge_case'] else ""
            print(f"  MISS: '{m['goal']}'{ec}")
            print(f"        detected={m['detected']!r}  expected={m['expected']!r}")
    else:
        print("\n  ✓ No detection misses!")

    return all_misses


if __name__ == "__main__":
    misses = main()
    sys.exit(1 if misses else 0)
