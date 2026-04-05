# Infrastructure as Code

The `infra/` folder contains infrastructure as code (IaC) configurations for provisioning and managing cloud resources using [Pulumi](https://www.pulumi.com/) with [Python and uv](https://www.pulumi.com/docs/iac/languages-sdks/python/#uv).

## Project Layout

```
infra/
└── app/
    ├── __main__.py      # Pulumi program defining your infrastructure
    ├── Pulumi.yml       # Project settings
    └── pyproject.toml   # Python dependencies (Pulumi SDK, Azure SDKs, etc.)
```

## Getting Started

```bash
cd infra/app
uv sync
pulumi login --local
export PULUMI_CONFIG_PASSPHRASE=$(openssl rand -hex 32)
pulumi stack select dev --create
pulumi up
```

For more details, see [Pulumi's documentation](https://www.pulumi.com/docs/).
