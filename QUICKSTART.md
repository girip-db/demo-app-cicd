# Quick Start Guide

Get your Databricks Table Viewer app up and running in minutes!

## 🎯 Option 1: Deploy to Databricks (Recommended)

### Step 1: Install Databricks CLI

```bash
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
```

### Step 2: Configure Databricks CLI

```bash
databricks configure --token
```

Enter:
- **Databricks Host**: `https://your-workspace.cloud.databricks.com`
- **Token**: Your personal access token (generate from User Settings > Access Tokens)

### Step 3: Update Configuration

Edit `databricks.yml` and set your SQL Warehouse ID:

```yaml
variables:
  warehouse_id:
    default: "your-warehouse-id-here"
```

### Step 4: Deploy and Run

```bash
# Deploy to development
databricks bundle deploy -t dev

# Start the app
databricks bundle run -t dev demo_table_viewer

# Or deploy to production
databricks bundle deploy -t prod
databricks bundle run -t prod demo_table_viewer
```

### Step 5: Access Your App

Go to your Databricks workspace → **Apps** → Find your deployed app!

---

## 🖥️ Option 2: Run Locally

### Step 1: Run Setup Script

```bash
./setup.sh
```

### Step 2: Configure Environment

Edit `.env` file with your credentials:

```bash
DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
DATABRICKS_TOKEN=dapi-your-token-here
```

### Step 3: Activate Virtual Environment

```bash
source venv/bin/activate
```

### Step 4: Run the App

```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser!

**Note**: The app automatically detects whether it's running locally or in Databricks Apps and uses the appropriate authentication method.

---

## 🚀 Option 3: CI/CD with GitHub Actions

### Step 1: Create GitHub Repository

```bash
# Add remote
git remote add origin https://github.com/your-username/demo-app-cicd.git

# Add all files
git add .
git commit -m "Initial commit: Databricks Table Viewer App"

# Push to GitHub
git push -u origin main
```

### Step 2: Configure GitHub Secrets

Go to **Settings** > **Secrets and variables** > **Actions** and add:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `DATABRICKS_HOST` | Workspace URL | `https://your-workspace.cloud.databricks.com` |
| `DATABRICKS_TOKEN` | Access token | `dapi-xxxxxxxxxxxxx` |
| `WAREHOUSE_ID` | SQL Warehouse ID | `abc123def456` |

### Step 3: Automatic Deployment

The app will automatically deploy when you:
- Push to `main` → Deploys to **production**
- Push to `develop` → Deploys to **staging**
- Open PR → Validates configuration

### Step 4: Manual Deployment

1. Go to **Actions** tab
2. Select **Deploy Databricks App with DABS**
3. Click **Run workflow**
4. Choose environment (dev/staging/prod)
5. Click **Run workflow**

---

## 📊 Using the App

1. **Select Catalog**: Choose from available Unity Catalogs
2. **Select Schema**: Pick a schema from the catalog
3. **Select Table**: Choose a table to view
4. **View Data**: See the first 100 rows
5. **Download**: Export to CSV

---

## 🔑 Getting Databricks Credentials

### SQL Warehouse ID

1. Go to **SQL Warehouses** in Databricks
2. Click on your warehouse
3. Copy the ID from the URL or connection details

### Access Token

1. Click your user icon (top right)
2. Go to **User Settings**
3. Select **Developer** > **Access tokens**
4. Click **Generate new token**
5. Copy and save securely

### Workspace URL

Your workspace URL looks like:
- `https://adb-123456789.azuredatabricks.net` (Azure)
- `https://your-workspace.cloud.databricks.com` (AWS/GCP)

---

## ❓ Troubleshooting

### "Connection failed"
- Verify your token is valid
- Check SQL Warehouse is running
- Ensure correct permissions

### "No catalogs available"
- Grant proper Unity Catalog permissions
- Check your user has access to catalogs

### GitHub Actions failing
- Verify all secrets are set correctly
- Check token permissions
- Review workflow logs for details

---

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize the app in `app.py`
- Modify DABS configuration in `databricks.yml`
- Add custom GitHub Actions workflows

---

**Need help?** Open an issue or check the [Databricks documentation](https://docs.databricks.com/).

