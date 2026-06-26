import docker
import os

class DinDManager:
    """
    Gerencia a execução de código em containers efêmeros usando a API do Docker.
    Essencial para o loop /tdd e /diagnosing-bugs sem comprometer o host.
    """
    def __init__(self):
        try:
            # Tenta conectar ao daemon local. Se estiver rodando o docker-compose, 
            # ele pode usar variáveis de ambiente ou o socket local.
            self.client = docker.from_env()
        except Exception as e:
            print(f"[DinDManager] Aviso: Não foi possível conectar ao Docker. {e}")
            self.client = None

    def run_sandbox_test(self, image: str, command: str, script_content: str, filename: str = "script.py") -> dict:
        """
        Gera um arquivo na sandbox, roda um comando (ex: pytest) e retorna os logs.
        """
        if not self.client:
            return {"status": "FAILED", "logs": "Docker não está rodando no host."}
            
        print(f"[DinDManager] Executando sandbox com imagem {image}...")
        
        # Criação de volume temporário ou uso de command pipes
        # Para simplificar na v1, rodaremos o script injetando via shell
        escaped_script = script_content.replace('"', '\\"')
        
        full_command = f'sh -c "echo \\"{escaped_script}\\" > {filename} && {command}"'
        
        try:
            container = self.client.containers.run(
                image,
                full_command,
                remove=True,
                detach=False,
                stdout=True,
                stderr=True
            )
            logs = container.decode("utf-8")
            return {"status": "SUCCESS", "logs": logs}
        except docker.errors.ContainerError as e:
            logs = e.stderr.decode("utf-8") if e.stderr else str(e)
            return {"status": "FAILED", "logs": logs}
        except Exception as e:
            return {"status": "ERROR", "logs": str(e)}
