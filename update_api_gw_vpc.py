import boto3
import readline

client = boto3.client('apigateway', region_name='us-east-1')
con = True

def getResources(apiId):
    noVpc = 0
    try:
        resources = client.get_resources(
            restApiId=apiId,
            limit=500
        )
        print("----------------------------------------------------------------")
        print("\nAPI: "+str(apiId))
        for r in resources['items']:
            if 'resourceMethods' in r:
                for method in r['resourceMethods'].keys():
                    if method in ["ANY", "GET", "POST", "DELETE"]: 
                        intg = client.get_integration(
                            restApiId=apiId,
                            resourceId=r['id'],
                            httpMethod=method
                        )
                        if 'connectionType' in intg:
                            print("\n\tResource: '"+r['path']+"' ("+r['id']+")\n")
                            print("\t\tURI: "+str(intg['uri'])+"\n\t\tType: "+str(intg['httpMethod'])+"\n\t\tVPC Link: "+str(intg['connectionId']+"\n"))
                        else:
                            noVpc += 1
                    else:
                        break
        if noVpc > 0:
            print("\n\t"+str(noVpc)+" RECURSOS SEM VPC LINK")
    except KeyError:
        print("\n\t\tSEM VPC ID")
    #except Exception:
        #print("\n\t"+str(r['id'])+": INTEGRATION NÃO CONFIGURADA")
    return getStages(apiId)

def getStages(apiId):
    try:
        stages = client.get_stages(
            restApiId=apiId
        )
        for s in stages['item']:
            if 'variables' in s:
                print("\n\n\tStage: '"+str(s['stageName'])+"'")
                for k in s['variables']:
                    print("\n\t\t"+str(k)+": "+str(s['variables'][k]))
            else:
                print("\n\t"+str(s['stageName'])+": SEM STAGE VARIABLES")
    except Exception:
        traceback.print_exc()

def updateApiGw(apiId):
    print("== ATUALIZAÇÃO DE API GW ==")
    response = client.update_integration(
        restApiId=apiId,
        resourceId=input("Digite o ID do Recurso: "),
        httpMethod=input("Insira o método HTTP utilizado: "),
        patchOperations=[
            {
                'op': 'replace',
                'path': '/connectionId',
                'value': input("Digite o novo valor de VPC Link: ")
            },
            {
                'op': 'replace',
                'path': '/uri',
                'value': input("Digite o novo valor para a Endpoint URL: ")
            },
        ]
    )
    return deploy(apiId)

def deploy(apiId):
    deployed_stages = []
    print("\n")
    ans = input("Deseja realizar o DEPLOY? (y/N)   ")
    if ans.upper() == 'Y':
        stages = client.get_stages(
            restApiId=apiId
        )
        for s in stages['item']:
            deployed_stages.append(s['stageName']) 
        print("\nSTAGES existentes:  ",str(deployed_stages))
        stName = input("\n\nInsira o nome do STAGE:   ")
        stageValidation(apiId, deployed_stages, stName)

def stageValidation(apiId, stages, stName):
    if stName in stages:
        ans = input("\nRealizar deploy no STAGE '"+str(stName)+"'? (Y/n)   ")
        if ans.upper() == 'N':
            return deploy(apiId)
    else:
        ans = input("\nDeseja criar o STAGE '"+str(stName)+"' e efetuar o deploy? (y/N)   ")
        if ans.upper() != 'Y':
            return deploy(apiId)
    response = client.create_deployment(
        restApiId=apiId,
        stageName=stName
    )

def main():
    while con == True:
        apiId = input("Digite o ID da RestAPI: ")
        getResources(apiId)
        ans = input("\nDeseja atualizar o API GW visualizado? (Y/n)   ")
        if ans.upper() != 'N':
            updateApiGw(apiId)
        ans = input("\nAtualizar outro API GW? (Y/n)   ")
        if ans.upper() == 'N':
            print("\n\n== PROCEDIMENTO FINALIZADO ==")
            return 0
        print("----------------------------\n")

main()
