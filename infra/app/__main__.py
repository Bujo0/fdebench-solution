# Copyright (c) Microsoft. All rights reserved.
"""Pulumi program to deploy FDEBench to Azure Container Apps.

Deploys:
- Azure Container Registry (ACR) in eastus2
- Log Analytics Workspace for container diagnostics
- Container Apps Environment in eastus2
- Container App for FDEBench with configured environment variables
- Managed Identity for ACR image pulls
"""

import pulumi
from pulumi_azure_native import app
from pulumi_azure_native import containerregistry
from pulumi_azure_native import managedidentity
from pulumi_azure_native import operationalinsights
from pulumi_azure_native import resources

# =============================================================================
# CONFIGURATION
# =============================================================================
config = pulumi.Config()
azure_config = pulumi.Config("azure-native")

# Get the location (default to eastus2)
location = "eastus2"

# Container registry configuration
acr_sku = "Standard"

# Container app configuration
app_name = "fdebench"
app_image_name = "fdebench"
app_port = 8000
cpu = "1.0"
memory_gb = "2"
min_replicas = 1
max_replicas = 3

# Get environment variables from config
azure_openai_endpoint = config.require("azure_openai_endpoint")
azure_openai_api_key = config.require_secret("azure_openai_api_key")
azure_openai_api_version = config.require("azure_openai_api_version")
triage_model = config.require("triage_model")
extract_model = config.require("extract_model")
orchestrate_model = config.require("orchestrate_model")
di_endpoint = config.require("di_endpoint")
di_api_key = config.require_secret("di_api_key")

# =============================================================================
# RESOURCE GROUP (already exists, get reference)
# =============================================================================
resource_group_name = "fbujaroski-fdebench-rg"

# Get reference to existing resource group
resource_group = resources.get_resource_group(
    name=resource_group_name,
)

pulumi.export("resourceGroup", resource_group_name)

# =============================================================================
# AZURE CONTAINER REGISTRY
# =============================================================================
acr = containerregistry.Registry(
    f"{app_name}-acr",
    resource_group_name=resource_group_name,
    location=location,
    sku=containerregistry.SkuArgs(name=acr_sku),
    admin_user_enabled=False,
    tags={
        "app": app_name,
        "managed-by": "pulumi",
    },
)

pulumi.export("acrName", acr.name)
pulumi.export("acrLoginServer", acr.login_server)

# =============================================================================
# LOG ANALYTICS WORKSPACE
# =============================================================================
log_analytics_workspace = operationalinsights.Workspace(
    f"{app_name}-logs",
    resource_group_name=resource_group_name,
    location=location,
    retention_in_days=30,
    sku=operationalinsights.WorkspaceSkuArgs(
        name=operationalinsights.WorkspaceSkuNameEnum.PER_GB2018,
    ),
    tags={
        "app": app_name,
        "managed-by": "pulumi",
    },
)

pulumi.export("logAnalyticsWorkspaceName", log_analytics_workspace.name)

# Get Log Analytics shared keys for Container Apps Environment
log_analytics_keys = operationalinsights.get_shared_keys_output(
    resource_group_name=resource_group_name,
    workspace_name=log_analytics_workspace.name,
)

# =============================================================================
# CONTAINER APPS ENVIRONMENT
# =============================================================================
container_apps_environment = app.ManagedEnvironment(
    f"{app_name}-env",
    resource_group_name=resource_group_name,
    location=location,
    app_logs_configuration=app.AppLogsConfigurationArgs(
        destination="log-analytics",
        log_analytics_configuration=app.LogAnalyticsConfigurationArgs(
            customer_id=log_analytics_workspace.customer_id,
            shared_key=log_analytics_keys.primary_shared_key,
        ),
    ),
    tags={
        "app": app_name,
        "managed-by": "pulumi",
    },
    opts=pulumi.ResourceOptions(custom_timeouts=pulumi.CustomTimeouts(create="15m")),
)

pulumi.export("containerAppsEnvironmentName", container_apps_environment.name)

# =============================================================================
# MANAGED IDENTITY FOR ACR PULL
# =============================================================================
acr_pull_identity = managedidentity.UserAssignedIdentity(
    f"{app_name}-acr-pull-identity",
    resource_group_name=resource_group_name,
    location=location,
    tags={
        "app": app_name,
        "managed-by": "pulumi",
    },
)

pulumi.export("acrPullIdentityId", acr_pull_identity.id)

# =============================================================================
# CONTAINER APP
# =============================================================================
# Build the image reference - for now using a placeholder
# In a real deployment, the image would be built and pushed to ACR
container_app = app.ContainerApp(
    app_name,
    resource_group_name=resource_group_name,
    location=location,
    managed_environment_id=container_apps_environment.id,
    identity=app.ManagedServiceIdentityArgs(
        type=app.ManagedServiceIdentityType.SYSTEM_ASSIGNED_USER_ASSIGNED,
        user_assigned_identities=[acr_pull_identity.id],
    ),
    configuration=app.ConfigurationArgs(
        registries=[
            app.RegistryCredentialsArgs(
                server=acr.login_server,
                identity=acr_pull_identity.id,
            ),
        ],
        ingress=app.IngressArgs(
            external=True,
            target_port=app_port,
            allow_insecure=False,
            traffic=[
                app.TrafficWeightArgs(
                    weight=100,
                    latest_revision=True,
                ),
            ],
        ),
    ),
    template=app.TemplateArgs(
        containers=[
            app.ContainerArgs(
                name=app_name,
                image=pulumi.Output.concat(acr.login_server, f"/{app_image_name}:latest"),
                resources=app.ContainerResourcesArgs(
                    cpu=cpu,
                    memory=f"{memory_gb}Gi",
                ),
                env=[
                    app.EnvironmentVarArgs(name="AZURE_OPENAI_ENDPOINT", value=azure_openai_endpoint),
                    app.EnvironmentVarArgs(name="AZURE_OPENAI_API_KEY", value=azure_openai_api_key),
                    app.EnvironmentVarArgs(name="AZURE_OPENAI_API_VERSION", value=azure_openai_api_version),
                    app.EnvironmentVarArgs(name="TRIAGE_MODEL", value=triage_model),
                    app.EnvironmentVarArgs(name="EXTRACT_MODEL", value=extract_model),
                    app.EnvironmentVarArgs(name="ORCHESTRATE_MODEL", value=orchestrate_model),
                    app.EnvironmentVarArgs(name="DI_ENDPOINT", value=di_endpoint),
                    app.EnvironmentVarArgs(name="DI_API_KEY", value=di_api_key),
                ],
            ),
        ],
        scale=app.ScaleArgs(
            min_replicas=min_replicas,
            max_replicas=max_replicas,
            rules=[
                app.ScaleRuleArgs(
                    name="http-rule",
                    http=app.HttpScaleRuleArgs(
                        metadata={"concurrentRequests": "100"},
                    ),
                ),
            ],
        ),
    ),
    tags={
        "app": app_name,
        "managed-by": "pulumi",
    },
)

pulumi.export("containerAppName", container_app.name)
pulumi.export("containerAppUrl", container_app.configuration.apply(
    lambda config: f"https://{config.ingress.fqdn}" if config and config.ingress else ""
))

