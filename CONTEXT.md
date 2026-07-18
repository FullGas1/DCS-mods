# DCS-mods Context

Réservoir de mods pour le simulateur de vol DCS World, destinés à être partagés avec la communauté.

## Language

**Mod**:
Extension DCS World packagée dans un unique fichier ZIP contenant `entry.lua` et les assets associés (shapes, textures, sons). Installé dans `Saved Games\DCS.openbeta\Mods\tech\[nom_du_mod]\`. Un mod peut déclarer plusieurs plugins via plusieurs appels `declare_plugin()` dans son `entry.lua`.
_Avoid_: plugin, add-on, package

**Plugin**:
Unité fonctionnelle déclarée dans `entry.lua` via `declare_plugin(name, {...})`. Un mod peut contenir un ou plusieurs plugins. Chaque plugin a un `name` (identifiant DCS), un `developerName`, une `version`, et une `category`.
_Avoid_: mod, objet, unité

**Version affichée**:
La version reprise dans le catalogue est la valeur littérale du champ `version` dans `declare_plugin()` (ex: `"2.7"`). Si la valeur est une constante Lua (`__DCS_VERSION__` ou autre), on affiche `"DCS compatible"`.

**entry.lua**:
Script obligatoire, point d'entrée de chaque mod, chargé par DCS au démarrage. Donne le type et les informations du mod. Toujours présent à la racine du dossier d'installation.
_Avoid_: script principal, loader

**Static**:
Type DCS interne regroupant tout objet qui n'est ni un aircraft ni une groundUnit. Dans le catalogue, les statics sont subdivisés en catégories plus précises.
_Avoid_: objet, décor, scenery

**Catégories catalogue** (valeurs contrôlées du champ `category` dans `declare_plugin`) :

- `"Cargo"` — charges cargo et objets de fret
- `"Helipad"` — helipads et zones d'atterrissage hélicoptères
- `"Static Personnel"` — personnels statiques (figurines, civils, soldats non jouables)
- `"Infantry"` — unités d'infanterie jouables
- `"Vehicle"` — véhicules terrestres
- `"Naval"` — unités navales
- `"Aircraft"` — appareils
- `"Misc"` — tout ce qui ne rentre dans aucune autre catégorie

**Infantry unit**:
Catégorie de mod pour les unités d'infanterie DCS.
_Avoid_: soldat, fantassin, piéton

**Catalogue**:
README principal du repo listant tous les mods publiés, organisé par catégorie. En-tête unique avec le nom de l'auteur. Chaque entrée affiche : nom du mod + description courte + version + hyperlien vers le dossier du mod. Structure : tableau Markdown par catégorie. La description est extraite du champ `description` ajouté dans `declare_plugin()` dans `entry.lua` (champ ignoré par DCS, parsé par le CI). La version est lue depuis `entry.lua` (`declare_plugin`) ; si constante Lua, on affiche `"DCS compatible"`.
_Avoid_: index, liste, inventaire

**README mod template**:
Sections dans l'ordre : titre (`# mod name`), première image de `media/` si elle existe (insérée par le CI entre le titre et `## Description`), `## Description`, `## Installation` (avec chemin générique), `## Usage`, `## Screenshots / Videos`. Si `media/` contient plusieurs images, les images supplémentaires (2ème et suivantes) sont listées dans `## Screenshots / Videos` (une par ligne, Markdown pur), suivies du placeholder vidéo. Généré automatiquement à la création du dossier mod.

**Chemin d'installation générique**:
`..\Saved Games\DCS.openbeta\Mods\tech\[nom_du_mod]` — chemin de référence communiqué aux utilisateurs, à adapter selon leur configuration locale.
