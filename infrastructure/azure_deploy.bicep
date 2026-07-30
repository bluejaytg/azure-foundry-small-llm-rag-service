param location string = 'eastus'
param workspaceName string = 'azure-ai-foundry-ws'

resource aiServices 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: workspaceName
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  properties: {
    customSubDomainName: workspaceName
    publicNetworkAccess: 'Enabled'
  }
}

output endpoint string = aiServices.properties.endpoint