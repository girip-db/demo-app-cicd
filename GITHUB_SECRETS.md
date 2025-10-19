# GitHub Secrets Configuration

This document describes the required GitHub secrets for CI/CD deployment.

## 🔐 Required Secrets

Set these secrets in your GitHub repository: **Settings** → **Secrets and variables** → **Actions**

### For All Environments

| Secret Name | Description | Example | Required |
|-------------|-------------|---------|----------|
| `DATABRICKS_HOST` | Your Databricks workspace URL | `https://your-workspace.cloud.databricks.com` | ✅ |
| `DATABRICKS_TOKEN` | Personal access token or service principal token | `dapi-abc123def456...` | ✅ |
| `DATABRICKS_WAREHOUSE_ID` | SQL Warehouse ID for the app | `a9c09471e8c02f2e` | ✅ |

## 🎯 Environment-Specific Configuration

### Development Environment
- Uses secrets as-is
- Deploys when pushing to feature branches or manually selecting 'dev'

### Staging Environment  
- Uses same secrets (can be different workspace if needed)
- Deploys when pushing to `develop` branch or manually selecting 'staging'

### Production Environment
- Uses same secrets (should be production workspace)
- Deploys when pushing to `main` branch or manually selecting 'prod'
- **Recommendation**: Use service principal token for production

## 🔧 How to Get These Values

### DATABRICKS_HOST
1. Go to your Databricks workspace
2. Copy the URL from your browser
3. Example: `https://your-company.cloud.databricks.com`

### DATABRICKS_TOKEN
**For Development/Testing:**
1. In Databricks workspace → User Settings → Developer → Access Tokens
2. Generate new token
3. Copy the token (starts with `dapi-`)

**For Production (Recommended):**
1. Create a service principal in Databricks
2. Generate token for the service principal
3. Grant appropriate permissions

### DATABRICKS_WAREHOUSE_ID
1. In Databricks workspace → SQL Warehouses
2. Click on your warehouse
3. Copy the warehouse ID from the URL or connection details
4. Example: `a9c09471e8c02f2e`

## 🚀 Deployment Workflow

The GitHub Actions workflow will:

1. **Validate** the bundle configuration
2. **Deploy** using the secrets
3. **Configure** the warehouse ID via bundle variables
4. **Summary** shows deployment details

## 🔒 Security Best Practices

- ✅ Use service principals for production deployments
- ✅ Rotate tokens regularly
- ✅ Use environment-specific secrets if deploying to multiple workspaces
- ✅ Limit token permissions to minimum required scope
- ❌ Never commit tokens to code repository

## 📝 Setting Up Secrets

```bash
# In your GitHub repository:
# 1. Go to Settings → Secrets and variables → Actions
# 2. Click "New repository secret"
# 3. Add each secret with exact names listed above
```

Your CI/CD pipeline will automatically use these secrets to deploy your Databricks App! 🎉
