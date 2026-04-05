"""Access & Authentication scenario definitions."""

from generator.models import Scenario

SCENARIOS: list[Scenario] = [
    Scenario(
        scenario_id="auth-password-expired",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["authentication_method"],
        subjects=[
            "Password expired — can't log in",
            "Account says password expired, locked out",
            "Need to reset my expired password",
            "Password reset needed — expired",
        ],
        descriptions=[
            "My password expired this morning and I can't log into my workstation. I've tried the self-service reset "
            "portal but it keeps saying 'service unavailable'. Can someone reset it manually? I have a client meeting "
            "in 2 hours.",
            "Tried to log in this morning and got a message that my password has expired. The SSPR portal doesn't seem "
            "to be working for me. I need access ASAP to finish a quarterly report.",
            "Password expiration notice popped up but I couldn't change it in time. Now locked out completely. "
            "Self-service portal gives a generic error.",
        ],
        next_best_actions=[
            "Verify user identity and initiate manual password reset. Check SSPR portal status for widespread issues.",
            "Reset user password via admin console and investigate SSPR portal availability.",
        ],
        remediation_steps=[
            [
                "Verify user identity via security questions or manager confirmation",
                "Perform manual password reset via Active Directory admin console",
                "Provide temporary password and instruct user to change at next login",
                "Investigate SSPR portal availability for potential widespread issues",
                "Follow up to confirm user can log in successfully",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-mfa-not-arriving",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["device_info", "authentication_method"],
        subjects=[
            "MFA push notification not coming through",
            "Not getting MFA codes on my phone",
            "Authenticator app stopped sending push notifications",
            "MFA verification failing — no push received",
        ],
        descriptions=[
            "Since this morning I haven't been able to receive MFA push notifications on my phone. I'm using Microsoft "
            "Authenticator on an iPhone 15. I've tried restarting the app and my phone but nothing works.",
            "My MFA push notifications stopped working today. The Authenticator app shows the account but tapping "
            "'approve' doesn't do anything. I can't get into email or Teams.",
            "Authenticator app on my Android phone isn't sending push notifications anymore. Was fine yesterday. I'm "
            "completely locked out of all Microsoft 365 services.",
        ],
        next_best_actions=[
            "Issue temporary access pass and troubleshoot MFA registration. Check for Authenticator service issues.",
            "Provide alternative MFA method (SMS/phone call) and re-register Authenticator app.",
        ],
        remediation_steps=[
            [
                "Issue a Temporary Access Pass (TAP) to restore immediate access",
                "Verify phone has internet connectivity and Authenticator app is updated",
                "Remove and re-add the MFA registration for the user account",
                "Test push notification delivery after re-registration",
                "If push still fails, configure SMS or phone call as backup MFA method",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-mfa-lost-phone",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=True,
        missing_information=["device_info"],
        subjects=[
            "Lost my phone — locked out of everything (MFA)",
            "Phone stolen, can't do MFA, completely locked out",
            "MFA locked out — lost phone, need emergency access",
            "Lost device with MFA — can't access any systems",
        ],
        descriptions=[
            "I lost my phone on the subway this morning and it had my Microsoft Authenticator app on it. I can't log in"
            "to anything now — email, Teams, VPN, nothing. I have a critical client presentation at 2 PM. Please help u"
            "rgently.",
            "My phone was stolen yesterday evening. It has my Authenticator app and I'm completely locked out of all "
            "company systems. I need emergency access set up on a new device.",
            "Left my phone in a taxi. Now I can't pass MFA for any login. I don't have backup codes. This is my only "
            "auth method. I need access restored immediately — I'm in the middle of quarter-end close.",
        ],
        next_best_actions=[
            "Issue Temporary Access Pass immediately. Revoke MFA on lost device and register new MFA method. If phone "
            "stolen, initiate remote wipe.",
            "Provide emergency access via TAP, revoke compromised device MFA registration, and set up replacement "
            "authentication method.",
        ],
        remediation_steps=[
            [
                "Verify user identity via manager or in-person at IT help desk",
                "Issue Temporary Access Pass for immediate system access",
                "Revoke all MFA sessions and registrations on the lost device",
                "If device was stolen, initiate remote wipe via Intune",
                "Register new MFA method on replacement device",
                "Confirm all services accessible with new MFA setup",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-sso-broken",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["error_message", "application_version"],
        subjects=[
            "SSO not working for Salesforce after password change",
            "Single sign-on broken — can't access Salesforce",
            "Salesforce SSO keeps asking me to re-authenticate",
            "SSO token error after password reset",
        ],
        descriptions=[
            "I changed my password yesterday per the quarterly reset policy. Now SSO into Salesforce is completely brok"
            "en. I get an 'invalid token' error every time. I've cleared cookies and tried incognito mode. I have a cri"
            "tical client demo scheduled for tomorrow.",
            "After my password change, Salesforce SSO stopped working. I get redirected in a loop between the login "
            "page and Salesforce. All other SSO apps work fine — just Salesforce is broken.",
            "Salesforce SSO has been failing since my password reset. Error says 'SAML assertion invalid'. Other apps "
            "using SSO work fine. Need access restored — I manage all our client accounts there.",
        ],
        next_best_actions=[
            "Investigate SSO token cache and SAML assertion for Salesforce integration. Clear cached SSO tokens for the"
            " user.",
            "Check Azure AD enterprise app configuration for Salesforce and refresh SAML token mappings.",
        ],
        remediation_steps=[
            [
                "Clear cached SSO tokens for the user in Azure AD",
                "Verify SAML assertion configuration for Salesforce enterprise app",
                "Check if password change triggered token refresh correctly",
                "Test SSO flow in private browser to rule out cached credentials",
                "If issue persists, re-provision user SSO assignment in Azure AD",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-badge-denied",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["network_location"],
        subjects=[
            "Badge not working at Building 7 entrance",
            "Access badge denied — can't get into the office",
            "Security badge doesn't open the door anymore",
            "Badge reader keeps saying 'access denied'",
        ],
        descriptions=[
            "My badge stopped working at the Building 7 main entrance this morning. I've used this entrance every day f"
            "or 2 years. The security guard let me in but I need this fixed — I work on the 3rd floor secure area too.",
            "I tried to tap my badge at the Building 7 entrance and got 'Access Denied'. Other people's badges work "
            "fine. This started today — no changes to my role or office location.",
            "My physical access badge is being rejected at Building 7. I haven't had any role changes. The badge works "
            "at the parking garage but not the building entrance.",
        ],
        next_best_actions=[
            "Check physical access control system for badge status. Verify no changes to building access groups or "
            "badge expiration.",
            "Investigate access group assignment for Building 7 and check badge reader logs.",
        ],
        remediation_steps=[
            [
                "Check badge status in physical access control system (active/expired/revoked)",
                "Verify user's building access group assignments",
                "Check for recent changes to Building 7 access policies",
                "If badge is expired, issue replacement or extend validity",
                "Test badge at the problematic entrance after fix",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-new-hire-no-account",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["affected_system", "contact_info"],
        subjects=[
            "New hire starting Monday — no account provisioned yet",
            "New employee has no IT account — starts tomorrow",
            "Account setup for new hire not done",
            "New joiner cannot log in — Day 1 issue",
        ],
        descriptions=[
            "We have a new hire, Jennifer Park, starting this Monday on the Wealth Management team. HR submitted the on"
            "boarding request two weeks ago but she still has no AD account, email, or laptop assignment. Her manager i"
            "s asking daily about this.",
            "I'm a new employee who started today but there's no account for me in the system. My manager said IT was "
            "supposed to set everything up. I've been sitting here for 3 hours with nothing to do. ID: EMP-78432.",
            "New team member was supposed to start today with full access provisioned. No email, no AD account, no "
            "badge. Onboarding ticket was raised 3 weeks ago. The hiring manager is escalating.",
        ],
        next_best_actions=[
            "Check onboarding request status in HR system. Expedite account provisioning for AD, email, and system "
            "access.",
            "Investigate delayed onboarding workflow and provision all required accounts immediately.",
        ],
        remediation_steps=[
            [
                "Check HR onboarding request status and identify the provisioning bottleneck",
                "Create Active Directory account with appropriate group memberships",
                "Provision Microsoft 365 mailbox and Teams access",
                "Assign appropriate software licenses (Office, Salesforce, etc.)",
                "Coordinate laptop assignment from Endpoint Engineering",
                "Set up physical badge access for the new hire's building and floor",
                "Confirm all access is working and send welcome credentials securely",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-service-account-expiring",
        category="Access & Authentication",
        priority="P1",
        assigned_team="Identity & Access Management",
        needs_escalation=True,
        missing_information=["affected_system", "configuration_details"],
        subjects=[
            "Service account password expiring in 48 hours — production systems at risk",
            "URGENT: Service account for payment processing expires tomorrow",
            "Critical service account credentials expiring — need rotation",
            "Production service account SVC-PAY-001 password expiry imminent",
        ],
        descriptions=[
            "The service account SVC-PAY-001 that our payment processing system uses has a password expiring in 48 "
            "hours. This account handles all client wire transfers. If it expires, the entire payment pipeline stops. "
            "We need coordinated password rotation across 5 dependent systems.",
            "Got an alert that the service account for our core trading platform (SVC-TRADE-MAIN) expires in 2 days. "
            "Last time this happened, we had a 4-hour outage. Requesting urgent password rotation coordination.",
            "Our monitoring detected that service account SVC-RISK-ENGINE will expire in 48 hours. This account is used"
            " by our real-time risk calculation engine. Failure would mean we can't process any trades. Need immediate "
            "attention.",
        ],
        next_best_actions=[
            "Initiate coordinated service account password rotation. Identify all dependent systems and schedule "
            "maintenance window.",
            "Plan coordinated password rotation with change management. Update all dependent system configurations.",
        ],
        remediation_steps=[
            [
                "Identify all systems and services that depend on the service account",
                "Schedule a maintenance window for coordinated password rotation",
                "Generate new password meeting complexity requirements",
                "Update the password in Active Directory / Azure AD",
                "Update all dependent system configurations with new credentials",
                "Verify each dependent service resumes normal operation",
                "Update password rotation schedule to prevent future near-expiry situations",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-shared-mailbox-access",
        category="Access & Authentication",
        priority="P4",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["affected_system", "business_impact"],
        subjects=[
            "Need access to shared mailbox for Client Services team",
            "Request access to shared mailbox clientservices@contoso.com",
            "Can't see the team shared mailbox in Outlook",
            "Add me to the Client Services shared mailbox please",
        ],
        descriptions=[
            "I recently transferred to the Client Services team and need access to the shared mailbox "
            "clientservices@contoso.com. My manager approved this — she's CC'd on this email. I need it for handling "
            "client inquiries.",
            "I've been asked to help with the quarterly investor communications and need access to the IR shared "
            "mailbox. My director approved the request. Please add me with send-as permissions.",
            "Just joined the Legal team and was told I should have access to legal-inbox@contoso.com. I don't see it in"
            " Outlook. My manager name is Sandra Williams.",
        ],
        next_best_actions=[
            "Verify manager approval and add user to the shared mailbox with appropriate permissions.",
            "Check approval chain and grant shared mailbox access with requested permission level.",
        ],
        remediation_steps=[
            [
                "Verify manager approval for shared mailbox access",
                "Check user's role aligns with shared mailbox access requirements",
                "Add user to the shared mailbox with Full Access permissions in Exchange Online",
                "Configure Send-As or Send-on-Behalf permissions if requested",
                "Instruct user to restart Outlook or wait for auto-mapping to take effect",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-guest-contractor-access",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["business_impact", "configuration_details"],
        subjects=[
            "Need to set up guest access for external contractor",
            "Azure AD B2B guest access for audit firm",
            "External consultant needs temporary system access",
            "Contractor access request — 3 month engagement",
        ],
        descriptions=[
            "We need to set up Azure AD B2B guest access for 3 consultants from Deloitte who are doing our annual "
            "audit. They need read-only access to SharePoint finance documents and the internal compliance portal. "
            "Engagement runs March through May.",
            "External penetration testing firm needs temporary accounts for a 2-week engagement starting next Monday. "
            "They'll need VPN access and limited network scanning permissions. SOW is signed — attaching approval from "
            "CISO.",
            "A contractor from McKinsey is joining our strategy team for 3 months. She needs email, Teams, and access "
            "to our strategic planning SharePoint site. Her laptop will be personal — not company-managed.",
        ],
        next_best_actions=[
            "Create guest accounts with appropriate Conditional Access policies. Ensure time-bound access with "
            "automatic expiry.",
            "Provision B2B guest accounts with minimum required permissions and set access review schedule.",
        ],
        remediation_steps=[
            [
                "Verify engagement approval and scope documentation",
                "Create Azure AD B2B guest accounts for external users",
                "Apply appropriate Conditional Access policies (MFA, device compliance)",
                "Grant minimum required permissions to specified resources",
                "Set access expiration date aligned with engagement end date",
                "Configure access review for periodic re-certification",
                "Send onboarding instructions to external users",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-vpn-cert-expired",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["device_info", "error_message"],
        subjects=[
            "VPN client certificate expired — can't connect remotely",
            "Certificate error when connecting to corporate VPN",
            "VPN says certificate invalid — worked fine last week",
            "Remote access broken — certificate authentication failure",
        ],
        descriptions=[
            "My VPN client is showing a certificate error when I try to connect from home. The error says 'certificate "
            "has expired or is not yet valid'. I need remote access for the rest of this week — I'm working from home "
            "due to a family situation.",
            "Can't connect to the corporate VPN. Getting a cert validation error. I'm a remote employee in Denver and "
            "this is my only way to access internal systems. Last connected successfully on Friday.",
            "VPN certificate-based authentication failing since this morning. Error code 0x80090328. I'm working "
            "remotely and need immediate access to internal resources.",
        ],
        next_best_actions=[
            "Issue new VPN client certificate. Check if this is an isolated expiry or part of a batch certificate "
            "renewal issue.",
            "Re-issue user VPN certificate and verify certificate authority chain.",
        ],
        remediation_steps=[
            [
                "Check user's VPN client certificate expiration date",
                "Issue a new client certificate from the internal CA",
                "Install the new certificate on the user's device",
                "Verify VPN connection works with the new certificate",
                "Check if other users are affected by similar certificate expirations",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-ad-group-request",
        category="Access & Authentication",
        priority="P4",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["business_impact"],
        subjects=[
            "Request to join AD group for financial reporting tools",
            "Need AD group membership for accessing BI dashboards",
            "AD group add request — reporting-analysts-global",
            "Please add me to the Financial Systems access group",
        ],
        descriptions=[
            "I need to be added to the AD group 'reporting-analysts-global' to access the financial reporting "
            "dashboards in Power BI. My manager approved this change. Group owner is Raj Mehta in IT.",
            "Requesting membership in the 'risk-analytics-users' AD group. I've been assigned to a new project that "
            "requires access to the risk analytics platform. Manager approval email attached.",
            "Please add my account to the 'trading-floor-apps' security group. I transferred from the London office and"
            " my group memberships didn't follow. Need access to trading tools.",
        ],
        next_best_actions=[
            "Verify approval and add user to the requested AD group after confirming group owner consent.",
            "Process AD group membership request with proper approval chain.",
        ],
        remediation_steps=[
            [
                "Verify manager and group owner approval",
                "Add user to the requested Active Directory security group",
                "Allow replication time for group membership to propagate",
                "Instruct user to sign out and back in to receive new group membership token",
                "Confirm user can access the intended resources",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-conditional-access-blocked",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["device_info", "network_location"],
        subjects=[
            "Can't access email from new personal device — blocked by policy",
            "Conditional Access blocking me from logging in",
            "Policy error: 'Your sign-in was blocked' on new laptop",
            "Azure AD blocking login — compliant device required",
        ],
        descriptions=[
            "I got a new personal laptop and I can't access my Contoso email through the browser. I get a message "
            "saying 'Your sign-in was blocked' and something about conditional access policy. I've always been able to "
            "check email from personal devices before.",
            "I'm trying to log in from my home desktop and getting blocked by Conditional Access. The error says my "
            "device isn't registered. I work remotely 3 days a week — this used to work. Something changed recently.",
            "After traveling to our Singapore office, I can't log into Teams or Outlook from the office workstation "
            "here. Getting a Conditional Access block. The Singapore team says they don't have this issue.",
        ],
        next_best_actions=[
            "Review Conditional Access policy triggers for the user's sign-in attempt. Determine if device compliance "
            "or location policy is the blocker.",
            "Check sign-in logs to identify which CA policy blocked access and determine appropriate remediation.",
        ],
        remediation_steps=[
            [
                "Review Azure AD sign-in logs to identify the blocking Conditional Access policy",
                "Determine if the block is due to device compliance, location, or risk level",
                "If device compliance issue, guide user to enroll device in Intune",
                "If location-based block, verify if location exception is needed",
                "Verify user can access resources after remediation",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-sspr-broken",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=True,
        missing_information=["error_message", "affected_users"],
        subjects=[
            "Self-service password reset portal not working for anyone",
            "SSPR down — multiple users reporting issues",
            "Password reset portal giving errors to everyone",
            "Company-wide self-service password reset failure",
        ],
        descriptions=[
            "Multiple users on our floor are reporting that the self-service password reset portal is giving a 500 "
            "error. At least 8 people can't reset their passwords this morning. This seems like a systemic issue, not "
            "individual.",
            "The SSPR portal has been down since 8 AM. I've had 12 users call me directly because they can't reset "
            "their passwords. The portal just spins and then shows 'Service unavailable'. This is impacting "
            "productivity across the organization.",
            "Self-service password reset is broken for the entire Finance department. Every attempt returns an error. "
            "We have 15+ users locked out and unable to work. Needs immediate attention.",
        ],
        next_best_actions=[
            "Investigate SSPR service health in Azure AD. Check for service incidents or configuration changes. Set up "
            "manual reset queue for affected users.",
            "Check Azure AD service health for SSPR outage. Establish manual reset process while investigating.",
        ],
        remediation_steps=[
            [
                "Check Azure AD service health dashboard for SSPR-related incidents",
                "Review recent changes to SSPR policy or authentication methods configuration",
                "Test SSPR from admin account to confirm scope of issue",
                "If service-side issue, open Microsoft support ticket with high priority",
                "Set up manual password reset queue for affected users as interim solution",
                "Communicate status and workaround to affected users",
                "Monitor SSPR service restoration and confirm functionality",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-pim-activation-failed",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["error_message", "affected_system"],
        subjects=[
            "PIM role activation failing — need Global Reader access",
            "Can't activate my privileged role in Azure PIM",
            "Privileged Identity Management activation stuck",
            "PIM elevation request denied — Error activating role",
        ],
        descriptions=[
            "I'm trying to activate my Global Reader role through PIM for an audit that starts in 1 hour, but the "
            "activation keeps failing with a vague error. I'm an eligible member — used this role last month without "
            "issues. The Azure portal just shows 'activation failed'.",
            "Need to activate my Security Administrator PIM role to investigate a potential incident but PIM is "
            "throwing errors. Activation request was submitted 30 minutes ago and is stuck in 'Pending' state. This is "
            "time-sensitive.",
            "PIM role activation for Exchange Administrator is failing. Error message says 'approval workflow error'. I"
            "'ve been eligible for this role for 6 months and activated it successfully many times before. Need it for "
            "an email migration starting today.",
        ],
        next_best_actions=[
            "Check PIM activation workflow status and approval chain. Investigate any recent PIM policy changes or "
            "Azure AD service issues.",
            "Review PIM audit logs for activation failure reason and manually approve if blocked by workflow.",
        ],
        remediation_steps=[
            [
                "Check Azure AD PIM activation logs for the specific error",
                "Verify PIM policy settings and approval requirements for the role",
                "Check if an approver needs to take action on the pending request",
                "If workflow is broken, manually grant the role with a time-limited assignment",
                "Investigate root cause of activation failure",
                "Confirm user can access required resources after role activation",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-account-disabled",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["timestamp", "business_impact"],
        subjects=[
            "My account was disabled — I haven't done anything wrong",
            "Account unexpectedly disabled — locked out of everything",
            "AD account disabled without explanation",
            "Can't log in — account disabled error message",
        ],
        descriptions=[
            "I came in this morning and my account is disabled. I can't log into my computer, email, or anything. I "
            "haven't violated any policies. My manager didn't get any notification about this. I've been with the "
            "company for 5 years. Is this a mistake?",
            "My Active Directory account was disabled overnight. When I try to log in I get 'your account has been "
            "disabled, contact your administrator'. I'm not on any PIP or leave. This seems like an error.",
            "Got a call from a team member that they can't reach me — turns out my account is disabled. I was working "
            "late last night and everything was fine at 11 PM. Something happened between then and this morning.",
        ],
        next_best_actions=[
            "Investigate why the account was disabled by checking audit logs. Determine if it was automated (security "
            "trigger) or manual action.",
            "Check AD audit logs for who/what disabled the account and re-enable if appropriate.",
        ],
        remediation_steps=[
            [
                "Check Azure AD / Active Directory audit logs for the disable action",
                "Determine if disabling was automated (security policy) or manual (admin action)",
                "If automated, investigate the trigger (e.g., risky sign-in, identity protection)",
                "If manual error, re-enable the account",
                "Verify no unauthorized access occurred that triggered the disable",
                "Confirm user can log in and access all required resources",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-oauth-consent",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["application_version", "affected_system"],
        subjects=[
            "Need admin consent for a third-party app in Azure AD",
            "OAuth consent required for new project tool",
            "App permissions consent request — blocked by admin policy",
            "Can't authorize Figma — needs admin approval",
        ],
        descriptions=[
            "I'm trying to use Figma for our new design project but when I sign in with my Contoso account, it says "
            "'Approval required — an admin must grant consent for this app'. Our design team of 12 people needs this "
            "tool for the rebrand project.",
            "A new analytics tool (Mixpanel) requires OAuth consent from an Azure AD admin. The entire product team is "
            "blocked — we purchased licenses already but can't actually use the service. Requesting admin consent for "
            "the app.",
            "Trying to connect a project management tool to our Azure AD for SSO but getting blocked by admin consent "
            "policy. We've completed the security review and got CISO approval — just need the technical consent "
            "granted.",
        ],
        next_best_actions=[
            "Review the app's requested permissions. If approved through procurement/security review, grant admin "
            "consent in Azure AD.",
            "Check if the app has been through security review and grant admin consent if approved.",
        ],
        remediation_steps=[
            [
                "Review the OAuth permissions requested by the application",
                "Verify the application has been approved through security review process",
                "Check procurement records for license purchase approval",
                "Grant admin consent in Azure AD Enterprise Applications",
                "Configure any additional Conditional Access policies for the app",
                "Notify requesting team that access is now available",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-kerberos-legacy",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["error_message", "configuration_details"],
        subjects=[
            "Kerberos authentication failing for legacy finance app",
            "Can't authenticate to on-prem finance system — Kerberos error",
            "Legacy application Kerberos ticket issue",
            "Internal finance app keeps asking for credentials — Kerberos broken",
        ],
        descriptions=[
            "Our legacy finance reconciliation system (on-prem, Windows Server 2016) is failing Kerberos authentication"
            " for my team. We keep getting prompted for credentials. The SPN might be misconfigured — we had a server m"
            "igration last week.",
            "The old FinRecon application that runs on-premises is throwing Kerberos errors. It was working fine until "
            "the domain controller maintenance last weekend. About 15 users in Finance are affected.",
            "Getting repeated credential prompts when accessing the on-prem risk management system. Kerberos ticket "
            "seems to be expiring immediately. Event logs show KRB_AP_ERR_MODIFIED errors.",
        ],
        next_best_actions=[
            "Check SPN registration for the application service account. Verify domain controller replication and "
            "Kerberos ticket issuance.",
            "Investigate SPN configuration and recent DC changes that may have broken Kerberos authentication.",
        ],
        remediation_steps=[
            [
                "Check Service Principal Name (SPN) registration for the application",
                "Verify domain controller replication is healthy",
                "Review recent changes to the application's service account",
                "Re-register SPNs if duplicates or misconfigurations are found",
                "Test Kerberos authentication with klist and kerbtray tools",
                "Confirm application authentication works for affected users",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-rbac-azure",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["affected_system", "configuration_details"],
        subjects=[
            "Need Contributor access to Azure resource group for deployment",
            "Azure RBAC — requesting access to production subscription",
            "Can't deploy to Azure — insufficient permissions",
            "Access denied on Azure resource group — need role assignment",
        ],
        descriptions=[
            "I need Contributor role on the 'rg-prod-trading-eastus' resource group to deploy our new microservice. "
            "Currently getting 403 Forbidden when running our CI/CD pipeline. My manager (Kevin O'Brien) approved this "
            "— he's the resource group owner.",
            "Requesting Reader access to the production Azure subscription for monitoring purposes. I'm on the SRE team"
            " and need to view resource health and metrics. Approved by our team lead.",
            "I can't access the Azure Key Vault in our staging environment. Getting 'AuthorizationFailed'. I need to "
            "configure secrets for our new application deployment. Manager has already approved.",
        ],
        next_best_actions=[
            "Verify manager approval and assign the requested Azure RBAC role with appropriate scope.",
            "Process Azure RBAC role assignment after confirming approval chain.",
        ],
        remediation_steps=[
            [
                "Verify manager/resource owner approval for the RBAC assignment",
                "Review the principle of least privilege for the requested role and scope",
                "Assign the role via Azure portal or CLI at the appropriate scope",
                "If production access, ensure PIM-eligible assignment instead of permanent",
                "Verify user can access the required resources with new permissions",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-cross-tenant-b2b",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["configuration_details", "affected_system"],
        subjects=[
            "Cross-tenant B2B collaboration not working with partner",
            "Can't access partner organization's Teams channels",
            "Azure AD B2B — external access to partner tenant failing",
            "Shared channels with Meridian Partners not accessible",
        ],
        descriptions=[
            "We set up shared Teams channels with Meridian Partners for a joint deal, but their users can't access our "
            "shared channels. They get a 'your organization doesn't allow external access' error. Our side looks "
            "configured correctly.",
            "B2B collaboration with our legal partner firm is broken. Their attorneys need access to a shared SharePoin"
            "t site for the merger documents but invitations keep failing. Cross-tenant access policy might be the issu"
            "e.",
            "I'm trying to invite external collaborators from our partner bank into a shared Teams workspace. The invit"
            "ations go out but when they try to accept, they get an access policy error. Both orgs supposedly have B2B "
            "enabled.",
        ],
        next_best_actions=[
            "Review cross-tenant access settings for both organizations. Check Teams external access policies and "
            "SharePoint sharing settings.",
            "Verify Azure AD cross-tenant access policy configuration and ensure both tenant admins have approved the "
            "B2B relationship.",
        ],
        remediation_steps=[
            [
                "Review Azure AD cross-tenant access settings for the partner organization",
                "Verify Teams external access policy allows the partner domain",
                "Check if SharePoint sharing settings permit B2B guest access",
                "Ensure both organizations have compatible B2B policies",
                "Re-send invitations after policy corrections",
                "Test access from partner organization side to confirm",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-account-lockout-brute",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=True,
        missing_information=["timestamp", "network_location"],
        subjects=[
            "Account keeps locking out every 15 minutes",
            "Repeated account lockouts — possible credential stuffing",
            "My account locks every time I unlock it — something is wrong",
            "Continuous account lockout loop",
        ],
        descriptions=[
            "My account has been locking out every 15 minutes since yesterday. I unlock it, work for 15 minutes, then g"
            "et locked out again. I've changed my password twice but it keeps happening. I think something is using my "
            "old credentials somewhere.",
            "I've been locked out 8 times today. Each time I reset my password, it locks again within minutes. I'm "
            "worried there might be a saved password somewhere that's trying the old one. Or worse — someone is trying "
            "to get into my account.",
            "Account lockout happening repeatedly. Changed password 3 times. IT unlocks me, then within 10-15 minutes "
            "I'm locked again. There might be a stale credential on a service or cached password somewhere.",
        ],
        next_best_actions=[
            "Investigate account lockout source by checking DC security logs. Look for stale credentials on services, "
            "scheduled tasks, or mapped drives.",
            "Analyze authentication logs to find the source of repeated lockouts. Check for compromised credential "
            "indicators.",
        ],
        remediation_steps=[
            [
                "Check domain controller security logs for lockout source IP and service",
                "Run lockout tools (Account Lockout and Management Tools) to trace the source",
                "Check for cached credentials in Windows Credential Manager on user's devices",
                "Verify no scheduled tasks or services are using old credentials",
                "Check mobile devices for saved email/VPN passwords",
                "If source is external, investigate possible credential compromise",
                "Reset password and clear all cached credentials on identified sources",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-ldap-bind-failure",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["error_message", "configuration_details"],
        subjects=[
            "LDAP bind failure on legacy HR application",
            "Legacy app can't authenticate via LDAP anymore",
            "LDAP connection refused after DC update",
            "HR system LDAP authentication broken",
        ],
        descriptions=[
            "Our legacy HR system (PeopleSoft) stopped authenticating users via LDAP this morning. The LDAP bind is "
            "failing with 'invalid credentials' even though the service account password hasn't changed. About 200 HR "
            "users can't log in.",
            "After the domain controller update last weekend, our legacy payroll application can no longer perform LDAP"
            " binds. We're getting connection refused errors. This is affecting the entire payroll team — payday is Fri"
            "day.",
            "The LDAP integration for our on-prem CRM system broke after the DC patching. LDAP simple bind is being "
            "rejected — the error indicates the server requires LDAPS now. This was a surprise change for our team.",
        ],
        next_best_actions=[
            "Check DC LDAP binding requirements post-update. Verify if LDAP channel binding or signing policy changed. "
            "Check service account status.",
            "Investigate DC LDAP policy changes and update legacy application LDAP configuration accordingly.",
        ],
        remediation_steps=[
            [
                "Check if domain controller LDAP channel binding or signing policies changed",
                "Verify service account status and credentials in Active Directory",
                "Test LDAP bind from the application server using ldp.exe or ldapsearch",
                "If LDAPS now required, update application configuration to use LDAPS (port 636)",
                "Install required certificates on the application server for LDAPS",
                "Coordinate with application team to update LDAP connection strings",
                "Verify authentication works for end users",
            ],
        ],
    ),
    Scenario(
        scenario_id="auth-saml-sso-loop",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["authentication_method", "steps_to_reproduce", "application_version"],
        subjects=[
            "SAML SSO login stuck in redirect loop",
            "Infinite redirect when trying to SSO into Workday",
            "SSO keeps bouncing between IdP and Workday — never logs in",
        ],
        descriptions=[
            "When I try to log into Workday through SSO, the browser just keeps bouncing between the Microsoft login "
            "page and Workday without ever completing. I've cleared cookies and tried multiple browsers. My colleague "
            "next to me can log in fine.",
            "Getting stuck in a redirect loop trying to SSO into Workday. Chrome DevTools shows a 302 redirect chain "
            "between login.microsoftonline.com and sso.workday.com that never ends. Started this morning.",
        ],
        next_best_actions=[
            "Check SAML configuration for Workday SSO enterprise application. Verify user is assigned to the app in "
            "Entra ID and claims mapping is correct.",
        ],
        remediation_steps=[
            [
                "Verify user is assigned to the Workday enterprise application in Entra ID",
                "Check SAML token claims mapping for correct NameID and attribute values",
                "Review Entra ID sign-in logs for SAML authentication failures",
                "Verify Workday SSO configuration matches the Entra ID SAML metadata",
                "Test in InPrivate/incognito browser to rule out cached token issues",
                "If claims mismatch, update SAML attribute mapping in Entra ID",
            ],
        ],
        tags=["sso", "saml"],
    ),
    Scenario(
        scenario_id="auth-pim-activation-fail",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=True,
        missing_information=["steps_to_reproduce", "error_message"],
        subjects=[
            "PIM role activation failing — need admin access urgently",
            "Can't activate privileged role in Entra PIM",
            "Privileged Identity Management role request stuck",
        ],
        descriptions=[
            "I'm trying to activate my Cloud Application Administrator role through PIM for a critical deployment, but "
            "it keeps erroring out with a generic 'request could not be processed' message. I've been approved by my "
            "manager already. Deployment deadline is in 3 hours.",
            "PIM activation for my Azure subscription Owner role is failing. The request shows as 'pending' but never "
            "transitions to 'active'. I need this for a production hotfix deployment today.",
        ],
        next_best_actions=[
            "Check PIM service health and verify the role assignment eligibility. If PIM is degraded, consider direct "
            "role assignment as temporary workaround.",
        ],
        remediation_steps=[
            [
                "Check Entra PIM service health in Azure status page",
                "Verify user's eligible role assignments and approval status",
                "Check PIM activation logs for specific error details",
                "If PIM is degraded, consider temporary direct role assignment by a Global Admin",
                "Ensure any required justification and ticket number are provided",
                "Confirm role activation and verify access to target resources",
            ],
        ],
        tags=["privileged_access", "urgent"],
    ),
    Scenario(
        scenario_id="auth-kerberos-constrained-delegation",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["configuration_details", "authentication_method", "environment_details"],
        subjects=[
            "Kerberos constrained delegation not working for internal app",
            "KCD authentication failing — double-hop issue",
            "Internal web app can't authenticate to backend SQL via Kerberos",
        ],
        descriptions=[
            "Our internal web application on IIS can't authenticate to the backend SQL Server using Kerberos "
            "constrained delegation. Users get an 'access denied' when the app tries to query SQL on behalf of the "
            "user. SPNs are configured but something seems off.",
            "We're hitting the classic Kerberos double-hop problem with our internal portal. The web tier can't pass th"
            "rough user credentials to the database tier. This was working before we migrated to new web servers last m"
            "onth.",
        ],
        next_best_actions=[
            "Verify SPN registration, delegation settings on service accounts, and KCD configuration in AD for the web "
            "and SQL service accounts.",
        ],
        remediation_steps=[
            [
                "Verify SPN registrations for both web server and SQL Server service accounts",
                "Check Active Directory delegation settings on the web server service account",
                "Ensure constrained delegation is configured to the correct SQL Server SPN",
                "Verify the web application pool identity matches the service account with delegation",
                "Test with setspn -L and klist to verify ticket issuance",
                "Check for duplicate SPNs that could cause authentication failures",
            ],
        ],
        tags=["kerberos", "authentication"],
    ),
    Scenario(
        scenario_id="auth-entra-connect-sync-fail",
        category="Access & Authentication",
        priority="P1",
        assigned_team="Identity & Access Management",
        needs_escalation=True,
        missing_information=["error_message", "timestamp"],
        subjects=[
            "Entra Connect sync has stopped — new users not provisioning",
            "Azure AD Connect sync broken — changes not replicating",
            "Directory sync failed — Entra Connect showing export errors",
        ],
        descriptions=[
            "Our Entra Connect server hasn't synced in over 6 hours. New hires who started today have no cloud accounts"
            " and can't access M365 services. The sync status dashboard shows multiple export errors. We have 15 new jo"
            "iners starting today across all three offices.",
            "Entra Connect delta sync is failing with 'stopped-server-down' status. Password hash sync and passthrough "
            "auth are also affected. Multiple users reporting they can't reset passwords via SSPR. This is impacting "
            "all 4500 employees.",
        ],
        next_best_actions=[
            "Immediately investigate Entra Connect server health and sync status. Check for expired certificates, "
            "service account issues, or server resource exhaustion.",
        ],
        remediation_steps=[
            [
                "Check Entra Connect server health (CPU, memory, disk, services running)",
                "Review Synchronization Service Manager for export/import error details",
                "Verify the Entra Connect service account credentials haven't expired",
                "Check for expired TLS certificates used by the sync engine",
                "Restart the Microsoft Azure AD Sync service if server is healthy",
                "If sync resumes, force a full sync cycle and monitor for errors",
                "For blocked new hires, create cloud-only accounts as temporary measure",
            ],
        ],
        tags=["directory_sync", "critical"],
        channel_weights={"email": 0.10, "chat": 0.20, "portal": 0.10, "phone": 0.60},
    ),
    Scenario(
        scenario_id="auth-fido2-key-not-recognized",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["device_info", "authentication_method", "steps_to_reproduce"],
        subjects=[
            "FIDO2 security key not recognized during sign-in",
            "YubiKey stopped working for passwordless login",
            "Hardware security key authentication failing",
        ],
        descriptions=[
            "My YubiKey 5 NFC that I use for passwordless sign-in to Microsoft 365 stopped working today. When I tap it"
            " during sign-in, nothing happens — the browser doesn't detect it. I've tested the key on a different compu"
            "ter and it works, so the key itself seems fine.",
            "FIDO2 passwordless sign-in with my security key isn't working anymore. Chrome says 'Security key not "
            "detected' but the key lights up when I touch it. Was working perfectly until yesterday.",
        ],
        next_best_actions=[
            "Check WebAuthn/FIDO2 browser support and driver status. Verify the FIDO2 key registration in Entra ID is "
            "still active.",
        ],
        remediation_steps=[
            [
                "Verify the FIDO2 security key registration is still active in Entra ID security info",
                "Check browser WebAuthn support (Chrome/Edge requirement for FIDO2)",
                "Verify USB/NFC drivers are installed and functioning on the workstation",
                "Try the security key in a different USB port or via NFC",
                "If registration is missing, re-register the FIDO2 key in security info",
                "Provide temporary alternative MFA method while troubleshooting",
            ],
        ],
        tags=["fido2", "passwordless"],
    ),
    Scenario(
        scenario_id="auth-oauth-consent-blocked",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["application_version", "business_impact"],
        subjects=[
            "OAuth app consent blocked by admin policy",
            "Can't authorize third-party app — needs admin consent",
            "Application requires permissions I can't grant",
        ],
        descriptions=[
            "I'm trying to connect Miro to my Microsoft 365 account for a project collaboration board, but I'm getting "
            "a message that says 'Need admin approval — this app requires permissions that only an admin can grant.' My"
            " team needs this for a client presentation on Friday.",
            "When I try to sign into a vendor's project management portal using my Contoso SSO, I get an 'admin consent"
            " required' error. The app is requesting Calendar.Read and User.Read permissions. Our vendor says all their"
            " other clients approved it easily.",
        ],
        next_best_actions=[
            "Review the OAuth application consent request and determine if the requested permissions are acceptable per"
            " security policy. If approved, grant admin consent.",
        ],
        remediation_steps=[
            [
                "Review the application's requested permissions in the admin consent workflow",
                "Verify the application publisher is verified and trustworthy",
                "Check if the app is on the organization's approved/blocked app list",
                "If permissions are acceptable, grant admin consent via Entra ID",
                "If permissions are excessive, work with the vendor on reduced scope",
                "Notify the user once consent is granted and verify access works",
            ],
        ],
        tags=["oauth", "consent"],
    ),
    Scenario(
        scenario_id="auth-conditional-access-travel",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["network_location", "timestamp"],
        subjects=[
            "Blocked by conditional access while traveling — can't access email",
            "Conditional access policy blocking me from overseas",
            "Can't log in from client site in Tokyo — geo-restriction",
        ],
        descriptions=[
            "I'm currently at a client site in Tokyo for business meetings and I'm completely blocked from accessing my"
            " email and Teams. The error says something about conditional access policy blocking sign-ins from this loc"
            "ation. I have critical client meetings all week and need access immediately.",
            "Traveling for work in Germany and conditional access is blocking all my Microsoft 365 access. I filed a "
            "travel notice with HR last week but apparently IT wasn't notified. I need this resolved ASAP — I have a "
            "board presentation tomorrow morning.",
        ],
        next_best_actions=[
            "Add temporary location exception to conditional access policy for the user's travel destination. Verify "
            "travel request was filed and approved.",
        ],
        remediation_steps=[
            [
                "Confirm the user's business travel is authorized (check with manager/HR)",
                "Add a temporary named location exception for the travel destination",
                "Set expiration date on the exception matching the travel return date",
                "Verify the user can now authenticate from the travel location",
                "Review the travel notification process to prevent future occurrences",
            ],
        ],
        tags=["conditional_access", "travel"],
    ),
    Scenario(
        scenario_id="auth-service-principal-expired",
        category="Access & Authentication",
        priority="P1",
        assigned_team="Identity & Access Management",
        needs_escalation=True,
        missing_information=["affected_system", "configuration_details"],
        subjects=[
            "Service principal credential expired — automated pipeline broken",
            "App registration secret expired — CI/CD pipeline failing",
            "Azure service principal auth failing across multiple applications",
        ],
        descriptions=[
            "Our CI/CD pipeline stopped deploying about an hour ago. After investigating, we found that the service "
            "principal secret used by our Azure DevOps pipeline expired today. This is blocking all deployments to "
            "production, staging, and dev environments. Multiple teams are affected.",
            "The Entra ID app registration for our data ingestion service has an expired client secret. Our entire ETL "
            "pipeline is down and no data is flowing into the data warehouse. Finance team needs their morning reports "
            "which depend on this pipeline.",
        ],
        next_best_actions=[
            "Immediately generate a new client secret for the service principal and update all dependent applications "
            "and pipelines.",
        ],
        remediation_steps=[
            [
                "Identify the expired service principal in Entra ID app registrations",
                "Generate a new client secret with appropriate expiration date",
                "Update the secret in Azure DevOps/pipeline variable groups",
                "Update any other applications consuming this service principal",
                "Trigger pipeline re-run to verify authentication works",
                "Set up expiration monitoring alerts for all service principal secrets",
            ],
        ],
        tags=["service_principal", "automation", "critical"],
        channel_weights={"email": 0.10, "chat": 0.30, "portal": 0.10, "phone": 0.50},
    ),
    Scenario(
        scenario_id="auth-batch-account-lockout",
        category="Access & Authentication",
        priority="P1",
        assigned_team="Identity & Access Management",
        needs_escalation=True,
        missing_information=["affected_users", "timestamp", "steps_to_reproduce"],
        subjects=[
            "Mass account lockout — entire trading floor affected",
            "Dozens of accounts locked out simultaneously",
            "Widespread account lockout event across multiple departments",
        ],
        descriptions=[
            "We're seeing a mass account lockout event across the trading floor. At least 40 traders have been locked "
            "out in the last 15 minutes. This is happening during market hours and we're losing millions in missed "
            "trades. Security team suspects it might be a credential stuffing attack or a misconfigured service.",
            "Approximately 50-60 user accounts got locked out simultaneously starting around 10:30 AM. It's affecting "
            "people across Trading, Operations, and Settlement teams. Some accounts are getting re-locked within "
            "minutes of being unlocked. We need to identify the source immediately.",
        ],
        next_best_actions=[
            "Immediately investigate lockout source by reviewing DC security event logs. Determine if this is an attack"
            " or misconfigured service account. Unlock affected accounts in parallel.",
        ],
        remediation_steps=[
            [
                "Review domain controller security event logs (Event ID 4740) for lockout source",
                "Identify the originating IP/workstation causing the lockouts",
                "If service account: identify the misconfigured application and update credentials",
                "If attack: engage Security Operations for incident response",
                "Bulk-unlock affected accounts via PowerShell",
                "Implement temporary lockout threshold increase if legitimate service issue",
                "Communicate status to trading floor management",
            ],
        ],
        tags=["mass_lockout", "critical", "trading"],
        channel_weights={"email": 0.05, "chat": 0.15, "portal": 0.05, "phone": 0.75},
    ),
]

