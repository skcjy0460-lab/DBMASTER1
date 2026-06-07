from __future__ import annotations

import argparse
from dotenv import load_dotenv

from src.utils.io import ensure_dirs
from src.utils.db import save_table, create_indexes
from src.loaders.file_loader import load_file
from src.collectors.api_collectors import collect_material, collect_mfds_drug_items
from src.loaders.normalizers import normalize_material


def main() -> None:
    load_dotenv()
    ensure_dirs()
    parser = argparse.ArgumentParser(description="병원 마스터DB 구축 도구")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_file = sub.add_parser("load-file", help="엑셀/CSV 원천자료를 정규화하여 SQLite/CSV 저장")
    p_file.add_argument("master", help="kcd, drug_benefit, fee_reflection, medical_act, material_file, special_case_rare, special_case_rule")
    p_file.add_argument("path", help="원천 파일 경로")
    p_file.add_argument("--sheet", default=0, help="엑셀 시트명 또는 번호. 기본 0")

    p_mat = sub.add_parser("collect-material", help="치료재료 API 수집")
    p_mat.add_argument("--max-pages", type=int, default=None)
    p_mat.add_argument("--material-code", default=None, help="API 파라미터명이 다르면 config/api_endpoints.json 또는 코드 수정")

    p_mfds = sub.add_parser("collect-mfds-drug", help="식약처 의약품 품목정보 API 수집")
    p_mfds.add_argument("--max-pages", type=int, default=None)
    p_mfds.add_argument("--item-name", default=None)

    args = parser.parse_args()

    if args.cmd == "load-file":
        sheet = int(args.sheet) if str(args.sheet).isdigit() else args.sheet
        df = load_file(args.master, args.path, sheet_name=sheet)
        print(f"완료: {args.master} {len(df):,}건")
    elif args.cmd == "collect-material":
        extra = {}
        if args.material_code:
            extra["materialCd"] = args.material_code
        raw = collect_material(max_pages=args.max_pages, **extra)
        df = normalize_material(raw)
        save_table(df, "material_master")
        create_indexes()
        print(f"완료: material {len(df):,}건")
    elif args.cmd == "collect-mfds-drug":
        extra = {}
        if args.item_name:
            extra["item_name"] = args.item_name
        df = collect_mfds_drug_items(max_pages=args.max_pages, **extra)
        save_table(df, "mfds_drug_item_master")
        create_indexes()
        print(f"완료: mfds_drug_item {len(df):,}건")


if __name__ == "__main__":
    main()
