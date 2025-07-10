#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Instalar bibliotecas necessárias

from IPython.display import display, Markdown
from google.colab import files
import fitz  # PyMuPDF

display(Markdown("## 📎 Faça upload do relatório PDF"))

# Upload do arquivo
uploaded = files.upload()
pdf_path = list(uploaded.keys())[0]
doc = fitz.open(pdf_path)

# Executar os minicódigos (cada um está definido nas células seguintes)
minicodigo1(doc)
minicodigo2(doc)
minicodigo3(doc)
minicodigo4(doc)


# In[ ]:


# 1. Instalar bibliotecas necessárias
get_ipython().system('pip install openai PyMuPDF Pillow --quiet')

# 2. Imports
import fitz  # PyMuPDF
import pandas as pd
from IPython.display import display, Markdown
from google.colab import files
import re
import unicodedata

# 3. Definir função principal
def minicodigo1(doc):
    # Análise 8 – Faltas Injustificadas
    relatorios_com_faltas = []
    estado_relatorio = 0
    numero_relatorio = 0

    for i, page in enumerate(doc):
        texto = page.get_text()
        texto_normalizado = texto.replace("\n", " ").strip().lower()

        nova_pagina_1 = (
            "declaro, para os devidos fins, junto à assembleia legislativa do estado de goiás" in texto_normalizado and
            "estou ciente que a prestação de declaração falsa" in texto_normalizado
        )

        if nova_pagina_1:
            estado_relatorio = 1
            numero_relatorio += 1
        elif estado_relatorio == 1:
            estado_relatorio = 2
        elif estado_relatorio >= 2:
            estado_relatorio += 1

        if estado_relatorio == 2:
            if re.search(r"\(\s*x\s*\)\s*declaro que neste período o servidor não", texto_normalizado):
                relatorios_com_faltas.append({
                    "Relatório": numero_relatorio,
                    "Página": i + 1,
                    "Resumo": "Faltas injustificadas foram assinaladas"
                })

    if relatorios_com_faltas:
        faltas_df = pd.DataFrame(relatorios_com_faltas)
        display(Markdown("### ❌ Faltas Injustificadas"))
        display(faltas_df)
        faltas_df.to_csv("relatorios_com_faltas.csv", index=False)
    else:
        print("✅ Nenhum caso de falta injustificada foi detectado.")

    # Análise 9 – Nenhuma Atividade Informada
    relatorios_sem_atividade = []
    estado_relatorio = 0
    numero_relatorio = 0

    for i, page in enumerate(doc):
        texto = page.get_text()
        texto_normalizado = texto.replace("\n", " ").strip().lower()

        nova_pagina_1 = (
            "declaro, para os devidos fins, junto à assembleia legislativa do estado de goiás" in texto_normalizado and
            "estou ciente que a prestação de declaração falsa" in texto_normalizado
        )

        if nova_pagina_1:
            estado_relatorio = 1
            numero_relatorio += 1
        elif estado_relatorio >= 1:
            estado_relatorio += 1

        if estado_relatorio == 1:
            if "nenhuma atividade informada" in texto_normalizado:
                relatorios_sem_atividade.append({
                    "Relatório": numero_relatorio,
                    "Página": i + 1,
                    "Resumo": "Nenhuma atividade informada"
                })

    if relatorios_sem_atividade:
        atividades_df = pd.DataFrame(relatorios_sem_atividade)
        display(Markdown("### ⚠️ Relatórios Sem Atividades Informadas"))
        display(atividades_df)
        atividades_df.to_csv("relatorios_sem_atividade.csv", index=False)
    else:
        print("✅ Todos os relatórios possuem atividades informadas.")

    # Análise 10 – Férias ou Afastamento
    def normalizar(texto):
        return unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII").strip().lower()

    ferias_afastamentos = []
    estado_relatorio = 0
    numero_relatorio = 0

    for i, page in enumerate(doc):
        texto_original = page.get_text()
        texto_normalizado = normalizar(texto_original.replace("\n", " "))

        nova_pagina_1 = (
            "declaro, para os devidos fins, junto a assembleia legislativa do estado de goias" in texto_normalizado and
            "estou ciente que a prestacao de declaracao falsa" in texto_normalizado
        )

        if nova_pagina_1:
            estado_relatorio = 1
            numero_relatorio += 1
        elif estado_relatorio >= 1:
            estado_relatorio += 1

        if estado_relatorio == 1:
            for tipo in ["férias no período:", "afastamento no período:"]:
                tipo_norm = normalizar(tipo)
                if tipo_norm in texto_normalizado:
                    idx = texto_normalizado.index(tipo_norm) + len(tipo_norm)
                    resto = texto_normalizado[idx:].strip()
                    valor = resto.split(":", 1)[0].split("afastamento no periodo")[0].strip()
                    if not valor.startswith("nao informado"):
                        ferias_afastamentos.append({
                            "Relatório": numero_relatorio,
                            "Página": i + 1,
                            "Tipo": tipo.split()[0].capitalize(),
                            "Informação Encontrada": texto_original[idx:idx+100].split("\n")[0].strip()
                        })

    if ferias_afastamentos:
        ferias_df = pd.DataFrame(ferias_afastamentos)
        display(Markdown("### 📌 Férias ou Afastamento Informados"))
        display(ferias_df)
        ferias_df.to_csv("ferias_afastamentos_informados.csv", index=False)
    else:
        print("✅ Nenhuma informação de férias ou afastamento foi detectada.")

    # Análise 11 – Observações do Servidor
    observacoes_servidor = []
    estado_relatorio = 0
    numero_relatorio = 0

    for i, page in enumerate(doc):
        texto_original = page.get_text()
        texto_normalizado = texto_original.replace("\n", " ").strip().lower()

        nova_pagina_1 = (
            "declaro, para os devidos fins, junto à assembleia legislativa do estado de goiás" in texto_normalizado and
            "estou ciente que a prestação de declaração falsa" in texto_normalizado
        )

        if nova_pagina_1:
            estado_relatorio = 1
            numero_relatorio += 1
        elif estado_relatorio >= 1:
            estado_relatorio += 1

        if estado_relatorio == 1:
            match = re.search(r"observa(?:ç(?:ã|a)o)? do servidor:\s*(.+)", texto_original, re.IGNORECASE)
            if match:
                observacoes_servidor.append({
                    "Relatório": numero_relatorio,
                    "Página": i + 1,
                    "Observação": match.group(1).strip()
                })

    if observacoes_servidor:
        obs_df = pd.DataFrame(observacoes_servidor)
        display(Markdown("### 📝 Observações do Servidor"))
        display(obs_df)
        obs_df.to_csv("observacoes_do_servidor.csv", index=False)
    else:
        print("✅ Nenhuma observação do servidor foi encontrada.")


# In[ ]:


def minicodigo2(doc):
    resultados = []
    estado_relatorio = 0
    numero_relatorio = 0

    for i, page in enumerate(doc):
        texto = page.get_text().replace("\n", " ").strip().lower()

        nova_pagina_1 = (
            "declaro, para os devidos fins, junto à assembleia legislativa do estado de goiás" in texto and
            "estou ciente que a prestação de declaração falsa" in texto
        )

        if nova_pagina_1:
            estado_relatorio = 1
            numero_relatorio += 1
        elif estado_relatorio >= 1:
            estado_relatorio += 1

        if estado_relatorio == 1:
            imagens = page.get_images(full=True)
            if len(imagens) >= 3:
                try:
                    img_bytes_2 = doc.extract_image(imagens[1][0])["image"]
                    img_bytes_3 = doc.extract_image(imagens[2][0])["image"]

                    response = rekognition.compare_faces(
                        SourceImage={"Bytes": img_bytes_2},
                        TargetImage={"Bytes": img_bytes_3},
                        SimilarityThreshold=0
                    )

                    similarity = response['FaceMatches'][0]['Similarity'] if response['FaceMatches'] else 0

                    if similarity < 66.6:
                        resultados.append({
                            "Relatório": numero_relatorio,
                            "Página": i + 1,
                            "Resultado": f"Similaridade: {similarity:.2f}%"
                        })

                except Exception as e:
                    resultados.append({
                        "Relatório": numero_relatorio,
                        "Página": i + 1,
                        "Resultado": f"Erro ao comparar imagens: {str(e)}"
                    })
            else:
                resultados.append({
                    "Relatório": numero_relatorio,
                    "Página": i + 1,
                    "Resultado": "Primeira página do relatório fora do padrão"
                })

    if resultados:
        resultado_df = pd.DataFrame(resultados)
        display(Markdown("### 📸 Similaridade Facial AWS (2ª e 3ª imagem da 1ª página de cada relatório)"))
        display(resultado_df)
        resultado_df.to_csv("relatorio_similaridade_aws.csv", index=False)
    else:
        print("✅ Nenhuma inconsistência de similaridade foi identificada nas primeiras páginas dos relatórios.")


# In[ ]:


# 1. Instalar e importar bibliotecas necessárias
get_ipython().system('pip install boto3 PyMuPDF Pillow --quiet')

import fitz  # PyMuPDF
import boto3
import io
from PIL import Image
import pandas as pd
from IPython.display import display, Markdown
from google.colab import files

# 2. Configurar cliente AWS Rekognition
rekognition = boto3.client(
    'rekognition',
    region_name='us-east-1',
    aws_access_key_id='AKIAQB7DBGBOST43HF4S',
    aws_secret_access_key='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'
)

# 3. Definir função principal
def minicodigo3(doc):
    conf_por_item = {
        "Headphones": 85.0,
        "Alcohol": 85.0,
        "Weapon": 85.0,
        "Nudity": 90.0,
        "Sunglasses": 95.0,
        "Drinking": 80.0,
        "Child": 85.0,
        "Baby": 85.0,
        "Male Torso": 83.0,
        "Drink": 80.0,
        "Liquor": 85.0,
        "Beverage": 82.0,
        "Bottle": 80.0,
        "Smoking": 88.0,
        "Tobacco": 85.0,
        "Swimwear": 80.0
    }

    estado_relatorio = 0
    numero_relatorio = 0
    resultados = []

    for i, page in enumerate(doc):
        texto = page.get_text().replace("\n", " ").strip().lower()

        nova_pagina_1 = (
            "declaro, para os devidos fins, junto à assembleia legislativa do estado de goiás" in texto and
            "estou ciente que a prestação de declaração falsa" in texto
        )

        if nova_pagina_1:
            estado_relatorio = 1
            numero_relatorio += 1
        elif estado_relatorio >= 1:
            estado_relatorio += 1

        if estado_relatorio == 1:
            imagens = page.get_images(full=True)
            if len(imagens) >= 3:
                try:
                    img_bytes = doc.extract_image(imagens[2][0])["image"]

                    problemas = {}

                    # Labels visuais
                    resposta_labels = rekognition.detect_labels(
                        Image={'Bytes': img_bytes},
                        MaxLabels=50,
                        MinConfidence=50
                    )
                    for label in resposta_labels.get('Labels', []):
                        nome = label['Name']
                        conf = label['Confidence']
                        if nome == "Sunglasses":
                            continue
                        if nome in conf_por_item and conf >= conf_por_item[nome]:
                            problemas[nome] = f"{nome} ({conf:.1f}%)"

                    # Detecção de rostos (óculos escuros)
                    resposta_faces = rekognition.detect_faces(
                        Image={'Bytes': img_bytes},
                        Attributes=['ALL']
                    )
                    for face in resposta_faces['FaceDetails']:
                        sunglasses = face.get('Sunglasses', {})
                        if (
                            "Sunglasses" in conf_por_item and
                            sunglasses.get('Value') and
                            sunglasses.get('Confidence', 0) >= conf_por_item["Sunglasses"]
                        ):
                            problemas["Sunglasses"] = f"Óculos escuros ({sunglasses['Confidence']:.1f}%)"
                            break

                    # Pessoas em destaque
                    pessoas_destaque = []
                    for lbl in resposta_labels.get('Labels', []):
                        if lbl['Name'] == "Person":
                            for inst in lbl.get('Instances', []):
                                box = inst['BoundingBox']
                                area = box['Width'] * box['Height']
                                center_x = box['Left'] + box['Width'] / 2
                                center_y = box['Top'] + box['Height'] / 2
                                if area >= 0.02 and 0.3 <= center_x <= 0.7 and 0.3 <= center_y <= 0.7:
                                    pessoas_destaque.append(inst)

                    if len(pessoas_destaque) > 1:
                        problemas["Multiplas"] = f"Mais de uma pessoa destacada ({len(pessoas_destaque)})"

                    # Crianças ou bebês
                    for nome in ["Child", "Baby"]:
                        for lbl in resposta_labels.get('Labels', []):
                            if lbl['Name'] == nome and lbl['Confidence'] >= conf_por_item[nome]:
                                problemas[nome] = f"{nome} ({lbl['Confidence']:.1f}%)"

                    if problemas:
                        resultados.append({
                            "Relatório": numero_relatorio,
                            "Página": i + 1,
                            "Problemas detectados": ", ".join(problemas.values())
                        })

                except Exception as e:
                    resultados.append({
                        "Relatório": numero_relatorio,
                        "Página": i + 1,
                        "Problemas detectados": f"Erro: {str(e)}"
                    })

    if resultados:
        resultado_df = pd.DataFrame(resultados)
        display(Markdown("### 🚫 Problemas detectados na 3ª imagem da 1ª página de cada relatório"))
        display(resultado_df)
        resultado_df.to_csv("relatorio_problemas_terceira_imagem.csv", index=False)
    else:
        print("✅ Nenhum problema foi detectado nas terceiras imagens analisadas.")


# In[ ]:


# 1. Instalar e importar bibliotecas necessárias
get_ipython().system('pip install boto3 PyMuPDF Pillow --quiet')

import fitz  # PyMuPDF
import boto3
import io
from PIL import Image
import pandas as pd
from IPython.display import display, Markdown
from google.colab import files

# 2. Configurar cliente AWS Rekognition
rekognition = boto3.client(
    'rekognition',
    region_name='us-east-1',
    aws_access_key_id='AKIAQB7DBGBOST43HF4S',
    aws_secret_access_key='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'
)

# 3. Definir função principal
def minicodigo4(doc):
    conf_por_item = {
        "Explicit Nudity": 80.0,
        "Nudity": 80.0,
        "Suggestive": 80.0,
        "Sexual Activity": 80.0,
        "Sexual Situations": 80.0,
        "Revealing Clothes": 85.0,
        "Male Torso": 80.0,
        "Weapon": 85.0,
        "Alcohol": 80.0,
        "Beer": 80.0,
        "Can": 70.0,
        "Drink": 50.0,
        "Liquor": 80.0,
        "Beverage": 80.0,
        "Bottle": 75.0,
        "Smoking": 75.0,
        "Tobacco": 75.0,
        "Swimwear": 75.0,
        "Drinking": 50.0
    }

    estado_relatorio = 0
    numero_relatorio = 0
    resultados = []

    for i, page in enumerate(doc):
        texto = page.get_text().replace("\n", " ").strip().lower()

        nova_pagina_1 = (
            "declaro, para os devidos fins, junto à assembleia legislativa do estado de goiás" in texto and
            "estou ciente que a prestação de declaração falsa" in texto
        )

        if nova_pagina_1:
            estado_relatorio = 1
            numero_relatorio += 1
        elif estado_relatorio >= 1:
            estado_relatorio += 1

        if estado_relatorio >= 3:
            try:
                pix = page.get_pixmap(dpi=150)
                img_bytes = pix.tobytes("png")

                problemas = {}

                # Moderation labels
                resposta_moderation = rekognition.detect_moderation_labels(
                    Image={'Bytes': img_bytes},
                    MinConfidence=50
                )
                for label in resposta_moderation.get('ModerationLabels', []):
                    nome = label['Name']
                    conf = label['Confidence']
                    if nome in conf_por_item and conf >= conf_por_item[nome]:
                        problemas[nome] = f"{nome} ({conf:.1f}%)"

                # Visual labels
                resposta_labels = rekognition.detect_labels(
                    Image={'Bytes': img_bytes},
                    MaxLabels=50,
                    MinConfidence=50
                )
                for label in resposta_labels.get('Labels', []):
                    nome = label['Name']
                    conf = label['Confidence']
                    if nome in conf_por_item and conf >= conf_por_item[nome]:
                        problemas[nome] = f"{nome} ({conf:.1f}%)"

                if problemas:
                    resultados.append({
                        "Relatório": numero_relatorio,
                        "Página": i + 1,
                        "Problemas detectados": ", ".join(sorted(problemas.values()))
                    })

            except Exception as e:
                resultados.append({
                    "Relatório": numero_relatorio,
                    "Página": i + 1,
                    "Problemas detectados": f"Erro ao processar: {str(e)}"
                })

    if resultados:
        resultado_df = pd.DataFrame(resultados)
        display(Markdown("### 🚫 Problemas detectados a partir da 3ª página de cada relatório"))
        display(resultado_df)
        resultado_df.to_csv("relatorio_conteudo_inapropriado.csv", index=False)
    else:
        print("✅ Nenhum conteúdo inapropriado foi detectado nas páginas analisadas.")

