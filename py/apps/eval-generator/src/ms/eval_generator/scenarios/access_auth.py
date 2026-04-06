# Copyright (c) Microsoft. All rights reserved.
"""Access & Authentication category scenarios for eval dataset."""

from ms.eval_generator.scenarios._base import ScenarioDefinition
from ms.eval_generator.scenarios._base import ScenarioGold

ACCESS_AUTH_SCENARIOS: list[ScenarioDefinition] = [
    # ──────────────────────────────────────────────────────────────────
    # 1. SSO/SAML error for Salesforce
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-001",
        subjects=(
            "Can't log into Salesforce — SSO error",
            "Salesforce SAML assertion invalid",
        ),
        descriptions=(
            "Getting 'SAML assertion invalid' when trying to log into Salesforce. Worked fine yesterday. "
            "Other apps like Outlook and Teams work normally. I have a client meeting in 2 hours and need "
            "to pull up their account history.",
            "SSO login to Salesforce is broken since this morning. I keep getting redirected back to the "
            "login page with a SAML error. Cleared cookies and tried incognito — same result. Need this "
            "fixed ASAP for client work.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(
                "error_message",
                "authentication_method",
            ),
            next_best_action=(
                "Verify SAML assertion configuration for Salesforce in Entra ID and check for recent IdP "
                "certificate changes"
            ),
            remediation_steps=(
                "Check Entra ID SAML configuration for Salesforce app registration",
                "Verify IdP signing certificate has not expired or rotated",
                "Review SAML assertion logs for specific error details",
                "Test SSO flow in a separate browser session",
                "If certificate issue, update the certificate in the Salesforce SSO settings",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 2. Account lockout after vacation
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-002",
        subjects=(
            "Account locked out — just returned from vacation",
            "Can't log in after being away for 3 weeks",
        ),
        descriptions=(
            "I just came back from a 3-week vacation and my account is completely locked out. Can't log "
            "into my laptop, email, or anything. My password hasn't expired as far as I know — I changed it "
            "right before I left.",
            "Returning from PTO and I'm locked out of everything. Laptop shows 'your account has been "
            "locked' message. I need to get back to work today — have a team standup in 45 minutes.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=("error_message",),
            next_best_action="Unlock the user account in Active Directory and verify no suspicious activity caused the "
            "lockout",
            remediation_steps=(
                "Check Active Directory for lockout reason and timestamp",
                "Verify no suspicious login attempts during absence",
                "Unlock the account in AD",
                "If password expired, initiate password reset",
                "Confirm user can log in successfully",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 3. MFA authenticator app not generating codes
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-003",
        subjects=(
            "MFA not working — authenticator app blank",
            "Microsoft Authenticator stopped showing codes",
        ),
        descriptions=(
            "My Microsoft Authenticator app on my phone stopped generating verification codes this morning. "
            "When I open the app, my Contoso account is listed but no code appears. I can't log into any "
            "MFA-protected resources.",
            "Authenticator app issue — the one-time codes aren't appearing for my work account. I've tried "
            "closing and reopening the app. My personal accounts in the app still work fine, just the "
            "Contoso one is broken.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=("device_info",),
            next_best_action="Re-register the user's MFA authenticator app in Entra ID",
            remediation_steps=(
                "Verify the user's MFA registration status in Entra ID",
                "Issue a temporary access pass for immediate access",
                "Guide user to remove and re-add the Contoso account in Authenticator",
                "Re-register MFA method in the security info portal",
                "Confirm MFA codes generate correctly after re-registration",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 4. Password reset portal (SSPR) failure
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-004",
        subjects=(
            "Self-service password reset not working",
            "SSPR portal gives error when I try to reset password",
        ),
        descriptions=(
            "I'm trying to reset my password through the self-service portal but it keeps saying 'unable to "
            "verify your identity.' I set up my security questions and phone number when I started. Not "
            "sure what's wrong.",
            "The password reset portal at passwordreset.microsoftonline.com won't let me reset. It says my "
            "authentication methods aren't registered, but I definitely set them up months ago. I'm "
            "completely locked out.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=("authentication_method",),
            next_best_action="Verify SSPR registration status and manually reset the user's password",
            remediation_steps=(
                "Check user's SSPR registration status in Entra ID",
                "Verify authentication methods are properly registered",
                "Perform manual password reset via admin portal",
                "Provide temporary password to user via secure channel",
                "Guide user to re-register SSPR authentication methods",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 5. New employee provisioning delayed
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-005",
        subjects=(
            "New hire starting Monday — no accounts created yet",
            "Account provisioning for new team member",
        ),
        descriptions=(
            "I have a new hire starting this Monday and their accounts haven't been set up yet. I submitted "
            "the provisioning request in ServiceNow two weeks ago (REQ-29481). They need AD account, email, "
            "Teams, and Salesforce access for the Wealth Management team.",
            "We have a new analyst joining our team on Monday morning and their IT setup isn't ready. No "
            "laptop delivered, no accounts created. I filled out the onboarding form ages ago. This is "
            "really frustrating — their first day is going to be wasted.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(),
            next_best_action=(
                "Expedite new user provisioning and verify all required accounts and access are configured "
                "before Monday"
            ),
            remediation_steps=(
                "Locate the provisioning request REQ-29481 in ServiceNow",
                "Create AD account with appropriate group memberships",
                "Provision Microsoft 365 mailbox and Teams access",
                "Set up Salesforce access for Wealth Management team",
                "Notify the manager when provisioning is complete",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 6. Service account password expired
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-006",
        subjects=(
            "Service account expired — batch jobs failing",
            "svc_etl_prod password needs rotation",
        ),
        descriptions=(
            "The service account svc_etl_prod that runs our nightly ETL jobs has an expired password. All "
            "batch processing stopped at 2 AM. Finance team is waiting on this morning's data refresh. Can "
            "someone rotate the credentials ASAP?",
            "Our production service account for the data pipeline expired overnight. The ETL jobs haven't "
            "run since midnight. This affects the daily financial reports that the trading desk needs by 8 "
            "AM.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Rotate the service account password and update all dependent configurations",
            remediation_steps=(
                "Reset the svc_etl_prod service account password in AD",
                "Update the credential in the ETL job configuration and key vault",
                "Restart the failed batch jobs",
                "Verify ETL pipeline completes successfully",
                "Set up password expiry alerting for service accounts",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 7. Directory sync delay — new user not appearing
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-007",
        subjects=(
            "Entra Connect sync seems delayed",
            "New user account not showing in Azure AD",
        ),
        descriptions=(
            "I created a new user account in on-prem AD about 4 hours ago but it still hasn't synced to "
            "Entra ID. Normally the sync happens within 30 minutes. The new employee can't access any cloud "
            "apps.",
            "Azure AD sync appears broken. Added a user to on-prem Active Directory this morning and "
            "they're still not visible in Entra ID. Previous syncs were working fine. Other users added "
            "last week synced normally.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(
                "error_message",
                "timestamp",
            ),
            next_best_action="Check Entra Connect sync status and force a delta sync cycle",
            remediation_steps=(
                "Check Entra Connect sync status on the sync server",
                "Review sync error logs for any failures",
                "Force a delta sync cycle and monitor for completion",
                "Verify the new user appears in Entra ID after sync",
                "If sync server is unhealthy, investigate and restart the sync service",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 8. Conditional access policy blocking remote work
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-008",
        subjects=(
            "Can't access work apps from home — blocked by policy",
            "Conditional access blocking me on home network",
        ),
        descriptions=(
            "I've been working from home all week without issues but suddenly today I can't access "
            "SharePoint or Teams. Getting a 'your sign-in was blocked' error mentioning conditional access. "
            "Nothing changed on my end — same laptop, same home WiFi.",
            "Conditional access is blocking my login to Microsoft 365 from my home office. Error says my "
            "device doesn't meet compliance requirements. I'm on my company-managed laptop running Windows "
            "11. Was working fine yesterday.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(
                "device_info",
                "error_message",
            ),
            next_best_action="Review conditional access policy evaluation logs and verify device compliance status",
            remediation_steps=(
                "Check sign-in logs in Entra ID for the specific conditional access failure",
                "Verify the device compliance status in Intune",
                "Check if any conditional access policies were recently modified",
                "If device is non-compliant, identify the specific compliance check that failed",
                "Remediate the compliance issue or grant a temporary exception",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 9. OAuth token expiration for third-party API
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-009",
        subjects=(
            "API authentication failing — OAuth token expired",
            "Third-party API integration broken",
        ),
        descriptions=(
            "Our integration with the Bloomberg API stopped working this morning. The OAuth refresh token "
            "seems to have expired. Our trading dashboard depends on this feed and traders can't see "
            "real-time market data.",
            "The OAuth tokens for our Refinitiv data feed integration have expired. The service account "
            "that manages the token refresh is returning 401 errors. This is impacting the entire trading "
            "floor's market data access.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=("configuration_details",),
            next_best_action="Re-authenticate the service principal and generate new OAuth tokens for the API "
            "integration",
            remediation_steps=(
                "Identify the expired OAuth token and associated service principal",
                "Re-authenticate with the third-party API provider",
                "Generate new access and refresh tokens",
                "Update token storage in the key vault",
                "Verify the data feed integration is functioning correctly",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 10. Certificate-based authentication failure
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-010",
        subjects=(
            "Smart card login not working",
            "Certificate authentication failing on VPN",
        ),
        descriptions=(
            "My smart card login stopped working as of this morning. When I insert my PIV card, Windows "
            "says 'the certificate is not valid for the requested usage.' I need smart card auth for the "
            "secure trading terminal.",
            "Certificate-based authentication to the VPN gateway is failing. The client cert on my laptop "
            "was working until the weekend. I get a TLS handshake failure when trying to connect.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(
                "device_info",
                "error_message",
            ),
            next_best_action="Verify certificate validity and check if the issuing CA certificate chain is intact",
            remediation_steps=(
                "Check the user certificate expiration date and revocation status",
                "Verify the certificate chain and root CA trust",
                "Check if the certificate template or CA has been recently updated",
                "Re-enroll the certificate if expired or revoked",
                "Test smart card or certificate-based login after renewal",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 11. Guest/external user can't access shared resources
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-011",
        subjects=(
            "External consultant can't access our Teams channel",
            "Guest user getting access denied on SharePoint",
        ),
        descriptions=(
            "We invited an external consultant (john.doe@partnerllc.com) to our project Teams channel two "
            "days ago but they still can't access it. They get 'you don't have access to this resource' "
            "when clicking the invite link.",
            "Our auditing partner was added as a guest user to access the Q1 Audit SharePoint site, but "
            "they're unable to view any documents. They confirmed they accepted the B2B invitation email.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(
                "affected_system",
                "contact_info",
            ),
            next_best_action="Verify guest user provisioning in Entra ID and check external sharing policies",
            remediation_steps=(
                "Verify the guest account exists in Entra ID B2B",
                "Check external collaboration settings and allowed domains",
                "Verify the specific Teams channel or SharePoint site permissions",
                "Re-send the invitation if the original expired",
                "Confirm guest user can access after permission remediation",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 12. Shared mailbox access request
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-012",
        subjects=(
            "Need access to team shared mailbox",
            "Can't open shared mailbox for Client Services",
        ),
        descriptions=(
            "I recently transferred to the Client Services team and need access to the shared mailbox "
            "clientservices@contoso.com. My manager Angela Thompson has approved this. Can you add me?",
            "Requesting access to the shared mailbox 'deals@contoso.com' for the M&A advisory group. I need "
            "both send and read permissions. My manager should have submitted the approval through "
            "ServiceNow already.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P4",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Add user to the shared mailbox with requested permissions after manager approval "
            "verification",
            remediation_steps=(
                "Verify manager approval for shared mailbox access",
                "Add the user to the shared mailbox in Exchange Online with full access permissions",
                "Add send-as or send-on-behalf permissions if requested",
                "Instruct user to add the shared mailbox in Outlook",
                "Confirm the user can access the shared mailbox",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 13. Role/group membership change needed
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-013",
        subjects=(
            "Need to be added to the Risk Analytics security group",
            "AD group membership update request",
        ),
        descriptions=(
            "I've moved from the retail banking division to risk management. I need to be removed from the "
            "RetailBanking-Users group and added to RiskManagement-Analysts in AD. My new manager Raj Mehta "
            "approved this on March 10th.",
            "Please update my AD group memberships: remove me from Finance-ReadOnly and add me to "
            "Finance-PowerUsers. I was promoted to senior analyst and need write access to the financial "
            "reporting dashboards.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P4",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Update Active Directory group memberships per the approved request",
            remediation_steps=(
                "Verify manager approval for the group membership change",
                "Remove user from the old security group in AD",
                "Add user to the new security group",
                "Wait for group membership to propagate (up to 1 hour)",
                "Confirm user has appropriate access after the change",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 14. Session timeout too frequent
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-014",
        subjects=(
            "Keep getting logged out every 15 minutes",
            "Session timeout way too aggressive — can't get work done",
        ),
        descriptions=(
            "I'm constantly getting logged out of every app — Outlook, Teams, SharePoint — roughly every 15 "
            "minutes. I have to re-authenticate with MFA each time. This started after some policy change "
            "last week and it's making it impossible to do deep work.",
            "The session timeout on our internal apps is ridiculously short. I get kicked out of the risk "
            "management portal mid-analysis every 15 minutes. My colleagues on the same team don't seem to "
            "have this issue.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(
                "device_info",
                "affected_system",
            ),
            next_best_action="Review conditional access and token lifetime policies affecting the user's session "
            "duration",
            remediation_steps=(
                "Check Entra ID sign-in logs for session termination reasons",
                "Review conditional access policies and token lifetime configurations",
                "Compare user's policy assignments with unaffected colleagues",
                "Check if the user's device compliance status is causing re-authentication",
                "Adjust token lifetime policy or investigate device compliance if appropriate",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 15. SSO works for Teams but not SAP
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-015",
        subjects=(
            "SSO works for some apps but not SAP",
            "Can't sign into SAP with single sign-on",
        ),
        descriptions=(
            "Single sign-on works fine for Teams, Outlook, and SharePoint, but when I try to access SAP it "
            "asks me for a separate username/password that I don't have. I thought SSO was supposed to work "
            "for all our apps?",
            "Hi, our new SAP deployment was supposed to be integrated with Entra ID SSO but when I try to "
            "access it, I get prompted for credentials. All other enterprise apps work with SSO. Is SAP not "
            "configured yet?",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(
                "error_message",
                "application_version",
            ),
            next_best_action="Verify SAP application SSO configuration in Entra ID enterprise applications",
            remediation_steps=(
                "Check if SAP is registered as an enterprise application in Entra ID",
                "Verify SAML/OIDC SSO configuration for the SAP application",
                "Confirm the user is assigned to the SAP application in Entra ID",
                "Test SSO flow and review SAML response for errors",
                "Coordinate with SAP admin to verify SP-side SSO configuration",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 16. Azure AD/Entra ID join failure on new device
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-016",
        subjects=(
            "New laptop won't join Azure AD",
            "Entra join failing with error 0x801c03ed",
        ),
        descriptions=(
            "Trying to set up a new Surface Pro for a VP and the Entra ID join keeps failing during OOBE. "
            "Error code 0x801c03ed. I've tried three times with different network connections. We need this "
            "ready for the exec by tomorrow.",
            "Fresh Windows 11 laptop from our vendor won't complete the Azure AD join. Gets stuck at the "
            "'setting up your organization' step and eventually times out. Other laptops from the same "
            "batch joined fine.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=("device_info",),
            next_best_action="Investigate Entra ID join failure and check device registration prerequisites",
            remediation_steps=(
                "Check Entra ID device registration settings and join limits",
                "Verify the user has permission to join devices to the directory",
                "Check if the device serial number is pre-registered in Autopilot",
                "Review network connectivity to Entra ID endpoints",
                "Attempt join with a different user account or reset the device and retry",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 17. B2B collaboration — partner can't access project site
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-017",
        subjects=(
            "Partner company can't access our collaboration site",
            "B2B guest access issue with Deloitte team",
        ),
        descriptions=(
            "The Deloitte consulting team we're working with on the digital transformation project can't "
            "access our collaboration SharePoint site. We set up B2B guest invitations for 5 users last "
            "week, but they all get 'access denied.' The project kickoff is tomorrow.",
            "Our external legal counsel at Baker McKenzie needs access to the M&A deal room in SharePoint. "
            "We sent B2B invitations to 3 attorneys but they say the links expired. Can we re-invite them? "
            "The due diligence deadline is Friday.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=("contact_info",),
            next_best_action="Re-issue B2B guest invitations and verify external collaboration policies allow the "
            "partner domain",
            remediation_steps=(
                "Verify B2B external collaboration settings allow the partner domain",
                "Check if the guest invitations were accepted or expired",
                "Re-send invitations to external users",
                "Grant appropriate permissions on the SharePoint site",
                "Confirm external users can access the collaboration site",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 18. Privileged access management (PAM) request
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-018",
        subjects=(
            "Need temporary admin access for server migration",
            "PAM request for elevated privileges",
        ),
        descriptions=(
            "I need temporary elevated admin access to the Azure subscription 'contoso-prod-east' for the "
            "scheduled server migration this weekend. My manager approved it in ServiceNow (CHG-45892). "
            "Please grant contributor role scoped to the migration resource group.",
            "Requesting just-in-time admin access through our PAM system. I need Global Reader role in "
            "Entra ID for 4 hours tomorrow to complete the security audit. Approved by CISO office "
            "(CHG-46001).",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Process the approved PAM request and grant time-limited elevated access",
            remediation_steps=(
                "Verify the change request approval in ServiceNow",
                "Configure time-bound elevated role assignment in Entra PIM",
                "Set the appropriate scope and duration for the access grant",
                "Notify the user when access is activated",
                "Confirm access is automatically revoked after the specified time window",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 19. Break-glass emergency account access needed
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-019",
        subjects=(
            "URGENT: Need break-glass account — all admins locked out",
            "Emergency admin access required immediately",
        ),
        descriptions=(
            "CRITICAL: All IT admin accounts appear to be locked out after a conditional access policy "
            "change went wrong. Nobody can manage Entra ID or Azure. We need the break-glass emergency "
            "account activated immediately. This is affecting our ability to manage the entire tenant.",
            "Emergency situation — the MFA enforcement policy we deployed is blocking all admin accounts "
            "including the service desk. We need the break-glass emergency access account credentials from "
            "the safe to restore admin access. Production management capability is down.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P1",
            assigned_team="Identity & Access Management",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Activate break-glass emergency account and restore admin access "
            "to the tenant immediately",
            remediation_steps=(
                "Retrieve break-glass account credentials from physical safe",
                "Sign in with the emergency account to Entra ID portal",
                "Identify and revert the misconfigured conditional access policy",
                "Restore access for IT admin accounts",
                "Conduct post-incident review and update emergency procedures",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 20. Cross-tenant access issue after merger
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-020",
        subjects=(
            "Can't access acquired company's resources after merger",
            "Cross-tenant authentication not working",
        ),
        descriptions=(
            "Since the Northwind Traders acquisition closed last week, I still can't access their "
            "SharePoint sites or Teams channels even though IT said cross-tenant trust was configured. I "
            "need access for the integration planning meetings starting tomorrow.",
            "The cross-tenant access policies between Contoso and the newly acquired Fabrikam tenant don't "
            "seem to be working. Users from both sides are getting access denied when trying to "
            "collaborate. This is blocking the post-merger integration.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(
                "configuration_details",
                "affected_users",
            ),
            next_best_action="Review cross-tenant access settings in both Entra ID tenants and verify trust "
            "configuration",
            remediation_steps=(
                "Check cross-tenant access settings in both Entra ID tenants",
                "Verify inbound and outbound trust policies are correctly configured",
                "Confirm the external collaboration settings allow the partner tenant",
                "Test cross-tenant authentication with a specific user pair",
                "Coordinate with the acquired company's IT team to align configurations",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 21. Self-service password reset not sending SMS
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-021",
        subjects=(
            "Password reset SMS never arrives",
            "SSPR verification code not being sent to my phone",
        ),
        descriptions=(
            "I'm trying to reset my password through the self-service portal and I chose SMS verification, "
            "but the code never arrives on my phone. I've waited 10 minutes and tried 3 times. My phone "
            "number is correct in my profile.",
            "SSPR SMS codes aren't coming through. I checked — my phone number in my security info is "
            "current. I can receive regular texts fine. I've tried both the 'text me' and 'call me' "
            "options. Neither work.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(
                "device_info",
                "contact_info",
            ),
            next_best_action="Verify SSPR SMS configuration and check if the phone number is correctly registered",
            remediation_steps=(
                "Verify the user's registered phone number in Entra ID security info",
                "Check SSPR configuration for SMS delivery settings",
                "Review MFA/SSPR service health for any outages",
                "Manually reset the password and provide a temporary credential",
                "Guide user to re-register their phone number for SSPR",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 22. Kerberos authentication failure for legacy app
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-022",
        subjects=(
            "Legacy trading app Kerberos auth broken",
            "Can't authenticate to internal app — Kerberos error",
        ),
        descriptions=(
            "Our legacy internal trading application that uses Kerberos authentication stopped working "
            "after the domain controller update last night. Getting 'KRB_AP_ERR_MODIFIED' errors. This app "
            "is used by 30+ traders and there's no workaround.",
            "Kerberos authentication to the compliance reporting portal is failing. The SPN registration "
            "seems wrong. Error: 'the target principal name is incorrect.' We need this for the regulatory "
            "filing due Friday.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(
                "affected_system",
                "error_message",
            ),
            next_best_action="Verify Kerberos SPN configuration and check for issues after the recent domain "
            "controller update",
            remediation_steps=(
                "Check the SPN registration for the application service account",
                "Verify the domain controller update didn't change SPN mappings",
                "Run setspn -L to list current SPNs for the service account",
                "Re-register the SPN if incorrect or duplicate",
                "Restart the application service and verify Kerberos auth works",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 23. Account disabled unexpectedly — possible security issue
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-023",
        subjects=(
            "My account was disabled without warning",
            "Account suddenly deactivated — need investigation",
        ),
        descriptions=(
            "My account was disabled sometime overnight and I can't log into anything. I haven't given "
            "notice or done anything wrong. My manager doesn't know why either. There might be a security "
            "issue — I noticed some weird emails in my sent folder last week that I didn't send.",
            "Just arrived at work and my entire account is disabled. Badge doesn't work, laptop is locked. "
            "HR confirmed I'm not being terminated. Something is very wrong. I think someone might have "
            "compromised my account — I got a suspicious MFA prompt I didn't initiate yesterday.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=("timestamp",),
            next_best_action="Investigate potential account compromise and coordinate with SecOps "
            "for incident response",
            remediation_steps=(
                "Escalate to Security Operations for compromise investigation",
                "Review sign-in logs and audit trails for suspicious activity",
                "Check if automated security rules triggered the account disable",
                "Keep account disabled until investigation is complete",
                "If compromise confirmed, initiate full incident response procedures",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 24. Multiple failed logins from unknown location
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-024",
        subjects=(
            "ALERT: Multiple failed login attempts from Russia",
            "Suspicious login attempts on my account",
        ),
        descriptions=(
            "I just got 12 MFA push notifications in a row that I didn't initiate. The notifications are "
            "showing login attempts from an IP in Moscow. I haven't traveled. I denied all of them but I'm "
            "worried my password is compromised.",
            "Entra ID Identity Protection flagged my account with a 'high risk' sign-in from an unfamiliar "
            "location (IP: 185.xxx.xxx.xxx). I'm in the NYC office right now. Someone else is trying to "
            "access my account. Please investigate and secure it immediately.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Initiate security incident response for suspected account compromise with credential "
            "stuffing",
            remediation_steps=(
                "Block the suspicious IP addresses in conditional access",
                "Force password reset for the affected account",
                "Revoke all active sessions and refresh tokens",
                "Review sign-in and audit logs for any successful unauthorized access",
                "Enable enhanced monitoring on the account and investigate the attack vector",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 25. SSO redirect loop in Chrome
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-025",
        subjects=(
            "SSO login stuck in infinite redirect loop",
            "Chrome redirect loop when signing into portal",
        ),
        descriptions=(
            "When I try to access the internal HR portal through Chrome, I get stuck in an infinite "
            "redirect loop between the portal and the Entra ID login page. The browser eventually shows "
            "'too many redirects.' Works fine in Edge though.",
            "I'm stuck in a redirect loop when trying to SSO into ServiceNow through Chrome. URL just keeps "
            "bouncing between login.microsoftonline.com and the ServiceNow instance. Cleared cache, "
            "disabled extensions, same issue.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(
                "application_version",
                "error_message",
            ),
            next_best_action="Investigate browser-specific SSO redirect issue and check cookie/session configuration",
            remediation_steps=(
                "Clear all cookies and cached data for the affected sites in Chrome",
                "Check if third-party cookie blocking is causing the issue",
                "Verify the application's redirect URI configuration in Entra ID",
                "Test in Chrome incognito with no extensions",
                "Check if a Chrome update changed cookie handling behavior",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 26. Password expired during critical trading hours
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-026",
        subjects=(
            "URGENT: Password expired mid-trade — locked out of trading system",
            "Trading system lockout during market hours",
        ),
        descriptions=(
            "My password expired at 10:15 AM during an active trade execution. I'm completely locked out of "
            "the Bloomberg terminal and our order management system. I have open positions that need "
            "monitoring RIGHT NOW. This is a revenue-critical emergency.",
            "PASSWORD EXPIRED IN THE MIDDLE OF LIVE TRADING. I can't access the trading platform or risk "
            "management system. I have $4.2M in open FX positions that need to be managed. Someone needs to "
            "reset my password IMMEDIATELY or we face significant financial exposure.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P1",
            assigned_team="Identity & Access Management",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Immediately reset the trader's password and restore access to the trading platform",
            remediation_steps=(
                "Perform emergency password reset via admin portal",
                "Provide the new temporary password via secure phone call",
                "Confirm the trader can access the trading system",
                "Review password expiry policy for trading floor accounts",
                "Consider implementing longer password validity for trading accounts with compensating controls",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 27. Intern batch provisioning — 15 accounts needed
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-027",
        subjects=(
            "Batch account creation for summer intern cohort",
            "Need 15 intern accounts provisioned by June 1st",
        ),
        descriptions=(
            "We have 15 summer interns starting on June 1st across Engineering, Finance, and Marketing. "
            "I've attached the spreadsheet with their names, departments, and manager assignments. They "
            "each need: AD account, email, Teams, and basic Office 365 access. No VPN or Salesforce needed.",
            "Submitting a batch provisioning request for our incoming intern class. Attached is the CSV "
            "file with 15 names and departments. Standard intern access profile please — limited to email, "
            "Teams, SharePoint, and department-specific shared drives.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P4",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Process batch intern provisioning using the standard intern access template",
            remediation_steps=(
                "Review the attached intern roster spreadsheet",
                "Create AD accounts using the standard intern naming convention",
                "Assign the Intern license pack in Microsoft 365",
                "Add interns to their respective department security groups",
                "Send welcome emails with credentials to each intern's manager",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 28. Service principal secret rotation needed
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-028",
        subjects=(
            "Azure service principal secret expiring in 3 days",
            "App registration credential rotation needed",
        ),
        descriptions=(
            "The client secret for our production API app registration (app ID: 12345-abcde-67890) expires "
            "in 3 days. This powers the authentication for our customer-facing wealth management portal. We "
            "need to rotate the secret and update all consuming applications.",
            "Heads up — the Azure AD app registration 'Contoso-WealthAPI-Prod' has a client secret expiring "
            "this Friday. Need to generate a new secret, update the key vault, and coordinate deployment of "
            "the new credential across 4 microservices.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Generate a new client secret and coordinate rotation across all dependent services",
            remediation_steps=(
                "Generate a new client secret in the Entra ID app registration",
                "Store the new secret in Azure Key Vault",
                "Update all consuming applications to use the new secret",
                "Verify each service authenticates successfully with the new credential",
                "Remove the old secret after confirming all services are updated",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 29. MFA bypass request for conference room shared device
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-029",
        subjects=(
            "MFA bypass for conference room kiosk device",
            "Shared device in boardroom can't do MFA",
        ),
        descriptions=(
            "The shared Surface Hub in the main boardroom requires MFA every time someone starts a meeting, "
            "which means nobody can join a Teams meeting without their personal phone. Can we get an MFA "
            "exception for this device? It's a managed, fixed-location device.",
            "Requesting an MFA exclusion for the conference room kiosk device (asset tag CONF-BR-001). It's "
            "impractical to require MFA on a shared device that multiple people use throughout the day. "
            "This is in a physically secured, badge-access-only room.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P4",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(
                "device_info",
                "network_location",
            ),
            next_best_action="Evaluate MFA exception request and configure compliant device conditional access policy",
            remediation_steps=(
                "Review the MFA exception request against security policy",
                "Assess the physical security controls of the device location",
                "Configure a conditional access policy that excludes compliant shared devices on the corporate network",
                "Ensure the device is enrolled in Intune as a shared device",
                "Document the exception and schedule periodic security review",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 30. Federated identity provider outage
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="access-auth-030",
        subjects=(
            "Multiple users can't authenticate — possible IdP outage",
            "SSO down for everyone — federation issue",
        ),
        descriptions=(
            "Starting around 8:30 AM, we're getting reports from approximately 200+ users who can't sign "
            "into any Microsoft 365 app. They all get 'unable to contact the identity provider' errors. "
            "This appears to be a federated authentication outage affecting our ADFS servers.",
            "We have a widespread authentication outage. Our ADFS farm seems to be down — federation "
            "service is unreachable. Hundreds of users across all departments are unable to authenticate. "
            "This is impacting the entire organization's ability to work.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P1",
            assigned_team="Identity & Access Management",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Investigate ADFS farm health immediately and consider failover to cloud authentication",
            remediation_steps=(
                "Check ADFS server health and service status on all federation servers",
                "Verify network connectivity to the ADFS farm",
                "Review ADFS event logs for error details",
                "If ADFS cannot be restored quickly, enable Entra ID cloud authentication as failover",
                "Communicate status updates to all affected users through the service desk",
            ),
        ),
    ),
]
