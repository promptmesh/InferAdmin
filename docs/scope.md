# Scope for MVP:

## Features:
- Local Model storage
    - Unified location
    - Downloading models
    - Updating models
    - Deleting models
    - Storage available

- Deploy vLLM docker
    - Deploy instance
    - Stop instance
    - Status of instance (Docker health check)

- vLLM container version control
    - Dropdown for selecting vLLM container version
    - Checkbox for most recent version
    - Nightly job to pull available version to populate dropdown

- Deploy OpenWebUI
    - Initial config
    - Status
    - Delete
    - Stopping
    - Status of instance (Docker health check)

- GPU state
    - Vram load
    - Utilization
    - Power consumption?

- Use health checks for containers
- Unified local model location

## Config

### LLM Specific
- Ability to set all the args for vLLM when launching instance (pydantic)

### Host Specific
- Unified location of model
- The port/interface (default to 0.0.0.0) where is deployed on
- Nvidia docker toolkit installed
- Refresh interval for gpu state
- Refresh interval for container state
- HF token

## Operating Data
- What assets are deployed via docker

## Stack
- Deploy InferAdmin in docker
- InferAdmin interacts with host docker to deploy docker containers for inference/interface
- FastApi for backend
- Frontend html/css/js (maybe do VueJS)
- YML for config and data, pydantic for representation

## Ideas
- Gpu assignment per instance
- Proxy server in front of vLLM to handle loading/unloading of models
- Stuff other than vLLM
- Have multiple storage locations

## Initial assumption
- Nvidia gpus
- All gpus are same type
- Interface launches on all exposed via 0.0.0.0