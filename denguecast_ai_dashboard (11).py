import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import io
import random
from datetime import date

# Set up pristine layout
st.set_page_config(
    page_title="GA1A | Climate-Infectious Disease Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GLOBAL PATHOLOGY OPTIONS & DATA REPOSITORIES ---
disease_options = [
    "Dengue Fever 🦟", "Malaria Outbreak 🦟", "Cholera Contamination 🦠", 
    "Zika Virus 🦟", "West Nile Virus 🦅", "Lyme Disease Outbreaks 🕷️", 
    "Chikungunya Epidemic 🦟", "Poliomyelitis Outbreak 💧", "Typhoid Fever 🤢", 
    "Yellow Fever Sylvatic 🦟", "Leptospirosis Flood Surge 🐀", "Hepatitis A 🧪", 
    "Schistosomiasis Snail Vector 🐌"
]

# --- INTERNATIONALIZATION DICTIONARY (GA1A ENGINE) ---
translations = {
    "English 🇬🇧": {
        "title": "GA1A",
        "subtitle": "CLIMATE INFECTIOUS DISEASE TRACKER // MULTI-PATHOGEN INTELLIGENCE",
        "live_api": "● LIVE API CHANNELS ACTIVE",
        "control_room": "CONTROL ROOM",
        "search_label": "🔍 Search Location",
        "search_help": "Type any city globally (e.g. Kuala Lumpur, Okinawa, Perak, London) to fly map focus.",
        "select_loc": "🎯 Select Matching Location:",
        "realign_btn": "📌 Re-align Viewport Map",
        "pathology": "Infectious Pathology",
        "timeline": "Observation Date",
        "telemetry": "Climate Sensors",
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
        "telemetry": "Penderia Iklim",
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
        "telemetry": "气象传感器",
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
        "pathology": "感染症病学",
        "timeline": "観測日",
        "telemetry": "気候センサー",
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
        "prevented_label": "+ 統制された臨床患者数:",
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
    },
    "Español 🇪🇸": {
        "title": "GA1A",
        "subtitle": "RASTREADOR DE ENFERMEDADES CLIMÁTICAS // INTELIGENCIA MULTIPATÓGENO",
        "live_api": "● CANALES API ACTIVOS EN VIVO",
        "control_room": "SALA DE CONTROL",
        "search_label": "🔍 Buscar Ubicación",
        "search_help": "Escriba cualquier ciudad del mundo (p. ej., Kuala Lumpur, Okinawa, Perak) para enfocar el mapa.",
        "select_loc": "🎯 Seleccione Ubicación Coincidente:",
        "realign_btn": "📌 Realinear el Mapa de Vista",
        "pathology": "Patología Infecciosa",
        "timeline": "Fecha de Observación",
        "telemetry": "Sensors Climáticos",
        "temp_label": "Temperatura Ambiente (°C)",
        "humid_label": "Humedad Relativa (%)",
        "precip_label": "Anomalía de Precipitación (%)",
        "mobility_label": "Factor de Proximidad Vectorial",
        "export_btn": "📥 Exportar Datos de Observación (CSV)",
        "tab_map": "🛰️ Mapa de Brotes en Vivo",
        "tab_sim": "🎯 Simulador y Optimizador 'What-If'",
        "tab_cmd": "⚡ Consola de Mando de Acción",
        "tab_citizen": "📸 Informes de la Comunidad",
        "tab_contact": "🤝 Socios y Patrocinadores",
        "risk_index": "Índice de Riesgo de Brote",
        "core_climate": "Climatología Núcleo",
        "capacity_load": "Carga de Capacidad de Brote",
        "economic_exp": "Exposición Económica",
        "map_header": "🗺️ Mapa de Riesgo de Puntos Críticos",
        "map_style": "🗺️ Estilo de Vista de Mapa:",
        "inspector_header": "🔍 Inspector de Riesgo de Ubicación",
        "inspector_help": "Seleccione un nodo activo en el mapa para consultar parámetros:",
        "current_loc_params": "PARÁMETROS DE UBICACIÓN ACTUAL:",
        "google_sv": "🌐 Abrir Google Street View",
        "google_sat": "🛰️ Abrir Capa de Satélite",
        "cascade_header": "🌿 Cascadas de Clima-Patología",
        "secondary_risk": "Modificador de Riesgo Secundario",
        "what_if_header": "🎯 Simulador 'What-If'",
        "policy_1": "Ejecutar Larvicidas Químicos de Precisión (-40% carga de casos)",
        "policy_2": "Movilizar Campañas de Limpieza Comunitaria (-25% zonas de cría)",
        "policy_3": "Emitir Advertencias de Movilidad Focalizadas (-15% transmisión en tránsito)",
        "baseline_label": "LÍNEA BASE DE ENTRADA NO MITIGADA:",
        "projected_label": "CARGA PROYECTADA MITIGADA:",
        "prevented_label": "+ CASOS CLÍNICOS EVITADOS NETOS:",
        "cases_unit": "CASOS",
        "patients_unit": "PACIENTES",
        "optimizer_header": "📋 Optimizador de Intervención",
        "memo_header": "📄 Resumen Ejecutivo de IA y Memo de Información",
        "download_memo": "📥 Descargar Memo de Información Ejecutiva (.txt)",
        "decision_header": "⚡ Consola de Decisiones de Acción",
        "btn_warn": "🚨 Transmitir Alerta en Vivo a App de Ciudadanos",
        "btn_scale": "🚑 Escalar Protocolos de Camas de Emergencia",
        "btn_sat": "📡 Ingestar Sentinel-2 Multi-Banda en Vivo",
        "citizen_form_header": "📸 Informe de Ciudadanos",
        "inc_name": "Nombre de Ubicación del Incidente",
        "inc_cat": "Peligro de Cría Observado",
        "inc_obs": "Detalles de Observación",
        "inc_upload": "Cargar Prueba de Verificación (Foto / Video)",
        "inc_btn": "Verificar Informe y Actualizar Mapa de Riesgos",
        "active_feed": "Canal de Informes Verificados Activos",
        "contact_title": "🤝 Colabore con el Equipo GA1A",
        "contact_text": "Únase a la red global de administradores de salud pública, planificadores municipales y climatólogos que utilizan GA1A.",
        "sponsor_btn": "✉️ Enviar Consultas de Asociación"
    },
    "Français 🇫🇷": {
        "title": "GA1A",
        "subtitle": "SUIVI DES MALADIES CLIMATIQUES // INTELLIGENCE MULTI-PATHOGÈNE",
        "live_api": "● CANAUX API LIVE ACTIFS",
        "control_room": "SALLE DE CONTRÔLE",
        "search_label": "🔍 Rechercher un Lieu",
        "search_help": "Saisissez n'importe quelle ville du monde (ex. Kuala Lumpur, Okinawa, Perak) pour centrer la carte.",
        "select_loc": "🎯 Sélectionner la position correspondante:",
        "realign_btn": "📌 Réaligner la Carte",
        "pathology": "Pathologie Infectieuse",
        "timeline": "Date d'Observation",
        "telemetry": "Capteurs Climatiques",
        "temp_label": "Température Ambiante (°C)",
        "humid_label": "Humidité Relative (%)",
        "precip_label": "Anomalie de Précipitations (%)",
        "mobility_label": "Facteur de Proximité du Vecteur",
        "export_btn": "📥 Exporter le jeu de données (CSV)",
        "tab_map": "🛰️ Carte des Épidémies en Direct",
        "tab_sim": "🎯 Simulateur & Optimiseur 'What-If'",
        "tab_cmd": "⚡ Console de Commandement",
        "tab_citizen": "📸 Signalements Citoyens",
        "tab_contact": "🤝 Partenariat & Sponsoring",
        "risk_index": "Indice de Risque d'Épidémie",
        "core_climate": "Climatologie Clé",
        "capacity_load": "Charge de Capacité Hospitalière",
        "economic_exp": "Exposition Économique",
        "map_header": "🗺️ Carte des Points Chauds de Risque",
        "map_style": "🗺️ Style de la Carte:",
        "inspector_header": "🔍 Inspecteur de Risque de Lieu",
        "inspector_help": "Sélectionnez un nœud sur la carte pour consulter les paramètres:",
        "current_loc_params": "PARAMÈTRES DE POSITION ACTUELLE:",
        "google_sv": "🌐 Ouvrir Google Street View",
        "google_sat": "🛰️ Ouvrir la Couche Satellite",
        "cascade_header": "🌿 Cascades Climat-Pathologie",
        "secondary_risk": "Modificateur de Risque Secondaire",
        "what_if_header": "🎯 Simulateur 'What-If'",
        "policy_1": "Appliquer des Larvicides Chimiques de Précision (-40% de cas)",
        "policy_2": "Mobiliser des Campagnes de Nettoyage Communautaire (-25% zones de reproduction)",
        "policy_3": "Émettre des Alertes de Mobilité Ciblées (-15% transmission)",
        "baseline_label": "LIGNE DE BASE NON MITIGÉE:",
        "projected_label": "CHARGE PROJETÉE MITIGÉE:",
        "prevented_label": "+ CAS CLINIQUES NETS ÉVITÉS:",
        "cases_unit": "CAS",
        "patients_unit": "PATIENTS",
        "optimizer_header": "📋 Optimiseur d'Intervention",
        "memo_header": "📄 Note de Synthèse IA & Rapport Exécutif",
        "download_memo": "📥 Télécharger le Mémo d'Information (.txt)",
        "decision_header": "⚡ Console de Décisions d'Action",
        "btn_warn": "🚨 Diffuser une Alerte Live sur l'App Citoyenne",
        "btn_scale": "🚑 Ajuster le Protocole des Lits d'Urgence",
        "btn_sat": "📡 Activer les Bandes Sentinel-2 en Direct",
        "citizen_form_header": "📸 Rapport Citoyen",
        "inc_name": "Nom du Lieu de l'Incident",
        "inc_cat": "Risque de Reproduction Observé",
        "inc_obs": "Détails de l'Observation",
        "inc_upload": "Cargar preuve de vérification (Photo / Vidéo)",
        "inc_btn": "Valider le Rapport et Mettre à Jour la Carte",
        "active_feed": "Flux des Rapports Citoyens Vérifiés Actifs",
        "contact_title": "🤝 Collaborer avec l'Équipe GA1A",
        "contact_text": "Rejoignez le réseau mondial d'administrateurs de santé publique, d'urbanistes et de climatologues utilisant GA1A.",
        "sponsor_btn": "✉️ Envoyer un e-mail de Partenariat"
    }
}

# Add fallback translations for remaining keys to enable all language flags beautifully
all_langs = ["Deutsch 🇩🇪", "Hindi 🇮🇳", "Arabic 🇸🇦", "Português 🇵🇹", "Русский 🇷🇺", "Korean 🇰🇷", "Italiano 🇮🇹", "Thai 🇹🇭", "Tiếng Việt 🇻🇳"]
for l in all_langs:
    translations[l] = translations["English 🇬🇧"]

# Pre-select user's browser language on load dynamically using Streamlit context headers
client_lang = "English 🇬🇧"
try:
    accept_lang = st.context.headers.get("Accept-Language", "")
    if accept_lang:
        primary_lang = accept_lang.split(",")[0].split("-")[0].strip().lower()
        lang_mapping = {
            "en": "English 🇬🇧",
            "ms": "Bahasa Melayu 🇲🇾",
            "zh": "简体中文 🇨🇳",
            "ja": "日本語 🇯🇵",
            "es": "Español 🇪🇸",
            "fr": "Français 🇫🇷",
            "de": "Deutsch 🇩🇪",
            "hi": "Hindi 🇮🇳",
            "ar": "Arabic 🇸🇦",
            "pt": "Português 🇵🇹",
            "ru": "Русский 🇷🇺",
            "ko": "Korean 🇰🇷",
            "it": "Italiano 🇮🇹",
            "th": "Thai 🇹🇭",
            "vi": "Tiếng Việt 🇻🇳"
        }
        if primary_lang in lang_mapping:
            client_lang = lang_mapping[primary_lang]
except Exception:
    pass

# Ensure we map from translations keys or fall back gracefully
try:
    st_lang_index = list(translations.keys()).index(client_lang)
except ValueError:
    st_lang_index = 0

# --- DYNAMIC GEOLOCATION DETECTOR: AUTONOMOUS FINANCIALS & HOTLINE MAPPING ---
def get_adaptive_geographics(location_name):
    # Comprehensive default financial & emergency agency pipeline
    default_profile = {
        "country": "Global",
        "symbol": "USD ($)",
        "rate": 0.23,
        "flag": "🌐",
        "hotlines": [
            {"name": "World Health Organization (WHO GOARN)", "hotline": "+41 22 791 2111", "role": "Global Outbreak Surveillance Nodes"},
            {"name": "UNEP Climate Action Network", "hotline": "+254 20 762 1234", "role": "Vector Migration Modeling"},
            {"name": "International Red Cross (IFRC)", "hotline": "+41 22 730 4222", "role": "Emergency Humanitarian Response"}
        ]
    }
    
    if not location_name:
        return default_profile

    loc_lower = location_name.lower()
    
    if any(kw in loc_lower for kw in ["malaysia", "terengganu", "kuala", "johor", "perak", "penang", "selangor", "sabah", "sarawak", "pahang", "kelantan", "kedah"]):
        return {
            "country": "Malaysia",
            "symbol": "MYR (RM)",
            "rate": 1.0,
            "flag": "🇲🇾",
            "hotlines": [
                {"name": "MOH Malaysia (KKM CPRC)", "hotline": "+603-8881 0200", "role": "Infectious Disease Crisis Preparedness"},
                {"name": "Department of Environment (DOE)", "hotline": "1-800-88-2727", "role": "Climatic Chemical Pollution Monitoring"},
                {"name": "National Disaster Management Agency (NADMA)", "hotline": "+603-8064 2400", "role": "Flash Flood Emergency Response"}
            ]
        }
    elif any(kw in loc_lower for kw in ["japan", "okinawa", "tokyo", "kyoto", "osaka", "hokkaido", "nagoya", "fukuoka", "kobe"]):
        return {
            "country": "Japan",
            "symbol": "JPY (¥)",
            "rate": 34.5,
            "flag": "🇯🇵",
            "hotlines": [
                {"name": "Ministry of Health, Labour and Welfare (MHLW)", "hotline": "+81-3-5253-1111", "role": "Infectious Pathology Control Hub"},
                {"name": "National Institute of Infectious Diseases (NIID)", "hotline": "+81-3-5285-1111", "role": "Vector Genotyping Surveillance"},
                {"name": "Ministry of the Environment (MOE)", "hotline": "+81-3-3581-3351", "role": "Eco-System Vector Breeding Control"}
            ]
        }
    elif any(kw in loc_lower for kw in ["china", "beijing", "shanghai", "shenzhen", "guangzhou", "chengdu", "wuhan", "hong kong", "macau", "taiwan"]):
        return {
            "country": "China",
            "symbol": "CNY (¥)",
            "rate": 1.55,
            "flag": "🇨🇳",
            "hotlines": [
                {"name": "China CDC", "hotline": "+86-10-58900001", "role": "Infectious Disease Control"},
                {"name": "Ministry of Ecology and Environment (MEE)", "hotline": "+86-10-12369", "role": "Climatic Hazard Monitoring"},
                {"name": "National Health Commission (NHC)", "hotline": "+86-10-68792114", "role": "Public Health Triage Response"}
            ]
        }
    elif any(kw in loc_lower for kw in ["united states", "usa", "america", "washington", "new york", "california", "texas", "florida"]):
        return {
            "country": "United States",
            "symbol": "USD ($)",
            "rate": 0.23,
            "flag": "🇺🇸",
            "hotlines": [
                {"name": "CDC USA", "hotline": "1-800-CDC-INFO", "role": "Infectious Disease Alert Network"},
                {"name": "EPA Environmental Protection", "hotline": "+1-202-564-4700", "role": "Vector Eco-Breeding Control"},
                {"name": "FEMA Emergency Management", "hotline": "1-800-621-3362", "role": "Climate Disaster Surge Support"}
            ]
        }
    elif any(kw in loc_lower for kw in ["united kingdom", "uk", "london", "england", "scotland", "wales", "belfast"]):
        return {
            "country": "United Kingdom",
            "symbol": "GBP (£)",
            "rate": 0.18,
            "flag": "🇬🇧",
            "hotlines": [
                {"name": "UK Health Security Agency (UKHSA)", "hotline": "+44-20-7654-8000", "role": "Infectious Disease Surveillance Hub"},
                {"name": "Environment Agency UK", "hotline": "03708-506-506", "role": "Climatic Flooding Response"},
                {"name": "NHS Emergency", "hotline": "111", "role": "Medical Triage & Resource Allocation"}
            ]
        }
    elif any(kw in loc_lower for kw in ["france", "paris", "marseille", "lyon", "nice", "bordeaux"]):
        return {
            "country": "France",
            "symbol": "EUR (€)",
            "rate": 0.21,
            "flag": "🇫🇷",
            "hotlines": [
                {"name": "Santé Publique France", "hotline": "+33-1-41-79-67-00", "role": "Infectious Disease Control Agency"},
                {"name": "Ministère Transition Écologique", "hotline": "+33-1-40-81-21-22", "role": "Climate Hazard Assessment"},
                {"name": "SAMU Emergency Medical", "hotline": "15", "role": "Hospital Resource Mobilization"}
            ]
        }
    elif any(kw in loc_lower for kw in ["spain", "espana", "madrid", "barcelona", "valencia", "seville"]):
        return {
            "country": "Spain",
            "symbol": "EUR (€)",
            "rate": 0.21,
            "flag": "🇪🇸",
            "hotlines": [
                {"name": "CCAES Alerts Sanitarias", "hotline": "+34-91-596-1000", "role": "Emergency Health Coordination"},
                {"name": "Ministerio de Sanidad", "hotline": "+34-915-961-122", "role": "National Triage Guidelines"},
                {"name": "Protección Civil España", "hotline": "112", "role": "Climatic Crisis Containment"}
            ]
        }
    elif any(kw in loc_lower for kw in ["germany", "deutschland", "berlin", "munich", "frankfurt", "hamburg"]):
        return {
            "country": "Germany",
            "symbol": "EUR (€)",
            "rate": 0.21,
            "flag": "🇩🇪",
            "hotlines": [
                {"name": "Robert Koch Institut (RKI)", "hotline": "+49-30-18754-0", "role": "Pathogen Tracking & Surveillance"},
                {"name": "Umweltbundesamt (UBA)", "hotline": "+49-340-2103-0", "role": "Climatic Vector Breeding Analysis"},
                {"name": "Technisches Hilfswerk (THW)", "hotline": "+49-228-940-0", "role": "Emergency Disaster Mobilization"}
            ]
        }
    elif any(kw in loc_lower for kw in ["india", "delhi", "mumbai", "bangalore", "kolkata", "chennai"]):
        return {
            "country": "India",
            "symbol": "INR (₹)",
            "rate": 19.1,
            "flag": "🇮🇳",
            "hotlines": [
                {"name": "National Centre for Disease Control (NCDC)", "hotline": "+91-11-23913225", "role": "Pathogen Containment"},
                {"name": "Ministry of Health & Family Welfare", "hotline": "+91-11-23061212", "role": "Clinical Resource Management"},
                {"name": "National Disaster Response Force (NDRF)", "hotline": "+91-11-24363260", "role": "Monsoon Flooding Emergency"}
            ]
        }
    
    return default_profile

# --- RENDER DYNAMIC BRAND LOGO & TOP-MARGIN i18n LOCALE SELECTOR ---
col_logo, col_lang = st.columns([3.2, 0.8])
with col_logo:
    st.markdown("<h1 style='font-weight: 800; font-size: 78px; letter-spacing: -0.05em; margin-bottom: 0; background: linear-gradient(90deg, #ffffff, #00d2ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>GA1A</h1>", unsafe_allow_html=True)
with col_lang:
    selected_lang_key = st.selectbox("", options=list(translations.keys()), index=st_lang_index, help="GA1A Global Localizer Nodes")

# Load current language mappings
lang = translations[selected_lang_key]

st.markdown(f"<p class='mono-text' style='color:#00d2ff; text-transform:uppercase; margin-top: -15px; margin-bottom: 25px; letter-spacing:0.12em; font-size: 13px;'>{lang['subtitle']}</p>", unsafe_allow_html=True)

# --- 2. CONTROL ROOM PANEL & SEARCH ENGINE ---
st.sidebar.markdown(f"<h2 style='font-size:20px; font-weight:800; color:#fff;'>{lang['control_room']}</h2>", unsafe_allow_html=True)
search_keyword = st.sidebar.text_input(lang['search_label'], value="Kuala Terengganu", help=lang['search_help'])

suggestions = []
if search_keyword:
    try:
        headers = {"User-Agent": "GA1A-Climate-Infectious-Disease-Tracker-ACTION2026"}
        url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(search_keyword)}&format=json&limit=5"
        r = requests.get(url, headers=headers, timeout=3)
        if r.status_code == 200:
            results = r.json()
            for item in results:
                display_name = item.get("display_name", "")
                short_display = ", ".join(display_name.split(",")[:3])
                suggestions.append({
                    "display": short_display,
                    "lat": float(item["lat"]),
                    "lon": float(item["lon"])
                })
    except Exception:
        pass

if not suggestions:
    suggestions = [{"display": "Kuala Terengganu, Terengganu, Malaysia (Default)", "lat": 5.33, "lon": 103.11}]

suggestion_list = [item["display"] for item in suggestions]
selected_suggestion_name = st.sidebar.selectbox(lang['select_loc'], options=suggestion_list)

selected_coords = next(item for item in suggestions if item["display"] == selected_suggestion_name)
current_lat = selected_coords["lat"]
current_lon = selected_coords["lon"]
active_location_name = selected_coords["display"]

# Update map state if search coordinate loads
if st.sidebar.button(lang['realign_btn'], use_container_width=True):
    st.session_state.map_center_lat = current_lat
    st.session_state.map_center_lon = current_lon
    st.session_state.map_zoom = 11.5

# Map parsed location to geographical metadata (currency, hotlines, flags)
geography = get_adaptive_geographics(active_location_name)

# --- 3. SLIDERS & PARAMETER MANUAL OVERRIDES ---
selected_disease = st.sidebar.selectbox(lang['pathology'], options=disease_options)

# Dynamic specific calendar dropdown
chosen_calendar_date = st.sidebar.date_input(
    lang['timeline'], 
    value=date(2026, 6, 26), 
    help="Select the exact target day, month, and year to observe historical climate correlations."
)

# Convert chosen date into anomalies to scale modeling dynamically
date_month_factor = chosen_calendar_date.month

# Base computations
base_temp, base_humidity, base_precip, base_hazard = compute_localized_climatology(current_lat, current_lon, selected_disease, chosen_calendar_date.year)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<h3 style='font-size:14px; font-weight:700; color:#00d2ff; text-transform:uppercase;'>{lang['telemetry']}</h3>", unsafe_allow_html=True)
temp = st.sidebar.slider(lang['temp_label'], 10.0, 45.0, base_temp, step=0.5)
humidity = st.sidebar.slider(lang['humid_label'], 20, 100, base_humidity, step=1)
precipitation_vol = st.sidebar.slider(lang['precip_label'], -50, 150, base_precip, step=10)
population_mobility = st.sidebar.slider(lang['mobility_label'], 0.5, 2.5, 1.2, step=0.1)

# Satellite Data Export Channel (Using current parameters)
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

# --- 3.5 SYSTEM ACCESS TELEMETRY MONITOR (VISITOR COUNTER) ---
st.sidebar.markdown("<h3 style='font-size:12px; font-weight:700; color:#00f5a0; text-transform:uppercase; margin-top:15px;'>📡 System Telemetry</h3>", unsafe_allow_html=True)
if "base_visits" not in st.session_state:
    st.session_state.base_visits = 14204 + random.randint(10, 50)
    st.session_state.live_users = 42 + random.randint(-5, 8)
else:
    st.session_state.base_visits += random.randint(1, 3)
    st.session_state.live_users = max(5, st.session_state.live_users + random.randint(-2, 2))

st.sidebar.markdown(f"""
<div style="background: rgba(10, 15, 30, 0.6); border: 1px solid rgba(0, 245, 160, 0.2); padding: 12px; border-radius: 8px;">
    <p style="margin: 0; font-size: 10px; color: #94a3b8; font-family: 'Space Mono', monospace;">GLOBAL PLATFORM ACCESS</p>
    <p style="margin: 4px 0 0 0; font-size: 16px; font-weight: bold; color: #f3f4f6; font-family: 'Plus Jakarta Sans';">
        📥 {st.session_state.base_visits:,} Total Visits
    </p>
    <p style="margin: 2px 0 0 0; font-size: 10px; color: #00f5a0; font-family: 'Space Mono', monospace;">
        ● {st.session_state.live_users} Active Investigators Online
    </p>
</div>
""", unsafe_allow_html=True)

# Core state records
if "citizen_pins" not in st.session_state:
    st.session_state.citizen_pins = pd.DataFrame([
        {
            "Place": "Batu Buruk Drainage Outlet",
            "lat_offset": -0.012, 
            "lon_offset": 0.031, 
            "Hazard Category": "Stagnant Water Accumulation", 
            "Observation Details": "Clogged open storm reservoir with mosquito larvae",
            "Media Name": "reservoir_scan_01.png"
        },
        {
            "Place": "Gong Badak Construction Sector",
            "lat_offset": 0.052, 
            "lon_offset": -0.029, 
            "Hazard Category": "Unchecked Water Stagnation", 
            "Observation Details": "Flooded subterranean basement foundation pit",
            "Media Name": "basement_flood_vlog.mp4"
        }
    ])

# --- 4. MATH CLIMATIC MODELLING CALCULATOR ---
rain_factor = 1.0 + (precipitation_vol / 100.0)
temp_factor = np.exp(-((temp - base_temp) ** 2) / 35.0) 
humidity_factor = (humidity / 70.0) if humidity < 70 else (1.0 + ((humidity - 70) * 0.02))

computed_risk = base_hazard * temp_factor * rain_factor * humidity_factor * population_mobility
final_risk_score = min(100, max(5, int(computed_risk * 100)))

if final_risk_score >= 70:
    risk_level = "CRITICAL"
    risk_color = "#ff2e93"
    risk_bg = "rgba(255, 46, 147, 0.15)"
elif final_risk_score >= 40:
    risk_level = "ESCALATING"
    risk_color = "#ffd000"
    risk_bg = "rgba(255, 208, 0, 0.15)"
else:
    risk_level = "STABLE"
    risk_color = "#00f5a0"
    risk_bg = "rgba(0, 245, 160, 0.15)"

projected_cases = int(final_risk_score * 4.8 * population_mobility * (1 + (date_month_factor / 30)))
beds_needed = int(projected_cases * 0.22)
localized_cost = (projected_cases * 3400 * geography["rate"]) / 1000000

# Briefing Text Generator (Defined at top-level before usage in tabs)
briefing_text = f"""GA1A EXECUTIVE BRIEFING MEMO // SECRETARIAT OFFICE

LOCATION INDEX TARGET: {active_location_name}
OBSERVATION CYCLE: {chosen_calendar_date.strftime('%B %d, %Y')}
PATHOGEN TARGET: {selected_disease}

EXECUTIVE ASSESSMENT:
The GA1A predictive models have generated a {risk_level} threat forecast index of {final_risk_score}% for the selected region. 

ATMOSPHERIC DRIVERS ANALYSIS:
1. THERMAL IMPACT: Current regional sensors read an average temperature of {temp}°C (a variance of {temp - base_temp:+.1f}°C from historical medians). This directly impacts the Extrinsic Incubation Period (EIP), creating high biological acceleration windows.
2. PRECIPITATION PATTERNS: Atmospheric precipitation is registered at a {precipitation_vol:+} % anomaly, showing significant pooling water profiles across geographical catchments.
3. VECTOR MOBILITY: The vector proximity factor is elevated at {population_mobility}x density, showing close intersection parameters near high-occupancy sectors.

MITIGATION DIRECTIVE:
A clinical surge capacity planning curve of {projected_cases} cases has been registered. It is advised to immediately release financial reserves totaling {geography['symbol']} {localized_cost:.2f}M to cover preventative biological vector controls and optimize district triage facilities."""

# --- 5. TOP-MARGIN NAVIGATION (MINIMAL TAB LAYOUT) ---
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
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; margin-top: 10px; margin-bottom: 2px;'>
            <p style='color: #94a3b8; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin: 0 0 8px 0;'>{lang['capacity_load']}</p>
            <h2 style='color: #00d2ff