from __future__ import annotations

import re
import pandas as pd


def pick_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    cols = list(df.columns)
    norm = {re.sub(r"\s+", "", str(c)).lower(): c for c in cols}
    for cand in candidates:
        key = re.sub(r"\s+", "", cand).lower()
        if key in norm:
            return norm[key]
    for c in cols:
        text = re.sub(r"\s+", "", str(c)).lower()
        if any(re.sub(r"\s+", "", cand).lower() in text for cand in candidates):
            return c
    return None


def normalize_kcd(df: pd.DataFrame) -> pd.DataFrame:
    code = pick_col(df, ["KCD코드", "상병코드", "분류번호", "코드"])
    name = pick_col(df, ["한글명", "질병명", "상병명", "명칭"])
    out = pd.DataFrame()
    out["kcd_code"] = df[code].astype(str).str.strip() if code else ""
    out["kcd_name_ko"] = df[name].astype(str).str.strip() if name else ""
    return out.drop_duplicates()


def normalize_drug_benefit(df: pd.DataFrame) -> pd.DataFrame:
    code = pick_col(df, ["급여코드", "약품코드", "제품코드", "표준코드"])
    name = pick_col(df, ["제품명", "품명", "약품명", "한글명"])
    comp = pick_col(df, ["업체명", "제조사", "제약사"])
    price = pick_col(df, ["상한금액", "상한가", "금액"])
    out = pd.DataFrame()
    out["drug_code"] = df[code].astype(str).str.strip() if code else ""
    out["drug_name"] = df[name].astype(str).str.strip() if name else ""
    out["company"] = df[comp].astype(str).str.strip() if comp else ""
    out["max_price"] = df[price].astype(str).str.strip() if price else ""
    return out.drop_duplicates()


def normalize_fee(df: pd.DataFrame) -> pd.DataFrame:
    code = pick_col(df, ["수가코드", "행위코드", "코드"])
    name = pick_col(df, ["한글명", "명칭", "분류명", "행위명"])
    point = pick_col(df, ["상대가치점수", "점수"])
    out = pd.DataFrame()
    out["fee_code"] = df[code].astype(str).str.strip() if code else ""
    out["fee_name"] = df[name].astype(str).str.strip() if name else ""
    out["relative_value_score"] = df[point].astype(str).str.strip() if point else ""
    return out.drop_duplicates()


def normalize_medical_act(df: pd.DataFrame) -> pd.DataFrame:
    out = normalize_fee(df).rename(columns={"fee_code": "act_code", "fee_name": "act_name"})
    return out


def normalize_material(df: pd.DataFrame) -> pd.DataFrame:
    code = pick_col(df, ["재료대코드", "치료재료코드", "materialCd", "matrCd", "코드"])
    name = pick_col(df, ["품목명", "품명", "재료명", "materialNm"])
    maker = pick_col(df, ["제조업체명", "제조사", "업체명"])
    price = pick_col(df, ["상한단가", "상한금액", "금액"])
    spec = pick_col(df, ["규격"])
    benefit = pick_col(df, ["급여구분", "급여여부"])
    out = pd.DataFrame()
    out["material_code"] = df[code].astype(str).str.strip() if code else ""
    out["material_name"] = df[name].astype(str).str.strip() if name else ""
    out["manufacturer"] = df[maker].astype(str).str.strip() if maker else ""
    out["spec"] = df[spec].astype(str).str.strip() if spec else ""
    out["benefit_type"] = df[benefit].astype(str).str.strip() if benefit else ""
    out["max_price"] = df[price].astype(str).str.strip() if price else ""
    return out.drop_duplicates()


def normalize_special_case_rare(df: pd.DataFrame) -> pd.DataFrame:
    kcd = pick_col(df, ["KCD코드", "상병코드", "질병분류코드"])
    vcode = pick_col(df, ["산정특례코드", "특정기호", "V코드"])
    name = pick_col(df, ["질환명(국문)", "질환명", "국문명"])
    cls = pick_col(df, ["질환분류", "구분"])
    out = pd.DataFrame()
    out["kcd_code"] = df[kcd].astype(str).str.strip() if kcd else ""
    out["special_code"] = df[vcode].astype(str).str.strip() if vcode else ""
    out["disease_name"] = df[name].astype(str).str.strip() if name else ""
    out["category"] = df[cls].astype(str).str.strip() if cls else ""
    return out.drop_duplicates()


def normalize_special_case_rule(df: pd.DataFrame) -> pd.DataFrame:
    vcode = pick_col(df, ["산정특례코드", "특정기호", "V코드"])
    name = pick_col(df, ["질환명", "상병명", "명칭"])
    rule = pick_col(df, ["등록기준", "검사기준", "기준"])
    out = pd.DataFrame()
    out["special_code"] = df[vcode].astype(str).str.strip() if vcode else ""
    out["disease_name"] = df[name].astype(str).str.strip() if name else ""
    out["registration_rule"] = df[rule].astype(str).str.strip() if rule else ""
    return out.drop_duplicates()
