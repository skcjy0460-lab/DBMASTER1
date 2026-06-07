from __future__ import annotations

from typing import Any
import requests
import xmltodict


def parse_response(resp: requests.Response, response_type: str) -> Any:
    resp.raise_for_status()
    if response_type.lower() == "json":
        return resp.json()
    return xmltodict.parse(resp.text)


def find_items(obj: Any) -> list[dict[str, Any]]:
    """공공데이터 응답 구조가 조금씩 달라서 item/items를 재귀 탐색합니다."""
    if obj is None:
        return []
    if isinstance(obj, list):
        out = []
        for x in obj:
            out.extend(find_items(x))
        return out
    if isinstance(obj, dict):
        if "item" in obj:
            item = obj["item"]
            if isinstance(item, list):
                return [i for i in item if isinstance(i, dict)]
            if isinstance(item, dict):
                return [item]
        for v in obj.values():
            found = find_items(v)
            if found:
                return found
    return []


def find_total_count(obj: Any) -> int | None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k).lower() == "totalcount":
                try:
                    return int(v)
                except Exception:
                    return None
        for v in obj.values():
            found = find_total_count(v)
            if found is not None:
                return found
    if isinstance(obj, list):
        for x in obj:
            found = find_total_count(x)
            if found is not None:
                return found
    return None
