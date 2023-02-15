import boto3
import traceback

client = boto3.client('apigateway', region_name='sa-east-1')
apiGWs = client.get_rest_apis(limit=200)
count = 1

def get_resources(api):
    global client, count
    noVpc = 0
    try:
        resources = client.get_resources(
            restApiId=api['id'],
            limit=500
        )
        print("----------------------------------------------------------------")
        print("\n"+str(count)+") "+str(api['name'])+" ("+str(api['id'])+") :")
        count += 1
        for r in resources['items']:
            if 'resourceMethods' in r:
                for method in r['resourceMethods'].keys():
                    if method in ["ANY", "GET", "POST", "DELETE"]: 
                        intg = client.get_integration(
                            restApiId=api['id'],
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
    except Exception:
        print("\n\t"+str(r['id'])+": INTEGRATION NÃO CONFIGURADA")
def get_stages(api):
    global client
    try:
        stages = client.get_stages(
            restApiId=api['id']
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

for api in apiGWs['items']:
    get_resources(api) 
    get_stages(api)
    print("\n")
