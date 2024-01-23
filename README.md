 # E-Paper Display mit Schulzimmerbelegungsplan.

## Idee
  * Input ICS + aktuelles Datum
  * Erzeugung einer 800x480 PNG-Datei (vorzugsweise via vektorielles Format).
  * Dithering und Konvertierung in 96kB binäre Daten.
  * Bereitstellen der Daten auf dem Server
  * ESP32 pollt Server via https, holt Daten, stellt diese auf dem Display dar.

ESP32 identifiziert gegenüber dem Server (z.B. via Mac-Adresse).

## Links zu ReadMe 
[Hier](basics/ics/README.md) geht es zum icalender  
[Hier](INSTALL.md) geht es zur benötigten Software