#!/usr/bin/env python3
"""Merge funnel translations into locale/*/LC_MESSAGES/django.po and compile .mo."""
from __future__ import annotations

import sys
from pathlib import Path

import polib

ROOT = Path(__file__).resolve().parents[1]
LOCALE_DIR = ROOT / "locale"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "de": {
        "Riparazione Grandine Ticino": "Hagelschaden-Reparatur Tessin",
        "Riparazione danni da grandine in Ticino senza verniciatura. Preventivo gratuito in 24 ore con KESI SA.": (
            "Hagelschaden-Reparatur im Tessin ohne Lackierung. Kostenlose Offerte innerhalb von 24 Stunden mit KESI SA."
        ),
        "Ticino · Risposta in 24h": "Tessin · Antwort in 24 Std.",
        "Risparmia fino al 70% sulla grandine — senza verniciare.": (
            "Sparen Sie bis zu 70 %% bei Hagelschäden — ohne Lackierung."
        ),
        "Risparmia fino al 70%% sulla grandine — senza verniciare.": (
            "Sparen Sie bis zu 70 %% bei Hagelschäden — ohne Lackierung."
        ),
        "Invia le foto ora. Valutazione gratuita con KESI SA: 97 tecnici PDR, 30 anni di esperienza, sede a Riazzino.": (
            "Senden Sie jetzt Fotos. Kostenlose Bewertung mit KESI SA: 97 PDR-Techniker, 30 Jahre Erfahrung, Sitz in Riazzino."
        ),
        "Zero vernice: la tua auto resta originale": "Kein Lack: Ihr Auto bleibt original",
        "Riparazione in giorni, non settimane": "Reparatur in Tagen, nicht Wochen",
        "Servizio mobile in tutto il Ticino e Svizzera": "Mobiler Service im ganzen Tessin und in der Schweiz",
        "Stagione grandine 2026": "Hagelsaison 2026",
        "Slot di valutazione gratuita disponibili in Ticino — invia le foto oggi per una risposta entro 24 ore.": (
            "Kostenlose Bewertungsslots im Tessin verfügbar — senden Sie heute Fotos für eine Antwort innerhalb von 24 Stunden."
        ),
        "Confronto diretto": "Direkter Vergleich",
        "PDR vs carrozzeria tradizionale": "PDR vs traditionelle Karosserie",
        "La nostra missione": "Unsere Mission",
        "Ripariamo. Preserviamo. Innoviamo.": "Reparieren. Bewahren. Innovieren.",
        "KESI SA è carrozzeria alternativa: ripariamo il danno nel punto esatto, senza cambiare il pezzo e senza verniciatura. Meno costi, meno sprechi, stesso risultato.": (
            "KESI SA ist alternative Karosserie: Wir reparieren den Schaden genau am betroffenen Punkt, ohne Teiletausch und ohne Lackierung. Weniger Kosten, weniger Abfall, gleiches Ergebnis."
        ),
        "Certificazioni e valori": "Zertifizierungen und Werte",
        "Servizio in Svizzera": "Service in der Schweiz",
        "Riparazioni ecologiche": "Ökologische Reparaturen",
        "Evita questi errori": "Vermeiden Sie diese Fehler",
        "5 errori da non fare dopo la grandine": "5 Fehler nach einem Hagelschaden",
        "Come funziona": "So funktioniert es",
        "Il processo in 4 passi": "Der Ablauf in 4 Schritten",
        "Foto del danno": "Fotos des Schadens",
        "superfici pulite, luce naturale": "saubere Oberflächen, natürliches Licht",
        "Valutazione KESI": "KESI-Bewertung",
        "entro 24 ore lavorative": "innerhalb von 24 Arbeitsstunden",
        "Appuntamento": "Termin",
        "Riazzino o servizio mobile": "Riazzino oder mobiler Service",
        "Riparazione PDR": "PDR-Reparatur",
        "vernice originale intatta": "Originallack unberührt",
        "Officina KESI": "KESI-Werkstatt",
        "Prima": "Vorher",
        "Dopo": "Nachher",
        "Prima: danni da grandine con marcature PDR": "Vorher: Hagelschäden mit PDR-Markierungen",
        "Dopo: riparazione PDR in officina KESI": "Nachher: PDR-Reparatur in der KESI-Werkstatt",
        "Prima: ammaccature da grandine sul parafango": "Vorher: Hageldellen am Kotflügel",
        "Dopo: parafango ripristinato senza verniciatura": "Nachher: Kotflügel ohne Lackierung wiederhergestellt",
        "Fondatore": "Gründer",
        "Salvatore Catania": "Salvatore Catania",
        "Salvatore Catania — fondatore KESI SA": "Salvatore Catania — Gründer KESI SA",
        "Ogni ammaccatura è una sfida tecnica. Il nostro obiettivo è ripristinare il veicolo come se il danno non fosse mai esistito.": (
            "Jede Delle ist eine technische Herausforderung. Unser Ziel ist es, das Fahrzeug so wiederherzustellen, als hätte der Schaden nie existiert."
        ),
        "Pronto?": "Bereit?",
        "Richiedi il preventivo gratuito": "Kostenlose Offerte anfordern",
        "Compila il form e carica le foto: ti rispondiamo entro 24 ore.": (
            "Füllen Sie das Formular aus und laden Sie Fotos hoch: Wir antworten innerhalb von 24 Stunden."
        ),
        "Non aspettare! Il preventivo è <b>GRATUITO</b>": "Warten Sie nicht! Die Offerte ist <b>KOSTENLOS</b>",
        "Invia foto ora": "Jetzt Fotos senden",
        "Chiama": "Anrufen",
        "Carrozzeria tradizionale": "Traditionelle Karosserie",
        "PDR KESI o CARROZZERIA PARTNER": "PDR KESI oder PARTNER-KAROSSERIE",
        "Vernice": "Lack",
        "Ritocchi o verniciatura completa": "Ausbesserungen oder Komplettlackierung",
        "Originale preservata": "Original erhalten",
        "Tempi": "Dauer",
        "1–3 settimane": "1–3 Wochen",
        "1–3 giorni": "1–3 Tage",
        "Costo medio": "Durchschnittskosten",
        "Più alto": "Höher",
        "40–70% in meno": "40–70 %% weniger",
        "40–70%% in meno": "40–70 %% weniger",
        "Valore auto": "Fahrzeugwert",
        "Può diminuire": "Kann sinken",
        "Protetto": "Geschützt",
        "Passaggi del modulo": "Formularschritte",
        "Risposta entro 24 ore · Gratuito · Senza impegno": "Antwort in 24 Std. · Kostenlos · Unverbindlich",
        "Es. Locarno, Lugano, Bellinzona": "z. B. Locarno, Lugano, Bellinzona",
        "Preferenza di appuntamento": "Terminpräferenz",
        "Seleziona…": "Auswählen…",
        "Servizio Mobile": "Mobiler Service",
        "Servizio in Sede (Riazzino)": "Service vor Ort (Riazzino)",
        "Carica foto del danno": "Schadensfotos hochladen",
        "max 15 file": "max. 15 Dateien",
        "Foto chiare dei bolli su superfici pulite e asciutte.": "Klare Fotos der Dellen auf sauberen, trockenen Oberflächen.",
        "Quando è successo? Quanti bolli circa?": "Wann ist es passiert? Wie viele Dellen ungefähr?",
        "Marca, modello, anno": "Marke, Modell, Jahr",
        "Accetto i termini e acconsento a essere ricontattato per la valutazione del danno.": (
            "Ich akzeptiere die Bedingungen und stimme zu, für die Schadensbewertung kontaktiert zu werden."
        ),
        "Indietro": "Zurück",
        "Continua": "Weiter",
        "INVIA RICHIESTA GRATUITA": "KOSTENLOSE ANFRAGE SENDEN",
        "Contatto": "Kontakt",
        "Foto": "Fotos",
        "Invio": "Senden",
        "Accetta i termini per continuare.": "Akzeptieren Sie die Bedingungen, um fortzufahren.",
        "Carica almeno una foto del danno.": "Laden Sie mindestens ein Schadensfoto hoch.",
        "Totale allegati troppo grande per l'invio via email. Rimuovi alcuni file fino a tornare sotto i 20 MB.": (
            "Gesamtgrösse der Anhänge zu gross für den E-Mail-Versand. Entfernen Sie Dateien, bis Sie unter 20 MB sind."
        ),
        "Rimuovi": "Entfernen",
        "Grazie": "Danke",
        "Richiesta inviata!": "Anfrage gesendet!",
        "Grazie per aver contattato KESI SA tramite grandineticino.ch. Ti risponderemo entro 24 ore lavorative con una valutazione gratuita del danno.": (
            "Vielen Dank für Ihre Kontaktaufnahme mit KESI SA über grandineticino.ch. Wir antworten innerhalb von 24 Arbeitsstunden mit einer kostenlosen Schadensbewertung."
        ),
        "Cosa succede ora": "Was passiert jetzt",
        "Il nostro team analizza le foto che hai inviato": "Unser Team analysiert die von Ihnen gesendeten Fotos",
        "Ti contattiamo via telefono o email con la stima": "Wir kontaktieren Sie per Telefon oder E-Mail mit der Schätzung",
        "Fissiamo l'appuntamento per la riparazione PDR": "Wir vereinbaren den Termin für die PDR-Reparatur",
        "Torna alla pagina": "Zurück zur Seite",
        "Icona ecologia di": "Ökologie-Icon von",
        "PDR?": "PDR?",
        "PDR significa Paintless Dent Repair: levabolli senza verniciatura.": (
            "PDR bedeutet Paintless Dent Repair: Ausbeulen ohne Lackierung."
        ),
        "La vernice resta intatta?": "Bleibt der Lack intakt?",
        "Sì. Il PDR lavora sulla lamiera senza verniciare: la vernice di fabbrica resta originale e il valore del veicolo è protetto.": (
            "Ja. PDR arbeitet am Blech ohne zu lackieren: der Werkslack bleibt original und der Fahrzeugwert ist geschützt."
        ),
        "Dipende però dall'entità del danno: contattaci per una consulenza gratuita. Come carrozzieri professionisti ti diciamo se la tua auto grandinata è riparabile senza verniciatura.": (
            "Es hängt jedoch vom Schadensumfang ab: Kontaktieren Sie uns für eine kostenlose Beratung. Als professionelle Karosseriebetriebe sagen wir Ihnen, ob Ihr hagelschadengeschädigtes Auto ohne Lackierung reparierbar ist."
        ),
        "Quanto costa rispetto alla carrozzeria tradizionale?": "Was kostet es im Vergleich zur traditionellen Karosserie?",
        "In media il PDR costa dal 40% al 70% in meno rispetto a verniciatura e sostituzione pannelli, con tempi molto più brevi.": (
            "Im Durchschnitt kostet PDR 40 %% bis 70 %% weniger als Lackierung und Paneltausch, bei deutlich kürzeren Zeiten."
        ),
        "Si tratta di un risparmio indicativo, calcolato sul confronto con una riparazione tradizionale con verniciatura rispetto a un intervento senza riverniciatura eseguito da tecnici esperti in danni da grandine.": (
            "Dies ist eine Richtwert-Ersparnis, berechnet im Vergleich zwischen einer traditionellen Lackreparatur und einem Eingriff ohne Neulackierung durch erfahrene Hagelschaden-Techniker."
        ),
        "L'assicurazione copre i danni da grandine?": "Deckt die Versicherung Hagelschäden ab?",
        "In Svizzera i danni da grandine sono generalmente coperti dalla casco.": (
            "In der Schweiz sind Hagelschäden in der Regel durch die Vollkasko abgedeckt."
        ),
        "Verifichiamo noi se il tuo veicolo è coperto: con la foto della carta grigia possiamo gestire la Pratica per tuo conto.": (
            "Wir prüfen, ob Ihr Fahrzeug abgedeckt ist: Mit dem Foto des Fahrzeugausweises können wir die Anfrage für Sie bearbeiten."
        ),
        "Se è prevista una franchigia, te la comunichiamo subito così ci mettiamo d'accordo nel migliore dei modi.": (
            "Falls eine Selbstbeteiligung vorgesehen ist, teilen wir Ihnen das sofort mit, damit wir uns bestmöglich einigen."
        ),
        "Quanto tempo ci vuole?": "Wie lange dauert es?",
        "Molti interventi si completano da 1 a 3 giorni, contro settimane in carrozzeria tradizionale.": (
            "Viele Eingriffe werden in 1 bis 3 Tagen abgeschlossen, statt Wochen in der traditionellen Karosserie."
        ),
        "Dove intervenite in Ticino?": "Wo sind Sie im Tessin tätig?",
        "Sede a Riazzino e servizio mobile in tutto il canton Ticino e in tutta la Svizzera.": (
            "Sitz in Riazzino und mobiler Service im ganzen Kanton Tessin und in der ganzen Schweiz."
        ),
        "Aspettare settimane prima di fare il preventivo: l'auto potrebbe andare in danno totale in caso di grandinata o danno aggiuntivo": (
            "Wochen mit der Offerte warten: Bei weiterem Hagelschaden oder Zusatzschaden kann das Fahrzeug totalschaden werden"
        ),
        "Non sapere chi ripara la vostra macchina grandinata: KESI è una garanzia": (
            "Nicht zu wissen, wer Ihr hagelschadengeschädigtes Auto repariert: KESI ist eine Garantie"
        ),
        "Non fotografare tutti i bolli prima di portare l'auto in carrozzeria.": (
            "Nicht alle Dellen fotografieren, bevor Sie das Auto in die Karosserie bringen."
        ),
        "Non verificare la copertura assicurativa per danni da grandine.": (
            "Die Versicherungsdeckung für Hagelschäden nicht prüfen."
        ),
        "Scegliere il preventivo più basso senza controllare la qualità del lavoro.": (
            "Die günstigste Offerte wählen, ohne die Arbeitsqualität zu prüfen."
        ),
        "Compila tutti i campi obbligatori.": "Füllen Sie alle Pflichtfelder aus.",
        "Inserisci un numero di telefono valido (es. +41 79 123 45 67 o +39 333 123 4567).": (
            "Geben Sie eine gültige Telefonnummer ein (z. B. +41 79 123 45 67 oder +39 333 123 4567)."
        ),
        "Seleziona le preferenze di consegna.": "Wählen Sie die Terminpräferenz.",
        "Seleziona la preferenza di appuntamento.": "Wählen Sie die Terminpräferenz.",
        "Devi accettare i termini per inviare la richiesta.": "Sie müssen die Bedingungen akzeptieren, um die Anfrage zu senden.",
        "Prefisso internazionale": "Internationale Vorwahl",
        "79 123 45 67": "79 123 45 67",
        "Numero senza prefisso internazionale": "Nummer ohne internationale Vorwahl",
        "Inserisci un indirizzo email valido.": "Geben Sie eine gültige E-Mail-Adresse ein.",
        "Correggi i campi evidenziati e riprova.": "Bitte korrigieren Sie die markierten Felder und versuchen Sie es erneut.",
        "Puoi caricare al massimo %(max)s file.": "Sie können maximal %(max)s Dateien hochladen.",
        "Formato file non supportato. Usa JPG o PNG.": "Dateiformat nicht unterstützt. Verwenden Sie JPG oder PNG.",
        "Formato file non supportato. Carica solo immagini (JPG, PNG, HEIC, WebP, GIF, …).": (
            "Dateiformat nicht unterstützt. Laden Sie nur Bilder hoch (JPG, PNG, HEIC, WebP, GIF, …)."
        ),
        "Numero bolli non valido.": "Ungültige Anzahl Dellen.",
        "Grazie — richiesta ricevuta": "Danke — Anfrage erhalten",
        "KESI SA — Abbiamo ricevuto la tua richiesta": "KESI SA — Wir haben Ihre Anfrage erhalten",
        "Gentile cliente,": "Sehr geehrte Kundin, sehr geehrter Kunde,",
        "Grazie per averci contattato tramite grandineticino.ch.": "Vielen Dank für Ihre Kontaktaufnahme über grandineticino.ch.",
        "Abbiamo ricevuto le tue foto e i tuoi dati.": "Wir haben Ihre Fotos und Daten erhalten.",
        "Ti risponderemo entro 24 ore lavorative con una valutazione gratuita.": (
            "Wir antworten innerhalb von 24 Arbeitsstunden mit einer kostenlosen Bewertung."
        ),
        "Per urgenze puoi chiamarci al +41 78 967 43 37 o scriverci su WhatsApp.": (
            "Bei Dringlichkeit können Sie uns unter +41 78 967 43 37 anrufen oder uns auf WhatsApp schreiben."
        ),
        "Cordiali saluti,": "Freundliche Grüsse,",
        "Grandine Ticino - vorrei un preventivo": "Hagel Tessin - ich möchte eine Offerte",
    },
    "fr": {
        "Riparazione Grandine Ticino": "Réparation grêle Tessin",
        "Riparazione danni da grandine in Ticino senza verniciatura. Preventivo gratuito in 24 ore con KESI SA.": (
            "Réparation des dégâts de grêle au Tessin sans peinture. Devis gratuit sous 24 heures avec KESI SA."
        ),
        "Ticino · Risposta in 24h": "Tessin · Réponse sous 24 h",
        "Risparmia fino al 70% sulla grandine — senza verniciare.": (
            "Économisez jusqu'à 70 %% sur la grêle — sans repeindre."
        ),
        "Risparmia fino al 70%% sulla grandine — senza verniciare.": (
            "Économisez jusqu'à 70 %% sur la grêle — sans repeindre."
        ),
        "Invia le foto ora. Valutazione gratuita con KESI SA: 97 tecnici PDR, 30 anni di esperienza, sede a Riazzino.": (
            "Envoyez les photos maintenant. Évaluation gratuite avec KESI SA : 97 techniciens PDR, 30 ans d'expérience, siège à Riazzino."
        ),
        "Zero vernice: la tua auto resta originale": "Zéro peinture : votre voiture reste d'origine",
        "Riparazione in giorni, non settimane": "Réparation en jours, pas en semaines",
        "Servizio mobile in tutto il Ticino e Svizzera": "Service mobile dans tout le Tessin et la Suisse",
        "Stagione grandine 2026": "Saison grêle 2026",
        "Slot di valutazione gratuita disponibili in Ticino — invia le foto oggi per una risposta entro 24 ore.": (
            "Créneaux d'évaluation gratuite disponibles au Tessin — envoyez les photos aujourd'hui pour une réponse sous 24 heures."
        ),
        "Confronto diretto": "Comparaison directe",
        "PDR vs carrozzeria tradizionale": "PDR vs carrosserie traditionnelle",
        "La nostra missione": "Notre mission",
        "Ripariamo. Preserviamo. Innoviamo.": "Nous réparons. Nous préservons. Nous innovons.",
        "KESI SA è carrozzeria alternativa: ripariamo il danno nel punto esatto, senza cambiare il pezzo e senza verniciatura. Meno costi, meno sprechi, stesso risultato.": (
            "KESI SA est une carrosserie alternative : nous réparons le dommage exactement au bon endroit, sans changer la pièce et sans peinture. Moins de coûts, moins de gaspillage, même résultat."
        ),
        "Certificazioni e valori": "Certifications et valeurs",
        "Servizio in Svizzera": "Service en Suisse",
        "Riparazioni ecologiche": "Réparations écologiques",
        "Evita questi errori": "Évitez ces erreurs",
        "5 errori da non fare dopo la grandine": "5 erreurs à éviter après la grêle",
        "Come funziona": "Comment ça marche",
        "Il processo in 4 passi": "Le processus en 4 étapes",
        "Foto del danno": "Photos du dommage",
        "superfici pulite, luce naturale": "surfaces propres, lumière naturelle",
        "Valutazione KESI": "Évaluation KESI",
        "entro 24 ore lavorative": "sous 24 heures ouvrables",
        "Appuntamento": "Rendez-vous",
        "Riazzino o servizio mobile": "Riazzino ou service mobile",
        "Riparazione PDR": "Réparation PDR",
        "vernice originale intatta": "peinture d'origine intacte",
        "Officina KESI": "Atelier KESI",
        "Prima": "Avant",
        "Dopo": "Après",
        "Prima: danni da grandine con marcature PDR": "Avant : dégâts de grêle avec marquages PDR",
        "Dopo: riparazione PDR in officina KESI": "Après : réparation PDR dans l'atelier KESI",
        "Prima: ammaccature da grandine sul parafango": "Avant : bosses de grêle sur l'aile",
        "Dopo: parafango ripristinato senza verniciatura": "Après : aile restaurée sans peinture",
        "Fondatore": "Fondateur",
        "Salvatore Catania": "Salvatore Catania",
        "Salvatore Catania — fondatore KESI SA": "Salvatore Catania — fondateur KESI SA",
        "Ogni ammaccatura è una sfida tecnica. Il nostro obiettivo è ripristinare il veicolo come se il danno non fosse mai esistito.": (
            "Chaque bosse est un défi technique. Notre objectif est de restaurer le véhicule comme si le dommage n'avait jamais existé."
        ),
        "Pronto?": "Prêt ?",
        "Richiedi il preventivo gratuito": "Demandez un devis gratuit",
        "Compila il form e carica le foto: ti rispondiamo entro 24 ore.": (
            "Remplissez le formulaire et téléchargez les photos : nous répondons sous 24 heures."
        ),
        "Non aspettare! Il preventivo è <b>GRATUITO</b>": "N'attendez pas ! Le devis est <b>GRATUIT</b>",
        "Invia foto ora": "Envoyer les photos maintenant",
        "Chiama": "Appeler",
        "Carrozzeria tradizionale": "Carrosserie traditionnelle",
        "PDR KESI o CARROZZERIA PARTNER": "PDR KESI ou CARROSSERIE PARTENAIRE",
        "Vernice": "Peinture",
        "Ritocchi o verniciatura completa": "Retouches ou peinture complète",
        "Originale preservata": "Originale préservée",
        "Tempi": "Délais",
        "1–3 settimane": "1–3 semaines",
        "1–3 giorni": "1–3 jours",
        "Costo medio": "Coût moyen",
        "Più alto": "Plus élevé",
        "40–70% in meno": "40–70 %% de moins",
        "40–70%% in meno": "40–70 %% de moins",
        "Valore auto": "Valeur du véhicule",
        "Può diminuire": "Peut diminuer",
        "Protetto": "Protégé",
        "Passaggi del modulo": "Étapes du formulaire",
        "Risposta entro 24 ore · Gratuito · Senza impegno": "Réponse sous 24 h · Gratuit · Sans engagement",
        "Es. Locarno, Lugano, Bellinzona": "ex. Locarno, Lugano, Bellinzona",
        "Preferenza di appuntamento": "Préférence de rendez-vous",
        "Seleziona…": "Sélectionner…",
        "Servizio Mobile": "Service mobile",
        "Servizio in Sede (Riazzino)": "Service sur site (Riazzino)",
        "Carica foto del danno": "Télécharger des photos du dommage",
        "max 15 file": "max. 15 fichiers",
        "Foto chiare dei bolli su superfici pulite e asciutte.": "Photos nettes des bosses sur des surfaces propres et sèches.",
        "Quando è successo? Quanti bolli circa?": "Quand cela s'est-il produit ? Combien de bosses environ ?",
        "Marca, modello, anno": "Marque, modèle, année",
        "Accetto i termini e acconsento a essere ricontattato per la valutazione del danno.": (
            "J'accepte les conditions et consens à être recontacté pour l'évaluation du dommage."
        ),
        "Indietro": "Retour",
        "Continua": "Continuer",
        "INVIA RICHIESTA GRATUITA": "ENVOYER LA DEMANDE GRATUITE",
        "Contatto": "Contact",
        "Foto": "Photos",
        "Invio": "Envoi",
        "Accetta i termini per continuare.": "Acceptez les conditions pour continuer.",
        "Carica almeno una foto del danno.": "Téléchargez au moins une photo du dommage.",
        "Totale allegati troppo grande per l'invio via email. Rimuovi alcuni file fino a tornare sotto i 20 MB.": (
            "Taille totale des pièces jointes trop importante pour l'envoi par e-mail. Supprimez des fichiers jusqu'à revenir sous 20 Mo."
        ),
        "Rimuovi": "Supprimer",
        "Grazie": "Merci",
        "Richiesta inviata!": "Demande envoyée !",
        "Grazie per aver contattato KESI SA tramite grandineticino.ch. Ti risponderemo entro 24 ore lavorative con una valutazione gratuita del danno.": (
            "Merci d'avoir contacté KESI SA via grandineticino.ch. Nous vous répondrons sous 24 heures ouvrables avec une évaluation gratuite du dommage."
        ),
        "Cosa succede ora": "Que se passe-t-il maintenant",
        "Il nostro team analizza le foto che hai inviato": "Notre équipe analyse les photos que vous avez envoyées",
        "Ti contattiamo via telefono o email con la stima": "Nous vous contactons par téléphone ou e-mail avec l'estimation",
        "Fissiamo l'appuntamento per la riparazione PDR": "Nous fixons le rendez-vous pour la réparation PDR",
        "Torna alla pagina": "Retour à la page",
        "Icona ecologia di": "Icône écologie de",
        "PDR?": "PDR ?",
        "PDR significa Paintless Dent Repair: levabolli senza verniciatura.": (
            "PDR signifie Paintless Dent Repair : débosselage sans peinture."
        ),
        "La vernice resta intatta?": "La peinture reste-t-elle intacte ?",
        "Sì. Il PDR lavora sulla lamiera senza verniciare: la vernice di fabbrica resta originale e il valore del veicolo è protetto.": (
            "Oui. Le PDR travaille sur la tôle sans peindre : la peinture d'usine reste d'origine et la valeur du véhicule est protégée."
        ),
        "Dipende però dall'entità del danno: contattaci per una consulenza gratuita. Come carrozzieri professionisti ti diciamo se la tua auto grandinata è riparabile senza verniciatura.": (
            "Cela dépend toutefois de l'ampleur du dommage : contactez-nous pour une consultation gratuite. En tant que carrossiers professionnels, nous vous dirons si votre voiture endommagée par la grêle est réparable sans peinture."
        ),
        "Quanto costa rispetto alla carrozzeria tradizionale?": "Combien cela coûte-t-il par rapport à la carrosserie traditionnelle ?",
        "In media il PDR costa dal 40% al 70% in meno rispetto a verniciatura e sostituzione pannelli, con tempi molto più brevi.": (
            "En moyenne, le PDR coûte de 40 %% à 70 %% de moins que la peinture et le remplacement de panneaux, avec des délais bien plus courts."
        ),
        "Si tratta di un risparmio indicativo, calcolato sul confronto con una riparazione tradizionale con verniciatura rispetto a un intervento senza riverniciatura eseguito da tecnici esperti in danni da grandine.": (
            "Il s'agit d'une économie indicative, calculée en comparant une réparation traditionnelle avec peinture à une intervention sans repeinture réalisée par des techniciens experts en dégâts de grêle."
        ),
        "L'assicurazione copre i danni da grandine?": "L'assurance couvre-t-elle les dégâts de grêle ?",
        "In Svizzera i danni da grandine sono generalmente coperti dalla casco.": (
            "En Suisse, les dégâts de grêle sont généralement couverts par la casco."
        ),
        "Verifichiamo noi se il tuo veicolo è coperto: con la foto della carta grigia possiamo gestire la pratica per tuo conto.": (
            "Nous vérifions si votre véhicule est couvert : avec la photo de la carte grise, nous pouvons gérer la démarche pour vous."
        ),
        "Se è prevista una franchigia, te la comunichiamo subito così ci mettiamo d'accordo nel migliore dei modi.": (
            "Si une franchise est prévue, nous vous l'indiquons immédiatement afin de nous mettre d'accord au mieux."
        ),
        "Quanto tempo ci vuole?": "Combien de temps cela prend-il ?",
        "Molti interventi si completano da 1 a 3 giorni, contro settimane in carrozzeria tradizionale.": (
            "De nombreuses interventions se terminent en 1 à 3 jours, contre des semaines en carrosserie traditionnelle."
        ),
        "Dove intervenite in Ticino?": "Où intervenez-vous au Tessin ?",
        "Sede a Riazzino e servizio mobile in tutto il canton Ticino e in tutta la Svizzera.": (
            "Siège à Riazzino et service mobile dans tout le canton du Tessin et dans toute la Suisse."
        ),
        "Aspettare settimane prima di fare il preventivo: l'auto potrebbe andare in danno totale in caso di grandinata o danno aggiuntivo": (
            "Attendre des semaines avant de demander un devis : la voiture pourrait être déclarée perte totale en cas de nouvelle grêle ou dommage supplémentaire"
        ),
        "Non sapere chi ripara la vostra macchina grandinata: KESI è una garanzia": (
            "Ne pas savoir qui répare votre voiture endommagée par la grêle : KESI est une garantie"
        ),
        "Non fotografare tutti i bolli prima di portare l'auto in carrozzeria.": (
            "Ne pas photographier toutes les bosses avant d'emmener la voiture en carrosserie."
        ),
        "Non verificare la copertura assicurativa per danni da grandine.": (
            "Ne pas vérifier la couverture d'assurance pour les dégâts de grêle."
        ),
        "Scegliere il preventivo più basso senza controllare la qualità del lavoro.": (
            "Choisir le devis le plus bas sans vérifier la qualité du travail."
        ),
        "Compila tutti i campi obbligatori.": "Remplissez tous les champs obligatoires.",
        "Inserisci un numero di telefono valido (es. +41 79 123 45 67 o +39 333 123 4567).": (
            "Saisissez un numéro de téléphone valide (ex. +41 79 123 45 67 ou +39 333 123 4567)."
        ),
        "Seleziona le preferenze di consegna.": "Sélectionnez la préférence de rendez-vous.",
        "Seleziona la preferenza di appuntamento.": "Sélectionnez la préférence de rendez-vous.",
        "Devi accettare i termini per inviare la richiesta.": "Vous devez accepter les conditions pour envoyer la demande.",
        "Prefisso internazionale": "Indicatif international",
        "79 123 45 67": "79 123 45 67",
        "Numero senza prefisso internazionale": "Numéro sans indicatif international",
        "Inserisci un indirizzo email valido.": "Saisissez une adresse e-mail valide.",
        "Correggi i campi evidenziati e riprova.": "Corrigez les champs indiqués et réessayez.",
        "Puoi caricare al massimo %(max)s file.": "Vous pouvez télécharger au maximum %(max)s fichiers.",
        "Formato file non supportato. Usa JPG o PNG.": "Format de fichier non pris en charge. Utilisez JPG ou PNG.",
        "Formato file non supportato. Carica solo immagini (JPG, PNG, HEIC, WebP, GIF, …).": (
            "Format de fichier non pris en charge. Téléchargez uniquement des images (JPG, PNG, HEIC, WebP, GIF, …)."
        ),
        "Numero bolli non valido.": "Nombre de bosses invalide.",
        "Grazie — richiesta ricevuta": "Merci — demande reçue",
        "KESI SA — Abbiamo ricevuto la tua richiesta": "KESI SA — Nous avons reçu votre demande",
        "Gentile cliente,": "Cher client, chère cliente,",
        "Grazie per averci contattato tramite grandineticino.ch.": "Merci de nous avoir contactés via grandineticino.ch.",
        "Abbiamo ricevuto le tue foto e i tuoi dati.": "Nous avons reçu vos photos et vos données.",
        "Ti risponderemo entro 24 ore lavorative con una valutazione gratuita.": (
            "Nous vous répondrons sous 24 heures ouvrables avec une évaluation gratuite."
        ),
        "Per urgenze puoi chiamarci al +41 78 967 43 37 o scriverci su WhatsApp.": (
            "En cas d'urgence, appelez-nous au +41 78 967 43 37 ou écrivez-nous sur WhatsApp."
        ),
        "Cordiali saluti,": "Cordialement,",
        "Grandine Ticino - vorrei un preventivo": "Grêle Tessin - je souhaite un devis",
    },
    "en": {
        "Riparazione Grandine Ticino": "Hail Repair Ticino",
        "Riparazione danni da grandine in Ticino senza verniciatura. Preventivo gratuito in 24 ore con KESI SA.": (
            "Hail damage repair in Ticino without repainting. Free quote within 24 hours with KESI SA."
        ),
        "Ticino · Risposta in 24h": "Ticino · Reply within 24h",
        "Risparmia fino al 70% sulla grandine — senza verniciare.": (
            "Save up to 70%% on hail damage — without repainting."
        ),
        "Risparmia fino al 70%% sulla grandine — senza verniciare.": (
            "Save up to 70%% on hail damage — without repainting."
        ),
        "Invia le foto ora. Valutazione gratuita con KESI SA: 97 tecnici PDR, 30 anni di esperienza, sede a Riazzino.": (
            "Send photos now. Free assessment with KESI SA: 97 PDR technicians, 30 years of experience, based in Riazzino."
        ),
        "Zero vernice: la tua auto resta originale": "Zero paint: your car stays original",
        "Riparazione in giorni, non settimane": "Repair in days, not weeks",
        "Servizio mobile in tutto il Ticino e Svizzera": "Mobile service throughout Ticino and Switzerland",
        "Stagione grandine 2026": "Hail season 2026",
        "Slot di valutazione gratuita disponibili in Ticino — invia le foto oggi per una risposta entro 24 ore.": (
            "Free assessment slots available in Ticino — send photos today for a reply within 24 hours."
        ),
        "Confronto diretto": "Direct comparison",
        "PDR vs carrozzeria tradizionale": "PDR vs traditional body shop",
        "La nostra missione": "Our mission",
        "Ripariamo. Preserviamo. Innoviamo.": "We repair. We preserve. We innovate.",
        "KESI SA è carrozzeria alternativa: ripariamo il danno nel punto esatto, senza cambiare il pezzo e senza verniciatura. Meno costi, meno sprechi, stesso risultato.": (
            "KESI SA is alternative bodywork: we repair damage exactly where it is, without replacing parts or repainting. Lower costs, less waste, same result."
        ),
        "Certificazioni e valori": "Certifications and values",
        "Servizio in Svizzera": "Service in Switzerland",
        "Riparazioni ecologiche": "Eco-friendly repairs",
        "Evita questi errori": "Avoid these mistakes",
        "5 errori da non fare dopo la grandine": "5 mistakes to avoid after hail damage",
        "Come funziona": "How it works",
        "Il processo in 4 passi": "The 4-step process",
        "Foto del danno": "Damage photos",
        "superfici pulite, luce naturale": "clean surfaces, natural light",
        "Valutazione KESI": "KESI assessment",
        "entro 24 ore lavorative": "within 24 business hours",
        "Appuntamento": "Appointment",
        "Riazzino o servizio mobile": "Riazzino or mobile service",
        "Riparazione PDR": "PDR repair",
        "vernice originale intatta": "original paint intact",
        "Officina KESI": "KESI workshop",
        "Prima": "Before",
        "Dopo": "After",
        "Prima: danni da grandine con marcature PDR": "Before: hail damage with PDR markings",
        "Dopo: riparazione PDR in officina KESI": "After: PDR repair at KESI workshop",
        "Prima: ammaccature da grandine sul parafango": "Before: hail dents on the wing",
        "Dopo: parafango ripristinato senza verniciatura": "After: wing restored without repainting",
        "Fondatore": "Founder",
        "Salvatore Catania": "Salvatore Catania",
        "Salvatore Catania — fondatore KESI SA": "Salvatore Catania — KESI SA founder",
        "Ogni ammaccatura è una sfida tecnica. Il nostro obiettivo è ripristinare il veicolo come se il danno non fosse mai esistito.": (
            "Every dent is a technical challenge. Our goal is to restore the vehicle as if the damage never existed."
        ),
        "Pronto?": "Ready?",
        "Richiedi il preventivo gratuito": "Request your free quote",
        "Compila il form e carica le foto: ti rispondiamo entro 24 ore.": (
            "Fill in the form and upload photos: we reply within 24 hours."
        ),
        "Non aspettare! Il preventivo è <b>GRATUITO</b>": "Don't wait! The quote is <b>FREE</b>",
        "Invia foto ora": "Send photos now",
        "Chiama": "Call",
        "Carrozzeria tradizionale": "Traditional body shop",
        "PDR KESI o CARROZZERIA PARTNER": "PDR KESI or PARTNER BODY SHOP",
        "Vernice": "Paint",
        "Ritocchi o verniciatura completa": "Touch-ups or full repaint",
        "Originale preservata": "Original preserved",
        "Tempi": "Time",
        "1–3 settimane": "1–3 weeks",
        "1–3 giorni": "1–3 days",
        "Costo medio": "Average cost",
        "Più alto": "Higher",
        "40–70% in meno": "40–70% less",
        "40–70%% in meno": "40–70% less",
        "Valore auto": "Car value",
        "Può diminuire": "May decrease",
        "Protetto": "Protected",
        "Passaggi del modulo": "Form steps",
        "Risposta entro 24 ore · Gratuito · Senza impegno": "Reply within 24h · Free · No obligation",
        "Es. Locarno, Lugano, Bellinzona": "e.g. Locarno, Lugano, Bellinzona",
        "Preferenza di appuntamento": "Appointment preference",
        "Seleziona…": "Select…",
        "Servizio Mobile": "Mobile service",
        "Servizio in Sede (Riazzino)": "On-site service (Riazzino)",
        "Carica foto del danno": "Upload damage photos",
        "max 15 file": "max 15 files",
        "Foto chiare dei bolli su superfici pulite e asciutte.": "Clear photos of dents on clean, dry surfaces.",
        "Quando è successo? Quanti bolli circa?": "When did it happen? Roughly how many dents?",
        "Marca, modello, anno": "Make, model, year",
        "Accetto i termini e acconsento a essere ricontattato per la valutazione del danno.": (
            "I accept the terms and agree to be contacted for damage assessment."
        ),
        "Indietro": "Back",
        "Continua": "Continue",
        "INVIA RICHIESTA GRATUITA": "SEND FREE REQUEST",
        "Contatto": "Contact",
        "Foto": "Photos",
        "Invio": "Submit",
        "Accetta i termini per continuare.": "Accept the terms to continue.",
        "Carica almeno una foto del danno.": "Upload at least one damage photo.",
        "Totale allegati troppo grande per l'invio via email. Rimuovi alcuni file fino a tornare sotto i 20 MB.": (
            "Total attachment size too large for email delivery. Remove files until you are under 20 MB."
        ),
        "Rimuovi": "Remove",
        "Grazie": "Thank you",
        "Richiesta inviata!": "Request sent!",
        "Grazie per aver contattato KESI SA tramite grandineticino.ch. Ti risponderemo entro 24 ore lavorative con una valutazione gratuita del danno.": (
            "Thank you for contacting KESI SA via grandineticino.ch. We will reply within 24 business hours with a free damage assessment."
        ),
        "Cosa succede ora": "What happens next",
        "Il nostro team analizza le foto che hai inviato": "Our team reviews the photos you sent",
        "Ti contattiamo via telefono o email con la stima": "We contact you by phone or email with the estimate",
        "Fissiamo l'appuntamento per la riparazione PDR": "We schedule the PDR repair appointment",
        "Torna alla pagina": "Back to page",
        "Icona ecologia di": "Ecology icon by",
        "PDR?": "PDR?",
        "PDR significa Paintless Dent Repair: levabolli senza verniciatura.": (
            "PDR means Paintless Dent Repair: dent removal without repainting."
        ),
        "La vernice resta intatta?": "Does the paint stay intact?",
        "Sì. Il PDR lavora sulla lamiera senza verniciare: la vernice di fabbrica resta originale e il valore del veicolo è protetto.": (
            "Yes. PDR works on the metal without painting: factory paint stays original and the vehicle's value is protected."
        ),
        "Dipende però dall'entità del danno: contattaci per una consulenza gratuita. Come carrozzieri professionisti ti diciamo se la tua auto grandinata è riparabile senza verniciatura.": (
            "However, it depends on the extent of the damage: contact us for a free consultation. As professional body shops, we will tell you if your hail-damaged car can be repaired without repainting."
        ),
        "Quanto costa rispetto alla carrozzeria tradizionale?": "How much does it cost compared to traditional bodywork?",
        "In media il PDR costa dal 40% al 70% in meno rispetto a verniciatura e sostituzione pannelli, con tempi molto più brevi.": (
            "On average, PDR costs 40%% to 70%% less than repainting and panel replacement, with much shorter turnaround."
        ),
        "Si tratta di un risparmio indicativo, calcolato sul confronto con una riparazione tradizionale con verniciatura rispetto a un intervento senza riverniciatura eseguito da tecnici esperti in danni da grandine.": (
            "This is an indicative saving, calculated by comparing traditional repainting with a non-repainting repair carried out by expert hail-damage technicians."
        ),
        "L'assicurazione copre i danni da grandine?": "Does insurance cover hail damage?",
        "In Svizzera i danni da grandine sono generalmente coperti dalla casco.": (
            "In Switzerland, hail damage is generally covered by comprehensive insurance."
        ),
        "Verifichiamo noi se il tuo veicolo è coperto: con la foto della carta grigia possiamo gestire la Pratica per tuo conto.": (
            "We check whether your vehicle is covered: with a photo of the registration document we can handle the process for you."
        ),
        "Se è prevista una franchigia, te la comunichiamo subito così ci mettiamo d'accordo nel migliore dei modi.": (
            "If a deductible applies, we tell you right away so we can agree on the best approach."
        ),
        "Quanto tempo ci vuole?": "How long does it take?",
        "Molti interventi si completano da 1 a 3 giorni, contro settimane in carrozzeria tradizionale.": (
            "Many repairs are completed in 1 to 3 days, versus weeks at a traditional body shop."
        ),
        "Dove intervenite in Ticino?": "Where do you operate in Ticino?",
        "Sede a Riazzino e servizio mobile in tutto il canton Ticino e in tutta la Svizzera.": (
            "Based in Riazzino with mobile service throughout Canton Ticino and all of Switzerland."
        ),
        "Aspettare settimane prima di fare il preventivo: l'auto potrebbe andare in danno totale in caso di grandinata o danno aggiuntivo": (
            "Waiting weeks before getting a quote: the car could become a total loss if hail strikes again or additional damage occurs"
        ),
        "Non sapere chi ripara la vostra macchina grandinata: KESI è una garanzia": (
            "Not knowing who repairs your hail-damaged car: KESI is a guarantee"
        ),
        "Non fotografare tutti i bolli prima di portare l'auto in carrozzeria.": (
            "Not photographing all dents before taking the car to the body shop."
        ),
        "Non verificare la copertura assicurativa per danni da grandine.": (
            "Not checking insurance coverage for hail damage."
        ),
        "Scegliere il preventivo più basso senza controllare la qualità del lavoro.": (
            "Choosing the lowest quote without checking work quality."
        ),
        "Compila tutti i campi obbligatori.": "Fill in all required fields.",
        "Inserisci un numero di telefono valido (es. +41 79 123 45 67 o +39 333 123 4567).": (
            "Enter a valid phone number (e.g. +41 79 123 45 67 or +39 333 123 4567)."
        ),
        "Seleziona le preferenze di consegna.": "Select your appointment preference.",
        "Seleziona la preferenza di appuntamento.": "Select your appointment preference.",
        "Devi accettare i termini per inviare la richiesta.": "You must accept the terms to submit the request.",
        "Prefisso internazionale": "International prefix",
        "79 123 45 67": "79 123 45 67",
        "Numero senza prefisso internazionale": "Number without international prefix",
        "Inserisci un indirizzo email valido.": "Enter a valid email address.",
        "Correggi i campi evidenziati e riprova.": "Please correct the highlighted fields and try again.",
        "Puoi caricare al massimo %(max)s file.": "You can upload at most %(max)s files.",
        "Formato file non supportato. Usa JPG o PNG.": "Unsupported file format. Use JPG or PNG.",
        "Formato file non supportato. Carica solo immagini (JPG, PNG, HEIC, WebP, GIF, …).": (
            "Unsupported file format. Upload images only (JPG, PNG, HEIC, WebP, GIF, …)."
        ),
        "Numero bolli non valido.": "Invalid dent count.",
        "Grazie — richiesta ricevuta": "Thank you — request received",
        "KESI SA — Abbiamo ricevuto la tua richiesta": "KESI SA — We received your request",
        "Gentile cliente,": "Dear customer,",
        "Grazie per averci contattato tramite grandineticino.ch.": "Thank you for contacting us via grandineticino.ch.",
        "Abbiamo ricevuto le tue foto e i tuoi dati.": "We have received your photos and details.",
        "Ti risponderemo entro 24 ore lavorative con una valutazione gratuita.": (
            "We will reply within 24 business hours with a free assessment."
        ),
        "Per urgenze puoi chiamarci al +41 78 967 43 37 o scriverci su WhatsApp.": (
            "For urgent matters, call us on +41 78 967 43 37 or message us on WhatsApp."
        ),
        "Cordiali saluti,": "Kind regards,",
        "Grandine Ticino - vorrei un preventivo": "Hail Ticino - I would like a quote",
    },
}


def merge_locale(lang: str) -> tuple[int, int]:
    po_path = LOCALE_DIR / lang / "LC_MESSAGES" / "django.po"
    mo_path = LOCALE_DIR / lang / "LC_MESSAGES" / "django.mo"
    po = polib.pofile(str(po_path))
    added = 0
    updated = 0

    for msgid, msgstr in TRANSLATIONS[lang].items():
        entry = po.find(msgid)
        if entry is None:
            po.append(polib.POEntry(msgid=msgid, msgstr=msgstr))
            added += 1
        elif entry.msgstr != msgstr:
            entry.msgstr = msgstr
            updated += 1

    po.save(str(po_path))
    po.save_as_mofile(str(mo_path))
    return added, updated


def main() -> int:
    for lang in ("de", "fr", "en"):
        added, updated = merge_locale(lang)
        print(f"{lang}: +{added} new, ~{updated} updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
