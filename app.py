!pip install koreanize-matplotlib
import warnings
from pathlib import Path

import koreanize_matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")
plt.style.use("ggplot")
pd.set_option("display.max_columns", None)


def load_and_preprocess_data(data_path):
    """
    데이터를 로드하고 전처리합니다.
    - timestamp 컬럼을 datetime으로 변환합니다.
    - measure_deviation과 spec_margin 컬럼을 계산합니다.
    """
    df = pd.read_csv(data_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["measure_deviation"] = df["measure_value"] - (df["lsl"] + df["usl"]) / 2
    df["spec_margin"] = np.minimum(df["measure_value"] - df["lsl"], df["usl"] - df["measure_value"])
    return df


def calculate_cpk(df):
    """
    주어진 DataFrame에서 품목별 Cpk를 계산합니다.
    """
    def calc_cpk_single_group(group):
        mean = group["measure_value"].mean()
        std = group["measure_value"].std()
        usl = group["usl"].iloc[0]
        lsl = group["lsl"].iloc[0]
        # Handle case where std is zero to avoid division by zero
        if std == 0:
            return 0.0 # Or np.inf if you prefer to indicate perfect process (no variation)
        cpu = (usl - mean) / (3 * std)
        cpl = (mean - lsl) / (3 * std)
        return round(min(cpu, cpl), 3)

    cpk_df = df.groupby("product_type").apply(calc_cpk_single_group).reset_index(name="cpk").sort_values("cpk")
    return cpk_df


def generate_control_chart_data(df, target_product):
    """
    특정 품목의 관리도 시각화에 필요한 데이터를 준비합니다.
    측정값, 평균, UCL, LCL을 포함하는 DataFrame을 반환합니다.
    """
    chart_df = df.loc[df["product_type"] == target_product].sort_values("timestamp").copy()

    mean_value = chart_df["measure_value"].mean()
    std_value = chart_df["measure_value"].std()
    ucl = mean_value + 3 * std_value
    lcl = mean_value - 3 * std_value

    # Prepare data for plotting
    control_chart_data = pd.DataFrame({
        "timestamp": chart_df["timestamp"],
        "measure_value": chart_df["measure_value"],
        "mean_value": mean_value,
        "ucl": ucl,
        "lcl": lcl
    })
    return control_chart_data


def summarize_warning_and_process_vars(df):
    """
    품목별 경고 비율과 주요 공정 변수(온도, 압력, 습도)의 평균을 요약합니다.
    """
    warning_summary = (
        df.groupby("product_type", as_index=False)
        .agg(
            warning_ratio=("warning_flag", "mean"),
            avg_temp=("temperature_c", "mean"),
            avg_pressure=("pressure_bar", "mean"),
            avg_humidity=("humidity_pct", "mean"),
        )
    )
    warning_summary["warning_ratio"] = (warning_summary["warning_ratio"] * 100).round(2)
    return warning_summary


def train_early_warning_model(df, model_cols, target_col):
    """
    조기 경보 모델(RandomForestClassifier)을 학습시키고 학습된 모델 객체를 반환합니다.
    """
    X = df[model_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    warning_model = RandomForestClassifier(
        random_state=42,
        n_estimators=150,
        max_depth=5,
        min_samples_leaf=3,
    )
    warning_model.fit(X_train, y_train)

    # Return the trained model and test sets for later evaluation
    return warning_model, X_test, y_test


def predict_top_risk_lots(model, df, model_cols, n_top_lots=10):
    """
    학습된 모델을 사용하여 각 lot의 경고 확률을 예측하고, 경고 확률이 높은 상위 N개 lot을 반환합니다.
    """
    risk_table = df.copy()
    risk_table["warning_probability"] = model.predict_proba(df[model_cols])[:, 1]
    top_risk_lots = (
        risk_table.sort_values("warning_probability", ascending=False)
        .loc[:, ["timestamp", "product_type", "lot_id", "measure_value", "warning_flag", "warning_probability"]]
        .head(n_top_lots)
    )
    return top_risk_lots
