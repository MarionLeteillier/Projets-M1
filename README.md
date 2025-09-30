# Projets-M1

[Technologies vocales TTS (PDF)](./technologies_vocales_examen_final_individuel.pdf) 
Évaluation écrite des fondamentaux des technologies de la parole : pipeline TTS/ASR (front-end/back-end), méthodes classiques vs neuronales et limites en dialogue spontané. Une partie appliquée porte sur la grammaire de transcription (orthographe → phonétique) : ordre des règles, détection des redondances et corrections.  

[Théorie des langages RegEx (PDF)](./théorie_des_langages_devoir_maison_individuel.pdf)
Constitution d’un petit corpus (résumés DUMAS) et conception d’une expression régulière capable de détecter/extraire les annonces de plan (1re/2e/3e partie, connecteurs « Ensuite », « Enfin », etc.), puis évaluation de la généralisation sur d’autres disciplines.

[Exposé Base et éthique du TAL (PDF)](./bases_ethique_TAL_Projet.pdf) Exposé sur les “thanabots” et la résurrection numérique : étude de cas (Alexa/voice cloning, Eternime, Project December, deepfakes – pub d’Elis Regina, Black Mirror “Be Right Back”) et mise en perspective éthique & juridique (consentement post-mortem, deuil, exploitation commerciale, RGPD/France, RUFADAA, etc.).  

[Compte-rendu de corpus écrits (PDF)](./corpus_ecrits_inception_projet.pdf)
Compte-rendu d’annotation de coréférence sur des contes : justification des choix (anaphores zéro, pronoms clitiques, cataphores, métonymies), adjudication des désaccords, et scores inter-annotateurs (0.35 à 1.00). Discussion des ambiguïtés fréquentes (discours direct, multiplicité de personnages) et mini-analyse statistique (pronoms, anaphores, longueur des textes). Inception = plateforme web open-source d’annotation de textes pour le TAL/NLP, conçue pour des projets multi-utilisateurs et pour des tâches sémantiques avancées.
[Captures d'annotations (PDF)](./captures_ecran_textes_finaux.pdf)
Jeu de captures d’annotations (.conllu) des textes finaux servant d’illustrations/annexes au projet d’annotation.

[Compte-rendu de corpus oraux et multimodaux (PDF)](./corpus_oraux_projet.pdf)
Analyse d’interactions en grande section autour d'un conte : transcription (segmentation respi/pauses), alignement phonologique BAS Web Services / MAUS → TextGrid, schéma d’annotation (types de phrases, questions ouvertes/fermées, interventions de la maîtresse) puis synthèse des résultats par élève (3 vidéos). 
[Fichier Praat TextGrid (txt)](./exemple_textgrid_praat_104C0005merged__2_.txt)
Fichier Praat TextGrid alignés au temps

[Compte-rendu de formalisme / chunker (PDF)](./compterendu_chunker_formalisme_individuel.pdf)  
Implémentation d’un [chunker](./chunker.py) en Python qui segmente des phrases en groupes (GN/PN, GV/SV, etc.) à partir d’un [lexique](./lexique.txt) et d’une [base de règles](./regles.txt). Pipeline : pré-tokenisation → application séquentielle des règles → [sortie XML](./sortie_chunker.xml) validée par la [dtd](./chunker.dtd) → [visualisation HTML/CSS](./chunking_live.html). Démonstration sur un article satirique (Le Gorafi) avec un [texte](./texte.txt). Évaluation par comparaison à une segmentation manuelle de référence [Excel](./chunk_excel.pdf) , avec analyse d’erreurs et pistes d’amélioration. Explication des choix de modélisation, des expérimentations, des limites et des pistes d’amélioration.

[Exposé Gestion de projet OCR (PDF)](./gestiondeprojet_OCR.pdf)
Conception d’un cours en ligne sur l’OCR (Moodle) pour combler un manque dans la formation TAL. Objectifs **SMART** (publication avant mi-avril, cible de performance ~70 % sur l’évaluation), **parties prenantes**, **personae**, **story-mapping** → **backlog** priorisé, planification/échéances, et bilans **RH/RSE**.  

[Cahier des charges — Projet Programmation Web & TAL (PDF)](./Compte%20rendu%20.pdf)  
Application pour les enseignants pour gérer des **dictées** : création d’une dictée par l'enseignant, passation par les élèves, **correction** et **statistiques**, plus **exports** par élève et par dictée. Le cahier des charges précise l’**analyse orthographique automatique** (distance de **Levenshtein**, lexique avec **catégorie/lemme/désinence**, détection accent / désinence / segmentation / omission / ponctuation), l’**intégration LanguageTool** et le lien **Le Conjugueur**. Conception d’un CRUD web complet, modélisation SQL, intégration d’API/outils, logique métier (analyse/correction) et production d’exports.
- Base de données (dumps) : [eleves.sql](./eleves%20(1).sql) · [dictees.sql](./dictees%20(2).sql) · [lexique.sql](./lexique%20(2).sql) · [reponses.sql](./reponses%20(1).sql)  
- Code (dossier `app/`) : [index.php](./app/index.php) · [passation.php](./app/passation.php) · [create_dictee.php](./app/create_dictee.php) · [save_dictee.php](./app/save_dictee.php) · [analyser_reponse.php](./app/analyser_reponse.php) · [stats.php](./app/stats.php) · [export_par_dictee.php](./app/export_par_dictee.php) · [export_par_eleve.php](./app/export_par_eleve.php) · [correction_externe.php](./app/correction_externe.php) · [connexion.php](./app/connexion.php)

[Compte rendu Programmation WEB (PDF)](./Programmation_web.pdf)  
Mini-site **HTML/CSS** de révision *Français CE1* : pages **Accueil**, **Lexique**, **Conjugaison**, **Grammaire**, **Orthographe**, **Lecture**, **Dictée**, **Bilan**. Mise en forme via [`styles.css`](./styles.css) et médias d’illustration.
- Pages : [accueil1.html](./accueil1.html) · [lexique.html](./lexique.html) · [conjugaison.html](./conjugaison.html) · [grammaire.html](./grammaire.html) · [orthographe.html](./orthographe.html) · [lecture.html](./lecture.html) · [dictée.html](./dictée.html) · [bilan.html](./bilan.html)  
- Assets : `vrai.png`, `faux.png`, `gifvrai.gif`, `faux.gif`, `vraianimal.jpg`

[Notebook Python](./Python%20Projet%201.ipynb)
Lecture d’un fichier **CoNLL-U** → génération d’un **JSON** récapitulatif : `nbToks`, `nbSents`, `nbForms`, `nbPuncts`, `nbTypes`, longueurs moyennes, indexes de fréquences par **POS** (noms, verbes, adj., adv., lemmes) et **ngrams** (longueurs *nMin…nMax*). 






