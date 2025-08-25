import json
from pathlib import Path
from typing import Optional, Dict, Any
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

class BalanceFakeService:
    def __init__(self, file_path: str = "app/data/balances.json") -> None:
        self._file_path = Path(file_path)
        if self._file_path.exists():
            with open(self._file_path, "r", encoding="utf-8") as f:
                self._balances: Dict[str, Dict[str, Any]] = json.load(f)
        else:
            self._balances = {}

    def get(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self._balances.get(user_id)

service = BalanceFakeService()

@tool("get_balance", return_direct=False)
def get_balance(
    config: RunnableConfig
) -> Dict[str, Any]:
    """
    Retrieve the digital account balance for a given user.

    Returns
    -------
    dict
        A dictionary containing the user's balance information if found.
        Example: {"found": True, "balance": {"balance": 1250.75, "currency": "BRL"}}
        If not found, returns {"found": False, "message": "..."}.
    """
    uid = (config.get("configurable") or {}).get("user_id")
    data = service.get(uid)
    if data:
        return {"found": True, "balance": data}
    return {"found": False, "message": f"No balance found for user '{uid}'."}
