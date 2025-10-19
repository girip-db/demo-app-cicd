# Deployment Guide

Comprehensive guide for deploying the Databricks Table Viewer App using DABS.

## 🏗️ Architecture Overview

```
┌─────────────────┐
│  GitHub Repo    │
│  (Source Code)  │
└────────┬────────┘
         │
         │ git push
         │
    ┌────▼──────────────────────────┐
    │  GitHub Actions               │
    │  - Validate Bundle            │
    │  - Deploy with DABS           │
    └────┬──────────────────────────┘
         │
         │ databricks bundle deploy
         │
    ┌────▼──────────────────────────┐
    │  Databricks Workspace         │
    │  ┌──────────────────────┐    │
    │  │  Databricks App      │    │
    │  │  (Streamlit)         │    │
    │  └──────┬───────────────┘    │
    │         │                     │
    │    ┌────▼────────┐           │
    │    │ SQL Warehouse│           │
    │    └────┬────────┘           │
    │         │                     │
    │    ┌────▼────────┐           │
    │    │Unity Catalog│           │
    │    │   Tables    │           │
    │    └─────────────┘           │
    └───────────────────────────────┘
```

## 📋 Prerequisites

### 1. Databricks Workspace Requirements

- **Workspace Edition**: Premium or Enterprise
- **Unity Catalog**: Enabled
- **SQL Warehouse**: Serverless or Pro SQL warehouse
- **Databricks Runtime**: 13.3 LTS or higher (for apps)

### 2. Permissions Required

#### For Development/Personal Access Token:
- Workspace access
- SQL Warehouse usage
- Unity Catalog read access on catalogs/schemas/tables
- App creation and management

#### For Production/Service Principal:
```sql
-- Grant catalog access
GRANT USE CATALOG ON CATALOG <catalog_name> TO `<service_principal>`;

-- Grant schema access
GRANT USE SCHEMA ON SCHEMA <catalog_name>.<schema_name> TO `<service_principal>`;

-- Grant table access
GRANT SELECT ON TABLE <catalog_name>.<schema_name>.<table_name> TO `<service_principal>`;

-- Grant SQL warehouse access (via Databricks UI)
```

### 3. Tools Required

- **Databricks CLI**: Latest version (v0.205.0+)
- **Git**: For version control
- **Python**: 3.8 or higher (for local testing)

## 🚀 Deployment Methods

### Method 1: Direct CLI Deployment

#### Development Environment
```bash
# Deploy to dev
databricks bundle deploy -t dev

# Start the app
databricks bundle run -t dev demo_table_viewer

# Or with custom variables
databricks bundle deploy -t dev \
  --var="warehouse_id=abc123"
```

#### Staging Environment
```bash
databricks bundle deploy -t staging \
  --var="warehouse_id=xyz789"
```

#### Production Environment
```bash
databricks bundle deploy -t prod \
  --var="warehouse_id=prod123"
```

### Method 2: GitHub Actions CI/CD

#### Branch-Based Deployment

1. **Development**: Any branch push triggers validation
2. **Staging**: Push to `develop` branch
3. **Production**: Push to `main` branch

```bash
# Deploy to staging
git checkout -b develop
git add .
git commit -m "Deploy to staging"
git push origin develop

# Deploy to production
git checkout main
git merge develop
git push origin main
```

#### Manual Workflow Dispatch

```bash
# Via GitHub UI
1. Go to Actions tab
2. Select "Deploy Databricks App with DABS"
3. Click "Run workflow"
4. Select target environment
5. Click "Run workflow"

# Via GitHub CLI
gh workflow run deploy.yml -f environment=prod
```

## 🔧 Configuration Details

### Environment Variables

Each environment can have different configurations:

```yaml
# databricks.yml
targets:
  dev:
    variables:
      warehouse_id: "dev-warehouse-123"
      
  staging:
    variables:
      warehouse_id: "staging-warehouse-456"
      
  prod:
    variables:
      warehouse_id: "prod-warehouse-789"
```

### Resource Naming

Apps are named based on the target:
- Dev: `demo-table-viewer-dev`
- Staging: `demo-table-viewer-staging`
- Prod: `demo-table-viewer-prod`

### Workspace Paths

Bundle artifacts are stored at:
```
/Workspace/.bundle/demo-app-cicd/{target}/
```

## 🔐 Security Configuration

### Service Principal Setup (Production)

1. **Create Service Principal**
```bash
databricks service-principals create \
  --display-name "demo-app-cicd-prod"
```

2. **Generate Token**
```bash
databricks tokens create \
  --comment "CI/CD token for demo-app" \
  --lifetime-seconds 7776000  # 90 days
```

3. **Update databricks.yml**
```yaml
targets:
  prod:
    run_as:
      service_principal_name: "${service_principal_client_id}"
```

4. **Set GitHub Secrets**
- `DATABRICKS_TOKEN`: Service principal token
- `SERVICE_PRINCIPAL_CLIENT_ID`: Service principal ID

### Secret Management

For sensitive configurations:

```yaml
# Use Databricks Secrets
env:
  - name: DATABASE_PASSWORD
    valueFrom:
      secretKeyRef:
        scope: prod-secrets
        key: db-password
```

## 📊 Monitoring and Validation

### Pre-Deployment Validation

```bash
# Validate bundle syntax
databricks bundle validate -t prod

# Preview changes
databricks bundle deploy -t prod --dry-run
```

### Post-Deployment Checks

```bash
# List deployed apps
databricks apps list

# Get app details
databricks apps get --name demo-table-viewer-prod

# View app logs
databricks apps logs --name demo-table-viewer-prod
```

### Health Checks

Add to your workflow:

```yaml
- name: Health Check
  run: |
    # Wait for app to be ready
    sleep 30
    
    # Check app status
    STATUS=$(databricks apps get --name demo-table-viewer-${{ env.TARGET }} | jq -r '.state')
    
    if [ "$STATUS" != "RUNNING" ]; then
      echo "App deployment failed"
      exit 1
    fi
```

## 🔄 Rollback Procedures

### Method 1: Redeploy Previous Version

```bash
# Checkout previous version
git checkout <previous-commit-hash>

# Redeploy
databricks bundle deploy -t prod --force
```

### Method 2: Delete and Redeploy

```bash
# Delete current deployment
databricks bundle destroy -t prod

# Deploy previous version
git checkout <previous-commit-hash>
databricks bundle deploy -t prod
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Bundle Validation Fails

```bash
# Check for syntax errors
databricks bundle validate -t dev

# Common causes:
# - Invalid YAML syntax
# - Missing required fields
# - Invalid warehouse ID
```

#### 2. Deployment Fails

```bash
# Check CLI configuration
databricks current-user me

# Check workspace connectivity
databricks workspace list /

# Verify permissions
databricks warehouses list
```

#### 3. App Not Starting

```bash
# Check app logs
databricks apps logs --name demo-table-viewer-dev

# Common causes:
# - Missing dependencies in requirements.txt
# - SQL warehouse not running
# - Invalid credentials
```

#### 4. GitHub Actions Fails

```yaml
# Debug steps in workflow
- name: Debug Info
  run: |
    echo "Target: ${{ env.TARGET }}"
    echo "Workspace: ${{ secrets.DATABRICKS_HOST }}"
    databricks --version
    databricks current-user me
```

### Debug Mode

```bash
# Enable verbose output
databricks bundle deploy -t dev --debug

# Set log level
export DATABRICKS_LOG_LEVEL=DEBUG
databricks bundle deploy -t dev
```


### Caching Strategies

Add caching in `app.py`:

```python
import streamlit as st

@st.cache_resource
def get_connection():
    # Connection caching
    pass

@st.cache_data(ttl=300)  # 5 minutes
def get_catalogs(connection):
    # Data caching
    pass
```

## 🔄 Update Strategy

### Zero-Downtime Updates

1. Deploy to staging first
2. Run smoke tests
3. Deploy to production during low-traffic period
4. Monitor for errors
5. Rollback if needed

### Blue-Green Deployment

```bash
# Deploy new version (green)
databricks bundle deploy -t prod-green

# Test green deployment
# Switch traffic to green
# Keep blue as fallback

# After validation, remove blue
databricks bundle destroy -t prod-blue
```

## 📚 Additional Resources

- [Databricks Apps Documentation](https://docs.databricks.com/apps/index.html)
- [DABS Documentation](https://docs.databricks.com/dev-tools/bundles/index.html)
- [Databricks CLI Reference](https://docs.databricks.com/dev-tools/cli/index.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 💡 Best Practices

1. **Use Service Principals** for production deployments
2. **Test in staging** before production
3. **Monitor app health** regularly
4. **Rotate credentials** periodically
5. **Use version tags** for tracking
6. **Document changes** in commit messages
7. **Review logs** after deployments
8. **Keep dependencies updated**

---

**Questions?** Check the [main README](README.md) or open an issue.

