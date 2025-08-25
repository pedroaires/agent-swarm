from __future__ import annotations
import json
from pathlib import Path
from typing import Optional, Dict, Any
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

class UserFakeService:
    def __init__(self, file_path: str = "app/data/users.json") -> None:
        self._file_path = Path(file_path)
        if self._file_path.exists():
            with open(self._file_path, "r", encoding="utf-8") as f:
                self._users: Dict[str, Dict[str, Any]] = json.load(f)
        else:
            self._users = {}

    def get(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retorna o dicionário com informações do usuário, se existir.
        """
        return self._users.get(user_id)

service = UserFakeService()
@tool("get_user_profile", return_direct=False)
def get_user_profile(config: RunnableConfig):
    """
    Retrieve the profile information of a specific user.
    Returns
    -------
    dict
        A dictionary containing the user profile data if found.
        Example: {"found": True, "data": {...}}
        If not found, returns {"found": False, "message": "..."}.
    """
    uid = (config.get("configurable") or {}).get("user_id")
    user_data = service.get(uid)
    if user_data:
        return {"found": True, "data": user_data}
    return {
        "found": False,
        "message": f"User with id '{uid}' was not found in the dataset."
    }