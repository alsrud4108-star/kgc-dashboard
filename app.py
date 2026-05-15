import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 데이터 불러오기 (미리 생성한 csv 파일이 코랩 경로에 있어야 합니다)
df = pd.read_csv('manufacturing_process_data.csv')

# 2. 규격 및 파라미터 설정
USL, LSL = 15.0, 5.0
BATCH_SIZE = 50

# 3. 배치별 통계량 계산 함수
def get_cpk(series, u, l):
    mu = series.mean()
    sigma = series.std(ddof=1)
    if sigma == 0: return 0
    return min((u - mu) / (3 * sigma), (mu - l) / (3 * sigma))

# 배치별 요약 데이터 생성
batch_stats = df.groupby('Batch_ID')['Measurement'].agg(['mean', 'std']).reset_index()
batch_stats['cpk'] = df.groupby('Batch_ID')['Measurement'].apply(lambda x: get_cpk(x, USL, LSL)).values

# 4. 관리 한계선 산출 (안정 상태인 1~70번 배치 기준)
phase1 = batch_stats[batch_stats['Batch_ID'] <= 70]
cl = phase1['mean'].mean()
sd_avg = phase1['std'].mean()
# X-bar 관리 한계선 (3-sigma 원칙)
ucl = cl + 3 * (sd_avg / np.sqrt(BATCH_SIZE))
lcl = cl - 3 * (sd_avg / np.sqrt(BATCH_SIZE))

# 5. 조기 경보(Early Warning) 로직 예시
batch_stats['Warning'] = (batch_stats['mean'] > ucl) | (batch_stats['mean'] < lcl) | (batch_stats['cpk'] < 1.0)

print(f"조기 경보가 발생한 총 배치 수: {batch_stats['Warning'].sum()}개")
print(batch_stats[batch_stats['Warning'] == True].head())

# 6. 시각화 코드는 위 이미지 생성 코드와 동일하게 활용 가능합니다.
