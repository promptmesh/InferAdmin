from enum import Enum


class Tag(str, Enum):
    """Tag for OpenAPI"""

    deployments = "Deployed Services API"
    images = "Docker Images API"
    infra = "GPU and Volume info API"
    models = "ML Model API"


tags_metadata = [
    {
        "name": Tag.deployments,
        "description": "API endpoints to manage service deployments such as vLLM and OpenWebUI instances. "
                      "Allows deploying, stopping, configuring, and checking the status of running instances. ",
    },
    {
        "name": Tag.images,
        "description": "API endpoints to manage Docker images used for deployments. "
                      "Supports listing available images, pulling new versions, and deleting images.",
    },
    {
        "name": Tag.infra,
        "description": "API endpoints to monitor and manage infrastructure resources. "
                      "Provides GPU information including VRAM usage, utilization, and power consumption. "
                      "Manages storage volumes for model files and reports available space. "
    },
    {
        "name": Tag.models,
        "description": "API endpoints to manage machine learning models. "
                      "Supports listing, downloading, updating, and deleting models from a unified location. "
                      "Provides model metadata, size information, and compatibility data with available "
                      "deployment options. Requires Hugging Face token for accessing gated models.",
    },
]