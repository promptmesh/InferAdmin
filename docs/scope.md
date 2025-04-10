# Scope for MVP:

## Features:
- Local Model storage
    - Unified location
    - Downloading models (asynchronously)
    - Updating models
    - Deleting models (asynchronously)
    - Storage available

- Deploy vLLM docker
    - Deploy instance (asynchronously)
    - Stop instance (asynchronously)
    - Status of instance (Docker health check)
    - Attach GPUs to instance

- vLLM container version control
    - Dropdown for selecting vLLM container version
    - Checkbox for most recent version
    - Nightly job to pull available version to populate dropdown

- Deploy OpenWebUI
    - Initial config
    - Status
    - Delete
    - Stopping (asynchronously)
    - Status of instance (Docker health check)

- GPU state
    - Vram load
    - Utilization
    - Power consumption

- Async operations for IO-bound tasks
    - Container management
    - Image operations
    - Model downloads
    - Graceful thread pool shutdown

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
- Thread pool sizes for IO and CPU operations

## Operating Data
- What assets are deployed via docker
- Thread pool utilization metrics

## Architecture
- Async operations with specialized thread pools
- FastApi with asyncio for non-blocking event loop
- Proper exception handling and propagation
- Graceful application shutdown

## Stack
- Deploy InferAdmin in docker
- InferAdmin interacts with host docker to deploy docker containers for inference/interface
- FastApi for backend (async mode)
- Frontend Vue JS + Shadcn
- YML for config and data, pydantic for representation

## Ideas
- Proxying inference requests in front of vLLM to route to correct model
    - Placeholding /llms endpoing for this functionality
- Engines other than vLLM
- Have multiple storage locations
- Add analytics for vLLM instances collected from vLLM's prometheus instance
- Enhanced logging system to replace print statements

## Initial assumption
- Nvidia gpus
- All gpus are same type
- Interface launches on all exposed via 0.0.0.0