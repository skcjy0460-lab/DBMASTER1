from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv
from tqdm import tqdm

from src.utils.api import parse_response, find_items, find_total_count
from src.utils.io import load_json, save_csv


def _endpoint_url(base_url: str, operation: str) -> str:
    return base_url.rstrip("/") + "/" + operation.lstrip("/")


def collect_paginated_api(source_name: str, max_pages: int | None = None, extra_params: dict[str, Any] | None = None) -> pd.DataFrame:
    load_dotenv()
    endpoints = load_json("config/api_endpoints.json")
    cfg = endpoints[source_name]
    key = os.getenv("DATA_GO_KR_SERVICE_KEY") or os.getenv("MFDS_SERVICE_KEY")
    if source_name.startswith("mfds"):
        key = os.getenv("MFDS_SERVICE_KEY") or os.getenv("DATA_GO_KR_SERVICE_KEY")
    if not key:
        raise RuntimeError(".env에 DATA_GO_KR_SERVICE_KEY를 입력하세요.")

    params = dict(cfg.get("default_params", {}))
    params.update(extra_params or {})
    params["serviceKey"] = key
    url = _endpoint_url(cfg["base_url"], cfg["operation"])
    response_type = cfg.get("response_type", "xml")

    first = parse_response(requests.get(url, params=params, timeout=30), response_type)
    items = find_items(first)
    total = find_total_count(first)
    num_rows = int(params.get("numOfRows", 100))
    total_pages = max_pages or (math.ceil(total / num_rows) if total else 1)

    all_items = list(items)
    for page in tqdm(range(2, total_pages + 1), desc=f"collect {source_name}"):
        params["pageNo"] = page
        data = parse_response(requests.get(url, params=params, timeout=30), response_type)
        all_items.extend(find_items(data))

    df = pd.DataFrame(all_items)
    out = Path("data/processed") / f"{source_name}.csv"
    save_csv(df, out)
    return df


def collect_material(max_pages: int | None = None, **kwargs: Any) -> pd.DataFrame:
    return collect_paginated_api("material", max_pages=max_pages, extra_params=kwargs)


def collect_mfds_drug_items(max_pages: int | None = None, **kwargs: Any) -> pd.DataFrame:
    return collect_paginated_api("mfds_drug_item", max_pages=max_pages, extra_params=kwargs)
