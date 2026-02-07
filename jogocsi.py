import sys
import os
import time
import json
import random
import subprocess
import threading
import textwrap
from datetime import datetime

import sys
import os

# --- FUNÇÃO OBRIGATÓRIA PARA O EXE FUNCIONAR ---
def resource_path(relative_path):
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- CONFIGURAÇÕES DE DIRETÓRIOS (USANDO A FUNÇÃO NOVA) ---
# Em vez de usar DIRETORIO_RAIZ fixo, uso a função:
PASTA_AUDIO = resource_path(os.path.join("assets", "audio"))
PASTA_VIDEO = resource_path(os.path.join("assets", "video"))
PASTA_DADOS = resource_path(os.path.join("data"))


# --- CONFIGURAÇÕES GERAIS ---
ARQUIVO_DADOS = "agentes_csi.json"
MODO_OFFLINE = False 
LARGURA_TELA = 80

# --- CORES ---
class Cor:
    VERDE = '\033[92m'
    VERDE_NEON = '\033[1;92m'
    VERMELHO = '\033[91m'
    VERMELHO_SANGUE = '\033[1;91m'
    AZUL_CYBER = '\033[96m'
    CYAN = '\033[36m' 
    AMARELO = '\033[93m'
    BRANCO = '\033[97m'
    CINZA = '\033[90m'
    ROXO = '\033[95m'
    RESET = '\033[0m'
    NEGRITO = '\033[1m'

# --- BANCO DE DADOS COMPLETO  ---

# --- BANCO DE DADOS: SEGREDOS DA VÍTIMA (MOTIVAÇÃO GERAL) ---
HISTORIAS_VITIMA = [
    {
        "titulo": "A Dívida de Jogo",
        "item_bruto": "Bilhete de Aposta Rasgado",
        "ferramenta": "Fita Adesiva",
        "item_final": "Comprovante de Dívida Milionária",
        "revelacao": "A vítima perdeu todo o capital de giro da empresa em corridas de cavalo na semana passada."
    },
    {
        "titulo": "O Filho Secreto",
        "item_bruto": "Foto Queimada",
        "ferramenta": "Luz Ultravioleta",
        "item_final": "Foto Restaurada (Família Secreta)",
        "revelacao": "A vítima tinha uma segunda família em outra cidade e planejava mudar o testamento hoje."
    },
    {
        "titulo": "A Chantagem",
        "item_bruto": "Gravador de Voz Quebrado",
        "ferramenta": "Software de Áudio",
        "item_final": "Áudio Comprometedor",
        "revelacao": "A vítima gravava conversas dos funcionários e sócios para chantageá-los."
    }
]

ARQUETIPOS_COMPLETOS = [

    {"nome": "O médico",
     "video": "medico.mp4",
     "visuais_possiveis": ["jaleco branco", "roupa cirúrgica", "terno com estetoscópio"],
     "personalidade": "calmo e meticuloso",
     "luto": "Ele era mais que um paciente, era um amigo.",
     "segredos": [
         {
             "titulo": "Prescrição Ilegal",
             "item_bruto": "Receita Médica Rasgada",
             "ferramenta": "Scanner",
             "item_final": "Lista de Prescrições Ilegais",
             "revelacao": "Ele vendia medicamentos controlados para traficantes locais."
         },
         {
             "titulo": "Erro Médico",
             "item_bruto": "Prontuário Amassado",
             "ferramenta": "Luz Ultravioleta",
             "item_final": "Relatório de Erro Médico",
             "revelacao": "A vítima morreu devido a um erro cirúrgico que ele tentou encobrir."
         },
         {
             "titulo": "Suborno",
             "item_bruto": "Envelope Lacrado",
             "ferramenta": "Abridor de Cartas (Bisturi)",
             "item_final": "Comprovante de Suborno",
             "revelacao": "Ele recebia dinheiro da vítima para falsificar laudos médicos."
         }
     ]
    },
  {
    "nome": "O Chef",
    "video": "chef.mp4",
    "visuais_possiveis": ["dólmã branco manchado", "avental preto sujo", "uniforme de cozinha"],
    "personalidade": "orgulhoso e estressado",
    "luto": "Perdi o apetite desde então.",
    "segredos": [
        {
            "titulo": "O Desvio de Verba",
            "item_bruto": "Notas Fiscais Amassadas",
            "ferramenta": "Scanner",
            "item_final": "Planilha de Caixa 2",
            "revelacao": "Ele comprava carne de segunda e cobrava como Wagyu, embolsando a diferença."
        },
        {
            "titulo": "A Demissão",
            "item_bruto": "Carta na Lixeira",
            "ferramenta": "Fita Adesiva",
            "item_final": "Aviso Prévio Rasgado",
            "revelacao": "A vítima ia demiti-lo por incompetência após 15 anos de casa."
        },
        {
            "titulo": "O Veneno",
            "item_bruto": "Frasco Sem Rótulo",
            "ferramenta": "Kit Químico",
            "item_final": "Veneno de Rato (Arsênico)",
            "revelacao": "Ele jura que era para a dedetização da despensa, mas estava escondido em suas coisas."
        }
    ]
  },

  {
    "nome": "O Hacker",
    "video": "hacker.mp4",
    "visuais_possiveis": ["moletom com capuz", "camiseta de anime", "roupa preta discreta"],
    "personalidade": "irônico e desconfiado",
    "luto": "Isso saiu do controle. Deu tela azul.",
    "segredos": [
        {
            "titulo": "Espionagem Industrial",
            "item_bruto": "HD Externo Danificado",
            "ferramenta": "Computador Forense",
            "item_final": "Arquivos de Venda de Dados",
            "revelacao": "Ele estava vendendo os segredos da empresa da vítima para concorrentes."
        },
        {
            "titulo": "Roubo de Cripto",
            "item_bruto": "Papel com Códigos QR",
            "ferramenta": "Scanner",
            "item_final": "Carteira de Bitcoin da Vítima",
            "revelacao": "Ele transferiu fundos da conta da vítima minutos antes do crime."
        },
        {
            "titulo": "Identidade Falsa",
            "item_bruto": "Passaporte Escondido",
            "ferramenta": "Luz Ultravioleta",
            "item_final": "Passaporte Falso (Interpol)",
            "revelacao": "Ele é um fugitivo internacional e a vítima havia descoberto sua identidade real."
        }
    ]
  },

  {
    "nome": "A Viúva",
    "video": "viuva.mp4",
    "visuais_possiveis": ["vestido preto longo", "roupão de seda", "traje de luto chique"],
    "personalidade": "emocionalmente instável",
    "luto": "Como vou viver sem o dinheiro... digo, sem ele?",
    "segredos": [
        {
            "titulo": "O Amante",
            "item_bruto": "Celular Descartável",
            "ferramenta": "Cabo de Dados",
            "item_final": "Histórico de Chat (Amante)",
            "revelacao": "Ela mantinha um caso secreto e planejava fugir com o amante."
        },
        {
            "titulo": "O Divórcio",
            "item_bruto": "Papéis Molhados",
            "ferramenta": "Secador Térmico", # Ferramenta nova (vamos assumir que o Lab tem)
            "item_final": "Petição de Divórcio",
            "revelacao": "A vítima ia pedir o divórcio litigioso e deixá-la sem nenhum centavo."
        },
        {
            "titulo": "Seguro de Vida",
            "item_bruto": "Envelope Lacrado",
            "ferramenta": "Abridor de Cartas (Bisturi)",
            "item_final": "Apólice de Seguro Alterada",
            "revelacao": "Ela dobrou o valor do seguro de vida da vítima na semana passada."
        }
    ]
  },

  {
    "nome": "O Guarda-Costas",
    "video": "guarda_costas.mp4",
    "visuais_possiveis": ["terno e óculos escuros", "jaqueta tática", "uniforme de segurança"],
    "personalidade": "reservado e profissional",
    "luto": "Falhei na proteção. O alvo foi eliminado.",
    "segredos": [
        {
            "titulo": "Falha de Segurança",
            "item_bruto": "Registro de Ponto",
            "ferramenta": "Lupa",
            "item_final": "Log de Ausência",
            "revelacao": "Ele saiu para beber no bar da esquina na hora exata do crime."
        },
        {
            "titulo": "Passado Violento",
            "item_bruto": "Ficha Criminal Velha",
            "ferramenta": "Banco de Dados Policial",
            "item_final": "Mandado de Prisão (Agressão)",
            "revelacao": "Ele mentiu na contratação e a vítima ameaçou denunciá-lo."
        },
        {
            "titulo": "Dívida",
            "item_bruto": "Nota Promissória",
            "ferramenta": "Luz Ultravioleta",
            "item_final": "Reconhecimento de Dívida",
            "revelacao": "Ele devia uma fortuna para a vítima e estava sendo cobrado diariamente."
        }
    ]
  },

  {
    "nome": "O Mordomo",
    "video": "mordomo.mp4",
    "visuais_possiveis": ["uniforme clássico", "colete preto", "luvas brancas"],
    "personalidade": "discreto e observador",
    "luto": "Servi esta casa por décadas. Uma tragédia.",
    "segredos": [
        {
            "titulo": "O Testamento",
            "item_bruto": "Rascunho Manuscrito",
            "ferramenta": "Análise Grafotécnica", # Pode simplificar pra Lupa
            "item_final": "Testamento Falsificado",
            "revelacao": "O testamento foi alterado à mão para incluir o mordomo na herança."
        },
        {
            "titulo": "Vinhos Roubados",
            "item_bruto": "Garrafa Vazia de 1950",
            "ferramenta": "Lupa",
            "item_final": "Rótulo Trocado",
            "revelacao": "Ele bebia os vinhos caros da adega e enchia as garrafas com vinho barato."
        },
        {
            "titulo": "Vingança Antiga",
            "item_bruto": "Diário Velho",
            "ferramenta": "Lupa",
            "item_final": "Página Marcada (Ódio)",
            "revelacao": "O pai da vítima arruinou a família do mordomo no passado."
        }
    ]
  }
]


# Dados Complementares para evitar erros
LOCAIS_EXPANDIDOS = ["Apartamento de Luxo", "Beco Escuro", "Sala de Servidores", "Estacionamento Subsolo", "Mansão na Serra", "Laboratório,quarto andar", "Cobertura Panorâmica", "Clube Noturno", "Escritório Corporativo", "Parque Abandonado, Centro da Cidade", "Restaurante Chique", "Hotel 5 Estrelas", "Bar da Esquina", "Galeria de Arte", "Cinema Privado"]

TESTEMUNHAS_INICIAIS = ["o entregador", "uma vizinha", "o zelador", "um corredor", "a faxineira", "um segurança", "o porteiro", "um turista perdido", "a garçonete", "um ciclista", "o motorista de táxi", "um pedestre apressado", "a criança brincando", "o jardineiro", "o vendedor ambulante", "a fotógrafa", "o policial de ronda", "o morador local"]


POSICOES_CORPO = ["caído de bruços", "sentado na poltrona", "estirado no chão", "escondido no armário", "encostado na parede", "deitado na cama", "ajoelhado no tapete", "em pé, encostado na mesa", "caído na escada", "dentro do carro", "no banheiro", "na varanda", "no porão", "na cozinha", "no jardim", "na garagem"]    

# ---  BANCO DE PISTAS IRRELEVANTES  ---
PISTAS_IRRELEVANTES = [
    # >> LIXO REAL (TIER 0 - Não serve pra nada)
    "Embalagem de Fast-Food", "Jornal Velho de Ontem", "Lata de Refrigerante",
    "Cigarro Apagado", "Chiclete Grudado", "Clipe de Papel", "Garrafa de Água",
    "Panfleto de Pizzaria", "Recibo de Mercado (Leite/Pão)", "Caneta sem Tinta",
    
    # >> ITENS DE CRAFTING (TIER 1 - Precisam do Laboratório)
    "Bilhete de Aposta Rasgado", "Foto Queimada", "Gravador de Voz Quebrado", # Vítima
    "Notas Fiscais Amassadas", "Carta na Lixeira", "Frasco Sem Rótulo", # Chef
    "HD Externo Danificado", "Papel com Códigos QR", "Passaporte Escondido", # Hacker
    "Celular Descartável", "Papéis Molhados", "Envelope Lacrado", # Viúva
    "Registro de Ponto", "Ficha Criminal Velha", "Nota Promissória", # Guarda     
    "Rascunho Manuscrito", "Garrafa Vazia de 1950", "Diário Velho", # Mordomo
    
    # >> FERRAMENTAS DE LAB (NECESSÁRIAS PARA CRAFTING) <<:
    "Fita Adesiva", "Luz Ultravioleta", "Scanner de Mão", "Kit Químico",
    "Software de Áudio", "Cabo de Dados", "Lupa", "Abridor de Cartas"

]

# Lista VIP para a Equipe Forense (Mais ferramentas, menos lixo)
SUPRIMENTOS_FORENSE = [
    "Fita Adesiva", "Luz Ultravioleta", "Scanner de Mão", 
    "Kit Químico", "Software de Áudio", "Cabo de Dados", 
    "Lupa", "Abridor de Cartas", "Luvas de Látex", 
    "Cotonete Estéril", "Saco de Evidência",
    "Lanterna Tática" # Adicionei uns itens novos pra dar clima
]

# ---  O CRIMES_DB  ---
CRIMES_DB = [
    {
        "arma": "Arsênico (Veneno)", 
        "evidencia": "Odor de amêndoas amargas e coloração vermelho-cereja na pele", # Dica técnica
        "dica_neide": "frascos de remédio sem rótulo", 
        "pistas_relevantes": ["Copo com resíduo químico", "Vômito com sangue", "Pó cristalino branco"]
    },
    {
        "arma": "Pistola 9mm", 
        "evidencia": "pó preto", # Dica técnica
        "dica_neide": "uma peça de metal preta", 
        "pistas_relevantes": ["Cápsula de bala deflagrada", "Resíduo de chumbo nas mãos", "Buraco na parede"]
    },
    {
        "arma": "Faca de Caça", 
        "evidencia": "Lacerações defensivas nos antebraços e choque hipovolêmico", # Dica técnica
        "dica_neide": "brilho de metal afiado", 
        "pistas_relevantes": ["Padrão de sangue em esguicho (Arterial)", "Faca limpa no escorredor", "Luva rasgada"]
    },
    {
        "arma": "Corda de Piano", 
        "evidencia": "Petéquias (pontos vermelhos) nos olhos e fratura no osso hioide", # Dica técnica para estrangulamento
        "dica_neide": "algo enrolado nas mãos", 
        "pistas_relevantes": ["Fibras sintéticas sob as unhas", "Marca linear no pescoço", "Cadeira tombada"]
    },
    {
        "arma": "Objeto Contundente (Troféu)", 
        "evidencia": "Traumatismo craniano com afundamento parietal", # Dica técnica para pancada
        "dica_neide": "algo pesado sendo erguido", 
        "pistas_relevantes": ["Fragmentos de vidro/metal no cabelo", "Mancha de sangue radial", "Objeto pesado fora do lugar"]
    }
]

# --- SISTEMA DE NOTÍCIAS (TURNO A TURNO) ---
MANCHETES_DB = {
    "inicio": [
        "URGENTE: Corpo encontrado. Polícia isola a área.",
        "MISTÉRIO: Vizinhos relatam silêncio absoluto na hora do crime.",
        "SEM PISTAS no momento, Delegado pede paciência à imprensa.",
        "QUEM É A VÍTIMA? Redes sociais especulam teorias."
    ],
    "meio": [ # Aparece depois de 5 ações
        "PRESSÃO AUMENTA: Prefeito cobra resultados rápidos.",
        "MEDO NA VIZINHANÇA: Vendas de cadeados triplicam na cidade.",
        "ASSASSINO ENTRE NÓS? Moradores evitam sair de casa.",
        "VAZAMENTO: Fonte anônima diz que a polícia já tem um suspeito."
    ],
    "fim": [ # Aparece depois de 10 ações (O cerco fecha)
        "CRISE NA SEGURANÇA: População exige a cabeça do Chefe de Polícia.",
        "PÂNICO TOTAL: Rumores de que o assassino esta indo atras da Dona Neide.",
        "ULTIMATO: Governador dá 24 horas para solução do caso.",
        "aSSASSINO À SOLTA: Cidadãos formam grupos de vigilância noturna.",
        "JUSTIÇA OU CAOS? Protestos marcados em frente à delegacia."
    ]
}

# --- SISTEMAS VISUAIS (EFEITOS HACKER) ---
def digitar(texto, velocidade=0.015, cor=Cor.VERDE_NEON):
    sys.stdout.write(cor)
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(velocidade)
    sys.stdout.write(Cor.RESET + "\n")

def barra_carregamento(titulo="PROCESSANDO"):
    sys.stdout.write(f"{Cor.CINZA}{titulo}...{Cor.RESET}\n")
    largura = 30
    sys.stdout.write(f"{Cor.AZUL_CYBER}[")
    for i in range(largura):
        time.sleep(random.uniform(0.01, 0.03))
        sys.stdout.write("█")
        sys.stdout.flush()
    sys.stdout.write(f"] 100%{Cor.RESET}\n")
    time.sleep(0.3)

# --- DRIVERS E CLASSES ---
try:
    import pygame
    pygame.init(); pygame.mixer.init()
    TEM_PYGAME = True
except: TEM_PYGAME = False

try:
    import pywhatkit; import pyautogui 
    TEM_ZAP = True
except: TEM_ZAP = False

# 1. DEFINIÇÃO DA CLASSE DE MÍDIA
class MediaManager:
    def tocar_ambiente(self, nome):
        # Monta o caminho completo: assets/audio/nome_do_arquivo
        caminho_completo = os.path.join(PASTA_AUDIO, nome)
        
        if TEM_PYGAME and os.path.exists(caminho_completo):
            try: 
                pygame.mixer.music.load(caminho_completo) # Usa o caminho completo
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.4)
            except: pass

    def tocar_efeito(self, nome, loop=False):
        caminho_completo = os.path.join(PASTA_AUDIO, nome) # Monta o caminho
        
        if TEM_PYGAME and os.path.exists(caminho_completo):
            try: 
                som = pygame.mixer.Sound(caminho_completo) # Usa o caminho completo
                som.play(-1 if loop else 0)
                return som
            except: return None

    def parar_ambiente(self):
        if TEM_PYGAME: 
            try: pygame.mixer.music.stop()
            except: pass

    def parar_tudo(self):
        if TEM_PYGAME: 
            try: pygame.mixer.stop(); pygame.mixer.music.stop()
            except: pass

    def tocar_video_hacker(self, video_file, audio_file=None):
        # --- PAUSA A CÂMERA DE VIGILÂNCIA PARA NÃO TRAVAR ---
        global cctv_em_pausa
        cctv_em_pausa = True
        time.sleep(0.5) # Dá meio segundo para a janela fechar
        # ----------------------------------------------------

        # Verifica se o arquivo existe
        if not os.path.exists(video_file):
            print(f"{Cor.AMARELO}>> ARQUIVO DE VÍDEO NÃO ENCONTRADO...{Cor.RESET}")
            cctv_em_pausa = False # <--- IMPORTANTE: RELIGA SE DER ERRO
            time.sleep(1)
            return

        # Toca audio de fundo
        if audio_file and TEM_PYGAME and os.path.exists(audio_file):
            som_fundo = pygame.mixer.Sound(audio_file)
            som_fundo.play()
        else:
            som_fundo = None

        try:
            import cv2
            cap = cv2.VideoCapture(video_file)
            window_name = "PERFILAMENTO (ENTER para PULAR)"
            
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
            cv2.resizeWindow(window_name, 960, 540) 

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break 
                cv2.imshow(window_name, frame)
                
                if cv2.waitKey(25) in [13, 32, 27, ord('q')]: 
                    print(f"\n{Cor.AMARELO}>> VÍDEO INTERROMPIDO PELO USUÁRIO.{Cor.RESET}")
                    break
            
            cap.release()
            cv2.destroyAllWindows()
        except:
            try: os.startfile(video_file)
            except: pass
        
        if som_fundo: som_fundo.stop()

        # --- RELIGA A CÂMERA DE VIGILÂNCIA ---
        cctv_em_pausa = False
        # -------------------------------------

    def efeito_matrix(self):
        # ... (seu código matrix continua igual)
        pass

media = MediaManager()

# 3. DEFINIÇÃO DA CLASSE DE ÁUDIO (ANTES DE USAR!)
class AudioSystem:
    def falar(self, texto):
        # Limpa o texto
        limpo = texto.replace('*', '').replace('"', '').replace("'", "")
        
        # Gera nome temporário
        nome_arq = f"temp_voz_{random.randint(1000,9999)}.mp3"
        # Define o caminho para SALVAR DENTRO DA PASTA DE AUDIO (Organização)
        caminho_final = os.path.join(PASTA_AUDIO, nome_arq)
        
        try:
            # Cria o arquivo de áudio
            subprocess.run([sys.executable, "-m", "edge_tts", "--voice", "pt-BR-AntonioNeural", "--text", limpo, "--write-media", caminho_final], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if os.path.exists(caminho_final) and TEM_PYGAME:
                # Toca o áudio
                pygame.mixer.music.set_volume(0.1) # Baixa o som de fundo
                som = pygame.mixer.Sound(caminho_final)
                som.play()
                
                # TRAVA O CÓDIGO ENQUANTO FALA (Essencial para não encavalar)
                while pygame.mixer.get_busy(): 
                    time.sleep(0.1)
                
                pygame.mixer.music.set_volume(0.4) # Restaura volume
                
                # Tenta deletar o arquivo para não sujar o PC
                try:
                    som.stop()
                    del som
                    os.remove(caminho_final)
                except: pass # Se o Windows bloquear, pelo menos está na pasta audio escondido
        except: pass

# 4. INSTANCIA O AUDIO SYSTEM (SÓ AGORA, QUE A CLASSE JÁ EXISTE)
audio = AudioSystem()

# --- SISTEMA DE VIGILÂNCIA (OMNI-VIEW) ---
executando_cctv = False
cctv_em_pausa = False

def sistema_omni_view():
    global executando_cctv, cctv_em_pausa # <--- ADICIONE cctv_em_pausa AQUI
    import cv2
    import numpy as np 
    
    janela_nome = "SISTEMA DE VIGILANCIA (AO VIVO)"
    
    # Configurações iniciais
    video_padrao = "chiado.mp4"
    videos_evento = ["suspeito1.mp4", "suspeito2.mp4", "matrix.mp4","suspeito3.mp4","suspeito4.mp4"] 
    proximo_evento = time.time() + random.randint(30, 60)
    
    while executando_cctv:
        # --- PROTOCOLO DE PAUSA (EVITA O TRAVAMENTO) ---
        if cctv_em_pausa:
            # Se estiver pausado, fecha a janela para liberar recurso pro outro vídeo
            try: cv2.destroyWindow(janela_nome)
            except: pass
            time.sleep(1) # Dorme 1 segundo e checa de novo
            continue
        # -----------------------------------------------

        # Recria a janela se ela tiver sido fechada
        cv2.namedWindow(janela_nome, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(janela_nome, 600, 400)
        cv2.moveWindow(janela_nome, 950, 50)
        try: cv2.setWindowProperty(janela_nome, cv2.WND_PROP_TOPMOST, 1)
        except: pass

        # A. DECIDE QUAL VÍDEO TOCAR
        agora = time.time()
        
        if agora >= proximo_evento:
            nome_video = random.choice(videos_evento)
            proximo_evento = time.time() + random.randint(60, 120)
            modo_susto = True
        else:
            nome_video = video_padrao
            modo_susto = False

        caminho = os.path.join(PASTA_VIDEO, nome_video)
        cap = cv2.VideoCapture(caminho)
        
        if not cap.isOpened():
             time.sleep(1)
             continue

        # B. TOCA O VÍDEO SELECIONADO
        while cap.isOpened() and executando_cctv:
            # VERIFICA PAUSA DENTRO DO LOOP TAMBÉM
            if cctv_em_pausa: break 

            ret, frame = cap.read()
            if not ret: break 
            
            # Interrompe chiado para susto
            if not modo_susto and time.time() >= proximo_evento: break 

            cv2.putText(frame, "REC AO VIVO", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            if modo_susto:
                cv2.putText(frame, "MOVIMENTO DETECTADO", (20, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "SEM SINAL...", (20, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
            
            cv2.imshow(janela_nome, frame)
            
            if cv2.waitKey(30) & 0xFF == ord('q'):
                executando_cctv = False
                break
        
        cap.release()
    
    cv2.destroyAllWindows()

class InvestigationManager:
    def __init__(self, suspeitos, culpado):
        self.suspeitos = suspeitos
        self.culpado = culpado
        self.contador_pressao = {s['nome']: 0 for s in suspeitos}
        self.inventario = []
        
        # --- SORTEIO DOS SEGREDOS ---
        self.segredo_vitima = random.choice(HISTORIAS_VITIMA)
        self.mapa_segredos = {} 
        self.segredos_ativos = [] 
        
        # Adiciona o da vítima
        self.segredos_ativos.append(self.segredo_vitima)
        self.mapa_segredos[self.segredo_vitima['item_final']] = "VITIMA"
        
        for s in self.suspeitos:
            if 'segredos' in s:
                segredo_escolhido = random.choice(s['segredos'])
                self.segredos_ativos.append(segredo_escolhido)
                self.mapa_segredos[segredo_escolhido['item_final']] = s 

    def adicionar_item(self, item):
        if item not in self.inventario:
            self.inventario.append(item)
            return True
        return False

    def combinar_itens(self):
        receitas = {}
        for segredo in self.segredos_ativos:
            par = (segredo['item_bruto'], segredo['ferramenta'])
            receitas[par] = segredo['item_final']

        if len(self.inventario) < 2:
            return "ERRO: Você precisa de pelo menos 2 itens (Pista + Ferramenta).", False
            
        print("\nSELECIONE DOIS ITENS PARA PROCESSAR:")
        for i, item in enumerate(self.inventario):
            print(f"[{i+1}] {item}")
        
        try:
            print("\n--------------------------------")
            escolha1 = int(input("Digite o número do 1º item: ")) - 1
            escolha2 = int(input("Digite o número do 2º item: ")) - 1
            print("--------------------------------")

            if escolha1 < 0 or escolha1 >= len(self.inventario) or \
               escolha2 < 0 or escolha2 >= len(self.inventario) or \
               escolha1 == escolha2:
                return "ERRO: Escolha inválida.", False
            
            item_A = self.inventario[escolha1]
            item_B = self.inventario[escolha2]
            
            print(f"PROCESSANDO: {item_A} + {item_B}...")
            time.sleep(1) 

            novo_item = None
            for (ingrediente1, ingrediente2), resultado in receitas.items():
                if (item_A == ingrediente1 and item_B == ingrediente2) or \
                   (item_A == ingrediente2 and item_B == ingrediente1):
                    novo_item = resultado
                    break 

            if novo_item:
                if escolha1 > escolha2:
                    self.inventario.pop(escolha1); self.inventario.pop(escolha2)
                else:
                    self.inventario.pop(escolha2); self.inventario.pop(escolha1)
                self.inventario.append(novo_item)
                return f"SUCESSO! Análise revelou:\n>> {novo_item}", True
            else:
                # --- CORREÇÃO DA MENSAGEM DE ERRO ---
                # Lista de ferramentas conhecidas para checagem
                ferramentas_validas = [
                    "Fita", "Luz", "Scanner", "Kit", "Software", 
                    "Cabo", "Lupa", "Abridor", "Computador", "Análise"
                ]
                
                tem_ferramenta_A = any(f in item_A for f in ferramentas_validas)
                tem_ferramenta_B = any(f in item_B for f in ferramentas_validas)

                # SE NENHUM DOS DOIS FOR FERRAMENTA:
                if not tem_ferramenta_A and not tem_ferramenta_B:
                    return "ERRO: Combinação inválida! Você precisa de pelo menos uma FERRAMENTA (Lupa, Scanner, Cabo, etc) para analisar uma Pista.", False

                # SE TEM FERRAMENTA MAS NÃO DEU CERTO (Dicas Específicas):
                dica = "FALHA: Essas peças não reagem entre si."
                if ("Foto" in item_A or "Foto" in item_B) and "Fita" in item_A:
                     dica = "DICA: Fita adesiva não conserta fotos queimadas. Tente Luz UV."
                elif ("Scanner" in item_A or "Scanner" in item_B) and ("Celular" in item_A or "Celular" in item_B):
                    dica = "DICA: O Scanner só serve para PAPEL! Para o celular, tente conectar um CABO."
                elif ("Cabo" in item_A or "Cabo" in item_B) and ("Papel" in item_A or "Carta" in item_B):
                    dica = "DICA: Não tem onde plugar o cabo no papel! Use o SCANNER."
                elif ("Luz" in item_A or "Luz" in item_B) and ("Celular" in item_A or "Notebook" in item_B):
                    dica = "DICA: A Luz UV serve para achar manchas, não eletrônicos."
                
                return dica, False

        except ValueError: return "ERRO: Digite apenas números.", False

    def pressionar_suspeito(self, idx):
        alvo = self.suspeitos[idx]
        nome = alvo['nome']
        self.contador_pressao[nome] += 1
        pressao = self.contador_pressao[nome]
        
        if pressao == 1:
            fala = alvo.get('luto', "Estou em choque.")
            return f"Depoimento: {nome}\nStatus: EM LUTO\n---\n\"{fala}\"", False, pressao
        elif pressao == 2:
            alibi = alvo.get('alibi', "Estava em casa.")
            fala = f"Eu não fiz nada! {alibi}."
            return f"Depoimento: {nome}\nStatus: DEFENSIVO (ÁLIBI)\n---\n\"{fala}\"", False, pressao
        elif pressao < 5:
            fala = "Vocês estão perdendo tempo."
            return f"Depoimento: {nome}\nStatus: RESISTINDO\n---\n\"{fala}\"", False, pressao
        else:
            return f"{nome} ESTÁ EM PÂNICO! (Use evidência)", True, pressao

    def get_prova_alibi(self, idx): 
        return self.suspeitos[idx].get('prova_alibi', 'Nenhuma prova registrada.')
    
    def verificar_alibi_prova(self, idx):
        if idx < 0 or idx >= len(self.suspeitos): return "Erro."
        alvo = self.suspeitos[idx]
        if self.contador_pressao[alvo['nome']] < 2:
            return f"{alvo['nome']} ainda não deu álibi. Pressione mais."
        return f"VERIFICAÇÃO DE ÁLIBI:\nPROVA: {alvo.get('prova_alibi', 'Sem registro')}"
    
    def pegar_pista_camera(self): 
        return f"Vulto detectado: {self.culpado.get('visual', 'Desconhecido')}."

    def confrontar_com_evidencia(self, idx_suspeito, item_usado, detalhes_crime):
        alvo = self.suspeitos[idx_suspeito]
        
        # 1. É A ARMA DO CRIME?
        if item_usado in detalhes_crime['pistas_relevantes']:
            if alvo == self.culpado:
                self.contador_pressao[alvo['nome']] = 6
                return (f"(PÂNICO) \"VOCÊ ACHOU?! {item_usado}... Eu explico!\""), True
            else:
                return (f"(ASSUSTADO) \"Isso é do assassino! Tira daqui!\""), False

        # 2. É UM SEGREDO?
        if item_usado in self.mapa_segredos:
            dono = self.mapa_segredos[item_usado]
            if dono == alvo:
                historia = next(s for s in self.segredos_ativos if s['item_final'] == item_usado)
                return (f"[BARGANHA]\n{alvo['nome']}: \"Ok! {historia['revelacao']}\nMas não matei!\""), True
            elif dono != "VITIMA":
                return (f"[DELAÇÃO]\n{alvo['nome']}: \"Haha! Isso é podre do {dono['nome']}!\""), False
            else:
                return (f"[MOTIVO]\n{alvo['nome']}: \"A vítima fez isso? {self.segredo_vitima['revelacao']}?\""), False

        return f"{alvo['nome']}: \"{item_usado}? Lixo irrelevante.\"", False

    def get_prova_alibi(self, idx):
        # Função simples para pegar a prova sem aumentar a pressão
        return self.suspeitos[idx]['prova_alibi']

    # --- NOVA FUNÇÃO PARA CHECAR A PROVA ---
    def verificar_alibi_prova(self, idx):
        if idx < 0 or idx >= len(self.suspeitos): return "Erro: Suspeito inválido."
        
        alvo = self.suspeitos[idx]
        pressao = self.contador_pressao[alvo['nome']]
        
        # Só libera a prova se já tiver passado do nível 1 (Luto)
        if pressao < 2:
            return f"{alvo['nome']} ainda não declarou um álibi oficial. Pressione-o mais um pouco."
        else:
            return f"VERIFICAÇÃO DE ÁLIBI ({alvo['nome']}):\nPROVA APRESENTADA: {alvo['prova_alibi']}"

    def pegar_pista_camera(self):
        chance = random.random()

        if chance < 0.3:
            return f"Vulto detectado: Alguém vestindo {self.culpado['visual']}."
        elif chance < 0.6:
            return "Imagem com ruído intenso. Possível sabotagem no sistema."
        else:
            return "Imagem corrompida. Interferência estática."

class DonaNeide:
    def __init__(self, suspeitos, culpado, historia):
        self.papo_furado = [
            "Noite passada a Taynara só gritava Bryan!",
            "Fiquei sabendo que o Maykon corta muito bem os cabelos.",  
            "Comprei um sapato novo semana passada, lindo demais.",          
            "A Professora Angelica é um doce de pessoa.",
            "O Michael se formou em eletrotécnica, menino inteligente.",
            "Aquele ator novo da Globo é a cara do Luciano Huck, acho que se chama Jhon",
            "O bolo de cenoura da Kenya parece tão gostoso o cheiro vem aqui.",
            "Minha neta instalou esse tal de 'Tinder' no meu celular.",
            "Você viu o novo filme do Alice no país das maldiçoes? Dizem que é ótimo!",
            "Ontem o vizinho do 302 estava falando sozinho, sera que é o Senhor fulano? coitado.",
            "Aceita um cafezinho? Acabei de passar."
        ]
        
        self.fofocas = []
        
        # 1. Fofocas sobre Inocentes (Gera 3 aleatórias para não poluir)
        inocentes = [s for s in suspeitos if s != culpado]
        random.shuffle(inocentes)
        for inocente in inocentes[:3]: # Pega só 3 inocentes para não encher de texto
            fatos = [
                f"Não fui com a cara de {inocente['nome']}.",
                f"Vi {inocente['nome']} saindo apressado ontem.",
                f"Dizem que {inocente['nome']} devia dinheiro à vítima.",
                f"O {inocente['nome']} estava rondando o prédio."
            ]
            self.fofocas.append(random.choice(fatos))
        
        # 2. Fofoca sobre o Culpado (Dica Visual)
        visual = culpado['visual'].lower()
        dica_visual = random.choice(visual.split()) if ' ' in visual else visual
        self.fofocas.append(f"O suspeito corria... usava algo '{dica_visual}'.")
        self.fofocas.append(f"Vi um vulto com roupa '{dica_visual}' fugindo.")

        # 3. ITENS ÚNICOS (Sem repetição!)
        # Adiciona apenas UMA vez cada item.
        itens_neide = [
            "Achei este papel: 'Senha Anotada'. Pode ficar.",
            "Vi uma 'Chave Enferrujada' no vaso. Toma.",
            "Menino, achei essa 'Lupa' velha. Serve?",
            "Toma essa 'Fita Adesiva', vai que precisa.",
            "Achei esse 'Cartão de Acesso' no tapete.",
            "Esqueceram essa 'Tabela de Símbolos' no elevador.",
            "Peguei essa 'Carta de Advogado' por engano."
             
        ]
        # Adiciona todos os itens à lista de fofocas
        self.fofocas.extend(itens_neide)
        
        # Embaralha tudo para você não saber quando vem item ou fofoca
        random.shuffle(self.fofocas)

    def fofocar(self):
        if self.fofocas:
            intro = random.choice(self.papo_furado)
            dica = self.fofocas.pop(0) 
            
            # LISTA DE ITENS QUE A NEIDE PODE ENTREGAR
            # O código procura se o nome do item está na frase da fofoca
            itens_neide = [
                "Senha Anotada", "Chave Enferrujada", "Lupa", 
                "Fita Adesiva", "Cartão de Acesso", "Tabela de Símbolos",
                "Carta de Advogado"
            ]
            
            item_encontrado = None
            for item in itens_neide:
                if item in dica: # Se o nome do item estiver na frase
                    item_encontrado = item
                    break
            
            if item_encontrado:
                return f"{intro}\n\n(Ela te entrega algo) Toma, achei isso: {item_encontrado}", item_encontrado
            
            return f"{intro}\n\n(Sussurrando) Mas olha... {dica}", None
        else:
            return "Menino, já te contei tudo! Não sei de mais nada. Vai trabalhar!", None

def gerar_detalhes_crime():
    # 1. Gera a Hora da Morte (Entre 00:00 e 05:00 da manhã)
    hora_h = random.randint(1, 4)
    minuto_h = random.randint(0, 59)
    hora_morte_str = f"{hora_h:02d}:{minuto_h:02d}"
    
    # 2. Gera a Hora da Câmera (30 a 50 minutos ANTES da morte)
    # Isso garante que a cena da câmera seja o "motivo" ou a "briga"
    minutos_totais_morte = hora_h * 60 + minuto_h
    minutos_camera = minutos_totais_morte - random.randint(30, 50)
    
    # Converte de volta para Texto (HH:MM)
    h_cam = minutos_camera // 60
    m_cam = minutos_camera % 60
    hora_camera_str = f"{h_cam:02d}:{m_cam:02d}"

    c = random.choice(CRIMES_DB)
    return {
        "local": random.choice(LOCAIS_EXPANDIDOS),
        "hora": hora_morte_str,       # Hora oficial do óbito
        "hora_camera": hora_camera_str, # Hora da filmagem (NOVO CAMPO)
        "quem_achou": random.choice(TESTEMUNHAS_INICIAIS),
        "posicao": random.choice(POSICOES_CORPO),
        "arma_real": c['arma'], "evidencia": c['evidencia'],
        "dica_neide": c['dica_neide'], "pistas_relevantes": c['pistas_relevantes']
    }

MANCHETES_DO_DIA = {
    "inicio": [
        "URGENTE: Corpo encontrado em circunstâncias misteriosas.",
        "POLÍCIA NO LOCAL: Moradores relatam movimentação estranha.",
        "SILÊNCIO NAS RUAS: Bairro isolado para investigação.",
        "QUEM É A VÍTIMA? Especulações tomam conta das redes sociais."
    ],
    "meio": [
        "SEM RESPOSTAS: Polícia ainda não tem um suspeito principal.",
        "MEDO CRESCE: Vendas de alarmes disparam na região.",
        "EXCLUSIVO: Testemunha afirma ter visto 'vulto' fugindo.",
        "PREFEITO COBRA: 'Precisamos de justiça rápida', diz em coletiva."
    ],
    "fim": [ # Essas aparecem quando o tempo está acabando
        "PÂNICO TOTAL: Assassino pode estar planejando fugir do país!",
        "ULTIMATO: Chefe de Polícia ameaça demissões se caso não for resolvido.",
        "CIDADE EM ALERTA: População tranca as portas com medo.",
        "FRACASSO IMINENTE? Especialistas criticam lentidão da perícia."
    ]
}
 

# --- SUBSTITA A FUNÇÃO gerar_briefing POR ESTA ---
def gerar_briefing_pro(h):
    # Gera dados táticos falsos para imersão
    cod_op = f"OP-{random.randint(100,999)}-BRAVO"
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
    lat = f"-22.{random.randint(1000,9999)}"
    long = f"-43.{random.randint(1000,9999)}"
    
    # Texto formatado como documento oficial
    relatorio = (
        f"--------------ATENÇÃO AGENTES-----------------------\n"
        f"RELATÓRIO DE INCIDENTE CRÍTICO // \n"
        f"--------------------------------------------------------------\n"
        f"DATA/HORA: {data_hora} | "
        f"LOCAL DA OCORRÊNCIA: {h['local']}\n"
        f"CLASSIFICAÇÃO: SIGILOSO (NÍVEL 4)\n"
        f"--------------------------------------------------------------\n"
        f"VÍTIMA IDENTIFICADA: {h['vitima']}\n"
        f"SITUAÇÃO: O corpo foi localizado às {h['hora']} na posição '{h['posicao']}'.\n"
        f"PRIMEIRA RESPOSTA: A testemunha '{h['quem_achou']}' acionou a polícia.\n"
        f"ANÁLISE FORENSE PRELIMINAR: Indica óbito por {h['evidencia']}.\n"
        f"--------------------------------------------------------------\n"
        f"ORDEM DE MISSÃO: Isole o perímetro. Interrogue os suspeitos listados.\n"
        f"Colete evidências físicas e digitais. Autorização de força letal: NEGADA."
        f" Estou enviando para vocês a lista dos suspeitos e detalhes adicionais no arquivo anexo.\n"
        f"Agentes, visitem a Dona Neide. Ela parece ter visto bastante coisa.\n"
        
    )
    return relatorio

def gerar_dossie_suspeitos(lista_suspeitos):
       
    # Cabeçalho do Anexo
    relatorio = (
        f"📂 *LISTA DE PESSOAS SUSPEITAS (PDI)*\n"
        f"PRIORIDADE: ALTA // CONFIDENCIAL\n"
        f"════════════════════════════════════\n"
    )
    
    for i, s in enumerate(lista_suspeitos):
        # Ícones para dar visual no WhatsApp
        icone = "👤"
        if "nervoso" in s['personalidade']: icone = "😰"
        elif "arrogante" in s['personalidade']: icone = "😒"
        elif "calmo" in s['personalidade']: icone = "😐"
        elif "instável" in s['personalidade']: icone = "😭"
        
        # --- AQUI ESTAVA O ERRO, AGORA CORRIGIDO ---
        # Removemos a chave { antes do ID
        relatorio += f"*ID #{i+1:02d} | {s['nome'].upper()}* {icone}\n"
        
        relatorio += f"├─ Perfil: {s['personalidade']}\n\n"
       
    
    relatorio += "------------------------------------\n"
    relatorio += "⚠️ *CUIDADO:* O assassino está nesta lista."
    return relatorio

# --- INTERFACE ---
def limpar_tela(): os.system('cls' if os.name == 'nt' else 'clear')

def logo_profissional():
    limpar_tela()
    print(f"{Cor.AZUL_CYBER}")
    print(r"""
    ██████╗ ███████╗██╗     ██████╗ ██████╗  ██████╗ 
    ██╔════╝██╔════╝██║     ██╔══██╗██╔══██╗██╔═══██╗
    ██║     ███████╗██║     ██████╔╝██████╔╝██║   ██║
    ██║     ╚════██║██║     ██╔═══╝ ██╔══██╗██║   ██║
    ╚██████╗███████║██║     ██║     ██║  ██║╚██████╔╝
     ╚═════╝╚══════╝╚═╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ SYSTEM v15.2
    """)
    # Barra de Status Fake
    memoria = random.randint(12, 64)
    print(f"  ┌────────────────────────────────────────────────────────┐")
    print(f"  │ [SERVER]: {Cor.VERDE_NEON}ONLINE{Cor.AZUL_CYBER}   [MEM]: {memoria}GB   [LATENCY]: {random.randint(10,50)}ms       │")
    print(f"  └────────────────────────────────────────────────────────┘{Cor.RESET}\n")

def painel(titulo, conteudo, cor=Cor.AZUL_CYBER):
    largura_total = 60  # Largura fixa da caixa
    largura_texto = largura_total - 4  # Espaço útil para o texto (tira as bordas)
    
    print(f"\n{cor}╔{'═'* (largura_total-2)}╗{Cor.RESET}")
    print(f"{cor}║{Cor.RESET} {titulo.center(largura_texto)} {cor}║{Cor.RESET}")
    print(f"{cor}╠{'═'* (largura_total-2)}╣{Cor.RESET}")
    
    # Se o conteúdo for uma string única com \n, quebra em lista primeiro
    if isinstance(conteudo, str): 
        paragrafos = conteudo.split('\n')
    else:
        paragrafos = conteudo

    for paragrafo in paragrafos:
        # Aqui está a mágica: O textwrap quebra a linha se ela for grande demais
        # e também lida com as linhas tracejadas (---)
        if set(paragrafo) == {'-'}: # Se for apenas uma linha separadora
             print(f"{cor}║{Cor.RESET} {'-' * largura_texto} {cor}║{Cor.RESET}")
        else:
            linhas_quebradas = textwrap.wrap(paragrafo, width=largura_texto)
            
            # Se a linha for vazia (pulo de linha), imprime espaço em branco
            if not linhas_quebradas:
                print(f"{cor}║{Cor.RESET} {' ' * largura_texto} {cor}║{Cor.RESET}")
            
            for linha in linhas_quebradas:
                # O ljust garante que sobrem espaços em branco até a borda da direita
                print(f"{cor}║{Cor.RESET} {linha.ljust(largura_texto)} {cor}║{Cor.RESET}")
                
    print(f"{cor}╚{'═'* (largura_total-2)}╝{Cor.RESET}\n")

def enviar_zap_turbo(agente, texto):
    if not TEM_ZAP or MODO_OFFLINE: return
    print(f">> Enviando dados para {agente['nome']}...")
    try:
        # 1. Envia a mensagem (o parâmetro 15 é o tempo para carregar a página)
        # O True no final avisa para fechar a aba, mas nem sempre funciona sozinho
        pywhatkit.sendwhatmsg_instantly(agente['telefone'], texto, 20, True)
        
        # 2. Segurança para garantir o envio (Enter)
        time.sleep(5) # Espera a aba abrir
        pyautogui.press('enter')
        
        # 3. Força o fechamento da aba
        time.sleep(4) # Espera a mensagem ir
        print(f"{Cor.CINZA}>> Fechando conexão segura...{Cor.RESET}")
        
        # Tenta fechar a aba atual (CTRL + W)
        pyautogui.hotkey('ctrl', 'w')
        
        # Caso o navegador peça confirmação, aperta Enter de novo
        time.sleep(0.5)
        pyautogui.press('enter')

        # 4. Pausa longa para garantir que o navegador processou antes do próximo
        time.sleep(4) 
        
    except Exception as e: 
        print(f"Erro no envio: {e}")

def menu():
    media.tocar_ambiente("login.mp3")
    
    # Carrega agentes
    agentes = []
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, 'r') as f: agentes = json.load(f)
        except: pass

    while True:
        logo_profissional()
        
        # --- DESENHA A TABELA DE AGENTES ---
        print(f"{Cor.BRANCO}  ♦ EQUIPE OPERACIONAL ATIVA ♦{Cor.RESET}")
        print(f"  {Cor.CINZA}┌{'─'*56}┐{Cor.RESET}")
        
        if not agentes:
            print(f"  {Cor.CINZA}│{Cor.RESET} {Cor.VERMELHO}NENHUM AGENTE REGISTRADO{' '*30}{Cor.CINZA}│{Cor.RESET}")
        else:
            # Cria linhas com 2 agentes por vez (Colunas)
            for i in range(0, len(agentes), 2):
                ag1 = agentes[i]
                ag2 = agentes[i+1] if (i+1) < len(agentes) else None
                
                # Formata o texto para ficar alinhado
                txt1 = f"[{i+1:02d}] {ag1['nome'][:10]}"
                txt2 = f"[{i+2:02d}] {ag2['nome'][:10]}" if ag2 else ""
                
                # Espaçamento mágico para alinhar a borda da direita
                espacos = 54 - len(txt1) - len(txt2)
                print(f"  {Cor.CINZA}│{Cor.RESET} {Cor.CYAN}{txt1}{Cor.RESET}{' '*espacos}{Cor.CYAN}{txt2}{Cor.RESET} {Cor.CINZA}│{Cor.RESET}")

        print(f"  {Cor.CINZA}└{'─'*56}┘{Cor.RESET}")

        # --- OPÇÕES DO SISTEMA ---
        print(f"\n{Cor.BRANCO}  COMANDOS:{Cor.RESET}")
        print(f"  {Cor.VERDE}[1]{Cor.RESET} Adicionar Agente    {Cor.AMARELO}[2]{Cor.RESET} Remover Agente")
        print(f"  {Cor.VERMELHO}[3]{Cor.RESET} Limpar Base         {Cor.CINZA}[4]{Cor.RESET} Sair do Sistema")
        
        # O BOTÃO GRANDE DE INICIAR
        print(f"\n  {Cor.VERDE_NEON}╔{'═'*20}╗")
        print(f"  ║ [ENTER] INICIAR    ║")
        print(f"  ╚{'═'*20}╝{Cor.RESET}")
        
        op = input(f"\n{Cor.AZUL_CYBER}  TERMINAL >> {Cor.RESET}").upper()
        
        # --- LÓGICA ---
        
        if op == '1': # ADICIONAR
            print(f"\n  {Cor.AMARELO}>> NOVO REGISTRO:{Cor.RESET}")
            n = input("  Nome do Agente: ")
            t = input("  Frequência whatsapp: ")
            nums = "".join(filter(str.isdigit, t))
            if not nums.startswith("55"): nums = "55" + nums
            agentes.append({"nome": n, "telefone": "+" + nums})
            with open(ARQUIVO_DADOS, 'w') as f: json.dump(agentes, f)
            print(f"  {Cor.VERDE}>> REGISTRO SALVO.{Cor.RESET}"); time.sleep(1)
            

        elif op == '2': 
            if not agentes:
                print(f"  {Cor.VERMELHO}>> ERRO: Lista vazia.{Cor.RESET}"); time.sleep(1)
                continue
            
            try:
                print(f"\n  {Cor.VERMELHO}>> PROTOCOLO DE DEMISSÃO:{Cor.RESET}")
                idx = int(input("  Digite o NÚMERO do agente para remover: ")) - 1
                
                if 0 <= idx < len(agentes):
                    removido = agentes.pop(idx) # Remove da lista
                    with open(ARQUIVO_DADOS, 'w') as f: json.dump(agentes, f) # Salva
                    print(f"  {Cor.AMARELO}>> AGENTE {removido['nome']} REMOVIDO.{Cor.RESET}")
                else:
                    print(f"  {Cor.VERMELHO}>> ID INVÁLIDO.{Cor.RESET}")
                time.sleep(1.5)
            except ValueError:
                print(f"  {Cor.VERMELHO}>> ENTRADA INVÁLIDA.{Cor.RESET}"); time.sleep(1)                

        elif op == '4': # SAIR
            print(f"  {Cor.AZUL_CYBER}>> ENCERRANDO SESSÃO...{Cor.RESET}")
            break
            
        elif op == '': # ENTER (INICIAR)
            if agentes: 
                jogar(agentes)
            else: 
                print(f"  {Cor.VERMELHO}>> ERRO: ALOCAR EQUIPE PRIMEIRO.{Cor.RESET}"); time.sleep(1)
               
# --- FUNÇÃO DE FICHA DE SUSPEITO COM RELATÓRIO LIMPO PARA whatZAP ---
def mostrar_ficha_suspeito(suspeito, index):
    limpar_tela()
    
    niveis = ["BAIXO", "MÉDIO", "ALTO", "CRÍTICO", "OBSERVAÇÃO"]
    nivel_fake = random.choice(niveis)
    
    comportamentos = [
        f"- Evita contato visual ao ser pressionado",
        f"- {suspeito['reacao_pressao']}",
        "- Apresenta microexpressões de desprezo",
        "- Mantém postura defensiva (braços cruzados)",
        "- Demonstra luto contido, mas oscila o humor",
        "- Olha frequentemente para as saídas de emergência"
    ]
    comp_selecionados = random.sample(comportamentos, 2)
    
    # --- AQUI ESTÁ A CORREÇÃO ---
    # Criamos uma variável SÓ para o texto limpo
    relatorio_limpo = ""

    # Função interna para separar: Imprime com cor, Salva sem cor
    def adicionar_linha(texto_tela, texto_zap):
        print(texto_tela) # Mostra colorido no terminal
        return texto_zap + "\n" # Guarda limpo para o zap

    # Cabeçalho
    print(f"{Cor.VERMELHO}") # Cor apenas no print solto
    print("══════════════════════════════════════════════════════════")
    print("RELATÓRIO DE SUSPEITO – CLASSIFICAÇÃO SIGILOSA")
    print("══════════════════════════════════════════════════════════")
    print(f"{Cor.RESET}")

    # Montando o texto (Observe que removemos Cor.X do segundo parâmetro)
    print("══════════════════════════════════════════════════════════")
    relatorio_limpo += " RELATÓRIO CONFIDENCIAL \n" # Título manual pro Zap
    print("══════════════════════════════════════════════════════════")
    
    relatorio_limpo += adicionar_linha(
        f"CODIGO DO SUSPEITO: {index + 1:03d}", 
        f"CODIGO DO SUSPEITO: {index + 1:03d}"
    )
    
    relatorio_limpo += adicionar_linha(
        f"NOME: {suspeito['nome']}", 
        f"NOME: {suspeito['nome']}"
    )
    
    relatorio_limpo += adicionar_linha(
        f"STATUS: {Cor.AMARELO}SOB INVESTIGAÇÃO{Cor.RESET}", 
        f"STATUS: SOB INVESTIGAÇÃO" 
    )
    
    relatorio_limpo += adicionar_linha(
        f"NÍVEL DE SUSPEITA: {nivel_fake}", 
        f"NÍVEL DE SUSPEITA: {nivel_fake}"
    )
    
    relatorio_limpo += adicionar_linha(
        f"PERSONALIDADE: {suspeito['personalidade'].upper()}", 
        f"PERSONALIDADE: {suspeito['personalidade'].upper()}"
    )

    print("-" * 58)
    relatorio_limpo += "--------------------------------\n"

    relatorio_limpo += adicionar_linha("ANÁLISE COMPORTAMENTAL:", "ANÁLISE COMPORTAMENTAL:")
    
    for c in comp_selecionados:
        relatorio_limpo += adicionar_linha(c, c)

    # Rodapé visual (só na tela)
    print(f"{Cor.VERMELHO}")
    print("══════════════════════════════════════════════════════════")
    print(f"{Cor.RESET}")
    
    return relatorio_limpo

# --- NOVO SISTEMA DE AMBIENTE DINÂMICO ---
def ambiente_terror_background():
    # Lista de sons que você precisa ter na pasta
    sons_aleatorios = ["tiro.mp3", "vidro.mp3", "grito_longe.mp3", "respiracao.mp3", "passos_correndo.mp3"]
    
    while True:
        # Espera um tempo aleatório entre 15 e 40 segundos
        tempo_espera = random.randint(15, 40)
        time.sleep(tempo_espera)
        
        # Só toca se o pygame estiver ativo
        if TEM_PYGAME:
            som_escolhido = random.choice(sons_aleatorios)
            # Toca com volume mais baixo para ser apenas "ambiente"
            efeito = media.tocar_efeito(som_escolhido)
            if efeito:
                efeito.set_volume(0.3) # 30% do volume

def preparar_suspeitos_para_jogo(lista_bruta):
    suspeitos_prontos = []
    
    for modelo in lista_bruta:
        # Cria uma cópia para não estragar o banco de dados original
        s = modelo.copy()
        
        # 1. SORTEIA O VISUAL
        # Se tiver a lista nova, sorteia. Se for o antigo (texto), mantém.
        if "visuais_possiveis" in s:
            s['visual'] = random.choice(s['visuais_possiveis'])
        
        # 2. SORTEIA O ÁLIBI + PROVA (O par correto)
        if "setup_alibi" in s:
            escolha = random.choice(s['setup_alibi'])
            s['alibi'] = escolha['onde']
            s['prova_alibi'] = escolha['prova']
            
        suspeitos_prontos.append(s)
        
    return suspeitos_prontos

def jogar(agentes):
    barra_carregamento("BAIXANDO DADOS DA INTERPOL")

    global forense_pendente, alerta_neide_ativo
    forense_pendente = None # Guarda o item achado: {'item': 'Celular', 'agente': 'Lucas'}
    alerta_neide_ativo = False # Se True, a Neide pisca no menu
    jogo_rodando = True
    
    # --- A NOVA THREAD FORENSE (ROBÔ) ---
    def rotina_forense():
        global forense_pendente, alerta_neide_ativo 
        
        while jogo_rodando:
            # AUMENTADO: Espera entre 90 e 150 segundos (1m30s a 2m30s)
            # Isso resolve a sensação de "spam" e valoriza cada item
            tempo_espera = random.randint(90, 150)
            
            for _ in range(tempo_espera):
                if not jogo_rodando: return
                time.sleep(1)
            
            if forense_pendente is None:
                #(Mais ferramentas!)
                item_achado = random.choice(SUPRIMENTOS_FORENSE)
                nome_agente = random.choice(agentes)['nome'] if agentes else "CENTRAL"
                
                forense_pendente = {'item': item_achado, 'agente': nome_agente}
                
                if TEM_PYGAME: media.tocar_efeito("forense.mp3") # Mudei o som para diferenciar da Neide
                
                
                time.sleep(30)
                if forense_pendente is not None: 
                    alerta_neide_ativo = True


    # Inicia o robô forense
    threading.Thread(target=rotina_forense, daemon=True).start()
    
    # 1. GERA OS DADOS
    detalhes = gerar_detalhes_crime()
    
   # 1. CONVERTE OS DADOS BRUTOS EM SUSPEITOS ÚNICOS PARA ESSA PARTIDA
    # Isso transforma as listas de opções em 1 opção escolhida
    todos_personagens = preparar_suspeitos_para_jogo(ARQUETIPOS_COMPLETOS)

    # 2. AGORA SORTEIA USANDO A LISTA JÁ PROCESSADA
    vitima = random.choice(todos_personagens)
    
    # Remove a vítima da lista de possíveis suspeitos
    pool = [p for p in todos_personagens if p['nome'] != vitima['nome']]
    
    # Sorteia os 5 suspeitos
    suspeitos = pool # Pega todos os 4 restantes
    
    culpado = random.choice(suspeitos)
    random.shuffle(suspeitos)
    detalhes['vitima'] = vitima['nome']
    
    inv = InvestigationManager(suspeitos, culpado)
    neide = DonaNeide(suspeitos, culpado, detalhes) # Adicionei a Neide aqui pra garantir
    
    # 2. GERA OS TEXTOS (MAS NÃO MOSTRA O DOSSIÊ AINDA)
    texto_missao = gerar_briefing_pro(detalhes)
    texto_suspeitos = gerar_dossie_suspeitos(suspeitos) # Gera, mas guarda na memória
    
    # 3. MOSTRA NA TELA APENAS A MISSÃO GERAL
    limpar_tela()
    media.tocar_ambiente("ambience.mp3")

# --- ATIVANDO A TELA DE VIGILÂNCIA ---
    
    # Liga os sons aleatórios
    threading.Thread(target=ambiente_terror_background, daemon=True).start()
    
    logo_profissional()
    
    # AQUI: Mostra só o briefing na tela preta
    painel("BRIEFING TÁTICO", texto_missao, Cor.VERMELHO_SANGUE)
    
    # Narrador lê a missão
    def narrar_missao(): audio.falar(texto_missao)
    threading.Thread(target=narrar_missao).start()
    
    # 4. ENVIA O SEGREDO PELO WHATSAPP (SEM MOSTRAR NA TELA)
    if TEM_ZAP and not MODO_OFFLINE:
        print(f"\n{Cor.AMARELO}>> TRANSFERINDO ARQUIVOS SIGILOSOS PARA OS AGENTES...{Cor.RESET}")
        
        for ag in agentes: 
            # Envia a Capa da Missão
            print(f">> Enviando Briefing para {ag['nome']}...")
            enviar_zap_turbo(ag, f"📁 NOVA MISSÃO \n\n{texto_missao}")
            time.sleep(3) 
            
            # Envia o Dossiê (O SEGREDO)
            print(f">> Enviando Lista de Suspeitos para {ag['nome']}...")
            enviar_zap_turbo(ag, f"{texto_suspeitos}")
            
            print(f"{Cor.CINZA}>> Aguardando confirmação de recebimento (5s)...{Cor.RESET}")
            time.sleep(5)

    # 5. MANTENHA A TRAVA DE SEGURANÇA
    print(f"\n{Cor.BRANCO}================================================{Cor.RESET}")
    print(f"{Cor.CINZA}(Os dados dos suspeitos foram enviados para o seu dispositivo móvel){Cor.RESET}")
    while True:
        resp = input(f"{Cor.VERDE_NEON}>> DIGITE [S] E ENTER PARA INICIAR A MISSÃO...{Cor.RESET}").upper()
        if resp == 'S': break

    print(f"{Cor.AZUL_CYBER}>> ESTABELECENDO CONEXÃO COM CÂMERAS...{Cor.RESET}")
    time.sleep(1)

    global executando_cctv
    executando_cctv = True 
    threading.Thread(target=sistema_omni_view, daemon=True).start()
    # >>>>> FIM DA COLAGEM <<<<<
    
    # --- MOVA PARA CÁ (FORA DO LOOP, ALINHADO À ESQUERDA) ---
    tentativas_restantes = 2
    rodadas_jogadas = 0
    
    
    while True:
        limpar_tela(); logo_profissional()
        
        # --- LÓGICA DA MANCHETE (Baseada em Rodadas) ---
        if rodadas_jogadas < 20:
            fase = "inicio"; cor_news = Cor.BRANCO
        elif rodadas_jogadas < 40:
            fase = "meio"; cor_news = Cor.AMARELO
        else:
            fase = "fim"; cor_news = Cor.VERMELHO_SANGUE
            
        noticia = random.choice(MANCHETES_DB[fase])
        
        # CABEÇALHO DO JORNAL
        print(f"{Cor.CINZA}╔{'═'*80}╗{Cor.RESET}")
        print(f"{Cor.CINZA}║ {Cor.VERMELHO_SANGUE}MANCHETE DO DIA: {cor_news}{noticia.center(61)} {Cor.CINZA}║{Cor.RESET}")
        print(f"{Cor.CINZA}╚{'═'*80}╝{Cor.RESET}\n")

        print(f"LOCAL: {detalhes['local']} | VÍTIMA: {vitima['nome']} | HORA DO CRIME: {detalhes['hora']}\n")
        print(f"AÇÕES REALIZADAS: {rodadas_jogadas} (Quanto mais demora, pior a imprensa fica)\n")   
        
        # --- MENU DE AÇÕES (COM NOTIFICAÇÕES) ---
        print(f"{Cor.BRANCO}MENU DE AÇÕES TÁTICAS:{Cor.RESET}")
        print("[1] 👥  Falar com Suspeitos")
        
        # Opção 2 (Câmera) - Só visual
        print("[2] 📹  Usar Câmeras")

        # --- OPÇÃO 3: EQUIPE FORENSE (DINÂMICA) ---
        if forense_pendente:
            # SE TIVER MENSAGEM: Mostra em AMARELO PISCANDO (Conceito)
            print(f"{Cor.AMARELO}[3] 📩  RECEBER RELATÓRIO FORENSE (1 PENDENTE){Cor.RESET}")
        else:
            # SE NÃO TIVER: Mostra cinza/apagado
            print(f"{Cor.CINZA}[3] ... (Aguardando Equipe de Campo){Cor.RESET}")

        # --- OPÇÃO 4: DONA NEIDE (COM ALERTA) ---
        if alerta_neide_ativo:
            print(f"{Cor.VERMELHO_SANGUE}[4] ❗  DONA NEIDE (GRITANDO NA PORTA){Cor.RESET}")
        else:
            print("[4] ☕  Visitar Dona Neide")
            
        print(f"{Cor.AZUL_CYBER}[5] ⚗️  LABORATÓRIO{Cor.RESET}")
        print(f"{Cor.VERMELHO}[6] 🚨  ACUSAR (FINAL){Cor.RESET}")
        print("[7] ❌  Sair")
        
        op = input(f"\n{Cor.VERDE_NEON}>> {Cor.RESET}")
        
        # --- OPÇÃO 1: GERENCIAR SUSPEITOS (Aqui estava o erro) ---
        if op == '1':
            print(f"\n{Cor.AMARELO}SELECIONE O SUSPEITO:{Cor.RESET}")
            for i,s in enumerate(suspeitos): 
                nvl = inv.contador_pressao[s['nome']]
                barra = "█"*nvl + "░"*(6-nvl)
                print(f"[{i+1}] {s['nome']} {Cor.CINZA}(Pressão: {barra}){Cor.RESET}")
            
            try:
                entrada = input(f"\n{Cor.VERDE}NÚMERO >> {Cor.RESET}")
                idx = int(entrada) - 1
                
                if idx < 0 or idx >= len(suspeitos): 
                    print(">> Número inválido."); time.sleep(1); continue
                
                alvo = suspeitos[idx]
                
                # SUB-MENU
                print(f"\n{Cor.BRANCO}O QUE FAZER COM {alvo['nome'].upper()}?{Cor.RESET}")
                print(f"[1] 🗣️  INICIAR INTERROGATÓRIO")
                print(f"[2] 📄  VER PERFIL TÁTICO (Vídeo + Relatório)")
                print(f"[3] 🔙  VOLTAR")
                
                acao = input(f"\n{Cor.VERMELHO}ORDEM >> {Cor.RESET}")
                
                if acao == '1':
                    # --- INTERROGATÓRIO (MODO TRAVADO) ---
                    txt, nerv, nivel = inv.pressionar_suspeito(idx)
                    digitar(">> REGISTRANDO DEPOIMENTO...", velocidade=0.01)
                    painel("SALA DE INTERROGATÓRIO", txt, Cor.VERDE)
                    
                    # 1. Toca o áudio
                    def narrar(): audio.falar(txt)
                    threading.Thread(target=narrar).start()
                    
                    # 2. Som de tensão se estiver nervoso
                    if nerv: media.tocar_efeito("coracao.mp3", True)

                    # 3. LOOP DE ESPERA (A tela não fecha sozinha!)
                    # 3. LOOP DE INTERROGATÓRIO (COM EVIDÊNCIAS)
                    while True:
                        print(f"\n{Cor.BRANCO}TÁTICAS DISPONÍVEIS:{Cor.RESET}")
                        print(f"[S] Encerrar Depoimento")
                        
                        if nivel >= 2: # Álibi aparece no nível 2
                            print(f"{Cor.CYAN}[A] VERIFICAR ÁLIBI{Cor.RESET}")
                        
                        # AQUI ESTÁ A OPÇÃO DOS ITENS
                        print(f"{Cor.AMARELO}[E] CONFRONTAR COM EVIDÊNCIA (INVENTÁRIO){Cor.RESET}")
                        
                        op_int = input(f"\n{Cor.VERDE_NEON}>> TÁTICA: {Cor.RESET}").upper()

                        if op_int == 'S':
                            # Garante que o coração parou (caso tenha sobrado) e restaura o clima
                            media.parar_tudo() 
                            media.tocar_ambiente("login.mp3") 
                            break
                        
                        elif op_int == 'A' and nivel >= 2:
                            texto_prova = inv.get_prova_alibi(idx)
                            painel("EVIDÊNCIA DE ÁLIBI", texto_prova, Cor.CYAN)
                            audio.falar(texto_prova)
                            input(">> Enter para voltar")

                        elif op_int == 'E':
                            if not inv.inventario:
                                print(f"\n{Cor.VERMELHO}>> VOCÊ NÃO TEM ITENS! USE O DRONE (OPÇÃO 3).{Cor.RESET}")
                                time.sleep(2)
                            else:
                                print(f"\n{Cor.AMARELO}QUAL ITEM USAR?{Cor.RESET}")
                                for i, item in enumerate(inv.inventario):
                                    print(f"[{i+1}] {item}")
                                
                                try:
                                    esc_item = int(input(">> NÚMERO DO ITEM: ")) - 1
                                    if 0 <= esc_item < len(inv.inventario):
                                        item_selecionado = inv.inventario[esc_item]
                                        
                                        # Chama a função de reação
                                        reacao, ficou_nervoso = inv.confrontar_com_evidencia(idx, item_selecionado, detalhes)
                                        
                                        # 1. MOSTRA A REAÇÃO
                                        painel("REAÇÃO DO SUSPEITO", reacao, Cor.VERMELHO_SANGUE)
                                        
                                        # 2. PREPARA O ÁUDIO (ISSO É O IMPORTANTE)
                                        som_cardiaco = None
                                        
                                        # Toca a voz
                                        audio.falar(reacao.replace('"', ''))
                                        
                                        # Se ficou nervoso, liga o coração e GUARDA na variável
                                        if ficou_nervoso:
                                            som_cardiaco = media.tocar_efeito("coracao.mp3", loop=True)
                                        
                                        # 3. TRAVA O JOGO AQUI
                                        input(f"\n{Cor.AMARELO}>> Pressione Enter para acalmar o suspeito...{Cor.RESET}")
                                        
                                        # 4. MATAR O SOM DO CORAÇÃO (BRUTALMENTE)
                                        if som_cardiaco:
                                            som_cardiaco.stop()
                                        
                                        # Garante que nenhum efeito sobrou
                                        media.parar_tudo() 
                                        # Volta a música de fundo
                                        media.tocar_ambiente("login.mp3") 
                                        
                                    else:
                                        print("Item inválido.")
                                except ValueError:
                                    print("Digite um número.")
                        
                        elif op_int == 'A' and nivel == 2:
                            # Mostra a prova sem sair da tela
                            texto_prova = inv.get_prova_alibi(idx)
                            painel("EVIDÊNCIA DE ÁLIBI", texto_prova, Cor.CYAN)
                            audio.falar(texto_prova)
                            print(">> Pressione Enter para voltar ao depoimento...")
                            input()
                            # Redesenha o depoimento para não perder o contexto
                            painel("SALA DE INTERROGATÓRIO", "(Continuação do depoimento...)", Cor.VERDE)

                    # --- AQUI É O LUGAR CERTO DO ÁLIBI ---
                elif acao == '2':
                    # --- RELATÓRIO + VÍDEO ---
                   # --- RELATÓRIO + VÍDEO (CORRIGIDO) ---
                    nome_video_arquivo = alvo.get('video', 'padrao.mp4')
                    # Junta o caminho da pasta + o nome do arquivo
                    caminho_completo_video = os.path.join(PASTA_VIDEO, nome_video_arquivo)
                    
                    print(f"{Cor.AZUL_CYBER}>> CARREGANDO PERFIL VISUAL...{Cor.RESET}")
                    
                    # Passa o caminho completo agora
                    media.tocar_video_hacker(caminho_completo_video, "suspense.mp3")
                    
                    # Agora essa variável recebe o texto (graças à correção 1)
                    texto_relatorio = mostrar_ficha_suspeito(alvo, idx)
                    
                    # --- ADICIONE ISSO PARA O LOCUTOR LER O RELATÓRIO ---
                    def narrar_relatorio(): 
                        # Limpa caracteres especiais visuais antes de ler
                        txt_limpo = texto_relatorio.replace("═", "").replace("-", "")
                        audio.falar(txt_limpo)
                    
                    threading.Thread(target=narrar_relatorio).start()
                    # ----------------------------------------------------
                    
                    print(f"\n{Cor.AMARELO}>> TRANSMITINDO DADOS...{Cor.RESET}")
                    if TEM_ZAP and not MODO_OFFLINE:
                         # ... resto do envio do zap ...
                        for agente in agentes:
                            enviar_zap_turbo(agente, f"📄 *PERFIL: {alvo['nome']}*\n\n{texto_relatorio}")
                    
                    if nerv: media.tocar_efeito("coracao.mp3", True)
                    
                    # --- CORREÇÃO: TRAVA DE SEGURANÇA ---
                    print(f"\n{Cor.BRANCO}========================================{Cor.RESET}")
                    while True:
                        saida = input(f"{Cor.VERDE_NEON}>> DIGITE [S] E ENTER PARA SAIR DO DEPOIMENTO: {Cor.RESET}").upper()
                        if saida == 'S':
                            break
                    # ------------------------------------
                    
                    media.parar_ambiente(); media.tocar_ambiente("login.mp3")

            except ValueError:
                print(f"{Cor.VERMELHO}>> Digite apenas números.{Cor.RESET}"); time.sleep(1)
            except Exception as e:
                print(f"{Cor.VERMELHO}>> ERRO: {e}{Cor.RESET}"); time.sleep(2)

        # --- OUTRAS OPÇÕES ---
        if op == '2':
            barra_carregamento("HACKEANDO SERVIDOR DE VÍDEO")
            suspeito_cam = random.choice(suspeitos)
            acoes = ["discutindo com a vítima", "entregando um pacote suspeito", "saindo irritado da sala"]
            # Usa o horário NOVO calculado na etapa 1
            pista = f"[{detalhes['hora_camera']}] A câmera pegou {suspeito_cam['nome']} {random.choice(acoes)}."
            painel("CFTV - REGISTRO ANTERIOR AO CRIME", pista, Cor.AZUL_CYBER)
            audio.falar(pista)
            input("[ENTER]")

        # [OPÇÃO 3: CAIXA DE ENTRADA]
        # [OPÇÃO 3: CAIXA DE ENTRADA (FORENSE) - CORRIGIDA]
        elif op == '3':
            if forense_pendente:
                print(f"\n{Cor.AZUL_CYBER}>> ESTABELECENDO LINK COM AGENTE DE CAMPO...{Cor.RESET}")
                time.sleep(1)
                
                item = forense_pendente['item']
                agente = forense_pendente['agente']
                msg = f"AGENTE {agente}: 'Chefe, solicitei esse equipamento do estoque: {item}.'"
                
                painel("SUPRIMENTO TÁTICO", msg, Cor.VERDE_NEON)
                audio.falar(msg) 
                
                inv.adicionar_item(item)
                
                forense_pendente = None
                # REMOVIDO: alerta_neide_ativo = False 
                # ^ Agora a Neide continua gritando se você não for lá ver ela!
                
                print(f"\n{Cor.BRANCO}O ITEM JÁ ESTÁ NA SUA MOCHILA. O QUE DESEJA FAZER?{Cor.RESET}")
                print(f"[1] ⚗️  IR PARA O LABORATÓRIO")
                print(f"[2] 👮  VOLTAR PARA A PATRULHA")
                
                decisao = input(f"\n{Cor.VERDE_NEON}>> DECISÃO: {Cor.RESET}")
                
                if decisao == '1':
                    barra_carregamento("ABRINDO BANCADA")
                    msg_lab, sucesso = inv.combinar_itens()
                    painel("RESULTADO", msg_lab, Cor.AMARELO)
                    audio.falar(msg_lab)
                    input("[ENTER]")
                else:
                    print(f"{Cor.CINZA}>> Item guardado.{Cor.RESET}")
                    time.sleep(1)
                
            else:
                print(f"\n{Cor.CINZA}>> SEM NOVOS RELATÓRIOS.{Cor.RESET}")
                time.sleep(1)
            
            rodadas_jogadas += 1

        # [OPÇÃO 4: DONA NEIDE (COM INSISTÊNCIA)]
        elif op == '4':
            media.tocar_efeito("campainha.mp3")
            
            # Lógica: Se o alerta estiver ativo, ela entrega o item secreto direto
            # Se não, ela só fofoca até você insistir (perguntar 2x)
            
            # Vamos simplificar: Se tiver alerta, ela dá o item EXTRA (Senha)
            if alerta_neide_ativo:
                fofoca_urgente = "MENINO! ATÉ QUE ENFIM! Aquele policial deixou cair esse 'Papel com Senha' na minha planta!"
                painel("DONA NEIDE (URGENTE)", fofoca_urgente, Cor.VERMELHO)
                audio.falar(fofoca_urgente)
                inv.adicionar_item("Papel com Senha")
                alerta_neide_ativo = False # Desliga o alerta
            else:
                # Rotina normal (Fofoca)
                fofoca, item = neide.fofocar()
                painel("DONA NEIDE", fofoca, Cor.ROXO)
                audio.falar(fofoca)
                if item: inv.adicionar_item(item)
            
            input("[ENTER]")
            rodadas_jogadas += 1
            

       # --- OPÇÃO 5: LABORATÓRIO E COMUNICAÇÃO (CORRIGIDO) ---
        # --- OPÇÃO 5: LABORATÓRIO E COMUNICAÇÃO (ATUALIZADO) ---
        # --- OPÇÃO 5: LABORATÓRIO E COMUNICAÇÃO ---
        elif op == '5':
            print(f"\n{Cor.AZUL_CYBER}>> ACESSANDO BANCADA DE LABORATÓRIO...{Cor.RESET}")
            
            print(f"\n{Cor.BRANCO}O QUE DESEJA FAZER?{Cor.RESET}")
            print(f"[1] 🎒  VER MOCHILA (INVENTÁRIO)")
            print(f"[2] ⚗️  COMBINAR ITENS (CRAFTING)")
            print(f"[3] 📲  ENVIAR RELATÓRIO (ZAP)")
            print(f"[4] 🔙  VOLTAR")
            
            sub_op = input(f"\n{Cor.VERDE_NEON}>> ESCOLHA: {Cor.RESET}")

            if sub_op == '1':
                painel("INVENTÁRIO ATUAL", "Verificando itens...", Cor.CYAN)
                if not inv.inventario:
                    print(f"{Cor.VERMELHO}>> A MOCHILA ESTÁ VAZIA.{Cor.RESET}")
                else:
                    print(f"{Cor.AMARELO}ITENS NA BANCADA:{Cor.RESET}")
                    for i, item in enumerate(inv.inventario):
                        print(f"  [{i+1}] 📦 {item}")
                input(f"\n>> Enter para voltar...")

            elif sub_op == '2':
                barra_carregamento("INICIANDO SISTEMA DE ANÁLISE")
                msg, sucesso = inv.combinar_itens() # Chama a função corrigida
                
                cor_msg = Cor.VERDE_NEON if sucesso else Cor.AMARELO
                painel("RELATÓRIO DE ANÁLISE", msg, cor_msg)
                
                if sucesso:
                    media.tocar_efeito("acertopoints.mp3")
                    audio.falar("Sucesso. Nova evidência gerada.")
                else:
                    media.tocar_efeito("falha1.mp3")
                    audio.falar(msg)
                
                input("[ENTER]")
                rodadas_jogadas += 1 

            # --- C. ENVIAR ZAP ---
            elif sub_op == '3':
                if not TEM_ZAP or MODO_OFFLINE:
                    print(f"\n{Cor.VERMELHO}>> ERRO: SISTEMA DE COMUNICAÇÃO OFFLINE.{Cor.RESET}")
                    time.sleep(2)
                else:
                    print(f"\n{Cor.AMARELO}>> SELECIONE O DESTINATÁRIO:{Cor.RESET}")
                    print("[0] 📢 ENVIAR PARA TODOS")
                    for i, ag in enumerate(agentes):
                        print(f"[{i+1}] 👤 {ag['nome']}")
                    
                    try:
                        dest = int(input(f"\n{Cor.VERDE}>> NÚMERO: {Cor.RESET}"))
                        txt_zap = "📦 *RELATÓRIO DE EVIDÊNCIAS COLETADAS:*\n\n"
                        if not inv.inventario:
                            txt_zap += "(Mochila Vazia)"
                        else:
                            for item in inv.inventario:
                                txt_zap += f"✅ {item}\n"
                        txt_zap += "\n_Solicito análise imediata._"

                        if dest == 0:
                            for ag in agentes: enviar_zap_turbo(ag, txt_zap)
                        elif 0 < dest <= len(agentes):
                            enviar_zap_turbo(agentes[dest-1], txt_zap)  
                    except ValueError: pass
                    rodadas_jogadas += 1
            
            # Se for 3, ele só sai e volta pro menu principal

        elif op == '6':
            # --- ACUSAÇÃO FINAL (SISTEMA DE VIDAS + REVELAÇÃO) ---
            digitar(f"{Cor.VERMELHO}>> INICIANDO PROTOCOLO FINAL...{Cor.RESET}")
            media.parar_ambiente()
            
            print(f"{Cor.AMARELO}>> EXECUTANDO VÍDEO...{Cor.RESET}")           
            caminho_hack = os.path.join(PASTA_VIDEO, "hack.mp4")
            media.tocar_video_hacker(caminho_hack)
            
            print(f"\n{Cor.BRANCO}========================================{Cor.RESET}")
            input(f"{Cor.VERMELHO_SANGUE}>> PRESSIONE [ENTER] PARA ACUSAR...{Cor.RESET}")
            
            limpar_tela(); logo_profissional()
            media.tocar_efeito("alarme.mp3", loop=True)
            
            print(f"\n{Cor.VERMELHO_SANGUE}>> SISTEMA COMPROMETIDO <<{Cor.RESET}")
            
            try:
                # FASE 1: ASSASSINO
                lista = [f"[{i+1}] {s['nome']}" for i,s in enumerate(suspeitos)]
                painel(f"PASSO 1/2: QUEM É O ASSASSINO? (CHANCES: {tentativas_restantes})", lista, Cor.VERMELHO)
                
                # VOZ EM THREAD
                def narrar_acusacao(): audio.falar("Identifique o assassino e a arma.")
                threading.Thread(target=narrar_acusacao).start()

                esc_susp = int(input(f"{Cor.VERMELHO}NÚMERO DO CULPADO >> {Cor.RESET}")) - 1
                
                # FASE 2: ARMA
                todas_armas = [c['arma'] for c in CRIMES_DB]
                # DICA: Não vamos embaralhar as armas aqui para facilitar a leitura se o jogador decorar a ordem
                # Mas se quiser embaralhar, descomente a linha abaixo:
                # random.shuffle(todas_armas)
                
                limpar_tela(); logo_profissional()
                painel("PASSO 2/2: QUAL FOI A ARMA?", [f"[{i+1}] {a}" for i,a in enumerate(todas_armas)], Cor.VERMELHO)
                
                esc_arma_idx = int(input(f"{Cor.VERMELHO}NÚMERO DA ARMA >> {Cor.RESET}")) - 1
                arma_escolhida = todas_armas[esc_arma_idx]

                media.parar_ambiente() 
                barra_carregamento("PROCESSANDO SENTENÇA")

                # VERIFICAÇÃO
                acertos = 0
                if suspeitos[esc_susp] == culpado: acertos += 1
                if arma_escolhida == detalhes['arma_real']: acertos += 1
                
                # --- CENÁRIO 1: VITÓRIA ---
                if acertos == 2:
                    media.tocar_efeito("win.mp3")
                    painel("SUCESSO", "CULPADO PRESO E ARMA RECUPERADA.", Cor.VERDE_NEON)
                    audio.falar("Excelente trabalho, Agente. Caso encerrado.")
                    break 
                
              # --- CENÁRIO 2: ERRO (MAS TEM SEGUNDA CHANCE) ---
                else:
                    tentativas_restantes -= 1 
                    
                    # 1. MATA A SIRENE NA HORA (IMPORTANTE!)
                    media.parar_tudo() 
                    
                    if tentativas_restantes > 0:
                        media.tocar_efeito("fail.mp3") 
                        msg = [
                            f"Sua teoria tem furos.",
                            f"O promotor rejeitou a acusação.",
                            f"VOCÊ TEM MAIS {tentativas_restantes} CHANCE."
                        ]
                        painel("DEDUÇÃO INCORRETA", msg, Cor.AMARELO)
                        audio.falar("Você errou. O promotor te deu mais uma chance.")
                        
                        input(">> Pressione Enter para voltar e investigar mais...")
                        
                        # 2. RELIGA A MÚSICA DE FUNDO
                        media.tocar_ambiente("login.mp3") 
                    
                    # --- CENÁRIO 3: GAME OVER ---
                    else:
                        media.tocar_efeito("fail.mp3")
                        # ... (o resto do código de Game Over continua igual)
                        
                        # AQUI ESTÁ A REVELAÇÃO
                        revelacao = [
                            f"O CULPADO ERA: {culpado['nome'].upper()}",
                            f"A ARMA ERA: {detalhes['arma_real'].upper()}",
                            f"MOTIVAÇÃO: {culpado['luto']}"
                        ]
                        
                        painel("CASO ARQUIVADO (FRACASSO)", revelacao, Cor.VERMELHO_SANGUE)
                        
                        txt_final = f"Você falhou. O culpado era {culpado['nome']} e usou {detalhes['arma_real']}."
                        audio.falar(txt_final)
                        
                        print(f"\n{Cor.CINZA}>> O assassino fugiu do país.{Cor.RESET}")
                        break

            except Exception as e:
                media.parar_ambiente(); media.tocar_ambiente("ambience.mp3")
                print(f"{Cor.VERMELHO}>> ERRO DE ENTRADA: {e}{Cor.RESET}"); time.sleep(2)
            # --- ACUSAÇÃO FINAL (Versão Corrigida) ---
           

        elif op == '7': break

if __name__ == "__main__":
    menu()
    