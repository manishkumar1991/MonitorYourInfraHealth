import sys
from azure.identity import DefaultAzureCredential
import csv
import json
import requests

workspace_id = "c64eb659-e5d8-4727-a9cd-ea4a085138e6"
workspaceName = "personal-workspace"
resourceGroupName = "test_infrastructure"
subscriptionId = "f70efef4-6505-4727-acd8-9d0b3bc0b80e"
dataCollectionEndpointname = "ingestsamplelogs"

lia_supported_builtin_table = ['ADAssessmentRecommendation','ADSecurityAssessmentRecommendation','Anomalies','ASimAuditEventLogs','ASimAuthenticationEventLogs','ASimDhcpEventLogs','ASimDnsActivityLogs','ASimDnsAuditLogs','ASimFileEventLogs','ASimNetworkSessionLogs','ASimProcessEventLogs','ASimRegistryEventLogs','ASimUserManagementActivityLogs','ASimWebSessionLogs','AWSCloudTrail','AWSCloudWatch','AWSGuardDuty','AWSVPCFlow','AzureAssessmentRecommendation','CommonSecurityLog','DeviceTvmSecureConfigurationAssessmentKB','DeviceTvmSoftwareVulnerabilitiesKB','ExchangeAssessmentRecommendation','ExchangeOnlineAssessmentRecommendation','GCPAuditLogs','GoogleCloudSCC','SCCMAssessmentRecommendation','SCOMAssessmentRecommendation','SecurityEvent','SfBAssessmentRecommendation','SharePointOnlineAssessmentRecommendation','SQLAssessmentRecommendation','StorageInsightsAccountPropertiesDaily','StorageInsightsDailyMetrics','StorageInsightsHourlyMetrics','StorageInsightsMonthlyMetrics','StorageInsightsWeeklyMetrics','Syslog','UCClient','UCClientReadinessStatus','UCClientUpdateStatus','UCDeviceAlert','UCDOAggregatedStatus','UCServiceUpdateStatus','UCUpdateAlert','WindowsEvent','WindowsServerAssessmentRecommendation']
reserved_columns = ["_ResourceId", "id", "_SubscriptionId", "TenantId", "Type", "UniqueId", "Title","_ItemId"]
def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    print(f"Content of {file_path}:\n{content}")

def convert_schema_csv_to_json(csv_file):
    data = []
    with open(csv_file, 'r',encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['ColumnName'] in reserved_columns:
                continue
            elif row['ColumnType'] == "bool":
                data.append({        
                'name': row['ColumnName'],
                'type': "boolean",
                })
            else:
                data.append({        
                'name': row['ColumnName'],
                'type': row['ColumnType'],
                })           
    return data

def convert_data_csv_to_json(csv_file):
    data = []
    with open(csv_file, 'r',encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            table_name=row['Type']
            data.append(row)       
    return data , table_name

def check_for_custom_table(table_name):
    if table_name in lia_supported_builtin_table:
        log_ingestion_supported=True
        table_type="builtin"
    if table_name not in lia_supported_builtin_table:
        if table_name.endswith('_CL') or table_name.endswith('_cl'):
            log_ingestion_supported=True
            table_type="custom_log"           
        else:
            log_ingestion_supported=False
            table_type="unknown"
    return log_ingestion_supported,table_type

def create_table(schema,table):
     request_object = {
    "properties": {
        "schema": {
        "name": table,
        "columns": json.loads(schema)
        },
        "retentionInDays": 30,
        "totalRetentionInDays": 30
    }
    }
     method="PUT"
     url=f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.OperationalInsights/workspaces/{workspaceName}/tables/{table}?api-version=2022-10-01"
     return request_object , url , method

def create_dcr(schema,table):
    dcrname=table+"_DCR"
    request_object={  
            "location": "eastus", 			
            "properties": {
                "streamDeclarations": {
                    "Custom-dcringestlogs": {
                        "columns": json.loads(schema)
                    }
                },				
			"dataCollectionEndpointId": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Insights/dataCollectionEndpoints/{dataCollectionEndpointname}",			
              "dataSources": {}, 
              "destinations": { 
                "logAnalytics": [ 
                  { 
                    "workspaceResourceId": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.OperationalInsights/workspaces/{workspaceName}",
                    "workspaceId": workspace_id,
                    "name": "DataCollectionEventCEF" 
                  } 
                ] 
              }, 
              "dataFlows": [ 
                    {
                        "streams": [
                            "Custom-dcringestlogs"
                        ],
                        "destinations": [
                            "DataCollectionEventCEF"
                        ],
                        "transformKql": "source",
                        "outputStream": f"Custom-{table}"
                    } 
                        ] 
                }
        }
    method="PUT"
    url=f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Insights/dataCollectionRules/{dcrname}?api-version=2022-06-01"
    return request_object , url , method


def get_access_token():
    credential = DefaultAzureCredential()
    token = credential.get_token('https://management.azure.com/.default')
    return token.token   

def hit_api(url,request,method):
    access_token = get_access_token()
    headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
    }
    response = requests.request(method, url, headers=headers, json=request)	
    return response


if __name__ == "__main__":
	current_directory = os.path.dirname(os.path.abspath(__file__))
	GetModifiedFiles = f"git diff --name-only origin/main {current_directory}/../../../Parsers/"
	try:
        	modified_files = subprocess.run(GetModifiedFiles, shell=True, text=True, capture_output=True, check=True)
    	except subprocess.CalledProcessError as e:
        	print(f"::error::An error occurred while executing the command: {e}")
        	sys.stdout.flush()  # Explicitly flush stdout
	print(modified_files)
