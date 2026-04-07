# Copyright (c) Microsoft. All rights reserved.
"""Mastery-level data cleanup evaluation scenarios (dc-171 through dc-190).

These scenarios push the limits of the triage API's data-cleaning resilience
with extreme real-world noise patterns rarely covered by basic tests:
- Zalgo text (combining Unicode characters)
- Emoji-only subject lines
- Control characters and null bytes
- URL-encoded entire bodies
- Tab-delimited data dumps
- SQL query dumps
- Extremely long single-line descriptions
- Base64-encoded entire email bodies
- Deeply nested JSON config dumps
- Mixed RTL/LTR Unicode
- Corrupted PDF text extraction artifacts
- Inline SVG content
- Auto-generated repetitive content
- Phone transcripts with timestamps
- Binary/hex dumps
- Excessive punctuation and special characters
- Very long query-string URLs
- Merged multi-ticket artifacts
- Windows Event Log XML dumps
- Double-encoded UTF-8 (Mojibake chains)
"""

import base64 as _b64

from ms.evals_core.framework.models.scenario import EvalReporter
from ms.evals_core.framework.models.scenario import EvalScenario
from ms.evals_core.framework.models.scenario import EvalTicket
from ms.evals_core.framework.models.scenario import ExpectedTriage
from ms.evals_core.framework.models.scenario import ScenarioCategory
from ms.evals_core.framework.scenarios.registry import default_registry

_CATEGORY = ScenarioCategory.DATA_CLEANUP


def _reporter(name: str, email: str, department: str) -> EvalReporter:
    return EvalReporter(name=name, email=email, department=department)


# ---------------------------------------------------------------------------
# dc-171: Zalgo text — combining characters make text unreadable
# ---------------------------------------------------------------------------
_ZALGO_FRAGMENT = (
    "M\u0335\u0310\u0366\u0300y\u0336\u030f\u0312\u0360 "
    "l\u0334\u031b\u0358\u0340a\u0337\u0352\u0357\u0309"
    "p\u0335\u033e\u0313\u0368t\u0336\u0360\u033e\u0351"
    "o\u0337\u030b\u031b\u0366p\u0334\u0300\u034c\u0360"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-171",
        name="Zalgo text combining characters",
        description=(
            "Ticket description heavily corrupted with Unicode combining "
            "characters (Zalgo text), making visual rendering unreadable "
            "but with a valid software issue buried underneath."
        ),
        category=_CATEGORY,
        tags=["zalgo", "unicode_combining", "encoding_abuse"],
        ticket=EvalTicket(
            ticket_id="INC-5171",
            subject=f"O{_ZALGO_FRAGMENT}utlook cr{_ZALGO_FRAGMENT}ashing on start",
            description=(
                f"H{_ZALGO_FRAGMENT}i IT Su{_ZALGO_FRAGMENT}pport,\n\n"
                f"My Out{_ZALGO_FRAGMENT}look crashes every time I open it. "
                f"I get a Microsoft Visual C++ Runtime error dialog. "
                f"This started after the la{_ZALGO_FRAGMENT}test Windows Update "
                f"(KB5034765). I am running Outlook 365, version 16.0.17328.20162 "
                f"on Windows 11. Already tried /resetnavpane and safe mode — "
                f"same crash. The {_ZALGO_FRAGMENT} profile is 'Contoso-Main'.\n\n"
                f"Ple{_ZALGO_FRAGMENT}ase help,\n"
                f"Natasha Romanova\nDerivatives"
            ),
            reporter=_reporter("Natasha Romanova", "n.romanova@contoso.com", "Derivatives"),
            created_at="2026-03-18T08:45:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-172: Emoji-only subject line
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-172",
        name="Emoji-only subject line",
        description=(
            "Subject line consists entirely of emoji with no text. "
            "The description contains the actual access issue."
        ),
        category=_CATEGORY,
        tags=["emoji_subject", "minimal_metadata", "unicode"],
        ticket=EvalTicket(
            ticket_id="INC-5172",
            subject="🔒🚫💻😭🆘❗❗❗",
            description=(
                "I can't log in to the internal finance portal since this morning. "
                "It shows 'Your account has been locked due to too many failed "
                "attempts.' I didn't try to log in multiple times, so I think "
                "someone else was trying my account. My username is jpark-fin, "
                "and the portal URL is https://finance.internal.contoso.com. "
                "I need access urgently for the quarterly close.\n\n"
                "Jin Park\nFinance, NYC office"
            ),
            reporter=_reporter("Jin Park", "j.park@contoso.com", "Finance"),
            created_at="2026-03-18T07:15:00Z",
            channel="chat",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=True,
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-173: Control characters and null bytes in description
# ---------------------------------------------------------------------------
_CONTROL_CHARS = (
    "\x01\x02\x03\x04\x05\x06\x07\x08"
    "\x0b\x0c\x0e\x0f\x10\x11\x12\x13"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-173",
        name="Control characters and null bytes",
        description=(
            "Ticket body contains ASCII control characters from a "
            "corrupted copy-paste from a terminal session."
        ),
        category=_CATEGORY,
        tags=["control_chars", "binary_artifact", "corrupted_paste"],
        ticket=EvalTicket(
            ticket_id="INC-5173",
            subject="Network share not mapping on login",
            description=(
                f"Hi,{_CONTROL_CHARS}\n\n"
                "My network drive \\\\contoso-fs01\\shared\\trading is not "
                f"mapping automatically on login anymore.{_CONTROL_CHARS} "
                "I used to have it as Z: drive. The Group Policy should be "
                f"mapping it but{_CONTROL_CHARS} I checked gpresult /r and "
                "the drive mapping policy is listed as applied. When I try "
                f"to map it manually I get 'System error 53'{_CONTROL_CHARS} "
                "which usually means the network path was not found.\n\n"
                f"Marcus Chen{_CONTROL_CHARS}\nTrading Floor, Building 2"
            ),
            reporter=_reporter("Marcus Chen", "m.chen@contoso.com", "Trading"),
            created_at="2026-03-18T08:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-174: Entire body is URL-encoded
# ---------------------------------------------------------------------------
_URL_ENCODED_BODY = (
    "Hi%20IT%2C%0A%0AMy%20laptop%20screen%20is%20flickering%20"
    "intermittently.%20It%20happens%20every%2010-15%20minutes%20"
    "and%20lasts%20about%205%20seconds.%20The%20issue%20started%20"
    "after%20connecting%20to%20an%20external%20monitor%20yesterday.%20"
    "Dell%20Latitude%205540%2C%20Windows%2011%2C%20Intel%20Iris%20Xe%20"
    "graphics.%20Driver%20version%2031.0.101.4953.%20The%20external%20"
    "monitor%20is%20a%20Dell%20U2722D%20connected%20via%20USB-C.%20"
    "Flickering%20happens%20on%20both%20screens%20simultaneously.%0A%0A"
    "Thanks%2C%0AAisha%20Patel%0APortfolio%20Management"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-174",
        name="URL-encoded entire body",
        description=(
            "The entire ticket description is URL-encoded, as if submitted "
            "through a broken form handler that didn't decode the payload."
        ),
        category=_CATEGORY,
        tags=["url_encoded", "form_corruption", "encoding"],
        ticket=EvalTicket(
            ticket_id="INC-5174",
            subject="Screen flickering issue",
            description=_URL_ENCODED_BODY,
            reporter=_reporter("Aisha Patel", "a.patel@contoso.com", "Portfolio Management"),
            created_at="2026-03-18T10:30:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-175: Tab-delimited data dump embedded in ticket
# ---------------------------------------------------------------------------
_TAB_DUMP = "\n".join(
    f"SRV-{i:03d}\t{'CRITICAL' if i % 7 == 0 else 'WARNING' if i % 3 == 0 else 'OK'}\t"
    f"{90 + (i % 12):.1f}%\t{1024 * (i % 8)}MB\t{i * 3 + 100}ms"
    for i in range(1, 51)
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-175",
        name="Tab-delimited server monitoring data dump",
        description=(
            "Ticket body contains a 50-row tab-delimited monitoring "
            "data export with server health metrics, burying the actual "
            "request for help with a specific critical server."
        ),
        category=_CATEGORY,
        tags=["tab_delimited", "data_dump", "monitoring"],
        ticket=EvalTicket(
            ticket_id="INC-5175",
            subject="Server SRV-007 needs immediate attention",
            description=(
                "Hi team,\n\n"
                "Our monitoring dashboard is showing issues. Here's the full "
                "server health report from this morning:\n\n"
                "SERVER\tSTATUS\tCPU\tMEM_FREE\tLATENCY\n"
                + _TAB_DUMP
                + "\n\nAs you can see, SRV-007 is CRITICAL. It's our primary "
                "database replication server for the London office and it's at "
                "96.0% CPU with only 0MB free memory. Latency is 121ms which "
                "is 3x normal. Can someone check if the replication job is "
                "stuck? This is blocking end-of-day settlement processing.\n\n"
                "David Morrison\nData Platform Engineering"
            ),
            reporter=_reporter("David Morrison", "d.morrison@contoso.com", "Data Engineering"),
            created_at="2026-03-18T16:45:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Data & Storage",
            priority="P1",
            assigned_team="Data Platform",
            needs_escalation=True,
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-176: SQL query dump in ticket body
# ---------------------------------------------------------------------------
_SQL_DUMP = """
SELECT u.user_id, u.display_name, u.email, u.last_login,
       r.role_name, d.department_name, u.account_status,
       DATEDIFF(day, u.last_login, GETDATE()) AS days_inactive
FROM dbo.Users u
    LEFT JOIN dbo.UserRoles ur ON u.user_id = ur.user_id
    LEFT JOIN dbo.Roles r ON ur.role_id = r.role_id
    LEFT JOIN dbo.Departments d ON u.department_id = d.department_id
WHERE u.account_status = 'active'
    AND u.last_login < DATEADD(month, -3, GETDATE())
    AND d.department_name NOT IN ('Service Accounts', 'System')
ORDER BY u.last_login ASC;

/* Results: 847 rows returned
   user_id | display_name          | last_login  | days_inactive
   10234   | jsmith_legacy         | 2025-06-14  | 277
   10891   | trading_bot_03        | 2025-07-22  | 239
   ...
   (truncated for brevity)
*/
"""

default_registry.register(
    EvalScenario(
        scenario_id="dc-176",
        name="SQL query dump embedded in ticket",
        description=(
            "User pastes a full SQL query and partial results into the "
            "ticket body while asking for help cleaning up stale accounts."
        ),
        category=_CATEGORY,
        tags=["sql_dump", "code_paste", "data_cleanup_request"],
        ticket=EvalTicket(
            ticket_id="INC-5176",
            subject="Need help with stale account cleanup",
            description=(
                "Hi IAM team,\n\n"
                "I ran this query against our user directory to find stale accounts:\n"
                + _SQL_DUMP
                + "\nThere are 847 accounts that haven't logged in for 3+ months. "
                "Per our security policy (SEC-POL-007), accounts inactive for 90+ "
                "days should be disabled. Can you run the bulk disable process? "
                "I've attached the full CSV export. Please exclude any accounts "
                "in the 'Service Accounts' department.\n\n"
                "Regards,\nSophie Williams\nIT Security"
            ),
            reporter=_reporter("Sophie Williams", "s.williams@contoso.com", "IT Security"),
            created_at="2026-03-18T14:00:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-177: Extremely long single line (no line breaks)
# ---------------------------------------------------------------------------
_LONG_SINGLE_LINE = (
    "My printer on floor 3 next to the break room the HP LaserJet Pro M404dn with asset tag "
    "WM-PRN-0342 has been jamming constantly for the past three days and I have tried clearing "
    "the paper path and replacing the toner cartridge and checking the rollers and even doing a "
    "factory reset from the control panel but nothing works and every time I send a print job it "
    "gets about halfway through and then jams and the LCD shows error code 13.B2.D4 and I looked "
    "it up online and it said something about the fuser assembly but I am not sure if that is "
    "something I should try to fix myself or if it needs a technician and this is really urgent "
    "because we have the quarterly board meeting on Friday and I need to print about 200 pages of "
    "financial reports and there is no other color printer on this floor and the one on floor 2 "
    "requires a different driver that IT hasn't installed on my machine yet and I tried to install "
    "it myself but I don't have admin rights and my manager Raj Krishnamurthy said I should contact "
    "IT support directly because he already submitted a ticket last week about the same printer but "
    "hasn't heard back which is ticket number INC-4897 if you want to reference it "
) * 3  # Repeat to make it excessively long

default_registry.register(
    EvalScenario(
        scenario_id="dc-177",
        name="Extremely long single line with no breaks",
        description=(
            "Ticket description is one continuous line (~3000 characters) "
            "with no line breaks, paragraphs, or formatting."
        ),
        category=_CATEGORY,
        tags=["no_linebreaks", "wall_of_text", "stream_of_consciousness"],
        ticket=EvalTicket(
            ticket_id="INC-5177",
            subject="Printer keeps jamming",
            description=_LONG_SINGLE_LINE.strip(),
            reporter=_reporter("Elena Vasquez", "e.vasquez@contoso.com", "Finance"),
            created_at="2026-03-18T11:20:00Z",
            channel="chat",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-178: Base64-encoded entire email body
# ---------------------------------------------------------------------------

_PLAIN_BODY = (
    "Hi IT Support,\n\n"
    "I'm unable to access the SharePoint site for the M&A deal room "
    "(https://contoso.sharepoint.com/sites/MA-Project-Atlas). I get a "
    "'403 Forbidden' error. I was added to the project last week by "
    "Lisa from Legal, and I could access it fine until yesterday. "
    "My permissions haven't changed as far as I know. I need access "
    "restored ASAP — we have a filing deadline on Thursday.\n\n"
    "Tom Henderson\nCorporate Strategy\nBuilding 1, Floor 7"
)
_BASE64_BODY = _b64.b64encode(_PLAIN_BODY.encode()).decode()

default_registry.register(
    EvalScenario(
        scenario_id="dc-178",
        name="Base64-encoded entire email body",
        description=(
            "Entire ticket body is base64-encoded, as if the email "
            "gateway failed to decode a MIME transfer-encoding."
        ),
        category=_CATEGORY,
        tags=["base64_full_body", "mime_encoding", "transfer_encoding"],
        ticket=EvalTicket(
            ticket_id="INC-5178",
            subject="SharePoint access issue - URGENT",
            description=(
                "Content-Transfer-Encoding: base64\n"
                "Content-Type: text/plain; charset=UTF-8\n\n"
                + _BASE64_BODY
            ),
            reporter=_reporter("Tom Henderson", "t.henderson@contoso.com", "Corporate Strategy"),
            created_at="2026-03-18T09:15:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-179: Deeply nested JSON config dump
# ---------------------------------------------------------------------------
_NESTED_JSON = """{
  "cluster": {
    "name": "prod-east-01",
    "config": {
      "networking": {
        "ingress": {
          "controller": {
            "replicas": 3,
            "resources": {
              "limits": {
                "cpu": "2000m",
                "memory": "4Gi"
              },
              "requests": {
                "cpu": "500m",
                "memory": "1Gi"
              }
            },
            "annotations": {
              "service.beta.kubernetes.io/azure-load-balancer-internal": "true",
              "service.beta.kubernetes.io/azure-load-balancer-internal-subnet": "aks-subnet-01"
            }
          },
          "tls": {
            "enabled": true,
            "secretName": "contoso-wildcard-tls",
            "certificateAuthority": {
              "issuer": {
                "name": "letsencrypt-prod",
                "kind": "ClusterIssuer",
                "config": {
                  "acme": {
                    "server": "https://acme-v02.api.letsencrypt.org/directory",
                    "email": "platform@contoso.com"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}"""

default_registry.register(
    EvalScenario(
        scenario_id="dc-179",
        name="Deeply nested JSON config dump",
        description=(
            "Ticket body contains a deeply nested JSON Kubernetes config "
            "dump (~10 levels deep) that buries the actual issue."
        ),
        category=_CATEGORY,
        tags=["nested_json", "config_dump", "kubernetes"],
        ticket=EvalTicket(
            ticket_id="INC-5179",
            subject="AKS ingress controller not routing traffic after config change",
            description=(
                "Hi team,\n\n"
                "After applying the following config update to our AKS cluster, "
                "the ingress controller stopped routing traffic to the backend "
                "pods. All HTTP requests return 502 Bad Gateway. This is affecting "
                "our production API that the trading desk depends on.\n\n"
                "Current config:\n"
                + _NESTED_JSON
                + "\n\nI think the issue might be with the subnet annotation — "
                "we moved to aks-subnet-02 last week but this config still "
                "references aks-subnet-01. The cert rotation also happened "
                "yesterday so it could be a TLS issue too.\n\n"
                "Ryan Kowalski\nCloud Infrastructure\n"
                "Cluster: prod-east-01, Resource Group: rg-aks-production"
            ),
            reporter=_reporter("Ryan Kowalski", "r.kowalski@contoso.com", "Cloud Infrastructure"),
            created_at="2026-03-18T06:30:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-180: Mixed RTL/LTR Unicode (Hebrew + English)
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-180",
        name="Mixed RTL/LTR Unicode text",
        description=(
            "Ticket contains both Hebrew (RTL) and English (LTR) text, "
            "creating bidirectional layout issues in the ticket body."
        ),
        category=_CATEGORY,
        tags=["bidi", "rtl_ltr_mix", "hebrew", "unicode"],
        ticket=EvalTicket(
            ticket_id="INC-5180",
            subject="VPN connection issue — \u05d1\u05e2\u05d9\u05d4 \u05d1\u05d7\u05d9\u05d1\u05d5\u05e8 VPN",
            description=(
                "שלום צוות IT,\n\n"
                "יש לי בעיה בחיבור ל-VPN מהמשרד בתל אביב. "
                "I am trying to connect to the GlobalProtect VPN gateway "
                "vpn-eu.contoso.com but I keep getting error GP-0011 "
                "(\"Gateway not reachable\"). "
                "הבעיה התחילה אחרי שדרוג הרשת אתמול. "
                "My colleague next to me can connect fine. "
                "אני משתמש ב-Windows 11 עם GlobalProtect 6.2.1. "
                "The local network works fine — I can access internal sites "
                "over the LAN. Only VPN is broken.\n\n"
                "תודה,\nDaniel Levy\nInstitutional Trading, Tel Aviv office"
            ),
            reporter=_reporter("Daniel Levy", "d.levy@contoso.com", "Institutional Trading"),
            created_at="2026-03-18T07:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-181: Corrupted PDF text extraction artifacts
# ---------------------------------------------------------------------------
_PDF_GARBLE = (
    "Th(cid:3)s (cid:2)s a pr(cid:2)nt(cid:3)r (cid:2)ssu(cid:3). "
    "Th(cid:3) HP Las(cid:3)rJ(cid:3)t on Floor 5 (cid:2)s pr(cid:2)nt(cid:2)ng "
    "garbl(cid:3)d t(cid:3)xt. (cid:1)(cid:1)(cid:1) "
    "S(cid:2)nc(cid:3) Monday, all docum(cid:3)nts pr(cid:2)nt(cid:3)d from "
    "th(cid:2)s pr(cid:2)nt(cid:3)r hav(cid:3) m(cid:2)ss(cid:2)ng charact(cid:3)rs "
    "and (cid:2) symbols (cid:2)nst(cid:3)ad of normal l(cid:3)tt(cid:3)rs."
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-181",
        name="Corrupted PDF text extraction artifacts",
        description=(
            "Ticket was submitted by extracting text from a scanned PDF, "
            "resulting in CID-reference artifacts throughout the body."
        ),
        category=_CATEGORY,
        tags=["pdf_extraction", "ocr_artifacts", "cid_references"],
        ticket=EvalTicket(
            ticket_id="INC-5181",
            subject="Printer outputting garbled text",
            description=(
                "Original ticket from PDF scan:\n\n"
                + _PDF_GARBLE
                + "\n\n"
                "Additional context from phone follow-up: The user reports "
                "that the HP LaserJet Pro on Floor 5, Building 3 is printing "
                "documents with missing or substituted characters. Started "
                "Monday morning. Other printers on the same floor work fine. "
                "Asset tag: WM-PRN-0518. PCL driver version 6.9.0.\n\n"
                "Transcribed by: Amy Rodriguez, Help Desk"
            ),
            reporter=_reporter("Carlos Mendez", "c.mendez@contoso.com", "Operations"),
            created_at="2026-03-18T10:45:00Z",
            channel="phone",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-182: Inline SVG content in email
# ---------------------------------------------------------------------------
_SVG_CONTENT = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400">'
    '<rect width="100%" height="100%" fill="#f0f0f0"/>'
    '<text x="50%" y="30%" text-anchor="middle" font-size="24">'
    "CPU Usage Over Time</text>"
    '<line x1="50" y1="350" x2="750" y2="350" stroke="#000" stroke-width="2"/>'
    '<line x1="50" y1="50" x2="50" y2="350" stroke="#000" stroke-width="2"/>'
    + "".join(
        f'<circle cx="{50 + i * 14}" cy="{350 - (i * 3 + 20) * 3}" r="3" fill="red"/>'
        for i in range(50)
    )
    + "</svg>"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-182",
        name="Inline SVG chart content",
        description=(
            "Ticket body contains a full inline SVG chart that was "
            "pasted from a monitoring dashboard. The SVG markup is "
            "interleaved with the actual problem description."
        ),
        category=_CATEGORY,
        tags=["svg_inline", "html_content", "chart_data"],
        ticket=EvalTicket(
            ticket_id="INC-5182",
            subject="Production server CPU spike — see attached chart",
            description=(
                "Hi team,\n\n"
                "We're seeing sustained high CPU on SQLSRV-PROD-01. "
                "Here is the chart from our monitoring:\n\n"
                + _SVG_CONTENT
                + "\n\n"
                "As shown above, CPU has been climbing steadily since 4 AM "
                "and is now at ~95%. The SQL Server instance is running our "
                "core trading platform database. Query Store shows a new "
                "plan regression on the GetActivePositions procedure. "
                "This is impacting trade execution latency — we need someone "
                "to investigate immediately.\n\n"
                "Priya Sharma\nData Platform Engineering"
            ),
            reporter=_reporter("Priya Sharma", "p.sharma@contoso.com", "Data Engineering"),
            created_at="2026-03-18T05:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Data & Storage",
            priority="P1",
            assigned_team="Data Platform",
            needs_escalation=True,
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-183: Auto-generated repetitive monitoring alerts
# ---------------------------------------------------------------------------
_ALERT_BLOCK = "\n".join(
    f"[ALERT {i:04d}] {['WARNING', 'CRITICAL', 'INFO'][i % 3]}: "
    f"Service 'contoso-api-gateway' health check failed at "
    f"2026-03-18T{6 + i // 60:02d}:{i % 60:02d}:00Z — "
    f"HTTP 503 Service Unavailable (attempt {(i % 5) + 1}/5)"
    for i in range(100)
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-183",
        name="Auto-generated repetitive monitoring alerts",
        description=(
            "Ticket body is a dump of 100 auto-generated monitoring "
            "alert lines, all saying roughly the same thing. The user's "
            "actual request is in the first and last few lines."
        ),
        category=_CATEGORY,
        tags=["alert_flood", "monitoring_dump", "repetitive"],
        ticket=EvalTicket(
            ticket_id="INC-5183",
            subject="FW: [PagerDuty] API Gateway health check failures (100+ alerts)",
            description=(
                "Hi, this was auto-forwarded from PagerDuty. Our API gateway "
                "has been failing health checks since 6 AM. Here are all the "
                "alerts:\n\n"
                + _ALERT_BLOCK
                + "\n\nCan someone please look into why the API gateway is "
                "returning 503s? The backend services seem to be running "
                "fine — I can hit them directly. I think it might be the "
                "load balancer health probe configuration that was changed "
                "in yesterday's maintenance window.\n\n"
                "Ben Okafor\nBackend Engineering"
            ),
            reporter=_reporter("Ben Okafor", "b.okafor@contoso.com", "Backend Engineering"),
            created_at="2026-03-18T07:30:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-184: Phone transcript with timestamps
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-184",
        name="Phone transcript with timestamps",
        description=(
            "Ticket is a raw phone call transcript with speaker labels "
            "and timestamps, making it hard to extract the actual issue."
        ),
        category=_CATEGORY,
        tags=["phone_transcript", "timestamps", "speaker_labels"],
        ticket=EvalTicket(
            ticket_id="INC-5184",
            subject="Phone call transcript — user reporting software issue",
            description=(
                "[Call Start: 2026-03-18 09:14:22 EST]\n"
                "[00:00] AGENT (Amy): Thank you for calling Contoso IT support. "
                "How can I help you today?\n"
                "[00:05] CALLER (Robert): Hi, yeah, so, um, I've been having "
                "this issue with, uh, Excel. It keeps crashing.\n"
                "[00:12] AGENT: I'm sorry to hear that. Can you tell me which "
                "version of Excel you're using?\n"
                "[00:17] CALLER: Um, let me check... [typing sounds] It says "
                "Microsoft 365, version... 2402, build 17328.20162.\n"
                "[00:28] AGENT: And when does it crash? Is it when you open "
                "a specific file?\n"
                "[00:33] CALLER: Yeah, it's this one spreadsheet. It's our "
                "end-of-quarter financial model. It's about 85 megabytes with "
                "a ton of VLOOKUP formulas and pivot tables. Used to work fine "
                "until the update last Tuesday.\n"
                "[00:48] AGENT: Does it give you an error message?\n"
                "[00:51] CALLER: [pause] Yes, it says something like... "
                "'Excel has stopped working. A problem caused the program to "
                "stop working correctly. Windows will close the program and "
                "notify you if a solution is available.' And then it just closes.\n"
                "[01:05] AGENT: Have you tried opening it in safe mode?\n"
                "[01:08] CALLER: No, how do I do that?\n"
                "[01:10] AGENT: Hold Ctrl while opening Excel. But let me "
                "create a ticket for this. Your name?\n"
                "[01:15] CALLER: Robert Kim, Wealth Management.\n"
                "[01:18] AGENT: And your employee ID?\n"
                "[01:20] CALLER: E-72845.\n"
                "[01:22] AGENT: Thank you, Robert. I'm creating ticket INC-5184.\n"
                "[Call End: 2026-03-18 09:16:02 EST]"
            ),
            reporter=_reporter("Robert Kim", "r.kim@contoso.com", "Wealth Management"),
            created_at="2026-03-18T09:16:00Z",
            channel="phone",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-185: Binary/hex dump in description
# ---------------------------------------------------------------------------
_HEX_DUMP = "\n".join(
    f"0x{i * 16:08x}  " + " ".join(f"{(i * 16 + j) % 256:02x}" for j in range(16)) + "  "
    + "".join(chr((i * 16 + j) % 94 + 33) for j in range(16))
    for i in range(30)
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-185",
        name="Binary/hex dump pasted in description",
        description=(
            "User pasted a hex dump from a memory debugger into the "
            "ticket body while reporting an application crash."
        ),
        category=_CATEGORY,
        tags=["hex_dump", "binary_data", "debug_output"],
        ticket=EvalTicket(
            ticket_id="INC-5185",
            subject="Application crash with memory dump",
            description=(
                "Our custom trading application (ContosoTrader v4.2.1) is "
                "crashing with an access violation. Here is the memory dump "
                "from WinDbg at the crash point:\n\n"
                + _HEX_DUMP
                + "\n\n"
                "The crash happens when loading the options pricing module. "
                "Stack trace points to ntdll!RtlAllocateHeap. Looks like a "
                "heap corruption issue. This affects 12 traders on the "
                "derivatives desk — they can't run the options pricer.\n\n"
                "Kenji Yamamoto\nQuantitative Analysis"
            ),
            reporter=_reporter("Kenji Yamamoto", "k.yamamoto@contoso.com", "Quantitative Analysis"),
            created_at="2026-03-18T13:30:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-186: Excessive punctuation and special characters
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-186",
        name="Excessive punctuation and special characters",
        description=(
            "User emphasizes frustration with excessive punctuation, "
            "special characters, and decorative Unicode symbols."
        ),
        category=_CATEGORY,
        tags=["excessive_punctuation", "special_chars", "emphasis_abuse"],
        ticket=EvalTicket(
            ticket_id="INC-5186",
            subject="!!! *** URGENT *** !!! WiFi NOT WORKING !!! ★★★ HELP ★★★ !!!",
            description=(
                "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
                "★★★★★★★★★ EXTREMELY URGENT ★★★★★★★★★\n"
                "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
                "THE WIFI ON THE ENTIRE 4TH FLOOR IS DOWN!!!!!!!\n"
                ">>> BUILDING 2, NEW YORK OFFICE <<<\n\n"
                "◆◆◆ Details ◆◆◆\n"
                "- All 50+ people on Floor 4 have no WiFi since 8 AM\n"
                "- Access points show solid red light (not blinking)\n"
                "- AP names: CONTOSO-AP-4F-01 through CONTOSO-AP-4F-08\n"
                "- Ethernet still works for people with docks\n"
                "- We have client meetings starting at 10 AM!!!!!!\n\n"
                "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                "★★★ THIS IS BLOCKING THE ENTIRE FLOOR ★★★\n"
                "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n"
                "—— Submitted by: Lisa Thompson, Wealth Management ——"
            ),
            reporter=_reporter("Lisa Thompson", "l.thompson@contoso.com", "Wealth Management"),
            created_at="2026-03-18T08:15:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-187: Very long URL with query parameters
# ---------------------------------------------------------------------------
_LONG_URL = (
    "https://sso.contoso.com/oauth2/authorize?"
    "client_id=4a7b8c9d-1e2f-3a4b-5c6d-7e8f9a0b1c2d&"
    "redirect_uri=https%3A%2F%2Fapp.contoso.com%2Fauth%2Fcallback&"
    "response_type=code&"
    "scope=openid%20profile%20email%20offline_access%20api%3A%2F%2Fcontoso-api%2F.default&"
    "state=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZWRpcmVjdCI6Ii9kYXNoYm9hcmQiLCJ"
    "ub25jZSI6ImFiYzEyMyIsInRpbWVzdGFtcCI6MTcxMTAwMDAwMH0.placeholder_signature_value&"
    "nonce=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz&"
    "code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM&"
    "code_challenge_method=S256&"
    "prompt=login&"
    "login_hint=m.oconnor%40contoso.com&"
    "domain_hint=contoso.com"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-187",
        name="Very long OAuth URL with query parameters",
        description=(
            "User pastes an extremely long OAuth authorization URL "
            "containing JWT tokens and PKCE parameters as the main "
            "content of their error description."
        ),
        category=_CATEGORY,
        tags=["long_url", "oauth_url", "query_params"],
        ticket=EvalTicket(
            ticket_id="INC-5187",
            subject="SSO login redirect loop",
            description=(
                "I'm stuck in an infinite redirect loop when trying to log in "
                "to the Contoso dashboard app. The browser address bar shows "
                "this URL before it redirects again:\n\n"
                + _LONG_URL
                + "\n\nAfter about 5 redirects it gives me an ERR_TOO_MANY_REDIRECTS "
                "error. I've cleared cookies and tried incognito mode — same issue. "
                "This started today. Chrome 123.0.6312.86, Windows 11.\n\n"
                "Michael O'Connor\nFrontend Engineering"
            ),
            reporter=_reporter("Michael O'Connor", "m.oconnor@contoso.com", "Frontend Engineering"),
            created_at="2026-03-18T09:30:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-188: Merged multi-ticket artifact
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-188",
        name="Merged multi-ticket artifact",
        description=(
            "Two unrelated tickets were accidentally merged by the "
            "ticketing system, creating a confusing combined body. "
            "The system should triage based on the higher-priority issue."
        ),
        category=_CATEGORY,
        tags=["merged_tickets", "multi_issue", "system_artifact"],
        ticket=EvalTicket(
            ticket_id="INC-5188",
            subject="[MERGED] INC-5188a + INC-5188b — Multiple issues reported",
            description=(
                "=== TICKET INC-5188a (Original) ===\n"
                "Reporter: Alice Wong (a.wong@contoso.com)\n"
                "Department: Compliance\n"
                "Date: 2026-03-18 08:30:00 UTC\n\n"
                "Our compliance monitoring system (ComplianceGuard v3.1) is "
                "showing a critical alert: 47 trade records from yesterday "
                "failed to sync to the audit database. Error in the sync log: "
                "'FK_CONSTRAINT_VIOLATION: trade_counterparty_id references "
                "non-existent counterparty record.' This is a SOX compliance "
                "issue — we need those records in the audit trail within 24 hours.\n\n"
                "=== MERGED WITH TICKET INC-5188b ===\n"
                "Reporter: Bob Martinez (b.martinez@contoso.com)\n"
                "Department: Facilities\n"
                "Date: 2026-03-18 09:15:00 UTC\n\n"
                "The badge reader on the 3rd floor south entrance (Building 1) "
                "has stopped working. Employees have been propping the door open "
                "which is a security concern. The reader model is HID iCLASS "
                "SE R10. The LED is solid red instead of green.\n\n"
                "=== END MERGED TICKETS ==="
            ),
            reporter=_reporter("Alice Wong", "a.wong@contoso.com", "Compliance"),
            created_at="2026-03-18T09:20:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-189: Windows Event Log XML dump
# ---------------------------------------------------------------------------
_EVENTLOG_XML = "\n".join(
    f'<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">'
    f"<System><EventID>{1000 + i}</EventID>"
    f"<Level>{[1, 2, 3, 4][i % 4]}</Level>"
    f'<TimeCreated SystemTime="2026-03-18T{8 + i // 6:02d}:{(i * 10) % 60:02d}:00.000Z"/>'
    f"<Source Name=\"{'Application Error' if i % 3 == 0 else 'Microsoft-Windows-Security-Auditing'}\"/>"
    f"</System><EventData><Data>Process: outlook.exe, PID: {4000 + i * 7}</Data>"
    f"<Data>Exception code: 0x{0xC0000005 + i:08x}</Data></EventData></Event>"
    for i in range(20)
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-189",
        name="Windows Event Log XML dump",
        description=(
            "Ticket body contains 20 Windows Event Log entries in raw "
            "XML format, dumped from Event Viewer."
        ),
        category=_CATEGORY,
        tags=["event_log", "xml_dump", "windows"],
        ticket=EvalTicket(
            ticket_id="INC-5189",
            subject="Outlook keeps crashing — event log attached",
            description=(
                "Outlook is crashing multiple times per day. Here are the "
                "relevant events from Windows Event Viewer:\n\n"
                + _EVENTLOG_XML
                + "\n\nThe crashes seem to happen when I switch between "
                "calendar and email views. Running Outlook 365 on Windows 11, "
                "machine name WS-NYC-7845. This has been going on for a week.\n\n"
                "Grace Li\nInvestor Relations"
            ),
            reporter=_reporter("Grace Li", "g.li@contoso.com", "Investor Relations"),
            created_at="2026-03-18T11:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
        ),
    )
)

# ---------------------------------------------------------------------------
# dc-190: Double-encoded UTF-8 (Mojibake chain)
# ---------------------------------------------------------------------------
_MOJIBAKE = (
    "Iâ\x80\x99m having trouble with my laptopâ\x80\x99s Wi-Fi. "
    "It keeps disconnecting and the signal strength shows â\x80\x9cpoorâ\x80\x9d "
    "even though Iâ\x80\x99m sitting right next to the access point. "
    "The error message says â\x80\x9cLimited connectivityâ\x80\x9d and "
    "the network adapter is an Intel Wi-Fi 6E AX211. "
    "Iâ\x80\x99ve tried updating the driver from Intelâ\x80\x99s website "
    "but it didnâ\x80\x99t help. My colleague Angela doesnâ\x80\x99t have "
    "this issue on the same floor."
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-190",
        name="Double-encoded UTF-8 (Mojibake)",
        description=(
            "Ticket was saved in Latin-1 encoding but contains UTF-8 "
            "smart quotes, producing classic Mojibake artifacts "
            "(â€™ instead of ', â€œ instead of \")."
        ),
        category=_CATEGORY,
        tags=["mojibake", "double_encoding", "utf8_latin1"],
        ticket=EvalTicket(
            ticket_id="INC-5190",
            subject="Wi-Fi disconnecting â\x80\x93 limited connectivity",
            description=(
                "Hi IT support,\n\n"
                + _MOJIBAKE
                + "\n\nIâ\x80\x99m on Floor 3, Building 2, London office. "
                "Machine: Dell Latitude 7440, Windows 11 23H2.\n\n"
                "Thanks,\nOliver Jenkins\nFixed Income"
            ),
            reporter=_reporter("Oliver Jenkins", "o.jenkins@contoso.com", "Fixed Income"),
            created_at="2026-03-18T12:15:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
        ),
    )
)
