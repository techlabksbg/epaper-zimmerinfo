 # E-Paper Display mit Schulzimmerbelegungsplan.

## Idee
  * Input ICS + aktuelles Datum
  * Erzeugung einer 800x480 PNG-Datei (vorzugsweise via vektorielles Format).
  * Dithering und Konvertierung in 96kB binäre Daten.
  * Bereitstellen der Daten auf dem Server
  * ESP32 pollt Server via https, holt Daten, stellt diese auf dem Display dar.

ESP32 identifiziert gegenüber dem Server (z.B. via Mac-Adresse).


