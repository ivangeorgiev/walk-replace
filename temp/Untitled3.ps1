
. $PSScriptRoot/../powershell/DoDatabricks.ps1

Connect-DoDatabricks -AccessToken 'dapi8fa2387ef69905382de7b96724c354fe'


{"scope":"MyKvScope","initial_manage_acl":null,"initial_manage_principal":null,"scope_backend_type":2,"backend_azure_keyvault":{"resource_id":"/subscriptions/29df80dc-0182-4e3e-940f-78eae6d7ae08/resourceGroups/learn-adf/providers/Microsoft.KeyVault/vaults/learn-adf-01-kv","dns_name":"https://learn-adf-01-kv.vault.azure.net/"},"is_databricks_managed":null,"encrypt_with_customer_key":null}


Invoke-WebRequest -Uri "https://westeurope.azuredatabricks.net/ajax-api/2.0/secrets/scopes/create" -Method "POST" -Headers @{"X-CSRF-Token"="9cc9006f-8ec6-4616-a17e-fb80ef151558"; "User-Agent"="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"; "Accept"="application/json, text/javascript, */*; q=0.01"; "X-Databricks-Org-Id"="8907199705255746"; "Sec-Fetch-Dest"="empty"; "X-Requested-With"="XMLHttpRequest"; "X-Databricks-Attribution-Tags"="%7B%22browserTabId%22%3A%22abe3fb53-8c16-4042-a385-3e65369d972f%22%2C%22browserHasFocus%22%3Atrue%2C%22browserIsHidden%22%3Afalse%2C%22browserHash%22%3A%22%23secrets%2FcreateScope%22%2C%22browserHostName%22%3A%22westeurope.azuredatabricks.net%22%2C%22browserUserAgent%22%3A%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F80.0.3987.132%20Safari%2F537.36%22%2C%22eventWindowTime%22%3A58207.325000315905%2C%22clientBranchName%22%3A%223.15.2123%22%2C%22browserIdleTime%22%3A220%7D"; "Origin"="https://westeurope.azuredatabricks.net"; "Sec-Fetch-Site"="same-origin"; "Sec-Fetch-Mode"="cors"; "Referer"="https://westeurope.azuredatabricks.net/?o=8907199705255746"; "Accept-Encoding"="gzip, deflate, br"; "Accept-Language"="en-US,en;q=0.9,bg-BG;q=0.8,bg;q=0.7"; "Cookie"="workspace-url=westeurope.azuredatabricks.net; JSESSIONID=auth-auth-7f5c8b84b6-5dv2bwf3ih6360h856o39kz5idfbs.webapp-cons-webapp-4"} -ContentType "application/x-www-form-urlencoded; charset=UTF-8" -Body "{`"scope`":`"MyKvScope`",`"initial_manage_acl`":null,`"initial_manage_principal`":null,`"scope_backend_type`":2,`"backend_azure_keyvault`":{`"resource_id`":`"/subscriptions/29df80dc-0182-4e3e-940f-78eae6d7ae08/resourceGroups/learn-adf/providers/Microsoft.KeyVault/vaults/learn-adf-01-kv`",`"dns_name`":`"https://learn-adf-01-kv.vault.azure.net/`"},`"is_databricks_managed`":null,`"encrypt_with_customer_key`":null}";
Invoke-WebRequest -Uri "https://westeurope.azuredatabricks.net/health?_=1585254619207" -Headers @{"X-CSRF-Token"="9cc9006f-8ec6-4616-a17e-fb80ef151558"; "User-Agent"="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"; "Accept"="*/*"; "X-Databricks-Org-Id"="8907199705255746"; "Sec-Fetch-Dest"="empty"; "X-Requested-With"="XMLHttpRequest"; "X-Databricks-Attribution-Tags"="%7B%22browserTabId%22%3A%22abe3fb53-8c16-4042-a385-3e65369d972f%22%2C%22browserHasFocus%22%3Atrue%2C%22browserIsHidden%22%3Afalse%2C%22browserHash%22%3A%22%23secrets%2FcreateScope%22%2C%22browserHostName%22%3A%22westeurope.azuredatabricks.net%22%2C%22browserUserAgent%22%3A%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F80.0.3987.132%20Safari%2F537.36%22%2C%22eventWindowTime%22%3A61008.25000042096%2C%22clientBranchName%22%3A%223.15.2123%22%2C%22browserIdleTime%22%3A2322%7D"; "Sec-Fetch-Site"="same-origin"; "Sec-Fetch-Mode"="cors"; "Referer"="https://westeurope.azuredatabricks.net/?o=8907199705255746"; "Accept-Encoding"="gzip, deflate, br"; "Accept-Language"="en-US,en;q=0.9,bg-BG;q=0.8,bg;q=0.7"; "Cookie"="workspace-url=westeurope.azuredatabricks.net; JSESSIONID=auth-auth-7f5c8b84b6-5dv2bwf3ih6360h856o39kz5idfbs.webapp-cons-webapp-4"}


$Global:DoDatabricksURI
$Headers = Get-DoDatabricksHeaders

Invoke-RestMethod -Uri "$Global:DoDatabricksURI/api/2.0/secrets/scopes/list" -Headers $Headers -Method "GET" 

$Body = '{"scope":"MyKvScope1","initial_manage_acl":null,"initial_manage_principal":null,"scope_backend_type":2,"userAADToken":"xyzy","backend_azure_keyvault":{"resource_id":"/subscriptions/29df80dc-0182-4e3e-940f-78eae6d7ae08/resourceGroups/learn-adf/providers/Microsoft.KeyVault/vaults/learn-adf-01-kv","dns_name":"https://learn-adf-01-kv.vault.azure.net/"},"is_databricks_managed":null,"encrypt_with_customer_key":null}'
Invoke-RestMethod -Uri "$Global:DoDatabricksURI/api/2.0/secrets/scopes/create" -Headers $Headers -Method "POST" -Body $Body


$Secret = "-j7qA3/-9QelM2J=9U8bm9A3e3v.FcHv"
$ApplicationId = "b008cf3a-fde3-447c-9977-050ec9d2d161"
$tenantId = "0ffdfde4-8090-4bd8-ab2e-b4112d4be8e3"
$SubscriptionId = "29df80dc-0182-4e3e-940f-78eae6d7ae08"
$ResourceGroupName = "learn-adf"
$WorkspaceName = "learn-adf"
$AzureRegion = "westeurope"

$URI = "https://login.microsoftonline.com/$tenantId/oauth2/token/"
$DatabricksURI = "https://$AzureRegion.azuredatabricks.net"

# $Secret_Encoded = [System.Web.HttpUtility]::UrlEncode($Secret)
$Secret_Encoded = [uri]::EscapeDataString($Secret)
$BodyText="grant_type=client_credentials&client_id=$ApplicationId&resource=https://management.core.windows.net/&client_secret=$Secret_Encoded"
$Response = Invoke-RestMethod -Method POST -Body $BodyText -Uri $URI -ContentType application/x-www-form-urlencoded
$ManagementAccessToken = $Response.access_token
$ManagementRefreshToken = $Response.refresh_token
$ManagementTokenExpires = (Get-Date).AddSeconds($Response.expires_in)

$BodyText="grant_type=client_credentials&client_id=$ApplicationId&resource=2ff814a6-3304-4ab8-85cb-cd0e6f879c1d&client_secret=$Secret_Encoded"
$Response = Invoke-RestMethod -Method POST -Body $BodyText -Uri $URI -ContentType application/x-www-form-urlencoded

$DatabricksAccessToken = $Response.access_token
$DatabricksRefeshToken = $Response.refresh_token
$DatabricksTokenExpires = (Get-Date).AddSeconds($Response.expires_in)

$DatabricksHeaders = @{"Authorization"="Bearer $DatabricksAccessToken";
    "X-Databricks-Azure-SP-Management-Token"=$ManagementAccessToken;
    "X-Databricks-Azure-Workspace-Resource-Id"="/subscriptions/$SubscriptionId/resourceGroups/$ResourceGroupName/providers/Microsoft.Databricks/workspaces/$WorkspaceName"
}



$Body = '{"scope":"MyKvScope1","initial_manage_acl":null,"initial_manage_principal":null,"scope_backend_type":2,"backend_azure_keyvault":{"resource_id":"/subscriptions/29df80dc-0182-4e3e-940f-78eae6d7ae08/resourceGroups/learn-adf/providers/Microsoft.KeyVault/vaults/learn-adf-01-kv","dns_name":"https://learn-adf-01-kv.vault.azure.net/"},"is_databricks_managed":null,"encrypt_with_customer_key":null}'
Invoke-RestMethod -Uri "$Global:DoDatabricksURI/api/2.0/secrets/scopes/create" -Headers $DatabricksHeaders -Method "POST" -Body $Body

# AZURE_KEYVAULT
$Body = '{"scope":"MyKvScope1","initial_manage_principal":"users","scope_backend_type":"AZURE_KEYVAULT", "backend_azure_keyvault":{"resource_id":"/subscriptions/29df80dc-0182-4e3e-940f-78eae6d7ae08/resourceGroups/learn-adf/providers/Microsoft.KeyVault/vaults/learn-adf-01-kv","dns_name":"https://learn-adf-01-kv.vault.azure.net/","is_databricks_managed":null,"encrypt_with_customer_key":null}}'
$Headers = Get-DoDatabricksHeaders
Invoke-RestMethod -Uri "$Global:DoDatabricksURI/api/2.0/secrets/scopes/create" -Headers $Headers -Method "POST" -Body $Body

Invoke-RestMethod -Uri "$Global:DoDatabricksURI/api/2.0/secrets/scopes/delete" -Headers $Headers -Method "POST" -Body '{"scope":"MyKvScope1"}'


$Scopes = Invoke-RestMethod -Uri "$Global:DoDatabricksURI/api/2.0/secrets/scopes/list" -Headers $Headers -Method "GET"
Write-Host $Scopes.scopes[0].keyvault_metadata.dns_name

