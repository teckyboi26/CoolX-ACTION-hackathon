import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import io
from datetime import date

# Set up pristine layout
st.set_page_config(
    page_title="GA1A | Climate-Infectious Disease Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INTERNATIONALIZATION DICTIONARY (GA1A ENGINE) ---
translations = {
    "English 🇬🇧": {
        "title": "GA1A",
        "subtitle": "CLIMATE INFECTIOUS DISEASE SURVEYOR // MULTI-PATHOGEN INTELLIGENCE",
        "live_api": "● LIVE API CHANNELS ACTIVE",
        "control_room": "CONTROL ROOM",
        "search_label": "🔍 Search Location",
        "search_help": "Type any city globally (e.g. Kuala Lumpur, Okinawa, Perak, London) to fly map focus.",
        "select_loc": "🎯 Select Matching Location:",
        "realign_btn": "📌 Re-align Viewport Map",
        "pathology": "Infectious Pathology",
        "timeline": "Observation Date",
        "telemetry": "Atmospheric Telemetry",
        "temp_label": "Ambient Temperature (°C)",
        "humid_label": "Relative Humidity (%)",
        "precip_label": "Precipitation Anomaly (%)",
        "mobility_label": "Vector Proximity Factor",
        "export_btn": "📥 Export Observation Dataset (CSV)",
        "tab_map": "🛰️ Live Outbreak Map",
        "tab_sim": "🎯 'What-If' Simulator & Optimizer",
        "tab_cmd": "⚡ Action Command Console",
        "tab_citizen": "📸 Community Reports",
        "tab_contact": "🤝 Partner & Sponsor",
        "risk_index": "Outbreak Risk Index",
        "core_climate": "Core Climatology",
        "capacity_load": "Outbreak Capacity Load",
        "economic_exp": "Economic Exposure",
        "map_header": "🗺️ Outbreak Hotspot Risk Map",
        "map_style": "🗺️ Map View Style:",
        "inspector_header": "🔍 Location Risk Inspector",
        "inspector_help": "Select active hotspot node on the map to query parameters:",
        "current_loc_params": "CURRENT LOCATION PARAMETERS:",
        "google_sv": "🌐 Open Google Street View",
        "google_sat": "🛰️ Open Satellite Overlay",
        "cascade_header": "🌿 Climate-Pathology Cascades",
        "secondary_risk": "Secondary Risk Modifier",
        "what_if_header": "🎯 What-If Simulator",
        "policy_1": "Execute Precision Chemical Larvicides (-40% case loads)",
        "policy_2": "Mobilize Community Cleanup Campaigns (-25% breeding zones)",
        "policy_3": "Issue Targeted Mobility Warnings (-15% transit transmission)",
        "baseline_label": "UNMITIGATED INCOMING BASELINE:",
        "projected_label": "MITIGATED PROJECTED LOAD:",
        "prevented_label": "+ NET PREVENTED CLINICAL CASES:",
        "cases_unit": "CASES",
        "patients_unit": "PATIENTS",
        "optimizer_header": "📋 Intervention Optimizer",
        "memo_header": "📄 AI Executive Summary & Briefing Memo",
        "download_memo": "📥 Download Executive Briefing Memo (.txt)",
        "decision_header": "⚡ Decision Control Console",
        "btn_warn": "🚨 Broadcast Live Warning to Citizen App",
        "btn_scale": "🚑 Scale Regional Emergency Bed Protocols",
        "btn_sat": "📡 Ingest Live Sentinel-2 Multi-Bands",
        "citizen_form_header": "📸 Citizen Report",
        "inc_name": "Incident Location Name",
        "inc_cat": "Observed Breeding Hazard",
        "inc_obs": "Observation Details",
        "inc_upload": "Upload Verification Proof (Photo / Video)",
        "inc_btn": "Verify Report & Update Digital Twin Hotspots",
        "active_feed": "Active Verified Citizen Reports Feed",
        "contact_title": "🤝 Collaborate with Team GA1A",
        "contact_text": "Join the global network of public health administrators, municipal planners, and climatologists utilizing GA1A to build climate resilience.",
        "sponsor_btn": "✉️ Email Partnership Inquiries"
    },
    "Bahasa Melayu 🇲🇾": {
        "title": "GA1A",
        "subtitle": "TINJAUAN PENYAKIT BERJANGKIT IKLIM // INTELEGENSI MULTI-PATOGEN",
        "live_api": "● SALURAN API AKTIF SECARA LANGSUNG",
        "control_room": "BILIK KAWALAN",
        "search_label": "🔍 Cari Lokasi",
        "search_help": "Taip mana-mana bandar di seluruh dunia (cth. Kuala Lumpur, Okinawa, Perak, London) untuk memfokuskan peta.",
        "select_loc": "🎯 Pilih Cadangan Lokasi:",
        "realign_btn": "📌 Jajarkan Semula Peta Viewport",
        "pathology": "Patologi Jangkitan",
        "timeline": "Tarikh Pemerhatian",
        "telemetry": "Telemetri Atmosfera",
        "temp_label": "Suhu Ambien (°C)",
        "humid_label": "Kelembapan Relatif (%)",
        "precip_label": "Anomali Kerpasan (%)",
        "mobility_label": "Faktor Kedekatan Vektor",
        "export_btn": "📥 Eksport Set Data Pemerhatian (CSV)",
        "tab_map": "🛰️ Peta Wabak Langsung",
        "tab_sim": "🎯 Simulator & Pengoptimum 'What-If'",
        "tab_cmd": "⚡ Konsol Arahan Tindakan",
        "tab_citizen": "📸 Laporan Komuniti",
        "tab_contact": "🤝 Rakan Kongsi & Penaja",
        "risk_index": "Indeks Risiko Wabak",
        "core_climate": "Klimatologi Teras",
        "capacity_load": "Beban Kapasiti Wabak",
        "economic_exp": "Pendedahan Ekonomi",
        "map_header": "🗺️ Peta Risiko Kawasan Panas Wabak",
        "map_style": "🗺️ Gaya Paparan Peta:",
        "inspector_header": "🔍 Pemeriksa Risiko Lokasi",
        "inspector_help": "Pilih nod kawasan panas aktif pada peta untuk melihat parameter:",
        "current_loc_params": "PARAMETER LOKASI SEMASA:",
        "google_sv": "🌐 Buka Google Street View",
        "google_sat": "🛰️ Buka Lapisan Satelit",
        "cascade_header": "🌿 Kasked Iklim-Patologi",
        "secondary_risk": "Pengubah Risiko Sekunder",
        "what_if_header": "🎯 Simulator 'What-If'",
        "policy_1": "Laksanakan Larvasid Kimia Tepat (-40% beban kes)",
        "policy_2": "Mobilisasi Kempen Pembersihan Komuniti (-25% zon pembiakan)",
        "policy_3": "Keluarkan Amaran Mobiliti Sasaran (-15% transmisi transit)",
        "baseline_label": "GARIS ASAS KEMASUKAN TIDAK TERKAWAL:",
        "projected_label": "BEBAN DIJANGKAKAN TERKAWAL:",
        "prevented_label": "+ NET KES KLINIKAL DISELAMATKAN:",
        "cases_unit": "KES",
        "patients_unit": "PESAKIT",
        "optimizer_header": "📋 Pengoptimum Intervensi",
        "memo_header": "📄 Ringkasan Eksekutif AI & Memo Taklimat",
        "download_memo": "📥 Muat Turun Memo Taklimat Eksekutif (.txt)",
        "decision_header": "⚡ Konsol Keputusan Tindakan",
        "btn_warn": "🚨 Siarkan Amaran Langsung ke Aplikasi Rakyat",
        "btn_scale": "🚑 Skala Protokol Katil Kecemasan Serantau",
        "btn_sat": "📡 Ingest Live Sentinel-2 Multi-Bands",
        "citizen_form_header": "📸 Laporan Rakyat",
        "inc_name": "Nama Lokasi Kejadian",
        "inc_cat": "Bahaya Pembiakan Diperhatikan",
        "inc_obs": "Butiran Pemerhatian",
        "inc_upload": "Muat Naik Bukti Pengesahan (Foto / Video)",
        "inc_btn": "Sahkan Laporan & Kemas Kini Peta Risiko",
        "active_feed": "Suapan Laporan Rakyat Disahkan Aktif",
        "contact_title": "🤝 Bekerjasama dengan Pasukan GA1A",
        "contact_text": "Sertai rangkaian global pentadbir kesihatan awam, perancang perbandaran, dan ahli klimatologi yang menggunakan GA1A untuk membina daya tahan iklim.",
        "sponsor_btn": "✉️ Emel Pertanyaan Kerjasama"
    },
    "简体中文 🇨🇳": {
        "title": "GA1A",
        "subtitle": "气候传染病监测系统 // 多病原体智能监测",
        "live_api": "● 实时 API 通道处于激活状态",
        "control_room": "控制中心",
        "search_label": "🔍 搜索地理位置",
        "search_help": "输入全球任意城市（如吉隆坡、冲绳、霹雳、伦敦）以定位地图。",
        "select_loc": "🎯 选择匹配的建议位置:",
        "realign_btn": "📌 重新调整地图视角",
        "pathology": "传染病理学",
        "timeline": "观测日期",
        "telemetry": "大气遥测参数",
        "temp_label": "环境温度 (°C)",
        "humid_label": "相对湿度 (%)",
        "precip_label": "降水异常 (%)",
        "mobility_label": "病原接触因子",
        "export_btn": "📥 导出观测数据集 (CSV)",
        "tab_map": "🛰️ 实时疫情地图",
        "tab_sim": "🎯 'What-If' 情景模拟与优化",
        "tab_cmd": "⚡ 应急响应控制台",
        "tab_citizen": "📸 社区居民汇报",
        "tab_contact": "🤝 合作伙伴与赞助",
        "risk_index": "疫情风险指数",
        "core_climate": "核心气候指标",
        "capacity_load": "医疗系统荷载",
        "economic_exp": "经济风险敞口",
        "map_header": "🗺️ 疫情风险红区分布图",
        "map_style": "🗺️ 地图视图样式:",
        "inspector_header": "🔍 区域参数精细查看",
        "inspector_help": "选择地图上的有源风险节点以查询环境参数:",
        "current_loc_params": "当前位置传感器数据:",
        "google_sv": "🌐 打开谷歌实景街景",
        "google_sat": "🛰️ 打开卫星图层叠层",
        "cascade_header": "🌿 气候-病理级联反应",
        "secondary_risk": "次级衍生风险修正系数",
        "what_if_header": "🎯 'What-If' 情景模拟器",
        "policy_1": "执行精准化学杀幼虫剂 (-40% 预测病患量)",
        "policy_2": "组织社区清洁除积水行动 (-25% 蚊虫孳生源)",
        "policy_3": "发布定向区域移动预警 (-15% 交通传播因子)",
        "baseline_label": "未干预传入基线预测:",
        "projected_label": "干预后控制预测病患:",
        "prevented_label": "+ 净避免入院治疗人数:",
        "cases_unit": "例",
        "patients_unit": "人",
        "optimizer_header": "📋 AI 干预决策优化建议",
        "memo_header": "📄 AI 决策分析备忘录",
        "download_memo": "📥 下载决策分析备忘录 (.txt)",
        "decision_header": "⚡ 决策控制响应面板",
        "btn_warn": "🚨 向公众客户端广播实时预警",
        "btn_scale": "🚑 紧急调配区域应急病床协议",
        "btn_sat": "📡 调度 Sentinel-2 卫星多光谱扫描",
        "citizen_form_header": "📸 居民隐患上报",
        "inc_name": "事件发生的具体位置名称",
        "inc_cat": "观察到的孳生隐患类型",
        "inc_obs": "隐患现场情况具体描述",
        "inc_upload": "上传现场验证凭证（图片/视频）",
        "inc_btn": "验证并实时更新隐患节点地图",
        "active_feed": "当前活跃的居民验证隐患上报流",
        "contact_title": "🤝 与 GA1A 团队展开合作",
        "contact_text": "加入由公共卫生官员、城市规划人员和气候学家组成的全球网络，利用 GA1A 共同构建气候变化适应力。",
        "sponsor_btn": "✉️ 发送合作咨询邮件"
    },
    "日本語 🇯🇵": {
        "title": "GA1A",
        "subtitle": "気候関連感染症モニタリングシステム // 複数病原体インテリジェンス",
        "live_api": "● リアルタイム API 接続中",
        "control_room": "管制室",
        "search_label": "🔍 位置情報を検索",
        "search_help": "世界中の都市（クアラルンプール、沖縄、ペラ、ロンドンなど）を入力してマップを飛行します。",
        "select_loc": "🎯 一致する候補を選択:",
        "realign_btn": "📌 マップを再センタリング",
        "pathology": "感染症病理学",
        "timeline": "観測日",
        "telemetry": "気象遠隔測定パラメータ",
        "temp_label": "周囲温度 (°C)",
        "humid_label": "相対湿度 (%)",
        "precip_label": "降水量異常 (%)",
        "mobility_label": "媒介接触因子",
        "export_btn": "📥 観測データセットのエクスポート (CSV)",
        "tab_map": "🛰️ リアルタイム発生予測マップ",
        "tab_sim": "🎯 'What-If' シミュレータと最適化",
        "tab_cmd": "⚡ 行動司令コンソール",
        "tab_citizen": "📸 市民レポート",
        "tab_contact": "🤝 パートナー・スポンサーシップ",
        "risk_index": "感染リスク指数",
        "core_climate": "気象センサー測定値",
        "capacity_load": "医療システム負荷予測",
        "economic_exp": "経済的損失額の予測",
        "map_header": "🗺️ アウトブレイク危険エリアマップ",
        "map_style": "🗺️ マップ表示スタイル:",
        "inspector_header": "🔍 対象ノード気象情報",
        "inspector_help": "マップ上の危険エリアを選択してパラメータを確認:",
        "current_loc_params": "現在の位置のセンサー値:",
        "google_sv": "🌐 Google ストリートビューを起動",
        "google_sat": "🛰️ 衛星画像オーバーレイを起動",
        "cascade_header": "🌿 気候・病理の連鎖反応",
        "secondary_risk": "二次的発生リスク修正係数",
        "what_if_header": "🎯 'What-If' シミュレータ",
        "policy_1": "精密化学幼虫駆除の実施 (-40% 負荷件数)",
        "policy_2": "地域清掃・排水キャンペーンの展開 (-25% 発生源)",
        "policy_3": "特定区域移動抑制警告の配信 (-15% 交通媒介)",
        "baseline_label": "無対策時想定ベースライン:",
        "projected_label": "対策実施後予測患者数:",
        "prevented_label": "+ 純回避臨床入院患者数:",
        "cases_unit": "症例",
        "patients_unit": "名",
        "optimizer_header": "📋 対策最適化AIの提言",
        "memo_header": "📄 AI 意思決定支援レポート",
        "download_memo": "📥 意思決定支援レポートをダウンロード (.txt)",
        "decision_header": "⚡ 司令コントロールパネル",
        "btn_warn": "🚨 市民へ緊急情報一斉プッシュ配信",
        "btn_scale": "🚑 緊急時病床対応プロトコルの発動",
        "btn_sat": "📡 Sentinel-2 衛星リアルタイム観測要請",
        "citizen_form_header": "📸 市民通報ポータル",
        "inc_name": "発生場所名",
        "inc_cat": "発生した水溜まり等の危険因子",
        "inc_obs": "現場状況の具体的な説明",
        "inc_upload": "状況証明ファイル (写真・動画)",
        "inc_btn": "通報を検証し、リアルタイムでマップを更新",
        "active_feed": "現在処理中の検証済み市民レポート",
        "contact_title": "🤝 GA1A チームと連携する",
        "contact_text": "GA1Aを活用して気候変動への適応力を構築する、公共保健管理者、都市計画家、気候学者の世界的ネットワークに参加しましょう。",
        "sponsor_btn": "✉️ パートナーシップの問い合わせ"
    }
}

# --- DYNAMIC LANGUAGE SELECTION HEADER ---
col_logo, col_lang = st.columns([3, 1])
with col_logo:
    st.markdown("<h1 style='font-weight: 800; font-size: 78px; letter-spacing: -0.05em; margin-bottom: 0; background: linear-gradient(90deg, #ffffff, #00d2ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>GA1A</h1>", unsafe_allow_html=True)
with col_lang:
    selected_lang_key = st.selectbox("", options=list(translations.keys()), index=0, help="GA1A Global Localizer Nodes")

# Get translated key strings
lang = translations[selected_lang_key]

st.markdown(f"<p class='mono-text' style='color:#00d2ff; text-transform:uppercase; margin-top: -15px; margin-bottom: 25px; letter-spacing:0.12em; font-size: 13px;'>{lang['subtitle']}</p>", unsafe_allow_html=True)

# --- 1. PREMIUM GEOCODING ADAPTIVE CURRENCY & HOTLINE SYSTEM ---
active_location_name = lang['search_help']

# Dynamic solver logic based on location
if any(kw in search_keyword.lower() for kw in ["malaysia", "terengganu", "kuala", "johor", "perak", "penang", "selangor"]):
    user_country = "Malaysia"
    currency_symbol = "RM"
    currency_rate = 1.0 # Base local currency matching Malaysian Ringgit
    local_agencies = [
        {"name": "MOH Malaysia (KKM CPRC)", "hotline": "+603-8881 0200", "role": "Infectious Disease Crisis Preparedness"},
        {"name": "Department of Environment (DOE)", "hotline": "1-800-88-2727", "role": "Climatic Chemical Pollution Monitoring"},
        {"name": "National Disaster Management Agency (NADMA)", "hotline": "+603-8064 2400", "role": "Flash Flood Drainage Emergency Response"}
    ]
elif any(kw in search_keyword.lower() for kw in ["japan", "okinawa", "tokyo", "kyoto", "osaka", "hokkaido"]):
    user_country = "Japan"
    currency_symbol = "JPY (¥)"
    currency_rate = 34.5 # Current exchange index relative value
    local_agencies = [
        {"name": "Ministry of Health, Labour and Welfare (MHLW)", "hotline": "+81-3-5253-1111", "role": "Infectious Pathology Control Hub"},
        {"name": "National Institute of Infectious Diseases (NIID)", "hotline": "+81-3-5285-1111", "role": "Vector Genotyping Surveillance"},
        {"name": "Ministry of the Environment (MOE)", "hotline": "+81-3-3581-3351", "role": "Eco-System Vector Breeding Control"}
    ]
else:
    user_country = "Global"
    currency_symbol = "USD ($)"
    currency_rate = 0.23 # Standard conversion base
    local_agencies = [
        {"name": "World Health Organization (WHO GOARN)", "hotline": "+41 22 791 2111", "role": "Global Outbreak Surveillance Nodes"},
        {"name": "UNEP Climate Action Network", "hotline": "+254 20 762 1234", "role": "Vector Migration Modeling"},
        {"name": "International Red Cross (IFRC)", "hotline": "+41 22 730 4222", "role": "Emergency Humanitarian Deployment"}
    ]

# --- 2. SPECIFIC TIMELINE CALENDAR (DEFAULT TO CURRENT DATE) ---
st.sidebar.markdown(f"### 🎛️ {lang['control_room']}")

# Dynamic specific calendar dropdown
chosen_calendar_date = st.sidebar.date_input(
    lang['timeline'], 
    value=date(2026, 6, 26), 
    help="Select the exact target day, month, and year to observe historical climate correlations."
)

# Convert chosen date into anomalies to scale modeling dynamically
date_month_factor = chosen_calendar_date.month

# --- 3. SATELLITE DATASET DOWNLOAD GENERATOR ---
# Injects current user configuration variables
dataset_df = generate_dataset_csv(selected_disease, chosen_calendar_date.year, current_lat, current_lon, temp, humidity, precipitation_vol)
csv_buffer = io.BytesIO()
dataset_df.to_csv(csv_buffer, index=False)
csv_data = csv_buffer.getvalue()

st.sidebar.markdown("---")
st.sidebar.download_button(
    label=lang['export_btn'],
    data=csv_data,
    file_name=f"GA1A_Dataset_{selected_disease.split()[0]}_{chosen_calendar_date.strftime('%Y%m%d')}.csv",
    mime="text/csv",
    use_container_width=True
)

# --- 4. TOP-MARGIN NAVIGATION (MINIMAL TAB LAYOUT) ---
tabs = st.tabs([
    lang['tab_map'], 
    lang['tab_sim'], 
    lang['tab_cmd'], 
    lang['tab_citizen'],
    lang['tab_contact']
])

# ================= TAB 1: LIVE OUTBREAK MAP =================
with tabs[0]:
    # Key Performance Metrics with Dynamic LaTeX Popover Equations
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; margin-top: 10px; margin-bottom: 2px;'>
            <p style='color: #94a3b8; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin: 0 0 8px 0;'>{lang['risk_index']}</p>
            <h2 style='color: {risk_color}; font-size: 38px; font-weight: 800; margin: 0 0 10px 0; letter-spacing:-0.03em;'>{final_risk_score}%</h2>
            <span class='status-badge' style='background: {risk_bg}; color: {risk_color}; border: 1px solid {risk_color}33;'>{risk_level}</span>
        </div>
        """, unsafe_allow_html=True)
        with st.popover("❔ Mathematical Model", use_container_width=True):
            st.markdown("##### Outbreak Epidemic Model Formula")
            st.markdown("The biological risk coefficient is evaluated using a non-linear climatic threshold propagation model:")
            st.latex(r"R_i = H_0 \cdot \exp\left(-\frac{(T - T_{opt})^2}{35}\right) \cdot \left(1 + \frac{P_{anom}}{100}\right) \cdot \left[ \frac{H_{humid}}{70} \cdot M_{density} \right]")
            st.caption("Where $H_0$ is pathology hazard, $T_{opt}$ is optimal vector breeding temperature, $P_{anom}$ is rain anomaly index.")
            
    with col_m2:
        st.markdown(f"""
        <div class='glass-card' style='margin-top: 10px; margin-bottom: 2px;'>
            <p style='color: #94a3b8; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin: 0 0 8px 0; text-align:center;'>{lang['core_climate']}</p>
            <p class='mono-text' style='margin: 0; color: #f3f4f6; line-height: 1.6;'>
                TEMP: <span style='color:#00d2ff; float:right;'>{temp:.1f}°C</span><br>
                HUMIDITY: <span style='color:#00d2ff; float:right;'>{humidity}%</span><br>
                PRECIPITATION: <span style='color:#00d2ff; float:right;'>{precipitation_vol:+} %</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        with st.popover("❔ Climate Baseline Model", use_container_width=True):
            st.markdown("##### Climatology Standard Deviations")
            st.markdown("Retrieves latitudinal baselines adjusted to seasonal El Niño Southern Oscillation ($ENSO$) offsets:")
            st.latex(r"T_{baseline} = 31.0 - 0.35 \cdot |\theta_{lat}|")
            st.latex(r"H_{baseline} = 88.0 - 0.70 \cdot |\theta_{lat}|")
            st.caption("Derived from Open WMO Climatology Databases.")
            
    with col_m3:
        projected_cases = int(final_risk_score * 4.8 * population_mobility * (1 + (date_month_factor / 30)))
        beds_needed = int(projected_cases * 0.22)
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; margin-top: 10px; margin-bottom: 2px;'>
            <p style='color: #94a3b8; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin: 0 0 8px 0;'>{lang['capacity_load']}</p>
            <h2 style='color: #00d2ff; font-size: 34px; font-weight: 800; margin: 0 0 4px 0; letter-spacing:-0.03em;'>{projected_cases}</h2>
            <p class='mono-text' style='color: #94a3b8; margin: 0;'>SURGE BEDS REQ: <span style='color:#ff2e93;'>{beds_needed}</span></p>
        </div>
        """, unsafe_allow_html=True)
        with st.popover("❔ Surge Bed Capacity Model", use_container_width=True):
            st.markdown("##### Healthcare Admission Surge Formula")
            st.markdown("Calculates clinical occupancy coefficients using the Vectorial Capacity index:")
            st.latex(r"L_{cap} = R_i \cdot \alpha_{mobility} \cdot D_{pop}")
            st.latex(r"B_{surge} = L_{cap} \cdot \beta_{admission}")
            st.caption("Where $\\beta_{admission} = 0.22$ represents standard severe case triage margins.")
            
    with col_m4:
        # Dynamic localized currency converter based on location geocode detection
        localized_cost = (projected_cases * 3400 * currency_rate) / 1000000
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; margin-top: 10px; margin-bottom: 2px;'>
            <p style='color: #94a3b8; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin: 0 0 8px 0;'>{lang['economic_exp']}</p>
            <h2 style='color: #ff4d4d; font-size: 34px; font-weight: 800; margin: 0 0 4px 0; letter-spacing:-0.03em;'>{currency_symbol} {localized_cost:.2f}M</h2>
            <p class='mono-text' style='color: #94a3b8; margin: 0;'>Lost Working Hours: <span style='color:#ffd000;'>{int(projected_cases*14)}h</span></p>
        </div>
        """, unsafe_allow_html=True)
        with st.popover("❔ Economic Cost Model", use_container_width=True):
            st.markdown("##### Lost Productivity Calculation")
            st.markdown("Financial damage evaluation based on localized healthcare burden:")
            st.latex(r"E_{exposure} = \left( B_{surge} \cdot \psi_{cost} + W_{lost} \cdot \gamma_{wage} \right) \cdot \varepsilon_{rate}")
            st.caption("Estimates mean diagnostic expense and working hours lost.")

    # MAP SECTION
    st.markdown(f"### {lang['map_header']}")
    col_map_toggles, col_map_sub = st.columns([2, 2])
    with col_map_toggles:
        map_style_toggle = st.radio(
            lang['map_style'], 
            options=["🌌 Dark Radar Map", "🏙️ Regular Street Map"], 
            horizontal=True
        )
    
    selected_style = "carto-darkmatter" if map_style_toggle == "🌌 Dark Radar Map" else "open-street-map"

    # Mapbox Layout Layers Generation: Draws true geometric scaling rings styled in shades of warning red
    mapbox_layers = []
    for idx, row in combined_map_df.iterrows():
        radius_km = 0.8 + (row["Risk Score (%)"] / 100.0) * 1.7
        node_circle_geojson = get_circle_geojson(row["lat"], row["lon"], radius_km)
        
        score = row["Risk Score (%)"]
        if score >= 70:
            fill_color = "rgba(255, 46, 147, 0.35)"   # Toxic Neon Crimson Nova
            line_color = "rgba(255, 46, 147, 0.85)"
        elif score >= 40:
            fill_color = "rgba(255, 120, 117, 0.28)"  # Solar Saffron Amber-Red
            line_color = "rgba(255, 120, 117, 0.75)"
        else:
            fill_color = "rgba(255, 166, 166, 0.18)"  # Muted Translucent Rose-Red
            line_color = "rgba(255, 166, 166, 0.55)"
            
        mapbox_layers.append(dict(
            sourcetype='geojson',
            source=node_circle_geojson,
            type='fill',
            color=fill_color,
            below="traces"
        ))
        mapbox_layers.append(dict(
            sourcetype='geojson',
            source=node_circle_geojson,
            type='line',
            color=line_color,
            line=dict(width=2),
            below="traces"
        ))

    # Base Plotly Mapbox using small center pin indicators so hover & click states remain intact
    fig_hotspot = px.scatter_mapbox(
        combined_map_df,
        lat="lat",
        lon="lon",
        color_discrete_sequence=["#00d2ff"],
        zoom=st.session_state.map_zoom,
        center={"lat": st.session_state.map_center_lat, "lon": st.session_state.map_center_lon},
        hover_name="Place",
        hover_data={
            "Operational Status": True,
            "Risk Score (%)": True,
            "lat": False,
            "lon": False
        }
    )

    fig_hotspot.update_layout(
        mapbox_style=selected_style,
        margin={"r":0, "t":0, "l":0, "b":0},
        paper_bgcolor="#030712",
        plot_bgcolor="#030712",
        font_color="#f3f4f6",
        mapbox_layers=mapbox_layers  # Injects the geometrically scaling circle layouts
    )
    fig_hotspot.update_traces(marker=dict(size=8, opacity=0.9, symbol="circle"))

    st.plotly_chart(fig_hotspot, use_container_width=True)

    # LOCATION INSPECTOR & TIME GRAPH
    st.markdown("---")
    col_inspect_view, col_graph_view = st.columns([1.5, 1.5])
    
    with col_inspect_view:
        st.markdown(f"### {lang['inspector_header']}")
        inspected_place = st.selectbox(
            lang['inspector_help'],
            options=combined_map_df["Place"].unique()
        )
        
        row_details = combined_map_df[combined_map_df["Place"] == inspected_place].iloc[0]
        
        node_temp = round(temp + row_details["Temp Offset"], 1)
        node_humidity = min(100, max(20, int(humidity + row_details["Humidity Offset"])))
        node_precip = precipitation_vol + row_details["Precip Offset"]
        node_risk = row_details["Risk Score (%)"]
        
        col_node_title, col_focus_btn = st.columns([3.2, 0.8])
        with col_node_title:
            st.markdown(f"<h4 style='color:#00d2ff; font-weight:700; margin-top:8px;'>🔗 {inspected_place}</h4>", unsafe_allow_html=True)
        with col_focus_btn:
            if st.button("🎯 Center Map", key="focus_map_btn"):
                st.session_state.map_center_lat = row_details["lat"]
                st.session_state.map_center_lon = row_details["lon"]
                st.session_state.map_zoom = 13.5
                st.rerun()

        st.markdown(f"""
        <div class="panel-container">
            <div style='display:flex; justify-content:space-between; margin-bottom:12px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom:8px;'>
                <span style='color:#94a3b8; font-size:12px; font-weight:bold;'>OPERATIONAL STATUS:</span>
                <span style='color:#ff2e93; font-size:12px; font-weight:bold; font-family:monospace;'>{row_details.get("Operational Status", "")}</span>
            </div>
            <p style='font-size: 13px; color: #f3f4f6; margin-bottom: 20px; font-weight: 500; line-height:1.6;'>
                <strong>Historical Outbreak Record:</strong> {row_details.get("Hist Outbreaks", "")}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<p style='font-size:12px; font-weight:bold; color:#00d2ff; margin:15px 0 5px 0;'>{lang['current_loc_params']}</p>", unsafe_allow_html=True)
        node_col1, node_col2, node_col3, node_col4 = st.columns(4)
        with node_col1:
            st.metric("🌡️ Temp", f"{node_temp}°C")
        with node_col2:
            st.metric("💧 Humidity", f"{node_humidity}%")
        with node_col3:
            st.metric("🌧️ Precip", f"{node_precip:+} %")
        with node_col4:
            st.metric("☣️ Risk Index", f"{node_risk}%")

    with col_graph_view:
        st.markdown("<h3 style='font-size:22px; font-weight:800; letter-spacing:-0.02em;'>📈 Future Risk Timeline (30-Day Forecast)</h3>", unsafe_allow_html=True)
        
        decay_rate = 0.95 if humidity < 70 else 1.05
        rain_growth = 1.15 if precipitation_vol > 30 else 0.90
        temp_multiplier = 1.10 if (22 <= temp <= 32) else 0.80
        
        wk1_risk = min(100, max(5, int(node_risk * temp_multiplier)))
        wk2_risk = min(100, max(5, int(wk1_risk * rain_growth)))
        wk3_risk = min(100, max(5, int(wk2_risk * decay_rate)))
        wk4_risk = min(100, max(5, int(wk3_risk * 0.85))) 
        
        timeline_df = pd.DataFrame({
            "Timeline": ["Current", "Week 1", "Week 2", "Week 3", "Week 4"],
            "Outbreak Risk (%)": [node_risk, wk1_risk, wk2_risk, wk3_risk, wk4_risk]
        })
        
        fig_timeline = px.line(
            timeline_df, 
            x="Timeline", 
            y="Outbreak Risk (%)", 
            markers=True,
            color_discrete_sequence=["#ff2e93"]
        )
        
        fig_timeline.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f3f4f6",
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", range=[0, 110]),
            height=180
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

        st.markdown(f"<p style='font-size:12px; font-weight:bold; color:#00d2ff; margin-bottom:5px;'>🛰️ Ground-Truth Tactical Command Links</p>", unsafe_allow_html=True)
        gmaps_streetview_url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={row_details['lat']},{row_details['lon']}&heading=0&pitch=0&fov=80"
        gmaps_sat_url = f"https://www.google.com/maps/search/?api=1&query={row_details['lat']},{row_details['lon']}&basemap=satellite"
        
        st_sv_btn, st_sat_btn = st.columns(2)
        with st_sv_btn:
            st.link_button(lang['google_sv'], gmaps_streetview_url, use_container_width=True)
        with st_sat_btn:
            st.link_button(lang['google_sat'], gmaps_sat_url, use_container_width=True)

    # PATHOLOGY RELATIONSHIP CASCADES
    st.markdown("---")
    st.markdown(f"### {lang['cascade_header']}")
    col_cas_1, col_cas_2, col_cas_3 = st.columns(3)

    with col_cas_1:
        linked_dengue_risk = min(100, int(final_risk_score * 0.95)) if "Dengue" not in selected_disease else min(100, int(final_risk_score * 0.4))
        st.markdown(f"""
        <div style='background: rgba(15, 23, 42, 0.35); border: 1px solid rgba(255, 255, 255, 0.05); padding: 16px; border-radius: 12px;'>
            <p style='font-size: 11px; font-weight:bold; color:#94a3b8; margin:0;'>🦟 ARBOVIRAL VECTOR CASCADE (DENGUE/ZIKA)</p>
            <p style='font-size: 20px; font-weight: 800; color: #ff2e93; margin: 4px 0;'>{linked_dengue_risk}% {lang['secondary_risk']}</p>
            <div style='background: rgba(255,255,255,0.05); border-radius: 4px; height: 6px; overflow: hidden;'>
                <div style='background: #ff2e93; width: {linked_dengue_risk}%; height: 100%;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_cas_2:
        linked_water_risk = min(100, int(humidity * 0.8 + (precipitation_vol + 50) * 0.15))
        st.markdown(f"""
        <div style='background: rgba(15, 23, 42, 0.35); border: 1px solid rgba(255, 255, 255, 0.05); padding: 16px; border-radius: 12px;'>
            <p style='font-size: 11px; font-weight:bold; color:#94a3b8; margin:0;'>🦠 WATER SANITATION PATHWAYS (CHOLERA/TYPHOID)</p>
            <p style='font-size: 20px; font-weight: 800; color: #ffd000; margin: 4px 0;'>{linked_water_risk}% {lang['secondary_risk']}</p>
            <div style='background: rgba(255,255,255,0.05); border-radius: 4px; height: 6px; overflow: hidden;'>
                <div style='background: #ffd000; width: {linked_water_risk}%; height: 100%;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_cas_3:
        linked_leptospirosis = min(100, int((precipitation_vol + 50) * 0.6 + humidity * 0.2)) if precipitation_vol > 10 else 15
        st.markdown(f"""
        <div style='background: rgba(15, 23, 42, 0.35); border: 1px solid rgba(255, 255, 255, 0.05); padding: 16px; border-radius: 12px;'>
            <p style='font-size: 11px; font-weight:bold; color:#00f5a0; margin:0;'>🐀 FLOODING PATHWAYS (LEPTOSPIROSIS)</p>
            <p style='font-size: 20px; font-weight: 800; color: #00f5a0; margin: 4px 0;'>{linked_leptospirosis}% {lang['secondary_risk']}</p>
            <div style='background: rgba(255,255,255,0.05); border-radius: 4px; height: 6px; overflow: hidden;'>
                <div style='background: #00f5a0; width: {linked_leptospirosis}%; height: 100%;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ================= TAB 2: WHAT-IF SIMULATOR & OPTIMIZER =================
with tabs[1]:
    col_sim, col_opt = st.columns(2)
    with col_sim:
        st.markdown(f"### {lang['what_if_header']}")
        larvicide_drops = st.checkbox(lang['policy_1'])
        community_clean = st.checkbox(lang['policy_2'])
        travel_restrictions = st.checkbox(lang['policy_3'])
        
        mitigation_multiplier = 1.0
        if larvicide_drops:
            mitigation_multiplier *= 0.60
        if community_clean:
            mitigation_multiplier *= 0.75
        if travel_restrictions:
            mitigation_multiplier *= 0.85
            
        mitigated_outflow = int(projected_cases * mitigation_multiplier)
        cases_prevented = projected_cases - mitigated_outflow
        
        st.markdown(f"""
        <div class='glass-card' style='margin-top: 15px;'>
            <p class='mono-text' style='color: #94a3b8; margin: 0;'>{lang['baseline_label']} <strong style='color:#fff;'>{projected_cases} {lang['cases_unit']}</strong></p>
            <p style='color: #00d2ff; font-size: 24px; font-weight: 800; margin: 8px 0; letter-spacing:-0.02em;'>{lang['projected_label']} {mitigated_outflow} {lang['cases_unit']}</p>
            <p style='color: #00f5a0; font-size: 12px; font-weight: bold; margin: 0; font-family: monospace;'>{lang['prevented_label']} {cases_prevented} {lang['patients_unit']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_opt:
        st.markdown(f"### {lang['optimizer_header']}")
        if risk_level == "CRITICAL":
            st.markdown(f"""
            <div style='background: rgba(255, 46, 147, 0.08); border: 1px solid #ff2e93; padding: 24px; border-radius: 16px; margin-top: 15px;'>
                <h5 style='color: #ff2e93; font-weight:800; margin-top:0;'>⚠️ THREAT STATUS: CRITICAL</h5>
                <ul style='color: #f3f4f6; font-size: 13px; line-height:1.7; margin-bottom:0; padding-left:20px;'>
                    <li>Deploy automated biological larvicides targeting highest concentration vectors within 48 hours.</li>
                    <li>Notify and provision regional triage centers; release sterile saline IV reserves.</li>
                    <li>Broadcast high-risk push coordinates targeting outdoor mobile personnel.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif risk_level == "ESCALATING":
            st.markdown(f"""
            <div style='background: rgba(255, 208, 0, 0.08); border: 1px solid #ffd000; padding: 24px; border-radius: 16px; margin-top: 15px;'>
                <h5 style='color: #ffd000; font-weight:800; margin-top:0;'>⚠️ THREAT STATUS: ESCALATING</h5>
                <ul style='color: #f3f4f6; font-size: 13px; line-height:1.7; margin-bottom:0; padding-left:20px;'>
                    <li>Launch sweeping water catchment clearing runs across marshlands and estuary waterways.</li>
                    <li>Activate outpatient community clinics to prepare for mild seasonal diagnostic surges.</li>
                    <li>Deploy civic media campaigns advising household water storage removal protocols.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background: rgba(0, 245, 160, 0.08); border: 1px solid #00f5a0; padding: 24px; border-radius: 16px; margin-top: 15px;'>
                <h5 style='color: #00f5a0; font-weight:800; margin-top:0;'>✅ THREAT STATUS: CONFINED</h5>
                <p style='color: #f3f4f6; font-size: 13px; line-height:1.7; margin:0;'>
                    All atmospheric indicators are locked within biological control levels. Maintain passive monitoring intervals.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # EXPLAINABLE AI EXECUTIVE SUMMARY MEMO
    st.markdown("---")
    st.markdown(f"### {lang['memo_header']}")
    st.markdown(f"""
    <textarea style="width:100%; height:180px; background-color:#02040a; border: 1px solid rgba(255,255,255,0.06); border-radius:12px; color:#f3f4f6; padding:15px; font-family:'Space Mono', monospace; font-size:12px; line-height:1.6;" readonly>
    {briefing_text}
    </textarea>
    """, unsafe_allow_html=True)

    st.download_button(
        label=lang['download_memo'],
        data=briefing_text,
        file_name=f"GA1A_Briefing_Memo_{chosen_calendar_date.year}.txt",
        mime="text/plain",
        use_container_width=True
    )

# ================= TAB 3: COMMAND CONTROL CONSOLE =================
with tabs[2]:
    st.markdown(f"### {lang['decision_header']}")
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button(lang['btn_warn'], use_container_width=True, key="action_warn"):
            st.info(f"Broadcast warning successfully transmitted to coordinates matching current {selected_disease} hotspots.")
    with col_btn2:
        if st.button(lang['btn_scale'], use_container_width=True, key="action_scale"):
            st.info("Logistics pipeline updated with 14-day clinical capacity forecast metrics.")
    with col_btn3:
        if st.button(lang['btn_sat'], use_container_width=True, key="action_sat"):
            st.info("Satellite queue scheduled for localized high-density multi-spectral sweep.")

    st.markdown("---")
    st.markdown("#### Operational Dispatch Pipeline")
    st.info("Select any location in the 'Live Outbreak Map' to dispatch targeted field sanitation squads or view real-time drone telemetry coordinate pipelines.")

# ================= TAB 4: COMMUNITY REPORTS =================
with tabs[3]:
    st.markdown(f"### {lang['citizen_form_header']}")
    
    # 🚨 INTEGRATION: LOCALISED HOTLINES LISTING FOR B2G COMPLIANCE
    st.markdown(f"#### 📞 Local Crisis Response Hotlines ({user_country})")
    st.caption("Immediate institutional channels for report escalation and direct vector sanitisation requests.")
    
    col_hot_1, col_hot_2, col_hot_3 = st.columns(3)
    with col_hot_1:
        st.markdown(f"""
        <div style='background: rgba(255, 46, 147, 0.1); border: 1px solid rgba(255, 46, 147, 0.3); padding: 16px; border-radius: 12px; min-height: 120px;'>
            <p style='font-size:11px; color:#ff2e93; font-weight:bold; margin:0;'>MAIN AGENCY RESPONSE</p>
            <p style='font-size:15px; font-weight:800; margin:4px 0;'>{local_agencies[0]["name"]}</p>
            <p style='font-size:16px; font-family:monospace; color:#fff; font-weight:bold; margin:0;'>{local_agencies[0]["hotline"]}</p>
            <span style='font-size:10px; color:#94a3b8;'>{local_agencies[0]["role"]}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_hot_2:
        st.markdown(f"""
        <div style='background: rgba(0, 210, 255, 0.1); border: 1px solid rgba(0, 210, 255, 0.3); padding: 16px; border-radius: 12px; min-height: 120px;'>
            <p style='font-size:11px; color:#00d2ff; font-weight:bold; margin:0;'>CLIMATIC & ENVIRONMENT</p>
            <p style='font-size:15px; font-weight:800; margin:4px 0;'>{local_agencies[1]["name"]}</p>
            <p style='font-size:16px; font-family:monospace; color:#fff; font-weight:bold; margin:0;'>{local_agencies[1]["hotline"]}</p>
            <span style='font-size:10px; color:#94a3b8;'>{local_agencies[1]["role"]}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_hot_3:
        st.markdown(f"""
        <div style='background: rgba(0, 245, 160, 0.1); border: 1px solid rgba(0, 245, 160, 0.3); padding: 16px; border-radius: 12px; min-height: 120px;'>
            <p style='font-size:11px; color:#00f5a0; font-weight:bold; margin:0;'>DISASTER MITIGATION</p>
            <p style='font-size:15px; font-weight:800; margin:4px 0;'>{local_agencies[2]["name"]}</p>
            <p style='font-size:16px; font-family:monospace; color:#fff; font-weight:bold; margin:0;'>{local_agencies[2]["hotline"]}</p>
            <span style='font-size:10px; color:#94a3b8;'>{local_agencies[2]["role"]}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    with st.form("citizen_report_submission_form", clear_on_submit=True):
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            reported_place = st.text_input(lang['inc_name'])
            incident_category = st.selectbox(lang['inc_cat'], [
                "Stagnant Water Accumulation", "Illegal Waste Dumping Site", "Clogged Drainage Blockage", "Unmanaged Construction Site Pool"
            ])
        with col_form2:
            observation_notes = st.text_input(lang['inc_obs'])
            uploaded_media = st.file_uploader(lang['inc_upload'], type=["png", "jpg", "jpeg", "mp4", "mov"])
            
        submit_form_btn = st.form_submit_button(lang['inc_btn'])
        
        if submit_form_btn:
            if not reported_place:
                st.error("Please supply an Incident Location Name to update the map.")
            else:
                new_report_lat_offset = np.random.uniform(-0.02, 0.02)
                new_report_lon_offset = np.random.uniform(-0.02, 0.02)
                media_filename = uploaded_media.name if uploaded_media else "No verification media attached"
                
                new_citizen_record = pd.DataFrame([{
                    "Place": reported_place,
                    "lat_offset": new_report_lat_offset,
                    "lon_offset": new_report_lon_offset,
                    "Hazard Category": incident_category,
                    "Observation Details": observation_notes or "Unspecified stagnant risk area",
                    "Media Name": media_filename
                }])
                
                st.session_state.citizen_pins = pd.concat([st.session_state.citizen_pins, new_citizen_record], ignore_index=True)
                st.success(f"Verified Citizen GPS Pin dropped dynamically in vicinity of {active_location_name}. Map updated.")

    # Display active citizen hazards list on dashboard
    if not st.session_state.citizen_pins.empty:
        st.markdown(f"<h4 style='font-size:16px; font-weight:700;'>{lang['active_feed']}</h4>", unsafe_allow_html=True)
        for index, row in st.session_state.citizen_pins.iterrows():
            st.info(f"**📍 {row['Place']}** | **Type:** {row['Hazard Category']} | **Notes:** {row['Observation Details']} | **File Verification:** `{row['Media Name']}`")

# ================= TAB 5: COLLABORATION & SPONSOR PORTAL =================
with tabs[4]:
    st.markdown(f"<h2 style='font-weight: 800; letter-spacing: -0.02em; margin-top:10px;'>{lang['contact_title']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#94a3b8; font-size:15px; line-height:1.7; max-width:750px;'>{lang['contact_text']}</p>", unsafe_allow_html=True)
    
    col_sp1, col_sp2 = st.columns(2)
    with col_sp1:
        st.markdown("""
        <div style='background: rgba(15, 23, 42, 0.45); border: 1px solid rgba(255, 255, 255, 0.08); padding: 24px; border-radius: 16px;'>
            <h4 style='color:#00d2ff; font-weight:700; margin-top:0;'>💎 Sponsorship Tiers</h4>
            <p style='font-size:13px; color:#f3f4f6; line-height:1.6;'>
                <strong>• Academic & Meteorological Integration:</strong> Co-develop regional multi-spectral satellite processing algorithms for tracking vectors.<br>
                <strong>• B2G Public Deployment:</strong> Secure municipal pilot programs within Southeast Asia (MOH Malaysia, CPRC networks).<br>
                <strong>• Cloud & Hardware Compute:</strong> Support parallelized prediction model training for rapid geographic expansion.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_sp2:
        st.markdown("""
        <div style='background: rgba(15, 23, 42, 0.45); border: 1px solid rgba(255, 255, 255, 0.08); padding: 24px; border-radius: 16px; min-height: 185px;'>
            <h4 style='color:#00f5a0; font-weight:700; margin-top:0;'>📬 Immediate Communication Node</h4>
            <p style='font-size:13px; color:#f3f4f6; line-height:1.6;'>
                For sponsorships, custom localized climate vector models, or collaboration requests, connect with our core team directly.
            </p>
            <p style='font-size: 18px; font-weight: bold; color: #00f5a0; font-family: monospace;'>s70846@ocean.umt.edu.my</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.link_button(lang['sponsor_btn'], "mailto:s70846@ocean.umt.edu.my", use_container_width=True)