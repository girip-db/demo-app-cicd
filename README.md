# Databricks Table Viewer App

A simple, interactive Databricks app that allows users to browse and query tables across catalogs and schemas, displaying the first 100 rows of data.

## 🚀 Features

- **Catalog Selection**: Browse all available Unity Catalog catalogs
- **Schema Selection**: View schemas within selected catalogs
- **Table Selection**: Choose tables to query
- **Data Display**: View first 100 rows with a clean, responsive interface
- **CSV Export**: Download query results as CSV files
- **CI/CD Pipeline**: Automated deployment using GitHub Actions and Databricks Asset Bundles (DABS)

## 📋 Prerequisites

- Databricks workspace with Unity Catalog enabled
- SQL Warehouse configured
- Databricks CLI installed (for local deployment)
- GitHub repository (for CI/CD)

## 🛠️ Local Development

### 1. Clone the repository

```bash
git clone https://github.com/your-username/demo-app-cicd.git
cd demo-app-cicd
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

```bash
export DATABRICKS_SERVER_HOSTNAME="your-workspace.cloud.databricks.com"
export DATABRICKS_HTTP_PATH="/sql/1.0/warehouses/your-warehouse-id"
export DATABRICKS_TOKEN="your-access-token"
```

### 4. Run the app locally

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 🔧 Databricks Asset Bundle (DABS) Configuration

The project uses DABS for deployment management. The configuration is defined in `databricks.yml`.

### Project Structure

```
demo-app-cicd/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── databricks.yml             # DABS configuration
├── resources/
│   └── app.yml               # App resource definition
├── .github/
│   └── workflows/
│       └── deploy.yml        # CI/CD pipeline
└── README.md
```

### Deployment Targets

The project supports three deployment environments:

- **dev**: Development environment (default)
- **staging**: Staging/pre-production environment
- **prod**: Production environment

## 🚀 CI/CD with GitHub Actions

### Setup GitHub Secrets

Configure the following secrets in your GitHub repository (Settings > Secrets and variables > Actions):

1. `DATABRICKS_HOST`: Your Databricks workspace URL (e.g., `https://your-workspace.cloud.databricks.com`)
2. `DATABRICKS_TOKEN`: Databricks personal access token or service principal token  
3. `DATABRICKS_WAREHOUSE_ID`: Your SQL warehouse ID (e.g., `a9c09471e8c02f2e`)

See `GITHUB_SECRETS.md` for detailed instructions on obtaining these values.

### Deployment Workflow

The GitHub Actions workflow automatically deploys the app based on:

- **Push to `main` branch** → Deploys to **production**
- **Push to `develop` branch** → Deploys to **staging**
- **Pull requests** → Validates bundle configuration
- **Manual dispatch** → Deploy to any environment

### Manual Deployment

You can manually trigger deployment from GitHub:

1. Go to **Actions** tab in your repository
2. Select **Deploy Databricks App with DABS** workflow
3. Click **Run workflow**
4. Select the target environment (dev/staging/prod)
5. Click **Run workflow**

## 📦 Deploying with Databricks CLI

### Install Databricks CLI

```bash
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
```

### Configure Authentication

```bash
databricks configure --token
```

Enter your Databricks host and token when prompted.

### Deploy to Development

```bash
# Deploy the bundle
databricks bundle deploy -t dev

# Start the app
databricks bundle run -t dev demo_table_viewer
```

### Deploy to Staging

```bash
# Deploy the bundle
databricks bundle deploy -t staging

# Start the app
databricks bundle run -t staging demo_table_viewer
```

### Deploy to Production

```bash
# Deploy the bundle
databricks bundle deploy -t prod

# Start the app
databricks bundle run -t prod demo_table_viewer
```

## 🔐 Security Best Practices

1. **Use Service Principals**: For production deployments, use service principals instead of personal access tokens
2. **Rotate Tokens**: Regularly rotate Databricks tokens and GitHub secrets
3. **Least Privilege**: Grant only necessary permissions to the app and service principals
4. **Environment Isolation**: Keep dev, staging, and prod environments separate

## 📊 Using the App

1. **Access the App**: Navigate to the Databricks Apps section in your workspace
2. **Select Catalog**: Choose from available Unity Catalog catalogs
3. **Select Schema**: Pick a schema from the selected catalog
4. **Select Table**: Choose a table to query
5. **View Data**: The app displays the first 100 rows
6. **Download**: Export results as CSV using the download button

## 🐛 Troubleshooting

### Connection Issues

If you encounter connection errors:

- Verify your `DATABRICKS_TOKEN` is valid and not expired
- Check that the SQL Warehouse is running
- Ensure proper permissions are granted to access catalogs/schemas/tables

### Deployment Failures

If deployment fails:

- Validate your `databricks.yml` configuration: `databricks bundle validate`
- Check GitHub Actions logs for detailed error messages
- Verify all required secrets are configured in GitHub

### App Not Loading

If the app doesn't load in Databricks:

- Check the app logs in the Databricks workspace
- Verify the SQL Warehouse ID is correct
- Ensure all dependencies in `requirements.txt` are compatible


## 🔧 Troubleshooting

### Databricks App Issues

**App shows 500/505 error:**
- Ensure `app.yaml` command is simple: `["streamlit", "run", "app.py"]`
- Verify authentication logic detects Databricks Apps environment correctly
- Check SQL Warehouse ID is correct in the configuration

**App not accessible after deployment:**
- Make sure to run both commands: `databricks bundle deploy` AND `databricks bundle run`
- Verify GitHub secrets are set correctly
- Check app status in Databricks workspace → Apps section

### Local Development Issues

**Missing connection parameters error:**
- Run `./setup.sh` to create `.env` file template
- Verify `.env` contains valid Databricks credentials:
  - `DATABRICKS_SERVER_HOSTNAME`
  - `DATABRICKS_HTTP_PATH` 
  - `DATABRICKS_TOKEN`
- Ensure `load_dotenv()` is called before accessing environment variables

**Authentication errors:**
- Generate a new personal access token in Databricks
- Check token has proper permissions for SQL Warehouse access
- Verify workspace hostname format (no `https://` prefix in `.env`)

## 📋 Key Configuration Insights

### Environment Detection
| Environment | Detection Method | Authentication |
|-------------|------------------|----------------|
| **Databricks Apps** | `DATABRICKS_HOST` environment variable exists | Automatic (service principal) |
| **Local Development** | `.env` file credentials loaded | Manual (personal token) |

### Best Practices
1. **Keep `app.yaml` simple** - avoid port/address specifications
2. **Detect environment dynamically** in Python code  
3. **Use different authentication paths** for each environment
4. **Provide clear user feedback** about connection status
5. **Test both environments** to ensure compatibility


### Getting Started Options

Choose your path:
- **🚀 Quick Deploy**: Run `databricks bundle deploy -t dev && databricks bundle run -t dev demo_table_viewer`
- **💻 Local Test**: Run `./setup.sh` then `streamlit run app.py`
- **⚙️ Full CI/CD**: Push to GitHub with secrets configured