# LIBRARIES ON
import os
import string
import json
import requests
import re
import PyPDF2 
from PyPDF2 import PdfReader
import nltk
import spacy
import mimetypes
import urllib.request
import pandas as pd
import openpyxl
import textstat
import ast
import xml.etree.ElementTree as ET
from nltk.corpus import cmudict
from io import StringIO
import re
import fitz
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# nltk - spacy
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets')
nltk.download('large_grammars')
nltk.download('cmudict')
nlp = spacy.load("en_core_web_sm")
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import cmudict
nltk.download('wordnet', quiet=True)

# Complex word index
Palabras_Complejas = ['Aberration', 'Abstemious', 'Abyssal', 'Acquiesce', 'Adjudicate', 'Adroit', 'Aesthetic', 'Affable', 'Affluent', 'Alacrity', 'Altruistic', 'Amalgamate', 'Ambivalent', 'Ameliorate', 'Anachronistic', 'Analogous', 'Anathema', 'Anomaly', 'Antecedent', 'Antediluvian', 'Antiquated', 'Antithesis', 'Apathetic', 'Apocryphal', 'Approbation', 'Arbitrary', 'Arcane', 'Ardent', 'Articulate', 'Ascetic', 'Asperity', 'Assiduous', 'Assuage', 'Astringent', 'Auspicious', 'Avarice', 'Axiomatic', 'Banal', 'Belligerent', 'Benevolent', 'Benign', 'Bequeath', 'Bucolic', 'Cadence', 'Cajole', 'Capricious', 'Catharsis', 'Cerebral', 'Chicanery', 'Circumlocution', 'Circumscribe', 'Clandestine', 'Cognizant', 'Collusion', 'Complacency', 'Concomitant', 'Confluence', 'Congenial', 'Conscientious', 'Consensus', 'Consummate', 'Contemptuous', 'Contrite', 'Conundrum', 'Convivial', 'Corollary', 'Coterie', 'Credulous', 'Cryptic', 'Culpable', 'Cursory', 'Debacle', 'Deleterious', 'Demagogue', 'Denigrate', 'Derivative', 'Desultory', 'Diatribe', 'Diffident', 'Dilatory', 'Dilettante', 'Discernment', 'Discomfit', 'Disparate', 'Disseminate', 'Dissolution', 'Divisive', 'Docile', 'Duplicity', 'Ebullient', 'Effervescent', 'Efficacious', 'Effrontery', 'Egregious', 'Elegiac', 'Elucidate', 'Emanate', 'Emollient', 'Empirical']
dir_path = "Your Directory"

# SECTIONS - TEXT
SECCIONES = ['introduction', 'state of the art', 'development', 'materials and methods', 'methodology', 'results', 'conclusion', 'discussion', 'Declaration of Competing Interest', 'Declaration of interests', 'Author contributions', 'Author Contribution Statement', 'author statement', 'Authors’ contribution', 'Author’s statements', 'Acknowledgements',]
SECCIONES_TABLAS = ['Table 01', 'Table 1', 'Table I', 'Table A','Table A1', 'Table B','Table B1', 'Table 01.', 'Table 1.', 'Table I.', 'Table A.','Table A1.', 'Table B.','Table B1.']
SECCIONES_FIGURAS = ['Fig.1', 'Fig. 1', 'Figure 1', 'Fig. A1', 'Fig. B2', 'Fig.1', 'Fig. 1.', 'Figure 1.', 'Fig. A1.', 'Fig. B2.', 'Fig1', 'Fig 1', 'Figure 1', 'Fig A1', 'Fig B2'] 

# REGEX - DEPTH OF SECTIONS
# Elsevier
Elsevier_LVL_2 = r'\b\d\.\d\. \b'
Elsevier_LVL_3 = r'\b\d\.\d\.\d\. \b'
Elsevier_LVL_4 = r'\b\d\.\d\.\d\.\d\. \b'
# SPRINGER
Springer_LVL_2 = r'\b\d\.\d\ +\b'
Springer_LVL_3 = r'\b\d\.\d\.\d\ +\b'
Springer_LVL_4 = r'\b\d\.\d\.\d\.\d\ +\b'
# IEEE
Ieee_LVL_2 = r'\n([A-B]\.)\s'
Ieee_LVL_3 = r'\b \d\) \b'

# Loop through PDF and count // Function call.(D)
for filename in os.listdir(dir_path):    
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(dir_path, filename)

        valueVisi = 0.65
        valueMeta = 0.5198
        valueEdit = 0.74
        

        ValueDoi=0; ValueAuthor=0; ValueTitle=0; ValueYear=0; ValueAbstract=0; ValueUrl=0; ValueLink=0;  ValueUri=0; ValueVersion=0; ValueKeyword=0; ValueOpenAccess=0; ValueOpenAccessTotal=0; ValueFullText=0; ValueSoftware=0; Valuerestringed=0; ValueSubscribe=0; Valuedownload=0; ValueparcialAccess=0; ValueOnlyMetadata=0; ValueDataset=0; ValueEmbargado=0; ValueIssn=0; ValueImagen=0
        DoiSW=0; autorSW=0; tituloSW=0; yearSW=0; keywordSW=0; IssnSW=0; abstractSW=0; linkSW=0; urlSW=0; uriSW=0; versionSW=0; accesoabiertoSW=0; openAccessTotalSW=0; fulltextSW=0; softwareSW=0; parcialAccessSW=0; downloadSW=0; SubscribeSW=0; restringedSW=0; onlymetadataSW=0; datasetSW=0; embargadoSW=0; imagenSW=0
        
        # Others
        afiliacionSW = 0
        grad_cumpli = 0
        referenciasSW = 0
        Publicador_Name = ''

        abstract = ''

        # MULTIMEDIA - ACCESSIBILITY - VERSION 2.0
        pdf_file = fitz.open(pdf_path)
        for page_index in range(len(pdf_file)):
            page = pdf_file[page_index]
            image_list = page.get_images()
            if image_list:
                imagenSW = 1
                ValueImagen = valueMeta
                break
        print("MULTIMEDIA: ", imagenSW,"\n") 



        #FINAL ABSTRACT FILTER - EXTRACT FROM THE DOCUMENT
        if abstractSW == 0:
            pdf_reader = PyPDF2.PdfReader(pdf_path)

            num_pages = len(pdf_reader.pages)
            all_text = ''
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                all_text += page_text

            # Look for the pattern of the abstract
            abstract_pattern = re.compile(r'abstract', re.IGNORECASE)
            match = abstract_pattern.search(all_text)

            # Extract the text from the abstract
            if match:
                abstract_text = all_text[match.start():]
                next_heading = re.compile(r'^\s*(1\.|i\.|a\.)\s', re.MULTILINE)
                match = next_heading.search(abstract_text)
                if match:
                    abstract_text = abstract_text[:match.start()]

                # Look for the pattern of the introduction
                intro_pattern = re.compile(r'^(1|I)\.\s*INTRODUCTION', re.MULTILINE)
                match = intro_pattern.search(all_text)
                if match:
                    intro_text = all_text[match.start():]
                    abstract_text += intro_text

                # Look for the pattern of the keywords
                keywords_pattern = re.compile(r'^(1|I{1,3})?\.\s*(KEYWORDS|Keywords)', re.MULTILINE)
                match = keywords_pattern.search(all_text)
                if match:
                    keywords_text = all_text[match.start():]
                    abstract_text += keywords_text
        
            abstract = abstract_text
            abstractSW = 1
            ValueAbstract = valueMeta


        #_______________▲▼_______________# LEXICAL DENSITY #______________▲▼__________________#
        DL_palabras = abstract.split()
        DL_total_palabras = len(DL_palabras) # N
        DL_vocabulario = set(DL_palabras)  
        DL_total_vocabulario = len(DL_vocabulario)  # V
        
        Densidad_Lexica = DL_total_vocabulario / DL_total_palabras  * 3.49

        # Normalizar SIN PESO
        #Norm_Densidad_lexica = (Densidad_Lexica - 0) / (DL_total_palabras - 0)
        # Normalizar CON PESO
        #Norm_Densidad_lexica_Peso = (Densidad_Lexica - 0) / (DL_total_palabras - 0) * 3.49


        #print("*********************** COMPRESNIBILIDAD  *************************")
        #print("******* DENSIDAD LEXICA *********")
        print("Densidad Lexica: ",Densidad_Lexica)
        #print("Densidad Lexica: ",Densidad_Lexica)
        #print("Densidad Lexica-Normalizada: ",Norm_Densidad_lexica)
        #print("Densidad Lexica-Normalizada Con Peso: ",Norm_Densidad_lexica_Peso)
        #print("********************************","\n")
        

        #_____________▲▼________________# COMPLEJIDAD DE LA ORACION #______________▲▼__________________#
        

        CO_oraciones = nltk.sent_tokenize(abstract)
        palabras_por_oracion = [len(nltk.word_tokenize(oracion)) for oracion in CO_oraciones]
        indice_longitud_oracional = sum(palabras_por_oracion) / len(palabras_por_oracion)

        nlp = spacy.load('en_core_web_sm')
        
        # function to check if a sentence is complex
        def is_complex(sentence):
            doc = nlp(sentence)
            clauses = [chunk for chunk in doc.noun_chunks if chunk.root.dep_ == 'nsubj']
            for token in doc:
                if token.dep_ == 'mark':
                    clauses.append(token.text)
            if len(clauses) > 1:
                return True
            else:
                return False

        # Split abstract into sentences
        sentences = nltk.sent_tokenize(abstract)

        # Calculate the number of complex phrases per sentence
        complex_sentence_index = []
        complex_sentences_list = []
        for sentence in sentences:
            words = len(nltk.word_tokenize(sentence))
            if words > 0:
                if is_complex(sentence):
                    complex_sentences_list.append(sentence)
                complex_sentences = sum([is_complex(subsentence) for subsentence in nltk.sent_tokenize(sentence)])
                complex_sentence_index.append(complex_sentences / words)

        # Average number of complex phrases per sentence [Index]
        average_complex_sentence_index = sum(complex_sentence_index) / len(complex_sentence_index)


        # Words
        palabras = nltk.word_tokenize(abstract)
        palabras2 = len(palabras)
        # Sentences
        oraciones = nltk.sent_tokenize(abstract)
        oracion2 = len(oraciones)

        # complex words:
        frases_complejas = len(complex_sentences_list)
        
        #Calculation
        Complejidad_Oracion = (0.4 * (palabras2/oracion2) + 100 * (frases_complejas/palabras2))

        
        Nor_Complejidad_Oracion = (Complejidad_Oracion - 6) / (17 - 6)
        Nor_Complejidad_Oracion_Peso =  (Complejidad_Oracion - 6) / (17 - 6) * 3.49

        
        #print("******* COMPLEJIDAD DE LA ORACION *********")
        print("Complejidad Oracion: ",Complejidad_Oracion)
        #print("Complejidad Oracion-Normalizada: ", Nor_Complejidad_Oracion)
        #print("Complejidad Oracion-Normalizada Con Peso: ", Nor_Complejidad_Oracion_Peso)
        #print("********************************","\n")
        

        #________________▲▼___________# COMPLEJIDAD SINTACTICA #_____________▲▼________________#


        # Num words
        palabras = nltk.word_tokenize(abstract)
        nume_palabras = len(palabras)

        # number of sentences - Sentence Length
        oraciones = nltk.sent_tokenize(abstract)
        num_oraciones = len(oraciones)

        # Num Modifiers
        num_modifiers = 0
        for palabra in palabras:
            tag = nltk.pos_tag([palabra])[0][1]
            if tag.startswith('JJ') or tag.startswith('RB'):
                num_modifiers += 1
        
        # Average Modifiers Per Sentence.
        promedio_modificadores_oracion = (num_modifiers / num_oraciones)

        # Formula Syntactic Complexity: ((total number of sentences x average number of modifiers per sentence) / total number of words)
        Complejidad_Sintactica = (num_oraciones * promedio_modificadores_oracion) / nume_palabras
        # Normalize would look like this (value - 0) / (LO - 0)
        Norm_Complejidad_Sintactica = (Complejidad_Sintactica - 0) / (num_oraciones - 0)
        # Normalize With Weight - Sentence Length
        Norm_Complejidad_Sintactica_Peso = (Complejidad_Sintactica - 0) / (num_oraciones - 0) * 3.49

        
        #print("******* COMPLEJIDAD SINTACTICA *********")
        print("Complejidad Sintactica: ",Complejidad_Sintactica)
        #print("Complejidad Sintactica-Normalizar: ",Norm_Complejidad_Sintactica)
        #print("Complejidad Sintactica-Normalizar Con Peso: ",Norm_Complejidad_Sintactica_Peso)
        #print("********************************","\n")
        

        #_______________▲▼_______________# SCORE MARKS #______________▲▼__________________#


        patron = r'[^\w\s]'
        num_puntuacion = len(re.findall(patron, abstract))
        Marcas_Puntuacion = num_puntuacion / len(abstract)

        # Normalize (average–0) / (ns– 0) ns= number of signs
        Norm_Marcas_Puntuacion = (Marcas_Puntuacion - 0) / (num_puntuacion - 0)
        # Normalize With Weight
        Norm_Marcas_Puntuacion_Peso = (Marcas_Puntuacion - 0) / (num_puntuacion - 0) * 3.49
        
        
        #print("******* MARCAS DE PUNTUACION *********")
        print("Marcas puntuacion: ",Marcas_Puntuacion)
        #print("Marcas puntuacion-Normalizar: ",Norm_Marcas_Puntuacion)
        #print("Marcas puntuacion-Normalizar Con Peso: ",Norm_Marcas_Puntuacion_Peso)
        #print("********************************","\n")




        # call Depth Function.
        d = cmudict.dict()

        # -- CALCULATE VALUES (NUM: Words, Sentences, Letters, Syllables)
         # tokenize
        palabras = word_tokenize(abstract)
        oraciones = sent_tokenize(abstract)
        # Number of words and sentences
        num_palabras = len(palabras)
        num_oraciones = len(oraciones)
        # Number of letters and syllables
        num_letras = sum(len(palabra) for palabra in palabras)
        num_silabas = sum(len(d.get(palabra.lower(), [0])) for palabra in palabras)

        num_palabras_complejas = len([palabra for palabra in palabras if palabra in Palabras_Complejas])


        #_________________▲▼_______________# INDEX SSR #______________▲▼_________________#

        def calculate_ssr(abstract):
            s = abstract.count('.') + abstract.count('!') + abstract.count('?')
            w = len(abstract.split())
            
            # List of rare (complex) words for English
            Palabras_Complejas = ['Aberration', 'Abstemious', 'Abyssal', 'Acquiesce', 'Adjudicate', 'Adroit', 'Aesthetic', 'Affable', 'Affluent', 'Alacrity', 'Altruistic', 'Amalgamate', 'Ambivalent', 'Ameliorate', 'Anachronistic', 'Analogous', 'Anathema', 'Anomaly', 'Antecedent', 'Antediluvian', 'Antiquated', 'Antithesis', 'Apathetic', 'Apocryphal', 'Approbation', 'Arbitrary', 'Arcane', 'Ardent', 'Articulate', 'Ascetic', 'Asperity', 'Assiduous', 'Assuage', 'Astringent', 'Auspicious', 'Avarice', 'Axiomatic', 'Banal', 'Belligerent', 'Benevolent', 'Benign', 'Bequeath', 'Bucolic', 'Cadence', 'Cajole', 'Capricious', 'Catharsis', 'Cerebral', 'Chicanery', 'Circumlocution', 'Circumscribe', 'Clandestine', 'Cognizant', 'Collusion', 'Complacency', 'Concomitant', 'Confluence', 'Congenial', 'Conscientious', 'Consensus', 'Consummate', 'Contemptuous', 'Contrite', 'Conundrum', 'Convivial', 'Corollary', 'Coterie', 'Credulous', 'Cryptic', 'Culpable', 'Cursory', 'Debacle', 'Deleterious', 'Demagogue', 'Denigrate', 'Derivative', 'Desultory', 'Diatribe', 'Diffident', 'Dilatory', 'Dilettante', 'Discernment', 'Discomfit', 'Disparate', 'Disseminate', 'Dissolution', 'Divisive', 'Docile', 'Duplicity', 'Ebullient', 'Effervescent', 'Efficacious', 'Effrontery', 'Egregious', 'Elegiac', 'Elucidate', 'Emanate', 'Emollient', 'Empirical']
            
            # Number of rare words in the text
            rw = len([word for word in abstract.split() if word.lower() in Palabras_Complejas])
            
            # Calculation of the SSR index
            ssr = (1.609 * (w/s)) + (331.8 * (rw/w)) + 22.0
            
            return ssr

        text = abstract
        ssr = calculate_ssr(text)

        # RANKS TO BE: 
        # # Very simplified
        if ssr <= 39:
            rangoSSR = "Muy Simplificado"
        # Very easy
        if ssr >= 40 and ssr <= 60:
            rangoSSR = "Muy Facil"
        # Easy
        if ssr >= 61 and ssr <= 80:
            rangoSSR = "Facil" 
        # Moderate difficulty
        if ssr >= 81 and ssr <= 100:
            rangoSSR = "Dificultad Moderada"
        # Difficult
        if ssr >= 101 and ssr <= 120:
            rangoSSR = "Dificil"
        # Very difficult
        if ssr >= 121:
            rangoSSR = "Muy Dificil"

        # normalize
        Norm_ssr = (ssr - 0) / (121 - 0)
        # Normalize With Weight
        Norm_ssr_Peso = (ssr - 0) / (121 - 0) * 1.27

        
        #print("******* INDICE SSR *********")
        print("SRR: ", ssr,"\t", "Rango: ",rangoSSR)
        #print("SSR-Normalizado: ",Norm_ssr)
        #print("SSR-Normalizado Con Peso: ",Norm_ssr_Peso)
        #print("********************************","\n")
        

        #_________________________________# FACILIDAD DE LECTURA #___________________________________#

        palabras = word_tokenize(abstract)
        oraciones = sent_tokenize(abstract)
        num_palabras = len(palabras)
        num_oraciones = len(oraciones)

        d = cmudict.dict()
        num_silabas = sum(len(d.get(palabra.lower(), [0])) for palabra in palabras)

        Facilidad_Lectura = 206.835 - 1.015 * (num_palabras/num_oraciones) - 84.6 * (num_silabas/num_palabras)
        # Normalizar  (valor – 0) / (100– 0) 
        Norm_Facilidad_Lectura = (Facilidad_Lectura - 0) / (100 - 0) 
        # Normalizar Con Peso
        Norm_Facilidad_Lectura_Peso = (Facilidad_Lectura - 0) / (100 - 0) * 1.27

        
        #print("******* FACILIDAD DE LECTURA *********")
        print("Facilidad Lectura:", Facilidad_Lectura)
        #print("Facilidad Lectura-Norm:", Norm_Facilidad_Lectura)
        #print("Facilidad Lectura-Norm Con Peso:", Norm_Facilidad_Lectura_Peso)
        #print("********************************","\n")
         

        #_________________________________# TEXT ANALYSIS - TREE #___________________________________#

        doc = nlp(abstract)
        Densidad_Arbol = len(doc) / (len(doc) + 1)
        #print("DENSIDAD ARBOL NO PESO: ", Densidad_Arbol)
        Densidad_Arbol = Densidad_Arbol * 1.27
        #print("DENSIDAD ARBOL PESO: ", Densidad_Arbol, "\n")


        # Normalizar (valor - 0) / (1 - 0)
        # Norm_Arbol = (depth - 1) / (Mayor_Profundidad - 1)
        # Normalizar Con Peso
        #Norm_Arbol_Peso = (depth - 1) / (Mayor_Profundidad - 1) * 7.08


        
        #print("******* PROFUNDIDAD ARBOL *********")
        print("Profundidad Arbol :", Densidad_Arbol)
        #print("Profundidad Arbol-Norm",Norm_Arbol)
        #print("Profundidad Arbol-Norm Con Peso",Norm_Arbol_Peso)
        #print("********************************","\n")
        

        #_________________________________# DEGREE OF COMPLIANCE #___________________________________#

        grad_cumpli_doc = 0

        if tituloSW == 1:
            grad_cumpli = grad_cumpli + 1
        if autorSW == 1:
            grad_cumpli = grad_cumpli + 1
        if afiliacionSW == 1:
            grad_cumpli = grad_cumpli + 1
        if abstractSW == 1:
            grad_cumpli = grad_cumpli + 1
        if keywordSW == 1:
            grad_cumpli = grad_cumpli + 1
        if referenciasSW == 1:
            grad_cumpli = grad_cumpli + 1

        with open(os.path.join(dir_path, filename), 'rb') as archivo:
            lector_pdf = PyPDF2.PdfReader(archivo)

            
            texto = ''
            for pagina in lector_pdf.pages:
                texto += pagina.extract_text()

            
            titulos = {}

            # Sections
            for seccion in SECCIONES:
                inicio = texto.find(seccion)
                if inicio != -1:
                    fin_linea = texto.find('\n', inicio)
                    titulo = texto[inicio:fin_linea].strip()
                    grad_cumpli_doc += 1
                    titulos[seccion] = titulo

            # boards
            for seccion in SECCIONES_TABLAS:
                inicio = texto.find(seccion)
                if inicio != -1:
                    fin_linea = texto.find('\n', inicio)
                    titulo = texto[inicio:fin_linea].strip()
                    titulos[seccion] = titulo
                    grad_cumpli_doc += 1
                    break
            
            # Figures
            for seccion in SECCIONES_FIGURAS:
                inicio = texto.find(seccion)
                if inicio != -1:
                    fin_linea = texto.find('\n', inicio)
                    titulo = texto[inicio:fin_linea].strip()
                    titulos[seccion] = titulo
                    grad_cumpli_doc += 1
                    break

            
            Grado_Cumplimiento = len(titulos)
            Grado_Cumplimiento = Grado_Cumplimiento + grad_cumpli
            # Normalizar
            Norm_Grado_Cumplimiento = (Grado_Cumplimiento - 1) / (15 - 1)
            # Normalizar Con Peso
            Norm_Grado_Cumplimiento_Peso = (Grado_Cumplimiento - 1) / (15 - 1) * 7.08

            
            #print("******* GRADO DE CUMPLIMIENTO *********")
            print("Grado De Cumplimiento: ",Grado_Cumplimiento)
            #print("Grado Cumplimiento-Norm: ", Norm_Grado_Cumplimiento)
            #print("Grado Cumplimiento-Norm Con Peso: ", Norm_Grado_Cumplimiento_Peso)
            #print("********************************","\n")       

        #______________________________# PROFUNDIDAD DE SECCIONES #_______________________________#


        nivel_2_titulos = []
        nivel_3_titulos = []
        nivel_4_titulos = []

        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                content = page.extract_text()

                if Publicador_Name == "ELSEVIER":
                    nivel_2_titulos.extend(re.findall(Elsevier_LVL_2, content))
                    nivel_3_titulos.extend(re.findall(Elsevier_LVL_3, content))
                    nivel_4_titulos.extend(re.findall(Elsevier_LVL_4, content))

                if Publicador_Name == "SPRINGER":
                    nivel_2_titulos.extend(re.findall(Springer_LVL_2, content))
                    nivel_3_titulos.extend(re.findall(Springer_LVL_3, content))
                    nivel_4_titulos.extend(re.findall(Springer_LVL_4, content))
                
                if Publicador_Name == "IEEE":
                    nivel_2_titulos.extend(re.findall(Ieee_LVL_2, content))
                    nivel_3_titulos.extend(re.findall(Ieee_LVL_3, content))

        #print(f"Archivo: {pdf_path}")
        #print(f"Nivel 2: ",nivel_2_titulos)
        #print(f"Nivel 3: ",nivel_3_titulos)
        #print(f"Nivel 4: ",nivel_4_titulos)
        

        
        Profundidad_Secciones = 1

        if nivel_4_titulos:
            Profundidad_Secciones = 4
        elif nivel_3_titulos:
            Profundidad_Secciones = 3
        elif nivel_2_titulos:
            Profundidad_Secciones = 2

        # Normalizar (valor – 1) / (4 – 1) 
        Norm_Profundidad_Secciones = (Profundidad_Secciones - 1) / (4 - 1)
        # Normalizar Con Peso
        Norm_Profundidad_Secciones_Peso = (Profundidad_Secciones - 1) / (4 - 1) * 7.08

        # En caso de que de 0
        if Norm_Profundidad_Secciones_Peso == 0:
            Norm_Profundidad_Secciones_Peso = 1

         
        #print("******* PROFUNDIDAD DE SECCIONES *********")
        print("Profundidad Secciones: ",Profundidad_Secciones)
        #print("Profundidad Secciones-Norm: ",Norm_Profundidad_Secciones)
        #print("Profundidad Secciones-Norm Con Peso",Norm_Profundidad_Secciones_Peso)

        
        