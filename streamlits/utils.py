import pandas as pd
import unidecode

def normalizar_texto(texto: str) -> str:
    if pd.isna(texto):
        return texto
    return unidecode.unidecode(texto.strip().lower())

def corregir_departamentos(df: pd.DataFrame) -> pd.DataFrame:
    df["departamento"] = df["departamento"].str.replace(r"bogota.*", "bogota", regex=True)
    df["departamento"] = df["departamento"].str.replace(r"san andres.*", "san andres", regex=True)
    return df

def limpiar_metricas(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["tasa_matriculaci_n_5_16", "cobertura_neta", "cobertura_bruta"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df.loc[df[col] < 0, col] = None
    return df
