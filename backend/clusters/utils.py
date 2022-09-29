from subprocess import Popen
import os, time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def call_and_print(command):
    print(os.popen(command).read())

def check_pod_ready():
    cmd = os.popen('kubectl describe pods --namespace openfaas | findstr Ready:')
    readyList = cmd.readlines()
    for x in readyList:
        str = x.replace('\n','').replace(' ', '').replace("Ready:", '')
        if str == "False":
            return False
    return True

def forward():
    Popen(['kubectl','port-forward','-n','openfaas', 'svc/gateway' ,'8080:8080'])

def destroy_cluster():
    call_and_print('terraform destroy -auto-approve')

def register_faas():
    call_and_print('faas-cli login -g http://127.0.0.1:8080 -u admin --password "12345"')

def deploy_cluster():
    call_and_print(f'terraform -chdir={BASE_DIR} apply -auto-approve')
    call_and_print(
        'kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml')
    call_and_print(
        'helm repo add openfaas https://openfaas.github.io/faas-netes/')
    call_and_print('helm repo update')
    call_and_print(
        'kubectl -n openfaas create secret generic basic-auth --from-literal=basic-auth-user=admin --from-literal=basic-auth-password="12345"')
    call_and_print(
        'helm upgrade openfaas --install openfaas/openfaas --namespace openfaas --set functionNamespace=openfaas-fn --set basic_auth=true')
    ready = check_pod_ready()
    while(not ready):
        time.sleep(10)
        count = 10
        ready = check_pod_ready()
        print("Pods are ready: ", ready, f"Seconds {count}")
        count += 10 
    
    print("Ready for use")
    forward()

def read_terraform_file(name, agents, memory):
    root = str(Path(__file__).resolve().parent.parent)
    terraform_file = open(root+"\main.tf", "r")
    list_of_lines = terraform_file.readlines()
    list_of_lines[26] = '  name  = '+f'"{name}" \n'
    list_of_lines[28] = '  agents  = '+f'{agents} \n'
    list_of_lines[55] = '    agents_memory= "'+f'{memory}M" \n'

    terraform_file = open(root+"\main.tf", "w")
    terraform_file.writelines(list_of_lines)
    terraform_file.close()