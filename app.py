from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="✈️ API Atrasos - CatBoost GPU v4.0 Minimal")

# Carrega modelo leve via joblib
pipe = joblib.load("voos_pipeline_minimal.joblib")

model = pipe["model"]
calibrator = pipe.get("calibrator", None)
threshold = pipe["metadata"]["threshold"]

class FlightInput(BaseModel):
    empresa_aerea: str
    aeroporto_origem: str
    aeroporto_destino: str
    mes: int
    hora_do_dia: int
    dia_da_semana: int
    periodo_dia: str

@app.post("/predict")
def predict_delay(f: FlightInput):
    try:
        rota = f"{f.aeroporto_origem}_{f.aeroporto_destino}"
        rota_mes = f"{rota}_{f.mes}"
        empresa_periodo = f"{f.empresa_aerea}_{f.periodo_dia}"
        is_weekend = int(f.dia_da_semana in [5, 6])
        trimestre = (f.mes - 1) // 3 + 1
        ano = 2025
        num_assentos = 180
        atraso_padrao = 0.15

        df = pd.DataFrame([{
            "EMPRESA_PERIODO": empresa_periodo,
            "ROTA_MES": rota_mes,
            "SIGLA_ICAO_AEROPORTO_ORIGEM": f.aeroporto_origem,
            "ROTA": rota,
            "DIA_DA_SEMANA": str(f.dia_da_semana),
            "PERIODO_DIA": f.periodo_dia,
            "IS_WEEKEND": is_weekend,
            "MES": f.mes,
            "ANO": ano,
            "TRIMESTRE": trimestre,
            "NUMERO_DE_ASSENTOS": num_assentos,
            "HORA_DO_DIA": f.hora_do_dia,
            "ATRASO_MEDIO_ORIGEM": atraso_padrao,
            "ATRASO_MEDIO_DESTINO": atraso_padrao,
            "ATRASO_MEDIO_ROTA": atraso_padrao,
            "ATRASO_MEDIO_HORA": atraso_padrao,
            "ATRASO_MEDIO_TOTAL": atraso_padrao,
            "ATRASO_MEDIO_ROTA_HORA": atraso_padrao * atraso_padrao,
            "ATRASO_HORA_DESTINO": atraso_padrao * (f.hora_do_dia / 24),
            "TENDENCIA_ATRASO_MES": atraso_padrao * (f.mes / 12),
            "TENDENCIA_SAZONAL": atraso_padrao / (atraso_padrao + 1e-6)
        }])

        if calibrator:
            prob = calibrator.predict_proba(df)[:, 1][0]
        elif hasattr(model, "predict_proba"):
            prob = model.predict_proba(df)[:, 1][0]
        else:
            prob = float(model.predict(df)[0])

        pred = int(prob >= threshold)
        confidence = prob if pred == 1 else (1 - prob)

        return {"prediction": pred, "confidence": round(float(confidence), 4)}

    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "ok"}
