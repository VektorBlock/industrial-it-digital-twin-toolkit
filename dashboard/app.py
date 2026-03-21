from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Industrial IT Monitoring & Digital Twin Toolkit",
    layout="wide",
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "production_data.csv"

CUSTOM_CSS = """
<style>
.block-container {
    padding-top: 0.6rem;
    padding-bottom: 0.8rem;
    padding-left: 1.6rem;
    padding-right: 1.6rem;
    max-width: 97%;
}

h1 {
    margin-bottom: 0.2rem;
}

h2, h3 {
    margin-top: 0.2rem;
    margin-bottom: 0.25rem;
}

.small-note {
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.kpi-card {
    background: linear-gradient(135deg, #f8fbff, #ffffff);
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 12px 14px;
    text-align: center;
    min-height: 95px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}

.kpi-label {
    font-size: 0.92rem;
    color: #475569;
    margin-bottom: 0.35rem;
    font-weight: 700;
}

.kpi-value {
    font-size: 1.95rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.05;
}

.kpi-sub {
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 0.28rem;
}

.info-card {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 12px 14px;
    min-height: 165px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}

.metric-mini {
    font-size: 0.92rem;
    margin-bottom: 0.3rem;
    color: #111827;
}

.insight-box {
    background-color: #eef6ff;
    border-left: 5px solid #2563eb;
    border-radius: 10px;
    padding: 12px 14px;
    color: #0f172a;
    font-size: 0.96rem;
    margin-bottom: 0.5rem;
}

.footer-mini {
    color: #6b7280;
    font-size: 0.84rem;
    margin-top: 0.3rem;
}
</style>
"""


@st.cache_data
def load_data(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"File non trovato: {file_path}")

    df = pd.read_csv(file_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def compute_kpis(df: pd.DataFrame) -> dict:
    total_minutes = len(df)
    run_minutes = int((df["state"] == "RUN").sum())
    downtime_minutes = int(df["downtime_min"].sum())

    produced = int(df["produced_units"].sum())
    good = int(df["good_units"].sum())
    scrap = int(df["scrap_units"].sum())
    theoretical_output = int(df["ideal_units_per_min"].sum())

    availability = run_minutes / total_minutes if total_minutes else 0.0
    performance = produced / theoretical_output if theoretical_output else 0.0
    quality = good / produced if produced else 0.0
    oee = availability * performance * quality

    latest_state = df.iloc[-1]["state"] if not df.empty else "N/A"
    latest_reason = df.iloc[-1]["stop_reason"] if not df.empty else "N/A"

    cpu_avg = float(df["cpu_percent"].mean()) if not df.empty else 0.0
    ram_avg = float(df["ram_percent"].mean()) if not df.empty else 0.0
    fault_count = int((df["state"] == "FAULT").sum())
    stop_count = int((df["state"] == "STOP").sum())
    network_down_count = int((df["network_ok"] == False).sum())
    service_down_count = int((df["service_ok"] == False).sum())

    return {
        "total_minutes": total_minutes,
        "run_minutes": run_minutes,
        "downtime_minutes": downtime_minutes,
        "produced": produced,
        "good": good,
        "scrap": scrap,
        "availability": availability,
        "performance": performance,
        "quality": quality,
        "oee": oee,
        "latest_state": latest_state,
        "latest_reason": latest_reason,
        "cpu_avg": cpu_avg,
        "ram_avg": ram_avg,
        "fault_count": fault_count,
        "stop_count": stop_count,
        "network_down_count": network_down_count,
        "service_down_count": service_down_count,
    }


def build_alerts(kpis: dict) -> pd.DataFrame:
    alerts = []

    if kpis["oee"] < 0.75:
        alerts.append({"severity": "HIGH", "alert": "OEE basso", "detail": f"OEE = {kpis['oee']:.2%}"})
    elif kpis["oee"] < 0.85:
        alerts.append({"severity": "MEDIUM", "alert": "OEE da migliorare", "detail": f"OEE = {kpis['oee']:.2%}"})

    if kpis["cpu_avg"] > 85:
        alerts.append({"severity": "HIGH", "alert": "CPU media critica", "detail": f"CPU media = {kpis['cpu_avg']:.1f}%"})
    elif kpis["cpu_avg"] > 75:
        alerts.append({"severity": "MEDIUM", "alert": "CPU media elevata", "detail": f"CPU media = {kpis['cpu_avg']:.1f}%"})

    if kpis["fault_count"] > 15:
        alerts.append({"severity": "HIGH", "alert": "Numero fault elevato", "detail": f"FAULT = {kpis['fault_count']} eventi"})
    elif kpis["fault_count"] > 8:
        alerts.append({"severity": "MEDIUM", "alert": "Fault da monitorare", "detail": f"FAULT = {kpis['fault_count']} eventi"})

    if kpis["downtime_minutes"] > 45:
        alerts.append({"severity": "HIGH", "alert": "Downtime elevato", "detail": f"Downtime = {kpis['downtime_minutes']} min"})
    elif kpis["downtime_minutes"] > 20:
        alerts.append({"severity": "MEDIUM", "alert": "Downtime significativo", "detail": f"Downtime = {kpis['downtime_minutes']} min"})

    if kpis["network_down_count"] > 10:
        alerts.append({"severity": "MEDIUM", "alert": "Rete instabile", "detail": f"Eventi rete down = {kpis['network_down_count']}"})

    if kpis["service_down_count"] > 8:
        alerts.append({"severity": "MEDIUM", "alert": "Servizio applicativo instabile", "detail": f"Eventi service down = {kpis['service_down_count']}"})

    if not alerts:
        alerts.append({"severity": "INFO", "alert": "Nessuna criticità rilevante", "detail": "Sistema entro soglie accettabili"})

    return pd.DataFrame(alerts)


def build_production_timeseries(df: pd.DataFrame) -> pd.DataFrame:
    return df[["timestamp", "produced_units", "good_units", "scrap_units"]].copy().set_index("timestamp")


def build_cpu_vs_output(df: pd.DataFrame) -> pd.DataFrame:
    return df[["timestamp", "cpu_percent", "produced_units"]].copy().set_index("timestamp")


def build_state_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return df["state"].value_counts().rename_axis("state").reset_index(name="minutes")


def build_downtime_by_reason(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[df["downtime_min"] > 0]
        .groupby("stop_reason", as_index=False)["downtime_min"]
        .sum()
        .sort_values(by="downtime_min", ascending=False)
    )


def build_intelligent_metrics(df: pd.DataFrame, kpis: dict) -> dict:
    cpu_output_corr = 0.0
    if df["cpu_percent"].nunique() > 1 and df["produced_units"].nunique() > 1:
        cpu_output_corr = float(df["cpu_percent"].corr(df["produced_units"]))

    downtime_reason_df = build_downtime_by_reason(df)
    top_downtime_reason = "N/A"
    top_downtime_minutes = 0

    if not downtime_reason_df.empty:
        top_row = downtime_reason_df.iloc[0]
        top_downtime_reason = str(top_row["stop_reason"])
        top_downtime_minutes = int(top_row["downtime_min"])

    efficiency_loss = 1.0 - kpis["performance"]

    if kpis["oee"] >= 0.85 and kpis["downtime_minutes"] <= 20 and kpis["fault_count"] <= 8:
        system_health = "HEALTHY"
    elif kpis["oee"] >= 0.70 and kpis["downtime_minutes"] <= 45 and kpis["fault_count"] <= 15:
        system_health = "WARNING"
    else:
        system_health = "CRITICAL"

    return {
        "cpu_output_corr": cpu_output_corr,
        "top_downtime_reason": top_downtime_reason,
        "top_downtime_minutes": top_downtime_minutes,
        "efficiency_loss": efficiency_loss,
        "system_health": system_health,
    }


def build_insight_text(kpis: dict, smart: dict) -> str:
    corr = smart["cpu_output_corr"]

    if corr <= -0.50:
        corr_text = "È presente una forte correlazione inversa tra CPU e produzione."
    elif corr <= -0.25:
        corr_text = "È presente una correlazione inversa moderata tra CPU e produzione."
    elif corr < 0.10:
        corr_text = "La correlazione tra CPU e produzione risulta debole o trascurabile."
    else:
        corr_text = "La relazione tra CPU e produzione non evidenzia un impatto inverso significativo."

    downtime_text = (
        f"La principale causa di downtime è '{smart['top_downtime_reason']}' con {smart['top_downtime_minutes']} minuti."
        if smart["top_downtime_reason"] != "N/A"
        else "Non risultano cause di downtime dominanti."
    )

    performance_text = f"La perdita di efficienza rispetto al teorico è del {smart['efficiency_loss']:.2%}."
    health_text = f"Lo stato complessivo del sistema è classificato come {smart['system_health']}."

    return f"{health_text} {corr_text} {downtime_text} {performance_text}"


def state_badge(state: str) -> str:
    colors = {
        "RUN": "#166534",
        "STOP": "#b45309",
        "FAULT": "#b91c1c",
    }
    color = colors.get(state, "#374151")
    return (
        f"<div style='padding:12px 16px;border-radius:12px;"
        f"background-color:{color};color:white;font-weight:800;font-size:1rem;"
        f"display:inline-block;min-width:140px;text-align:center;'>{state}</div>"
    )


def health_badge(health: str) -> str:
    colors = {
        "HEALTHY": "#166534",
        "WARNING": "#b45309",
        "CRITICAL": "#b91c1c",
    }
    color = colors.get(health, "#374151")
    return (
        f"<div style='padding:12px 16px;border-radius:12px;"
        f"background-color:{color};color:white;font-weight:800;font-size:1rem;"
        f"display:inline-block;min-width:160px;text-align:center;'>{health}</div>"
    )


def kpi_color(value: float) -> str:
    if value >= 0.85:
        return "#16a34a"
    elif value >= 0.70:
        return "#f59e0b"
    else:
        return "#dc2626"


def render_kpi_card(label: str, value: str, sub: str = "", color: str = "#2563eb") -> str:
    return f"""
    <div class="kpi-card" style="border-top: 5px solid {color};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """


def color_alerts(row):
    if row["severity"] == "HIGH":
        return ["background-color: #fee2e2"] * len(row)
    elif row["severity"] == "MEDIUM":
        return ["background-color: #fef3c7"] * len(row)
    else:
        return ["background-color: #e0f2fe"] * len(row)


def oee_comment(oee: float) -> str:
    if oee >= 0.85:
        return "Prestazione complessiva molto buona."
    if oee >= 0.75:
        return "Prestazione buona con margine di miglioramento."
    if oee >= 0.60:
        return "Prestazione moderata: servono azioni correttive."
    return "Prestazione critica: analisi immediata consigliata."


def main() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.title("Industrial IT Monitoring & Digital Twin Toolkit")
    st.markdown(
        "<div class='small-note'>Dashboard V5 - visual refinement + analisi intelligente</div>",
        unsafe_allow_html=True,
    )

    try:
        df = load_data(DATA_PATH)
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.info("Esegui prima il simulatore con: python3 src/simulator.py")
        return

    kpis = compute_kpis(df)
    alerts_df = build_alerts(kpis)
    smart = build_intelligent_metrics(df, kpis)
    insight_text = build_insight_text(kpis, smart)

    st.subheader("KPI principali")
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            render_kpi_card("Availability", f"{kpis['availability']:.2%}", "Tempo operativo", kpi_color(kpis["availability"])),
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            render_kpi_card("Performance", f"{kpis['performance']:.2%}", "Output reale vs teorico", kpi_color(kpis["performance"])),
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            render_kpi_card("Quality", f"{kpis['quality']:.2%}", "Pezzi buoni", kpi_color(kpis["quality"])),
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            render_kpi_card("OEE", f"{kpis['oee']:.2%}", "Indice complessivo", kpi_color(kpis["oee"])),
            unsafe_allow_html=True,
        )

    c_left, c_mid, c_right = st.columns([1.15, 1.15, 1.35])

    with c_left:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("Stato corrente")
        st.markdown(state_badge(str(kpis["latest_state"])), unsafe_allow_html=True)
        st.markdown(f"<div class='metric-mini'><b>Motivo:</b> {kpis['latest_reason']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-mini'><b>CPU media:</b> {kpis['cpu_avg']:.1f}%</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-mini'><b>RAM media:</b> {kpis['ram_avg']:.1f}%</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c_mid:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("Salute sistema")
        st.markdown(health_badge(str(smart["system_health"])), unsafe_allow_html=True)
        st.markdown(f"<div class='metric-mini'><b>Correlazione CPU-Produzione:</b> {smart['cpu_output_corr']:.3f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-mini'><b>Top downtime:</b> {smart['top_downtime_reason']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-mini'><b>Perdita efficienza:</b> {smart['efficiency_loss']:.2%}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c_right:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("Valutazione OEE")
        st.progress(float(kpis["oee"]))
        st.markdown(f"<div class='metric-mini'><b>Indice OEE:</b> {kpis['oee']:.2%}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-mini'>{oee_comment(kpis['oee'])}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("Insight automatico")
    st.markdown(f"<div class='insight-box'>{insight_text}</div>", unsafe_allow_html=True)

    a1, a2 = st.columns([1.3, 1])

    with a1:
        st.subheader("Alert intelligenti")
        st.dataframe(
            alerts_df.style.apply(color_alerts, axis=1),
            use_container_width=True,
            hide_index=True
        )

    with a2:
        st.subheader("Riepilogo operativo")
        r1, r2, r3 = st.columns(3)
        r4, r5, r6 = st.columns(3)
        r1.metric("Prodotte", str(kpis["produced"]))
        r2.metric("Buone", str(kpis["good"]))
        r3.metric("Scarti", str(kpis["scrap"]))
        r4.metric("Fault", str(kpis["fault_count"]))
        r5.metric("Stop", str(kpis["stop_count"]))
        r6.metric("Downtime", f"{kpis['downtime_minutes']} min")

    st.subheader("Produzione nel tempo")
    st.line_chart(build_production_timeseries(df), use_container_width=True)

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("CPU vs produzione")
        st.line_chart(build_cpu_vs_output(df), use_container_width=True)
    with g2:
        st.subheader("Distribuzione stati macchina")
        state_dist = build_state_distribution(df)
        st.bar_chart(state_dist.set_index("state"), use_container_width=True)

    d1, d2 = st.columns([1.1, 1.4])
    downtime_reason = build_downtime_by_reason(df)

    with d1:
        st.subheader("Downtime per causa")
        if downtime_reason.empty:
            st.info("Nessun downtime registrato.")
        else:
            st.bar_chart(downtime_reason.set_index("stop_reason"), use_container_width=True)

    with d2:
        st.subheader("Dettaglio downtime")
        if downtime_reason.empty:
            st.info("Nessun dettaglio disponibile.")
        else:
            st.dataframe(downtime_reason, use_container_width=True, hide_index=True)

    st.subheader("Ultimi record")
    preview_cols = [
        "timestamp",
        "machine_id",
        "state",
        "stop_reason",
        "cpu_percent",
        "ram_percent",
        "network_ok",
        "service_ok",
        "produced_units",
        "good_units",
        "scrap_units",
        "downtime_min",
        "performance_factor",
    ]
    st.dataframe(df[preview_cols].tail(20), use_container_width=True)

    st.markdown(
        "<div class='footer-mini'>Simulazione dati macchina + metriche IT integrate per analisi KPI e decision support.</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
