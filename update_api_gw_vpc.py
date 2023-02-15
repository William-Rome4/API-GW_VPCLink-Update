import boto3
import readline

client = boto3.client('apigateway', region_name='us-east-1')
con = True

def updateApiGw():
    print("== ATUALIZAÇÃO DE API GW ==")
    apiId = input("Digite o ID da RestAPI: ")
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
        try:
            updateApiGw()
            ans = input("\nAtualizar outro API GW? (Y/n)   ")
            if ans.upper() == 'N':
                print("\n\n== PROCEDIMENTO FINALIZADO ==")
                return 0
            print("----------------------------\n")
        except Exception as e:
            print("\n[ERROR]",e,"\n")

main()
