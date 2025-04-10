import json
import os
from pathlib import Path
from typing import Any, List, Optional, TypeVar, Generic, Type
from datetime import datetime
from pydantic import BaseModel
from contextlib import asynccontextmanager
from loguru import logger

T = TypeVar("T", bound=BaseModel)


class StateManager(Generic[T]):
    """Manages state for deployments using JSON files."""

    def __init__(self, state_dir: str, filename: str, model_cls: Type[T]):
        """
        Initialize a state manager.

        Args:
            state_dir: Directory to store state files
            filename: Name of the state file
            model_cls: Pydantic model class to serialize/deserialize
        """
        self.state_dir = Path(state_dir)
        self.state_file = self.state_dir / filename
        self.model_cls = model_cls

        # Create state directory if it doesn't exist
        os.makedirs(self.state_dir, exist_ok=True)

        # Create empty state file if it doesn't exist
        if not self.state_file.exists():
            with open(self.state_file, "w") as f:
                json.dump([], f)

    def get_all(self) -> List[T]:
        """Get all items in the state file."""
        try:
            with open(self.state_file, "r") as f:
                data = json.load(f)

            # Convert each dict to a model instance
            return [self.model_cls.model_validate(item) for item in data]
        except Exception as e:
            logger.error(f"reading state file: {e}")
            return []

    def get_by_id(self, id: str) -> Optional[T]:
        """Get an item by its ID."""
        items = self.get_all()
        for item in items:
            if item.id == id:
                return item
        return None

    def _save_items(self, items: List[T]) -> None:
        """Save items to the state file with error handling."""
        try:
            with open(self.state_file, "w") as f:
                json.dump(
                    [item.model_dump() for item in items],
                    f,
                    default=self._json_serializer,
                )
        except Exception as e:
            logger.error(f"saving state file: {e}")
            raise

    def add(self, item: T) -> T:
        """Add a new item to the state."""
        items = self.get_all()
        items.append(item)
        self._save_items(items)
        return item

    def update(self, item: T) -> T:
        """Update an existing item in the state."""
        items = self.get_all()
        items = [i for i in items if i.id != item.id]
        items.append(item)
        self._save_items(items)
        return item

    def delete(self, id: str) -> bool:
        """Delete an item from the state."""
        items = self.get_all()
        new_items = [item for item in items if item.id != id]

        # If no items were removed, return False
        if len(new_items) == len(items):
            return False

        self._save_items(new_items)
        return True

    def _json_serializer(self, obj: Any) -> Any:
        """Custom JSON serializer to handle datetime objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    @asynccontextmanager
    async def lifespan(self):
        """Context manager to handle state loading and saving."""
        self.state = self.get_all()
        try:
            yield self
        finally:
            self._save_items(self.state)
