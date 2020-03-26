function Connect-DoDatabricks {
    param(
        [string]
        $AccessToken,

        [string]
        $AzureRegion = 'westeurope'
    )

    $Global:DoDatabricksAccessToken = $AccessToken
    $Global:DoDatabricksURI = "https://$AzureRegion.azuredatabricks.net"
    $Global:DoDatabricksHeaders = @{
        "Authorization"="Bearer $AccessToken"
    }
}

function Get-DoDatabricksHeaders {
    if (!$Global:DoDatabricksAccessToken -or !$Global:DoDatabricksHeaders) {
        Throw "Databricks is not connected. Consider using Connect-DoDatabricks first"
    }

    return $Global:DoDatabricksHeaders
}

function Get-DoDatabricksCluster([string]$ClusterName) {
    $Headers = Get-DoDatabricksHeaders

    $RequestUri = "${Global:DoDatabricksURI}/api/2.0/clusters/list"
    $RequestUri = [uri]::EscapeUriString($RequestUri)

    $Response = (Invoke-RestMethod -Uri "$RequestUri" -Method 'GET' -Headers $Headers).clusters
    if ($ClusterName) {
        $Response = $Response | Where-Object -Property cluster_name -EQ $ClusterName
    }
    return $Response
}

function Ensure-DoDatabricksCluster {
    param(
        [string]
        $ClusterName,
        
        [string]$SparkVersion = "6.4.x-scala2.11",
        [string]$WorkerNodeType = "Standard_DS3_v2",
        [string]$DriverNodeType = "Standard_DS3_v2",
        [int]$AutoterminationMinutes = 60,
        [int]$MinWorkers = 1,
        [int]$MaxWorkers = 2
    )

    $CurrentCluster = Get-DoDatabricksCluster -ClusterName $ClusterName
    if ($CurrentCluster) {
        if ($CurrentCluster -is [array]) {
            Write-Warning "Mulltiple results returned for $ClusterName"
            $CurrentCluster = $CurrentCluster[0]
        }
        return $CurrentCluster.cluster_id
    }


    $ClusterSettings = @{
       "cluster_name" = $ClusterName;
       "spark_version" = $SparkVersion;
       "node_type_id" = $WorkerNodeType;
       "driver_node_type_id" = $DriverNodeType;
       "autotermination_minutes" = $AutoterminationMinutes;
       "autoscale" = @{
         "min_workers" = $MinWorkers;
         "max_workers" = $MaxWorkers
       }
    }

    $Headers = Get-DoDatabricksHeaders

    $Body = $ClusterSettings | ConvertTo-Json -Depth 10
    $RequestUri = "${Global:DoDatabricksURI}/api/2.0/clusters/create"
    $RequestUri = [uri]::EscapeUriString($RequestUri)
    $Response = Invoke-RestMethod -Uri "$RequestUri" -Method 'POST' -Headers $Headers -Body $Body

    return $Response.cluster_id
}
