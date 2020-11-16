# logger

Cette application permet l'acquisition de températures et d'états électriques pour la surveillance du chauffage et de l'eau chaude. 
La mesure de température est basée sur des capteurs ds 18b20 et la mesure d'états sur des capteurs ds2413 avec une électronique dédicacée.

##### Applications:
- logger : acquisition des données est activée par crontab toutes les minutes 24/24 365/365
- monitor : permet l'analyse et l'affichage graphiques des mesures
