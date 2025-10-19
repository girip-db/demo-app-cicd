import streamlit as st
from databricks import sql
import os
import pandas as pd
from dotenv import load_dotenv
from databricks.sdk.core import Config



# Load environment variables from .env file FIRST
load_dotenv()

cfg = Config() 

# Get connection parameters from environment variables or use defaults
server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
http_path = os.getenv("DATABRICKS_HTTP_PATH")
access_token = os.getenv("DATABRICKS_TOKEN")
warehouse_id = os.getenv("DATABRICKS_WAREHOUSE_ID")  # Default fallback

# Configure the page
st.set_page_config(
    page_title="Databricks Table Viewer",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Databricks Table Viewer")
st.markdown("Select a catalog, schema, and table to view the first 100 rows of data.")

def get_connection():
    """Create a connection to Databricks SQL warehouse."""
    try:
        # Better detection: Check if DATABRICKS_HOST is set automatically (Databricks Apps)
        # vs manually via .env file (local development)
        databricks_host_env = os.getenv("DATABRICKS_HOST")
        is_databricks_app = databricks_host_env is not None and not server_hostname
        
        if is_databricks_app:
            # Use automatic authentication for Databricks Apps
            st.info("🔗 Connecting to Databricks using app authentication...")
            st.info(f"📍 Detected Databricks Apps environment")
            # In Databricks Apps, use the DATABRICKS_HOST environment variable
            databricks_host = databricks_host_env.replace("https://", "")
            connection = sql.connect(
                server_hostname=databricks_host,
                http_path=f"/sql/1.0/warehouses/{warehouse_id}",
                credentials_provider=lambda: cfg.authenticate 
            )
        else:
            # Use environment variables for local development
            st.info("📍 Detected local development environment")
            # For local development, all credentials are required
            if not all([server_hostname, http_path, access_token]):
                st.error("❌ Missing Databricks connection parameters for local development!")
                st.error("Please set the following in your .env file:")
                st.error("- DATABRICKS_SERVER_HOSTNAME")
                st.error("- DATABRICKS_HTTP_PATH") 
                st.error("- DATABRICKS_TOKEN")
                if not access_token:
                    st.error("💡 DATABRICKS_TOKEN is only required for local development")
                return None
                
            st.info(f"🔗 Connecting to Databricks at {server_hostname}...")
            connection = sql.connect(
                server_hostname=server_hostname,
                http_path=http_path,
                access_token=access_token
            )
        
        st.success("✅ Connected to Databricks successfully!")
        return connection
        
    except Exception as e:
        st.error(f"❌ Failed to connect to Databricks: {str(e)}")
        st.error("Please check your Databricks connection settings.")
        
        # Show debugging info
        st.error("🔍 **Environment Debugging Info:**")
        st.error(f"- DATABRICKS_HOST (auto): {databricks_host_env}")
        st.error(f"- DATABRICKS_SERVER_HOSTNAME (.env): {server_hostname}")
        st.error(f"- Detected environment: {'Databricks Apps' if is_databricks_app else 'Local Development'}")
        st.error(f"- SQL Warehouse ID: {warehouse_id}")
        st.error(f"- SQL Warehouse Path: /sql/1.0/warehouses/{warehouse_id}")
        return None

def get_catalogs(connection):
    """Fetch all available catalogs."""
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW CATALOGS")
        catalogs = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return catalogs
    except Exception as e:
        st.error(f"Error fetching catalogs: {str(e)}")
        return []

def get_schemas(connection, catalog):
    """Fetch all schemas in the selected catalog."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"SHOW SCHEMAS IN {catalog}")
        schemas = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return schemas
    except Exception as e:
        st.error(f"Error fetching schemas: {str(e)}")
        return []

def get_tables(connection, catalog, schema):
    """Fetch all tables in the selected schema."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"SHOW TABLES IN {catalog}.{schema}")
        tables = [row[1] for row in cursor.fetchall()]  # Second column is table name
        cursor.close()
        return tables
    except Exception as e:
        st.error(f"Error fetching tables: {str(e)}")
        return []

def query_table(connection, catalog, schema, table, limit=100):
    """Query the selected table and return results as a pandas DataFrame."""
    try:
        cursor = connection.cursor()
        query = f"SELECT * FROM {catalog}.{schema}.{table} LIMIT {limit}"
        cursor.execute(query)
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        # Fetch data
        rows = cursor.fetchall()
        cursor.close()
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(rows, columns=columns)
        return df
    except Exception as e:
        st.error(f"Error querying table: {str(e)}")
        return None

# Main app logic
def main():
    """Main function to run the Streamlit app."""
    
    # Display environment info
    databricks_host_env = os.getenv("DATABRICKS_HOST")
    is_databricks_app = databricks_host_env is not None and not server_hostname
    
    if is_databricks_app:
        st.info("🚀 Running in Databricks Apps environment")
        st.info(f"📍 Databricks Host: {databricks_host_env}")
    else:
        st.info("💻 Running in local development environment")
        st.info(f"📍 Using .env credentials for: {server_hostname}")
        # Check if .env parameters are set for local development
        # Note: DATABRICKS_TOKEN only required for local, not Databricks Apps
        if not all([server_hostname, http_path, access_token]):
            st.warning("""
            ⚠️ **Local Development Setup Required**
            
            Please set the following environment variables in your `.env` file:
            - `DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com`
            - `DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id`  
            - `DATABRICKS_TOKEN=dapi-your-token-here` (local development only)
            
            Run `./setup.sh` to create the .env file template.
            
            💡 Note: DATABRICKS_TOKEN is not needed when deployed to Databricks Apps
            """)
            return
    
    # Establish connection
    connection = get_connection()
    if not connection:
        return
    
    # Create three columns for selectors
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("1️⃣ Select Catalog")
        catalogs = get_catalogs(connection)
        if catalogs:
            selected_catalog = st.selectbox("Catalog", catalogs, key="catalog")
        else:
            st.warning("No catalogs available")
            return
    
    with col2:
        st.subheader("2️⃣ Select Schema")
        if selected_catalog:
            schemas = get_schemas(connection, selected_catalog)
            if schemas:
                selected_schema = st.selectbox("Schema", schemas, key="schema")
            else:
                st.warning("No schemas available")
                return
        else:
            selected_schema = None
    
    with col3:
        st.subheader("3️⃣ Select Table")
        if selected_catalog and selected_schema:
            tables = get_tables(connection, selected_catalog, selected_schema)
            if tables:
                selected_table = st.selectbox("Table", tables, key="table")
            else:
                st.warning("No tables available")
                return
        else:
            selected_table = None
    
    # Query and display data
    if selected_catalog and selected_schema and selected_table:
        st.markdown("---")
        st.subheader(f"📋 Data from `{selected_catalog}.{selected_schema}.{selected_table}`")
        
        with st.spinner("Loading data..."):
            df = query_table(connection, selected_catalog, selected_schema, selected_table)
            
            if df is not None:
                # Display metrics
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Rows Displayed", len(df))
                with col_b:
                    st.metric("Columns", len(df.columns))
                with col_c:
                    st.metric("Table", selected_table)
                
                # Display the dataframe
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"{selected_catalog}_{selected_schema}_{selected_table}.csv",
                    mime="text/csv"
                )
    
    # Close connection
    connection.close()

if __name__ == "__main__":
    main()

