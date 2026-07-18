# DCS-mods Context

Réservoir de mods pour le simulateur de vol DCS World, destinés à être partagés avec la communauté.

## Language

**Mod**:
Extension DCS World packagée dans un unique fichier ZIP contenant `entry.lua` et les assets associés (shapes, textures, sons). Installé dans `Saved Games\DCS.openbeta\Mods\tech\[nom_du_mod]\`.
_Avoid_: plugin, add-on, package

**entry.lua**:
Script obligatoire, point d'entrée de chaque mod, chargé par DCS au démarrage. Donne le type et les informations du mod. Toujours présent à la racine du dossier d'installation.
_Avoid_: script principal, loader

**Static**:
Catégorie de mod regroupant tout objet DCS qui n'est ni un aircraft ni une groundUnit — fortifications, charges cargo, helipads, obstacles, décors, etc.
_Avoid_: objet, décor, scenery

**Infantry unit**:
Catégorie de mod pour les unités d'infanterie DCS.
_Avoid_: soldat, fantassin, piéton

**Catalogue**:
README principal du repo listant tous les mods publiés, organisé par catégorie, avec un hyperlien vers chaque dossier de mod.
_Avoid_: index, liste, inventaire

**Chemin d'installation générique**:
`..\Saved Games\DCS.openbeta\Mods\tech\[nom_du_mod]` — chemin de référence communiqué aux utilisateurs, à adapter selon leur configuration locale.
