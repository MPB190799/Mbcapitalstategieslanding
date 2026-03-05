#!/usr/bin/env python3
"""
Adds FAQPage JSON-LD schema to blog articles that don't have one yet.
Generates context-aware FAQ questions based on article title and description.
"""

import os
import re
import json

BLOG_DIR = "/home/user/Mbcapitalstategieslanding/blog"
BASE_URL = "https://mbcapitalstrategies.com"

# Skip non-article files
SKIP_FILES = {"styles.css", "styles.min.css", "index.html"}

def get_faq_for_article(title, description, slug):
    """Generate relevant FAQ based on article content."""

    t = title.lower()
    d = description.lower()

    # --- Company stock analyses ---
    company_name = extract_company(title)

    # Mining companies
    if any(k in t for k in ["mining", "gold", "kupfer", "barrick", "bhp", "rio tinto",
                              "glencore", "angloamerican", "anglo american", "fortescue",
                              "vale", "newmont", "fresnillo", "central asia", "exxaro",
                              "thungela", "yancoal", "whitehaven", "valterra", "gerdau",
                              "jiangxi", "b2gold", "indo tambangraya", "suncoke"]):
        return mining_faq(company_name, title, description)

    # Uranium
    if any(k in t for k in ["uran", "uranium", "kazatomprom"]):
        return uranium_faq(company_name, title, description)

    # Energy / Oil & Gas (Upstream)
    if any(k in t for k in ["energie", "energy", "öl", "oil", "gas", "upstream",
                              "eni", "equinor", "petrobras", "woodside", "panoro",
                              "ecopetrol", "cardinal", "devon", "apa ", "aker",
                              "coterra", "repsol", "omv", "oneok", "bp ", "shell",
                              "total", "chevron", "suncor", "cenovus"]):
        return energy_faq(company_name, title, description)

    # Pipeline / Midstream
    if any(k in t for k in ["pipeline", "midstream", "pembina", "tc energy", "enbridge",
                              "mlp", "take-or-pay"]):
        return pipeline_faq(company_name, title, description)

    # Shipping / Tanker / LNG-Carrier
    if any(k in t for k in ["shipping", "tanker", "lng", "carrier", "fleet",
                              "schifffahrt", "avance", "bw lpg", "konsolidierung"]):
        return shipping_faq(company_name, title, description)

    # BDC
    if any(k in t for k in ["bdc", "business development", "newtek", "hercules",
                              "crescent", "blue owl", "debitum"]):
        return bdc_faq(company_name, title, description)

    # Tools / Rechner
    if any(k in t for k in ["rechner", "calculator", "toolbox", "tool", "finanzrechner"]):
        return tool_faq(title, description)

    # Market news
    if any(k in t for k in ["markt-news", "news", "cpi", "februar", "januar"]):
        return news_faq(title, description)

    # Rohstoff-Superzyklus
    if any(k in t for k in ["superzyklus", "rohstoff"]):
        return superzyklus_faq(title, description)

    # General / Travel
    if any(k in t for k in ["vietnam", "airalo", "wise", "reisen", "travel"]):
        return travel_faq(title, description)

    # Dividenden general
    if any(k in t for k in ["dividenden", "dividende", "cashflow", "high yield"]):
        return dividend_faq(title, description)

    # Fallback generic
    return generic_faq(title, description)


def extract_company(title):
    """Extract company name from title like 'Barrick Gold Analyse 2026 – ...'"""
    # Remove common suffixes
    name = re.sub(r'\s+(Analyse|Aktie|analyse|aktie)\s+\d{4}.*', '', title)
    name = re.sub(r'\s*[–—-].*', '', name)
    name = name.strip().rstrip('?!.')
    # Remove emoji
    name = re.sub(r'[^\x00-\x7FäöüÄÖÜß ]', '', name).strip()
    if len(name) > 60:
        name = name[:60]
    return name


def mining_faq(company, title, desc):
    # Extract year
    year = re.search(r'20\d\d', title)
    year = year.group(0) if year else "2026"

    # Extract metals from description
    metals = []
    for m in ["Gold", "Kupfer", "Silber", "Kohle", "Eisenerz", "Platin", "Palladium",
              "Rhodium", "Uran", "Zink", "Aluminium", "Nickel"]:
        if m.lower() in desc.lower():
            metals.append(m)
    metals_str = ", ".join(metals) if metals else "Rohstoffe"

    # Extract dividend info
    div_match = re.search(r'(\d+[\.,]\d+)\s*%', desc)
    div_str = div_match.group(0) if div_match else "attraktive Dividende"

    return [
        {
            "name": f"Was macht {company} und warum ist das Unternehmen für Rohstoffinvestoren interessant?",
            "text": f"{company} ist ein Bergbauunternehmen mit Fokus auf {metals_str}. Im Rohstoff-Superzyklus profitieren Mining-Unternehmen von steigender Nachfrage aus der Energiewende (E-Mobilität, Windkraft, Stromnetzausbau) sowie strukturell steigenden Rohstoffpreisen durch jahrelange Unterinvestition."
        },
        {
            "name": f"Wie hoch ist die Dividende von {company} und wie stabil ist sie?",
            "text": f"{company} zahlt {div_str} an seine Aktionäre. Rohstoff-Dividenden sind oft zyklisch und an den Cashflow gekoppelt. Wichtig sind: Ausschüttungsquote, Verschuldungsgrad und Break-even-Preis. Bei steigenden Rohstoffpreisen können Mining-Unternehmen Sonderdividenden zahlen."
        },
        {
            "name": f"Was sind die größten Risiken bei einem Investment in {company}?",
            "text": f"Hauptrisiken bei Mining-Aktien wie {company}: Rohstoffpreisschwankungen, politische Risiken im Abbauland, steigende Betriebskosten (Energy, Labor), Währungsrisiken sowie regulatorische Änderungen. Diversifikation über mehrere Rohstoffe und Regionen reduziert das Klumpenrisiko."
        },
        {
            "name": f"Wie profitiert {company} vom Rohstoff-Superzyklus {year}?",
            "text": f"Der Rohstoff-Superzyklus ist getrieben durch die Energie- und Mobilitätswende: Kupfer für Elektronetze, Lithium für Batterien, Uran für Kernkraft, Kohle als Brückenenergie. {company} ist im Segment {metals_str} positioniert und profitiert von strukturell steigender Nachfrage bis 2040."
        },
        {
            "name": f"Wie kauft man {company}-Aktien als deutscher Anleger?",
            "text": f"{company}-Aktien sind über deutsche Broker (Trade Republic, Scalable Capital, Consorsbank) über XETRA oder internationale Börsen handelbar. Achten Sie auf Quellensteuerabkommen, Währungsumrechnung und ggf. Doppelbesteuerung je nach Börsenplatz."
        }
    ]


def uranium_faq(company, title, desc):
    year = re.search(r'20\d\d', title)
    year = year.group(0) if year else "2026"
    return [
        {
            "name": f"Was macht {company} und warum ist Uran als Investment interessant?",
            "text": f"{company} ist einer der weltweit führenden Uranproduzenten. Uran erlebt durch den globalen Kernkraft-Renaissance eine strukturelle Nachfrageerholung: Neue Reaktoren in Asien, SMR-Technologie und das Netto-Null-Ziel treiben die Nachfrage langfristig nach oben."
        },
        {
            "name": f"Wie entwickelt sich der Uranpreis und was bedeutet das für {company}?",
            "text": f"Der Uranpreis stieg stark an nach jahrelanger Unterversorgung. Langfristverträge (Utilities) laufen neu und müssen zu höheren Preisen verlängert werden. {company} profitiert als Niedrigkostenproduzent überproportional von steigenden Spotpreisen."
        },
        {
            "name": f"Welche Risiken bestehen bei {company} als Uraninvestment?",
            "text": f"Risiken: geopolitische Abhängigkeit von Kasachstan/Russland, Uranpreisvola, regulatorische Änderungen in der Kernenergiebranche sowie politische Eingriffe in Produktion und Export. Diversifikation über mehrere Uranunternehmen empfehlenswert."
        },
        {
            "name": f"Wie hoch ist die Dividende und wie sieht das Geschäftsmodell aus?",
            "text": f"{company} erzielt Einnahmen aus Uranverkäufen über Spot- und Terminkontrakte. Die Ausschüttungspolitik orientiert sich am freien Cashflow. Mit steigendem Uranpreis verbessern sich Margen und Dividendenpotenzial erheblich."
        }
    ]


def energy_faq(company, title, desc):
    year = re.search(r'20\d\d', title)
    year = year.group(0) if year else "2026"

    div_match = re.search(r'(\d+[\.,]?\d*)\s*%.*(?:dividende|yield)', desc.lower())
    div_str = div_match.group(0) if div_match else "hohe Dividende"

    # FCF-Yield
    fcf_match = re.search(r'fcf[- ]?yield\s*[\d.,]+\s*%', desc.lower())
    fcf_str = fcf_match.group(0).upper() if fcf_match else "starken FCF-Yield"

    return [
        {
            "name": f"Was macht {company} und warum ist das Unternehmen für Dividendeninvestoren interessant?",
            "text": f"{company} ist ein internationales Energie- bzw. Öl & Gas-Unternehmen. Es erzielt Cashflow aus Exploration, Produktion und ggf. Downstream-Aktivitäten. Energieunternehmen bieten oft {div_str} und profitieren von einem {fcf_str}."
        },
        {
            "name": f"Wie hoch ist die Dividende von {company} {year} und wie wird sie finanziert?",
            "text": f"Die Dividende von {company} wird durch den operativen Cashflow und Free Cashflow gedeckt. Entscheidend ist der Break-even-Ölpreis: Liegt er unter $50-60/Barrel, ist die Dividende auch bei niedrigeren Energiepreisen stabil. Quelle und Höhe der Dividende sind in der Analyse detailliert aufgeführt."
        },
        {
            "name": f"Welche Risiken hat ein Investment in {company}?",
            "text": f"Hauptrisiken: Ölpreisverfall (unter Break-even), politische Eingriffe in staatlich kontrollierten Unternehmen, ESG-Druck (Desinvestitionen institutioneller Anleger), Währungsrisiken und regulatorische Änderungen. Upstream-Unternehmen sind direkt dem Rohstoffpreisrisiko ausgesetzt."
        },
        {
            "name": f"Wie profitiert {company} von hohen Energiepreisen?",
            "text": f"Jeder Dollar Ölpreisanstieg über den Break-even erhöht den freien Cashflow überproportional. {company} kann bei hohen Öl-/Gaspreisen Schulden abbauen, Dividenden erhöhen oder Aktienrückkäufe durchführen. Das macht Upstream-Aktien zu einem natürlichen Hedge gegen Inflation."
        },
        {
            "name": f"Wie kauft man {company}-Aktien als Anleger in Deutschland?",
            "text": f"Aktien von {company} sind über gängige deutsche Broker (Trade Republic, Scalable, Consorsbank) handelbar. Achten Sie auf Quellensteuer je nach Herkunftsland des Unternehmens, Währungsrisiko (USD, BRL, NOK etc.) und das Doppelbesteuerungsabkommen."
        }
    ]


def pipeline_faq(company, title, desc):
    year = re.search(r'20\d\d', title)
    year = year.group(0) if year else "2026"
    return [
        {
            "name": f"Was macht {company} und wie funktioniert das Pipeline-Geschäftsmodell?",
            "text": f"{company} betreibt Pipeline- und Midstream-Infrastruktur für Transport und Speicherung von Öl, Gas oder LNG. Das Take-or-Pay-Modell sichert planbare Einnahmen unabhängig vom Rohstoffpreis: Kunden zahlen für die Kapazität, egal ob sie sie nutzen oder nicht."
        },
        {
            "name": f"Wie hoch und wie stabil ist die Dividende von {company}?",
            "text": f"Pipeline-Unternehmen wie {company} sind bekannt für stabile und wachsende Dividenden. Die Ausschüttungen werden durch langfristige Take-or-Pay-Verträge gedeckt. Dividendenrenditen von 5–9 % sind in diesem Sektor typisch. Ausschüttungsquoten von 60–80 % des distributable Cash Flows gelten als gesund."
        },
        {
            "name": f"Welche Risiken bestehen bei einem Investment in {company}?",
            "text": f"Risiken bei Pipeline-Aktien: Regulierungsänderungen (Tariflimits), Refinanzierungsrisiko bei hoher Verschuldung, Kreditwürdigkeit der Kunden (Upstream-Unternehmen), sowie politische Risiken (Genehmigungen, ESG). Zinsanstiege wirken negativ auf Bewertung durch höhere Kapitalkosten."
        },
        {
            "name": f"Was ist der Unterschied zwischen MLPs und regulären Pipeline-Aktien?",
            "text": f"MLPs (Master Limited Partnerships) sind steuerlich auf Partnerschaftsebene nicht besteuert, schütten aber den Großteil des Cashflows aus. Für deutsche Anleger entstehen Komplexitäten bei der K-1-Besteuerung. Reguläre Corporations wie {company} sind für internationale Anleger oft einfacher steuerlich zu handhaben."
        },
        {
            "name": f"Wie kauft man {company}-Aktien und was sollte man steuerlich beachten?",
            "text": f"{company}-Aktien sind über deutsche Broker handelbar. Achten Sie auf die steuerliche Struktur (MLP vs. Corporation), Quellensteuer auf Dividenden aus Kanada oder den USA sowie das Doppelbesteuerungsabkommen Deutschland-Kanada / Deutschland-USA."
        }
    ]


def shipping_faq(company, title, desc):
    year = re.search(r'20\d\d', title)
    year = year.group(0) if year else "2026"

    div_match = re.search(r'(\d+[\.,]?\d*)\s*%', desc)
    div_str = div_match.group(0) if div_match else "hohe Dividende"

    return [
        {
            "name": f"Wie funktioniert das Geschäftsmodell im Shipping-Sektor?",
            "text": f"Shipping-Unternehmen verdienen Geld durch Charterverträge: Zeitcharter (fixer Tagessatz für fixe Laufzeit) oder Spotmarkt (variabler Marktpreis). Zeitcharter bieten planbare Einnahmen, Spotmarktexponierung ermöglicht höhere Gewinne in Hochphasen. Die Dividende folgt oft direkt dem Cashflow."
        },
        {
            "name": f"Was treibt die Shipping-Nachfrage und die Frachtraten {year}?",
            "text": f"Treiber: Globaler Rohstoffhandel, Energienachfrage (LNG, Öl), Umwegverkehr (Suez/Panama-Krise), Flottenalterung ohne ausreichend Neubestellungen und IMO-Regulierung (Schwefelobergrenzen, CII-Rating). Angebotsseitig sind Neubauten teuer und langwierig (2–3 Jahre)."
        },
        {
            "name": f"Wie hoch ist die Dividende im Shipping und wie stabil ist sie?",
            "text": f"Shipping-Dividenden sind oft variabel: Bei hohen Frachtraten werden Sonderdividenden gezahlt. {div_str} Rendite ist in Hochphasen möglich. Wichtig: Frachtraten sind zyklisch – in Tiefphasen können Dividenden stark reduziert werden. Zeitcharter-Deckung reduziert die Schwankung."
        },
        {
            "name": f"Welche Risiken hat ein Investment in Shipping-Aktien?",
            "text": f"Hauptrisiken: Frachtratenzyklizität, Überkapazitäten durch Neubauwellen, Treibstoffkosten (HFO, LNG, Scrubber-Kosten), geopolitische Risiken (Routenblockaden) und Bankenfinanzierung älterer Flotten. IMO-Regulierungen (Dekarbonisierung) erhöhen Capex-Bedarf."
        },
        {
            "name": f"Wie kauft man Shipping-Aktien und was ist die beste Strategie?",
            "text": f"Shipping-Aktien sind über US-Börsen (NYSE, NASDAQ) oder europäische Börsen (Oslo, Athen) handelbar. Für Dividendeninvestoren eignet sich eine Mischung aus Zeitcharter-lastigen Unternehmen (Stabilität) und spotmarkt-exponierten Unternehmen (Upside). Quellensteuer je nach Heimatland beachten."
        }
    ]


def bdc_faq(company, title, desc):
    return [
        {
            "name": f"Was ist ein BDC (Business Development Company) und warum zahlen sie hohe Dividenden?",
            "text": f"BDCs sind US-amerikanische Investmentgesellschaften, die Kredite und Eigenkapital an mittelständische Unternehmen vergeben, die keinen Bankzugang haben. Als regulierte Investmentgesellschaft müssen sie mindestens 90 % des Einkommens ausschütten – daher Dividendenrenditen von oft 8–14 %."
        },
        {
            "name": f"Was macht {company} und worin investiert das Unternehmen?",
            "text": f"{company} ist ein Business Development Company (BDC), das vorrangig in verzinsliche Wertpapiere (Senior Secured Loans, Mezzanine, Second Lien) von US-Mittelständlern investiert. Die Einnahmen stammen überwiegend aus Zinszahlungen der Kreditnehmer."
        },
        {
            "name": f"Wie sicher ist die Dividende von {company}?",
            "text": f"BDC-Dividenden hängen vom Net Investment Income (NII) ab. Wichtige Kennzahlen: Dividend Coverage (NII / Dividende > 100 % ist gut), Non-Accruals (nicht-zahlende Kredite < 3 % ideal) und NAV-Entwicklung. Variable Zinsen (Floating Rate Loans) begünstigen BDCs in Hochzinsphasen."
        },
        {
            "name": f"Welche Risiken hat ein Investment in BDCs wie {company}?",
            "text": f"Risiken: Kreditausfälle bei Rezession, NAV-Erosion, Leverage-Risiko (BDCs können bis 2:1 verschuldet sein), Zinsrisiko bei Zinssenkungen (sinkendes Zinseinkommen) sowie Managementqualität. Gut diversifizierte BDCs mit niedrigen Non-Accruals sind widerstandsfähiger."
        },
        {
            "name": f"Wie kauft man BDC-Aktien und was ist steuerlich zu beachten?",
            "text": f"BDCs sind an US-Börsen (NYSE, NASDAQ) gelistet und über Broker mit US-Aktien-Zugang handelbar. Für deutsche Anleger: 30 % US-Quellensteuer auf Dividenden (durch DBA auf 15 % reduzierbar), aber häufig aufwendige Erstattung. Depotbanken handhaben dies unterschiedlich."
        }
    ]


def tool_faq(title, desc):
    return [
        {
            "name": "Welche Dividenden-Tools bietet MB Capital Strategies kostenlos an?",
            "text": "MB Capital Strategies bietet kostenlose Finanzrechner: Dividendenrechner, Yield-on-Cost-Rechner, Dividend Snowball Simulator, Dividenden-Wachstumsrechner, Finanzielle-Freiheit-Rechner und den Shipping-Cashflow-Rechner. Alle Tools sind direkt im Browser nutzbar, ohne Anmeldung."
        },
        {
            "name": "Was ist der Yield on Cost (YoC) und wie berechnet man ihn?",
            "text": "Yield on Cost (YoC) ist die persönliche Dividendenrendite auf den ursprünglichen Kaufpreis. Formel: (aktuelle jährliche Dividende pro Aktie) / (Einstiegskurs) × 100. Ein YoC von 10 % bedeutet, dass Sie 10 % Ihrer ursprünglichen Investition jedes Jahr als Dividende erhalten – unabhängig vom aktuellen Kurs."
        },
        {
            "name": "Was ist der Dividend Snowball Effekt?",
            "text": "Der Dividend Snowball entsteht durch Wiederanlage der Dividenden: Dividenden kaufen neue Aktien, die wiederum Dividenden zahlen. Mit der Zeit beschleunigt sich das Wachstum exponentiell. Der Dividenden-Snowball-Rechner zeigt, wie aus regelmäßigen Einlagen und Dividendenreinvestition über 10–30 Jahre ein signifikantes passives Einkommen entsteht."
        },
        {
            "name": "Wie viel Kapital brauche ich für finanzielle Freiheit?",
            "text": "Die 4-%-Regel besagt: Kapital × 4 % = jährlicher Entnahme. Für 2.000 € monatlich (24.000 €/Jahr) bräuchten Sie 600.000 € Kapital. Mit Dividendenaktien und Yield-on-Cost-Optimierung kann die Grenze sinken. Der Finanzielle-Freiheit-Rechner kalkuliert Ihren individuellen Zielbetrag."
        }
    ]


def news_faq(title, desc):
    return [
        {
            "name": "Welche Marktentwicklungen sind für Rohstoff- und Dividendeninvestoren relevant?",
            "text": "Relevante Treiber für Hard-Asset-Investoren: Ölpreis (WTI, Brent), Rohstoffpreise (Kupfer, Gold, Eisenerz), Frachtindizes (Baltic Dry, BDTI, BLPG3), Fed-Zinsentscheid, CPI-Daten und globale Nachfrageentwicklung aus China und den USA."
        },
        {
            "name": "Wie wirken CPI-Daten auf Dividendenaktien?",
            "text": "Hohe Inflation (CPI) begünstigt Hard-Asset-Unternehmen (Rohstoffpreise steigen mit Inflation), belastet jedoch zinssensitive Sektoren. Sinkende Inflation ermöglicht Zinssenkungen – gut für Pipelines, REITs und BDCs, die dann attraktiver gegenüber Anleihen werden."
        },
        {
            "name": "Wo verfolgt man aktuelle Rohstoff- und Shipping-Markt-News?",
            "text": "Quellen: Bloomberg Commodities, Platts, TradeWinds (Shipping), Seeking Alpha (BDCs, MLPs), MB Capital Strategies Blog und YouTube-Kanal @mbcapitalstrategies für wöchentliche Marktanalysen."
        }
    ]


def superzyklus_faq(title, desc):
    return [
        {
            "name": "Was ist der Rohstoff-Superzyklus und wie lange dauert er?",
            "text": "Ein Rohstoff-Superzyklus ist eine multi-jahrzehnte Phase steigender Rohstoffpreise, getrieben durch strukturelle Nachfragesteigerung. Der aktuelle Superzyklus wird durch die Energiewende angetrieben: Kupfer, Uran, Lithium, Nickel und Kobalt sind essenziell für E-Mobilität, Windräder und Energiespeicher. Analysten erwarten die Hochphase 2025–2035."
        },
        {
            "name": "Welche Rohstoffe profitieren am stärksten vom Superzyklus?",
            "text": "Top-Profiteure: Kupfer (Elektroinfrastruktur, E-Autos), Uran (Kernkraft-Renaissance), Lithium/Kobalt (Batterien), Silber (Solarpanele), Nickel (Batterien, Stahl). Aber auch traditionelle Energieträger wie Öl und Gas bleiben durch Unterinvestition strukturell knapp."
        },
        {
            "name": "Wie investiert man in den Rohstoff-Superzyklus?",
            "text": "Möglichkeiten: Einzelaktien (Mining, Energie, Shipping), Rohstoff-ETFs (z.B. Global X Copper Miners, Sprott Uranium ETF), Royalty-Unternehmen (Franco-Nevada, Wheaton Precious Metals) oder diversifizierte Rohstoff-Konglomerate (Glencore, BHP). Die 80/20-Strategie von MB Capital Strategies kombiniert stabile Dividendenzahler mit taktischer Flexibilität."
        },
        {
            "name": "Was ist Unterinvestition und warum treibt sie Rohstoffpreise?",
            "text": "Nach dem Rohstoffpreisverfall 2014–2020 investierten Minenkonzerne und Ölproduzenten massiv weniger in neue Projekte. Die Nachfrage wächst weiter (Bevölkerung, Energiewende), das Angebot kann nicht mithalten. Diese Angebotslücke führt strukturell zu höheren Preisen – Kern des aktuellen Superzyklus."
        }
    ]


def travel_faq(title, desc):
    return [
        {
            "name": "Welche Erfahrungen gibt es mit Wise und Airalo im Ausland?",
            "text": "Wise ist ideal für Auslandsreisen: Echtzeit-Wechselkurse ohne Aufschlag, kostenlose Abhebungen (bis ca. 200 €/Monat) und einfache App-Nutzung. Airalo bietet eSIM-Datenpakete für über 190 Länder – günstiger als Roaming-Tarife der deutschen Netzbetreiber."
        },
        {
            "name": "Lohnt sich eine eSIM über Airalo für Reisen nach Vietnam?",
            "text": "Ja: Airalo bietet Vietnam-eSIMs ab ca. 5 USD für 1 GB (7 Tage). Lokale SIM-Karten sind zwar noch günstiger, erfordern aber physischen Kauf vor Ort. Der Vorteil von Airalo: Sofortige Aktivierung, keine SIM-Tausch-Notwendigkeit und gute Netzabdeckung über lokale Partner."
        },
        {
            "name": "Was kostet Wise im Vergleich zur Kreditkarte im Ausland?",
            "text": "Wise berechnet ca. 0,4–2 % Wechselkursgebühr (je nach Währung), deutlich weniger als klassische Banken (1,5–3 % + 1,5 % Auslandseinsatzgebühr). Für größere Summen (Hotelkosten, Reisebudget) spart man mit Wise im Jahresschnitt signifikant."
        }
    ]


def dividend_faq(title, desc):
    return [
        {
            "name": "Was sind Dividendenaktien mit 10 % Rendite und wie realistisch sind sie?",
            "text": "Dividendenrenditen über 8–10 % sind bei Shipping-Aktien, BDCs, MLPs und Öl-Royalties realistisch. Der Schlüssel ist die Nachhaltigkeit: Ist die Dividende durch Cashflow gedeckt? Eine hohe Rendite kann auch ein Warnsignal sein (fallender Kurs, drohende Kürzung). Cashflow-Analyse ist essenziell."
        },
        {
            "name": "Welche Sektoren bieten die höchsten nachhaltigen Dividendenrenditen?",
            "text": "Top-Sektoren für Dividendenrendite: Shipping/Tanker (6–15 % variabel), BDCs (8–12 %), MLPs/Pipelines (5–9 %), Upstream-Öl (5–10 %) und Mining-Royalties (3–6 %). MB Capital Strategies analysiert alle diese Sektoren mit Cashflow-Fokus."
        },
        {
            "name": "Wie baut man ein Dividenden-Portfolio für passives Einkommen auf?",
            "text": "Grundprinzipien: Diversifikation über 10–20 Positionen, Mix aus zyklischen (Shipping, Mining) und defensiven Dividendenzahlern (Pipelines, Infrastruktur), regelmäßige Reinvestition (Dividend Snowball) und monatliche Überprüfung der Dividendendeckung. MB Capital Strategies zeigt das echte Depot mit Parqet-Portfolio-Integration."
        },
        {
            "name": "Was ist der Unterschied zwischen Dividendenrendite und Yield on Cost?",
            "text": "Dividendenrendite = aktuelle Dividende / aktueller Kurs. Yield on Cost (YoC) = aktuelle Dividende / Einstiegskurs. Wenn ein Unternehmen die Dividende erhöht und Sie früh eingestiegen sind, kann Ihr YoC 15–20 % betragen, obwohl die aktuelle Rendite nur 4 % beträgt. YoC misst Ihren persönlichen Erfolg."
        }
    ]


def generic_faq(title, desc):
    return [
        {
            "name": f"Worum geht es in diesem Beitrag auf MB Capital Strategies?",
            "text": f"{desc[:200] if desc else 'MB Capital Strategies bietet Analysen, Tools und Strategien für Dividendeninvestoren mit Fokus auf Hard Assets: Energie, Shipping, Mining und Infrastruktur.'}"
        },
        {
            "name": "Was ist das Investmentfokus von MB Capital Strategies?",
            "text": "MB Capital Strategies fokussiert sich auf Dividenden aus Hard Assets: Energie (Öl, Gas, LNG), Shipping (Tanker, Bulk, LNG-Carrier), Mining (Gold, Kupfer, Kohle) und Midstream/Pipelines. Das Ziel: nachhaltiger Cashflow und passives Einkommen durch reale Sachwerte."
        },
        {
            "name": "Ist MB Capital Strategies Anlageberatung?",
            "text": "Nein. Alle Inhalte auf MB Capital Strategies dienen ausschließlich Informations- und Bildungszwecken. Nichts davon stellt eine Anlageberatung, Empfehlung oder Aufforderung zum Kauf oder Verkauf von Wertpapieren dar. Jeder Anleger sollte seine eigene Due Diligence durchführen."
        }
    ]


def build_faq_schema(faqs):
    entities = []
    for faq in faqs:
        entities.append({
            "@type": "Question",
            "name": faq["name"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["text"]
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already has FAQPage
    if '"FAQPage"' in content:
        return False, "already has FAQ"

    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else ""

    # Extract meta description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.DOTALL)
    desc = desc_match.group(1).strip() if desc_match else ""

    slug = os.path.basename(filepath).replace(".html", "")

    faqs = get_faq_for_article(title, desc, slug)
    if not faqs:
        return False, "no FAQ generated"

    schema_json = build_faq_schema(faqs)
    schema_block = f'\n  <script type="application/ld+json">\n{schema_json}\n  </script>'

    # Insert before </head>
    if "</head>" not in content:
        return False, "no </head> found"

    new_content = content.replace("</head>", schema_block + "\n</head>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True, f"added {len(faqs)} FAQs"


def main():
    processed = 0
    skipped = 0
    errors = []

    for filename in sorted(os.listdir(BLOG_DIR)):
        if not filename.endswith(".html"):
            continue
        if filename in SKIP_FILES:
            continue

        filepath = os.path.join(BLOG_DIR, filename)
        try:
            success, msg = process_file(filepath)
            if success:
                print(f"  OK  {filename}: {msg}")
                processed += 1
            else:
                print(f" SKIP {filename}: {msg}")
                skipped += 1
        except Exception as e:
            print(f"  ERR {filename}: {e}")
            errors.append(filename)

    print(f"\nDone: {processed} updated, {skipped} skipped, {len(errors)} errors")


if __name__ == "__main__":
    main()
