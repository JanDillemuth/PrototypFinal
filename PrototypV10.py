# =============================================================================
# app.py – KOMM Ambulante Dienste e.V. | Wissensmanagementsystem (WMS)
# Prototyp (Proof of Concept) – Vollständig gemockt (In-Memory)
# Finaler Stand: Absolut Cloud-stabil & Fixiertes Dropdown-Verhalten
# =============================================================================
# Ausführung: streamlit run app.py
# Abhängigkeiten: streamlit (pip install streamlit)
# =============================================================================

import time
import os
import base64
import streamlit as st

# --- Seitenkonfiguration ---
st.set_page_config(
    page_title="KOMM WMS – Wissensmanagementsystem",
    page_icon=":material/health_and_safety:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Hilfsfunktion für nahtlose Logo-Integration ---
def get_image_base64(pfad):
    """Liest ein lokales Bild und gibt es als Base64-String zurück, um es in HTML einzubetten."""
    if os.path.exists(pfad):
        with open(pfad, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Bild laden (Fallback ist None, falls die Datei nicht gefunden wird)
LOGO_BASE64 = get_image_base64("Komm.png")


# =============================================================================
# ABSCHNITT 1: CORPORATE DESIGN & CSS (Isoliert für maximale Cloud-Stabilität)
# =============================================================================
st.html("""
<style>
    /* Google Material Symbols (Rounded) importieren für professionelle Piktogramme */
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,1,0');

    /* Globale Farbvariablen */
    :root {
        --komm-gruen: #12734a;
        --komm-gruen-hover: #0e5c3a;
        --komm-gruen-hell: #eaf4ee;
        --text-dunkel: #2c3e50;
        --text-grau: #7f8c8d;
        --bg-chat-system: #f8fcf9;
        --radius-klein: 12px;
        --radius-gross: 24px;
        --schatten-weich: 0 4px 20px rgba(0, 0, 0, 0.04);
        --schatten-gruen: 0 4px 15px rgba(18, 115, 74, 0.15);
    }

    /* Piktogramm-Klasse für eigene HTML-Elemente */
    .icon {
        font-family: 'Material Symbols Rounded' !important;
        font-weight: normal;
        font-style: normal;
        font-size: 24px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        vertical-align: middle;
        -webkit-font-smoothing: antialiased;
    }

    /* Minimal-invasive Button-Abrundung */
    .stButton > button, .stFormSubmitButton > button {
        border-radius: var(--radius-klein) !important;
        font-weight: 600 !important;
    }

    /* Header-Leiste */
    .wms-header {
        background: linear-gradient(135deg, var(--komm-gruen), #1a9660);
        color: #ffffff;
        padding: 1.2rem 1.8rem;
        border-radius: var(--radius-klein);
        margin-bottom: 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        box-shadow: var(--schatten-gruen);
        display: flex;
        align-items: center;
        gap: 12px;
    }

    /* Login-Container */
    .login-container {
        background-color: #ffffff;
        border: none;
        border-radius: var(--radius-gross);
        padding: 3rem 2.5rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        margin-top: 5vh;
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-icon {
        font-size: 48px;
        color: var(--komm-gruen);
        margin-bottom: 1rem;
    }

    /* Modernes Chat-Design mit Avataren */
    .chat-row-user {
        display: flex;
        justify-content: flex-end;
        align-items: flex-end;
        margin-bottom: 1.5rem;
        gap: 12px;
    }
    .chat-row-system {
        display: flex;
        justify-content: flex-start;
        align-items: flex-end;
        margin-bottom: 1.5rem;
        gap: 12px;
    }
    
    .chat-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
    }
    .avatar-user {
        background-color: var(--komm-gruen-hell);
        color: var(--komm-gruen);
    }
    .avatar-system {
        background-color: #1a9660;
        color: #ffffff;
        box-shadow: var(--schatten-gruen);
    }

    .msg-user {
        background-color: var(--komm-gruen);
        color: #ffffff;
        padding: 1.2rem 1.4rem;
        border-radius: 24px 24px 4px 24px;
        max-width: 75%;
        box-shadow: var(--schatten-gruen);
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .msg-system {
        background-color: var(--bg-chat-system);
        border: 1px solid #eaf0ed;
        color: var(--text-dunkel);
        padding: 1.2rem 1.4rem;
        border-radius: 24px 24px 24px 4px;
        max-width: 75%;
        box-shadow: var(--schatten-weich);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .msg-label {
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .label-user { color: rgba(255,255,255,0.8); }
    .label-system { color: var(--komm-gruen); }

    /* Lade-Animation */
    .loader-container {
        margin: 1rem 0;
        padding: 1.5rem;
        background: #ffffff;
        border-radius: var(--radius-klein);
        border: 1px solid #eaeaea;
        box-shadow: var(--schatten-weich);
        text-align: center;
    }
    .loader-text {
        font-weight: 600;
        color: var(--komm-gruen);
        margin-bottom: 0.8rem;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    .modern-loader {
        width: 100%;
        height: 6px;
        background-color: var(--komm-gruen-hell);
        border-radius: 10px;
        overflow: hidden;
        position: relative;
    }
    .modern-loader::after {
        content: '';
        position: absolute;
        left: -50%;
        height: 100%;
        width: 50%;
        background-color: var(--komm-gruen);
        border-radius: 10px;
        animation: slide 1.2s infinite ease-in-out;
    }
    @keyframes slide {
        0% { left: -50%; }
        100% { left: 100%; }
    }

    /* Disclaimer-Kasten */
    .disclaimer {
        background-color: #fff8e1;
        border: 1px solid #fde68a;
        border-left: 4px solid #f59e0b;
        border-radius: var(--radius-klein);
        padding: 1.2rem 1.4rem;
        margin: 1rem 0 1.4rem 0;
        font-size: 0.92rem;
        color: var(--text-dunkel);
        line-height: 1.5;
        box-shadow: var(--schatten-weich);
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .onto-titel {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--komm-gruen);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Status-Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .badge-ok { background-color: var(--komm-gruen-hell); color: var(--komm-gruen); }
    .badge-nein { background-color: #fee2e2; color: #b91c1c; }
    .badge-neutral { background-color: #f3f4f6; color: #4b5563; }

    /* Metriken-Spezial */
    .metrik-wert { font-size: 2rem; font-weight: 800; color: var(--komm-gruen); margin-bottom: 0.2rem; }
    .metrik-label { font-size: 0.85rem; color: var(--text-grau); font-weight: 600; text-transform: uppercase; }

    /* Profile Subpage Styles */
    .profil-header-label { font-size: 0.8rem; text-transform: uppercase; color: var(--text-grau); letter-spacing: 0.05em; margin-bottom: 0.2rem;}
    .profil-header-wert { font-size: 1.1rem; font-weight: 600; color: var(--text-dunkel); margin-bottom: 1.2rem;}

    /* Verblassende Trennlinien */
    hr { 
        border: 0 !important; 
        height: 1px !important; 
        background: linear-gradient(to right, rgba(18, 115, 74, 0), rgba(18, 115, 74, 0.4), rgba(18, 115, 74, 0)) !important;
        margin: 2rem 0 !important; 
    }
    
    /* ONTOLOGIE-REFERENZEN (INLINE TOOLTIPS) */
    .onto-ref {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: var(--komm-gruen-hell);
        color: var(--komm-gruen);
        border-radius: 50%;
        width: 18px;
        height: 18px;
        font-size: 10px;
        font-weight: 800;
        cursor: pointer;
        margin: 0 4px;
        position: relative;
        vertical-align: super;
        box-shadow: 0 2px 4px rgba(18, 115, 74, 0.1);
    }
    .onto-ref:hover, .onto-ref:active {
        background-color: var(--komm-gruen);
        color: #ffffff;
    }
    .onto-ref .tooltiptext {
        visibility: hidden;
        width: 260px;
        background-color: var(--text-dunkel);
        color: #ffffff;
        text-align: left;
        border-radius: 8px;
        padding: 10px 14px;
        position: absolute;
        z-index: 9999;
        bottom: 140%;
        left: 50%;
        transform: translateX(-50%) translateY(10px);
        opacity: 0;
        transition: opacity 0.3s, transform 0.3s;
        font-size: 0.85rem;
        font-weight: normal;
        line-height: 1.5;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        pointer-events: none;
    }
    .onto-ref .tooltiptext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -6px;
        border-width: 6px;
        border-style: solid;
        border-color: var(--text-dunkel) transparent transparent transparent;
    }
    .onto-ref:hover .tooltiptext, .onto-ref:active .tooltiptext {
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
</style>
""")


# =============================================================================
# ABSCHNITT 2: GEMOCKTE WISSENSBASIS & METRIKEN
# =============================================================================

BEISPIELFRAGEN = {
    "Abrechnung Pflegegrad 1": {
        "frage_voll": "Wie wird Pflegegrad 1 korrekt abgerechnet?",
        "antwort": (
            "Pflegegrad 1 berechtigt zur Inanspruchnahme des Entlastungsbetrages "
            "gemäß § 45b SGB XI in Höhe von 125 Euro monatlich. "
            "<span class='onto-ref'>1<span class='tooltiptext'><strong>📌 Abrechnungsregel Pflegegrad 1</strong><br>Ontologie erzwang Verweis auf § 45b SGB XI. Sachleistungen wurden logisch ausgeschlossen.</span></span> "
            "Eine Anerkennung als Pflegeleistung im Sinne der Sachleistungsvergabe (§ 36 SGB XI) ist "
            "bei Pflegegrad 1 nicht möglich. Die Abrechnung erfolgt ausschließlich "
            "über den Entlastungsbetrag direkt mit die Pflegekasse. Interne "
            "Abrechnungsfrist: bis zum 5. des Folgemonats. "
            "<span class='onto-ref'>2<span class='tooltiptext'><strong>📑 Vereinsinterne Richtlinie #08</strong><br>Standard-Fristen für die Finanzbuchhaltung aus dem Qualitätsmanagement-Handbuch geladen.</span></span>"
        ),
    },
    "Dokumentationsfristen": {
        "frage_voll": "Welche Dokumentationsfristen gelten für ambulante Pflegeeinsätze?",
        "antwort": (
            "Gemäß den MDK-Qualitätsrichtlinien und den internen Vorgaben von KOMM e.V. "
            "müssen Leistungsnachweise und Pflegeberichte tagaktuell dokumentiert werden. "
            "<span class='onto-ref'>1<span class='tooltiptext'><strong>📌 MDK-Dokumentationsstandard</strong><br>Konformitätsregel C-44 (Tagaktualität der Pflegeberichte) aus der Domäne 'Pflege' angewendet.</span></span> "
            "Die endgültige Übertragung in das Dokumentationssystem hat spätestens "
            "24 Stunden nach Erbringung der Leistung zu erfolgen. Bei Abweichungen vom "
            "Hilfeplan ist umgehend die Pflegedienstleitung zu informieren. "
            "<span class='onto-ref'>2<span class='tooltiptext'><strong>⚠️ Eskalationsregel-Reasoner</strong><br>Logische Verknüpfung: Wenn Abweichung = True, dann Benachrichtigung_PDL auslösen.</span></span>"
        ),
    },
    "Abrechnungsprozess (Schema)": {
        "frage_voll": "Wie läuft das Schema für den monatlichen Abrechnungsprozess ab?",
        "antwort": (
            "Der monatliche Abrechnungsprozess bei KOMM e.V. erfolgt in einem vierstufigen Schema: "
            "Zunächst müssen alle Leistungsnachweise bis zum 3. Werktag des Folgemonats vollständig signiert vorliegen. "
            "<span class='onto-ref'>1<span class='tooltiptext'><strong>📌 Qualitätsregel: Signaturprüfung</strong><br>Axiom: IF Signatur == FEHLT THEN Status = SPERRE. System blockiert unvollständige Nachweise für die Abrechnung.</span></span> "
            "Danach werden die erfassten Daten in das zentrale Abrechnungssystem übertragen. "
            "Die Hauptabrechnung mit den Pflege- und Krankenkassen erfolgt zwingend elektronisch im Datenträgeraustausch (DTA) nach § 105 SGB XI. "
            "<span class='onto-ref'>2<span class='tooltiptext'><strong>⚙️ Routing-Regel SGB XI</strong><br>Logik: IF Kostenträger == Pflegekasse THEN Export = DTA-Format (verschlüsselt). Papierformate werden abgelehnt.</span></span> "
            "Offene Eigenanteile, Investitionskosten oder privat vereinbarte Zusatzleistungen werden in einem separaten Lauf am 10. des Monats direkt dem Klienten in Rechnung gestellt."
        ),
    },
}

PLATZHALTER_ANTWORT = (
    "Hier würde dann die präzise Antwort des Systems stehen, basierend auf den "
    "abgerufenen Richtlinien und Handbüchern des Vereins."
)

REGEL_KANDIDATEN = [
    {
        "id": 1,
        "titel": "Abrechnungsregel Pflegegrad 1",
        "beschreibung": (
            "Wenn Pflegegrad = 1, dann Abrechnung ausschließlich über "
            "Entlastungsbetrag (§ 45b SGB XI). Sachleistungsabrechnung ausschließen."
        ),
        "haeufigkeit": 14,
    },
    {
        "id": 2,
        "titel": "Dokumentationsfrist-Eskalation",
        "beschreibung": (
            "Wenn Dokumentationszeitpunkt > 24 h nach Leistungserbringung, dann "
            "automatische Benachrichtigung der Pflegedienstleitung auslösen."
        ),
        "haeufigkeit": 9,
    },
]

METRIKEN = {
    "serverauslastung_pct": 34,
    "antwortlatenz_ms": 187,
    "maskierte_pii": 1243,
    "positives_feedback_pct": 78,
    "negatives_feedback_pct": 22,
    "anfragen_heute": 57,
    "aktive_axiome": 12,
}


# =============================================================================
# ABSCHNITT 3: SESSION STATE INITIALISIERUNG & SAFE CALLBACK
# =============================================================================
def init_session():
    defaults = {
        "eingeloggt": False,
        "benutzername": "",
        "rolle": "",
        "aktuelle_seite": "main",
        "modus": "Web UI Chat Interface",
        "ki_modus": "Ausgewogen (Standard)",
        "chat_verlauf": [],
        "feedback": {},
        "eingereichtes_feedback": [
            "Die Antwort zur Verhinderungspflege war etwas zu lang formuliert.",
            "Mir fehlt in manchen Texten der direkte Verweis auf die internen Leitfäden."
        ],
        "manuelle_regeln": [],
        "regel_status": {r["id"]: None for r in REGEL_KANDIDATEN},
        "tickets": [
            {"id": 1, "titel": "Fehler bei SGB XII Abfrage", "beschreibung": "Das System gibt manchmal noch die veralteten Pauschalen aus.", "status": "Offen", "ersteller": "Mitarbeiter A"},
            {"id": 2, "titel": "Ladezeit bei Dokumenten", "beschreibung": "Das Office-Plugin braucht sehr lange, um zu analysieren.", "status": "In Bearbeitung", "ersteller": "Mitarbeiter B"},
        ],
        "ticket_counter": 3
    }
    for schluessel, wert in defaults.items():
        if schluessel not in st.session_state:
            st.session_state[schluessel] = wert

init_session()

def sichere_ticket_status_direkt(ticket_id, selectbox_key):
    if "tickets" in st.session_state:
        for tk in st.session_state.tickets:
            if tk['id'] == ticket_id:
                tk['status'] = st.session_state[selectbox_key]
                break


# =============================================================================
# ABSCHNITT 4: LOGIN-BILDSCHIRM (Zugriffskontrolle)
# =============================================================================
if not st.session_state.eingeloggt:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        if LOGO_BASE64:
            st.markdown(
                f'<div class="login-container">'
                f'<img src="data:image/png;base64,{LOGO_BASE64}" style="max-width: 280px; margin-bottom: 2rem;">'
                f'<p style="color: #7f8c8d; margin-bottom: 2rem; font-weight: 600; font-size: 1.1rem;">Wissensmanagementsystem</p>'
                f'</div>', 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="login-container">'
                '<span class="icon login-icon">shield_person</span>'
                '<h2 style="color: #12734a; font-weight: 800; margin-bottom: 0;">KOMM e.V.</h2>'
                '<p style="color: #7f8c8d; margin-bottom: 2rem;">Wissensmanagementsystem</p>'
                '</div>', 
                unsafe_allow_html=True
            )
        
        with st.form("login_form"):
            eingabe_nutzer = st.text_input("Benutzername", placeholder="Geben Sie Bilal, Jan, Youssef, Weinß (Admin) oder Farhad ein")
            eingabe_passwort = st.text_input("Passwort", type="password", placeholder="Beliebiges Passwort eingeben")
            
            submit_login = st.form_submit_button("System betreten", icon=":material/login:", use_container_width=True)
            
            if submit_login:
                nutzer_klein = eingabe_nutzer.strip().lower()
                if nutzer_klein == "bilal":
                    st.session_state.eingeloggt = True
                    st.session_state.benutzername = "Bilal"
                    st.session_state.rolle = "Nutzer"
                    st.session_state.aktuelle_seite = "main"
                    st.rerun()
                elif nutzer_klein == "jan":
                    st.session_state.eingeloggt = True
                    st.session_state.benutzername = "Jan"
                    st.session_state.rolle = "Nutzer"
                    st.session_state.aktuelle_seite = "main"
                    st.rerun()
                elif nutzer_klein == "youssef":
                    st.session_state.eingeloggt = True
                    st.session_state.benutzername = "youssef"
                    st.session_state.rolle = "Nutzer"
                    st.session_state.aktuelle_seite = "main"
                    st.rerun()
                elif nutzer_klein == "weinß":
                    st.session_state.eingeloggt = True
                    st.session_state.benutzername = "weinß"
                    st.session_state.rolle = "Administrator"
                    st.session_state.aktuelle_seite = "main"
                    st.rerun()
                elif nutzer_klein == "farhad":
                    st.session_state.eingeloggt = True
                    st.session_state.benutzername = "farhad"
                    st.session_state.rolle = "Nutzer"
                    st.session_state.aktuelle_seite = "main"
                    st.rerun()
                else:
                    st.error("Zugriff verweigert. Bitte 'Bilal', 'Jan', 'Youssef', 'Weinß' (Admin) oder 'Farhad' verwenden.")
                    
        st.markdown("<p style='font-size: 0.85rem; color: #95a5a6; text-align: center;'>Demo-Umgebung: Bilal = Nutzer | Jan = Nutzer | Youssef = Nutzer | Weinß = Administrator | Farhad = Nutzer</p>", unsafe_allow_html=True)
    
    st.stop()


# =============================================================================
# ABSCHNITT 5: SEITENLEISTE (Nach erfolgreichem Login)
# =============================================================================
with st.sidebar:
    if LOGO_BASE64:
        st.markdown(
            f'<div style="text-align: center; margin-bottom: 1.5rem; margin-top: 1rem;">'
            f'<img src="data:image/png;base64,{LOGO_BASE64}" style="max-width: 85%; height: auto;">'
            f'<p style="color: var(--text-grau); font-size: 0.85rem; margin-top: 0.5rem; font-weight: 600;">WMS Prototyp</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown("<h3 style='color:#12734a; font-weight:700; display:flex; align-items:center; gap:8px;'><span class='icon'>neurology</span> WMS Prototyp</h3>", unsafe_allow_html=True)
        
    st.divider()

    if st.button(f"{st.session_state.benutzername} ({st.session_state.rolle})", icon=":material/account_circle:", use_container_width=True):
        st.session_state.aktuelle_seite = "profil"
        st.rerun()

    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

    if st.button("Sitzung beenden", icon=":material/logout:", use_container_width=True):
        st.session_state.eingeloggt = False
        st.session_state.benutzername = ""
        st.session_state.rolle = ""
        st.session_state.aktuelle_seite = "main"
        st.rerun()
    
    st.divider()

    if st.session_state.aktuelle_seite == "main":
        st.markdown("**Schnittstellen-Modus**")
        
        # FIX: Direkte State-Bindung über `key="modus"`. 
        # Keine asynchronen Zwischen-Variablen mehr, die ein Collapsing triggern!
        st.selectbox(
            "Aktiver Modus",
            options=["Web UI Chat Interface", "Dokumenten-Integration (Office Plugin)"],
            key="modus",
            label_visibility="collapsed"
        )
        st.divider()

    st.caption("Version 1.2.0 — Cloud Stable")
    st.caption("Stand: 2026")


# =============================================================================
# ABSCHNITT 6: HEADER
# =============================================================================
st.markdown(
    '<div class="wms-header">'
    '<span class="icon">local_hospital</span>'
    '<span><strong>KOMM Ambulante Dienste e.V.</strong> &nbsp;|&nbsp; Wissensmanagementsystem</span>'
    '</div>',
    unsafe_allow_html=True,
)

# =============================================================================
# ABSCHNITT 7: ROUTING (Profil oder WMS)
# =============================================================================

if st.session_state.aktuelle_seite == "profil":
    st.markdown("### :material/manage_accounts: Benutzerprofil & Einstellungen")
    st.markdown(
        "<p style='color: var(--text-grau); margin-bottom: 2rem;'>"
        "Verwalten Sie hier Ihre persönlichen Daten, Sicherheitsfreigaben und Systemschnittstellen."
        "</p>", unsafe_allow_html=True
    )
    
    if st.button("Zurück zum WMS Dashboard", icon=":material/arrow_back:"):
        st.session_state.aktuelle_seite = "main"
        st.rerun()
    
    st.markdown("---")

    col_prof1, col_prof2 = st.columns(2)

    with col_prof1:
        with st.container(border=True):
            st.markdown('<div class="onto-titel"><span class="icon">badge</span> Persönliche Daten</div>', unsafe_allow_html=True)
            st.markdown('<div class="profil-header-label">Vollständiger Name</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="profil-header-wert">{st.session_state.benutzername}</div>', unsafe_allow_html=True)
            st.markdown('<div class="profil-header-label">Organisatorische Zuordnung</div>', unsafe_allow_html=True)
            st.markdown('<div class="profil-header-wert">Zentrale Dienste (Bockenheim)</div>', unsafe_allow_html=True)
            st.markdown('<div class="profil-header-label">Dienstliche E-Mail</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="profil-header-wert">{st.session_state.benutzername.lower()}@komm-ev.de</div>', unsafe_allow_html=True)

    with col_prof2:
        with st.container(border=True):
            st.markdown('<div class="onto-titel"><span class="icon">security</span> Sicherheit & Autorisierung</div>', unsafe_allow_html=True)
            st.markdown('<div class="profil-header-label">Systemrolle (RBAC)</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="profil-header-wert">{st.session_state.rolle}</div>', unsafe_allow_html=True)
            st.markdown('<div class="profil-header-label">Zugriffslevel</div>', unsafe_allow_html=True)
            if st.session_state.rolle == "Administrator":
                st.markdown('<div class="profil-header-wert"><span class="badge badge-ok"><span class="icon" style="font-size:14px;">check_circle</span> Vollzugriff (Tier 1)</span></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="profil-header-wert"><span class="badge badge-neutral"><span class="icon" style="font-size:14px;">info</span> Standardzugriff (Tier 3)</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="profil-header-label">Letzter Login</div>', unsafe_allow_html=True)
            st.markdown('<div class="profil-header-wert">Heute, 08:14 Uhr (IP: 192.168.10.45)</div>', unsafe_allow_html=True)

else:
    if st.session_state.modus == "Web UI Chat Interface":
        ist_admin = (st.session_state.rolle == "Administrator")

        # ULTIMATIVE RETTUNG: Explizite Vergabe von statischen Keys für st.tabs.
        # Damit weiß das React-DOM im Browser bei JEDEM Dropdown-Wechsel exakt, welcher Tab aktiv ist.
        if ist_admin:
            tab_chat, tab_ticket, tab_onto, tab_regeln, tab_ticket_admin, tab_metriken = st.tabs([
                ":material/forum: Wissensabfrage",
                ":material/support_agent: Support",
                ":material/account_tree: Ontologie",
                ":material/rule: Regelerkennung",
                ":material/confirmation_number: Tickets",
                ":material/analytics: Metriken",
            ], key="komm_wms_admin_tabs")
        else:
            tab_chat, tab_ticket = st.tabs([
                ":material/forum: Wissensabfrage", 
                ":material/support_agent: Support"
            ], key="komm_wms_user_tabs")

        # --- TAB: WISSENSABFRAGE ---
        with tab_chat:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                "<p style='color: var(--text-grau); margin-bottom: 2rem;'>"
                "Stellen Sie eine natürlichsprachliche Frage zu Pflegeleistungen, Abrechnungsregeln "
                "oder internen Verfahrensrichtlinien."
                "</p>", unsafe_allow_html=True
            )

            st.markdown("**Nutzer haben oft gefragt – anklicken zum Abrufen:**")
            col_b1, col_b2, col_b3 = st.columns(3)
            bsp_keys = list(BEISPIELFRAGEN.keys())

            for col, key in zip([col_b1, col_b2, col_b3], bsp_keys):
                with col:
                    if st.button(key, key=f"bsp_{key}", icon=":material/lightbulb:", use_container_width=True):
                        eintrag = {
                            "frage": BEISPIELFRAGEN[key]["frage_voll"],
                            "antwort": BEISPIELFRAGEN[key]["antwort"],
                        }
                        st.session_state.chat_verlauf.append(eintrag)
                        st.rerun()

            st.markdown("---")

            if not st.session_state.chat_verlauf:
                st.info("Noch keine Anfragen im aktuellen Verlauf vorhanden. Wählen Sie eine der oberen Beispielfragen oder tippen Sie einen Freitext ein.")
            else:
                verlauf = st.session_state.chat_verlauf
                for idx in range(len(verlauf)):
                    eintrag = verlauf[idx]
                    fb_key = f"fb_{idx}"

                    st.markdown(f"""
                    <div class="chat-row-user">
                        <div class="msg-user">
                            <div class="msg-label label-user"><span class="icon" style="font-size:14px;">person</span> Ihre Anfrage</div>
                            {eintrag["frage"]}
                        </div>
                        <div class="chat-avatar avatar-user"><span class="icon">person</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="chat-row-system">
                        <div class="chat-avatar avatar-system"><span class="icon">smart_toy</span></div>
                        <div class="msg-system">
                            <div class="msg-label label-system"><span class="icon" style="font-size:14px;">verified</span> Systemantwort (Validiert)</div>
                            {eintrag["antwort"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    akt_fb = st.session_state.feedback.get(fb_key)

                    if akt_fb is None:
                        col_p, col_n, col_leer = st.columns([1.5, 2, 5])
                        with col_p:
                            if st.button("Hilfreich", key=f"pos_{idx}", icon=":material/thumb_up:"):
                                st.session_state.feedback[fb_key] = "positiv"
                                st.rerun()
                        with col_n:
                            if st.button("Verbesserungsbedarf", key=f"neg_{idx}", icon=":material/thumb_down:"):
                                st.session_state.feedback[fb_key] = "negativ"
                                st.rerun()

                    elif akt_fb == "positiv":
                        st.success("Feedback erfolgreich gespeichert: Antwort war hilfreich.")

                    elif akt_fb == "negativ":
                        st.warning("Wir danken für das Feedback. Bitte konkretisieren Sie den Bedarf:")
                        with st.form(key=f"vb_form_{idx}", clear_on_submit=True):
                            vb_text = st.text_area(
                                "Konstruktiver Vorschlag",
                                key=f"vb_text_{idx}",
                                height=80,
                                label_visibility="collapsed",
                                placeholder="Was hat gefehlt oder war unpräzise?",
                            )
                            einreichen = st.form_submit_button("Vorschlag einreichen", icon=":material/send:")
                        if einreichen:
                            st.session_state.feedback[fb_key] = "eingereicht"
                            st.session_state.eingereichtes_feedback.append(vb_text)
                            st.rerun()

                    elif akt_fb == "eingereicht":
                        st.info("Ihr Optimierungsvorschlag wurde eingereicht und wird administrativ geprüft.")

                    st.markdown("<hr>", unsafe_allow_html=True)

            with st.form(key="freitext_form", clear_on_submit=True):
                freitext = st.text_area(
                    "Ihre Frage",
                    placeholder="Geben Sie hier Ihr Anliegen ein...",
                    height=90,
                    label_visibility="collapsed",
                )
                
                col_btn, col_modus, col_space = st.columns([1.5, 2.5, 6])
                with col_btn:
                    absenden = st.form_submit_button("Senden", icon=":material/send:")
                with col_modus:
                    ki_modi = [
                        "Ausgewogen (Standard)",
                        "Ressourcenschonend (Eco)",
                        "Analytisch (Deep-Thinking)"
                    ]
                    neuer_ki_modus = st.selectbox(
                        "KI-Verarbeitungsmodus",
                        options=ki_modi,
                        index=ki_modi.index(st.session_state.ki_modus) if st.session_state.ki_modus in ki_modi else 0,
                        label_visibility="collapsed"
                    )

            if absenden and freitext.strip():
                st.session_state.ki_modus = neuer_ki_modus
                
                if "Eco" in st.session_state.ki_modus:
                    warp = 1.0 
                    lade_text = '<span class="icon">energy_savings_leaf</span> Eco-Modus aktiv: Schnelle Verarbeitung läuft ...'
                elif "Deep-Thinking" in st.session_state.ki_modus:
                    warp = 3.5
                    lade_text = '<span class="icon">psychology</span> Analytischer Modus: Tiefgreifende SGB-Prüfung läuft ...'
                else:
                    warp = 2.0
                    lade_text = '<span class="icon">memory</span> Neuro-Symbolische Verarbeitung läuft ...'

                lade_platzhalter = st.empty()
                lade_platzhalter.markdown(f"""
                <div class="loader-container">
                    <div class="loader-text">{lade_text}</div>
                    <div class="modern-loader"></div>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(warp)
                lade_platzhalter.empty()

                eintrag = {
                    "frage": freitext.strip(),
                    "antwort": PLATZHALTER_ANTWORT,
                }
                st.session_state.chat_verlauf.append(eintrag)
                st.rerun()


        # --- TAB: SUPPORT-TICKET ERSTELLEN ---
        with tab_ticket:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                "<p style='color: var(--text-grau); margin-bottom: 2rem;'>"
                "Melden Sie hier inhaltliche Fehler, fehlende SGB-Richtlinien oder technische Anomalien an die Systemadministration. Zum Absenden beide Felder ausfüllen!"
                "</p>", unsafe_allow_html=True
            )

            with st.form(key="ticket_erstellen_form", clear_on_submit=True):
                ticket_titel = st.text_input("Gegenstand der Meldung", placeholder="Kurze und präzise Zusammenfassung...")
                ticket_beschr = st.text_area("Detaillierte Beschreibung", placeholder="Welcher Fehler ist aufgetreten? Welche Information fehlt?", height=120)
                
                col_tbtn, col_tspace = st.columns([2.5, 7.5])
                with col_tbtn:
                    ticket_absenden = st.form_submit_button("Support-Ticket sicher übertragen", icon=":material/send_and_archive:")

            if ticket_absenden:
                if not ticket_titel.strip() or not ticket_beschr.strip():
                    st.error("Bitte füllen Sie sowohl den Titel als auch die Beschreibung aus, bevor Sie das Ticket absenden.", icon=":material/warning:")
                else:
                    neues_ticket = {
                        "id": st.session_state.ticket_counter,
                        "titel": ticket_titel.strip(),
                        "beschreibung": ticket_beschr.strip(),
                        "status": "Offen",
                        "ersteller": f"{st.session_state.benutzername} ({st.session_state.rolle})"
                    }
                    st.session_state.tickets.append(neues_ticket)
                    st.session_state.ticket_counter += 1
                    st.success("Ihr Support-Ticket wurde im System erfasst und an die Administration weitergeleitet.", icon=":material/check_circle:")
               

        # --- ADMINISTRATOR-TABS ---
        if ist_admin:
            
            # --- TAB: ONTOLOGIE ---
            with tab_onto:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    "<p style='color: var(--text-grau); margin-bottom: 2rem;'>"
                    "Übersicht der implementierten Wissensdomänen. Dies ist das Fundament des regelbasierten Reasoners zur Vermeidung von Halluzinationen."
                    "</p>", unsafe_allow_html=True
                )

                col_p, col_a, col_j = st.columns(3)

                with col_p:
                    with st.container(border=True):
                        st.markdown('<div class="onto-titel"><span class="icon">elderly</span> Domäne: Pflege</div>', unsafe_allow_html=True)
                        st.markdown("""
**SGB XI – Pflegeleistungen**
- Pflegegrade 1 bis 5
- Sachleistungen (§ 36)
- Entlastungsbetrag (§ 45b)
- Verhinderungspflege (§ 39)

**Dokumentationsstandards**
- Leistungsnachweise
- Pflegeberichte
- MDK-Vorgaben
""")
                        st.markdown("<br>", unsafe_allow_html=True)
                        with st.expander("🔍 Hinterlegte Axiome einsehen"):
                            st.markdown("""
                            **Axiom P-01 (Exklusivität):** `IF Pflegegrad == 1 THEN LOCK(Sachleistung) AND ALLOW(Entlastungsbetrag)`  
                            *Sichert ab, dass bei Pflegegrad 1 keine unzulässigen Sachleistungen abgerechnet werden.*
                            
                            **Axiom P-02 (Fristen-Eskalation):** `IF Zeit(Leistungserbringung) + 24h < Zeit(Jetzt) AND Status(Doku) == "Offen" THEN TRIGGER(Warnung_PDL)`  
                            *Erzwingt MDK-konforme, tagaktuelle Dokumentation.*
                            """)

                with col_a:
                    with st.container(border=True):
                        st.markdown('<div class="onto-titel"><span class="icon">accessible</span> Domäne: Assistenz</div>', unsafe_allow_html=True)
                        st.markdown("""
**SGB IX – Eingliederungshilfe**
- Persönliche Assistenz
- Teilhabe am Arbeitsleben
- Soziale Teilhabe

**Hilfeplanverfahren**
- Bedarfsermittlung
- Zielvereinbarungen
- Fortschreibung
""")
                        st.markdown("<br>", unsafe_allow_html=True)
                        with st.expander("🔍 Hinterlegte Axiome einsehen"):
                            st.markdown("""
                            **Axiom A-01 (Kausalität Hilfeplan):** `IF NOT EXISTS(Bedarfsermittlung) THEN LOCK(Zielvereinbarung)`  
                            *Stellt sicher, dass keine Maßnahmen ohne vorherige, dokumentierte Bedarfsermittlung geplant werden.*
                            
                            **Axiom A-02 (Ressourcenzuteilung):** `IF Status(Bewilligung) == "Ausstehend" THEN LIMIT(Leistung, Notfallversorgung)`  
                            *Verhindert die Erbringung nicht-gedeckter Leistungen vor Kostenzusage.*
                            """)

                with col_j:
                    with st.container(border=True):
                        st.markdown('<div class="onto-titel"><span class="icon">child_care</span> Domäne: Jugendhilfe</div>', unsafe_allow_html=True)
                        st.markdown("""
**SGB VIII – Leistungen**
- Ambulante Hilfen (§ 27 ff.)
- Sozialpädagogische Familienhilfe
- Erziehungsbeistandschaft

**Datenschutz (Sonderregeln)**
- Schweigepflicht (§ 203 StGB)
- Aufbewahrungsfristen
""")
                        st.markdown("<br>", unsafe_allow_html=True)
                        with st.expander("🔍 Hinterlegte Axiome einsehen"):
                            st.markdown("""
                            **Axiom J-01 (Schutzauftrag § 8a):** `IF Indikator(Kindeswohlgefährdung) == True THEN OVERRIDE(Schweigepflicht) AND REQUIRE(Meldung_Jugendamt)`  
                            *Priorisiert den aktiven Kinderschutz über Standard-Datenschutzvorgaben im Notfall.*
                            
                            **Axiom J-02 (Altersgrenzen):** `IF Alter(Klient) > 21 THEN REQUIRE(Sonderfallprüfung_SGB_VIII)`  
                            *Löst automatische Prüfprozesse für Hilfe für junge Volljährige aus.*
                            """)

                st.markdown("<br>", unsafe_allow_html=True)
                
                with st.container(border=True):
                    st.markdown('<div class="onto-titel"><span class="icon">playlist_add_check</span> Produktiv geschaltete Reasoner-Regeln</div>', unsafe_allow_html=True)
                    st.markdown("Hier sehen Sie alle Axiome, die aus dem Vorschlagswesen administrativ in den active Betrieb übernommen wurden.")
                    
                    alle_regeln_gesamt = REGEL_KANDIDATEN + st.session_state.manuelle_regeln
                    akzeptierte = [r for r in alle_regeln_gesamt if st.session_state.regel_status.get(r["id"]) == "akzeptiert"]
                    
                    if not akzeptierte:
                        st.info("Aktuell wurden noch keine neuen Regeln in den produktiven Reasoner übernommen.")
                    else:
                        st.markdown("<br>", unsafe_allow_html=True)
                        col_rtitel, col_rdatum = st.columns([3, 1])
                        with col_rtitel:
                            st.markdown("**Regeltitel / Axiom-Logik**")
                        with col_rdatum:
                            st.markdown("**Integration**")
                            
                        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
                        
                        for regel in reversed(akzeptierte):
                            col_rtitel, col_rdatum = st.columns([3, 1])
                            with col_rtitel:
                                st.markdown(f"**{regel['titel']}**")
                                LOGIC_DESC = regel['beschreibung']
                                st.caption(f"{LOGIC_DESC}")
                            with col_rdatum:
                                st.markdown('<span class="badge badge-ok"><span class="icon" style="font-size:14px;">bolt</span> Zuletzt hinzugefügt</span>', unsafe_allow_html=True)
                            
                            st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

                st.markdown("---")
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.markdown(f"Aktive logische Axiome: **{METRIKEN['aktive_axiome']}**")
                with col_m2:
                    st.markdown("Ontologie-Version: **1.3.0**")
                with col_m3:
                    st.markdown("Stand der Revision: **07.07.2026**")


            # --- TAB: REGELERKENNUNG ---
            with tab_regeln:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    "<p style='color: var(--text-grau); margin-bottom: 2rem;'>"
                    "Das System schlägt auf Basis von Nutzungsstatistiken neue logische Verknüpfungen vor. Als Administrator verwalten Sie die Übernahme in den produktiven Reasoner."
                    "</p>", unsafe_allow_html=True
                )

                if "manuelle_regeln" not in st.session_state:
                    st.session_state.manuelle_regeln = []

                with st.container(border=True):
                    st.markdown('<div class="onto-titel"><span class="icon">schema</span> Neue Ontologie-Regel erstellen</div>', unsafe_allow_html=True)
                    st.markdown("Definieren Sie hier manuell neue semantische Zusammenhänge (Wenn-Dann-Abfolgen).")
                    
                    with st.form("axiom_form", clear_on_submit=True):
                        regel_titel = st.text_input("Titel der Regel", placeholder="z.B. Abrechnungsregel Sonderfall")
                        
                        col_w, col_b, col_d = st.columns(3)
                        with col_w:
                            entitaet = st.text_input("Wenn (Entität)", placeholder="z.B. Pflegegrad")
                        with col_b:
                            beziehung = st.text_input("Beziehung", placeholder="z.B. ist gleich (=) 1")
                        with col_d:
                            objekt = st.text_input("Dann (Objekt / Aktion)", placeholder="z.B. greift Entlastungsbetrag")
                            
                        submit_axiom = st.form_submit_button("Regel generieren", icon=":material/add_task:")
                        
                        if submit_axiom:
                            if regel_titel.strip() and entitaet.strip() and beziehung.strip() and objekt.strip():
                                neue_id = 100 + len(st.session_state.manuelle_regeln)
                                neue_regel = {
                                    "id": neue_id,
                                    "titel": regel_titel.strip(),
                                    "beschreibung": f"Wenn {entitaet.strip()} {beziehung.strip()}, dann {objekt.strip()}.",
                                    "haeufigkeit": "Manuell erstellt"
                                }
                                st.session_state.manuelle_regeln.append(neue_regel)
                                st.session_state.regel_status[neue_id] = None 
                                
                                st.success("Neue Regel erfolgreich zur Liste hinzugefügt.")
                                st.rerun()
                            else:
                                st.error("Bitte füllen Sie alle vier Felder aus, um die Regel zu generieren.", icon=":material/warning:")
                
                st.markdown("---")

                alle_regeln = REGEL_KANDIDATEN + st.session_state.manuelle_regeln

                for regel in alle_regeln:
                    rid = regel["id"]
                    status = st.session_state.regel_status[rid]

                    with st.container(border=True):
                        col_info, col_btn = st.columns([4, 1.5])

                        with col_info:
                            st.markdown(f"**{regel['titel']}**")
                            st.markdown(regel["beschreibung"])
                            
                            if "Manuell" in str(regel['haeufigkeit']):
                                st.caption("Evidenz: Manuell durch Administrator erstellt")
                            else:
                                st.caption(f"Statistische Evidenz: Abgeleitet aus {regel['haeufigkeit']} Interaktionen")

                            if status == "akzeptiert":
                                st.markdown('<span class="badge badge-ok"><span class="icon" style="font-size:14px;">check</span> Freigegeben</span>', unsafe_allow_html=True)
                            elif status == "abgelehnt":
                                st.markdown('<span class="badge badge-nein"><span class="icon" style="font-size:14px;">close</span> Verworfen</span>', unsafe_allow_html=True)

                        with col_btn:
                            if status is None:
                                if st.button("Axiom freigeben", key=f"akz_{rid}", icon=":material/check:", use_container_width=True):
                                    st.session_state.regel_status[rid] = "akzeptiert"
                                    st.rerun()
                                st.markdown("<br>", unsafe_allow_html=True)
                                if st.button("Axiom verwerfen", key=f"abl_{rid}", icon=":material/close:", use_container_width=True):
                                    st.session_state.regel_status[rid] = "abgelehnt"
                                    st.rerun()
                            else:
                                st.markdown("**Status: Geprüft**")


            # --- TAB: TICKET-VERWALTUNG (ADMIN BEREICH) ---
            with tab_ticket_admin:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    "<p style='color: var(--text-grau); margin-bottom: 2rem;'>"
                    "Zentrale Verwaltung aller Support-Eskalationen aus dem Mitarbeiterstamm. "
                    "Änderungen am Status werden sofort live übernommen."
                    "</p>", unsafe_allow_html=True
                )

                if not st.session_state.tickets:
                    st.info("Das Ticket-System verzeichnet aktuell keine offenen Vorgänge.")
                else:
                    for tk in reversed(st.session_state.tickets):
                        auswahl_key = f"select_{tk['id']}"
                        
                        with st.container(border=True):
                            col_t1, col_t2 = st.columns([3, 1.2])
                            
                            with col_t1:
                                st.markdown(f"**Vorgang #{tk['id']} | {tk['titel']}**")
                                st.markdown(f"{tk['beschreibung']}")
                                st.caption(f"Gemeldet von: {tk['ersteller']}")

                                if tk['status'] == "Offen":
                                    st.markdown('<span class="badge badge-nein">📋 STATUS: OFFEN</span>', unsafe_allow_html=True)
                                elif tk['status'] == "In Bearbeitung":
                                    st.markdown('<span class="badge badge-neutral">⏳ STATUS: IN BEARBEITUNG</span>', unsafe_allow_html=True)
                                else:
                                    st.markdown('<span class="badge badge-ok">✅ STATUS: GESCHLOSSEN</span>', unsafe_allow_html=True)

                            with col_t2:
                                status_optionen = ["Offen", "In Bearbeitung", "Geschlossen"]
                                
                                # SICHERER INTERAKTIONS-FLOW: Wir nutzen den legalen `on_change` Callback.
                                # Streamlit wickelt die Änderung reaktiv ab, ohne die Tabs kollabieren zu lassen.
                                st.selectbox(
                                    "Status direkt ändern:",
                                    options=status_optionen,
                                    index=status_optionen.index(tk['status']),
                                    key=auswahl_key,
                                    on_change=sichere_ticket_status_direkt,
                                    args=(tk['id'], auswahl_key)
                                )


            # --- TAB: METRIKEN ---
            with tab_metriken:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    "<p style='color: var(--text-grau); margin-bottom: 2rem;'>"
                    "Telemetrie-Daten und Leistungskennzahlen des On-Premise Betriebs."
                    "</p>", unsafe_allow_html=True
                )

                m1, m2, m3, m4 = st.columns(4)
                
                with m1:
                    with st.container(border=True):
                        st.markdown(f'<div class="metrik-wert">{METRIKEN["serverauslastung_pct"]} %</div>', unsafe_allow_html=True)
                        st.markdown('<div class="metrik-label"><span class="icon" style="font-size:16px;">dns</span> Infrastrukturlast</div>', unsafe_allow_html=True)
                with m2:
                    with st.container(border=True):
                        st.markdown(f'<div class="metrik-wert">{METRIKEN["antwortlatenz_ms"]} ms</div>', unsafe_allow_html=True)
                        st.markdown('<div class="metrik-label"><span class="icon" style="font-size:16px;">timer</span> Ø Inferenzzeit</div>', unsafe_allow_html=True)
                with m3:
                    with st.container(border=True):
                        st.markdown(f'<div class="metrik-wert">{METRIKEN["maskierte_pii"]:,}</div>'.replace(",", "."), unsafe_allow_html=True)
                        st.markdown('<div class="metrik-label"><span class="icon" style="font-size:16px;">policy</span> Gefilterte PII</div>', unsafe_allow_html=True)
                with m4:
                    with st.container(border=True):
                        st.markdown(f'<div class="metrik-wert">{METRIKEN["anfragen_heute"]}</div>', unsafe_allow_html=True)
                        st.markdown('<div class="metrik-label"><span class="icon" style="font-size:16px;">forum</span> Anfragen heute</div>', unsafe_allow_html=True)

                st.markdown("---")

                col_fp, col_fn, col_bars = st.columns([1, 1, 3])

                with col_fp:
                    st.markdown(f"**Positives Signal:** {METRIKEN['positives_feedback_pct']} %")
                with col_fn:
                    st.markdown(f"**Optimierungsbedarf:** {METRIKEN['negatives_feedback_pct']} %")
                with col_bars:
                    st.markdown("Akzeptanzrate:")
                    st.progress(METRIKEN["positives_feedback_pct"] / 100)

                st.markdown("---")

                st.markdown("**Eingereichte Freitext-Rückmeldungen der Belegschaft:**")
                if not st.session_state.eingereichtes_feedback:
                    st.info("Aktuell liegen keine manuellen Nutzer-Evaluationen vor.")
                else:
                    for fbt in reversed(st.session_state.eingereichtes_feedback):
                        with st.container(border=True):
                            st.markdown(f'<span class="icon" style="color:var(--text-grau); margin-right:8px; vertical-align: middle;">chat_bubble</span> {fbt}', unsafe_allow_html=True)


    # -----------------------------------------------------------------------
    # MODUS B: DOKUMENTEN-INTEGRATION (Office Plugin)
    # -----------------------------------------------------------------------
    elif st.session_state.modus == "Dokumenten-Integration (Office Plugin)":

        st.markdown("### :material/description: Dokumenten-Integration – Office Plugin")

        st.markdown(
            '<div class="disclaimer">'
            '<span class="icon" style="color:#f59e0b; font-size:28px;">warning</span>'
            '<div>Architektonischer Vorbehalt: Diese Funktion theoretisiert die geplante Endnutzer-Integration. '
            'Eine operative Bereitstellung erfolgt nach erfolgreicher Konfiguration der internen API-Gateways.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")

        col_dok, col_panel = st.columns([2, 1])

        with col_dok:
            st.markdown("**Simuliertes Dokument: Pflegeeinsatzprotokoll**")
            st.text_area(
                "Dokumentinhalt",
                value=(
                    "KOMM Ambulante Dienste e.V.\n"
                    "Pflegeeinsatzprotokoll\n"
                    "\n"
                    "Datum:           14.06.2026\n"
                    "Mitarbeiter/in:  [geschwärzt – PII]\n"
                    "Klient/in:       [geschwärzt – PII]\n"
                    "Pflegegrad:      2\n"
                    "\n"
                    "Erbrachte Leistungen:\n"
                    "  - Grundpflege (Körperpflege, Ankleiden)\n"
                    "  - Medikamentengabe nach ärztlicher Anordnung\n"
                    "  - Mobilisation und Sturzprävention\n"
                    "\n"
                    "Besonderheiten / Abweichungen vom Hilfeplan:\n"
                    "  Keine Abweichungen festgestellt.\n"
                    "\n"
                    "Nächster Einsatz: 15.06.2026, 08:00 Uhr\n"
                    "\n"
                    "Unterschrift: ___________________________________"
                ),
                height=380,
                disabled=True,
                label_visibility="collapsed",
            )

        with col_panel:
            with st.container(border=True):
                st.markdown('<div class="onto-titel"><span class="icon">neurology</span> WMS Systemassistenz</div>', unsafe_allow_html=True)

                st.markdown("**Extrahierte Parameter:**")
                st.markdown("- Pflegegrad 2  \n- Grundpflege  \n- Medikamentengabe")

                st.markdown("---")

                st.markdown("**Korrelierte Richtlinien:**")
                st.markdown(
                    "1. Abrechnungsregeln Pflegegrad 2 (§ 36 SGB XI)  \n"
                    "2. Dokumentationsstandards MDK  \n"
                    "3. Protokollierungspflicht Medikamente"
                )

                st.markdown("---")

                if st.button("Richtlinie einsehen", icon=":material/visibility:", use_container_width=True):
                    st.info("Der direkte Dokumenten-Abruf ist in der Sandbox-Umgebung deaktiviert.")

                if st.button("Compliance-Scan ausführen", icon=":material/fact_check:", use_container_width=True):
                    st.info("Das Compliance-Modul benötigt die Freischaltung der REST-Schnittstellen.")

                st.markdown("---")
                st.caption("Verbindungsstatus: API Offline (Simulation)")