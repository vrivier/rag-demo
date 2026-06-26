from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import os

OUTPUT_DIR = r"C:\Users\vrivi\OneDrive\Bureau\rag"
COMPANY = "FICTIVE INDUSTRIE S.A."
COMPANY_SHORT = "Fictive Industrie"

# ─── Color palette ───────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#1A2E4A")
STEEL  = colors.HexColor("#3A6186")
LIGHT  = colors.HexColor("#EEF2F7")
ACCENT = colors.HexColor("#E07B39")
GREY   = colors.HexColor("#555555")

# ─── Style helpers ────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["doc_title"] = ParagraphStyle(
        "doc_title", fontSize=22, textColor=colors.white,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=6
    )
    styles["doc_subtitle"] = ParagraphStyle(
        "doc_subtitle", fontSize=11, textColor=colors.HexColor("#CCDDEE"),
        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4
    )
    styles["h1"] = ParagraphStyle(
        "h1", fontSize=14, textColor=NAVY,
        fontName="Helvetica-Bold", spaceBefore=18, spaceAfter=6,
        borderPad=4
    )
    styles["h2"] = ParagraphStyle(
        "h2", fontSize=11, textColor=STEEL,
        fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=4
    )
    styles["body"] = ParagraphStyle(
        "body", fontSize=9.5, textColor=GREY,
        fontName="Helvetica", leading=14, spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", fontSize=9.5, textColor=GREY,
        fontName="Helvetica", leading=14, spaceAfter=3,
        leftIndent=14, bulletIndent=4
    )
    styles["note"] = ParagraphStyle(
        "note", fontSize=8.5, textColor=colors.HexColor("#777777"),
        fontName="Helvetica-Oblique", leading=12, spaceAfter=4,
        alignment=TA_JUSTIFY
    )
    styles["footer"] = ParagraphStyle(
        "footer", fontSize=7.5, textColor=colors.HexColor("#999999"),
        fontName="Helvetica", alignment=TA_CENTER
    )
    return styles

S = make_styles()

def header_block(title, subtitle, version, date):
    """Returns a list of flowables for the document header."""
    # Title box via a 1-cell table
    tbl = Table([[Paragraph(title, S["doc_title"])]],
                colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("ROUNDEDCORNERS", [6,6,6,6]),
        ("TOPPADDING",    (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ]))

    meta = Table([[
        Paragraph(f"<b>{COMPANY}</b>", ParagraphStyle("m", fontSize=9, textColor=NAVY, fontName="Helvetica-Bold")),
        Paragraph(f"Version {version} — {date}", ParagraphStyle("m2", fontSize=9, textColor=GREY, fontName="Helvetica", alignment=2)),
    ]], colWidths=[9*cm, 8*cm])
    meta.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))

    return [
        tbl,
        Spacer(1, 8),
        Paragraph(subtitle, ParagraphStyle("sub", fontSize=10, textColor=STEEL, fontName="Helvetica-Oblique", alignment=TA_CENTER)),
        Spacer(1, 4),
        meta,
        HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=14),
    ]

def section(title, content_items):
    """title + list of (kind, text) where kind in ['p','b','h2','note']"""
    items = [Paragraph(title, S["h1"]),
             HRFlowable(width="100%", thickness=0.5, color=LIGHT, spaceAfter=6)]
    for kind, text in content_items:
        if kind == "p":
            items.append(Paragraph(text, S["body"]))
        elif kind == "b":
            items.append(Paragraph(f"&#x2022;  {text}", S["bullet"]))
        elif kind == "h2":
            items.append(Paragraph(text, S["h2"]))
        elif kind == "note":
            items.append(Paragraph(f"<i>{text}</i>", S["note"]))
        elif kind == "spacer":
            items.append(Spacer(1, 8))
        elif kind == "table":
            # text is (data, colWidths)
            data, widths = text
            t = Table(data, colWidths=widths)
            t.setStyle(TableStyle([
                ("BACKGROUND",    (0,0), (-1,0), NAVY),
                ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
                ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
                ("FONTSIZE",      (0,0), (-1,-1), 9),
                ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.white, LIGHT]),
                ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#CCCCCC")),
                ("TOPPADDING",    (0,0), (-1,-1), 5),
                ("BOTTOMPADDING", (0,0), (-1,-1), 5),
                ("LEFTPADDING",   (0,0), (-1,-1), 6),
                ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
            ]))
            items.append(t)
            items.append(Spacer(1, 8))
    return items


def build_doc(filename, story):
    path = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2*cm, bottomMargin=2.5*cm,
        title=filename.replace(".pdf","").replace("_"," ")
    )
    doc.build(story)
    print(f"  ✓ {filename}")
    return path


# ══════════════════════════════════════════════════════════════════════════════
# 1. RÈGLEMENT INTÉRIEUR
# ══════════════════════════════════════════════════════════════════════════════
def doc_reglement():
    story = header_block(
        "Règlement Intérieur",
        "Document obligatoire — Article L.1321-1 du Code du travail",
        "3.2", "1er janvier 2025"
    )

    story += section("Article 1 — Champ d'application", [
        ("p", "Le présent règlement intérieur s'applique à l'ensemble du personnel salarié d'Fictive Industrie S.A., quelle que soit la nature de leur contrat (CDI, CDD, intérim), dès lors qu'ils exercent leur activité dans les établissements, usines et bureaux de la société situés en France métropolitaine."),
        ("p", "Les prestataires externes et sous-traitants intervenant sur les sites de la société sont tenus de respecter les dispositions relatives à la sécurité, à l'hygiène et à la discipline figurant dans ce règlement."),
    ])

    story += section("Article 2 — Horaires de travail", [
        ("p", "La durée légale du travail est fixée à 35 heures hebdomadaires conformément à l'article L.3121-27 du Code du travail. Des dispositions spécifiques s'appliquent selon les établissements et les conventions d'aménagement du temps de travail en vigueur."),
        ("h2", "2.1 Horaires fixes (personnel administratif)"),
        ("b", "Matin : 8h30 – 12h30"),
        ("b", "Après-midi : 13h30 – 17h30"),
        ("b", "Pause déjeuner : 1 heure minimum, non incluse dans le temps de travail effectif"),
        ("h2", "2.2 Horaires postés (personnel de production)"),
        ("p", "Le personnel de production est soumis à un régime d'horaires postés en 3x8 (matin, après-midi, nuit) défini par les plannings établis par les chefs d'équipe et communiqués au moins 7 jours calendaires à l'avance."),
        ("h2", "2.3 Pointage et contrôle"),
        ("p", "Tout salarié est tenu de pointer à l'entrée et à la sortie du site via le système de badgeage électronique. Toute anomalie doit être signalée au service RH dans les 48 heures."),
    ])

    story += section("Article 3 — Discipline et sanctions", [
        ("p", "Tout manquement aux règles du présent règlement est susceptible de faire l'objet d'une sanction disciplinaire proportionnée à la gravité des faits reprochés. La procédure disciplinaire respecte les dispositions des articles L.1332-1 à L.1332-4 du Code du travail."),
        ("h2", "Échelle des sanctions"),
        ("table", (
            [["Niveau", "Type de sanction", "Exemples de faits"],
             ["1", "Avertissement écrit", "Retard répété, non-respect des consignes mineures"],
             ["2", "Mise à pied conservatoire (1 à 3 jours)", "Insubordination, absence injustifiée"],
             ["3", "Mise à pied disciplinaire (3 à 5 jours)", "Manquement grave aux règles de sécurité"],
             ["4", "Licenciement pour faute", "Faute grave ou lourde, vol, harcèlement"]],
            [2*cm, 6*cm, 8.5*cm]
        )),
    ])

    story += section("Article 4 — Hygiène et sécurité", [
        ("p", "La sécurité est une priorité absolue chez Fictive Industrie. Chaque salarié est responsable de sa propre sécurité et de celle de ses collègues. Le non-respect des consignes de sécurité peut entraîner des sanctions disciplinaires immédiates pouvant aller jusqu'au licenciement."),
        ("b", "Port obligatoire des Équipements de Protection Individuelle (EPI) dans toutes les zones de production"),
        ("b", "Interdiction absolue de consommer de l'alcool ou des stupéfiants sur le lieu de travail ou d'y accéder sous leur emprise"),
        ("b", "Obligation de signaler immédiatement tout incident, accident ou situation dangereuse au responsable HSE"),
        ("b", "Interdiction de fumer en dehors des zones fumeurs délimitées"),
        ("b", "Respect des procédures de consignation/déconsignation pour toute intervention sur les machines"),
        ("note", "Référence : Document Unique d'Évaluation des Risques Professionnels (DUERP) — mis à jour annuellement et consultable auprès du service HSE."),
    ])

    story += section("Article 5 — Harcèlement et discriminations", [
        ("p", "Fictive Industrie s'engage à garantir un environnement de travail respectueux et inclusif. Tout acte de harcèlement moral ou sexuel, toute discrimination fondée sur l'origine, le sexe, l'âge, le handicap, la religion, l'orientation sexuelle ou toute autre caractéristique protégée est formellement interdit et constitue une faute grave."),
        ("p", "Tout salarié qui s'estime victime ou témoin de tels agissements peut saisir, en toute confidentialité, le référent harcèlement (désigné par l'employeur et le CSE), le service RH ou les représentants du personnel."),
    ])

    story += section("Article 6 — Entrée en vigueur", [
        ("p", "Le présent règlement intérieur a été soumis pour avis au Comité Social et Économique lors de la réunion du 15 novembre 2024. Il a été déposé auprès de l'inspection du travail et du greffe du Conseil de Prud'hommes compétent. Il entre en vigueur le 1er janvier 2025."),
        ("note", "Document établi conformément aux articles L.1321-1 et suivants du Code du travail. Toute modification ultérieure fera l'objet de la même procédure de consultation et de dépôt."),
    ])

    return build_doc("01_reglement_interieur.pdf", story)


# ══════════════════════════════════════════════════════════════════════════════
# 2. POLITIQUE DE TÉLÉTRAVAIL
# ══════════════════════════════════════════════════════════════════════════════
def doc_teletravail():
    story = header_block(
        "Politique de Télétravail",
        "Accord d'entreprise — Chapitre RH-TT-2024",
        "2.0", "1er mars 2024"
    )

    story += section("1. Objet et principes généraux", [
        ("p", "Le présent accord définit les modalités de recours au télétravail au sein d'Fictive Industrie S.A., en application de l'article L.1222-9 du Code du travail et de l'Accord National Interprofessionnel (ANI) du 26 novembre 2020."),
        ("p", "Le télétravail est une modalité d'organisation du travail et non un droit absolu. Il repose sur un principe de double volontariat : il ne peut être imposé ni par le salarié ni par l'employeur, sauf circonstances exceptionnelles (ex : pandémie, épisode de pollution)."),
    ])

    story += section("2. Éligibilité", [
        ("p", "Peuvent bénéficier du télétravail les salariés réunissant l'ensemble des conditions suivantes :"),
        ("b", "Être titulaire d'un CDI ou d'un CDD d'une durée supérieure à 6 mois"),
        ("b", "Avoir validé une période d'intégration de 3 mois dans le poste actuel"),
        ("b", "Occuper un poste dont les missions sont compatibles avec le travail à distance (exclut les postes de production, maintenance sur site, logistique terrain)"),
        ("b", "Disposer d'un espace de travail adapté et d'une connexion internet fiable à son domicile"),
        ("b", "Avoir obtenu une évaluation satisfaisante lors du dernier entretien annuel"),
        ("note", "Les salariés en situation de handicap ou présentant un certificat médical justifiant une nécessité de télétravail bénéficient d'un accès prioritaire, indépendamment de la condition d'ancienneté."),
    ])

    story += section("3. Modalités d'organisation", [
        ("h2", "3.1 Nombre de jours"),
        ("table", (
            [["Catégorie", "Jours maxi/semaine", "Jours présentiel obligatoire"],
             ["Cadres", "2 jours", "3 jours"],
             ["ETAM", "2 jours", "3 jours"],
             ["Managers d'équipe", "1 jour", "4 jours"]],
            [5.5*cm, 5*cm, 6*cm]
        )),
        ("h2", "3.2 Jours fixes"),
        ("p", "Les jours de télétravail sont fixés d'un commun accord entre le salarié et son manager, formalisés dans un avenant au contrat de travail ou par mail avec accusé de réception. Ils sont en principe réguliers mais peuvent être modifiés avec un préavis de 48 heures."),
        ("h2", "3.3 Plages horaires"),
        ("p", "Pendant les jours de télétravail, le salarié reste joignable et disponible durant ses horaires habituels de travail. Il participe à toutes les réunions planifiées, en visioconférence si nécessaire."),
        ("p", "Le droit à la déconnexion s'applique pleinement : aucune réponse n'est exigée en dehors des horaires de travail contractuels."),
    ])

    story += section("4. Équipement et sécurité", [
        ("p", "La société met à disposition de chaque salarié en télétravail un ordinateur portable professionnel et un accès VPN sécurisé. L'utilisation de ces équipements est soumise à la Charte Informatique en vigueur."),
        ("b", "Il est interdit de travailler sur des réseaux Wi-Fi publics non sécurisés sans activation préalable du VPN"),
        ("b", "Les documents confidentiels ne doivent pas être imprimés à domicile sauf autorisation expresse"),
        ("b", "En cas de panne matérielle, le salarié doit en informer le service IT dans les 2 heures et se rendre sur site si la panne persiste"),
        ("h2", "4.1 Prise en charge des frais"),
        ("p", "Fictive Industrie verse une indemnité forfaitaire de 10,50 € par jour de télétravail effectif, dans la limite de 55 € par mois, conformément au barème URSSAF en vigueur. Cette indemnité est versée mensuellement sur justificatif déclaratif dans l'outil RH."),
    ])

    story += section("5. Suspension et réversibilité", [
        ("p", "Le télétravail peut être suspendu temporairement ou définitivement par l'employeur ou le salarié, moyennant un délai de prévenance de 15 jours calendaires, sans que cela ne constitue une modification du contrat de travail."),
        ("p", "En cas de changement de poste, de site ou de manager, les conditions de télétravail font l'objet d'une nouvelle négociation dans le mois suivant le changement."),
    ])

    return build_doc("02_politique_teletravail.pdf", story)


# ══════════════════════════════════════════════════════════════════════════════
# 3. CHARTE INFORMATIQUE
# ══════════════════════════════════════════════════════════════════════════════
def doc_charte_info():
    story = header_block(
        "Charte d'Utilisation des Systèmes d'Information",
        "Charte Informatique — Référence DSI-CHART-2024",
        "4.1", "15 septembre 2024"
    )

    story += section("1. Objet et périmètre", [
        ("p", "La présente charte définit les règles d'utilisation des ressources informatiques et des systèmes d'information d'Fictive Industrie S.A. Elle s'applique à l'ensemble des utilisateurs : salariés, intérimaires, stagiaires, prestataires et sous-traitants ayant accès au système d'information de la société."),
        ("p", "Sont concernés tous les équipements (ordinateurs, smartphones, tablettes), les applications métier, les messageries, les réseaux (y compris Wi-Fi), ainsi que les données hébergées dans le cloud ou sur site."),
    ])

    story += section("2. Règles d'utilisation", [
        ("h2", "2.1 Usage professionnel"),
        ("p", "Les ressources informatiques sont mises à disposition à des fins professionnelles. Un usage personnel raisonnable et occasionnel est toléré, à condition de ne pas nuire à la productivité, à la sécurité des systèmes ou à l'image de la société."),
        ("h2", "2.2 Usages strictement interdits"),
        ("b", "Accès, téléchargement ou diffusion de contenu illicite, pornographique, haineux ou portant atteinte à la dignité des personnes"),
        ("b", "Installation de logiciels non autorisés par la DSI (y compris logiciels gratuits, freeware, IA génératives non validées)"),
        ("b", "Utilisation des ressources de la société pour des activités commerciales personnelles ou concurrentes"),
        ("b", "Contournement des dispositifs de sécurité (pare-feu, proxy, filtres de contenu)"),
        ("b", "Partage des identifiants de connexion avec un tiers, même un collègue"),
        ("b", "Connexion de périphériques personnels (clés USB, disques durs) sans autorisation du service IT"),
    ])

    story += section("3. Gestion des mots de passe", [
        ("p", "Chaque utilisateur est responsable de la confidentialité de ses identifiants. Les mots de passe doivent respecter la politique de sécurité suivante :"),
        ("table", (
            [["Critère", "Exigence"],
             ["Longueur minimale", "12 caractères"],
             ["Complexité", "Majuscules, minuscules, chiffres, caractères spéciaux"],
             ["Renouvellement", "Tous les 90 jours"],
             ["Historique", "Impossibilité de réutiliser les 10 derniers mots de passe"],
             ["MFA", "Obligatoire pour les accès distants (VPN, messagerie externe)"]],
            [7*cm, 9.5*cm]
        )),
    ])

    story += section("4. Messagerie et communications", [
        ("p", "La messagerie professionnelle Outlook (@fictive-industrie.fr) est l'outil de communication officiel. Son utilisation doit respecter les règles suivantes :"),
        ("b", "Ne pas transmettre de données sensibles ou confidentielles sans chiffrement préalable"),
        ("b", "Ne pas s'abonner à des newsletters commerciales personnelles avec l'adresse professionnelle"),
        ("b", "Vider la corbeille régulièrement ; la boîte mail est archivée automatiquement après 3 ans"),
        ("b", "En cas de réception d'un message suspect (phishing), ne pas cliquer sur les liens et le signaler immédiatement à security@fictive-industrie.fr"),
        ("h2", "4.1 Réseaux sociaux"),
        ("p", "L'expression sur les réseaux sociaux en tant que représentant ou employé d'Fictive Industrie est soumise à une procédure d'autorisation préalable de la Direction Communication. Il est interdit de divulguer des informations confidentielles, des résultats financiers non publiés ou des données relatives aux clients et projets en cours."),
    ])

    story += section("5. Protection des données (RGPD)", [
        ("p", "Fictive Industrie traite des données personnelles dans le cadre de sa politique de confidentialité conforme au RGPD (Règlement (UE) 2016/679). Tout salarié ayant accès à des données personnelles (clients, fournisseurs, collaborateurs) est soumis à une obligation de confidentialité et doit respecter les principes de minimisation, de finalité et de sécurité des données."),
        ("p", "Toute violation de données (fuite, perte, accès non autorisé) doit être signalée au DPO (Data Protection Officer) dans les 24 heures via l'adresse dpo@fictive-industrie.fr."),
    ])

    story += section("6. Surveillance et contrôle", [
        ("p", "Conformément à la jurisprudence et aux recommandations de la CNIL, la société se réserve le droit de contrôler l'utilisation des ressources informatiques dans le respect des droits des salariés. Les connexions internet, les flux réseau et les accès aux applications sont journalisés à des fins de sécurité."),
        ("note", "Les salariés ont été informés de ces mesures de contrôle, conformément à l'article L.1222-4 du Code du travail. Les représentants du personnel ont été consultés avant leur mise en oeuvre."),
    ])

    return build_doc("03_charte_informatique.pdf", story)


# ══════════════════════════════════════════════════════════════════════════════
# 4. POLITIQUE DE CONGÉS & ABSENCES
# ══════════════════════════════════════════════════════════════════════════════
def doc_conges():
    story = header_block(
        "Politique de Congés et Absences",
        "Guide RH — Référence RH-CONG-2025",
        "5.0", "1er janvier 2025"
    )

    story += section("1. Congés payés annuels", [
        ("p", "Conformément à l'article L.3141-3 du Code du travail, chaque salarié acquiert 2,5 jours ouvrables de congés payés par mois de travail effectif, soit 30 jours ouvrables (5 semaines) pour une année complète."),
        ("h2", "1.1 Période d'acquisition et de prise"),
        ("table", (
            [["Paramètre", "Règle applicable"],
             ["Période d'acquisition", "1er juin au 31 mai"],
             ["Période de prise principale", "1er mai au 31 octobre (dont au moins 12 jours consécutifs)"],
             ["Report", "Possible jusqu'au 31 mai de l'année suivante sur accord du manager"],
             ["Paiement en lieu de prise", "Interdit sauf départ de l'entreprise"]],
            [6*cm, 10.5*cm]
        )),
        ("h2", "1.2 Congés supplémentaires (ancienneté)"),
        ("table", (
            [["Ancienneté", "Jours supplémentaires"],
             ["5 à 10 ans", "1 jour ouvrable"],
             ["10 à 15 ans", "2 jours ouvrables"],
             ["15 ans et plus", "3 jours ouvrables"]],
            [6*cm, 10.5*cm]
        )),
    ])

    story += section("2. Congés pour événements familiaux", [
        ("p", "Des autorisations d'absence rémunérées sont accordées sur justificatifs pour les événements suivants, conformément à la convention collective de la métallurgie :"),
        ("table", (
            [["Événement", "Durée"],
             ["Mariage ou PACS du salarié", "5 jours ouvrés"],
             ["Naissance ou adoption d'un enfant", "3 jours ouvrés"],
             ["Mariage d'un enfant", "2 jours ouvrés"],
             ["Décès du conjoint, concubin ou partenaire PACS", "5 jours ouvrés"],
             ["Décès d'un enfant", "12 jours calendaires (loi Perruchot)"],
             ["Décès d'un parent, beau-parent", "3 jours ouvrés"],
             ["Décès d'un frère, soeur, beau-frère, belle-soeur", "3 jours ouvrés"],
             ["Annonce d'un handicap chez l'enfant", "2 jours ouvrés"]],
            [9*cm, 7.5*cm]
        )),
    ])

    story += section("3. Absences maladie et accident du travail", [
        ("h2", "3.1 Maladie ordinaire"),
        ("p", "En cas d'absence pour maladie, le salarié doit informer son manager et le service RH le jour même (avant 9h si possible) et transmettre un certificat médical dans les 48 heures. Le maintien de salaire est assuré selon les conditions suivantes :"),
        ("table", (
            [["Ancienneté", "Durée maintien salaire à 100%", "Puis à 50%"],
             ["Moins d'1 an", "Non applicable (CC Métallurgie)", "—"],
             ["1 à 5 ans", "30 jours", "30 jours"],
             ["5 à 10 ans", "40 jours", "40 jours"],
             ["Plus de 10 ans", "60 jours", "60 jours"]],
            [5*cm, 6.5*cm, 5*cm]
        )),
        ("note", "Le maintien de salaire intervient en complément des indemnités journalières versées par la CPAM. La carence CPAM (3 jours) est prise en charge par l'entreprise à partir d'1 an d'ancienneté."),
        ("h2", "3.2 Accident du travail"),
        ("p", "Tout accident survenu au travail doit être déclaré immédiatement au responsable hiérarchique et au service HSE. L'entreprise procède à la déclaration d'accident du travail auprès de la CPAM dans les 48 heures. Le maintien de salaire à 100% est assuré dès le 1er jour, sans condition d'ancienneté."),
    ])

    story += section("4. Autres absences autorisées", [
        ("b", "Congé maternité : durée légale (16 semaines minimum), salaire maintenu à 100% en complément des IJSS"),
        ("b", "Congé paternité et d'accueil de l'enfant : 28 jours calendaires (dont 4 obligatoires), maintien à 100%"),
        ("b", "Congé parental d'éducation : jusqu'aux 3 ans de l'enfant, non rémunéré, poste garanti au retour"),
        ("b", "Congé de proche aidant : jusqu'à 3 mois (renouvelable), non rémunéré, allocation possible via la CNSA"),
        ("b", "Congé sabbatique : accessible après 6 ans d'ancienneté, durée 6 à 11 mois, non rémunéré"),
    ])

    story += section("5. Procédure de demande", [
        ("p", "Toute demande de congé doit être effectuée via l'outil de gestion des absences (Workday), selon les délais de prévenance suivants :"),
        ("b", "Congés de moins de 5 jours : 1 semaine de préavis minimum"),
        ("b", "Congés de 5 à 15 jours : 3 semaines de préavis minimum"),
        ("b", "Congés de plus de 15 jours : 6 semaines de préavis minimum"),
        ("p", "Le manager dispose de 5 jours ouvrés pour valider ou refuser la demande. Un refus doit être motivé et peut donner lieu à un report dans les 3 mois suivants."),
    ])

    return build_doc("04_politique_conges_absences.pdf", story)


# ══════════════════════════════════════════════════════════════════════════════
# 5. GUIDE D'ONBOARDING
# ══════════════════════════════════════════════════════════════════════════════
def doc_onboarding():
    story = header_block(
        "Guide d'Intégration des Nouveaux Collaborateurs",
        "Onboarding — Programme 90 jours",
        "3.0", "2025"
    )

    story += section("Bienvenue chez Fictive Industrie !", [
        ("p", "Nous sommes ravis de vous accueillir au sein d'Fictive Industrie S.A., acteur majeur de la transformation des métaux et de l'industrie manufacturière en France depuis 1978. Nos 4 200 collaborateurs répartis sur 8 sites en France partagent une même ambition : l'excellence industrielle au service de nos clients."),
        ("p", "Ce guide a été conçu pour vous accompagner lors de vos 90 premiers jours et vous donner toutes les clés pour réussir votre intégration. N'hésitez pas à poser des questions — la curiosité est une qualité que nous valorisons !"),
    ])

    story += section("Avant votre arrivée (J-7)", [
        ("p", "Votre manager et votre référent RH ont préparé votre arrivée. Vous devriez avoir reçu par e-mail les informations suivantes :"),
        ("b", "Confirmation de votre date et heure d'arrivée, lieu de RDV (accueil principal)"),
        ("b", "Documents à apporter : pièce d'identité, RIB, justificatif de domicile, diplômes"),
        ("b", "Identifiants provisoires pour la plateforme d'onboarding en ligne (my.fictive-industrie.fr)"),
        ("b", "Planning de votre première semaine"),
        ("note", "Si vous n'avez pas reçu ces informations à J-3, contactez onboarding@fictive-industrie.fr"),
    ])

    story += section("Semaine 1 — Découverte et installation", [
        ("table", (
            [["Jour", "Activité", "Responsable"],
             ["Lundi", "Accueil RH, remise badge, équipements, visite du site", "RH + IT"],
             ["Lundi", "Déjeuner de bienvenue avec l'équipe", "Manager"],
             ["Mardi", "Formation sécurité & HSE obligatoire (1/2 journée)", "Service HSE"],
             ["Mardi", "Présentation des outils métier (ERP, messagerie, Workday)", "IT"],
             ["Mercredi", "Rencontre avec les parties prenantes clés", "Manager"],
             ["Jeudi", "Immersion opérationnelle — observation des processus", "Binôme"],
             ["Vendredi", "Point de fin de semaine avec le manager", "Manager"]],
            [2.5*cm, 8.5*cm, 5.5*cm]
        )),
    ])

    story += section("Mois 1 — Prise en main du poste", [
        ("p", "L'objectif du premier mois est de comprendre votre périmètre de responsabilités, identifier vos interlocuteurs clés et commencer à contribuer à votre équipe."),
        ("b", "Compléter les modules e-learning obligatoires (RGPD, sécurité, éthique) via la plateforme Fictive Academy"),
        ("b", "Participer aux réunions d'équipe hebdomadaires"),
        ("b", "Réaliser une cartographie de vos parties prenantes internes et externes"),
        ("b", "Fixer avec votre manager les objectifs du premier trimestre"),
        ("b", "Point d'étonnement à J+30 : document libre sur ce qui vous a frappé (positif ou à améliorer)"),
        ("h2", "Votre binôme d'intégration"),
        ("p", "Un collaborateur expérimenté (votre 'buddy') a été désigné pour vous accompagner pendant les 3 premiers mois. Ce n'est pas votre supérieur hiérarchique — vous pouvez lui poser toutes vos questions sans filtre, y compris les plus basiques !"),
    ])

    story += section("Mois 2 et 3 — Montée en compétences", [
        ("p", "Cette période est consacrée à la montée en autonomie et au développement de vos premières contributions tangibles."),
        ("b", "À J+60 : entretien intermédiaire avec votre manager pour ajuster les objectifs si nécessaire"),
        ("b", "Identification des formations prioritaires avec votre manager (plan de formation)"),
        ("b", "Participation à un projet transverse ou groupe de travail si pertinent"),
        ("b", "À J+90 : entretien de fin de période d'essai (si applicable) et bilan d'intégration complet"),
        ("note", "L'entretien de J+90 n'est pas un entretien de performance. C'est une conversation bi-directionnelle sur votre vécu, vos besoins et la confirmation mutuelle de la collaboration."),
    ])

    story += section("Contacts utiles", [
        ("table", (
            [["Service", "Contact", "Pour quoi ?"],
             ["RH / Onboarding", "onboarding@fictive-industrie.fr", "Questions administratives, documents"],
             ["IT Helpdesk", "it-support@fictive-industrie.fr / ext. 4444", "Problèmes techniques, accès"],
             ["HSE", "hse@fictive-industrie.fr", "Sécurité, accidents, EPI"],
             ["Paye", "paye@fictive-industrie.fr", "Bulletins de salaire, mutuelle"],
             ["CSE", "cse@fictive-industrie.fr", "Avantages sociaux, activités"]],
            [4*cm, 7.5*cm, 5*cm]
        )),
    ])

    return build_doc("05_guide_onboarding.pdf", story)


# ══════════════════════════════════════════════════════════════════════════════
# 6. POLITIQUE DE FORMATION
# ══════════════════════════════════════════════════════════════════════════════
def doc_formation():
    story = header_block(
        "Politique de Formation Professionnelle",
        "Plan de développement des compétences 2025",
        "2.1", "1er janvier 2025"
    )

    story += section("1. Ambition et cadre légal", [
        ("p", "Fictive Industrie investit chaque année plus de 2,5% de sa masse salariale dans la formation professionnelle de ses collaborateurs, dépassant ainsi l'obligation légale minimale de 1% (article L.6331-1 du Code du travail). Cette politique traduit notre conviction que le développement des compétences est un levier stratégique de compétitivité et de fidélisation des talents."),
        ("p", "La politique de formation s'inscrit dans le cadre de la loi du 5 septembre 2018 'Pour la liberté de choisir son avenir professionnel', qui a notamment créé le Compte Personnel de Formation (CPF) et l'obligation d'entretien professionnel bisannuel."),
    ])

    story += section("2. Dispositifs de formation disponibles", [
        ("h2", "2.1 Plan de développement des compétences"),
        ("p", "Le plan de développement des compétences est élaboré annuellement par la DRH en concertation avec les managers et le CSE. Il recense les actions de formation nécessaires pour adapter les compétences aux évolutions des métiers et maintenir l'employabilité des salariés."),
        ("table", (
            [["Type d'action", "Initiative", "Rémunération", "Frais pris en charge"],
             ["Formation obligatoire (sécurité, réglementaire)", "Employeur", "100% maintien salaire", "100%"],
             ["Formation développement métier", "Employeur ou salarié", "100% maintien salaire", "100%"],
             ["Formation hors temps de travail", "Salarié (accord employeur)", "Non", "100%"]],
            [5*cm, 3.5*cm, 4*cm, 4*cm]
        )),
        ("h2", "2.2 Compte Personnel de Formation (CPF)"),
        ("p", "Chaque salarié cumule des droits CPF à hauteur de 500 € par an (800 € pour les non-qualifiés), plafonnés à 5 000 € (8 000 €). Ces droits sont utilisables librement pour toute formation éligible, sans accord de l'employeur si réalisée hors temps de travail."),
        ("p", "Fictive Industrie encourage l'utilisation du CPF en abondant les droits des salariés souhaitant se former dans des domaines stratégiques pour l'entreprise. Renseignez-vous auprès du service formation pour connaître les abondements disponibles."),
        ("h2", "2.3 Validation des Acquis de l'Expérience (VAE)"),
        ("p", "La VAE permet d'obtenir tout ou partie d'une certification professionnelle sur la base de l'expérience. L'entreprise soutient les démarches VAE en accordant jusqu'à 24 heures d'absence autorisée rémunérée pour les phases d'accompagnement et de jury."),
    ])

    story += section("3. Entretien professionnel", [
        ("p", "Chaque salarié bénéficie d'un entretien professionnel tous les 2 ans avec son manager, distinct de l'entretien annuel d'évaluation. Cet entretien porte sur les perspectives d'évolution professionnelle, les formations souhaitées et la mobilité interne."),
        ("p", "Tous les 6 ans, un bilan récapitulatif est réalisé pour vérifier que le salarié a bénéficié d'au moins une action de formation, d'une progression salariale ou professionnelle, ou d'un entretien professionnel. En cas de manquement, l'entreprise est tenue d'abonder le CPF du salarié de 3 000 €."),
    ])

    story += section("4. Mobilité interne et évolution de carrière", [
        ("p", "Fictive Industrie s'engage à privilégier la mobilité interne avant tout recrutement externe. Les offres de postes internes sont publiées sur l'intranet RH (Workday) au minimum 2 semaines avant publication externe."),
        ("b", "Tout salarié peut candidater à un poste interne après 18 mois dans son poste actuel"),
        ("b", "Les candidatures internes sont examinées en priorité à profil équivalent"),
        ("b", "En cas de mobilité géographique, la société prend en charge les frais de déménagement selon le barème en vigueur"),
        ("b", "Un accompagnement de 3 mois par un tuteur est prévu pour toute mobilité vers un poste de nature différente"),
    ])

    story += section("5. Fictive Academy — notre plateforme de formation", [
        ("p", "La plateforme Fictive Academy (academy.fictive-industrie.fr) donne accès à plus de 800 modules e-learning en auto-formation, disponibles 24h/24. Elle propose des parcours certifiants dans les domaines suivants : management, sécurité industrielle, excellence opérationnelle (Lean, Six Sigma), digital & data, langues étrangères."),
        ("p", "Chaque salarié dispose d'un budget formation individuel de 1 200 € par an pour des formations externes (hors plan collectif), mobilisable sur validation du manager et de la DRH."),
        ("note", "Pour toute demande de formation, rendez-vous sur Workday > Onglet Formation, ou contactez formation@fictive-industrie.fr. Le service formation répond sous 5 jours ouvrés."),
    ])

    return build_doc("06_politique_formation.pdf", story)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Génération des documents RH — Fictive Industrie S.A.")
    paths = []
    paths.append(doc_reglement())
    paths.append(doc_teletravail())
    paths.append(doc_charte_info())
    paths.append(doc_conges())
    paths.append(doc_onboarding())
    paths.append(doc_formation())
    print(f"\nTerminé — {len(paths)} documents générés dans {OUTPUT_DIR}")
