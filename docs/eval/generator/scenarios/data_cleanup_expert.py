"""Expert data cleanup edge-case scenario definitions.

Covers scenarios not in the base or advanced data_cleanup modules: GraphQL
response dumps, Kubernetes multi-container pod logs, double-escaped JSON
configuration strings, webpack bundler errors, PowerShell error streams,
Windows Registry exports, PEM certificate chains, systemd journal floods,
mixed CJK/Latin text, full HTTP response dumps, nested MIME multipart,
git commit history, Terraform plan output, DNS zone files, and packet
capture text output.
"""

from generator.models import Scenario

SCENARIOS: list[Scenario] = [
    # ──────────────────────────────────────────────────────────────────
    # 1. GraphQL nested response dump in ticket body
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-graphql-response",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["environment_details", "steps_to_reproduce"],
        subjects=[
            "Internal API returning malformed GraphQL response — pasted below",
            "GraphQL endpoint returning unexpected nested data — see dump",
        ],
        descriptions=[
            "Hi team,\n\nOur internal product catalog API started returning malformed "
            "GraphQL responses this morning. Here's the full response I captured from "
            "our monitoring dashboard:\n\n"
            '{"data":{"products":{"edges":[{"node":{"__typename":"Product",'
            '"id":"prod-8a7b","name":"Enterprise License","pricing":{'
            '"__typename":"PricingTier","monthly":299.99,"annual":2999.90,'
            '"currency":"USD"},"availability":{"__typename":"StockStatus",'
            '"inStock":true,"regions":{"edges":[{"node":{"__typename":"Region",'
            '"code":"US-EAST","warehouse":"WH-042","units":1847}},{"node":{'
            '"__typename":"Region","code":"EU-WEST","warehouse":"WH-019",'
            '"units":0}}],"pageInfo":{"hasNextPage":true,"endCursor":"abc123"}}}}},'
            '{"node":{"__typename":"Product","id":"prod-9c2d","name":null,'
            '"pricing":null,"availability":null}}],"pageInfo":{'
            '"hasNextPage":false,"endCursor":"def456"}}},'
            '"errors":[{"message":"Cannot resolve field \'deprecated_sku\' on type '
            'Product","locations":[{"line":12,"column":5}],'
            '"path":["products","edges",1,"node","deprecated_sku"],'
            '"extensions":{"code":"FIELD_NOT_FOUND"}}]}\n\n'
            "The second product node is coming back as all nulls, and there's a "
            "field resolution error. This is blocking our pricing display on the "
            "internal portal. Started after last night's deployment.",
            "GraphQL API for the product catalog is returning deeply nested responses "
            "with errors. The response includes __typename fields, pagination cursors, "
            "and partial null data. Our frontend can't parse it properly. "
            "Query was: query { products(first: 50) { edges { node { id name "
            "pricing { monthly annual } availability { inStock regions { edges "
            "{ node { code warehouse units } } pageInfo { hasNextPage } } } } } "
            "pageInfo { hasNextPage endCursor } } }\n\n"
            "Response has errors array with FIELD_NOT_FOUND for deprecated_sku.",
        ],
        next_best_actions=[
            "Investigate the GraphQL schema change from last night's deployment — "
            "the deprecated_sku field was likely removed without updating all queries.",
            "Review the product catalog API deployment and fix the null product node "
            "and deprecated field reference in the GraphQL schema.",
        ],
        remediation_steps=[
            [
                "Review the latest deployment changelog for schema changes to the product catalog API",
                "Identify which fields were removed or renamed in the GraphQL schema",
                "Update all client queries to remove references to deprecated_sku",
                "Investigate why the second product node returns all nulls",
                "Deploy the fix and verify the frontend pricing display works correctly",
            ],
        ],
        tags=["data-cleanup", "graphql", "api-response"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 2. Kubernetes multi-container pod logs (OOMKilled)
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-k8s-oomkilled",
        category="Software & Applications",
        priority="P1",
        assigned_team="Enterprise Applications",
        needs_escalation=True,
        missing_information=["environment_details", "timestamp"],
        subjects=[
            "CRITICAL: Order processing pods keep crashing — OOMKilled",
            "Production Kubernetes pods restarting — out of memory errors",
        ],
        descriptions=[
            "URGENT — our order-processing pods in the production Kubernetes cluster "
            "keep getting OOMKilled. This is affecting live customer orders.\n\n"
            "kubectl get pods -n order-processing:\n"
            "NAME                              READY   STATUS             RESTARTS   AGE\n"
            "order-svc-7d8f9b6c4-abc12         1/2     OOMKilled          14         2h\n"
            "order-svc-7d8f9b6c4-def34         0/2     CrashLoopBackOff   22         2h\n"
            "order-svc-7d8f9b6c4-ghi56         2/2     Running            0          5m\n"
            "order-worker-5c4a3b2d1-jkl78      1/1     Running            3          2h\n"
            "order-db-proxy-6e7f8a9b0-mno90    1/1     Running            0          5d\n\n"
            "kubectl describe pod order-svc-7d8f9b6c4-abc12 -n order-processing:\n"
            "...\n"
            "Containers:\n"
            "  order-api:\n"
            "    State:       Waiting (CrashLoopBackOff)\n"
            "    Last State:  Terminated (OOMKilled, exit code 137)\n"
            "    Resources:\n"
            "      Limits:  memory: 512Mi, cpu: 500m\n"
            "      Requests: memory: 256Mi, cpu: 250m\n"
            "  order-sidecar:\n"
            "    State:       Running\n"
            "    Resources:\n"
            "      Limits:  memory: 128Mi\n\n"
            "Events:\n"
            "  Warning  OOMKilling  2m ago   kubelet  Container order-api exceeded memory limit\n"
            "  Normal   Pulling     1m ago   kubelet  Pulling image order-api:v2.4.1\n"
            "  Warning  BackOff     30s ago  kubelet  Back-off restarting failed container\n\n"
            "This started right after we deployed v2.4.1 of the order-api. The previous "
            "version v2.3.8 was stable for weeks.",
            "Production order processing is down. Kubernetes pods are in OOMKilled / "
            "CrashLoopBackOff state. The namespace order-processing shows multiple "
            "pod restarts. Container order-api has memory limit 512Mi but is being "
            "terminated with exit code 137. Deployed v2.4.1 today — suspect memory leak "
            "in the new version.",
        ],
        next_best_actions=[
            "Roll back order-api from v2.4.1 to v2.3.8 immediately to restore order "
            "processing, then investigate the memory leak in the new version.",
            "Increase memory limits temporarily and schedule a rollback of order-api "
            "v2.4.1 to stabilize the production order processing pipeline.",
        ],
        remediation_steps=[
            [
                "Immediately roll back order-api from v2.4.1 to v2.3.8 in the order-processing namespace",
                "Monitor pod stability after rollback using kubectl get pods -w",
                "Analyze memory profiling data from v2.4.1 to identify the memory leak",
                "Review the v2.4.1 changelog for changes that could cause increased memory usage",
                "Fix the memory leak, test in staging with appropriate load testing, then redeploy",
            ],
        ],
        tags=["data-cleanup", "kubernetes", "oom-killed", "container-logs"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 3. Double-escaped JSON configuration strings
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-double-escaped-json",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "environment_details"],
        subjects=[
            "Config service returning double-escaped JSON — apps failing to parse",
            "Application config endpoint returns mangled JSON with extra escaping",
        ],
        descriptions=[
            "Our config service is returning double-escaped JSON that downstream apps "
            "can't parse. Here's what we're getting:\n\n"
            '{"config":"{\\"database\\":{\\"host\\":\\"sqlprod-01.contoso.com\\",'
            '\\"port\\":5432,\\"name\\":\\"orders_db\\",\\"pool\\":{'
            '\\"min\\":5,\\"max\\":20}},\\"cache\\":{\\"host\\":'
            '\\"redis-01.contoso.com\\",\\"ttl\\":300},'
            '\\"features\\":{\\"newCheckout\\":true,'
            '\\"betaSearch\\":false}}"}\n\n'
            "When we try to parse config.database.host, we get undefined because the "
            "entire config value is a string with escaped quotes instead of a proper "
            "nested object. The old config service returned:\n\n"
            '{"config":{"database":{"host":"sqlprod-01.contoso.com",...}}}\n\n'
            "This broke after the config service was migrated to the new API gateway "
            "last week. Looks like the gateway is double-serializing the JSON response.",
            "Config API returning escaped JSON strings instead of proper nested objects. "
            'The response body contains \\" sequences throughout. Downstream apps get '
            "parse errors. Started after API gateway migration. Need the gateway team "
            "to fix the serialization.",
        ],
        next_best_actions=[
            "Investigate the API gateway serialization — the config service response "
            "is being double-serialized, converting nested JSON into escaped strings.",
            "Check the API gateway configuration for the config service route — the "
            "response body is being string-escaped when it should be passed through.",
        ],
        remediation_steps=[
            [
                "Identify the API gateway route configuration for the config service endpoint",
                "Check if the gateway is applying a response transformation that double-serializes JSON",
                "Fix the gateway route to pass through the config service response without re-serialization",
                "Test the config endpoint with a curl request to verify proper JSON nesting",
                "Notify downstream application teams that the fix has been deployed",
            ],
        ],
        tags=["data-cleanup", "double-escaped", "json-parsing"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 4. Webpack bundler errors with chunk hashes
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-webpack-build-error",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "environment_details"],
        subjects=[
            "Internal dashboard build broken — webpack errors after dependency update",
            "Frontend build failing — webpack chunk compilation errors",
        ],
        descriptions=[
            "The internal dashboard build started failing after we updated dependencies "
            "yesterday. Here's the full webpack output:\n\n"
            "$ npm run build\n"
            "> dashboard@3.2.1 build\n"
            "> webpack --config webpack.prod.js\n\n"
            "asset main.8a7b3c2d.js 1.24 MiB [emitted] [minimized] (name: main)\n"
            "asset vendor.f9e8d7c6.js 892 KiB [emitted] [minimized] (name: vendor)\n"
            "asset styles.4b5a6c7d.css 156 KiB [emitted] (name: styles)\n\n"
            "ERROR in ./src/components/DataGrid/index.tsx 42:7\n"
            "Module not found: Error: Can't resolve '@tanstack/react-table' in "
            "'/app/src/components/DataGrid'\n"
            "  @ ./src/components/DataGrid/index.tsx 42:7-40\n"
            "  @ ./src/pages/Dashboard.tsx 8:0-52\n"
            "  @ ./src/App.tsx 15:0-44\n\n"
            "ERROR in ./src/utils/chart-helpers.ts 3:0\n"
            "Module not found: Error: Can't resolve 'chart.js/auto' in "
            "'/app/src/utils'\n"
            "  @ ./src/utils/chart-helpers.ts 3:0-35\n"
            "  @ ./src/components/RevenueChart.tsx 5:0-48\n\n"
            "webpack 5.89.0 compiled with 2 errors in 34521 ms\n\n"
            "The build was working fine before the npm update. Can someone help?",
            "Frontend dashboard build failing after dependency update. Webpack can't "
            "resolve @tanstack/react-table and chart.js/auto modules. Build had 2 errors "
            "in 34.5 seconds. Need to fix dependency resolution.",
        ],
        next_best_actions=[
            "Check package.json and package-lock.json for breaking changes in "
            "@tanstack/react-table and chart.js after the dependency update.",
            "Review the npm update output for major version bumps that changed "
            "module export paths for react-table and chart.js.",
        ],
        remediation_steps=[
            [
                "Review the npm update output to identify which packages had major version changes",
                "Check @tanstack/react-table migration guide for import path changes",
                "Verify chart.js/auto is still the correct import path in the updated version",
                "Update import statements in DataGrid/index.tsx and chart-helpers.ts",
                "Run the build locally to verify it succeeds before pushing",
            ],
        ],
        tags=["data-cleanup", "webpack", "build-error"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 5. PowerShell verbose error output
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-powershell-error-stream",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["environment_details", "error_message"],
        subjects=[
            "Automated deployment script failing — PowerShell errors pasted",
            "PowerShell deployment script errors — need help debugging",
        ],
        descriptions=[
            "Our automated deployment script started failing. Here's the PowerShell "
            "error output:\n\n"
            "PS C:\\Deploy> .\\Deploy-Application.ps1 -Environment Production\n\n"
            "VERBOSE: Starting deployment to Production environment...\n"
            "VERBOSE: Connecting to deployment server deploy-prod-01.contoso.com...\n"
            "VERBOSE: Authenticated as svc-deploy@contoso.com\n"
            "VERBOSE: Downloading artifact package v3.8.2 from repository...\n"
            "VERBOSE: Package downloaded: app-bundle-3.8.2.zip (142MB)\n"
            "VERBOSE: Extracting to C:\\Deploy\\staging\\...\n\n"
            "Stop-Service : Cannot find any service with service name 'ContosoAppSvc'.\n"
            "At C:\\Deploy\\Deploy-Application.ps1:87:5\n"
            "+     Stop-Service -Name 'ContosoAppSvc' -Force -ErrorAction Stop\n"
            "+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            "    + CategoryInfo          : ObjectNotFound: (ContosoAppSvc:String) "
            "[Stop-Service], ServiceCommandException\n"
            "    + FullyQualifiedErrorId : NoServiceFoundForGivenName,Microsoft.PowerShell"
            ".Commands.StopServiceCommand\n\n"
            "Copy-Item : Access to the path 'C:\\Program Files\\ContosoApp\\config.json' "
            "is denied.\n"
            "At C:\\Deploy\\Deploy-Application.ps1:95:5\n"
            "+     Copy-Item -Path $stagingPath\\* -Destination $installPath -Recurse\n"
            "+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            "    + CategoryInfo          : PermissionDenied: (config.json:FileInfo) "
            "[Copy-Item], UnauthorizedAccessException\n"
            "    + FullyQualifiedErrorId : CopyFileInfoItemUnauthorizedAccessError,"
            "Microsoft.PowerShell.Commands.CopyItemCommand\n\n"
            "ScriptStackTrace:\n"
            "  at Deploy-Package, C:\\Deploy\\Deploy-Application.ps1:95\n"
            "  at <ScriptBlock>, C:\\Deploy\\Deploy-Application.ps1:142\n\n"
            "The service name might have changed in the latest server config update.",
            "Deployment script failing with PowerShell errors. Two issues: service "
            "'ContosoAppSvc' not found (CategoryInfo: ObjectNotFound) and file access "
            "denied for config.json (FullyQualifiedErrorId: CopyFileInfoItem"
            "UnauthorizedAccessError). Script worked last week.",
        ],
        next_best_actions=[
            "Check if the ContosoAppSvc service was renamed or removed during the "
            "recent server configuration update, and verify deployment service account permissions.",
            "Investigate the service name change and file permission issue on the production deployment server.",
        ],
        remediation_steps=[
            [
                "Check the current service name on deploy-prod-01 using"
                " Get-Service | Where-Object {$_.DisplayName -like '*Contoso*'}",
                "Update the deployment script with the correct service name",
                "Verify the svc-deploy service account has write permissions to C:\\Program Files\\ContosoApp\\",
                "Test the deployment script in a staging environment first",
                "Re-run the production deployment after fixes are validated",
            ],
        ],
        tags=["data-cleanup", "powershell", "deployment-error"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 6. Windows Registry .reg file content
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-registry-export",
        category="Software & Applications",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "application_version"],
        subjects=[
            "App settings corrupted after Windows Update — registry dump attached",
            "Application registry keys look wrong after update — see export below",
        ],
        descriptions=[
            "After the latest Windows Update (KB5034441), our Contoso FinanceApp "
            "stopped saving user preferences. I exported the registry keys:\n\n"
            "Windows Registry Editor Version 5.00\n\n"
            "[HKEY_CURRENT_USER\\Software\\Contoso\\FinanceApp\\v4]\n"
            '"InstallPath"="C:\\\\Program Files\\\\Contoso\\\\FinanceApp"\n'
            '"UserDataPath"="C:\\\\Users\\\\%USERNAME%\\\\AppData\\\\Local\\\\Contoso\\\\FinanceApp"\n'
            '"Theme"=dword:00000001\n'
            '"AutoSave"=dword:00000001\n'
            '"LastSync"="2026-03-15T08:30:00Z"\n'
            '"ServerEndpoint"="https://api.contoso.com/finance/v4"\n\n'
            "[HKEY_CURRENT_USER\\Software\\Contoso\\FinanceApp\\v4\\Preferences]\n"
            '"DefaultCurrency"="USD"\n'
            '"DateFormat"="yyyy-MM-dd"\n'
            '"PageSize"=dword:00000019\n'
            '"EnableNotifications"=dword:00000000\n\n'
            "[HKEY_LOCAL_MACHINE\\SOFTWARE\\Contoso\\FinanceApp]\n"
            '"Version"="4.2.1"\n'
            '"LicenseKey"="XXXX-XXXX-XXXX-XXXX"\n'
            '"REG_MULTI_SZ_Servers"=hex(7):61,00,70,00,69,00,2d,00,30,00,31,00,00,00,\\\n'
            "  61,00,70,00,69,00,2d,00,30,00,32,00,00,00,00,00\n\n"
            "The EnableNotifications key is set to 0 but should be 1. And the "
            "Preferences subkey seems to have lost several entries that were there "
            "before the update.",
            "Windows Update KB5034441 appears to have corrupted or reset registry "
            "keys for FinanceApp v4. User preferences under "
            "HKEY_CURRENT_USER\\Software\\Contoso\\FinanceApp\\v4\\Preferences are "
            "missing entries. Registry export shows DWORD values and REG_MULTI_SZ "
            "entries. Need Endpoint Engineering to review.",
        ],
        next_best_actions=[
            "Compare the current registry state against a known-good backup to "
            "identify which keys were modified or removed by the Windows Update.",
            "Investigate if Windows Update KB5034441 has known compatibility issues with the FinanceApp registry keys.",
        ],
        remediation_steps=[
            [
                "Export the current FinanceApp registry keys for comparison with a pre-update backup",
                "Check Microsoft KB articles for known issues with KB5034441 and third-party software",
                "Restore missing preference keys from a known-good registry backup or default configuration",
                "Set EnableNotifications back to DWORD 1",
                "Test FinanceApp preference saving after the registry fix",
            ],
        ],
        tags=["data-cleanup", "windows-registry", "registry-export"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 7. PEM-encoded X.509 certificate chain
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-pem-certificate-chain",
        category="Security & Compliance",
        priority="P2",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=["affected_system", "environment_details"],
        subjects=[
            "TLS handshake failure — certificate chain pasted for review",
            "SSL certificate error on internal app — cert chain below",
        ],
        descriptions=[
            "Getting TLS handshake failures connecting to our internal payments API. "
            "Here is the certificate chain I pulled:\n\n"
            "-----BEGIN CERTIFICATE-----\n"
            "MIIFjTCCA3WgAwIBAgIUBzR3mHk4Z7xG+9LfK0Q8YK0gN2YwDQYJKoZIhvcNAQEL\n"
            "BQAwXjELMAkGA1UEBhMCVVMxEzARBgNVBAgMCldhc2hpbmd0b24xEDAOBgNVBAcM\n"
            "B1NlYXR0bGUxEDAOBgNVBAoMB0NvbnRvc28xFjAUBgNVBAMMDSouY29udG9zby5j\n"
            "b20wHhcNMjYwMTAxMDAwMDAwWhcNMjYwMzMxMjM1OTU5WjBeMQswCQYDVQQGEwJV\n"
            "UzETMBEGA1UECAwKV2FzaGluZ3RvbjEQMA4GA1UEBwwHU2VhdHRsZTEQMA4GA1UE\n"
            "CgwHQ29udG9zbzEWMBQGA1UEAwwNKi5jb250b3NvLmNvbTCCAiIwDQYJKoZIhvcN\n"
            "AQEBBQADggIPADCCAgoCggIBAL...[truncated]\n"
            "-----END CERTIFICATE-----\n\n"
            "-----BEGIN CERTIFICATE-----\n"
            "MIIEkjCCA3qgAwIBAgIQCgFBQgAAAVOFc2oLheynCDANBgkqhkiG9w0BAQsFADA/\n"
            "MSQwIgYDVQQKExtEaWdpdGFsIFNpZ25hdHVyZSBUcnVzdCBDby4xFzAVBgNVBAMT\n"
            "DkRTVCBSb290IENBIFgzMB4XDTE2MDMxNzE2NDA0NloXDTIxMDMxNzE2NDA0Nlow\n"
            "SjELMAkGA1UEBhMCVVMx...[truncated]\n"
            "-----END CERTIFICATE-----\n\n"
            "The wildcard cert *.contoso.com appears to be expired (valid until "
            "2026-03-31). The payments API is returning ERR_CERT_DATE_INVALID. "
            "This is blocking all payment processing.",
            "TLS certificate chain for payments API is failing validation. The wildcard "
            "*.contoso.com certificate shows expiry date 2026-03-31. PEM-encoded chain "
            "has two certificates (leaf + intermediate). All HTTPS connections to "
            "payments.contoso.com are failing with certificate date invalid errors.",
        ],
        next_best_actions=[
            "Renew the wildcard *.contoso.com TLS certificate immediately — it is "
            "expired or about to expire, blocking the payments API.",
            "Request an emergency certificate renewal for *.contoso.com and deploy "
            "the new cert to the payments API servers.",
        ],
        remediation_steps=[
            [
                "Verify the exact expiry date of the *.contoso.com wildcard certificate",
                "Request an emergency certificate renewal through the PKI team",
                "Deploy the renewed certificate to all payments API servers",
                "Verify the full chain of trust including intermediate certificates",
                "Test HTTPS connectivity to payments.contoso.com after deployment",
                "Set up certificate expiry monitoring alerts to prevent recurrence",
            ],
        ],
        tags=["data-cleanup", "pem-certificate", "tls-chain"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 8. Systemd journal output flood
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-systemd-journal-flood",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["environment_details", "configuration_details"],
        subjects=[
            "Linux app server won't start — systemd journal dump",
            "Application service failing on Linux server — journalctl output pasted",
        ],
        descriptions=[
            "Our reporting service on the Linux app server won't start. Here's the "
            "systemd journal output:\n\n"
            "$ journalctl -u contoso-reporting.service --no-pager -n 50\n"
            "-- Logs begin at Mon 2026-03-01 00:00:01 UTC, end at Tue 2026-03-17 "
            "09:15:32 UTC. --\n"
            "Mar 17 09:15:00 appserver-03 systemd[1]: Starting Contoso Reporting Service...\n"
            "Mar 17 09:15:01 appserver-03 contoso-reporting[8842]: [INFO] Loading "
            "configuration from /etc/contoso/reporting.yaml\n"
            "Mar 17 09:15:01 appserver-03 contoso-reporting[8842]: [INFO] Connecting "
            "to database postgresql://db-prod-02:5432/reporting\n"
            "Mar 17 09:15:03 appserver-03 contoso-reporting[8842]: [ERROR] Failed to "
            "connect to database: FATAL: password authentication failed for user "
            '"svc_reporting"\n'
            "Mar 17 09:15:03 appserver-03 contoso-reporting[8842]: [ERROR] Retrying "
            "connection (attempt 1/3)...\n"
            "Mar 17 09:15:06 appserver-03 contoso-reporting[8842]: [ERROR] Retrying "
            "connection (attempt 2/3)...\n"
            "Mar 17 09:15:09 appserver-03 contoso-reporting[8842]: [ERROR] Retrying "
            "connection (attempt 3/3)...\n"
            "Mar 17 09:15:12 appserver-03 contoso-reporting[8842]: [FATAL] Could not "
            "establish database connection after 3 attempts. Shutting down.\n"
            "Mar 17 09:15:12 appserver-03 systemd[1]: contoso-reporting.service: "
            "Main process exited, code=exited, status=1/FAILURE\n"
            "Mar 17 09:15:12 appserver-03 systemd[1]: contoso-reporting.service: "
            "Failed with result 'exit-code'.\n"
            "Mar 17 09:15:12 appserver-03 systemd[1]: Failed to start Contoso "
            "Reporting Service.\n\n"
            "The service was working yesterday. Did someone change the database password?",
            "Reporting service on appserver-03 failing to start. Systemd journal shows "
            "the service can't authenticate to the database — 'password authentication "
            "failed for user svc_reporting'. Tried systemctl restart but same error. "
            "The service unit file references /etc/contoso/reporting.yaml for config.",
        ],
        next_best_actions=[
            "Check if the svc_reporting database password was recently rotated — the "
            "reporting service can't authenticate to db-prod-02.",
            "Verify the database credentials in /etc/contoso/reporting.yaml match the "
            "current svc_reporting password on db-prod-02.",
        ],
        remediation_steps=[
            [
                "Check with the DBA team if the svc_reporting password was recently changed",
                "Update the password in /etc/contoso/reporting.yaml on appserver-03",
                "Restart the contoso-reporting.service with systemctl restart",
                "Verify the service starts successfully and can query the reporting database",
                "Review password rotation procedures to include service credential updates",
            ],
        ],
        tags=["data-cleanup", "systemd", "journal-log"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 9. Mixed CJK/Latin text with encoding issues
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-cjk-mixed-encoding",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["device_info", "application_version"],
        subjects=[
            "Outlook encoding issue — 邮件客户端显示乱码",
            "Email client showing garbled text — mixed language display problem",
        ],
        descriptions=[
            "Hi IT,\n\nOur team in the Shanghai office is having trouble with Outlook "
            "displaying garbled text. When we receive emails from the Tokyo office, "
            "the Japanese text shows up incorrectly.\n\n"
            "\u4f8b\u3048\u3070 (For example):\n"
            "Original: \u4f1a\u8b70\u306e\u8b70\u4e8b\u9332\u3092\u9001\u308a\u307e\u3059\u3002"
            "\u6dfb\u4ed8\u30d5\u30a1\u30a4\u30eb\u3092\u3054\u78ba\u8a8d\u304f\u3060\u3055\u3044\u3002\n"
            "Displayed: \u00e4\u00bc\u009a\u00e8\u00ad\u00b0\u00e3\u0081\u00ae"
            "\u00e8\u00ad\u00b0\u00e4\u00ba\u008b\u00e9\u008c\u00b2\n\n"
            "\u5f53\u6211\u4eec\u7528\u4e2d\u6587\u56de\u590d\u65f6 "
            "(When we reply in Chinese), the text also gets mangled:\n"
            "\u6211\u4eec\u8f93\u5165: \u8bf7\u67e5\u6536\u9644\u4ef6\u4e2d\u7684\u62a5\u544a\u3002\n"
            "They see: garbled mojibake characters instead of Chinese text\n\n"
            "English text works fine between both offices. The problem only occurs "
            "with CJK characters (Chinese, Japanese, Korean). We think it might be "
            "an encoding mismatch in the Exchange transport rules.",
            "Mixed CJK text encoding issue between Shanghai and Tokyo offices. Japanese "
            "\u4f1a\u8b70\u306e\u8b70\u4e8b\u9332 showing as mojibake. Chinese text also "
            "affected. English works fine. Likely UTF-8 vs Shift-JIS or GB2312 encoding "
            "conflict.",
        ],
        next_best_actions=[
            "Investigate Exchange transport rules for CJK character encoding — "
            "the issue is likely a UTF-8 vs legacy encoding mismatch between offices.",
            "Check Outlook and Exchange encoding settings for the Shanghai and Tokyo "
            "offices to resolve the CJK character display issue.",
        ],
        remediation_steps=[
            [
                "Check Exchange Online transport rules for character set conversion settings",
                "Verify that both Shanghai and Tokyo mailboxes are configured for UTF-8 encoding",
                "Check if any email security appliance is modifying content encoding",
                "Test sending CJK text directly via OWA to isolate whether it's a client or server issue",
                "Update Outlook language/encoding settings on affected machines if needed",
            ],
        ],
        tags=["data-cleanup", "cjk-text", "encoding-issue"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 10. Full HTTP response with headers and body
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-http-response-dump",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["affected_system", "network_location"],
        subjects=[
            "Internal web app returning 502 — full HTTP response attached",
            "Getting 502 Bad Gateway errors from the load balancer — response pasted",
        ],
        descriptions=[
            "Our internal web app behind the load balancer is returning 502 errors. "
            "Here's the full HTTP response I captured:\n\n"
            "HTTP/1.1 502 Bad Gateway\n"
            "Server: nginx/1.24.0\n"
            "Date: Tue, 17 Mar 2026 14:30:22 GMT\n"
            "Content-Type: text/html; charset=utf-8\n"
            "Content-Length: 497\n"
            "Connection: keep-alive\n"
            "X-Request-Id: 7b3a8c4d-2e1f-4a5b-9c6d-8e7f0a1b2c3d\n"
            "X-Upstream-Status: 502\n"
            "X-Upstream-Addr: 10.0.2.45:8080\n"
            "X-Upstream-Response-Time: 60.003\n"
            "Strict-Transport-Security: max-age=31536000; includeSubDomains\n\n"
            "<html>\n"
            "<head><title>502 Bad Gateway</title></head>\n"
            "<body>\n"
            "<center><h1>502 Bad Gateway</h1></center>\n"
            "<center>nginx/1.24.0</center>\n"
            "<hr><center>X-Request-Id: 7b3a8c4d-2e1f-4a5b-9c6d-8e7f0a1b2c3d</center>\n"
            "</body>\n"
            "</html>\n\n"
            "The upstream address is 10.0.2.45:8080 and the response time was 60 seconds "
            "(timeout). This happens intermittently — about 30% of requests fail.",
            "502 Bad Gateway from nginx load balancer for the internal web app. HTTP "
            "response shows upstream 10.0.2.45:8080 timing out at 60 seconds. Happens "
            "~30% of requests. X-Request-Id tracked. Need Network Ops to investigate.",
        ],
        next_best_actions=[
            "Investigate the upstream server 10.0.2.45:8080 — it's timing out after "
            "60 seconds causing nginx to return 502 Bad Gateway.",
            "Check the health of the upstream application on 10.0.2.45:8080 and "
            "increase the nginx proxy timeout if the app needs more processing time.",
        ],
        remediation_steps=[
            [
                "Check the health and logs of the upstream application at 10.0.2.45:8080",
                "Verify if the application is under heavy load causing timeouts",
                "Review nginx upstream configuration for timeout settings",
                "Increase proxy_read_timeout if the application legitimately needs more than 60 seconds",
                "Consider adding more upstream instances to the load balancer pool",
            ],
        ],
        tags=["data-cleanup", "http-response", "502-error"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 11. Nested MIME multipart email source
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-mime-multipart",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["device_info", "application_version"],
        subjects=[
            "Email attachments not rendering — raw MIME source pasted",
            "Outlook showing raw MIME data instead of formatted email",
        ],
        descriptions=[
            "When I open certain emails in Outlook, I see the raw MIME source instead "
            "of the formatted message. Here's what appears:\n\n"
            "MIME-Version: 1.0\n"
            "Content-Type: multipart/mixed;\n"
            ' boundary="----=_Part_99887_12345.1710500000000"\n\n'
            "------=_Part_99887_12345.1710500000000\n"
            "Content-Type: multipart/alternative;\n"
            ' boundary="----=_Part_99888_67890.1710500000001"\n\n'
            "------=_Part_99888_67890.1710500000001\n"
            "Content-Type: text/plain; charset=UTF-8\n"
            "Content-Transfer-Encoding: quoted-printable\n\n"
            "Please review the attached quarterly report.\n\n"
            "------=_Part_99888_67890.1710500000001\n"
            "Content-Type: text/html; charset=UTF-8\n"
            "Content-Transfer-Encoding: base64\n\n"
            "PGh0bWw+PGJvZHk+PHA+UGxlYXNlIHJldmlldyB0aGUgYXR0YWNoZWQgcXVhcnRlcmx5\n"
            "IHJlcG9ydC48L3A+PC9ib2R5PjwvaHRtbD4=\n\n"
            "------=_Part_99888_67890.1710500000001--\n\n"
            "------=_Part_99887_12345.1710500000000\n"
            "Content-Type: application/pdf;\n"
            ' name="Q1_Report_2026.pdf"\n'
            "Content-Transfer-Encoding: base64\n"
            "Content-Disposition: attachment;\n"
            ' filename="Q1_Report_2026.pdf"\n\n'
            "JVBERi0xLjQKMSAwIG9iago8PAovVGl0bGUgKFExIFJlcG9ydCAyMDI2KQov...\n"
            "[truncated — 500+ lines of base64 data]\n\n"
            "------=_Part_99887_12345.1710500000000--\n\n"
            "This only happens with emails from external senders. Internal emails "
            "display fine. Using Outlook desktop app.",
            "Outlook rendering raw MIME multipart data instead of formatted email. "
            "Content-Type boundaries, base64 encoded HTML and PDF attachment data "
            "visible in the email body. Affects external emails only.",
        ],
        next_best_actions=[
            "Investigate Outlook MIME rendering for external emails — likely a "
            "content-type handling or Exchange transport rule issue.",
            "Check Exchange Online transport rules for external email processing — "
            "MIME parsing may be broken for certain sender configurations.",
        ],
        remediation_steps=[
            [
                "Check Exchange transport rules for modifications to external email content",
                "Verify Outlook email rendering settings and cached profile data",
                "Test with Outlook Web App to determine if it's a desktop client issue",
                "Check if any email security appliance is modifying MIME structure",
                "Clear the Outlook profile cache and recreate if rendering is client-side",
            ],
        ],
        tags=["data-cleanup", "mime-multipart", "email-rendering"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 12. Git commit history dump
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-git-commit-history",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["environment_details", "steps_to_reproduce"],
        subjects=[
            "Deployment broke after merge — git log of recent changes",
            "App broken after latest deployment — git history pasted below",
        ],
        descriptions=[
            "The internal customer portal broke after our latest deployment. I pulled "
            "the git log to show recent changes:\n\n"
            "$ git log --oneline --graph -15\n"
            "* 8a7b3c2 (HEAD -> main, origin/main) Merge pull request #847 from "
            "feature/payment-refactor\n"
            "|\\\n"
            "| * f9e8d7c Fix payment webhook handler timeout\n"
            "| * 4b5a6c7 Refactor payment processing module\n"
            "| * 2d3e4f5 Add retry logic for failed payment callbacks\n"
            "|/\n"
            "* 1c2d3e4 Update dependencies — bump express to 4.19.2\n"
            "* 9a8b7c6 Fix CORS headers for mobile API\n"
            "* 6f5e4d3 Merge pull request #845 from feature/user-search\n"
            "|\\\n"
            "| * 3b2a1c0 Add fuzzy search to user directory\n"
            "|/\n"
            "* 7e6d5c4 Hotfix: session timeout increased to 30m\n\n"
            "$ git diff HEAD~3..HEAD --stat\n"
            " src/payment/handler.ts     | 142 +++++++++++++++++--------\n"
            " src/payment/webhook.ts     |  87 ++++++++++------\n"
            " src/payment/retry.ts       |  63 ++++++++++++\n"
            " src/config/payment.json    |  12 ++-\n"
            " package.json               |   4 +-\n"
            " 5 files changed, 218 insertions(+), 90 deletions(-)\n\n"
            "The payment-refactor merge (PR #847) is the most likely cause. The portal "
            "shows 'Payment service unavailable' for all checkout attempts.",
            "Customer portal checkout broken after deployment. Git log shows merge of "
            "payment-refactor branch (PR #847) with changes to handler.ts, webhook.ts, "
            "and new retry.ts. 218 insertions across 5 files. Need to investigate the "
            "payment refactor changes.",
        ],
        next_best_actions=[
            "Revert the payment-refactor merge (PR #847) to restore checkout "
            "functionality, then investigate the webhook handler changes.",
            "Roll back the latest deployment to the pre-merge commit and debug "
            "the payment handler timeout fix in staging.",
        ],
        remediation_steps=[
            [
                "Revert the merge commit 8a7b3c2 to restore the previous payment processing code",
                "Deploy the reverted codebase to production to restore checkout functionality",
                "Review the payment webhook handler changes in PR #847 for the root cause",
                "Test the payment refactor thoroughly in a staging environment with load testing",
                "Re-deploy the payment refactor only after staging validation passes",
            ],
        ],
        tags=["data-cleanup", "git-history", "deployment-issue"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 13. Terraform plan output with resource changes
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-terraform-plan",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["environment_details", "business_impact"],
        subjects=[
            "Azure infrastructure provisioning failed — Terraform plan output",
            "Terraform plan showing unexpected resource destruction — need review",
        ],
        descriptions=[
            "Our Terraform plan for the Azure data lake provisioning is showing "
            "unexpected resource changes. Here's the plan output:\n\n"
            "$ terraform plan -out=tfplan\n\n"
            "Terraform will perform the following actions:\n\n"
            "  # azurerm_storage_account.datalake will be updated in-place\n"
            '  ~ resource "azurerm_storage_account" "datalake" {\n'
            '      ~ account_tier             = "Standard" -> "Premium"\n'
            '      ~ account_replication_type = "GRS" -> "LRS"\n'
            '        name                     = "contosodatalake01"\n'
            '        resource_group_name      = "rg-data-prod"\n'
            "    }\n\n"
            "  # azurerm_storage_data_lake_gen2_filesystem.main will be destroyed\n"
            "  # (because azurerm_storage_data_lake_gen2_filesystem.main is not in "
            "configuration)\n"
            '  - resource "azurerm_storage_data_lake_gen2_filesystem" "main" {\n'
            '      - name               = "analytics"\n'
            '      - storage_account_id = "/subscriptions/abc123/resourceGroups/'
            'rg-data-prod/providers/Microsoft.Storage/storageAccounts/contosodatalake01"\n'
            "    }\n\n"
            "  # azurerm_synapse_workspace.analytics will be created\n"
            '  + resource "azurerm_synapse_workspace" "analytics" {\n'
            '      + name                = "contoso-synapse-01"\n'
            '      + resource_group_name = "rg-data-prod"\n'
            '      + location            = "eastus2"\n'
            "    }\n\n"
            "Plan: 1 to add, 1 to change, 1 to destroy.\n\n"
            "The destruction of the Data Lake Gen2 filesystem 'analytics' is NOT "
            "expected — that has production data in it. DO NOT APPLY this plan.",
            "Terraform plan for Azure data lake shows unexpected destruction of the "
            "analytics filesystem. Plan: 1 add (Synapse workspace), 1 change (storage "
            "tier Standard->Premium, GRS->LRS), 1 destroy (Data Lake Gen2 filesystem). "
            "The destroy is dangerous — contains production data.",
        ],
        next_best_actions=[
            "DO NOT apply the Terraform plan — the destruction of the Data Lake Gen2 "
            "filesystem would delete production analytics data. Review the Terraform "
            "configuration for the missing resource definition.",
            "Block the Terraform plan execution and investigate why the Data Lake "
            "Gen2 filesystem resource was removed from the configuration.",
        ],
        remediation_steps=[
            [
                "Do NOT apply the current Terraform plan — it would destroy production data",
                "Identify which configuration change removed the Data Lake Gen2 filesystem resource",
                "Restore the azurerm_storage_data_lake_gen2_filesystem.main resource definition",
                "Review the storage tier change from Standard/GRS to Premium/LRS for correctness",
                "Run terraform plan again to verify no unexpected destructions before applying",
            ],
        ],
        tags=["data-cleanup", "terraform", "infrastructure"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 14. DNS zone file records
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-dns-zone-file",
        category="Network & Connectivity",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["timestamp", "affected_users"],
        subjects=[
            "URGENT: Internal DNS resolution failing — zone file for reference",
            "DNS records corrupted — zone file excerpt below",
        ],
        descriptions=[
            "Internal DNS resolution is completely broken since this morning. Multiple "
            "services are unreachable. Here's an excerpt from the zone file:\n\n"
            "$ORIGIN contoso.internal.\n"
            "$TTL 3600\n"
            "@   IN  SOA ns1.contoso.internal. admin.contoso.com. (\n"
            "                2026031701  ; Serial\n"
            "                3600        ; Refresh\n"
            "                900         ; Retry\n"
            "                604800      ; Expire\n"
            "                86400 )     ; Minimum TTL\n\n"
            "    IN  NS  ns1.contoso.internal.\n"
            "    IN  NS  ns2.contoso.internal.\n\n"
            "ns1           IN  A     10.0.1.10\n"
            "ns2           IN  A     10.0.1.11\n"
            "dc-01         IN  A     10.0.1.20\n"
            "dc-02         IN  A     10.0.1.21\n"
            "mail          IN  A     10.0.2.30\n"
            "mail          IN  MX 10 mail.contoso.internal.\n"
            "vpn           IN  A     10.0.3.40\n"
            "portal        IN  CNAME webapp-prod.contoso.internal.\n"
            "webapp-prod   IN  A     10.0.4.50\n"
            "api           IN  CNAME api-lb.contoso.internal.\n"
            "api-lb        IN  A     10.0.4.60\n"
            "db-prod       IN  A     10.0.5.70\n\n"
            "I noticed the serial number was updated (2026031701) but several records "
            "that should point to our new servers are missing. The migration to new "
            "infrastructure was supposed to add records for the new subnet 10.0.6.x. "
            "Nothing resolves there now.",
            "Internal DNS zone file for contoso.internal has issues after serial update. "
            "Zone shows SOA, NS, A, MX, and CNAME records but migration records for "
            "new 10.0.6.x subnet are missing. Multiple services unreachable. Impacting "
            "all internal users.",
        ],
        next_best_actions=[
            "Restore the missing DNS records for the 10.0.6.x subnet immediately — "
            "the infrastructure migration zone changes were not applied correctly.",
            "Emergency DNS zone update needed — add the missing A records for the "
            "new 10.0.6.x subnet to restore internal service resolution.",
        ],
        remediation_steps=[
            [
                "Identify the missing DNS records by comparing with the migration plan documentation",
                "Add the missing A records for the 10.0.6.x subnet to the zone file",
                "Increment the zone serial number and reload the DNS service",
                "Verify resolution for all affected services using nslookup/dig",
                "Ensure zone transfer to ns2 completes successfully",
                "Communicate restoration to affected users and teams",
            ],
        ],
        tags=["data-cleanup", "dns-zone", "network-outage"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 15. Packet capture text output (tcpdump)
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-expert-pcap-text-output",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "affected_users"],
        subjects=[
            "Intermittent network drops between sites — tcpdump capture",
            "Network packet loss between offices — capture data pasted",
        ],
        descriptions=[
            "We're seeing intermittent network drops between the Seattle and London "
            "offices. I ran a tcpdump capture during a failure window:\n\n"
            "$ tcpdump -i eth0 -nn host 10.0.4.50 and host 172.16.2.30\n"
            "tcpdump: listening on eth0, link-type EN10MB, capture size 262144 bytes\n"
            "14:30:01.123456 IP 10.0.4.50.443 > 172.16.2.30.52847: "
            "Flags [S.], seq 2847103956, ack 1738294562, win 65535, "
            "options [mss 1460,sackOK,TS val 1234567 ecr 7654321,nop,wscale 7], length 0\n"
            "14:30:01.234567 IP 172.16.2.30.52847 > 10.0.4.50.443: "
            "Flags [.], ack 1, win 502, options [nop,nop,TS val 7654400 ecr 1234567], length 0\n"
            "14:30:01.345678 IP 10.0.4.50.443 > 172.16.2.30.52847: "
            "Flags [P.], seq 1:1449, ack 1, win 512, length 1448\n"
            "14:30:05.456789 IP 10.0.4.50.443 > 172.16.2.30.52847: "
            "Flags [P.], seq 1:1449, ack 1, win 512, length 1448 [TCP Retransmission]\n"
            "14:30:09.567890 IP 10.0.4.50.443 > 172.16.2.30.52847: "
            "Flags [P.], seq 1:1449, ack 1, win 512, length 1448 [TCP Retransmission]\n"
            "14:30:17.678901 IP 10.0.4.50.443 > 172.16.2.30.52847: "
            "Flags [R.], seq 1449, ack 1, win 512, length 0\n\n"
            "Notice the 4-second and 8-second retransmission gaps followed by a RST. "
            "Packets from Seattle (10.0.4.50) to London (172.16.2.30) are being "
            "dropped somewhere in the WAN. About 15% packet loss during business hours.",
            "tcpdump capture shows TCP retransmissions between Seattle 10.0.4.50 and "
            "London 172.16.2.30. Flags show SYN-ACK, then data packets retransmitted "
            "at 4s and 8s intervals before RST. ~15% packet loss during business hours. "
            "Likely WAN link congestion or QoS issue.",
        ],
        next_best_actions=[
            "Investigate the WAN link between Seattle and London for packet loss — "
            "TCP retransmissions and RST packets indicate connectivity issues.",
            "Check WAN link utilization and QoS policies between Seattle and London "
            "offices to identify the cause of the 15% packet loss.",
        ],
        remediation_steps=[
            [
                "Run continuous ping and traceroute between Seattle and London to identify the failure point",
                "Check WAN link utilization during business hours for saturation",
                "Review QoS policies to ensure business-critical traffic is prioritized",
                "Contact the WAN provider if the issue is on their network segment",
                "Consider increasing WAN bandwidth if utilization is consistently high",
            ],
        ],
        tags=["data-cleanup", "pcap", "network-trace"],
    ),
]
