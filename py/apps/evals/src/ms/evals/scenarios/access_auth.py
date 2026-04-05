# Copyright (c) Microsoft. All rights reserved.
"""Access & Authentication scenario templates.

Covers: password resets, account lockouts, SSO failures, MFA issues,
provisioning, service accounts, directory sync, conditional access,
certificate auth, and federated identity.
"""

from ms.evals.constants import Category
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.models import ScenarioTemplate
from ms.evals.scenarios.registry import register

register(
    ScenarioTemplate(
        scenario_id="aa-001",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "Can't reset my password through the self-service portal",
            "Password reset not working — SSPR portal gives an error",
            "Self-service password reset fails every time",
        ],
        descriptions=[
            "I've been trying to reset my password through the self-service portal since this morning but "
            "it keeps giving me a generic error. I've tried three different browsers. My account isn't "
            "locked — I can still log in with my old password but I need to change it per the 90-day "
            "policy reminder I got last week.",
            "The SSPR portal loads fine but when I submit my new password it just says 'Something went "
            "wrong. Please try again.' I've tried passwords that meet all the complexity requirements. "
            "Been at this for 20 minutes now.",
        ],
        next_best_actions=[
            "Check SSPR service health and verify user's authentication methods are properly registered "
            "in Entra ID. If SSPR is functional, perform admin-initiated password reset.",
            "Verify SSPR configuration for user's OU and check if password writeback is working. Reset "
            "password manually if self-service continues to fail.",
        ],
        remediation_steps=[
            [
                "Verify SSPR service health in Entra ID admin portal",
                "Check user's registered authentication methods for SSPR",
                "Verify password writeback is configured and operational",
                "If SSPR is down, perform admin-initiated password reset",
                "Confirm user can log in with new password",
            ],
            [
                "Check Entra ID SSPR logs for specific error details",
                "Verify user is in the SSPR-enabled group",
                "Test SSPR with a test account in the same OU",
                "If systemic, escalate to IAM engineering for SSPR service investigation",
                "Perform manual password reset as interim workaround",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-002",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.DEVICE_INFO],
        subjects=[
            "Account locked out — can't access anything",
            "My account keeps getting locked every 30 minutes",
            "Repeated account lockouts since yesterday",
        ],
        descriptions=[
            "My account gets locked out every 30 minutes or so. I unlock it through IT, log in, work for "
            "a bit, then it locks again. This started yesterday. I haven't changed my password recently. "
            "I'm in {department} and I can't get anything done like this.",
            "Account keeps locking. This is the fourth time today. The last time I called the help desk "
            "they unlocked it but it happened again within the hour. I think something is trying to "
            "authenticate with my old credentials somewhere.",
        ],
        next_best_actions=[
            "Check Entra ID sign-in logs for failed authentication attempts and identify the source of "
            "repeated lockouts. Look for stale credentials on devices or services.",
            "Investigate sign-in logs for brute-force patterns or stale credential usage. If suspicious "
            "activity detected, alert Security Operations.",
        ],
        remediation_steps=[
            [
                "Unlock the user's account in Entra ID",
                "Review sign-in logs for failed authentication sources",
                "Check for stale credentials on mobile devices, VPN clients, or cached sessions",
                "If a specific device is causing lockouts, clear saved credentials on that device",
                "Monitor for recurrence over the next 24 hours",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-003",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=True,
        missing_information=[],
        subjects=[
            "Account lockout with suspicious foreign login attempts",
            "Getting locked out and I see login attempts from China",
            "Account compromised? Seeing logins from unknown locations",
        ],
        descriptions=[
            "My account keeps getting locked and when I checked the sign-in activity page I see failed "
            "attempts from IP addresses in China and Russia. I haven't traveled. I changed my password "
            "immediately and enabled MFA but I'm worried my account was already accessed. I handle "
            "confidential client financial data.",
            "I noticed multiple failed sign-in attempts on my account from locations I've never been to — "
            "Brazil and Nigeria. My account was locked this morning. I changed my password but I need "
            "someone to check if any data was accessed before I noticed.",
        ],
        next_best_actions=[
            "Escalate to Security Operations for compromised account investigation. Review sign-in logs "
            "for any successful authentications from suspicious locations. Revoke all active sessions.",
            "Immediately revoke all active sessions and tokens. Coordinate with SecOps to investigate "
            "potential unauthorized access to confidential financial data.",
        ],
        remediation_steps=[
            [
                "Revoke all active sessions and refresh tokens in Entra ID",
                "Review sign-in logs for any successful authentications from suspicious IPs",
                "Verify MFA is properly configured and enforced",
                "Check for any mailbox forwarding rules or consent grants added",
                "Coordinate with Security Operations for full incident investigation",
                "If data access confirmed, initiate data breach response protocol",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-004",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "SSO not working for Salesforce",
            "Can't log into {app} — SSO redirect fails",
            "Single sign-on broken after update",
        ],
        descriptions=[
            "When I try to log into Salesforce through the SSO portal, it redirects me back to the login "
            "page without an error. It worked fine last week. Other apps through SSO seem fine — just "
            "Salesforce.",
            "SSO stopped working for me. I click the app tile in the portal and it just spins, then "
            "shows a blank page. I've tried clearing cookies and using incognito mode. Other people in "
            "my team seem to be able to log in fine.",
        ],
        next_best_actions=[
            "Check Entra ID enterprise application configuration for Salesforce. Verify the user's "
            "assignment and SSO certificate validity.",
        ],
        remediation_steps=[
            [
                "Verify user is assigned to the Salesforce enterprise application in Entra ID",
                "Check SSO certificate expiration for the Salesforce integration",
                "Review Entra ID sign-in logs for SAML assertion errors",
                "Test SSO flow with a known-good account for comparison",
                "If certificate expired, rotate and update in both Entra ID and Salesforce",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-005",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.DEVICE_INFO],
        subjects=[
            "MFA not working on my new phone",
            "Authenticator app stopped working after phone upgrade",
            "Can't complete MFA — phone shows no notifications",
        ],
        descriptions=[
            "I upgraded my phone last weekend and now the Microsoft Authenticator app doesn't show "
            "push notifications. I can still use it for codes but the push approval doesn't work. "
            "I need this fixed because I have to approve MFA like 20 times a day.",
            "Got a new phone and set up the Authenticator app but MFA prompts aren't coming through. "
            "I re-registered in the app but it still doesn't push. I can log in using the 6-digit code "
            "but it's really inconvenient.",
        ],
        next_best_actions=[
            "Guide user to re-register their new device in the MFA portal. Check notification settings "
            "and battery optimization on the new device.",
        ],
        remediation_steps=[
            [
                "Have user navigate to aka.ms/mfasetup to re-register authenticator app",
                "Remove old device registration from the user's MFA methods",
                "Verify push notifications are enabled in phone settings for Authenticator",
                "Check that battery optimization is not blocking Authenticator background activity",
                "Test MFA push notification after re-registration",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-006",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "New hire starting Monday — need full account setup",
            "Provisioning request for new team member",
            "New employee account creation — starting {date}",
        ],
        descriptions=[
            "We have a new analyst joining {department} on Monday. Manager approval has been submitted "
            "in ServiceNow (REQ-{number}). They'll need: Entra ID account, email, Teams, VPN access, "
            "and access to the {department} SharePoint site. Laptop is being shipped separately.",
            "Hi, I'm onboarding a new hire who starts next week. They need the standard {department} "
            "setup: AD account, M365 license, Teams, and access to our department SharePoint. Manager "
            "approval is in ServiceNow. Please prioritize — we need everything ready by day one.",
        ],
        next_best_actions=[
            "Initiate new user provisioning workflow. Verify manager approval in ServiceNow and "
            "create Entra ID account with standard department entitlements.",
        ],
        remediation_steps=[
            [
                "Verify manager approval in ServiceNow request",
                "Create Entra ID account with standard new hire attributes",
                "Assign M365 E5 license and enable Teams",
                "Add user to department-specific security groups",
                "Configure VPN access and distribute credentials securely",
                "Notify hiring manager when account is ready",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-007",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "Directory sync failing — users not showing in Entra ID",
            "Entra Connect sync stopped — 200+ users not synced",
            "AD sync broken since last night's maintenance",
        ],
        descriptions=[
            "Our on-prem AD to Entra ID sync hasn't run since last night. We can see in the Entra "
            "Connect Health portal that the last successful sync was at 11pm. New users created today "
            "in on-prem AD are not appearing in Entra ID. This is blocking onboarding for 3 people.",
            "Entra Connect delta sync is failing with error code 'stopped-server'. The sync appliance "
            "may have gone down during the maintenance window last night. We need this restored ASAP — "
            "password changes aren't syncing either.",
        ],
        next_best_actions=[
            "Check Entra Connect server health and service status. Restart the sync service and "
            "trigger a delta sync to clear the backlog.",
        ],
        remediation_steps=[
            [
                "Check Entra Connect server status and service health",
                "Review Entra Connect Health portal for specific error details",
                "Restart the Azure AD Sync service on the Connect server",
                "Trigger a manual delta sync and monitor completion",
                "Verify new users and password changes are propagating",
                "If server is unresponsive, check VM health and restart if needed",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-008",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Service account expired — automated reports failing",
            "Service principal secret expired — breaking CI/CD pipeline",
            "Automated process stopped — service account credentials expired",
        ],
        descriptions=[
            "Our nightly automated compliance report hasn't run for 3 days. The service account "
            "sa-compliance-reports@contoso.com appears to have an expired password. This account runs "
            "scheduled PowerShell scripts that pull data from Azure SQL. The compliance team needs "
            "these reports for the quarterly audit next week.",
            "The service principal for our CI/CD pipeline has an expired client secret. All deployments "
            "are blocked. The app registration is 'contoso-cicd-prod' in our production tenant. We "
            "need a new secret generated and rotated into Azure DevOps.",
        ],
        next_best_actions=[
            "Reset the service account password or rotate the service principal secret. Update "
            "credentials in the consuming application and verify automated processes resume.",
        ],
        remediation_steps=[
            [
                "Identify the expired credential (password or client secret)",
                "Generate a new password/secret with appropriate expiration policy",
                "Update the credential in the consuming application or key vault",
                "Trigger a test run of the automated process",
                "Verify successful execution and set a reminder for next rotation",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-009",
        category=Category.ACCESS_AUTH,
        priority=Priority.P1,
        assigned_team=Team.IAM,
        needs_escalation=True,
        missing_information=[],
        subjects=[
            "CRITICAL: Conditional access policy blocking all remote users",
            "Everyone working from home can't log in — CA policy issue",
            "Mass lockout — conditional access update broke remote access",
        ],
        descriptions=[
            "Starting at 8am, ALL remote workers are unable to authenticate to any M365 service. "
            "They get 'AADSTS53003: Access has been blocked by conditional access policies.' This "
            "started right after the IAM team pushed a conditional access policy update last night. "
            "Approximately 1,200 remote employees are affected across all three offices. Trading desk "
            "is impacted.",
            "We're getting flooded with calls. Nobody working remotely can sign in — they all get a "
            "conditional access block error. This seems to have started after last night's CA policy "
            "changes. We have ~60% of staff working remote today. Revenue-generating activities are "
            "blocked.",
        ],
        next_best_actions=[
            "Immediately review and roll back the conditional access policy change from last night. "
            "This is a P1 impacting ~1,200 remote workers including trading operations.",
        ],
        remediation_steps=[
            [
                "Identify the conditional access policy change made in the last maintenance window",
                "Roll back the policy to the previous known-good configuration",
                "Verify remote authentication is restored by testing with affected users",
                "Communicate status update to all impacted teams",
                "Conduct root cause analysis on the policy change that caused the outage",
                "Implement policy change review process to prevent recurrence",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-010",
        category=Category.ACCESS_AUTH,
        priority=Priority.P4,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "Guest account request for external auditor",
            "Need to set up B2B guest access for vendor",
            "External contractor needs temporary access",
        ],
        descriptions=[
            "Our external auditors from Deloitte need guest access to our compliance SharePoint site "
            "for the next 4 weeks. There are 3 auditors: {name1}@deloitte.com, {name2}@deloitte.com, "
            "and {name3}@deloitte.com. They only need read access to the Q4 audit documents folder. "
            "No deadline pressure — they start in two weeks.",
            "We're bringing in a vendor consultant who needs B2B guest access to our Azure DevOps "
            "project for 6 months. Their email is {name}@vendor.com. They'll need contributor access "
            "to the 'platform-modernization' repository only. Low priority — they don't start for "
            "another week.",
        ],
        next_best_actions=[
            "Create B2B guest accounts in Entra ID with appropriate scoped access. Set access "
            "expiration per the temporary access policy.",
        ],
        remediation_steps=[
            [
                "Create B2B guest invitations in Entra ID for the external users",
                "Assign read-only access to the specified SharePoint site or repository",
                "Configure access expiration date matching the engagement period",
                "Notify the requesting team when guest accounts are active",
                "Set calendar reminder for access review at expiration",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-011",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "Can't log in after vacation — password expired?",
            "Locked out of everything after 2 weeks off",
            "Back from leave, can't access my account",
        ],
        descriptions=[
            "I just got back from a 3-week vacation and I can't log into anything. When I try my "
            "password it says it's expired. I tried the self-service reset but it says my account "
            "needs admin assistance. Can someone help? I have meetings starting in an hour.",
            "Was out for 2 weeks on parental leave. Now my password doesn't work and when I try to "
            "reset it through the portal, it asks for my MFA but my authenticator app was on my old "
            "phone which I replaced during leave. I'm effectively locked out of everything.",
        ],
        next_best_actions=[
            "Perform admin-assisted password reset and verify MFA registration. Reset MFA methods "
            "if the user's authenticator device has changed.",
        ],
        remediation_steps=[
            [
                "Verify user identity through an alternative channel",
                "Perform admin-initiated password reset in Entra ID",
                "If MFA device has changed, reset MFA registration",
                "Guide user through re-registering authenticator app",
                "Verify user can successfully sign in to all required services",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-012",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.AFFECTED_USERS],
        subjects=[
            "Group policy not applying to new OU",
            "Security group membership changes not propagating",
            "RBAC role assignments failing for the new team",
        ],
        descriptions=[
            "We reorganized the Data Science team into a new OU last week and the group policies "
            "from the parent OU aren't being inherited. The team of 15 people is missing access to "
            "several applications they had before the move. We've verified the GPO links but "
            "something isn't right.",
            "After the Q1 reorg, our RBAC assignments in Azure aren't working for 8 team members who "
            "moved from Engineering to Cloud Infrastructure. Their old role assignments were removed "
            "but the new ones give 'authorization failed' errors on Azure resources.",
        ],
        next_best_actions=[
            "Audit group policy links and RBAC assignments for the reorganized OU. Verify inheritance "
            "settings and re-apply missing role assignments.",
        ],
        remediation_steps=[
            [
                "Review OU structure and GPO inheritance chain",
                "Verify security group memberships were transferred correctly during reorg",
                "Check for any explicit deny policies blocking inheritance",
                "Re-apply missing RBAC role assignments at the correct scope",
                "Test access for affected users after changes propagate",
                "Document the new OU structure and access matrix",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-013",
        category=Category.ACCESS_AUTH,
        priority=Priority.P4,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION],
        subjects=[
            "How do I set up MFA for the first time?",
            "Where do I register my phone for two-factor authentication?",
            "MFA setup instructions needed",
        ],
        descriptions=[
            "New to the company. My manager said I need to set up MFA but I don't know how. The "
            "onboarding guide mentions something about an authenticator app but doesn't give clear "
            "steps. Can someone walk me through it or send me instructions?",
            "I've been meaning to set up MFA for weeks but keep putting it off because the instructions "
            "I found on the intranet seem outdated. Is there a current guide? I'm using an iPhone.",
        ],
        next_best_actions=[
            "Provide user with current MFA registration guide and link to aka.ms/mfasetup. Offer "
            "remote assistance if needed.",
        ],
        remediation_steps=[
            [
                "Send user the current MFA setup guide from the IT knowledge base",
                "Direct user to aka.ms/mfasetup to register authentication methods",
                "Recommend Microsoft Authenticator app as the primary method",
                "Offer a brief remote assistance session if user needs help",
                "Verify MFA is successfully configured after setup",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-014",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.TIMESTAMP, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "VPN asks for credentials every single time",
            "Have to re-authenticate to VPN constantly",
            "VPN token not being cached — need to log in repeatedly",
        ],
        descriptions=[
            "Every time I open my laptop lid or switch networks, the VPN disconnects and asks me to "
            "re-enter my full credentials including MFA. Before the recent policy change it used to "
            "remember me for the whole day. This is happening to others on my team too.",
            "The VPN client now forces re-authentication every time. Even going from wired to Wi-Fi "
            "in the same building triggers a full re-login. It's extremely disruptive — I lose my "
            "connection to everything 5-6 times a day.",
        ],
        next_best_actions=[
            "Review recent conditional access and VPN authentication policy changes. Check if token "
            "lifetime policy was modified, causing frequent re-authentication.",
        ],
        remediation_steps=[
            [
                "Check recent conditional access policy changes affecting VPN authentication",
                "Review token lifetime policy for VPN-related applications",
                "Verify VPN client SSO and token caching configuration",
                "If policy was intentionally tightened, confirm with security team",
                "If unintended, restore previous token lifetime settings",
                "Notify affected users once the issue is resolved",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-015",
        category=Category.ACCESS_AUTH,
        priority=Priority.P1,
        assigned_team=Team.IAM,
        needs_escalation=True,
        missing_information=[],
        subjects=[
            "URGENT: Entra ID showing widespread auth failures across the org",
            "CRITICAL: Authentication service degradation affecting all M365 services",
            "Major Entra ID outage — nobody can sign in",
        ],
        descriptions=[
            "Starting at 7:45 AM EST, we're seeing authentication failures across the organization. "
            "Entra ID sign-in success rate dropped from 99.8% to 42%. All M365 services, VPN, and "
            "internal apps using SSO are affected. Our SRE dashboard shows the issue started after "
            "a scheduled certificate rotation on the Entra Connect servers. All three offices "
            "impacted — approximately 3,000+ users cannot work.",
            "Mass authentication failure in progress. Users across NYC, London, and Singapore "
            "reporting inability to sign into Teams, Outlook, and business applications. The IAM "
            "operations team identified that the SAML signing certificate was rotated to an incorrect "
            "cert. Immediate rollback needed.",
        ],
        next_best_actions=[
            "Immediately roll back the certificate rotation on Entra Connect servers. This is a "
            "P1 service-wide authentication outage affecting 3,000+ users across all offices.",
        ],
        remediation_steps=[
            [
                "Roll back the SAML signing certificate to the previous known-good certificate",
                "Verify authentication success rates are recovering in Entra ID health portal",
                "Clear token caches on federation servers if needed",
                "Send organization-wide communication about the incident and expected resolution",
                "Conduct post-incident review of the certificate rotation process",
                "Implement certificate rotation testing in staging before production",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-016",
        category=Category.ACCESS_AUTH,
        priority=Priority.P4,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.AFFECTED_USERS],
        subjects=[
            "Need shared mailbox for the project team",
            "Request for distribution list creation",
            "New security group needed for Azure resource access",
        ],
        descriptions=[
            "We need a shared mailbox created for our new M&A project team: ma-project-2026@contoso.com. "
            "There will be 6 team members who need access. No rush — the project kicks off next month.",
            "Can we get a new distribution list for the Singapore office IT team? About 12 people. "
            "Name: sg-it-team@contoso.com. Low priority, just want to have it ready for the next "
            "quarter.",
        ],
        next_best_actions=[
            "Create the requested shared mailbox or distribution list in Exchange Online/Entra ID. "
            "Add specified members and configure appropriate access permissions.",
        ],
        remediation_steps=[
            [
                "Create the shared mailbox or distribution list in Exchange Online admin center",
                "Add specified team members with appropriate permissions",
                "Configure send-as and send-on-behalf permissions if needed",
                "Notify the requesting team that the resource is ready",
                "Document in the group catalog for future reference",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-017",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Kerberos authentication failing for on-prem apps",
            "Legacy application can't authenticate — Kerberos errors",
            "NTLM fallback not working for internal application",
        ],
        descriptions=[
            "Our legacy trading platform uses Kerberos authentication and it stopped working after "
            "the domain controller update last night. Users get 'Kerberos pre-authentication failed' "
            "when trying to access the app. About 30 traders in the NYC office are affected and "
            "can't execute trades.",
            "After the weekend DC maintenance, several on-prem applications that use integrated Windows "
            "authentication are failing. Users see NTLM negotiation errors. The apps worked fine on "
            "Friday. Affecting the whole Finance department — 45 people.",
        ],
        next_best_actions=[
            "Check domain controller health and Kerberos ticket granting service. Review recent DC "
            "updates for potential breaking changes to authentication protocols.",
        ],
        remediation_steps=[
            [
                "Check domain controller health and service status",
                "Verify Kerberos KDC service is running on all DCs",
                "Review recent DC updates and patches for known auth issues",
                "Test Kerberos ticket generation with klist on an affected machine",
                "If DC update caused the issue, consult KB for hotfix or rollback",
                "Verify SPN registrations for affected applications",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-018",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.STEPS_TO_REPRODUCE, MissingInfo.DEVICE_INFO],
        subjects=[
            "Passwordless sign-in not working in Edge",
            "FIDO2 key stopped being recognized",
            "Windows Hello for Business enrollment failed",
        ],
        descriptions=[
            "I enrolled my FIDO2 security key last week and it worked fine for a few days. Now when "
            "I tap it during sign-in, nothing happens. The key's LED blinks but the browser doesn't "
            "respond. Works fine on other sites. Only failing on our Entra ID sign-in page.",
            "I'm trying to set up Windows Hello for Business but the enrollment wizard keeps failing "
            "at the PIN creation step. It says 'This request is not supported' — error code 0x80090029. "
            "My laptop was reimaged last week.",
        ],
        next_best_actions=[
            "Verify FIDO2/WHfB policy configuration and check for browser or device compatibility "
            "issues. Re-register the security key if needed.",
        ],
        remediation_steps=[
            [
                "Verify FIDO2 security key or WHfB policy is configured for the user",
                "Check browser version and WebAuthn support",
                "Remove and re-register the FIDO2 key in the security info portal",
                "For WHfB, verify TPM health and check for pending device registration",
                "Test with a different browser or device to isolate the issue",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-019",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=True,
        missing_information=[],
        subjects=[
            "Terminated employee still has active access — security concern",
            "Former employee's account not disabled after offboarding",
            "Ex-contractor can still log in — account was supposed to be deactivated",
        ],
        descriptions=[
            "I just found out that John Smith, who was terminated two weeks ago, still has an active "
            "Entra ID account and active VPN access. He was in the Compliance team and had access to "
            "sensitive regulatory documents. His offboarding request (REQ-8834) was submitted but "
            "apparently never processed. This is a compliance risk.",
            "A contractor who left the company a month ago still has access to our Azure DevOps "
            "repositories and SharePoint sites. They were supposed to be offboarded via the standard "
            "process. We discovered this during our quarterly access review. They had access to "
            "proprietary trading algorithms.",
        ],
        next_best_actions=[
            "Immediately disable the account and revoke all access tokens. Escalate to Security "
            "Operations for access audit during the gap period.",
        ],
        remediation_steps=[
            [
                "Immediately disable the user account in Entra ID",
                "Revoke all active sessions and refresh tokens",
                "Disable VPN and remote access credentials",
                "Audit sign-in and access logs during the gap period",
                "Review offboarding workflow to identify the process failure",
                "Report to Security Operations for compliance documentation",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-020",
        category=Category.ACCESS_AUTH,
        priority=Priority.P4,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Can't remember which MFA method I registered",
            "How do I change my MFA from phone to authenticator app?",
            "Want to add a backup MFA method",
        ],
        descriptions=[
            "I currently use SMS for MFA but I heard the authenticator app is more secure. How do I "
            "switch? I don't want to accidentally lock myself out in the process. Also, can I keep "
            "SMS as a backup?",
            "I want to add a second MFA method as a backup. Currently I only have the authenticator "
            "app set up. If I lose my phone I'd be completely locked out. Can I add a phone number "
            "as a backup method?",
        ],
        next_best_actions=[
            "Direct user to the security info management portal to add or modify MFA methods. "
            "Recommend keeping at least two authentication methods registered.",
        ],
        remediation_steps=[
            [
                "Direct user to aka.ms/mysecurityinfo to manage authentication methods",
                "Guide user to add the preferred new method while keeping the existing one",
                "Verify the new method works with a test sign-in",
                "Recommend keeping at least two registered methods for resilience",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-021",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.ERROR_MESSAGE, MissingInfo.DEVICE_INFO],
        subjects=[
            "Login works on laptop but fails on phone",
            "Can access email on desktop but not mobile",
            "Authentication works on one device but not the other",
        ],
        descriptions=[
            "I can sign into Outlook and Teams on my laptop no problem, but on my phone I get an "
            "authentication error. This started a few days ago. I haven't changed any settings.",
            "My desktop works fine for all apps. But on my personal tablet, I can't sign into the "
            "company portal or Teams anymore. It just shows a red error and kicks me back to the "
            "login screen.",
        ],
        next_best_actions=[
            "Check device compliance status in Intune and conditional access policies that may "
            "block non-compliant or personal devices.",
        ],
        remediation_steps=[
            [
                "Check device compliance status in Intune for the mobile device",
                "Review conditional access policies for device-based restrictions",
                "Verify the device meets minimum OS version requirements",
                "If personal device, check if BYOD policy allows access",
                "Re-enroll the device in Intune if compliance state is stale",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-022",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.AFFECTED_USERS],
        subjects=[
            "Token lifetime changed — breaking automated systems",
            "OAuth token expiration policy change broke our integrations",
            "Access tokens expiring too quickly after policy update",
        ],
        descriptions=[
            "Our automated trading data feeds started failing intermittently after the token "
            "lifetime policy was changed last Tuesday. The tokens now expire after 1 hour instead "
            "of 8 hours. Our feed applications weren't designed for frequent re-authentication "
            "and are dropping data during token refresh. This affects downstream analytics.",
            "Our internal API integrations are breaking because access tokens are expiring much "
            "faster than before. We have about 12 service-to-service integrations that depend on "
            "longer-lived tokens. The policy change wasn't communicated to application teams.",
        ],
        next_best_actions=[
            "Review the recent token lifetime policy change and assess impact on automated systems. "
            "Consider creating an exception policy for service accounts while applications are updated.",
        ],
        remediation_steps=[
            [
                "Identify the specific token lifetime policy change",
                "Assess which applications and service accounts are affected",
                "Create a temporary exception policy for critical service accounts",
                "Communicate the policy change to all application owners",
                "Work with app teams to implement proper token refresh logic",
                "Gradually transition service accounts to the new policy",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-023",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Prompted for MFA on every browser tab",
            "MFA challenge appearing too frequently — every 10 minutes",
            "Constant MFA popups disrupting my workflow",
        ],
        descriptions=[
            "Since the security update last week, I'm getting MFA challenges constantly. Every time "
            "I open a new browser tab to a different M365 app, I have to re-authenticate with MFA. "
            "It used to remember me for the day. I'm approving MFA prompts 40-50 times per day now.",
            "MFA is way too aggressive. I get prompted when I switch between Teams and Outlook, "
            "when I open SharePoint, basically every 5-10 minutes. This can't be right. My "
            "productivity has dropped significantly.",
        ],
        next_best_actions=[
            "Review sign-in frequency and persistent browser session settings in conditional access. "
            "Check if recent policy changes reduced the authentication session timeout.",
        ],
        remediation_steps=[
            [
                "Review conditional access sign-in frequency policies",
                "Check persistent browser session configuration",
                "Verify the user's device is joined or registered in Entra ID",
                "Check if device-based trust reduces MFA frequency for compliant devices",
                "Adjust sign-in frequency if the current setting is overly aggressive",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-024",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Can't access shared drive since last week",
            "Lost access to team file share after department move",
            "Permissions removed from network drive — need restoration",
        ],
        descriptions=[
            "I used to have access to the \\\\fs01\\compliance-reports share but since I moved from "
            "Compliance to Risk Management, my access was revoked. I still need it for the transition "
            "period — my old manager confirmed. Can you restore my access?",
            "After the team restructuring, I can't access the Marketing shared folder anymore. I get "
            "'Access Denied' when I try to open it. My new manager says I should still have access "
            "since I'm working on cross-team projects.",
        ],
        next_best_actions=[
            "Verify access request approval from the appropriate manager and add the user to the "
            "correct security group for the requested file share.",
        ],
        remediation_steps=[
            [
                "Confirm access approval from the data owner or manager",
                "Identify the security group controlling file share access",
                "Add the user to the appropriate security group",
                "Wait for group membership to propagate (up to 1 hour)",
                "Verify user can access the file share successfully",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-025",
        category=Category.ACCESS_AUTH,
        priority=Priority.P1,
        assigned_team=Team.IAM,
        needs_escalation=True,
        missing_information=[MissingInfo.AFFECTED_USERS],
        subjects=[
            "EMERGENCY: MFA service down — all logins failing",
            "Azure MFA service outage — widespread impact",
            "MFA completely non-functional — critical business impact",
        ],
        descriptions=[
            "Azure MFA is completely down. No one can complete MFA challenges — push notifications "
            "aren't being delivered, TOTP codes are being rejected, and phone calls aren't going "
            "through. This started at 6:15 AM and is affecting all three offices. The trading floor "
            "cannot operate. Our backup MFA method (SMS) is also failing.",
            "Complete MFA outage for the past 45 minutes. Azure Service Health shows a known issue "
            "with the MFA service in our region (East US). Approximately 2,500 users cannot "
            "authenticate. Trading operations are at a standstill. We need to either get MFA "
            "restored or implement a temporary bypass for critical users.",
        ],
        next_best_actions=[
            "Implement emergency conditional access policy to temporarily bypass MFA for critical "
            "business functions while coordinating with Microsoft support on the MFA service outage.",
        ],
        remediation_steps=[
            [
                "Verify Azure MFA service status in Azure Service Health",
                "Open a Sev-A support case with Microsoft for the MFA outage",
                "Implement emergency CA policy to bypass MFA for critical user groups",
                "Enable temporary alternative authentication for trading floor users",
                "Monitor Azure Service Health for resolution",
                "Remove emergency bypass policies once MFA service is restored",
                "Document the incident and review business continuity procedures",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-026",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.PREVIOUS_TICKET_ID, MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "Login issue is back again — same problem as last time",
            "Recurring authentication failure — had a ticket for this before",
            "Same login error I reported last month — still not fixed",
        ],
        descriptions=[
            "I'm getting the same login failure I reported a few weeks ago. IT fixed it last time but "
            "the issue has come back. I can't remember the ticket number but it was sometime in March. "
            "The login just spins and then times out. I'm not sure if it's my password, MFA, or "
            "something else — I just know the sign-in page won't let me through. I'm in the London "
            "office, Fixed Income team, and I have a client call in an hour.",
            "This is the third time I've had this authentication issue. There's a previous ticket "
            "somewhere in the system — the last tech said it was a known problem with my account. "
            "I keep getting 'Authentication failed' but no details about what specifically is failing. "
            "Can someone look up my history and figure out the root cause this time?",
        ],
        next_best_actions=[
            "Search for the user's previous tickets to identify recurring patterns. Determine the "
            "specific authentication method failing and apply a permanent fix.",
        ],
        remediation_steps=[
            [
                "Search the ticketing system for the user's prior authentication-related tickets",
                "Review the previous resolution to identify if the same root cause has recurred",
                "Check Entra ID sign-in logs to identify the specific authentication failure reason",
                "Determine which authentication method is failing (password, MFA push, TOTP, etc.)",
                "Apply a permanent fix based on the recurring pattern (e.g., re-register MFA, fix CA policy)",
                "Document the root cause linkage between the old and new tickets",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-027",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.CONTACT_INFO, MissingInfo.DEVICE_INFO],
        subjects=[
            "Remote worker can't authenticate — need callback",
            "Working from a client site and can't log in — no way to reach me easily",
            "Traveling employee locked out — please help urgently",
        ],
        descriptions=[
            "I'm at a client site in Tokyo and I can't authenticate to any of our systems. My laptop "
            "keeps saying my credentials are expired but I changed my password before I left. I don't "
            "have reliable phone service here so calling my usual number won't work. I managed to send "
            "this from the client's guest WiFi on my personal phone. Please help — I have a "
            "presentation in two hours.",
            "I'm working remotely from a rural area with very limited cell coverage and can't log in. "
            "MFA push notifications aren't coming through and I can't receive SMS codes either. I "
            "need someone to help me get authenticated but I'm not sure how you can reach me since my "
            "normal phone isn't working well out here. Email is the only reliable way to contact me "
            "right now.",
        ],
        next_best_actions=[
            "Obtain an alternate contact method for the user. Issue a temporary access pass or "
            "alternative MFA method that works without cellular connectivity.",
        ],
        remediation_steps=[
            [
                "Obtain a working contact method (personal email, Teams chat, client site phone)",
                "Verify the user's identity through an alternate channel",
                "Issue a Temporary Access Pass (TAP) in Entra ID for immediate access",
                "Guide the user to set up an offline MFA method (TOTP authenticator app)",
                "Confirm the user can authenticate and access required systems",
                "Schedule a follow-up to restore standard MFA when connectivity improves",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-028",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "SSO broken across multiple applications",
            "Single sign-on fails for several apps but works for others",
            "SSO not working — have to log in separately to every app",
        ],
        descriptions=[
            "SSO has stopped working for me across multiple apps. I can get into Outlook and Teams "
            "fine but when I try to access Workday, ServiceNow, or Salesforce through the SSO portal, "
            "I get redirected back to a login page. I don't know what SSO method these apps use — I "
            "just usually click the tile and it works. This has been going on since yesterday "
            "afternoon. Singapore office, Wealth Management.",
            "My single sign-on is broken for a bunch of apps. Some work, some don't. The ones that "
            "don't work just loop back to the sign-in page or show a vague 'authentication error'. "
            "I'm not sure if these apps use SAML or something else — they've always just worked "
            "seamlessly until now. I need access to at least five different systems for my daily work.",
        ],
        next_best_actions=[
            "Check the SSO configuration for the failing applications in Entra ID. Identify whether "
            "the issue is SAML, OIDC, or WS-Fed specific and review recent changes to app registrations.",
        ],
        remediation_steps=[
            [
                "Identify which applications are failing SSO and which protocol they use (SAML, OIDC, WS-Fed)",
                "Check Entra ID enterprise application sign-in logs for error details",
                "Review recent changes to app registrations or conditional access policies",
                "Test SSO for each failing app and capture the specific error codes",
                "Repair the SSO configuration (certificate renewal, endpoint update, or claim rule fix)",
                "Verify the user can access all affected applications via SSO",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-029",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.CONTACT_INFO, MissingInfo.PREVIOUS_TICKET_ID],
        subjects=[
            "Account issue called in from front desk phone",
            "Someone called in about an account lockout — no callback number",
            "Account disabled — employee called from a colleague's phone",
        ],
        descriptions=[
            "An employee called in from the front desk phone to report that their account has been "
            "disabled. They said they had a ticket about this before but couldn't remember the number. "
            "They hung up before I could get a callback number. The employee's name is in the notes "
            "but I have no way to reach them directly to verify their identity or walk them through "
            "the fix. They're apparently in the NYC office.",
            "I received a voicemail about an account lockout from someone who called from a shared "
            "phone in a conference room. They mentioned this happened once before and was fixed by "
            "the IAM team. They didn't leave a direct number or extension to call back, just their "
            "name and that they're on the compliance team. I need to find them to resolve this.",
        ],
        next_best_actions=[
            "Look up the user in the directory to find their contact information and previous tickets. "
            "Reach out via Teams or manager to verify identity before making account changes.",
        ],
        remediation_steps=[
            [
                "Look up the user in the corporate directory for direct contact info",
                "Search the ticketing system for any previous tickets under their name",
                "Reach out to the user via Teams chat or their manager to verify identity",
                "Once identity is verified, investigate the account lockout or disabled state",
                "Re-enable or unlock the account and resolve the root cause",
                "Update the ticket with verified contact information for follow-up",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-030",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
        subjects=[
            "Passwordless login stopped working — not sure which method I use",
            "Can't sign in without a password anymore — passwordless broken",
            "FIDO key or Windows Hello not working — can't tell which is failing",
        ],
        descriptions=[
            "I've been using passwordless login for months and it suddenly stopped working. I'm not "
            "sure exactly which method I was using — I either tap my security key or use the fingerprint "
            "reader, whatever pops up. Now neither seems to work but I can't describe the exact error "
            "because it just flashes briefly and goes back to the login screen. I didn't think to take "
            "a screenshot. NYC office, M&A team.",
            "My passwordless sign-in is broken. I used to just look at the camera or touch the "
            "fingerprint sensor and I was in. Now it prompts me for something but then fails. I'm not "
            "technical enough to know if it's Windows Hello, FIDO2, or what — it was just set up for "
            "me during onboarding. I don't have a screenshot of the error because it disappears too "
            "quickly. Can someone help me figure out what's going on?",
        ],
        next_best_actions=[
            "Check the user's registered authentication methods in Entra ID to identify the "
            "passwordless method in use. Re-register the credential if it has become corrupted.",
        ],
        remediation_steps=[
            [
                "Check the user's registered authentication methods in Entra ID (FIDO2, WHfB, phone sign-in)",
                "Review Entra ID sign-in logs to identify which method was attempted and the failure reason",
                "Ask the user to reproduce the error and capture a screenshot or photo of the message",
                "Re-register the passwordless credential (re-enroll FIDO2 key or reset Windows Hello)",
                "Test the passwordless sign-in flow end-to-end with the user",
                "Set up a backup authentication method in case the primary fails again",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-031",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[
            MissingInfo.AUTHENTICATION_METHOD,
            MissingInfo.PREVIOUS_TICKET_ID,
            MissingInfo.REPRODUCTION_FREQUENCY,
        ],
        subjects=[
            "SAML SSO failures after IdP certificate rotation — happening on and off",
            "Intermittent SSO login errors since certificate change on our IdP",
            "SSO broken after IdP cert renewal — some users affected, not all",
        ],
        descriptions=[
            "Since our identity provider certificate was rotated last Thursday, a number of users in the "
            "London office are reporting intermittent SAML SSO failures when signing into our internal "
            "finance portal. The error is not consistent — it seems to work sometimes and fail other "
            "times. I filed a ticket about this last week but I can't find the reference number. I'm not "
            "sure if we're using SAML 2.0 or WS-Fed for this particular app.",
            "After our IdP certificate renewal, SSO logins to several Contoso Financial Services apps "
            "are failing sporadically. Some users can log in on the first try, others get a certificate "
            "validation error after multiple attempts. We reported a similar issue a few months ago when "
            "the last rotation happened but I don't have the old ticket number handy. Not sure how often "
            "it reproduces — maybe 30-40% of the time.",
        ],
        next_best_actions=[
            "Verify the updated IdP certificate has been imported into the Entra ID SAML configuration "
            "for the affected application. Check whether both old and new certificates are active during "
            "the rollover window.",
            "Look up the user's previous ticket to identify if this is a recurring issue from the last "
            "certificate rotation. Compare the SAML configuration and federation metadata between the "
            "two incidents.",
        ],
        remediation_steps=[
            [
                "Identify the SAML or WS-Fed federation protocol in use for the affected application",
                "Verify the new IdP signing certificate is uploaded in the Entra ID enterprise app SSO config",
                "Check if the old certificate needs to remain active during a rollover period",
                "Update the federation metadata URL or manually replace the certificate if needed",
                "Test SSO login with an affected user and confirm consistent success",
                "Search for the previous ticket to document recurrence and update the knowledge base",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-032",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.SCREENSHOT_OR_ATTACHMENT, MissingInfo.CONTACT_INFO, MissingInfo.DEVICE_INFO],
        subjects=[
            "External contractor can't access Contoso portal from personal laptop",
            "BYOD access issue — contractor locked out of partner portal",
            "Contractor unable to reach internal apps on their own device",
        ],
        descriptions=[
            "One of our external contractors from Adatum Consulting is unable to access the Contoso "
            "partner portal from their personal laptop. They say they see an error page but didn't "
            "capture a screenshot. I don't have their direct contact info or their company IT team's "
            "details to troubleshoot further. They mentioned they were able to access it last week.",
            "A contractor working with our risk analytics team reports they're blocked from accessing "
            "the partner portal on their personal device. They get redirected to some kind of compliance "
            "error but couldn't describe it exactly and didn't take a screenshot. I'm not sure who their "
            "IT admin is at their company, and they didn't leave a callback number. The device is "
            "unmanaged as far as I know.",
            "External consultant from Adatum can't log into our collaboration portal on their BYOD "
            "laptop. They emailed us saying it shows some access denied message. No screenshot was "
            "provided. We need their company IT contact to check device compliance status on their end.",
        ],
        next_best_actions=[
            "Check Conditional Access policies for BYOD and guest user scenarios. Request a screenshot "
            "of the error and the contractor's direct contact information or their IT admin's details.",
            "Review Entra ID sign-in logs for the contractor's guest account to identify the specific "
            "Conditional Access policy blocking access. Obtain their contact info for follow-up.",
        ],
        remediation_steps=[
            [
                "Look up the contractor's guest account in Entra ID and review recent sign-in logs",
                "Identify the Conditional Access policy that is blocking the unmanaged device",
                "Request a screenshot of the error and direct contact info from the contractor",
                "Contact the contractor's company IT admin to verify device compliance posture",
                "Add a CA policy exception for the partner portal or require MAM enrollment for BYOD",
                "Confirm the contractor can access the portal and document the resolution",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-033",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
        subjects=[
            "Smartcard authentication failing at secure workstation",
            "PIV card login not working — getting certificate error at kiosk",
            "Can't log in with smartcard at restricted terminal in DC office",
        ],
        descriptions=[
            "I'm in the Washington DC office and I can't log into the secure workstation using my "
            "smartcard. It prompts me to insert the card, I enter my PIN, and then it shows a brief "
            "error about a certificate problem before kicking me back to the login screen. I didn't "
            "get a screenshot because it disappears quickly. I'm not sure if this is a PIV card, CAC, "
            "or a Contoso-issued smartcard — it was given to me by building security during onboarding.",
            "My smartcard-based login to the secure terminal in the trading floor area has stopped "
            "working. I swipe or insert my card and enter the PIN, and it just fails with some kind "
            "of certificate trust error. The error flashes too fast to read or capture. I don't know "
            "the specific type of card — I just know it's the one issued for accessing restricted "
            "workstations. This started happening after the weekend.",
        ],
        next_best_actions=[
            "Identify the smartcard type (PIV, CAC, or virtual smartcard) and check the certificate "
            "chain trust on the workstation. Verify the user's certificate has not expired or been "
            "revoked.",
            "Check the workstation's certificate trust store and CRL/OCSP responder connectivity. Ask "
            "the user to capture a phone photo of the error message on next attempt.",
        ],
        remediation_steps=[
            [
                "Determine the smartcard type by inspecting the user's account or asking security team",
                "Check the user's smartcard certificate expiration and revocation status in the CA",
                "Verify the workstation trusts the issuing CA and intermediate certificates",
                "Test CRL and OCSP endpoint connectivity from the secure workstation",
                "Re-issue the smartcard certificate if expired or re-enroll if corrupted",
                "Test smartcard login end-to-end and ask user to capture the error if it recurs",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-034",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[
            MissingInfo.PREVIOUS_TICKET_ID,
            MissingInfo.REPRODUCTION_FREQUENCY,
            MissingInfo.ERROR_MESSAGE,
        ],
        subjects=[
            "OAuth token refresh failing for our API integration — intermittent",
            "API calls returning 401 after token expiry — refresh flow broken",
            "Service integration OAuth tokens not refreshing — sporadic failures",
        ],
        descriptions=[
            "Our trading platform API integration with the Contoso identity service has started failing "
            "intermittently when refreshing OAuth tokens. The refresh call sometimes returns a 401 and "
            "other times works fine. I don't have the exact error body because our logging wasn't "
            "capturing the response payload at the time. We had a similar token refresh issue about two "
            "months ago that was resolved by your team but I can't locate that ticket number.",
            "The OAuth 2.0 refresh token flow for our risk reporting service is intermittently returning "
            "errors. It's been happening for about three days but we're not sure of the exact failure "
            "rate — maybe a few times per hour. We opened a ticket for a nearly identical issue earlier "
            "this quarter but I don't have the reference. The error message in our logs just says "
            "'unauthorized' without further detail.",
        ],
        next_best_actions=[
            "Check the OAuth app registration in Entra ID for token lifetime policies and refresh token "
            "validity. Review Entra ID sign-in and audit logs for the service principal to identify the "
            "root cause of intermittent failures.",
            "Search for the previous related ticket to check if the same root cause applies. Request "
            "the full error response body and review the app's token configuration.",
        ],
        remediation_steps=[
            [
                "Identify the app registration and service principal in Entra ID for the integration",
                "Review token lifetime and refresh token policies applied to the app",
                "Check Entra ID sign-in logs for the service principal to find detailed error codes",
                "Request the team enable verbose logging to capture the full error response body",
                "Rotate the client secret or certificate if credentials have expired or been revoked",
                "Test the token refresh flow and monitor for recurrence over 24 hours",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-035",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.CONTACT_INFO, MissingInfo.PREVIOUS_TICKET_ID],
        subjects=[
            "Bulk account creation request for new hires starting next month",
            "Need 25 new accounts provisioned for incoming analyst class",
            "HR requesting batch provisioning of accounts for new hire cohort",
        ],
        descriptions=[
            "HR has requested that we create accounts for approximately 25 new hires joining the "
            "investment banking analyst program next month. I received the request forwarded from "
            "someone in HR but I'm not sure who the actual point of contact is to verify the list and "
            "confirm start dates. I think a similar bulk request was handled a few months ago and there "
            "may have been a ticket with a CSV template we used, but I can't find it.",
            "We need to provision user accounts, mailboxes, and group memberships for a cohort of new "
            "analysts starting in the Chicago and NYC offices. The request came through our HR portal "
            "but the submitter didn't include a direct contact for validation. We've done this before "
            "for a previous cohort and I believe there was a standardized process documented in an "
            "older ticket, but I don't have the reference number to look it up.",
            "Incoming batch of new hires for Contoso Financial Services needs accounts set up across "
            "AD, Entra ID, Exchange, and our finance applications. HR sent a spreadsheet but didn't "
            "include who to reach out to for clarifications on role assignments or start dates. We "
            "handled a similar request last quarter — is there a previous ticket we can reference?",
        ],
        next_best_actions=[
            "Obtain the HR contact responsible for the new hire list to verify names, start dates, and "
            "role assignments. Search for previous bulk provisioning tickets to reuse the established "
            "process and CSV template.",
            "Reach out to the HR department to identify the point of contact for this cohort. Look up "
            "prior bulk account creation tickets for the provisioning checklist and template.",
        ],
        remediation_steps=[
            [
                "Contact HR to identify the responsible person and obtain a verified new hire list",
                "Search for previous bulk provisioning tickets to retrieve the CSV template and process",
                "Validate the new hire list — names, start dates, office locations, and role assignments",
                "Create accounts in AD and Entra ID using the established bulk provisioning workflow",
                "Provision mailboxes, group memberships, and application access per role",
                "Send welcome emails with credentials and confirm with the HR contact that all accounts are ready",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-036",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "MFA not working on my mobile app — can't approve sign-in",
            "Authenticator app on phone won't complete MFA challenge",
            "Mobile MFA broken — push notifications not coming through",
        ],
        descriptions=[
            "I can't complete the MFA challenge when signing into my Contoso account. The Microsoft "
            "Authenticator app on my phone either doesn't receive the push notification or shows an "
            "error when I try to approve it. I've tried over WiFi and cellular. I'm not sure if this "
            "is a problem with my phone or with my account's MFA configuration — I recently got a new "
            "phone and I thought I migrated the authenticator correctly. I don't know which MFA method "
            "my account is set to use as the default.",
            "My multi-factor authentication has stopped working on my mobile device. When I log in on "
            "my laptop, I get the MFA prompt but the approval request never reaches my phone app. I "
            "tried reinstalling the authenticator but the issue persists. I'm not sure if the problem "
            "is the app registration on my device or something with my Entra ID MFA settings — I don't "
            "know whether my account uses push notifications, TOTP codes, or SMS as the primary method.",
        ],
        next_best_actions=[
            "Collect the user's device details (phone model, OS version) and determine the configured "
            "MFA method in Entra ID. Check if the authenticator app registration is still valid after "
            "the device change.",
            "Verify the user's MFA registration status in Entra ID and identify the primary "
            "authentication method. Check for recent device changes that may have invalidated the "
            "authenticator enrollment.",
        ],
        remediation_steps=[
            [
                "Check the user's MFA registration in Entra ID to identify the configured methods",
                "Determine if the authenticator app registration was properly migrated to the new device",
                "Collect device details — phone model, OS version, and authenticator app version",
                "If the registration is stale, have the user re-register the authenticator app"
                " via aka.ms/mysecurityinfo",
                "Test the MFA flow end-to-end and confirm push notifications are received",
                "Set up a backup MFA method (phone call or FIDO2 key) to prevent future lockouts",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-037",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "SSO not working for Salesforce — login fails with federation error",
            "Can't sign into Salesforce via single sign-on",
            "Salesforce SSO broken — redirects to error page after login",
        ],
        descriptions=[
            "When I try to log into Salesforce using our company SSO, I get redirected through the "
            "Contoso Entra ID login page, authenticate successfully, and then Salesforce shows a "
            "federation error page instead of letting me in. This started after the Salesforce team "
            "mentioned they updated something on their side, but I'm not sure what version of "
            "Salesforce we're running. I didn't copy the exact error message because I assumed it "
            "was a temporary glitch, but it's been happening all day. Other SaaS apps with SSO work "
            "fine — it's just Salesforce.",
            "Our Salesforce single sign-on integration broke sometime this morning. I can authenticate "
            "through the Contoso identity provider but the SAML assertion seems to fail on the "
            "Salesforce side — I land on an error page instead of my dashboard. I don't have the "
            "exact error text or the Salesforce instance version. Other SAML-based apps like "
            "ServiceNow and Workday work normally, so the issue seems specific to the Salesforce SSO "
            "configuration or their recent changes.",
        ],
        next_best_actions=[
            "Check the Entra ID Enterprise Application SSO configuration for Salesforce and review "
            "the SAML assertion attributes. Ask the user to capture the exact error message from "
            "the Salesforce error page.",
            "Review the Entra ID SAML signing certificate and claim mappings for the Salesforce app "
            "registration. Determine if Salesforce made federation metadata changes that need to be "
            "reflected in Entra ID.",
        ],
        remediation_steps=[
            [
                "Ask the user to capture the full error message from the Salesforce federation error page",
                "Check the Entra ID Enterprise Application SAML configuration for Salesforce",
                "Review the SAML signing certificate expiration and claim/attribute mappings",
                "Contact the Salesforce admin to determine what changes were made and the current instance version",
                "Compare the Entra ID federation metadata with what Salesforce expects",
                "Update the SAML configuration if mismatches are found and test SSO end-to-end",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="aa-038",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.CONTACT_INFO, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "New contractor needs access to network share and application portal",
            "Contractor onboarding — requesting file share and portal access",
            "Set up access for new external contractor — shared drive and app portal",
        ],
        descriptions=[
            "We have a new contractor from Woodgrove Consulting starting next week who needs access to "
            "both our finance department's network share (\\\\contoso-fs01\\finance) and the internal "
            "project management portal. The request came through the hiring manager but they didn't "
            "include the contractor's direct contact information for account setup verification. I'm "
            "not sure which environment this needs to be set up in — we have both a staging and "
            "production instance of the portal, and the file share may have different permission tiers "
            "depending on the project.",
            "A new external contractor needs to be provisioned with access to our shared drive for "
            "project documents and the Contoso application portal for time tracking and deliverables. "
            "The contractor's manager submitted the request but didn't provide the contractor's phone "
            "number or personal email for identity verification. I also need clarification on which "
            "environment — the contractor may only need the sandbox portal for the first month, or they "
            "might need full production access. The network share permissions depend on which project "
            "team they're joining.",
        ],
        next_best_actions=[
            "Obtain the contractor's direct contact information for identity verification and account "
            "setup. Clarify the specific environment (staging vs. production) and permission level "
            "needed for both the network share and application portal.",
            "Contact the hiring manager to get the contractor's personal email or phone number. "
            "Determine the exact environment and access scope before provisioning accounts.",
        ],
        remediation_steps=[
            [
                "Contact the hiring manager to obtain the contractor's direct contact details",
                "Verify the contractor's identity and confirm the engagement start date",
                "Clarify the target environment (staging vs. production) and required permission levels",
                "Create the contractor's account in Entra ID with the appropriate external user type",
                "Grant access to the network share with the correct permission tier for their project",
                "Provision application portal access in the confirmed environment"
                " and send credentials to the contractor",
            ],
        ],
    )
)
