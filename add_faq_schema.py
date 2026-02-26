#!/usr/bin/env python3
"""
add_faq_schema.py – Fügt FAQPage JSON-LD Schema zu Mining + Upstream Blog-Artikeln hinzu.
5 FAQs pro Artikel, spezifisch zugeschnitten auf das Unternehmen.
"""

import os, json

BASE = '/home/user/Mbcapitalstategieslanding/blog'

FAQ_DATA = {

    # ── Mining-Artikel ──────────────────────────────────────────────────────
    'thungela-resources-analyse-2026.html': [
        {
            "question": "Was ist Thungela Resources und warum ist die Aktie für Dividendeninvestoren interessant?",
            "answer": "Thungela Resources ist ein südafrikanischer Kohleproduzent, der 2021 von Anglo American abgespalten wurde. Die Aktie gilt als High-Yield-Spezialität mit historischen Dividendenrenditen von über 15 %, schuldenfreier Bilanz und hohem freien Cashflow aus dem Export-Kohlegeschäft in Südafrika."
        },
        {
            "question": "Wie hoch ist die Dividendenrendite von Thungela Resources?",
            "answer": "Thungela hat in den Boomjahren 2022–2023 Dividendenrenditen von bis zu 50 % erzielt. Aktuell schwankt die Rendite je nach Kohlepreis zwischen 10 % und 20 %. Die Dividende ist variabel und an den Cashflow gebunden – sie kann bei fallenden Kohlepreisen stark sinken."
        },
        {
            "question": "Welche Risiken bestehen bei Thungela Resources?",
            "answer": "Die größten Risiken sind: starke Abhängigkeit vom Kohlepreis (zyklisches Geschäft), Infrastrukturprobleme bei der Transnet-Eisenbahn in Südafrika (Exportengpässe), politische Unsicherheit in Südafrika sowie der langfristige Kohle-Ausstieg in Europa. ESG-Restriktionen schränken die Investorenbasis ein."
        },
        {
            "question": "Wie bewertet man Thungela Resources fundamental?",
            "answer": "Thungela wird typischerweise mit einem niedrigen KGV (2–5x) und EV/EBITDA unter 3x bewertet. Die Bewertung ist günstig, spiegelt aber die strukturellen Risiken des Kohlesektors wider. Wichtige Kennzahlen: freier Cashflow je Aktie, Net Cash Position und Export-Tonnage."
        },
        {
            "question": "Ist Thungela Resources eine sichere Langfristinvestition?",
            "answer": "Nein, Thungela eignet sich eher als taktische High-Yield-Position im Rohstoffzyklus. Die Aktie ist hochzyklisch – sie glänzt bei hohen Kohlepreisen und leidet stark bei Preiskorrekturen. Für langfristige Dividendeninvestoren empfiehlt sich eine Positionsgröße entsprechend der persönlichen Risikotoleranz."
        }
    ],

    'whitehaven-coal-analyse-2026.html': [
        {
            "question": "Was ist Whitehaven Coal und warum ist die Aktie 2026 interessant?",
            "answer": "Whitehaven Coal ist Australiens führender unabhängiger Kohleproduzent mit Fokus auf Premium-Hartkohlekohle (Metallurgische Kohle) für den asiatischen Markt. Durch die Übernahme der BHP-Steinkohleminen 2023/24 hat Whitehaven sein Portfolio stark ausgebaut und positioniert sich als Premiumlieferant für die asiatische Stahlindustrie."
        },
        {
            "question": "Wie hoch ist das Upside-Potenzial bei Whitehaven Coal?",
            "answer": "Analysten sehen bei Whitehaven Coal ein Kurspotenzial von 30–50 % auf Basis von Normalisierung der Kohlepreise und Realisierung von Synergien aus den BHP-Akquisitionen. Die Bewertung liegt deutlich unter vergleichbaren Peers auf KGV- und EV/EBITDA-Basis."
        },
        {
            "question": "Wie entwickelt sich die Dividende von Whitehaven Coal?",
            "answer": "Whitehaven zahlt eine variable Dividende, die an den freien Cashflow geknüpft ist. In Hochpreisphasen wurden Renditen von 8–12 % erzielt. Der Fokus liegt derzeit auf Schuldenabbau nach den großen Akquisitionen, weshalb die Ausschüttungen temporär moderat sein könnten."
        },
        {
            "question": "Welche Risiken hat Whitehaven Coal?",
            "answer": "Risiken: Kohlepreiszyklus, hohe Schuldenlast nach BHP-Akquisition, Abhängigkeit von asiatischer Stahlnachfrage (v.a. China/Japan/Korea), steigende ESG-Bedenken bei institutionellen Investoren und Infrastrukturkosten in Australien."
        },
        {
            "question": "Wo notiert Whitehaven Coal und wie kauft man die Aktie?",
            "answer": "Whitehaven Coal ist an der Australian Securities Exchange (ASX) unter dem Kürzel WHC notiert. Deutsche Anleger können die Aktie über Broker mit ASX-Zugang (z.B. Interactive Brokers) oder als OTC-Handel kaufen. Auf Dividenden aus Australien gilt eine Quellensteuer, die verrechenbar ist."
        }
    ],

    'yancoal-australia-analyse-2026.html': [
        {
            "question": "Was ist Yancoal Australia und warum bietet die Aktie eine hohe Dividende?",
            "answer": "Yancoal Australia ist Australiens größter reiner Kohleproduzent mit Fokus auf thermische Kohle für den asiatischen Markt. Die Mehrheit gehört dem chinesischen Konzern Yankuang Group. Durch geringe Capex, niedrige Produktionskosten und hohen Cashflow erzielt Yancoal regelmäßig Dividendenrenditen von 8–12 %."
        },
        {
            "question": "Wie hoch ist die Dividendenrendite von Yancoal Australia?",
            "answer": "Yancoal hat in Hochpreisphasen Dividendenrenditen von über 15 % erzielt. Die aktuelle Rendite liegt typischerweise zwischen 8 % und 12 %. Dividenden werden halbjährlich ausgeschüttet und orientieren sich am erzielten Nettogewinn und freien Cashflow."
        },
        {
            "question": "Welche Risiken bestehen durch die chinesische Mehrheitsbeteiligung?",
            "answer": "Die chinesische Muttergesellschaft Yankuang hält ~62 % an Yancoal. Dies birgt Risiken: geopolitische Spannungen zwischen Australien und China, mögliche Interessenkonflikte bei Dividendenentscheidungen und eingeschränkte Handelsliquidität. Gleichzeitig bietet die Muttergesellschaft Stabilitätsunterstützung."
        },
        {
            "question": "Warum ist Kohle trotz Energiewende für Investoren interessant?",
            "answer": "Asiatische Schwellenländer (Indien, Vietnam, Bangladesch, Philippinen) bauen neue Kohlekraftwerke und erhöhen ihren Kohleverbrauch massiv. Thermische Kohle bleibt Jahrzehnte lang Teil des globalen Energiemixes. Gleichzeitig sinken Investitionen in neue Kohleminen, was das Angebot mittelfristig stützt."
        },
        {
            "question": "Wie kauft man Yancoal Australia Aktien als deutsches Anleger?",
            "answer": "Yancoal ist an der ASX (Kürzel: YAL) notiert. Der Kauf ist über internationale Broker wie Interactive Brokers möglich. Alternativ existieren OTC-Handelsmöglichkeiten in Deutschland. Die australische Quellensteuer auf Dividenden (15 % nach DBA) ist auf die deutsche Abgeltungssteuer anrechenbar."
        }
    ],

    'bhp-analyse-2026.html': [
        {
            "question": "Was macht BHP und warum ist der Konzern für Rohstoffinvestoren interessant?",
            "answer": "BHP ist der weltgrößte Bergbaukonzern mit Schwerpunkten auf Eisenerz (Australien), Kupfer (Chile, Australien), Kohle und Kali (Potash). Das diversifizierte Portfolio macht BHP zu einem Basisinvestment im Rohstoff-Superzyklus. Besonders die wachsende Kupferexponierung gilt als strategischer Vorteil."
        },
        {
            "question": "Wie hoch ist die BHP Dividende und wie wird sie berechnet?",
            "answer": "BHP verfolgt eine progressive Dividendenpolitik mit einer Ausschüttungsquote von mindestens 50 % des Nettogewinns nach Bereinigungen. Historisch wurden Renditen von 5–8 % erzielt. Dividenden werden halbjährlich ausgezahlt, wahlweise in AUD oder USD. Bei deutschen Anlegern greift das DBA Australien (15 % Quellensteuer)."
        },
        {
            "question": "Wie profitiert BHP vom Rohstoff-Superzyklus und der Kupfernachfrage?",
            "answer": "Kupfer ist das 'Metall der Energiewende' – Elektrofahrzeuge, Windräder und Strometze benötigen 3–5x mehr Kupfer als klassische Anwendungen. BHP ist einer der weltweit größten Kupferproduzenten (Escondida-Mine, Prominent Hill) und profitiert überproportional von steigenden Kupferpreisen."
        },
        {
            "question": "Was sind die größten Risiken bei BHP?",
            "answer": "Hauptrisiken: Eisenerzpreisabhängigkeit (~50 % des EBITDA), starke Abhängigkeit von Chinas Stahlproduktion, steigende Regulierung in Australien und Chile sowie Währungsrisiken (AUD/USD). Das OZ Minerals-Akquisition erhöhte die Verschuldung temporär."
        },
        {
            "question": "Wo ist BHP notiert und wie kauft man die Aktie?",
            "answer": "BHP ist dual notiert: in London (LSE: BHP) und in Sydney (ASX: BHP). Für Deutsche empfiehlt sich der Kauf über den XETRA oder direkt über die Londoner Börse. Die Londoner Notierung ist liquider für europäische Anleger."
        }
    ],

    'fortescue-analyse-2026.html': [
        {
            "question": "Was macht Fortescue und warum ist die Aktie für Dividendeninvestoren interessant?",
            "answer": "Fortescue ist der viertgrößte Eisenerzproduzent weltweit mit Sitz in Perth, Australien. Das Unternehmen ist für seine extrem hohen Ausschüttungsquoten (oft 65–75 % des Nettogewinns) bekannt, was in guten Jahren Dividendenrenditen von 8–15 % ermöglicht. Gründer Andrew Forrest hält ~36 % und bevorzugt hohe Dividenden."
        },
        {
            "question": "Wie hoch ist die Fortescue Dividende?",
            "answer": "Fortescue schüttet typischerweise 65–75 % des Nettogewinns als Dividende aus – halbjährlich. In Hochpreisphasen wurden Dividendenrenditen von über 10 % erzielt. Dividenden werden in AUD gezahlt; deutsche Anleger erhalten nach DBA-Australien 15 % Quellensteuerabzug, der auf die Abgeltungssteuer anrechenbar ist."
        },
        {
            "question": "Was ist Fortescue Future Industries (FFI) und welches Risiko bringt es?",
            "answer": "FFI (umbenannt zu Fortescue Energy) ist die Green-Hydrogen-Sparte des Konzerns. Gründer Forrest investierte Milliarden in Wasserstoffprojekte mit bisher geringem kommerziellem Erfolg. Kritiker sehen FFI als Kapitalvernichter, der die Dividendenfähigkeit des Kerngeschäfts belastet. 2024 wurden Mitarbeiter entlassen und das Budget gekürzt."
        },
        {
            "question": "Wie abhängig ist Fortescue vom Eisenerzpreis?",
            "answer": "Fortescue ist fast vollständig vom Eisenerzpreis abhängig (~100 % des Umsatzes). Bei einem Eisenerzpreis über 100 USD/t ist das Unternehmen hochprofitabel; bei Preisen unter 80 USD/t wird die Kapitalrendite deutlich schlechter. China konsumiert ~70 % des global gehandelten Eisenerzes – eine Konjunkturabkühlung trifft Fortescue stark."
        },
        {
            "question": "Warum gilt Fortescue als High-Grade-Eisenerz-Produzent?",
            "answer": "Fortescue produziert überwiegend Eisenerz mit ~57–60 % Eisengehalt, was im Vergleich zu Vale (65 %+) als 'mittlere Qualität' gilt. Durch Mischung und neue Deposits strebt Fortescue höheren Eisengehalt an. Ein höherer Fe-Gehalt erzielt Aufschläge am Markt und verbessert die Margen."
        }
    ],

    'rio-tinto-analyse-2026.html': [
        {
            "question": "Was macht Rio Tinto und warum ist der Konzern im Kupfer-Superzyklus interessant?",
            "answer": "Rio Tinto ist einer der weltgrößten Bergbaukonzerne mit Kerngeschäften in Eisenerz (Pilbara, Australien), Kupfer (Kennecott, Oyu Tolgoi), Aluminium und Lithium (Boron). Die massive Oyu-Tolgoi-Kupfermine in der Mongolei soll bis 2030 zu einem der weltgrößten Kupferproduzenten werden."
        },
        {
            "question": "Wie hoch ist die Rio Tinto Dividende?",
            "answer": "Rio Tinto zahlt eine hohe progressive Dividende: die Auszahlungsquote beträgt mindestens 50 % des Nettogewinns. Historisch wurden Renditen von 5–9 % erzielt. Dividenden werden in USD ausgezahlt (Londoner Notierung) oder AUD (ASX). Deutsche Anleger sollten das jeweilige Doppelbesteuerungsabkommen beachten."
        },
        {
            "question": "Welche Risiken hat Rio Tinto als Investor?",
            "answer": "Hauptrisiken: ~50 % des EBITDA kommt aus Eisenerz und damit China-abhängig; der Oyu-Tolgoi-Bau hat mehrfach den Kostenrahmen gesprengt; politische Risiken in der Mongolei; Umweltvorfälle (Juukan Gorge Australien 2020 zerstörte Ruf); sowie allgemeine Rohstoffzyklik."
        },
        {
            "question": "In welchen Segmenten wächst Rio Tinto besonders?",
            "answer": "Kupfer ist das Wachstumssegment: Oyu Tolgoi soll die Kupferproduktion bis 2030 auf ~500.000 t/Jahr steigern. Lithium (Rincon-Projekt in Argentinien) positioniert Rio Tinto für den Batteriemarkt. Aluminium bleibt ein Standbein, ist aber energieintensiv und konjunkturabhängig."
        },
        {
            "question": "Wie kauft man Rio Tinto Aktien als deutscher Anleger?",
            "answer": "Rio Tinto ist in London (LSE: RIO) und Sydney (ASX: RIO) notiert. Über XETRA oder direkt an der Londoner Börse kaufbar. Die Dividende der Londoner Aktie wird in USD ausgezahlt; Quellensteuer richtet sich nach dem britischen DBA (keine britische Quellensteuer auf Dividenden). An der ASX gilt australische Quellensteuer."
        }
    ],

    'vale-analyse-2026.html': [
        {
            "question": "Was macht Vale und warum ist die Aktie für Dividendeninvestoren interessant?",
            "answer": "Vale ist der weltgrößte Eisenerzproduzent und einer der führenden Nickelproduzenten (wichtig für Batterien). Sitz: Brasilien. Vale schüttet einen Großteil des Cashflows als Dividende aus und bietet historisch Renditen von 8–12 %. Das Unternehmen profitiert von der Nachfrage nach Hochqualitäts-Eisenerz für die Stahlindustrie."
        },
        {
            "question": "Was ist die Quellensteuer bei Vale und wie wirkt sie sich aus?",
            "answer": "Brasilien erhebt 15 % Quellensteuer auf Dividenden für ausländische Anleger. Nach dem Doppelbesteuerungsabkommen Deutschland-Brasilien sind jedoch nur 15 % abzuführen, die auf die deutsche Abgeltungssteuer anrechenbar sind. Anleger sollten mit ihrem Broker prüfen, ob die Anrechnung korrekt durchgeführt wird."
        },
        {
            "question": "Wie beeinflusst der Eisenerzpreis die Vale-Aktie?",
            "answer": "Vale ist stark vom Eisenerzpreis abhängig: Bei Eisenerz über 120 USD/t sprudeln Cashflows und Dividenden; unter 90 USD/t werden die Gewinne deutlich geringer. Die chinesische Stahlproduktion bestimmt maßgeblich den Eisenerzpreis. Nickel ist eine Diversifikation, macht aber nur ~15 % der Einnahmen aus."
        },
        {
            "question": "Welche Risiken bestehen bei einem Investment in Vale?",
            "answer": "Risiken: Brasilianisches Länderrisiko (politische Instabilität, Steuerpolitik), Brumadinho- und Samarco-Katastrophen (Dammbrüche, laufende Haftungskosten), starke China-Abhängigkeit, Eisenerzpreiszyklus und USD/BRL-Währungsschwankungen. Das Mariana-Samarco-Vergleichspaket belastet die Bilanz."
        },
        {
            "question": "Wie ist die Bewertung von Vale im Vergleich zu BHP und Rio Tinto?",
            "answer": "Vale wird typischerweise mit einem Abschlag zu BHP und Rio Tinto gehandelt – aufgrund des Brasilienrisikos und der Haftungslasten aus den Dammbrüchen. Das KGV liegt oft unter 5x, EV/EBITDA unter 4x. Für Contrarian-Investoren bietet dies Einstiegschancen bei hohem Dividendenertrag."
        }
    ],

    'glencore-analyse-2026.html': [
        {
            "question": "Was macht Glencore und warum ist das Unternehmen einzigartig unter Mining-Aktien?",
            "answer": "Glencore ist weltweit einzigartig: Neben der Rohstoffproduktion (Kupfer, Kobalt, Kohle, Zink) betreibt Glencore ein massives Rohstoff-Handelsgeschäft, das in allen Marktphasen Erträge generiert. Diese Kombination aus Bergbau und Trading macht Glencore widerstandsfähiger als reine Minenproduzenten."
        },
        {
            "question": "Wie hoch ist die Glencore Dividende?",
            "answer": "Glencore zahlt eine Basisdividende plus variable Sonderdividenden, die am freien Cashflow hängen. In Hochphasen wurden Gesamtrenditen von 8–12 % erzielt. Das Management setzt außerdem auf Aktienrückkäufe. Die Dividende ist in USD und wird zweimal jährlich ausgezahlt."
        },
        {
            "question": "Warum ist Glencore ein Profiteur des Rohstoff-Superzyklus?",
            "answer": "Glencore ist einer der weltgrößten Kupferproduzenten (Katanga, Collahuasi) und größter Kobaltproduzent – beides unverzichtbar für Energiewende-Technologien. Gleichzeitig ist das Kohlegeschäft profitabel und cashflow-stark. Der Trading-Arm profitiert besonders von Preisvolatilität, die Glencore für Arbitrage nutzt."
        },
        {
            "question": "Welche Risiken hat Glencore?",
            "answer": "Risiken: Hohe Verschuldung durch Rohstoff-Handelsbilanzen, Compliance-Risiken (Glencore zahlte 2022 über 1 Mrd. USD Strafe für Korruption und Marktmanipulation), Abhängigkeit von politisch instabilen Förderregionen (Kongo, Kasachstan), Zyklizität der Rohstoffpreise und ESG-Kritik wegen Kohle."
        },
        {
            "question": "Was macht das Glencore-Trading-Geschäft aus?",
            "answer": "Glencore handelt jährlich Hunderte Millionen Tonnen Rohstoffe und erzielt Margen aus Preisdifferenzen zwischen Regionen und Zeitpunkten. Das Trading-Geschäft generiert in volatilen Märkten besonders hohe Gewinne und hat ein niedrigeres Rohstoffpreisrisiko als reines Mining. Es ist der entscheidende Wettbewerbsvorteil Glencores."
        }
    ],

    'kazatomprom-analyse-2026.html': [
        {
            "question": "Was ist Kazatomprom und warum ist das Unternehmen für Uraninvestoren relevant?",
            "answer": "Kazatomprom ist der weltgrößte Uranproduzent mit Sitz in Kasachstan und kontrolliert etwa 40 % der weltweiten Uranproduktion. Als staatlich kontrolliertes Unternehmen (KazAtomProm) produziert es Uran zu extrem niedrigen Kosten via In-situ-Leaching (ISL) und beliefert Atomkraftwerke weltweit – besonders in Europa, China und Korea."
        },
        {
            "question": "Wie hoch ist die Dividende von Kazatomprom?",
            "answer": "Kazatomprom schüttet mindestens 75 % des freien Cashflows aus – eine der höchsten Ausschüttungsquoten im Minensektor. Bei steigenden Uranpreisen sind Dividendenrenditen von 5–10 % realisierbar. Dividenden werden halbjährlich in KZT ausgezahlt; die GDRs (Global Depositary Receipts) handeln in London (LSE)."
        },
        {
            "question": "Wie ist die Urannachfrage 2026 und darüber hinaus?",
            "answer": "Die globale Urannachfrage wächst durch Renaissance der Kernenergie: China baut 20+ Reaktoren, Indien und Osteuropa erweitern ihre Kapazitäten, USA und Europa verlängern Laufzeiten. Laut WNA-Prognosen steigt die Urannachfrage bis 2040 um 50 %. Das Angebot hinkt hinterher – ein klassisches Defizitumfeld."
        },
        {
            "question": "Welche Risiken hat Kazatomprom für westliche Anleger?",
            "answer": "Risiken: Kasachstan ist geopolitisch zwischen Russland und China eingeklemmt – Sanktionsrisiken, Lieferkettenstörungen. Kasachische Regierung hält ~75 % und bestimmt Dividendenpolitik. Währungsrisiken (KZT/USD). Die Aktie ist an der LSE als GDR und der AIX (Kasachstan) notierbar. Westliche Sanktionen gegen Russland betreffen Kasachstan indirekt."
        },
        {
            "question": "Wie kauft man Kazatomprom als europäischer Anleger?",
            "answer": "Kazatomprom GDRs sind an der London Stock Exchange (LSE: KAP) handelbar. Über Interactive Brokers oder andere internationale Broker kaufbar. Alternativ bieten Uran-ETFs (z.B. Global X Uranium ETF, Sprott Uranium Miners ETF) eine diversifizierte Uranexponierung. Direkt-Investment in GDRs ist für Privatanleger möglich, aber liquiditätsschwächer als ETFs."
        }
    ],
}


def faq_to_json_ld(faqs):
    """Erstellt FAQPage JSON-LD Schema-Block."""
    main_entity = []
    for faq in faqs:
        main_entity.append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity
    }
    return '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=2) + '\n</script>'


fixed = 0
skipped = []

for filename, faqs in FAQ_DATA.items():
    filepath = os.path.join(BASE, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  NOT FOUND: {filename}")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Schon FAQ-Schema vorhanden?
    if '"@type": "FAQPage"' in content or '"FAQPage"' in content:
        print(f"  ✅ Already has FAQPage: {filename}")
        continue

    # Einfügen vor </head>
    faq_block = faq_to_json_ld(faqs)
    if '</head>' not in content:
        print(f"  ⚠️  No </head> found: {filename}")
        skipped.append(filename)
        continue

    new_content = content.replace('</head>', f'\n  <!-- FAQ Schema -->\n  {faq_block}\n</head>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  ✅ FAQ added: {filename}")
    fixed += 1

print(f"\n✅ Done! {fixed} Artikel mit FAQ-Schema ausgestattet.")
if skipped:
    print(f"⚠️  Skipped: {skipped}")
