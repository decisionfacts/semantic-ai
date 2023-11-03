from semantic_ai.connectors import Sharepoint

CLIENT_ID = '<client_id>'  # sharepoint client id
CLIENT_SECRET = '<client_secret>'  # sharepoint client seceret
TENANT_ID = '<tenant_id>'  # sharepoint tenant id
SCOPE = 'https://graph.microsoft.com/.default'  # scope
HOST_NAME = "<tenant_name>.sharepoint.com"  # for example 'contoso.sharepoint.com'

# Sharepoint object creation
connection = Sharepoint(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        tenant_id=TENANT_ID,
                        host_name=HOST_NAME,
                        scope=SCOPE)

# List the sites
site_list = await connection.list_sites()

# Get the site id
site_id = await connection.connect("<site_name>")
print(site_id.get('id'))

# List the drives
drives = await connection.list_drives("<site_id>")

# List the folders
folders = await connection.list_folders("<site_id>", "<drive_id>")

# Download the files from particular url
download = await connection.download("<site_id>", "<drive_id>", "<folder_url>")
