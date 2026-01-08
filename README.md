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

## Real-Life-Validierung (Champions League 2024/25)

Zur Plausibilitätsprüfung wurde das Simulationsergebnis mit realen Daten
der Champions-League-Liga-Phase 2024/25 verglichen. Die Einordnung
„schwach“ erfolgt analog zur Simulation über einen Elo-Schwellenwert von
1500 Punkten (ClubElo).

**Ergebnis:**
- Schwache Teams in Top 8: **0 / 8**
- Schwache Teams in Top 24: **0 / 24**

Damit zeigt sich, dass sowohl in der Realität als auch in der Simulation
keine klar schwächeren Teams die oberen Platzierungen erreichen. Dies
spricht dafür, dass das Swiss-Format starke Teams zuverlässig nach oben
sortiert. Der Vergleich dient als Plausibilitätscheck und ersetzt keine
statistische Analyse, da nur eine einzelne Saison betrachtet wird.

## Autoren
Julian Eberl  
Samuel Bonk  
Yannic Leinweber
