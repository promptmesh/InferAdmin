from aiodocker import Docker

class DockerManagerClass:
    docker: Docker | None = None

    async def init(self):
        try:
            self.docker = Docker()
        except Exception as e:
            raise Exception(f"Failed to initialize Docker: {e}")
        
    def get(self) -> Docker:
        if self.docker is None:
            raise Exception("Docker not initialized")
        return self.docker
    
    async def close(self):
        if self.docker is not None:
            await self.docker.close()


DockerManager = DockerManagerClass()