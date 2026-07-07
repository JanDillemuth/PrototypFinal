# =============================================================================
# app.py – KOMM Ambulante Dienste e.V. | Wissensmanagementsystem (WMS)
# Modulare & Cloud-Stabile Version (Proof of Concept)
# =============================================================================
# Ausführung: streamlit run app.py
# =============================================================================

import time
import os
import base64
import streamlit as st

# --- 1. SEITENKONFIGURATION ---
st.set_page_config(
    page_title="KOMM WMS – Wissensmanagementsystem",
    page_icon=":material/health_and_safety:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. STATISCHE DATEN & MOCKS ---
BENUTZER_DATENBANK = {
    "bilal": {"name": "Bilal", "rolle": "Nutzer", "abteilung": "Ambulante Pflege"},
    "jan": {"name": "Jan", "rolle": "Nutzer", "abteilung": "Eingliederungshilfe"},
    "youssef": {"name": "Youssef", "rolle": "Nutzer", "abteilung": "Zentrale Dienste"},
    "farhad": {"name": "Farhad", "rolle": "Nutzer", "abteilung": "Jugendhilfe"},
    "weinß": {"name": "Weinß", "rolle": "Administrator", "abteilung": "Systemadministration"}
}

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

PLATZHALTER_ANTWORT = "Hier würde dann die präzise Antwort des Systems stehen, basierend auf den abgerufenen Richtlinien des Vereins."

REGEL_KANDIDATEN = [
    {"id": 1, "titel": "Abrechnungsregel Pflegegrad 1", "beschreibung": "Wenn Pflegegrad = 1, dann Abrechnung ausschließlich über Entlastungsbetrag (§ 45b SGB XI).", "haeufigkeit": 14},
    {"id": 2, "titel": "Dokumentationsfrist-Eskalation", "beschreibung": "Wenn Dokumentationszeitpunkt > 24 h nach Leistungserbringung, dann automatische PDL-Meldung.", "haeufigkeit": 9},
]

METRIKEN = {"serverauslastung_pct": 34, "antwortlatenz_ms": 187, "maskierte_pii": 1243, "positives_feedback_pct": 78, "negatives_feedback_pct": 22, "anfragen_heute": 57, "aktive_axiome": 12}


# --- 3. CORE STYLE ENGINES (CSS & UTILS) ---
def load_corporate_design():
    """Lädt das Corporate Design. Verhindert Layout-Crashes auf Streamlit Cloud."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,1,0');
        
        html, body, p, h1, h2, h3, h4, h5, h6, label {
            font-family: "-apple-system", BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        }
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
        .icon { font-family: 'Material Symbols Rounded' !important; font-size: 24px; display: inline-block; vertical-align: middle; }
        
        .stButton > button, .stFormSubmitButton > button {
            background: linear-gradient(135deg, var(--komm-gruen), #1a9660) !important;
            color: white !important; border: none !important; border-radius: var(--radius-klein) !important;
            font-weight: 600 !important; box-shadow: var(--schatten-gruen) !important;
        }
        .btn-sekundaer > button { background: white !important; color: var(--text-dunkel) !important; border: 1px solid #e0e0e0 !important; box-shadow: none !important; }
        
        .wms-header { background: linear-gradient(135deg, var(--komm-gruen), #1a9660); color: white; padding: 1.2rem 1.8rem; border-radius: var(--radius-klein); margin-bottom: 2rem; font-weight: 600; display: flex; align-items: center; gap: 12px; box-shadow: var(--schatten-gruen); }
        .login-container { background: white; border-radius: var(--radius-gross); padding: 3rem 2.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.08); text-align: center; margin-bottom: 2rem; }
        
        /* Modulares Chat-Design */
        .chat-row-user, .chat-row-system { display: flex; align-items: flex-end; margin-bottom: 1.5rem; gap: 12px; }
        .chat-row-user { justify-content: flex-end; }
        .chat-row-system { justify-content: flex-start; }
        .chat-avatar { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
        .avatar-user { background-color: var(--komm-gruen-hell); color: var(--komm-gruen); }
        .avatar-system { background-color: #1a9660; color: white; box-shadow: var(--schatten-gruen); }
        .msg-user { background-color: var(--komm-gruen); color: white; padding: 1.2rem 1.4rem; border-radius: 24px 24px 4px 24px; max-width: 75%; box-shadow: var(--schatten-gruen); }
        .msg-system { background-color: var(--bg-chat-system); border: 1px solid #eaf0ed; color: var(--text-dunkel); padding: 1.2rem 1.4rem; border-radius: 24px 24px 24px 4px; max-width: 75%; box-shadow: var(--schatten-weich); }
        .msg-label { font-size: 0.75rem; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 4px; }
        .label-user { color: rgba(255,255,255,0.8); }
        .label-system { color: var(--komm-gruen); }
        
        /* Cloud-Safe Card Styling (Klasse statt Test-ID) */
        .wms-card { padding: 1.5rem; background: white; border-radius: var(--radius-klein); border: 1px solid #eaeaea; box-shadow: var(--schatten-weich); margin-bottom: 1rem; }
        .onto-titel { font-size: 1.1rem; font-weight: 700; color: var(--komm-gruen); margin-bottom: 1rem; display: flex; align-items: center; gap: 8px; }
        .badge { display: inline-flex; align-items: center; gap: 4px; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
        .badge-ok { background-color: var(--komm-gruen-hell); color: var(--komm-gruen); }
        .badge-nein { background-color: #fee2e2; color: #b91c1c; }
        .badge-neutral { background-color: #f3f4f6; color: #4b5563; }
        
        .metrik-wert { font-size: 2rem; font-weight: 800; color: var(--komm-gruen); text-align: center; }
        .metrik-label { font-size: 0.85rem; color: var(--text-grau); font-weight: 600; text-transform: uppercase; text-align: center; margin-top: 0.4rem; }
        .disclaimer { background-color: #fff8e1; border-left: 4px solid #f59e0b; padding: 1.2rem; border-radius: var(--radius-klein); display: flex; align-items: center; gap: 12px; }
        
        /* Loader */
        .loader-container { margin: 1rem 0; padding: 1.5rem; background: white; border-radius: var(--radius-klein); border: 1px solid #eaeaea; text-align: center; }
        .modern-loader { width: 100%; height: 6px; background-color: var(--komm-gruen-hell); border-radius: 10px; overflow: hidden; position: relative; }
        .modern-loader::after { content: ''; position: absolute; left: -50%; height: 100%; width: 50%; background-color: var(--komm-gruen); animation: slide 1.2s infinite ease-in-out; }
        @keyframes slide { 0% { left: -50%; } 100% { left: 100%; } }
        
        /* Tooltips */
        .onto-ref { display: inline-flex; align-items: center; justify-content: center; background-color: var(--komm-gruen-hell); color: var(--komm-gruen); border-radius: 50%; width: 18px; height: 18px; font-size: 10px; font-weight: 800; cursor: pointer; margin: 0 4px; position: relative; vertical-align: super; }
        .onto-ref .tooltiptext { visibility: hidden; width: 260px; background-color: var(--text-dunkel); color: white; text-align: left; border-radius: 8px; padding: 10px 14px; position: absolute; z-index: 9999; bottom: 140%; left: 50%; transform: translateX(-50%); opacity: 0; transition: opacity 0.3s; font-weight: normal; font-size: 0.85rem; }
        .onto-ref:hover .tooltiptext { visibility: visible; opacity: 1; }
    </style>
    """, unsafe_allow_html=True)

def get_logo_base64():
    if os.path.exists("Komm.png"):
        with open("Komm.png", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None


# --- 4. SESSION STATE INITIALISIERUNG ---
def init_session_state():
    defaults = {
        "eingeloggt": False,
        "benutzername": "",
        "rolle": "",
        "abteilung": "",
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
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# --- 5. CALLBACK ACTIONS (STATE MANIPULATION) ---
def action_update_ticket_status(ticket_id, select_key):
    """Callback-Mechanismus: Aktualisiert Ticket-Status reaktiv und cloud-stabil vor dem Renderzyklus."""
    neuer_status = st.session_state[select_key]
    for tk in st.session_state.tickets:
        if tk["id"] == ticket_id:
            tk["status"] = neuer_status
            break

def action_select_sample_question(key):
    st.session_state.chat_verlauf.append({
        "frage": BEISPIELFRAGEN[key]["frage_voll"],
        "antwort": BEISPIELFRAGEN[key]["antwort"]
    })


# --- 6. MODULARE UI KOMPONENTEN (VIEWS) ---

def view_login_screen(logo_b64):
    """Ausgelagerte Login-Schnittstelle."""
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if logo_b64:
            st.markdown(f'<div class="login-container"><img src="data:image/png;base64,{logo_b64}" style="max-width: 250px; margin-bottom: 1rem;"><p style="color: var(--text-grau); font-weight:600;">Wissensmanagementsystem</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="login-container"><span class="icon" style="font-size:48px; color:var(--komm-gruen);">shield_person</span><h2>KOMM e.V.</h2><p style="color: var(--text-grau);">Wissensmanagementsystem</p></div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            user_input = st.text_input("Benutzername", placeholder="Registrierten Namen eingeben...")
            st.text_input("Passwort", type="password", placeholder="••••••••")
            submit = st.form_submit_button("System betreten", use_container_width=True)
            
            if submit:
                clean_name = user_input.strip().lower()
                if clean_name in BENUTZER_DATENBANK:
                    user_data = BENUTZER_DATENBANK[clean_name]
                    st.session_state.eingeloggt = True
                    st.session_state.benutzername = user_data["name"]
                    st.session_state.rolle = user_data["rolle"]
                    st.session_state.abteilung = user_data["abteilung"]
                    st.session_state.aktuelle_seite = "main"
                    st.rerun()
                else:
                    st.error("Zugriff verweigert. Gültige Demo-Nutzer: Bilal, Jan, Youssef, Farhad oder Weinß")
        st.markdown("<p style='font-size: 0.8rem; color: #95a5a6; text-align: center;'>Rollen-Sandbox: Weinß = Administrator | Alle anderen = Standard-Nutzer</p>", unsafe_allow_html=True)

def view_sidebar(logo_b64):
    """Modulare Navigations-Sidebar."""
    with st.sidebar:
        if logo_b64:
            st.markdown(f'<div style="text-align: center; margin: 1rem 0;"><img src="data:image/png;base64,{logo_b64}" style="max-width: 80%;"><p style="color: var(--text-grau); font-size: 0.85rem; font-weight: 600; margin-top:0.5rem;">WMS Prototyp</p></div>', unsafe_allow_html=True)
        st.divider()
        
        if st.button(f"{st.session_state.benutzername} ({st.session_state.rolle})", icon=":material/account_circle:", use_container_width=True):
            st.session_state.aktuelle_seite = "profil"
            st.rerun()
            
        st.markdown('<div class="btn-sekundaer">', unsafe_allow_html=True)
        if st.button("Sitzung beenden", icon=":material/logout:", use_container_width=True):
            st.session_state.eingeloggt = False
            st.session_state.aktuelle_seite = "main"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.divider()
        
        if st.session_state.aktuelle_seite == "main":
            st.markdown("**Schnittstellen-Modus**")
            modi = ["Web UI Chat Interface", "Dokumenten-Integration (Office Plugin)"]
            st.session_state.modus = st.selectbox("Aktiver Modus", options=modi, index=modi.index(st.session_state.modus), label_visibility="collapsed")

def tab_view_knowledge_base():
    """Modul für Wissensabfrage & Chat-Historie."""
    st.markdown("<br><p style='color: var(--text-grau);'>Stellen Sie Fragen zu Pflegeleistungen, Abrechnungsregeln oder internen Handbüchern.</p>", unsafe_allow_html=True)
    
    st.markdown("**Häufige Suchanfragen:**")
    cols = st.columns(len(BEISPIELFRAGEN))
    for col, key in zip(cols, BEISPIELFRAGEN.keys()):
        with col:
            st.button(key, key=f"btn_q_{key}", icon=":material/lightbulb:", use_container_width=True, on_click=action_select_sample_question, args=(key,))
            
    st.divider()
    
    if not st.session_state.chat_verlauf:
        st.info("Noch keine Anfragen dokumentiert. Nutzen Sie ein Schnellstart-Thema oder das Freitextfeld.")
    else:
        for idx, eintrag in enumerate(st.session_state.chat_verlauf):
            st.markdown(f'<div class="chat-row-user"><div class="msg-user"><div class="msg-label label-user"><span class="icon" style="font-size:14px;">person</span> Ihre Anfrage</div>{eintrag["frage"]}</div><div class="chat-avatar avatar-user"><span class="icon">person</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-row-system"><div class="chat-avatar avatar-system"><span class="icon">smart_toy</span></div><div class="msg-system"><div class="msg-label label-system"><span class="icon" style="font-size:14px;">verified</span> Systemantwort</div>{eintrag["antwort"]}</div></div>', unsafe_allow_html=True)
            
            fb_key = f"fb_{idx}"
            if st.session_state.feedback.get(fb_key) is None:
                c1, c2, _ = st.columns([1.5, 2, 5])
                if c1.button("Hilfreich", key=f"pos_{idx}", icon=":material/thumb_up:"):
                    st.session_state.feedback[fb_key] = "positiv"
                    st.rerun()
                if c2.button("Optimierungsbedarf", key=f"neg_{idx}", icon=":material/thumb_down:"):
                    st.session_state.feedback[fb_key] = "negativ"
                    st.rerun()
            elif st.session_state.feedback[fb_key] == "positiv":
                st.success("Feedback vermerkt: Antwort war präzise.")
            else:
                st.info("Verbesserungsvorschlag administrativ erfasst.")
            st.markdown("<hr style='margin:1rem 0;'>", unsafe_allow_html=True)

    with st.form(key="chat_input_form", clear_on_submit=True):
        freitext = st.text_area("Frage formulieren", placeholder="Geben Sie hier Ihr Anliegen ein...", height=80, label_visibility="collapsed")
        cb1, cb2, _ = st.columns([1.5, 2.5, 6])
        senden = cb1.form_submit_button("Senden", icon=":material/send:")
        ki_mode = cb2.selectbox("Modus", ["Ausgewogen (Standard)", "Ressourcenschonend (Eco)", "Analytisch (Deep-Thinking)"], label_visibility="collapsed")
        
    if senden and freitext.strip():
        st.session_state.ki_modus = ki_mode
        l_box = st.empty()
        l_box.markdown('<div class="loader-container"><div class="loader-text"><span class="icon">memory</span> Neuro-symbolische Validierung läuft...</div><div class="modern-loader"></div></div>', unsafe_allow_html=True)
        time.sleep(1.5)
        l_box.empty()
        st.session_state.chat_verlauf.append({"frage": freitext.strip(), "antwort": PLATZHALTER_ANTWORT})
        st.rerun()

def tab_view_support():
    """Modul für die Erstellung von Support-Tickets."""
    st.markdown("<br><p style='color: var(--text-grau);'>Inhaltliche Fehler oder Systemanomalien direkt an die Administration weiterleiten.</p>", unsafe_allow_html=True)
    with st.form("support_ticket_form", clear_on_submit=True):
        titel = st.text_input("Gegenstand der Meldung")
        beschr = st.text_area("Detaillierte Beschreibung")
        if st.form_submit_button("Ticket sicher absenden", icon=":material/send_and_archive:"):
            if titel.strip() and beschr.strip():
                st.session_state.tickets.append({
                    "id": st.session_state.ticket_counter, "titel": titel.strip(), "beschreibung": beschr.strip(),
                    "status": "Offen", "ersteller": f"{st.session_state.benutzername} ({st.session_state.rolle})"
                })
                st.session_state.ticket_counter += 1
                st.success("Support-Ticket erfolgreich im System registriert.")
            else:
                st.error("Bitte füllen Sie alle Pflichtfelder aus.")

def tab_view_admin_tickets():
    """Modul für reaktive Live-Ticketverwaltung (Ohne Formular-Crash)."""
    st.markdown("<br><p style='color: var(--text-grau);'>Live-Statusänderungen ohne störende Button-Bestätigungen.</p>", unsafe_allow_html=True)
    if not st.session_state.tickets:
        st.info("Keine Ticketvorgänge vorhanden.")
    else:
        for tk in reversed(st.session_state.tickets):
            select_key = f"sel_status_{tk['id']}"
            
            # Cloud-Safe HTML rendering blockiert keine Streamlit Layout-Engines
            st.markdown(f"""
            <div class="wms-card">
                <strong>Vorgang #{tk['id']} | {tk['titel']}</strong><br>
                <span style="font-size:0.92rem; color:#34495e;">{tk['beschreibung']}</span><br>
                <span style="font-size:0.8rem; color:var(--text-grau);">Erstellt von: {tk['ersteller']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Badge-Farbsteuerung
            if tk['status'] == "Offen":
                st.markdown('<span class="badge badge-nein">📋 Offen</span>', unsafe_allow_html=True)
            elif tk['status'] == "In Bearbeitung":
                st.markdown('<span class="badge badge-neutral">⏳ In Bearbeitung</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge badge-ok">✅ Geschlossen</span>', unsafe_allow_html=True)
                
            st.selectbox(
                "Status anpassen:", 
                options=["Offen", "In Bearbeitung", "Geschlossen"],
                index=["Offen", "In Bearbeitung", "Geschlossen"].index(tk['status']),
                key=select_key,
                on_change=action_update_ticket_status,
                args=(tk['id'], select_key)
            )
            st.markdown("<br>", unsafe_allow_html=True)

def tab_view_ontology():
    st.markdown("<br><p style='color: var(--text-grau);'>Hinterlegte Axiome und Regelwerke zur Absicherung der LLM-Inferenz.</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    domaenen = [
        ("elderly", "Domäne: Pflege", "SGB XI Richtlinien", "Axiom P-01: PG 1 schließt Sachleistungen strukturell aus."),
        ("accessible", "Domäne: Assistenz", "SGB IX Eingliederungshilfe", "Axiom A-01: Hilfeplanung setzt Bedarfsanalyse voraus."),
        ("child_care", "Domäne: Jugendhilfe", "SGB VIII Leistungen", "Axiom J-01: Schutzauftrag § 8a überschreibt Schweigepflicht im Notfall.")
    ]
    for col, (icon, titel, sub, axiom) in zip([c1, c2, c3], domaenen):
        with col:
            st.markdown(f'<div class="wms-card"><div class="onto-titel"><span class="icon">{icon}</span> {titel}</div><strong>{sub}</strong><br><p style="font-size:0.85rem; color:var(--text-grau);">{axiom}</p></div>', unsafe_allow_html=True)

def tab_view_rules():
    st.markdown("<br><p style='color: var(--text-grau);'>Statistische Evidenzen in harte logische Axiome transformieren.</p>", unsafe_allow_html=True)
    with st.form("rule_generation_form", clear_on_submit=True):
        titel = st.text_input("Titel der Ontologie-Regel")
        e1 = st.text_input("Wenn (Entität)")
        e2 = st.text_input("Dann (Aktion)")
        if st.form_submit_button("Axiom generieren"):
            if titel and e1 and e2:
                st.session_state.manuelle_regeln.append({"id": 99, "titel": titel, "beschreibung": f"Wenn {e1}, dann {e2}."})
                st.success("Regel erzeugt.")
            else:
                st.error("Alle Felder ausfüllen.")

def tab_view_metrics():
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="wms-card"><div class="metrik-wert">{METRIKEN["serverauslastung_pct"]}%</div><div class="metrik-label">Infrastrukturlast</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="wms-card"><div class="metrik-wert">{METRIKEN["antwortlatenz_ms"]}ms</div><div class="metrik-label">Inferenzlatenz</div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="wms-card"><div class="metrik-wert">{METRIKEN["maskierte_pii"]}</div><div class="metrik-label">PII Bereinigungen</div></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="wms-card"><div class="metrik-wert">{METRIKEN["anfragen_heute"]}</div><div class="metrik-label">Anfragen heute</div></div>', unsafe_allow_html=True)

def view_profile_page():
    st.markdown("### :material/manage_accounts: Benutzerprofil & Freigaben")
    if st.button("Zurück zum Dashboard", icon=":material/arrow_back:"):
        st.session_state.aktuelle_seite = "main"
        st.rerun()
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="wms-card"><div class="onto-titel"><span class="icon">badge</span> Mitarbeiterstamm</div>Identität: <b>{st.session_state.benutzername}</b><br>Abteilung: {st.session_state.abteilung}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="wms-card"><div class="onto-titel"><span class="icon">security</span> RBAC Status</div>Berechtigungsebene: <b>{st.session_state.rolle}</b></div>', unsafe_allow_html=True)

def view_office_plugin():
    st.markdown("### :material/description: Dokumenten-Integration (Office Plugin)")
    st.markdown('<div class="disclaimer"><span class="icon" style="color:#f59e0b;">warning</span><div>Architektonische Sandbox-Simulation. API-Anbindung erfolgt On-Premise nach Freigabe der Gateways.</div></div><br>', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.text_area("Simuliertes Word-Protokoll", value="KOMM Ambulante Dienste e.V.\nPflegeprotokoll vom 14.06.2026\n\nKlient: [Verschlüsselt]\nPflegegrad: 2\n\nErbrachte Leistung: Grundpflege.", height=250, disabled=True)
    with c2:
        st.markdown('<div class="wms-card"><strong>WMS Systemassistenz</strong><br>Extrahiert: Pflegegrad 2<br>Compliance: Konform</div>', unsafe_allow_html=True)


# --- 7. CORE APP ROUTER & ORCHESTRATOR ---
def main():
    load_corporate_design()
    init_session_state()
    logo_base64 = get_logo_base64()
    
    # Login Guard
    if not st.session_state.eingeloggt:
        view_login_screen(logo_base64)
        return
        
    # Navigation & Header
    view_sidebar(logo_base64)
    st.markdown('<div class="wms-header"><span class="icon">local_hospital</span><span><strong>KOMM Ambulante Dienste e.V.</strong> &nbsp;|&nbsp; Wissensmanagementsystem</span></div>', unsafe_allow_html=True)
    
    # Routing Logic
    if st.session_state.aktuelle_seite == "profil":
        view_profile_page()
    elif st.session_state.modus != "Web UI Chat Interface":
        view_office_plugin()
    else:
        # Rollenbasierte Tab-Generierung (Vermeidet Überlastung und Verschachtelungsfehler auf Streamlit Cloud)
        if st.session_state.rolle == "Administrator":
            t_chat, t_ticket, t_onto, t_rules, t_admin_tick, t_metrics = st.tabs([
                ":material/forum: Wissensabfrage", ":material/support_agent: Support", 
                ":material/account_tree: Ontologie", ":material/rule: Regelerkennung", 
                ":material/confirmation_number: Tickets", ":material/analytics: Metriken"
            ])
            with t_chat: tab_view_knowledge_base()
            with t_ticket: tab_view_support()
            with t_onto: tab_view_ontology()
            with t_rules: tab_view_rules()
            with t_admin_tick: tab_view_admin_tickets()
            with t_metrics: tab_view_metrics()
        else:
            t_chat, t_ticket = st.tabs([":material/forum: Wissensabfrage", ":material/support_agent: Support"])
            with t_chat: tab_view_knowledge_base()
            with t_ticket: tab_view_support()

if __name__ == "__main__":
    main()