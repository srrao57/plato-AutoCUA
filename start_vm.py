import os
from plato.sandbox_sdk import PlatoSandboxClient
from plato.models.sandbox import CreateSnapshotRequest, PlatoConfig
import yaml


client = PlatoSandboxClient(api_key = os.environ['PLATO_API_KEY']) # get api key from plato.so/settings
dataset = 'base'
sim_name = 'baserowsrihas'

with open(f"{sim_name}/plato-config.yml", "r") as f:
    cfg = PlatoConfig.model_validate(yaml.safe_load(f))

sandbox = client.create_sandbox(config=cfg.datasets[dataset], wait=True, timeout=900)
ssh_response = client.setup_ssh(sandbox, cfg.datasets[dataset], dataset=dataset)
creds = client.get_gitea_credentials()
clone_url = f"https://{creds['username']}:{creds['password']}@hub.plato.so/{creds['org_name']}/{sim_name}"
breakpoint()