import re
import xml.etree.ElementTree as ET
import datetime

def charger_lexique(nom_fichier): #on charge le lexique depuis fichier tabulé
    lexique = {}
    with open(nom_fichier, encoding='utf-8') as fichier:
        for ligne in fichier:
            mot, categorie = ligne.strip().split('\t')
            lexique[mot.lower()] = categorie #on stocke les mots en minuscules
    return lexique

def charger_regles(nom_fichier): #on charge les règles depuis fichier txt
    regles = []
    with open(nom_fichier, encoding='utf-8') as fichier:
        for ligne in fichier:
            ligne = ligne.split('//')[0].strip()#supprime commentaires s'il y en a
            if ligne:
                partie_gauche, partie_droite = ligne.split('=>')
                conditions = [cond.strip() for cond in partie_gauche.strip().split('+')]
                action = partie_droite.strip().replace('[', '') #on retire le crochet gauche
                regles.append((conditions, action))
    return regles

def pretokeniser_texte(texte_brut):
    texte = re.sub(r"([,.;!?])", r" \1 ", texte_brut) #séparation signes de ponctuation
    texte = re.sub(r"\b([ldnmstjcq])’", r"\1’ ", texte, flags=re.IGNORECASE) #élision à séparer
    texte = re.sub(r'\s+', ' ', texte) #si plusieurs espaces
    return texte.strip()

def charger_texte(nom_fichier):
    with open(nom_fichier, encoding='utf-8') as fichier:
        contenu = fichier.read()
    contenu = contenu.replace('\n', ' BR ')#insertion de BR pour les retours à la ligne
    tokens = contenu.strip().split(' ')
    return [mot for mot in tokens if mot]#élimination des chaînes vides

def regle_satisfait(tokens, lexique, position, conditions):
    extraits = [] #liste des mots qui correspondent aux conditions (si la règle s'applique)
    i = position

    for cond in conditions:
        if i >= len(tokens): #si on dépasse la fin du texte, la règle ne s'applique pas
            return False, []

        mot = tokens[i]
        categorie = lexique.get(mot.lower(), 'UNKNOWN') #on récupère la catégorie du mot

        if cond == '[0-9]+': #nombre
            if not re.fullmatch(r'[0-9]+', mot):
                return False, []
            extraits.append(mot)

        elif cond == '_': #mot inconnu du lexique
            if mot.lower() in lexique or categorie in {'Pctf', 'Pctnf', 'GO', 'GF'}: #on rejette si le mot est connu du lexique ou s'il s'agit d'un signe de ponctuation
                return False, []
            extraits.append(mot)

        elif cond.endswith(('er', 'ir', 'ant', 'ique')): #suffixes réguliers
            if not mot.endswith(cond[1:]):
                return False, []
            extraits.append(mot)

        elif cond == '*-PPS': #inversion sujet-verbe
            if not re.search(r'-[a-zA-Z]+$', mot):
                return False, []
            extraits.append(mot)

        elif cond in lexique.values(): #condition sur une catégorie grammaticale
            if categorie != cond:
                return False, []
            extraits.append(mot)

        else: #si aucune des conditions n'est satisfaite
            return False, []

        i += 1 #on avance

    return True, extraits

def appliquer_regles(tokens, lexique, regles): #on applique les règles à une séquence de tokens
    resultat = []  #liste finale des chunks ou des mots isolés
    i = 0 #position actuelle dans liste des tokens

    while i < len(tokens):
        trouve = False #indique si une règle a été trouvé à une position i

        for conditions, etiquette in regles:
            ok, extraits = regle_satisfait(tokens, lexique, i, conditions)

            if ok: #si la règle est satisfaite, on met le chunk
                contenu = ' '.join(extraits)
                regle_str = ' + '.join(conditions)
                resultat.append((etiquette, contenu, regle_str))
                i += len(extraits) #on avance dans les tokens autant que le chunk couvre
                trouve = True
                break #on ne teste pas d'autres règles à cette position

        if not trouve: #si aucune règle ne s'applique, on conserve le mot tel quel
            resultat.append(tokens[i])
            i += 1

    return resultat

def generer_xml_chunked(chunks, fichier_xml): #génère fichier XML à partir de la liste des chunks
    date_du_jour = datetime.date.today().strftime("%d/%m/%Y")
    racine = ET.Element("texte", {
        "src": "https://www.legorafi.fr/2024/11/25/pour-freiner-la-fonte-des-glaces-le-gouvernement-fait-installer-3000-climatiseurs-sur-la-banquise/",
        "date": date_du_jour
    })

    paragraphe = ET.SubElement(racine, "paragraphe")
    phrase = ET.SubElement(paragraphe, "phrase")

    for chunk in chunks: #parcours des chunks
        if isinstance(chunk, tuple): #quand chunk reconnu
            cat, contenu, regle_utilisee = chunk
            elt = ET.SubElement(phrase, "chunk", cat=cat, regle=regle_utilisee)
            elt.text = contenu
        else:
            if chunk == "BR": #quand retour à la ligne on ouvre un nouveau paragraphe
                elt = ET.SubElement(phrase, "chunk", cat="BR", regle="manuelle")
                elt.text = "BR"
                paragraphe = ET.SubElement(racine, "paragraphe")
                phrase = ET.SubElement(paragraphe, "phrase")
            elif chunk == ".": #quand point final on ouvre une nouvelle phrase
                phrase = ET.SubElement(paragraphe, "phrase")
            else: #quand non chunké
                elt = ET.SubElement(phrase, "chunk", cat="UNK", regle="aucune")
                elt.text = chunk

    arbre = ET.ElementTree(racine)
    arbre.write(fichier_xml, encoding="utf-8", xml_declaration=True)

import xml.etree.ElementTree as ET

def generer_html_depuis_xml(fichier_xml, fichier_html): #convertit fichier XMl chunké en page HTML
    import xml.etree.ElementTree as ET

    tree = ET.parse(fichier_xml)
    racine = tree.getroot()

    with open(fichier_html, 'w', encoding='utf-8') as f:
        #écriture de l'en-tête HTML
        f.write('<!DOCTYPE html>\n<html lang="fr">\n<head>\n')
        f.write('<meta charset="UTF-8">\n<title>Chunker</title>\n')
        f.write('<link rel="stylesheet" href="chunking.css">\n</head>\n<body>\n')
        f.write('<h1>Chunker</h1>\n<div>\n')

        for paragraphe in racine.findall('paragraphe'): #parcours des paragraphes et phrases
            for phrase in paragraphe.findall('phrase'):
                chunks = phrase.findall('chunk')
                if not chunks:
                    continue #ignore les phrases vides

                buffer_unk = [] #tampon qui accumule les mots non reconnus UNK
                for chunk in chunks:
                    cat = chunk.attrib.get('cat', 'UNK')
                    texte = (chunk.text or '').strip()

                    if cat == "BR": #affichage retour à la ligne
                        f.write(f'<span class="chunk" cat="BR">[BR]</span><br>\n')
                        continue

                    if cat == "UNK": #mots non reconnus dans le tampon
                        buffer_unk.append(texte)
                    else: #si accumulation UNK on les écrits en premier
                        if buffer_unk:
                            texte_fusionne = ' '.join(buffer_unk)
                            f.write(f'<span class="chunk" cat="UNK">[UNK {texte_fusionne}]</span> ')
                            buffer_unk = []
                        f.write(f'<span class="chunk" cat="{cat}">[{cat} {texte}]</span> ') #affichage chunk reconnu avec catégorie

                if buffer_unk: #si UNK restant on les écrit aussi
                    texte_fusionne = ' '.join(buffer_unk)
                    f.write(f'<span class="chunk" cat="UNK">[UNK {texte_fusionne}]</span> ')

                f.write('<br>\n')

        f.write('</div>\n</body>\n</html>')

def main(): #traitement du texte en chunk et génération XML et HTML
    lexique = charger_lexique('lexique.txt')
    regles = charger_regles('regles.txt')
    with open('texte.txt', encoding='utf-8') as f:
        contenu = f.read()
    contenu = contenu.replace('\n', ' BR ') #remplacement sauts de ligne par BR
    texte_pretokenise = pretokeniser_texte(contenu)
    tokens = texte_pretokenise.split(' ') #découpage texte en tokens
    chunks = appliquer_regles(tokens, lexique, regles)

    texte_formaté = [] #affichage console
    for item in chunks:
        if isinstance(item, tuple):
            cat, contenu, _ = item  
            texte_formaté.append(f"[{cat} {contenu}]")
        elif item == "BR":
            texte_formaté.append("\n[BR]") 
        else:
            texte_formaté.append(item)

    print("\nRésultat :")
    print(' '.join(texte_formaté))

    generer_xml_chunked(chunks, 'sortie_chunker.xml')
    print("\nFichier XML généré : sortie_chunker.xml")
    generer_html_depuis_xml('sortie_chunker.xml', 'chunking_live.html')
    print("Fichier HTML généré à partir du XML : chunking_live.html")

if __name__ == '__main__': #exécute la fonction main() seulement si ce fichier est lancé directement
    main()