import docker

class DockerManagerClass:
    client = None

    def init(self):
        """Initialize the Docker client"""
        try:
            self.client = docker.from_env()
        except Exception as e:
            raise Exception(f"Failed to initialize Docker: {e}")
        
    def get(self):
        """Get the Docker client instance"""
        if self.client is None:
            self.init()  # Auto-initialize if not done
        return self.client


DockerManager = DockerManagerClass()