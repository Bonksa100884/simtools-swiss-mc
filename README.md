# Simtools – Monte-Carlo-Simulation des Champions-League-Swiss-Formats

## Ziel der Arbeit
In dieser Studienarbeit untersuchen wir das neue UEFA-Champions-League-Format (Swiss Model)
mithilfe einer Monte-Carlo-Simulation.

Zentrale Fragestellung:
Wie häufig schaffen es schwache Teams im neuen Swiss-Format in die Top 8 bzw. Top 24
und wie unterscheidet sich dies vom alten Gruppenphasen-Format?

## Methodik
- Modellierung der Teamstärken über vereinfachte Elo-Ratings
- Simulation einzelner Spiele mit Elo-basierter Siegwahrscheinlichkeit und fixer Remiswahrscheinlichkeit
- Durchführung vieler simulierter Saisons (Monte Carlo)
- Vergleich zweier Formate:
  - Neues Swiss-Format (Top 8 / Top 24)
  - Altes Gruppenphasen-Format (Top 2 pro Gruppe / Gruppensieger)

## Projektstruktur
- src/ – Python-Code der Simulationen
- data/ – Ergebnisdaten (CSV)
- figures/ – Visualisierungen (Plots)
- notebook/ – Jupyter Notebooks (optional)
- reports/ – Report und Präsentation

## Ausführung
Vom Projektverzeichnis aus:
python3 src/compare.py

Optional (falls matplotlib installiert ist):
python3 src/plot_results.py

## Annahmen und Limitierungen
- Vereinfachte Abbildung des Swiss-Formats (potbasierte Gegnerauswahl)
- Keine Tiebreaker (z.B. Torverhältnis, direkte Duelle)
- Kein Heim-/Auswärtsvorteil
- Synthetische Elo-Werte statt realer Teamdaten

## Autoren
Julian Eberl  
Samuel Bonk  
Yannic Leinweber
