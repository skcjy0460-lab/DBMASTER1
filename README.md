# Medical Master DB Builder

병원 심사보조/수가계산기/약품·수가·상병 마스터DB 구축을 위한 파이썬 프로젝트입니다.

## 포함 범위

| 마스터 | 수집/적재 방식 | 비고 |
|---|---|---|
| KCD/상병코드 | XLSX/CSV 파일 적재 | 통계분류포털 KSSC 원천자료 권장 |
| 급여의약품 | XLSX/CSV 파일 적재 | 심평원 약제급여목록및급여상한금액표 |
| 식약처 의약품 품목정보 | API 수집 | 공공데이터포털 식약처 의약품 제품 허가정보 |
| 수가반영내역 | XLSX/CSV 파일 적재 | 심평원 수가반영내역 전체판 |
| 행위 급여목록 | XLSX/CSV 파일 적재 | 고시 첨부 또는 수가반영내역 전체판 |
| 치료재료 | API 수집 또는 파일 적재 | 건강보험심사평가원 치료재료정보조회서비스 |
| 희귀질환 산정특례 | XLSX/CSV 파일 적재 | 질병관리청 희귀질환 헬프라인 목록 |
| 산정특례 등록기준 | XLSX/CSV 파일 적재 | 건보공단 산정특례 질환별 등록기준 |

## 설치

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
copy .env.example .env
```

`.env` 파일에 공공데이터포털 인증키를 넣습니다.

```env
DATA_GO_KR_SERVICE_KEY=발급받은_인증키
DB_PATH=db/medical_master.db
```

## 파일 적재 예시

```bash
python manage.py load-file kcd data/raw/kcd.xlsx
python manage.py load-file drug_benefit data/raw/drug_benefit.xlsx
python manage.py load-file fee_reflection data/raw/fee_reflection.xlsx
python manage.py load-file medical_act data/raw/medical_act.xlsx
python manage.py load-file special_case_rare data/raw/rare_disease.xlsx
python manage.py load-file special_case_rule data/raw/special_case_rule.xlsx
```

엑셀 시트가 여러 개인 경우:

```bash
python manage.py load-file special_case_rule data/raw/special_case_rule.xlsx --sheet "희귀질환"
```

## API 수집 예시

치료재료 테스트 수집:

```bash
python manage.py collect-material --max-pages 1
```

식약처 의약품 품목정보 테스트 수집:

```bash
python manage.py collect-mfds-drug --max-pages 1
```

> 공공데이터포털 API는 endpoint 또는 operation 명칭이 활용가이드 버전별로 달라질 수 있습니다. 실행 오류가 나면 `config/api_endpoints.json`의 `base_url`, `operation`을 공공데이터포털 활용가이드와 맞추면 됩니다.

## 결과물

- SQLite DB: `db/medical_master.db`
- 정규화 CSV: `data/processed/*.csv`

## DB 테이블

| 테이블 | 설명 |
|---|---|
| kcd_master | KCD/상병코드 마스터 |
| drug_benefit_master | 급여의약품 마스터 |
| mfds_drug_item_master | 식약처 의약품 품목정보 |
| fee_master | 수가반영내역/수가 마스터 |
| medical_act_master | 행위 급여목록 마스터 |
| material_master | 치료재료 마스터 |
| special_case_rare_master | 희귀질환 산정특례 KCD 매핑 |
| special_case_rule_master | 산정특례 등록기준 |

## DB 확인

```bash
python scripts/check_db.py
```

## Git 업로드

```bash
git init
git add .
git commit -m "Initial medical master DB builder"
git branch -M main
git remote add origin https://github.com/사용자명/저장소명.git
git push -u origin main
```

## 중요 주의사항

- `.env`는 인증키가 들어가므로 Git에 올리면 안 됩니다.
- 원천자료는 대부분 XLSX입니다. CSV가 아니어도 이 프로젝트에서 읽어서 CSV/SQLite로 변환합니다.
- 일부개정 파일만으로 전체 마스터를 만들지 말고, 가능한 한 전체판 파일 또는 API를 기준으로 초기 구축하세요.
