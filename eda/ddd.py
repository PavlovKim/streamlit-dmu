import pandas as pd
from define_api2 import TCV_CD  # TCV_CD import

# 1️⃣ CSV 파일 읽기
df = pd.read_csv("Upload2.csv", encoding="utf-8")


# 2️⃣ Title과 Make를 함께 받아 모델명 추출
def get_model_from_row(row):
    title = row["Title"]
    make = row["Make"]

    if pd.isna(title) or pd.isna(make):
        return make + " Other" if pd.notna(make) else "Other"

    title_lower = title.lower()
    make_lower = make.lower()

    for model_name, details in TCV_CD.items():
        model_lower = model_name.lower()
        tcv_make_lower = details["MakeName"].lower()

        # Title에 모델명과 제조사 모두 포함되어 있는지 확인
        if model_lower in title_lower and tcv_make_lower in title_lower:
            return model_name

    return make + " Others"  # 없으면 해당 행의 Make 값을 기준으로 Other 반환


# 3️⃣ Model 컬럼 채우기
df["Model"] = df.apply(get_model_from_row, axis=1)

# 4️⃣ 결과 저장
df.to_csv("Updated_Upload2.csv", index=False, encoding="utf-8")

print("변환 완료: Updated_Upload2.csv")
