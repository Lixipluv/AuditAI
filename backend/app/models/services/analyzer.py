import docker
import json
import os

def run_slither_analysis(contract_filename: str, solc_version: str = "0.8.23"):
    client = docker.from_env()
    container = client.containers.get('smart_read_analyzer')

    # Ajuste para garantir que a versão correta do Solidity é usada
    cmd = f'/bin/bash -c "solc-select install {solc_version} && solc-select use {solc_version} && solc --version && slither /share/contracts/{contract_filename} --json /share/reports/{contract_filename}_report.json"'

    exit_code, output = container.exec_run(cmd)

    if exit_code != 0:
        return {"success": False, "error": output.decode("utf-8")}

    reports_dir = os.path.join(os.getcwd(), 'backend', 'app', 'reports')
    report_path = os.path.join(reports_dir, f"{contract_filename}_report.json")

    with open(report_path, 'r', encoding='utf-8') as f:
        analysis_result = json.load(f)

    return {"success": True, "result": analysis_result}
