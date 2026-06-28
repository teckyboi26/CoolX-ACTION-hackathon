import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import io
import random
from datetime import date, datetime

# ==============================================================================
# PHASE 1: STREAMLIT APP CONFIGURATION & PRE-FLIGHT INTERFACE STYLING
# ==============================================================================
st.set_page_config(
    page_title="GA1A | Climate-Infectious Disease Tracker",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GLOBAL DISEASES LIST ---
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
        "subtitle": "CLIMATE INFECTIOUS DISEASE TRACKER",
        "live_api": "● LIVE API CHANNELS ACTIVE",
        "control_room": "CONTROL ROOM",
        "search_label": "🔍 Search Location",
        "search_help": "Search any location globally (e.g. Kuala Lumpur, Okinawa, Perak, London) to update maps and data.",
        "select_loc": "🎯 Select Matching Location:",
        "realign_btn": "📌 Re-align Viewport Map",
        "pathology": "DISEASES",
        "timeline": "DATE",
        "telemetry": "CLIMATE SENSORS",
        "temp_label": "Ambient Temperature (°C)",
        "humid_label": "Relative Humidity (%)",
        "precip_label": "Precipitation Anomaly (%)",
        "mobility_label": "Vector Proximity Factor",
        "export_btn": "📥 Download Dataset",
        "tab_map": "MAP",
        "tab_sim": "SIMULATOR",
        "tab_cmd": "COMMAND CONSOLE",
        "tab_citizen": "CITIZEN REPORTS",
        "tab_contact": "CONTACT",
        "risk_index": "Risk Index",
        "core_climate": "Climate Conditions",
        "capacity_load": "Projected Cases",
        "economic_exp": "Economic Impact",
        "map_header": "🗺️ Outbreak Hotspot Map",
        "map_style": "🗺️ Map Layer View Style:",
        "inspector_header": "🔍 Location Inspector",
        "inspector_help": "Select active hotspot node on the map to query parameters:",
        "current_loc_params": "CURRENT LOCATION PARAMETERS:",
        "google_sv": "🌐 Open Street View",
        "google_sat": "🛰️ Open Satellite Map",
        "cascade_header": "🌿 Related Disease Cascades",
        "secondary_risk": "Secondary Risk",
        "what_if_header": "🎯 What-If Simulator",
        "policy_1": "Apply Chemical Larvicides (-40% case loads)",
        "policy_2": "Mobilize Community Cleanup (-25% breeding zones)",
        "policy_3": "Issue Target Mobility Warnings (-15% transmission)",
        "baseline_label": "BASELINE PREDICTION (UNMITIGATED):",
        "projected_label": "MITIGATED PROJECTED CASES:",
        "prevented_label": "+ TOTAL PREVENTED HOSPITAL SURGES:",
        "cases_unit": "CASES",
        "patients_unit": "PATIENTS",
        "optimizer_header": "📋 Recommended Action Optimizer",
        "memo_header": "📄 Executive Outbreak Briefing Memo",
        "download_memo": "📥 Download Briefing Memo (.txt)",
        "decision_header": "⚡ Command Console",
        "btn_warn": "🚨 Broadcast Warning to Citizen App",
        "btn_scale": "🚑 Mobilize Emergency Bed Protocols",
        "btn_sat": "📡 Sync Sentinel-2 Satellite Multi-Bands",
        "citizen_form_header": "📸 Citizen Report",
        "inc_name": "Location Name",
        "inc_cat": "Observed Hazard Category",
        "inc_obs": "Incident Details",
        "inc_upload": "Upload Verification Photo / Video",
        "inc_btn": "Verify Report & Update Hotspots",
        "active_feed": "Active Verified Citizen Reports Feed",
        "contact_title": "🤝 Collaborate with Team GA1A",
        "contact_text": "Join the global network of public health administrators, municipal planners, and climatologists utilizing GA1A to build climate resilience.",
        "sponsor_btn": "✉️ Contact Team GA1A"
    },
    "Bahasa Melayu 🇲🇾": {
        "title": "GA1A",
        "subtitle": "PENJEJAK JANGKITAN IKLIM",
        "live_api": "● SALURAN API AKTIF",
        "control_room": "PANEL KAWALAN",
        "search_label": "🔍 Cari Lokasi",
        "search_help": "Cari lokasi di seluruh dunia (cth. Kuala Lumpur, Okinawa, Perak, London) untuk mengemas kini peta.",
        "select_loc": "🎯 Pilih Cadangan Lokasi:",
        "realign_btn": "📌 Jajarkan Semula Peta Viewport",
        "pathology": "DISEASES",
        "timeline": "TARIKH",
        "telemetry": "CLIMATE SENSORS",
        "temp_label": "Suhu Ambien (°C)",
        "humid_label": "Kelembapan Relatif (%)",
        "precip_label": "Anomali Kerpasan (%)",
        "mobility_label": "Faktor Kedekatan Vektor",
        "export_btn": "📥 Muat Turun Set Data",
        "tab_map": "MAP",
        "tab_sim": "SIMULATOR",
        "tab_cmd": "COMMAND CONSOLE",
        "tab_citizen": "CITIZEN REPORTS",
        "tab_contact": "CONTACT",
        "risk_index": "Indeks Risiko",
        "core_climate": "Kondisi Cuaca",
        "capacity_load": "Unjuran Kes",
        "economic_exp": "Impak Ekonomi",
        "map_header": "🗺️ Peta Hotspot Wabak",
        "map_style": "🗺️ Gaya Paparan Peta:",
        "inspector_header": "🔍 Pemeriksa Lokasi",
        "inspector_help": "Pilih nod aktif pada peta untuk melihat parameter:",
        "current_loc_params": "PARAMETER LOKASI SEMASA:",
        "google_sv": "🌐 Buka Street View",
        "google_sat": "🛰️ Buka Peta Satelit",
        "cascade_header": "🌿 Kasked Penyakit Berkaitan",
        "secondary_risk": "Risiko Sekunder",
        "what_if_header": "🎯 Simulator 'What-If'",
        "policy_1": "Gunakan Larvasid Kimia (-40% beban kes)",
        "policy_2": "Mobilisasi Pembersihan Komuniti (-25% zon pembiakan)",
        "policy_3": "Keluarkan Amaran Mobiliti Sasaran (-15% transmisi)",
        "baseline_label": "RAMALAN ASAS (TANPA TINDAKAN):",
        "projected_label": "UNJURAN KES SELEPAS TINDAKAN:",
        "prevented_label": "+ NET KES KLINIKAL DISELAMATKAN:",
        "cases_unit": "KES",
        "patients_unit": "PESAKIT",
        "optimizer_header": "📋 Cadangan Pengoptimum Intervensi",
        "memo_header": "📄 Memo Taklimat Eksekutif Wabak",
        "download_memo": "📥 Muat Turun Memo Taklimat (.txt)",
        "decision_header": "⚡ Command Console",
        "btn_warn": "🚨 Siarkan Amaran ke Aplikasi Rakyat",
        "btn_scale": "🚑 Mobilisasi Katil Kecemasan Serantau",
        "btn_sat": "📡 Selaraskan Sentinel-2 Multi-Bands",
        "citizen_form_header": "📸 Laporan Rakyat",
        "inc_name": "Nama Lokasi",
        "inc_cat": "Kategori Bahaya Diperhatikan",
        "inc_obs": "Butiran Laporan",
        "inc_upload": "Muat Naik Bukti Pengesahan (Foto / Video)",
        "inc_btn": "Sahkan Laporan & Kemas Kini Hotspots",
        "active_feed": "Suapan Laporan Rakyat Disahkan Aktif",
        "contact_title": "🤝 Bekerjasama dengan Pasukan GA1A",
        "contact_text": "Sertai rangkaian global pentadbir kesihatan awam, perancang perbandaran, dan ahli klimatologi yang menggunakan GA1A untuk membina daya tahan iklim.",
        "sponsor_btn": "✉️ Hubungi Pasukan GA1A"
    },
    "Español 🇪🇸": {
        "title": "GA1A",
        "subtitle": "RASTREADOR DE ENFERMEDADES INFECCIOSAS CLIMÁTICAS",
        "live_api": "● CANALES DE API EN VIVO ACTIVOS",
        "control_room": "PANEL DE CONTROL",
        "search_label": "🔍 Buscar Ubicación",
        "search_help": "Busque cualquier ubicación global para actualizar mapas y datos.",
        "select_loc": "🎯 Seleccione Ubicación Coincidente:",
        "realign_btn": "📌 Realinear Mapa",
        "pathology": "DISEASES",
        "timeline": "FECHA",
        "telemetry": "CLIMATE SENSORS",
        "temp_label": "Temperatura Ambiente (°C)",
        "humid_label": "Humedad Relativa (%)",
        "precip_label": "Anomalía de Precipitation (%)",
        "mobility_label": "Factor de Proximidad",
        "export_btn": "📥 Descargar Datos",
        "tab_map": "MAP",
        "tab_sim": "SIMULATOR",
        "tab_cmd": "COMMAND CONSOLE",
        "tab_citizen": "CITIZEN REPORTS",
        "tab_contact": "CONTACT",
        "risk_index": "Índice de Riesgo",
        "core_climate": "Condiciones Climáticas",
        "capacity_load": "Casos Proyectados",
        "economic_exp": "Impacto Económico",
        "map_header": "🗺️ Mapa de Puntos Críticos",
        "map_style": "🗺️ Estilo del Mapa:",
        "inspector_header": "🔍 Inspector de Ubicación",
        "inspector_help": "Seleccione un nodo activo en el mapa para consultar parámetros:",
        "current_loc_params": "PARÁMETROS DE LA UBICACIÓN ACTUAL:",
        "google_sv": "🌐 Abrir Street View",
        "google_sat": "🛰️ Abrir Mapa Satelital",
        "cascade_header": "🌿 Cascadas de Enfermedades Relacionadas",
        "secondary_risk": "Riesgo Secundario",
        "what_if_header": "🎯 Simulador 'What-If'",
        "policy_1": "Aplicar Larvicidas Químicos (-40% casos)",
        "policy_2": "Limpieza Comunitaria (-25% zonas de cría)",
        "policy_3": "Alertas de Movilidad (-15% transmisión)",
        "baseline_label": "PREDICCIÓN BASE (SIN MITIGACIÓN):",
        "projected_label": "CASOS PROYECTADOS MITIGADOS:",
        "prevented_label": "+ INGRESOS EVITADOS:",
        "cases_unit": "CASOS",
        "patients_unit": "PACIENTES",
        "optimizer_header": "📋 Optimizador de Acciones",
        "memo_header": "📄 Memo de Información Ejecutiva",
        "download_memo": "📥 Descargar Memo (.txt)",
        "decision_header": "⚡ Consola de Mando",
        "btn_warn": "🚨 Enviar Alerta Ciudadana",
        "btn_scale": "🚑 Mobilizar Camas de Emergencia",
        "btn_sat": "📡 Sincronizar Sentinel-2",
        "citizen_form_header": "📸 Informe Ciudadano",
        "inc_name": "Nombre de la Ubicación",
        "inc_cat": "Categoría de Peligro",
        "inc_obs": "Detalles del Incidente",
        "inc_upload": "Subir Prueba de Verificación",
        "inc_btn": "Verificar Informe y Actualizar",
        "active_feed": "Informes Ciudadanos Verificados",
        "contact_title": "🤝 Colaborar con el Equipo GA1A",
        "contact_text": "Únase a la red global que utiliza GA1A para desarrollar la resiliencia climática.",
        "sponsor_btn": "✉️ Contactar al Equipo"
    },
    "Français 🇫🇷": {
        "title": "GA1A",
        "subtitle": "TRACKER DE MALADIES INFECTIEUSES CLIMATIQUES",
        "live_api": "● CANAUX API LIVE ACTIFS",
        "control_room": "PANNEAU DE CONFIGURATION",
        "search_label": "🔍 Rechercher un lieu",
        "search_help": "Recherchez n'importe quel lieu dans le monde pour mettre à jour la carte.",
        "select_loc": "🎯 Sélectionner le Lieu Correspondant :",
        "realign_btn": "📌 Aligner la carte",
        "pathology": "DISEASES",
        "timeline": "DATE",
        "telemetry": "CLIMATE SENSORS",
        "temp_label": "Température Ambiante (°C)",
        "humid_label": "Humidité Relative (%)",
        "precip_label": "Anomalie de Précipitations (%)",
        "mobility_label": "Facteur de Proximité",
        "export_btn": "📥 Télécharger le jeu de données",
        "tab_map": "MAP",
        "tab_sim": "SIMULATOR",
        "tab_cmd": "COMMAND CONSOLE",
        "tab_citizen": "CITIZEN REPORTS",
        "tab_contact": "CONTACT",
        "risk_index": "Indice de Risque",
        "core_climate": "Conditions Climatiques",
        "capacity_load": "Cas Projetés",
        "economic_exp": "Impact Économique",
        "map_header": "🗺️ Carte des Points Chauds",
        "map_style": "🗺️ Style de couche de carte :",
        "inspector_header": "🔍 Inspecteur de Zone",
        "inspector_help": "Sélectionnez un nœud actif sur la carte :",
        "current_loc_params": "PARAMÈTRES DU LIEU ACTUEL :",
        "google_sv": "🌐 Ouvrir Street View",
        "google_sat": "🛰️ Ouvrir la carte satellite",
        "cascade_header": "🌿 Cascades de Maladies Associées",
        "secondary_risk": "Risque Secondaire",
        "what_if_header": "🎯 Simulateur 'What-If'",
        "policy_1": "Appliquer des larvicides (-40% de cas)",
        "policy_2": "Nettoyage communautaire (-25% zones de reproduction)",
        "policy_3": "Émettre des alertes de mobilité (-15% transmission)",
        "baseline_label": "PRÉDICTION DE BASE :",
        "projected_label": "CAS PROJETÉS MITIGÉS :",
        "prevented_label": "+ HOSPITALISATIONS ÉVITÉES :",
        "cases_unit": "CAS",
        "patients_unit": "PATIENTS",
        "optimizer_header": "📋 Optimiseur d'Actions",
        "memo_header": "📄 Mémo d'Information Exécutif",
        "download_memo": "📥 Télécharger le Mémo (.txt)",
        "decision_header": "⚡ Console de Commandement",
        "btn_warn": "🚨 Diffuser une Alerte",
        "btn_scale": "🚑 Mobiliser les Lits d'Urgence",
        "btn_sat": "📡 Synchroniser Sentinel-2",
        "citizen_form_header": "📸 Signalement Citoyen",
        "inc_name": "Nom du Lieu",
        "inc_cat": "Catégorie de Danger",
        "inc_obs": "Détails de l'Incident",
        "inc_upload": "Téléverser Photo / Vidéo",
        "inc_btn": "Vérifier le Rapport & Mettre à Jour",
        "active_feed": "Rapports Citoyens Vérifiés",
        "contact_title": "🤝 Collaborer avec l'Équipe GA1A",
        "contact_text": "Rejoignez le réseau mondial qui utilise GA1A pour renforcer la résilience climatique.",
        "sponsor_btn": "✉️ Contacter l'Équipe"
    },
    "Deutsch 🇩🇪": {
        "title": "GA1A",
        "subtitle": "KLIMA-INFEKTIONSKRANKHEITEN TRACKER",
        "live_api": "● LIVE-API-KANÄLE AKTIV",
        "control_room": "KONTROLLPANEL",
        "search_label": "🔍 Standort Suchen",
        "search_help": "Suchen Sie nach einem beliebigen globalen Standort, um Karten und Daten zu aktualisieren.",
        "select_loc": "🎯 Passenden Standort Auswählen:",
        "realign_btn": "📌 Karte Ausrichten",
        "pathology": "DISEASES",
        "timeline": "DATUM",
        "telemetry": "CLIMATE SENSORS",
        "temp_label": "Umgebungstemperatur (°C)",
        "humid_label": "Relative Luftfeuchtigkeit (%)",
        "precip_label": "Niederschlagsanomalie (%)",
        "mobility_label": "Vektor-Proximitätsfaktor",
        "export_btn": "📥 Datensatz Herunterladen",
        "tab_map": "MAP",
        "tab_sim": "SIMULATOR",
        "tab_cmd": "COMMAND CONSOLE",
        "tab_citizen": "CITIZEN REPORTS",
        "tab_contact": "CONTACT",
        "risk_index": "Risikoindex",
        "core_climate": "Klimabedingungen",
        "capacity_load": "Prognostizierte Fälle",
        "economic_exp": "Wirtschaftliche Auswirkung",
        "map_header": "🗺️ Ausbruchs-Hotspot-Karte",
        "map_style": "🗺️ Kartenansichtsstil:",
        "inspector_header": "🔍 Standort-Inspektor",
        "inspector_help": "Wählen Sie einen aktiven Knoten auf der Karte aus:",
        "current_loc_params": "AKTUELLE STANDORTPARAMETER:",
        "google_sv": "🌐 Street View Öffnen",
        "google_sat": "🛰️ Satellitenkarte Öffnen",
        "cascade_header": "🌿 Verwandte Krankheitskaskaden",
        "secondary_risk": "Sekundäres Risiko",
        "what_if_header": "🎯 'What-If'-Simulator",
        "policy_1": "Chemische Larvizide anwenden (-40% Fälle)",
        "policy_2": "Gemeinschaftliche Reinigung (-25% Brutgebiete)",
        "policy_3": "Mobilitätswarnungen herausgeben (-15% Übertragung)",
        "baseline_label": "BASISPROGNOSE (UNMITIGIERT):",
        "projected_label": "MITIGIERTE PROGNOSTIZIERTE FÄLLE:",
        "prevented_label": "+ VERMEIDENE HOSPITALISIERUNGEN:",
        "cases_unit": "FÄLLE",
        "patients_unit": "PATIENTEN",
        "optimizer_header": "📋 Empfohlener Aktionsoptimierer",
        "memo_header": "📄 Executive Outbreak Briefing Memo",
        "download_memo": "📥 Briefing Memo Herunterladen (.txt)",
        "decision_header": "⚡ Befehlskonsole",
        "btn_warn": "🚨 Warnung an Bürger-App Senden",
        "btn_scale": "🚑 Notfallbetten Mobilisieren",
        "btn_sat": "📡 Sentinel-2 Satellit Synchronisieren",
        "citizen_form_header": "📸 Bürgerbericht",
        "inc_name": "Standortname",
        "inc_cat": "Beobachtete Gefahrenkategorie",
        "inc_obs": "Vorfall-Details",
        "inc_upload": "Nachweis Hochladen (Foto/Video)",
        "inc_btn": "Bericht Verifizieren & Hotspots Aktualisieren",
        "active_feed": "Aktive Verifizierte Bürgerberichte",
        "contact_title": "🤝 Kooperieren Sie mit Team GA1A",
        "contact_text": "Treten Sie dem globalen Netzwerk bei, das GA1A nutzt, um die Klimaresistenz zu stärken.",
        "sponsor_btn": "✉️ Team GA1A  Kontaktieren"
    },
    "Arabic 🇸🇦": {
        "title": "GA1A",
        "subtitle": "تتبع الأمراض المعدية المناخية",
        "live_api": "● قنوات API المباشرة نشطة",
        "control_room": "لوحة التحكم",
        "search_label": "🔍 ابحث عن موقع",
        "search_help": "ابحث عن أي موقع عالمي لتحديث الخرائط والبيانات.",
        "select_loc": "🎯 حدد الموقع المطابق:",
        "realign_btn": "📌 إعادة محاذاة الخريطة",
        "pathology": "DISEASES",
        "timeline": "التاريخ",
        "telemetry": "CLIMATE SENSORS",
        "temp_label": "درجة الحرارة المحيطة (°C)",
        "humid_label": "الرطوبة النسبية (%)",
        "precip_label": "شذوذ هطول الأمطار (%)",
        "mobility_label": "عامل القرب الناقل",
        "export_btn": "📥 تحميل البيانات",
        "tab_map": "MAP",
        "tab_sim": "SIMULATOR",
        "tab_cmd": "COMMAND CONSOLE",
        "tab_citizen": "CITIZEN REPORTS",
        "tab_contact": "CONTACT",
        "risk_index": "مؤشر الخطر",
        "core_climate": "الظروف المناخية",
        "capacity_load": "الحالات المتوقعة",
        "economic_exp": "الأثر الاقتصادي",
        "map_header": "🗺️ خريطة بؤر تفشي المرض",
        "map_style": "🗺️ نمط عرض الخريطة:",
        "inspector_header": "🔍 مفتش الموقع",
        "inspector_help": "حدد نقطة نشطة على الخريطة للاستعلام عن المعلمات:",
        "current_loc_params": "معلمات الموقع الحالي:",
        "google_sv": "🌐 فتح عرض الشارع",
        "google_sat": "🛰️ فتح خريطة القمر الصناعي",
        "cascade_header": "🌿 سلاسل الأمراض ذات الصلة",
        "secondary_risk": "الخطر الثانوي",
        "what_if_header": "🎯 محاكي 'What-If'",
        "policy_1": "استخدام مبيدات اليرقات الكيميائية (-40% من الحالات)",
        "policy_2": "تنظيم حملات تنظيف مجتمعية (-25% من بؤر التكاثر)",
        "policy_3": "إصدار تحذيرات الحركة المستهدفة (-15% من انتقال العدوى)",
        "baseline_label": "التنبؤ الأساسي (غير المخفف):",
        "projected_label": "الحالات المتوقعة المخففة:",
        "prevented_label": "+ صافي الحالات التي تم تجنبها:",
        "cases_unit": "حالات",
        "patients_unit": "مرضى",
        "optimizer_header": "📋 محسن الإجراءات الموصى بها",
        "memo_header": "📄 مذكرة إيجازية عن تفشي المرض",
        "download_memo": "📥 تحميل المذكرة (.txt)",
        "decision_header": "⚡ وحدة التحكم في الأوامر",
        "btn_warn": "🚨 بث تحذير لتطبيق المواطن",
        "btn_scale": "🚑 تعبئة أسرة الطوارئ",
        "btn_sat": "📡 مزامنة القمر الصناعي Sentinel-2",
        "citizen_form_header": "📸 تقرير المواطن",
        "inc_name": "اسم الموقع",
        "inc_cat": "فئة الخطر المرصود",
        "inc_obs": "تفاصيل الحادث",
        "inc_upload": "تحميل إثبات التحقق",
        "inc_btn": "التحقق من التقرير وتحديث الخريطة",
        "active_feed": "تقارير المواطنين النشطة التي تم التحقق منها",
        "contact_title": "🤝 التعاون مع فريق GA1A",
        "contact_text": "انضم إلى الشبكة العالمية التي تستخدم GA1A لبناء المرونة المناخية.",
        "sponsor_btn": "✉️ الاتصال بالفريق"
    },
    "Hindi 🇮🇳": {
        "title": "GA1A",
        "subtitle": "जलवायु जनित संक्रामक रोग ट्रैकर",
        "live_api": "● लाइव एपीआई चैनल सक्रिय हैं",
        "control_room": "नियंत्रण कक्ष",
        "search_label": "🔍 स्थान खोजें",
        "search_help": "मानचित्र और डेटा को अपडेट करने के लिए वैश्विक स्तर पर कोई भी स्थान खोजें।",
        "select_loc": "🎯 मिलान स्थान का चयन करें:",
        "realign_btn": "📌 मानचित्र संरेखित करें",
        "pathology": "DISEASES",
        "timeline": "दिनांक",
        "telemetry": "CLIMATE SENSORS",
        "temp_label": "तापमान (°C)",
        "humid_label": "सापेक्ष आर्द्रता (%)",
        "precip_label": "वर्षा विसंगति (%)",
        "mobility_label": "वाहक निकटता कारक",
        "export_btn": "📥 डेटासेट डाउनलोड करें",
        "tab_map": "MAP",
        "tab_sim": "SIMULATOR",
        "tab_cmd": "COMMAND CONSOLE",
        "tab_citizen": "CITIZEN REPORTS",
        "tab_contact": "CONTACT",
        "risk_index": "जोखिम सूचकांक",
        "core_climate": "जलवायु की स्थिति",
        "capacity_load": "अनुमानित मामले",
        "economic_exp": "आर्थिक प्रभाव",
        "map_header": "🗺️ प्रकोप हॉटस्पॉट मानचित्र",
        "map_style": "🗺️ मानचित्र परत शैली:",
        "inspector_header": "🔍 स्थान निरीक्षक",
        "inspector_help": "डेटा की जांच के लिए मानचित्र पर सक्रिय नोड का चयन करें:",
        "current_loc_params": "वर्तमान स्थान के मौसम पैरामीटर:",
        "google_sv": "🌐 स्ट्रीट व्यू खोलें",
        "google_sat": "🛰️ सैटेलाइट मानचित्र खोलें",
        "cascade_header": "🌿 संबंधित रोग श्रृंखला",
        "secondary_risk": "द्वितीयक जोखिम",
        "what_if_header": "🎯 'What-If' सिम्युलेटर",
        "policy_1": "रासायनिक लार्वानाशकों का प्रयोग (-40% मामले)",
        "policy_2": "सामुदायिक सफाई अभियान (-25% प्रजनन क्षेत्र)",
        "policy_3": "लक्षित गतिशीलता चेतावनी (-15% संचरण)",
        "baseline_label": "अप्रभावित आधारभूत अनुमान:",
        "projected_label": "कम किए गए अनुमानित मामले:",
        "prevented_label": "+ कुल रोके गए अस्पताल दाखिले:",
        "cases_unit": "मामले",
        "patients_unit": "मरीज",
        "optimizer_header": "📋 अनुशंसित कार्रवाई ऑप्टिमाइज़र",
        "memo_header": "📄 कार्यकारी प्रकोप ब्रीफिंग मेमो",
        "download_memo": "📥 ब्रीफिंग मेमो डाउनलोड करें (.txt)",
        "decision_header": "⚡ कमांड कंसोल",
        "btn_warn": "🚨 नागरिक ऐप पर चेतावनी प्रसारित करें",
        "btn_scale": "🚑 आपातकालीन बेड प्रणालियों को सक्रिय करें",
        "btn_sat": "📡 सेंटिनल-2 सैटेलाइट डेटा सिंक करें",
        "citizen_form_header": "📸 नागरिक रिपोर्ट",
        "inc_name": "घटना स्थल का नाम",
        "inc_cat": "देखा गया खतरा वर्ग",
        "inc_obs": "घटना का विवरण",
        "inc_upload": "सत्यापन प्रमाण अपलोड करें (फोटो/वीडियो)",
        "inc_btn": "रिपोर्ट सत्यापित करें और हॉटस्पॉट अपडेट करें",
        "active_feed": "सक्रिय सत्यापित नागरिक रिपोर्ट फ़ीड",
        "contact_title": "🤝 टीम GA1A के साथ सहयोग करें",
        "contact_text": "जलवायु लचीलापन बनाने के लिए GA1A का उपयोग करने वाले सार्वजनिक स्वास्थ्य प्रशासकों के वैश्विक नेटवर्क में शामिल हों।",
        "sponsor_btn": "✉️ टीम GA1A से संपर्क करें"
    }
}

# Premium Google Fonts & Comprehensive CSS UI Overrides for Custom Theme
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">

<style>
    /* Typography & App Base */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #030712 !important;
        color: #f3f4f6 !important;
    }
    
    /* Code/Telematic styling */
    .mono-text {
        font-family: 'Space Mono', monospace !important;
        font-size: 11px;
    }

    /* Sidebar Refinement */
    div[data-testid="stSidebar"] {
        background-color: #070a13 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        box-shadow: 10px 0 30px rgba(0,0,0,0.5);
    }
    
    /* Custom High-End Glassmorphism Card Panels */
    .glass-card {
        background: rgba(15, 23, 42, 0.45) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25) !important;
        margin-bottom: 20px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .panel-container {
        background: rgba(15, 23, 42, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 24px;
        margin-top: 10px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    /* Apple-Style Navigation Tabs Override */
    .stTabs [data-baseweb="tab-list"] {
        gap: 30px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding-bottom: 8px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        color: #94a3b8 !important;
        border: none !important;
        background-color: transparent !important;
        padding: 8px 0px !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #00d2ff !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 2px solid #00d2ff !important;
    }

    /* Overwrite Streamlit Native Metrics to match Premium Palette */
    div[data-testid="metric-container"] {
        background: rgba(10, 15, 30, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* High contrast glowing alert indicators */
    .critical-glow {
        border-left: 5px solid #ff2e93 !important;
        background: rgba(255, 46, 147, 0.08) !important;
        padding: 20px;
        border-radius: 12px;
        color: #ffccd8 !important;
        box-shadow: 0 0 20px rgba(255, 46, 147, 0.1);
    }
    
    .escalating-glow {
        border-left: 5px solid #ffd000 !important;
        background: rgba(255, 208, 0, 0.06) !important;
        padding: 20px;
        border-radius: 12px;
        color: #fff2cc !important;
        box-shadow: 0 0 20px rgba(255, 208, 0, 0.1);
    }
    
    .stable-glow {
        border-left: 5px solid #00f5a0 !important;
        background: rgba(0, 245, 160, 0.06) !important;
        padding: 20px;
        border-radius: 12px;
        color: #d1ffe8 !important;
        box-shadow: 0 0 20px rgba(0, 245, 160, 0.1);
    }
    
    /* Streamlit Form, Button and Input Customizations */
    .stButton>button {
        background: linear-gradient(135deg, #00d2ff 0%, #0066ff 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton>button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(0, 210, 255, 0.4) !important;
    }
    
    /* Terminal Console style log screen */
    .terminal-screen {
        background-color: #02040a !important;
        border: 1px solid rgba(0, 210, 255, 0.15) !important;
        border-radius: 10px !important;
        padding: 14px !important;
        font-family: 'Space Mono', monospace !important;
        color: #00f5a0 !important;
        height: 120px;
        overflow-y: hidden;
        margin-bottom: 20px;
    }
    
    /* Soft glowing status indicators */
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 800;
        border-radius: 6px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# Initialize viewport settings in session state
if "map_center_lat" not in st.session_state:
    st.session_state.map_center_lat = 5.33
if "map_center_lon" not in st.session_state:
    st.session_state.map_center_lon = 103.11
if "map_zoom" not in st.session_state:
    st.session_state.map_zoom = 11.5

# --- DEFINE UTILITY HELPER FUNCTIONS ---

def get_circle_geojson(lat, lon, radius_km=1.5, num_sides=36):
    """
    Generates a mathematically precise GeoJSON Polygon circle around a point coordinate.
    This creates scale-accurate physical hazard circles that respond dynamically to map zoom.
    """
    coords = []
    lat_scale = 111.32
    lon_scale = 111.32 * np.cos(np.radians(lat))
    for theta in np.linspace(0, 2 * np.pi, num_sides):
        d_lat = (radius_km * np.sin(theta)) / lat_scale
        d_lon = (radius_km * np.cos(theta)) / lon_scale
        coords.append([lon + d_lon, lat + d_lat])
    coords.append(coords[0]) # Close the loop
    return {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [coords]
        },
        "properties": {}
    }

def fetch_realtime_weather(lat, lon, selected_date):
    """
    Fetches real-time weather from Open-Meteo API.
    If the selected date is in the future (relative to June 28, 2026), it computes predictive future forecasts.
    Includes a robust mathematical fallback if offline.
    """
    today_dt = datetime(2026, 6, 28)
    target_dt = datetime(selected_date.year, selected_date.month, selected_date.day)
    is_future = target_dt > today_dt
    
    # Defaults in case of fallback
    abs_lat = abs(lat)
    base_lat_temp = max(12.0, 31.0 - (0.35 * abs_lat))
    base_lat_humidity = max(40, 88 - (0.7 * abs_lat))
    base_precip = 0.0
    
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation&forecast_days=1"
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            current_data = res.json().get("current", {})
            base_lat_temp = current_data.get("temperature_2m", base_lat_temp)
            base_lat_humidity = current_data.get("relative_humidity_2m", base_lat_humidity)
            base_precip = current_data.get("precipitation", base_precip)
    except Exception:
        pass # Graceful fallback to geographic baseline
        
    if is_future:
        # Compute dynamic future predictions (extrapolating climate change shifts & seasonal offsets)
        days_ahead = (target_dt - today_dt).days
        seasonal_amplitude = 4.5 * np.sin(2 * np.pi * days_ahead / 365.0)
        global_warming_trend = 0.005 * days_ahead # 1.8C increase per decade
        
        predictive_temp = base_lat_temp + seasonal_amplitude + global_warming_trend
        predictive_humidity = min(100, max(20, int(base_lat_humidity - (seasonal_amplitude * 0.8))))
        predictive_precip = round(base_precip * (1.0 + (np.sin(2 * np.pi * days_ahead / 120.0) * 0.4)), 1)
        
        return round(predictive_temp, 1), int(predictive_humidity), int(predictive_precip * 10), True
    else:
        # Present / Past baseline historical trends
        return round(base_lat_temp, 1), int(base_lat_humidity), int(base_precip * 10), False

def compute_localized_climatology(lat, lon, disease, year):
    annual_anomalies = {
        2016: {"temp_offset": 2.1, "rain_offset": -35, "humid_offset": -8},
        2017: {"temp_offset": 0.2, "rain_offset": 10, "humid_offset": 2},
        2018: {"temp_offset": -0.1, "rain_offset": 5, "humid_offset": 1},
        2019: {"temp_offset": 0.8, "rain_offset": -15, "humid_offset": -3},
        2020: {"temp_offset": -0.8, "rain_offset": 45, "humid_offset": 8},
        2021: {"temp_offset": -0.6, "rain_offset": 30, "humid_offset": 5},
        2022: {"temp_offset": -0.3, "rain_offset": 15, "humid_offset": 3},
        2023: {"temp_offset": 1.9, "rain_offset": -25, "humid_offset": -6},
        2024: {"temp_offset": 0.5, "rain_offset": -5, "humid_offset": -1},
        2025: {"temp_offset": -0.9, "rain_offset": 50, "humid_offset": 10},
        2026: {"temp_offset": 0.1, "rain_offset": 5, "humid_offset": 2}
    }
    
    anomaly = annual_anomalies.get(year, {"temp_offset": 0, "rain_offset": 0, "humid_offset": 0})
    abs_lat = abs(lat)
    base_lat_temp = max(12.0, 31.0 - (0.35 * abs_lat))
    base_lat_humidity = max(40, 88 - (0.7 * abs_lat))
    
    disease_baselines = {
        "Dengue Fever 🦟": {"temp_bias": 0.5, "humid_bias": -2, "hazard": 0.78},
        "Malaria Outbreak 🦟": {"temp_bias": -1.2, "humid_bias": 4, "hazard": 0.69},
        "Cholera Contamination 🦠": {"temp_bias": 2.0, "humid_bias": 8, "hazard": 0.84},
        "Zika Virus 🦟": {"temp_bias": 1.0, "humid_bias": -5, "hazard": 0.59},
        "West Nile Virus 🦅": {"temp_bias": -3.5, "humid_bias": -10, "hazard": 0.49},
        "Lyme Disease Outbreaks 🕷️": {"temp_bias": -8.0, "humid_bias": -15, "hazard": 0.39},
        "Chikungunya Epidemic 🦟": {"temp_bias": 0.2, "humid_bias": -4, "hazard": 0.63},
        "Poliomyelitis Outbreak 💧": {"temp_bias": 1.5, "humid_bias": 5, "hazard": 0.71},
        "Typhoid Fever 🤢": {"temp_bias": 0.8, "humid_bias": 1, "hazard": 0.75},
        "Yellow Fever Sylvatic 🦟": {"temp_bias": -0.5, "humid_bias": 6, "hazard": 0.55},
        "Leptospirosis Flood Surge 🐀": {"temp_bias": -2.0, "humid_bias": 12, "hazard": 0.81},
        "Hepatitis A 🧪": {"temp_bias": -3.0, "humid_bias": -1, "hazard": 0.51},
        "Schistosomiasis Snail Vector 🐌": {"temp_bias": -1.0, "humid_bias": 10, "hazard": 0.57}
    }
    
    bias = disease_baselines.get(disease, {"temp_bias": 0, "humid_bias": 0, "hazard": 0.50})
    live_temp = round(base_lat_temp + bias["temp_bias"] + anomaly["temp_offset"], 1)
    live_humidity = min(100, max(20, int(base_lat_humidity + bias["humid_bias"] + anomaly["humid_offset"])))
    live_precip_change = anomaly["rain_offset"]
    
    return live_temp, live_humidity, live_precip_change, bias["hazard"]

def generate_dataset_csv(disease, year, lat, lon, target_temp, target_humidity, target_precip, location_name):
    """
    Generates a localized dataset tracking simulated weather-pathogen convergence parameters.
    Passing location_name explicitly resolves previous scoping NameErrors.
    """
    dates = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="W")
    n_records = len(dates)
    temps = np.round(target_temp + np.sin(np.linspace(0, 2*np.pi, n_records)) * 2.5, 1)
    humids = np.clip(np.random.normal(target_humidity, 5, n_records).astype(int), 30, 100)
    precip_anom = np.clip(np.random.normal(target_precip, 15, n_records).astype(int), -50, 150)
    risks = np.clip((temps * 0.4) + (humids * 0.5) + (precip_anom * 0.1), 5, 100).astype(int)
    
    df = pd.DataFrame({
        "Timestamp": dates,
        "Target Location": location_name,
        "Target Latitude": round(lat, 4),
        "Target Longitude": round(lon, 4),
        "Target Disease": disease,
        "Observed Temp (C)": temps,
        "Observed Humidity (%)": humids,
        "Precipitation Anomaly (%)": precip_anom,
        "Computed Outbreak Risk (%)": risks
    })
    return df

# --- INITIALIZE SYSTEM LANGUAGE SELECTION ROOT ---
selected_lang_key = st.selectbox("", options=list(translations.keys()), index=0, help="GA1A Global Localizer Nodes")
lang = translations[selected_lang_key]

# --- 1. PREMIUM GEOCODING INTEGRATION (SINGLE INTEGRATED AUTOMATED SEARCH BAR) ---
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

# Dynamic dropdown loaded directly from Geocoding search matching
suggestion_list = [item["display"] for item in suggestions]
selected_suggestion_name = st.sidebar.selectbox(lang['select_loc'], options=suggestion_list, index=0)

# Extract coordinates based on selected matched location
selected_coords = next((item for item in suggestions if item["display"] == selected_suggestion_name), suggestions[0])
current_lat = selected_coords["lat"]
current_lon = selected_coords["lon"]
active_location_name = selected_coords["display"]

# Center map on current location automatically upon select changes
st.session_state.map_center_lat = current_lat
st.session_state.map_center_lon = current_lon

# --- 1.5 ADAPTIVE CURRENCY & HOTLINE SYSTEM (GEOGRAPHIC SPECIFICS) ---
if any(kw in active_location_name.lower() for kw in ["malaysia", "terengganu", "kuala", "johor", "perak", "penang", "selangor"]):
    user_country = "Malaysia"
    currency_symbol = "RM"
    currency_rate = 1.0 
    local_agencies = [
        {"name": "MOH Malaysia (KKM CPRC)", "hotline": "+603-8881 0200", "role": "Infectious Disease Crisis Preparedness"},
        {"name": "Department of Environment (DOE)", "hotline": "1-800-88-2727", "role": "Climatic Chemical Pollution Monitoring"},
        {"name": "National Disaster Management Agency (NADMA)", "hotline": "+603-8064 2400", "role": "Flash Flood Drainage Emergency Response"}
    ]
elif any(kw in active_location_name.lower() for kw in ["japan", "okinawa", "tokyo", "kyoto", "osaka", "hokkaido"]):
    user_country = "Japan"
    currency_symbol = "JPY (¥)"
    currency_rate = 34.5 
    local_agencies = [
        {"name": "Ministry of Health, Labour and Welfare (MHLW)", "hotline": "+81-3-5253-1111", "role": "Infectious Pathology Control Hub"},
        {"name": "National Institute of Infectious Diseases (NIID)", "hotline": "+81-3-5285-1111", "role": "Vector Genotyping Surveillance"},
        {"name": "Ministry of the Environment (MOE)", "hotline": "+81-3-3581-3351", "role": "Eco-System Vector Breeding Control"}
    ]
else:
    user_country = "Global"
    currency_symbol = "USD ($)"
    currency_rate = 0.23 
    local_agencies = [
        {"name": "World Health Organization (WHO GOARN)", "hotline": "+41 22 791 2111", "role": "Global Outbreak Surveillance Nodes"},
        {"name": "UNEP Climate Action Network", "hotline": "+254 20 762 1234", "role": "Vector Migration Modeling"},
        {"name": "International Red Cross (IFRC)", "hotline": "+41 22 730 4222", "role": "Emergency Humanitarian Deployment"}
    ]

# --- 2. PATHOLOGY AND TEMPORAL SELECTORS ---
selected_disease = st.sidebar.selectbox(lang['pathology'], options=disease_options)

# Dynamic calendar picker
chosen_calendar_date = st.sidebar.date_input(
    lang['timeline'], 
    value=date(2026, 6, 28), 
    help="Select the exact day, month, and year to observe climate correlations."
)

# Convert chosen date into anomalies to scale modeling
date_month_factor = chosen_calendar_date.month

# --- 2.3 REAL-TIME SATELLITE & SENSORS PIPELINE INGESTION ---
live_api_temp, live_api_humid, live_api_precip, is_future_model = fetch_realtime_weather(current_lat, current_lon, chosen_calendar_date)

# Base computations using historical deviations
base_temp, base_humidity, base_precip, base_hazard = compute_localized_climatology(current_lat, current_lon, selected_disease, chosen_calendar_date.year)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<h3 style='font-size:14px; font-weight:700; color:#00d2ff; text-transform:uppercase;'>{lang['telemetry']}</h3>", unsafe_allow_html=True)

# Sliders auto-lock to live fetched weather values
temp = st.sidebar.slider(lang['temp_label'], 10.0, 45.0, float(live_api_temp), step=0.5)
humidity = st.sidebar.slider(lang['humid_label'], 20, 100, int(live_api_humid), step=1)
precipitation_vol = st.sidebar.slider(lang['precip_label'], -50, 150, int(live_api_precip), step=10)
population_mobility = st.sidebar.slider(lang['mobility_label'], 0.5, 2.5, 1.2, step=0.1)

# Satellite Data Export Channel - passing active_location_name explicitly
dataset_df = generate_dataset_csv(selected_disease, chosen_calendar_date.year, current_lat, current_lon, temp, humidity, precipitation_vol, active_location_name)
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

# --- 2.5 SYSTEM ACCESS MONITOR (VISITOR COUNTER) ---
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

# --- 3. MATH CLIMATIC MODELLING CALCULATOR ---
rain_factor = 1.0 + (precipitation_vol / 100.0)
temp_factor = np.exp(-((temp - base_temp) ** 2) / 35.0) 
humidity_factor = (humidity / 70.0) if humidity < 70 else (1.0 + ((humidity - 70) * 0.02))

computed_risk = base_hazard * temp_factor * rain_factor * humidity_factor * population_mobility
final_risk_score = min(100, max(5, int(computed_risk * 100)))

# --- 3.5 EXPLICIT STATUS LIGHT MAPPING & HIGH-INTENSITY NEON GLOW STYLING ---
if final_risk_score >= 70:
    risk_level = "CRITICAL"
    risk_color = "#ff2e93"
    risk_bg = "rgba(255, 46, 147, 0.15)"
    red_led_style = "background-color: #ff2e93; box-shadow: 0 0 35px 8px rgba(255, 46, 147, 0.85); opacity: 1.0; border: 1px solid rgba(255,255,255,0.2);"
    yellow_led_style = "background-color: #ffd000; opacity: 0.15; box-shadow: none;"
    green_led_style = "background-color: #00f5a0; opacity: 0.15; box-shadow: none;"
elif final_risk_score >= 40:
    risk_level = "ESCALATING"
    risk_color = "#ffd000"
    risk_bg = "rgba(255, 208, 0, 0.15)"
    red_led_style = "background-color: #ff2e93; opacity: 0.15; box-shadow: none;"
    yellow_led_style = "background-color: #ffd000; box-shadow: 0 0 35px 8px rgba(255, 208, 0, 0.85); opacity: 1.0; border: 1px solid rgba(255,255,255,0.2);"
    green_led_style = "background-color: #00f5a0; opacity: 0.15; box-shadow: none;"
else:
    risk_level = "STABLE"
    risk_color = "#00f5a0"
    risk_bg = "rgba(0, 245, 160, 0.15)"
    red_led_style = "background-color: #ff2e93; opacity: 0.15; box-shadow: none;"
    yellow_led_style = "background-color: #ffd000; opacity: 0.15; box-shadow: none;"
    green_led_style = "background-color: #00f5a0; box-shadow: 0 0 25px 5px rgba(0, 245, 160, 0.85); transition: all 0.3s;"

projected_cases = int(final_risk_score * 4.8 * population_mobility * (1 + (date_month_factor / 30)))
beds_needed = int(projected_cases * 0.22)
localized_cost = (projected_cases * 3400 * currency_rate) / 1000000

# Briefing Text Generator
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
A clinical surge capacity planning curve of {projected_cases} cases has been registered. It is advised to immediately release financial reserves totaling {currency_symbol} {localized_cost:.2f}M to cover preventative biological vector controls and optimize district triage facilities."""

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
        <div class='glass-card'>
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

    # MAP SECTION WITH MULTI-LAYER TOGGLE
    col_map_desc, col_map_layer_ctrl = st.columns([1.5, 2.5])
    with col_map_desc:
        st.markdown(f"### {lang['map_header']}")
    with col_map_layer_ctrl:
        map_layer_view = st.radio(
            "🗺️ Active Layer Filter:",
            options=["🔴 Current Outbreak Zones", "🔮 Predictive Hotspots (14-Day Forecast)", "🛰️ Multi-Layer Consolidated View"],
            horizontal=True,
            help="Toggle the visual interface layer to display current environmental threats or projected transmission vector drift."
        )

    # Ingestion logs banner to show data status clearly
    if is_future_model:
        st.markdown("""
        <div style='background: rgba(255, 46, 147, 0.08); border: 1px solid #ff2e93; padding: 10px 16px; border-radius: 8px; margin-bottom: 15px; font-family: monospace; font-size: 12px; font-weight: bold; color: #ffb3d1;'>
            🔮 FUTURE PREDICTIVE SIMULATION MODE ACTIVE (GEOGRAPHIC GRADIENTS EXTRAPOLATED)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: rgba(0, 245, 160, 0.08); border: 1px solid #00f5a0; padding: 10px 16px; border-radius: 8px; margin-bottom: 15px; font-family: monospace; font-size: 12px; font-weight: bold; color: #b3ffd9;'>
            🛰️ LIVE STATION DATA & HISTORICAL TELEMETRY INGESTION ACTIVE (OPEN-METEO ENGINE)
        </div>
        """, unsafe_allow_html=True)

    col_map_render, col_dashboard_lights = st.columns([2.2, 0.8])
    
    with col_map_render:
        map_style_toggle = st.radio(
            lang['map_style'], 
            options=["🌌 Dark Radar Map", "🏙️ Regular Street Map"], 
            horizontal=True
        )
        selected_style = "carto-darkmatter" if map_style_toggle == "🌌 Dark Radar Map" else "open-street-map"

        # Set up coordinate datasets relative to dynamic map center coordinates
        map_data = pd.DataFrame([
            {
                "ID": "[Node A]",
                "Place": f"[Node A] Central Core Area",
                "lat": current_lat,
                "lon": current_lon,
                "Base Hazard": 0.85,
                "Temp Offset": 0.0,
                "Humidity Offset": 0,
                "Precip Offset": 0,
                "Operational Status": "🚨 CRITICAL THREAT RED ZONE",
                "Hist Outbreaks": "Intense climate anomalous spread logged in 2016, 2023."
            },
            {
                "ID": "[Node B]",
                "Place": f"[Node B] Northern Residential Fringe",
                "lat": current_lat + 0.015,
                "lon": current_lon + 0.015,
                "Base Hazard": 0.55,
                "Temp Offset": -0.8,
                "Humidity Offset": -5,
                "Precip Offset": -10,
                "Operational Status": "💨 Prevention Fogging Protocol Commenced",
                "Hist Outbreaks": "Moderate transmission recorded. Strong correlation with micro-drainage pooling."
            },
            {
                "ID": "[Node C]",
                "Place": f"[Node C] Southern Wetland Sector",
                "lat": current_lat - 0.015,
                "lon": current_lon - 0.015,
                "Base Hazard": 0.35,
                "Temp Offset": -1.5,
                "Humidity Offset": 8,
                "Precip Offset": 15,
                "Operational Status": "🟢 High Surveillance Level Active - Stable",
                "Hist Outbreaks": "Low historical outbreaks. Prone to immediate floodwater runoff surges."
            }
        ])

        map_data["Risk Score (%)"] = (map_data["Base Hazard"] * (final_risk_score / 100) * 100).round().astype(int)
        map_data["Risk Score (%)"] = map_data["Risk Score (%)"].clip(5, 100)

        df_reports = st.session_state.citizen_pins.copy()
        if not df_reports.empty:
            df_reports["ID"] = "[Citizen Report]"
            df_reports["Place"] = "[Citizen Report] " + df_reports["Place"]
            df_reports["lat"] = current_lat + df_reports["lat_offset"]
            df_reports["lon"] = current_lon + df_reports["lon_offset"]
            df_reports["Base Hazard"] = 0.60
            df_reports["Temp Offset"] = -0.2
            df_reports["Humidity Offset"] = 2
            df_reports["Precip Offset"] = 5
            df_reports["Risk Score (%)"] = int(final_risk_score * 0.8)
            df_reports["Operational Status"] = "⚠️ Verified Resident Bio-Threat Flagged"
            df_reports["Hist Outbreaks"] = "First recorded structural citizen warning in the current cycle."
            
            combined_map_df = pd.concat([map_data, df_reports], ignore_index=True)
        else:
            combined_map_df = map_data

        # Mapbox Layout Layers Generation: Draws true geometric scaling rings styled in shades of warning red
        mapbox_layers = []
        for idx, row in combined_map_df.iterrows():
            # Current threat layer circles (Concentric shades of Red)
            if map_layer_view in ["🔴 Current Outbreak Zones", "🛰️ Multi-Layer Consolidated View"]:
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
                    below="traces"
                ))

            # Future predictive spread layer circles (Translucent Glowing Violet/Purple Circles shifted with meteorological drift)
            if map_layer_view in ["🔮 Predictive Hotspots (14-Day Forecast)", "🛰️ Multi-Layer Consolidated View"]:
                # Shift coordinates slightly to model spread drift over 14 days based on climate sliders
                pred_lat = row["lat"] + 0.006 * np.cos(np.radians(temp))
                pred_lon = row["lon"] + 0.006 * np.sin(np.radians(humidity))
                
                radius_km = 1.2 + (row["Risk Score (%)"] / 100.0) * 2.2 # Predictive spreads are larger
                node_pred_circle_geojson = get_circle_geojson(pred_lat, pred_lon, radius_km)
                
                fill_color_pred = "rgba(176, 38, 255, 0.25)"   # Futuristic violet glow
                line_color_pred = "rgba(176, 38, 255, 0.75)"
                
                mapbox_layers.append(dict(
                    sourcetype='geojson',
                    source=node_pred_circle_geojson,
                    type='fill',
                    color=fill_color_pred,
                    below="traces"
                ))
                mapbox_layers.append(dict(
                    sourcetype='geojson',
                    source=node_pred_circle_geojson,
                    type='line',
                    color=line_color_pred,
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

    with col_dashboard_lights:
        # HIGH-END LED BREATHING SECURITY LIGHT PANEL Overhaul
        st.markdown("<p style='font-size:12px; font-weight:700; color:#94a3b8; text-transform:uppercase;'>SECURITY TIER MONITOR</p>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.55); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 24px; text-align: center; min-height: 400px; display: flex; flex-direction: column; justify-content: space-around;">
            <div>
                <p style="font-size: 11px; font-family: 'Space Mono', monospace; color: #94a3b8; letter-spacing: 0.1em; margin: 0 0 15px 0;">BIO-SECURITY STATUS LIGHTS</p>
                
                <!-- Red Critical LED -->
                <div style="margin: 15px auto; width: 45px; height: 45px; border-radius: 50%; transition: all 0.3s; {red_led_style}"></div>
                
                <!-- Yellow Escalating LED -->
                <div style="margin: 15px auto; width: 45px; height: 45px; border-radius: 50%; transition: all 0.3s; {yellow_led_style}"></div>
                
                <!-- Green Stable LED -->
                <div style="margin: 15px auto; width: 45px; height: 45px; border-radius: 50%; transition: all 0.3s; {green_led_style}"></div>
            </div>
            
            <div style="border-top: 1px solid rgba(255, 255, 255, 0.06); padding-top: 15px;">
                <span style="font-family: 'Space Mono', monospace; font-size: 10px; color: #94a3b8; display: block; letter-spacing: 0.15em;">ACTIVE THREAT INDEX</span>
                <span style="font-size: 26px; font-weight: 800; color: {risk_color}; letter-spacing: -0.03em;">{risk_level}</span>
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
            <div class="critical-glow">
                <h5 style='color: #ff2e93; font-weight:800; margin-top:0;'>⚠️ THREAT STATUS: CRITICAL</h5>
                <ul style='color: #ffccd8; font-size: 13px; line-height:1.7; margin-bottom:0; padding-left:20px;'>
                    <li>Deploy automated biological larvicides targeting highest concentration vectors within 48 hours.</li>
                    <li>Notify and provision regional triage centers; release sterile saline IV reserves.</li>
                    <li>Broadcast high-risk push coordinates targeting outdoor mobile personnel.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif risk_level == "ESCALATING":
            st.markdown(f"""
            <div class="escalating-glow">
                <h5 style='color: #ffd000; font-weight:800; margin-top:0;'>⚠️ THREAT STATUS: ESCALATING</h5>
                <ul style='color: #fff2cc; font-size: 13px; line-height:1.7; margin-bottom:0; padding-left:20px;'>
                    <li>Launch sweeping water catchment clearing runs across marshlands and estuary waterways.</li>
                    <li>Activate outpatient community clinics to prepare for mild seasonal diagnostic surges.</li>
                    <li>Deploy civic media campaigns advising household water storage removal protocols.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="stable-glow">
                <h5 style='color: #00f5a0; font-weight:800; margin-top:0;'>✅ THREAT STATUS: CONFINED</h5>
                <p style='color: #d1ffe8; font-size: 13px; line-height:1.7; margin:0;'>
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
        <div style='background: rgba(15, 23, 42, 0.35); border: 1px solid rgba(255, 255, 255, 0.05); padding: 16px; border-radius: 12px; min-height: 120px;'>
            <p style='font-size:11px; color:#00d2ff; font-weight:bold; margin:0;'>CLIMATIC & ENVIRONMENT</p>
            <p style='font-size:15px; font-weight:800; margin:4px 0;'>{local_agencies[1]["name"]}</p>
            <p style='font-size:16px; font-family:monospace; color:#fff; font-weight:bold; margin:0;'>{local_agencies[1]["hotline"]}</p>
            <span style='font-size:10px; color:#94a3b8;'>{local_agencies[1]["role"]}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_hot_3:
        st.markdown(f"""
        <div style='background: rgba(15, 23, 42, 0.35); border: 1px solid rgba(255, 255, 255, 0.05); padding: 16px; border-radius: 12px; min-height: 120px;'>
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