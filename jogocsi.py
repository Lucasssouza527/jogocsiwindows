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


ARQUETIPOS_COMPLETOS = [
  {
    "nome": "O Chef",
    "video": "chef.mp4",
    "visuais_possiveis": [
        "dólmã branco manchado",
        "avental preto e bandana",
        "uniforme de cozinha azul",
        "camiseta branca suja de molho"
    ],
    "personalidade": "orgulhoso e estressado",
    "relacao_com_vitima": "responsável pelas refeições",
    "setup_alibi": [
        {"onde": "na cozinha com a equipe", "prova": "Dois assistentes confirmam que ele estava gritando com eles."},
        {"onde": "no estoque contando vinhos", "prova": "A planilha de estoque foi atualizada naquele horário."},
        {"onde": "fumando nos fundos", "prova": "A câmera do beco gravou ele saindo para fumar."}
    ],
    "luto": "Perdi o apetite desde então.",
    "reacao_pressao": "fica agressivo se questionado"
  },

  {
    "nome": "O Hacker",
    "video": "hacker.mp4",
    "visuais_possiveis": [
        "moletom com capuz e máscara",
        "camiseta de anime e óculos",
        "roupa toda preta e luvas sem dedos",
        "casaco cinza e fones de ouvido"
    ],
    "personalidade": "irônico e desconfiado",
    "relacao_com_vitima": "prestador de serviços digitais",
    "setup_alibi": [
        {"onde": "online a noite inteira", "prova": "Logs da Twitch mostram ele em live stream."},
        {"onde": "dormindo na sala de servidores", "prova": "O sensor de movimento não detectou saída."},
        {"onde": "realizando manutenção remota", "prova": "Logs SSH mostram acesso contínuo ao sistema."}
    ],
    "luto": "Isso saiu totalmente do controle.",
    "reacao_pressao": "desvia com sarcasmo"
  },

  {
    "nome": "O Guarda-Costas",
    "video": "guarda_costas.mp4",
    "visuais_possiveis": [
        "terno preto e óculos escuros",
        "jaqueta tática e rádio no ombro",
        "capa de chuva escura e luvas",
        "camisa justa e coldre discreto"
    ],
    "personalidade": "reservado e profissional",
    "relacao_com_vitima": "proteção pessoal diária",
    "setup_alibi": [
        {"onde": "na ronda externa", "prova": "Registro eletrônico marca os checkpoints."},
        {"onde": "monitorando câmeras", "prova": "Login ativo na central de segurança."},
        {"onde": "revistando veículos", "prova": "Portão registra abertura manual naquele horário."}
    ],
    "luto": "Falhei no meu dever.",
    "reacao_pressao": "responde curto e evita detalhes"
  },

  {
    "nome": "A Viúva",
    "video": "viuva.mp4",
    "visuais_possiveis": [
        "vestido preto longo e véu",
        "roupão escuro e olhos inchados",
        "vestido sóbrio e joias discretas",
        "pijama de seda e lenço"
    ],
    "personalidade": "emocionalmente instável",
    "relacao_com_vitima": "casamento conturbado",
    "setup_alibi": [
        {"onde": "sozinha no quarto", "prova": "Histórico da Alexa tocando músicas tristes."},
        {"onde": "tomando banho", "prova": "O vapor ainda estava no espelho."},
        {"onde": "ligando para uma amiga", "prova": "Registro de chamada longa no celular."}
    ],
    "luto": "Nada disso faz sentido sem ele.",
    "reacao_pressao": "chora e se fecha"
  },

  {
    "nome": "O Mordomo",
    "video": "mordomo.mp4",
    "visuais_possiveis": [
        "uniforme clássico com luvas brancas",
        "colete preto e camisa engomada",
        "avental discreto e mangas dobradas",
        "paletó antigo e gravata borboleta"
    ],
    "personalidade": "discreto e observador",
    "relacao_com_vitima": "serviço de longa data",
    "setup_alibi": [
        {"onde": "preparando o jantar", "prova": "Câmera mostra ele na cozinha o tempo todo."},
        {"onde": "polindo a prataria", "prova": "Talheres ainda estavam quentes do polimento."},
        {"onde": "organizando a adega", "prova": "Garrafa aberta no horário do crime."}
    ],
    "luto": "Servi esta casa por décadas.",
    "reacao_pressao": "educado, mas evasivo"
  },

  {
    "nome": "O Médico",
    "video": "medico.mp4",
    "visuais_possiveis": [
        "jaleco branco e estetoscópio",
        "terno simples e pasta médica",
        "camisa clara e mangas arregaçadas",
        "roupa social com luvas descartáveis"
    ],
    "personalidade": "frio e analítico",
    "relacao_com_vitima": "acompanhamento clínico",
    "setup_alibi": [
        {"onde": "em ligação de emergência", "prova": "Registro da central médica."},
        {"onde": "examinando exames", "prova": "Arquivos abertos no computador."},
        {"onde": "descansando no consultório", "prova": "Câmera interna ativa."}
    ],
    "luto": "Era apenas mais um paciente.",
    "reacao_pressao": "responde tecnicamente"
  },

  {
    "nome": "O Advogado",
    "video": "advogado.mp4",
    "visuais_possiveis": [
        "terno caro e pasta de couro",
        "camisa social sem gravata",
        "paletó jogado no braço",
        "óculos finos e relógio discreto"
    ],
    "personalidade": "articulado e defensivo",
    "relacao_com_vitima": "assuntos jurídicos sensíveis",
    "setup_alibi": [
        {"onde": "em chamada confidencial", "prova": "Registro criptografado no celular."},
        {"onde": "redigindo documentos", "prova": "Arquivo salvo minutos antes do crime."},
        {"onde": "fumando na varanda", "prova": "Bituca encontrada no local."}
    ],
    "luto": "Isso complica muitas coisas.",
    "reacao_pressao": "escolhe cada palavra"
  }
]


# Dados Complementares para evitar erros
LOCAIS_EXPANDIDOS = ["Apartamento de Luxo", "Beco Escuro", "Sala de Servidores", "Estacionamento Subsolo", "Mansão na Serra", "Laboratório,quarto andar", "Cobertura Panorâmica", "Clube Noturno", "Escritório Corporativo", "Parque Abandonado, Centro da Cidade", "Restaurante Chique", "Hotel 5 Estrelas", "Bar da Esquina", "Galeria de Arte", "Cinema Privado"]

TESTEMUNHAS_INICIAIS = ["o entregador", "uma vizinha", "o zelador", "um corredor", "a faxineira", "um segurança", "o porteiro", "um turista perdido", "a garçonete", "um ciclista", "o motorista de táxi", "um pedestre apressado", "a criança brincando", "o jardineiro", "o vendedor ambulante", "a fotógrafa", "o policial de ronda", "o morador local"]


POSICOES_CORPO = ["caído de bruços", "sentado na poltrona", "estirado no chão", "escondido no armário", "encostado na parede", "deitado na cama", "ajoelhado no tapete", "em pé, encostado na mesa", "caído na escada", "dentro do carro", "no banheiro", "na varanda", "no porão", "na cozinha", "no jardim", "na garagem"]    

# ---  BANCO DE PISTAS IRRELEVANTES  ---
PISTAS_IRRELEVANTES = itens_encontrados = [
    "Marcas de lama","Café morno","Janela aberta",
    "Papel amassado","Chave de fenda","Garrafas vazias",
    "Roupas molhadas","Cartão de visita rasgado","Fios soltos",
    "Pegadas de sapato comum","Bilhete anônimo","Cigarro apagado",
    "Caneta sem tinta","Óculos de sol","Chapéu esquecido",

    "Embalagem de fast-food","Relógio parado","Jornal velho",
    "Guardanapo sujo",

    "Celular Bloqueado","Senha Anotada","Cofre Pequeno",
    "Chave Enferrujada","Copo com Saliva","Kit de Coleta de DNA",

    "HD Criptografado","Pen-drive 'CONFIDENCIAL'","Pendrive Oculto",
    "Notebook","Central de Câmeras","Cartão de Acesso",

    "Prontuário Rasgado","Lupa","Contrato Rasgado",
    "Fita Adesiva","Carta Queimada","Luz Ultravioleta",
    "Envelope Lacrado","Carta de Advogado","Gravação de Voz",
    "Software de Áudio","Agenda Codificada","Tabela de Símbolos"
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

        # PLOT TWISTS MAIS COMPLEXOS
        self.segredos = {
                        "financeiro": "A Vítima lavava dinheiro para a Máfia Russa.",
                        "pessoal": "Amanhã vou até a empresa e vou demitir 3 funcionários por justa causa.",
                        "genetico": "O teste de DNA provou que a Vítima já estava morta há 2 dias (sósia?).",
                        "digital": "A Vítima era, na verdade, um espião da ABIN infiltrado.",
                        "medico": "O prontuário indica uma doença terminal escondida da família.",
                        "juridico": "Um processo milionário estava prestes a ser revelado.",
                        "emocional": "A Vítima mantinha um relacionamento secreto dentro da mansão.",
                        "chantagem": "A Vítima estava sendo chantageada por fotos comprometedoras.",
                        "seguranca": "O sistema de câmeras foi desligado manualmente por alguém autorizado.",
                        "testamento": "O testamento foi alterado 24 horas antes da morte.",
                        "funcionarios": "Um funcionário descobriu algo e exigiu dinheiro para ficar calado.",
                        "mafioso": "A Vítima devia uma grande quantia a um grupo criminoso local."
                    }

    def combinar_itens(self):
        # 1. O LIVRO DE RECEITAS (DICIONÁRIO)
        # Estrutura: { ("Item 1", "Item 2") : "Resultado Final" }
        receitas = {
        ("Celular Bloqueado", "Senha Anotada"):
            f"Celular Desbloqueado (SMS: '{self.segredos['pessoal']}')",

        ("Cofre Pequeno", "Chave Enferrujada"):
            f"Livro Caixa (REGISTRO: '{self.segredos['financeiro']}')",

        ("Copo com Saliva", "Kit de Coleta de DNA"):
            f"Laudo Laboratorial (RESULTADO: '{self.segredos['genetico']}')",

        ("HD Criptografado", "Pen-drive 'CONFIDENCIAL'"):
            f"Arquivos Descriptografados (ALERTA: '{self.segredos['digital']}')",

        ("Prontuário Rasgado", "Lupa"):
            f"Relatório Médico Completo (SEGREDO: '{self.segredos['medico']}')",

        ("Contrato Rasgado", "Fita Adesiva"):
            f"Documento Reconstruído (PROCESSO: '{self.segredos['juridico']}')",

        ("Carta Queimada", "Luz Ultravioleta"):
            f"Mensagem Oculta (CONFISSÃO: '{self.segredos['emocional']}')",

        ("Pendrive Oculto", "Notebook"):
            f"Fotos Recuperadas (CHANTAGEM: '{self.segredos['chantagem']}')",

        ("Central de Câmeras", "Cartão de Acesso"):
            f"Log de Segurança (FALHA: '{self.segredos['seguranca']}')",

        ("Envelope Lacrado", "Carta de Advogado"):
            f"Testamento Revelado (HERANÇA: '{self.segredos['testamento']}')",

        ("Gravação de Voz", "Software de Áudio"):
            f"Áudio Limpo (AMEAÇA: '{self.segredos['funcionarios']}')",

        ("Agenda Codificada", "Tabela de Símbolos"):
            f"Anotações Decifradas (DÍVIDA: '{self.segredos['mafioso']}')"
    }
        
        # 2. MOSTRAR A LISTA PARA O JOGADOR
        if len(self.inventario) < 2:
            return "ERRO: Você precisa de pelo menos 2 itens no inventário.", False
            
        print("\nSELECIONE DOIS ITENS PARA COMBINAR:")
        for i, item in enumerate(self.inventario):
            print(f"[{i+1}] {item}")
        
        # 3. O JOGADOR ESCOLHE (INPUT MANUAL)
        try:
            print("\n--------------------------------")
            escolha1 = int(input("Digite o número do 1º item: ")) - 1
            escolha2 = int(input("Digite o número do 2º item: ")) - 1
            print("--------------------------------")

            # Verifica se os números existem na mochila
            if escolha1 < 0 or escolha1 >= len(self.inventario) or \
               escolha2 < 0 or escolha2 >= len(self.inventario) or \
               escolha1 == escolha2:
                return "ERRO: Escolha inválida ou itens iguais.", False
            
            # Pega os nomes dos itens baseados nos números
            item_A = self.inventario[escolha1]
            item_B = self.inventario[escolha2]
            
            print(f"TESTANDO: {item_A} + {item_B}...")
            time.sleep(1) # Charme de processamento

            # 4. A VERIFICAÇÃO (A LÓGICA MÁGICA)
            novo_item = None
            
            # Varre todas as receitas para ver se o par existe
            for (ingrediente1, ingrediente2), resultado in receitas.items():
                # Verifica a ordem normal (A + B) OU a ordem invertida (B + A)
                if (item_A == ingrediente1 and item_B == ingrediente2) or \
                   (item_A == ingrediente2 and item_B == ingrediente1):
                    novo_item = resultado
                    break # Achou! Para de procurar.

            # 5. RESULTADO
            if novo_item:
                # Remove os itens velhos
                # Dica: Remover o maior index primeiro para não bagunçar a lista
                if escolha1 > escolha2:
                    self.inventario.pop(escolha1)
                    self.inventario.pop(escolha2)
                else:
                    self.inventario.pop(escolha2)
                    self.inventario.pop(escolha1)
                
                # Adiciona o novo
                self.inventario.append(novo_item)
                return f"SUCESSO! A combinação gerou:\n>> {novo_item}", True
            else:
                return "FALHA: Esses itens não reagem entre si.", False

        except ValueError:
            return "ERRO: Digite apenas números.", False


    def adicionar_item(self, item):
        if item not in self.inventario:
            self.inventario.append(item)
            return True
        return False

    def pressionar_suspeito(self, idx):
        alvo = self.suspeitos[idx]
        nome = alvo['nome']
        
        self.contador_pressao[nome] += 1
        pressao = self.contador_pressao[nome]
        nervoso = False
        
        # --- NOVIDADE 1: ESCOLHER UM BODE EXPIATÓRIO (ALGUÉM PRA CULPAR) ---
        # Escolhe outro suspeito da lista que não seja ele mesmo
        outros = [s for s in self.suspeitos if s != alvo]
        inimigo = random.choice(outros)['nome'] if outros else "ninguém"

        if pressao == 1: 
            status = "COOPERATIVO (LUTO)"
            fala = f"({alvo['personalidade']}) \"{alvo['luto']}\""
        
        elif pressao == 2: 
            status = "DEFENSIVO (ÁLIBI)"
            fala = f"Eu não tenho nada a ver com isso. Eu estava {alvo['alibi']}."
        
        elif pressao == 3: 
            status = "DESVIANDO O FOCO" # <-- AQUI ELE DEDURA ALGUÉM
            # Se for fofoqueiro ou arrogante, culpa os outros
            if "fofoqueira" in alvo['personalidade'] or "arrogante" in alvo['personalidade']:
                fala = f"Por que está me apertando? O {inimigo} tinha muito mais motivos que eu!"
            else:
                fala = f"Minha relação era {alvo['relacao_com_vitima']}, mas o {inimigo} odiava a vítima!"
        
        elif pressao == 4: 
            status = "HOSTIL"
            fala = f"[{alvo['reacao_pressao'].upper()}] Já chega! Vocês deviam investigar o {inimigo}, não eu!"
        
        elif pressao == 5: 
            status = "PÂNICO (LIMITE)"
            nervoso = True
            fala = "MINHA CABEÇA VAI EXPLODIR! PAREM DE ME PRESSIONAR!"
            
        else: 
            status = "COLAPSO NERVOSO"
            nervoso = True
            if alvo == self.culpado: 
                fala = f"TÁ BOM! FUI EU! Eu vi alguém de {self.culpado['visual']}... Não, espera... EU NÃO TIVE ESCOLHA!"
            else: 
                fala = f"NÃO FUI EU! Pelo amor de Deus! Eu vi alguém vestindo {self.culpado['visual']} fugindo!"

        return f"Depoimento: {nome}\nStatus:\n---\n\"{fala}\"", nervoso, pressao

    def get_prova_alibi(self, idx):
        alvo = self.suspeitos[idx]
        
        # --- NOVIDADE 2: O ÁLIBI FALSO DO ASSASSINO ---
        if alvo == self.culpado:
            # O assassino tem uma prova forjada "perfeita"
            return (f"DOCUMENTO: {alvo['prova_alibi']}\n"
                    f"[ANÁLISE]: O documento parece autêntico, mas a hora foi alterada manualmente.\n"
                    f"(DICA: Pressione Dona Neide para confirmar se ele realmente estava lá.)"
                    f"(Sugestão: Verifique as câmeras de segurança para inconsistências.)")
                    
        else:
            # Inocentes têm provas normais ou falhas honestas
            return f"DOCUMENTO: {alvo['prova_alibi']}\n[ANÁLISE]: A prova confirma a versão do suspeito."

    def pegar_pista_camera(self):
        # Pega o visual real
        vis = self.culpado['visual'].lower()
        
        # Divide para pegar detalhes isolados
        if ' e ' in vis:
            detalhes = vis.split(' e ')
            item_chave = random.choice(detalhes) # Ex: "óculos escuros"
        else:
            # Se for "dólmã branco manchado", pega "branco" ou "manchado"
            palavras = vis.split()
            item_chave = random.choice(palavras[1:]) if len(palavras) > 1 else vis

        # FRASES QUE GERAM DÚVIDA
        frases_confusas = [
            f"Imagem granulada. Vulto detectado usando {item_chave}.",
            f"O sistema de IA identificou um objeto: {item_chave}.",
            f"Interferência na gravação. É possível ver apenas {item_chave}.",
            f"O suspeito cobriu o rosto, mas a câmera pegou {item_chave}.",
            f"Análise de pixel sugere a presença de {item_chave} na cena."
        ]
        
        # 30% de chance da câmera estar hackeada e não mostrar nada (Frustração gera desafio)
        if random.random() < 0.3:
            return "ERRO CRÍTICO: Arquivos de vídeo corrompidos ou deletados remotamente."
            
        return random.choice(frases_confusas)

    def confrontar_com_evidencia(self, idx_suspeito, item_usado, detalhes_crime):
        alvo = self.suspeitos[idx_suspeito]
        p_traits = alvo['personalidade'].lower()
        
        # --- CENÁRIO 1: O CULPADO SENDO PEGO (O item é a prova real) ---
        if item_usado in detalhes_crime['pistas_relevantes'] and alvo == self.culpado:
            
            # [REMOVIDO] Não aumentamos mais a pressão aqui.
            # A pressão continua a mesma que estava antes.
            
            return (f"(Os olhos de {alvo['nome']} se arregalam em pânico)\n"
                    f"\"Isso... Onde você achou isso? {item_usado}...\n"
                    f"Eu... eu posso explicar! Não é o que parece!\""), True 

        # --- CENÁRIO 2: INOCENTE VENDO PROVA REAL ---
        elif item_usado in detalhes_crime['pistas_relevantes']:
            
            # [REMOVIDO] Também não aumentamos pressão para inocentes.
            
            dica_visual = self.culpado['visual'].split(' ')[0] 
            return (f"({alvo['nome']} examina o objeto com cuidado)\n"
                    f"\"Isso é prova do crime? Não é meu.\n"
                    f"Mas olhe aqui... tem uma mancha. Parece que foi tocado por alguém usando {dica_visual}.\""), False

        # --- CENÁRIO 3: ITEM INÚTIL (LIXO) ---
        else:
            if "arrogante" in p_traits or "orgulhoso" in p_traits or "irônico" in p_traits:
                respostas = [
                    f"\"Sério? Você interrompeu meu dia para me mostrar {item_usado}? Patético.\"",
                    f"\"Uau. {item_usado}. A polícia está contratando qualquer um hoje em dia?\"",
                    f"\"O que você quer que eu faça com isso? Jogue no lixo.\"",
                    f"\"Isso é tão irrelevante quanto sua investigação.\""
                ]
            elif "nervoso" in p_traits or "simples" in p_traits or "instável" in p_traits:
                respostas = [
                    f"\"E-eu não sei o que é isso! Eu juro! É só {item_usado}!\"",
                    f"\"P-por que você está me mostrando isso? Eu fiz algo errado?\"",
                    f"\"Minha nossa... isso é seu? Eu não quero problemas.\"",
                    f"\"I-isso não tem nada a ver comigo, eu juro!\""
                ]
            elif "educado" in p_traits or "discreto" in p_traits or "calmo" in p_traits:
                respostas = [
                    f"\"Receio que {item_usado} não me pertença, Agente.\"",
                    f"\"Perdão, mas não vejo como isso ajuda na investigação.\"",
                    f"\"Creio que houve um engano. Nunca vi esse objeto.\"",
                    f"\"Lamento, mas isso não é relevante para mim.\""
                ]
            elif "curiosa" in p_traits or "fofoqueira" in p_traits:
                respostas = [
                    f"\"Hmm, {item_usado}? Onde você achou? Era da vítima? Conta tudo!\"",
                    f"\"Que coisa velha! Isso estava na cena do crime? Posso tirar uma foto?\"",
                    f"\"Adoro esses detalhes! Me conte mais sobre onde você encontrou isso.\""
                ]
            else:
                respostas = [
                    f"\"{item_usado}? Não faço ideia do que seja.\"",
                    f"\"Isso não é meu. Pode checar as digitais.\"",
                    f"\"Vocês estão desesperados se acham que isso é uma pista.\""
                ]

            frase_final = random.choice(respostas)
            return f"({alvo['personalidade'].upper()})\n{frase_final}", False
        
    def get_prova_alibi(self, idx): return self.suspeitos[idx]['prova_alibi']
    def pegar_pista_camera(self): return f"Vulto detectado: {self.culpado['visual']}."

    # --- A MÁGICA DO CONFRONTO ---
    # --- VERSÃO 2.0: RESPOSTAS DINÂMICAS ---
    def confrontar_com_evidencia(self, idx_suspeito, item_usado, detalhes_crime):
        alvo = self.suspeitos[idx_suspeito]
        p_traits = alvo['personalidade'].lower() # Pega a personalidade (ex: "arrogante e desconfiado")
        
        # --- CENÁRIO 1: O CULPADO SENDO PEGO (O item é a prova real) ---
        if item_usado in detalhes_crime['pistas_relevantes'] and alvo == self.culpado:
            self.contador_pressao[alvo['nome']] = 6 # Pressão máxima instantânea
            return (f"(Os olhos de {alvo['nome']} se arregalam em pânico)\n"
                    f"\"Isso... Onde você achou isso? {item_usado}...\n"
                    f"Eu... eu posso explicar! Não é o que parece!\""), True 

        # --- CENÁRIO 2: INOCENTE VENDO PROVA DO CRIME ---
        elif item_usado in detalhes_crime['pistas_relevantes']:
            # Respostas variadas para inocentes vendo algo perigoso
            if "nervoso" in p_traits or "instável" in p_traits:
                resp = f"\"Ai meu Deus! Isso é sangue? Tira isso de perto de mim!\""
                acao = "(Recua assustado)"
            elif "arrogante" in p_traits or "frio" in p_traits:
                resp = f"\"Interessante. Parece que vocês acharam a arma do crime. Mas não é minha.\""
                acao = "(Analisa friamente)"
            else:
                resp = f"\"Isso parece sério. Mas eu nunca toquei nesse objeto.\""
                acao = "(Parece confuso)"
                
            return f"{acao}\n{resp}", False

        # --- CENÁRIO 3: ITEM INÚTIL (LIXO/IRRELEVANTE) ---
        # AQUI ESTÁ A MÁGICA: Respostas baseadas na personalidade para não repetir
        else:
            if "arrogante" in p_traits or "orgulhoso" in p_traits or "irônico" in p_traits:
                respostas = [
                    f"\"Sério? Você interrompeu meu dia para me mostrar {item_usado}? Patético.\"",
                    f"\"Uau. {item_usado}. A polícia está contratando qualquer um hoje em dia?\"",
                    f"\"O que você quer que eu faça com isso? Jogue no lixo.\""
                ]
            elif "nervoso" in p_traits or "simples" in p_traits or "instável" in p_traits:
                respostas = [
                    f"\"E-eu não sei o que é isso! Eu juro! É só {item_usado}!\"",
                    f"\"P-por que você está me mostrando isso? Eu fiz algo errado?\"",
                    f"\"Minha nossa... isso é seu? Eu não quero problemas.\""
                ]
            elif "educado" in p_traits or "discreto" in p_traits or "calmo" in p_traits:
                respostas = [
                    f"\"Receio que {item_usado} não me pertença, Agente.\"",
                    f"\"Perdão, mas não vejo como isso ajuda na investigação.\"",
                    f"\"Creio que houve um engano. Nunca vi esse objeto.\""
                ]
            elif "curiosa" in p_traits or "fofoqueira" in p_traits:
                respostas = [
                    f"\"Hmm, {item_usado}? Onde você achou? Era da vítima? Conta tudo!\"",
                    f"\"Que coisa velha! Isso estava na cena do crime? Posso tirar uma foto?\"",
                ]
            else:
                # Resposta genérica para personalidades não mapeadas
                respostas = [
                    f"\"{item_usado}? Não faço ideia do que seja.\"",
                    f"\"Isso não é meu. Pode checar as digitais.\"",
                    f"\"Vocês estão desesperados se acham que isso é uma pista.\""
                ]

            # Escolhe uma aleatória da lista correta
            frase_final = random.choice(respostas)
            return f"({alvo['personalidade'].upper()})\n{frase_final}", False

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
            "Noite passada eu não consegui escutar nada, a Taynara só gritava Bryan!",
            "Noite passada ouvi alguem gritando, Inimigo chegando na AO, Mata ele",
            "Fiquei sabendo que o Maykon corta muito bem os cabelos, viu?",  
            "comprei um sapato novo semana passada, lindo demais, todo mundo elogiou.",          
            "Sabia que todo mundo gosta da Professora Angelica? Um doce de pessoa.",
            "fiquei sabendo que o Michael se formou e eletrotecnia, sera que ele arruma meu aparelho?",
            "Tem um ator novo na Globo que é a cara do Luciano Huck acho que se chama joão.",
            "Você já comeu o bolo de cenoura da Kenya? O cheiro veio aqui agora.",
            "Da minha janela não escapa nem pensamento.",
            "Não é fofoca, é investigação comunitária.",
            "Aceita um cafezinho? Acabei de passar. Tá fresquinho!",
            "Ai, minhas costas estão me matando hoje. Deve ser chuva.",
            "Minha neta instalou esse tal de 'Tinder' no meu celular, acredita?"
        ]

        
        self.fofocas = []
        
        # 1. Fofoca sobre Inocentes
        inocente = random.choice([s for s in suspeitos if s != culpado])
        self.fofocas.append(f"Eu não fui com a cara de {inocente['nome']}. Ele(a) estava suando frio!")
        self.fofocas.append(f"Vi {inocente['nome']} saindo apressado(a) da casa da vítima ontem à noite.")
        self.fofocas.append(f"Ouvi dizer que {inocente['nome']} tinha uma dívida grande com a vítima.")
        self.fofocas.append(f"Alguém me contou que {inocente['nome']} e a vítima brigaram feio semana passada.")
        self.fofocas.append(f"Vi {inocente['nome']} olhando nervosamente para o relógio várias vezes ontem.")
        self.fofocas.append(f"Soube que {inocente['nome']} estava procurando um emprego novo recentemente.")
        self.fofocas.append(f"Alguém viu {inocente['nome']} perto da cena do crime, mas ele(a) disse que estava em outro lugar.")
        self.fofocas.append(f"Ouvi dizer que {inocente['nome']} tinha um álibi meio fraco para a noite do crime.")
        self.fofocas.append(f"Fiquei sabendo que o {inocente['nome']} queria entrar para o grupo dos Los hermanos.")
        
        # 2. Fofoca sobre o Culpado (COM PROTEÇÃO CONTRA O ERRO DE SPLIT)
        visual = culpado['visual'].lower()
        if ' e ' in visual:
            partes = visual.split(' e ')
            dica_visual = random.choice(partes)
        else:
            # Pega a última palavra (ex: 'manchado' de 'dólmã branco manchado')
            dica_visual = visual.split()[-1]

        self.fofocas.append(f"Passou alguém correndo... só vi que usava algo {dica_visual}.")
        self.fofocas.append(f"Não vi o rosto, mas a roupa parecia ter {dica_visual}.")
        self.fofocas.append(f"Alguém falou alto sobre uma roupa {dica_visual} perto da cena do crime.")
        self.fofocas.append(f"Vi um vulto estranho com algo {dica_visual} fugindo do local.")
        self.fofocas.append(f"Ouvi um barulho e vi alguém com roupa {dica_visual} saindo apressado.")  
        self.fofocas.append(f"Alguém disse que viu uma pessoa com roupa {dica_visual} perto da casa da vítima.")
        self.fofocas.append(f"Uma testemunha mencionou uma roupa {dica_visual} na área na noite do crime.")
        self.fofocas.append(f"Alguém comentou sobre uma roupa {dica_visual} que parecia fora do lugar.")
        self.fofocas.append(f"Vi um vulto com algo {dica_visual} perto da cena do crime.")

        # 3. Dica de Item para o PLOT TWIST (Segredo)
        self.fofocas.append("Achei este papel no chão do corredor: 'Senha Anotada'. Pode ficar.")
        self.fofocas.append("Achei uma 'Chave Enferrujada' no vaso de plantas. Será que abre algo?")
        self.fofocas.append("Vi um cofre pequeno na sala da vítima. Tinha uma 'Chave Enferrujada' perto.")
        self.fofocas.append("A vítima costumava anotar senhas em um caderno. Encontrei uma 'Senha Anotada' aqui.")
        self.fofocas.append("Achei um pedaço de papel com uma 'Senha Anotada' perto da mesa da vítima.")
        self.fofocas.append("Vi uma 'Chave Enferrujada' caída perto da estante de livros da vítima.")
        self.fofocas.append("Achei este papel no chão: 'Senha Anotada'. Pode ficar.")
        self.fofocas.append("Achei uma 'Chave Enferrujada' no vaso. Será que abre algo?")
        self.fofocas.append("Menino(a), achei essa 'Lupa' velha na gaveta. Serve pra você?")
        self.fofocas.append("Toma essa 'Fita Adesiva', vai que você precisa colar algo.")
        self.fofocas.append("Achei esse 'Cartão de Acesso' caído no tapete.")
        self.fofocas.append("Alguém esqueceu essa 'Tabela de Símbolos' no elevador.")
        self.fofocas.append("Peguei essa 'Carta de Advogado' na caixa de correio por engano.")

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
    # Corrige o KeyError usando as listas novas
    c = random.choice(CRIMES_DB)
    return {
        "local": random.choice(LOCAIS_EXPANDIDOS),
        
        "hora": f"{random.randint(0,4):02d}:{random.randint(10,59):02d}",
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
        pywhatkit.sendwhatmsg_instantly(agente['telefone'], texto, 15, True)
        
        # 2. Segurança para garantir o envio (Enter)
        time.sleep(4) # Espera a aba abrir
        pyautogui.press('enter')
        
        # 3. Força o fechamento da aba
        time.sleep(2) # Espera a mensagem ir
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
            

        elif op == '2': # REMOVER (NOVO!)
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
                

        elif op == '3': # LIMPAR TUDO
            confirm = input(f"  {Cor.VERMELHO}>> TEM CERTEZA? (S/N): {Cor.RESET}").upper()
            if confirm == 'S':
                agentes = []
                with open(ARQUIVO_DADOS, 'w') as f: json.dump([], f)
                print(f"  {Cor.VERMELHO}>> DATABASE FORMATADA.{Cor.RESET}"); time.sleep(1)
                

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
    suspeitos = random.sample(pool, 5)
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
        print(f"{Cor.CINZA}╔{'═'*79}╗{Cor.RESET}")
        print(f"{Cor.CINZA}║ {Cor.VERMELHO_SANGUE}MANCHETE DO DIA: {cor_news}{noticia.center(61)} {Cor.CINZA}║{Cor.RESET}")
        print(f"{Cor.CINZA}╚{'═'*79}╝{Cor.RESET}\n")

        print(f"LOCAL: {detalhes['local']} | VÍTIMA: {vitima['nome']} | HORA DO CRIME: {detalhes['hora']}\n")
        print(f"AÇÕES REALIZADAS: {rodadas_jogadas} (Quanto mais demora, pior a imprensa fica)\n")   
        
        print(f"{Cor.BRANCO}MENU DE AÇÕES TÁTICAS:{Cor.RESET}")
        print("[1] 👥  Falar com Suspeitos")
        print("[2] 📹  Usar a Câmeras")
        print("[3] 🔬  Usar o Drone")
        print("[4] ☕  Visitar Dona Neide")
        print(f"{Cor.AZUL_CYBER}[5] ⚗️  LABORATÓRIO (COMBINAR ITENS){Cor.RESET}") # <--- NOVO
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
        elif op == '2':
            barra_carregamento("HACKEANDO SERVIDOR DE VÍDEO")
            
            # Gera horário aleatório
            hora_cam = f"{random.randint(0,3):02d}:{random.randint(10,59):02d}"
            
            # 1. Escolhe um suspeito ALEATÓRIO (pode ser o culpado ou um inocente)
            suspeito_no_video = random.choice(suspeitos)
            
            # 2. Lista de ações que parecem crime, mas podem não ser
            acoes_suspeitas = [
                f"discutindo agressivamente com a vítima.",
                f"carregando uma mala pesada pelo corredor.",
                f"apagando arquivos no computador da vítima.",
                f"mexendo no quadro de disjuntores elétricos.",
                f"escondendo um objeto atrás das costas.",
                f"saindo do prédio com uma sacola plástica.",
                f"falando ao telefone em tom nervoso.",
                f"olhando ao redor de forma suspeita.",
                f"tentando forçar a fechadura de uma porta.",
                f"correndo pelo corredor como se estivesse fugindo.",
                f"removendo fitas adesivas de uma caixa.",
                f"ajustando a câmera de segurança.",
                f"colocando luvas de látex nas mãos.",
                f"entregando um envelope pardo para a vítima.",
                f"chorando encostado na parede do corredor.",
                f"tentando abrir uma porta trancada, sem sucesso.",
                f"limpando uma mancha na manga da camisa.",
                f"saindo apressado(a) falando ao celular.",
                f"ameaçando a vítima com o dedo em riste.",
                f"vasculhando a bolsa da vítima quando ela não estava olhando."
            ]
            
            acao = random.choice(acoes_suspeitas)
            
            # 3. Monta a pista
            pista = f"[{hora_cam}] A câmera pegou {suspeito_no_video['nome']} {acao}"
            
            painel("CFTV - GRAVAÇÃO RECUPERADA", pista, Cor.AZUL_CYBER)
            audio.falar(pista)
            input("[ENTER]")

        elif op == '3':
            print(f"{Cor.AMARELO}>> INICIANDO VARREDURA TÉRMICA...{Cor.RESET}")
            som_drone = media.tocar_efeito("drone.mp3", loop=False) 
            barra_carregamento("MAPEANDO PERÍMETRO")
            
            # --- LÓGICA SIMPLIFICADA ---
            # O Drone procura nas pistas do crime E na lista gigante de ingredientes
            # Ele filtra (if i not in inv.inventario) para não pegar o que você já tem
            
            pool_de_busca = detalhes['pistas_relevantes'] + PISTAS_IRRELEVANTES
            
            itens_possiveis = [i for i in pool_de_busca if i not in inv.inventario]

            if not itens_possiveis:
                painel("SCANNER: VAZIO", ["Não há mais evidências nesta área."], Cor.CINZA)
                audio.falar("Área limpa.")
            else:
                item = random.choice(itens_possiveis)
                if som_drone: som_drone.stop()
                
                inv.adicionar_item(item)
                painel(f"SCANNER: EVIDÊNCIA", [f"Objeto: {item}", "STATUS: COLETADO"], Cor.VERDE_NEON)
                audio.falar(f"Encontrei {item}. Guardando.")
            
            input("[ENTER]")
            rodadas_jogadas += 1

        # --- OPÇÃO 4: DONA NEIDE (ATUALIZADA) ---
        elif op == '4':
            media.tocar_efeito("campainha.mp3")
            digitar(">> Dona Neide atende a porta...", 0.03)
            
            # Chama a Neide nova (que não repete e dá itens)
            fofoca, item_extra = neide.fofocar()
            
            painel("DONA NEIDE", fofoca, Cor.ROXO)
            audio.falar(fofoca)
            
            if item_extra:
                inv.adicionar_item(item_extra)
                print(f"\n{Cor.VERDE}>> {item_extra} ADICIONADO AO INVENTÁRIO!{Cor.RESET}")
            
            input("[ENTER]")
            rodadas_jogadas += 1

       # --- OPÇÃO 5: LABORATÓRIO E COMUNICAÇÃO (CORRIGIDO) ---
        elif op == '5':
            print(f"\n{Cor.AZUL_CYBER}>> ACESSANDO BANCADA DE LABORATÓRIO...{Cor.RESET}")
            
            # SUB-MENU DO LABORATÓRIO
            print(f"\n{Cor.BRANCO}O QUE DESEJA FAZER?{Cor.RESET}")
            print(f"[1] ⚗️  TENTAR COMBINAÇÃO (CRAFTING)")
            print(f"[2] 📲  ENVIAR INVENTÁRIO PARA EQUIPE")
            print(f"[3] 🔙  VOLTAR")
            
            sub_op = input(f"\n{Cor.VERDE_NEON}>> ESCOLHA: {Cor.RESET}")

            # --- A. COMBINAR ITENS ---
            if sub_op == '1':
                barra_carregamento("CRUZANDO DADOS")
                
                # Chama sua função de combinar (aquela manual que fizemos)
                msg, sucesso = inv.combinar_itens()
                
                cor_msg = Cor.VERDE_NEON if sucesso else Cor.AMARELO
                painel("RELATÓRIO DE ANÁLISE", msg, cor_msg)
                
                if sucesso:
                    media.tocar_efeito("acertopoints.mp3")
                    audio.falar("Sucesso. Nova evidência gerada.")
                else:
                    media.tocar_efeito("falha1.mp3")
                    audio.falar("Combinação falhou.")
                
                input("[ENTER]")
                rodadas_jogadas += 1 # Gasta tempo

            # --- B. ENVIAR ZAP ---
            elif sub_op == '2':
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
                    rodadas_jogadas += 1 # Gasta tempo
            
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
    