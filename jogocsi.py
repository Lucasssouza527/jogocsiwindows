import sys
import os
import time
import json
import random
import subprocess
import threading
import textwrap
from datetime import datetime

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

# --- BANCO DE DADOS COMPLETO (RECUPERADO E CORRIGIDO) ---
# ATENÇÃO: Agora está com apenas UM par de colchetes [ ] para não dar erro.

ARQUETIPOS_COMPLETOS = [
  {
    "nome": "O Guarda-Costas",
    "video": "guarda_costas.mp4",
    "visual": "terno preto e óculos escuros",
    "personalidade": "reservado e profissional",
    "relacao_com_vitima": "proteção pessoal diária",
    "alibi": "estava fazendo a ronda externa",
    "prova_alibi": "Registros do bastão de ronda eletrônico confirmam os horários.",
    "luto": "O silêncio dele pesa mais que palavras. Ele aperta os punhos ao lembrar.",
    "reacao_pressao": "responde curto, mantém postura rígida"
  },
  {
    "nome": "O Sócio",
    "video": "socio.mp4",
    "visual": "terno preto e relógio de ouro",
    "personalidade": "calculista e defensivo",
    "relacao_com_vitima": "negócios e interesses financeiros",
    "alibi": "reunião por chamada de vídeo",
    "prova_alibi": "Log de conexão do Zoom e gravação da reunião na nuvem.",
    "luto": "É uma perda enorme… para todos nós.",
    "reacao_pressao": "tenta inverter a culpa com lógica fria"
  },
  {
    "nome": "A Viúva",
    "video": "viuva.mp4",
    "visual": "vestido preto longo e véu",
    "personalidade": "emocionalmente instável",
    "relacao_com_vitima": "casamento conturbado",
    "alibi": "sozinha no quarto",
    "prova_alibi": "Histórico da Alexa: ela pediu músicas tristes às 23h40.",
    "luto": "Não consigo aceitar que nunca mais vou ouvi-lo.",
    "reacao_pressao": "chora, mas se fecha quando insistem"
  },
  {
    "nome": "O Mordomo",
    "video": "mordomo.mp4",
    "visual": "luvas brancas impecáveis",
    "personalidade": "discreto e observador",
    "relacao_com_vitima": "serviço de longa data",
    "alibi": "preparando o jantar",
    "prova_alibi": "Câmera da cozinha mostra ele polindo a prataria sem parar.",
    "luto": "Servi essa casa por anos… isso nunca deveria ter acontecido.",
    "reacao_pressao": "responde educadamente, mas omite detalhes"
  },
  {
    "nome": "O Jardineiro",
    "video": "jardineiro.mp4",
    "visual": "macacão sujo de terra",
    "personalidade": "simples e nervoso",
    "relacao_com_vitima": "empregado ocasional",
    "alibi": "trabalhando no fundo do terreno",
    "prova_alibi": "As ferramentas dele estão lá, e a terra está revirada fresca.",
    "luto": "Ele sempre foi bom comigo.",
    "reacao_pressao": "se confunde e entra em contradição"
  },
  {
    "nome": "A Vizinha",
    "video": "vizinha.mp4",
    "visual": "roupão velho e binóculos",
    "personalidade": "curiosa e intrometida",
    "relacao_com_vitima": "observadora constante",
    "alibi": "assistindo televisão",
    "prova_alibi": "Ela descreve exatamente o comercial que passou na hora do crime.",
    "luto": "Nunca pensei que veria algo assim da minha janela.",
    "reacao_pressao": "fala demais, entrega informações sem perceber"
  },
  {
    "nome": "O Hacker",
    "video": "hacker.mp4",
    "visual": "moletom com capuz e máscara",
    "personalidade": "irônico e desconfiado",
    "relacao_com_vitima": "prestador de serviços digitais",
    "alibi": "online a noite inteira",
    "prova_alibi": "Logs da Twitch mostram ele fazendo live stream sem interrupção.",
    "luto": "Isso saiu totalmente do controle.",
    "reacao_pressao": "desvia com sarcasmo"
  },
  {
    "nome": "A Influencer",
    "video": "influencer.mp4",
    "visual": "roupa de festa e anel de luz",
    "personalidade": "egocêntrica",
    "relacao_com_vitima": "amizade por interesse",
    "alibi": "live nas redes sociais",
    "prova_alibi": "O vídeo está salvo no perfil dela com o timestamp correto.",
    "luto": "Eu ainda estou em choque, sério.",
    "reacao_pressao": "atua emocionalmente para convencer"
  },
  {
    "nome": "O Chef",
    "video": "chef.mp4",
    "visual": "dólmã branco manchado",
    "personalidade": "orgulhoso e estressado",
    "relacao_com_vitima": "responsável pelas refeições",
    "alibi": "na cozinha com a equipe",
    "prova_alibi": "Dois assistentes confirmam que ele estava gritando com eles.",
    "luto": "Perdi o apetite desde então.",
    "reacao_pressao": "fica agressivo se questionado"
  },
  {
    "nome": "A Bailarina",
    "video": "bailarina.mp4",
    "visual": "sapatilhas e tutu rasgado",
    "personalidade": "sensível e retraída",
    "relacao_com_vitima": "relacionamento secreto",
    "alibi": "ensaiando sozinha",
    "prova_alibi": "Sapatilhas gastas e suor recente, mas sem testemunhas visuais.",
    "luto": "Tudo o que eu fazia era por ele.",
    "reacao_pressao": "quebra emocionalmente rápido"
  },
  { 
    "nome": "O Professor",
    "video": "professor.mp4",
    "visual": "camisa social e óculos",
    "personalidade": "intelectual e reservado",
    "relacao_com_vitima": "aluno antigo",
    "alibi": "em casa lendo",
    "prova_alibi": "Livros abertos e uma caneca de café na mesa.",
    "luto": "Ele era meu mentor.",
    "reacao_pressao": "fica calmo, mas evita responder"
  },
    { 
    "nome": "A Artista",
    "video": "artista.mp4",
    "visual": "roupas coloridas e tinta",
    "personalidade": "criativa e impulsiva",
    "relacao_com_vitima": "cliente e musa",
    "alibi": "pintando no estúdio",
    "prova_alibi": "Tela molhada e cheiro de tinta fresca.",
    "luto": "Ele inspirava minha arte.",
    "reacao_pressao": "fala em metáforas e divaga"
  },

  { 
    "nome": "O Motorista",
    "video": "motorista.mp4",
    "visual": "uniforme de taxi e óculos escuros",
    "personalidade": "calmo e observador",
    "relacao_com_vitima": "cliente ocasional",
    "alibi": "no trabalho",
    "prova_alibi": "Relatório de corridas e GPS do veículo.",
    "luto": "Ele era um cliente comum.",
    "reacao_pressao": "fica nervoso, mas tenta manter a compostura"
  },
]

# Dados Complementares para evitar erros
LOCAIS_EXPANDIDOS = ["Apartamento de Luxo", "Beco Escuro", "Sala de Servidores", "Estacionamento Subsolo", "Mansão na Serra", "Laboratório,quarto andar", "Cobertura Panorâmica", "Clube Noturno", "Escritório Corporativo", "Parque Abandonado, Centro da Cidade", "Restaurante Chique", "Hotel 5 Estrelas", "Bar da Esquina", "Galeria de Arte", "Cinema Privado"]
TESTEMUNHAS_INICIAIS = ["o entregador", "uma vizinha", "o zelador", "um corredor", "a faxineira", "um segurança", "o porteiro", "um turista perdido", "a garçonete", "um ciclista", "o motorista de táxi", "um pedestre apressado", "a criança brincando", "o jardineiro", "o vendedor ambulante", "a fotógrafa", "o policial de ronda", "o morador local"]
POSICOES_CORPO = ["caído de bruços", "sentado na poltrona", "estirado no chão", "escondido no armário", "encostado na parede", "deitado na cama", "ajoelhado no tapete", "em pé, encostado na mesa", "caído na escada", "dentro do carro", "no banheiro", "na varanda", "no porão", "na cozinha", "no jardim", "na garagem"]
PISTAS_IRRELEVANTES = ["Embalagem de fast-food", "Relógio parado", "Marcas de lama", "Café morno", "Janela aberta", "Papel amassado", "Chave de fenda", "Garrafas vazias", "Roupas molhadas", "Cartão de visita rasgado", "Fios soltos", "Pegadas de sapato comum", "Bilhete anônimo", "Cigarro apagado", "Caneta sem tinta"]

# --- SUBSTITA O CRIMES_DB ANTIGO POR ESTE ---
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
        if TEM_PYGAME and os.path.exists(nome):
            try: 
                pygame.mixer.music.load(nome)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.4)
            except: pass

    def tocar_efeito(self, nome, loop=False):
        if TEM_PYGAME and os.path.exists(nome):
            try: 
                som = pygame.mixer.Sound(nome)
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
        # Verifica se o arquivo existe ANTES de tentar abrir
        if not os.path.exists(video_file):
            print(f"{Cor.AMARELO}>> ARQUIVO DE VÍDEO NÃO ENCONTRADO: {video_file} (Pulando...){Cor.RESET}")
            time.sleep(1)
            return # Sai da função sem dar erro

        # Toca audio de fundo
        if audio_file and TEM_PYGAME and os.path.exists(audio_file):
            som_fundo = pygame.mixer.Sound(audio_file)
            som_fundo.play()
        else:
            som_fundo = None

        try:
            import cv2
            cap = cv2.VideoCapture(video_file)
            window_name = "PERFILAMENTO (ENTER para PULAR)" # Mudei o nome para avisar o usuário
            
            # Configura para permitir redimensionar
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
            
            # --- ADICIONE ISSO PARA O TAMANHO MÉDIO ---
            cv2.resizeWindow(window_name, 960, 540) 
            # ------------------------------------------

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break 
                cv2.imshow(window_name, frame)
                
                # --- ESTA LINHA É A QUE FECHA COM ENTER ---
                # 13 = Enter, 32 = Espaço, 27 = Esc, 'q' = Quit
                if cv2.waitKey(25) in [13, 32, 27, ord('q')]: 
                    print(f"\n{Cor.AMARELO}>> VÍDEO INTERROMPIDO PELO USUÁRIO.{Cor.RESET}")
                    break
                # ------------------------------------------
            
            cap.release()
            cv2.destroyAllWindows() # Garante que a janela some
        except:
            # Se der erro no OpenCV, tenta abrir normal ou ignora
            try: os.startfile(video_file)
            except: pass
        
        if som_fundo: som_fundo.stop()

    def efeito_matrix(self):
        # ... (seu código matrix continua igual)
        pass

media = MediaManager()

# 3. DEFINIÇÃO DA CLASSE DE ÁUDIO (ANTES DE USAR!)
class AudioSystem:
    def falar(self, texto):
        limpo = texto.replace('*', '').replace('"', '')
        arq = f"voz_{random.randint(1000,9999)}.mp3"
        try:
            subprocess.run([sys.executable, "-m", "edge_tts", "--voice", "pt-BR-AntonioNeural", "--text", limpo, "--write-media", arq], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(arq) and TEM_PYGAME:
                pygame.mixer.music.set_volume(0.1)
                s = pygame.mixer.Sound(arq); s.play()
                while pygame.mixer.get_busy(): time.sleep(0.1)
                pygame.mixer.music.set_volume(0.4)
                os.remove(arq)
        except: pass

# 4. INSTANCIA O AUDIO SYSTEM (SÓ AGORA, QUE A CLASSE JÁ EXISTE)
audio = AudioSystem()

class InvestigationManager:
    def __init__(self, suspeitos, culpado):
        self.suspeitos = suspeitos
        self.culpado = culpado
        self.contador_pressao = {s['nome']: 0 for s in suspeitos}
        self.inventario = []

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
                    f"(DICA: Pressione Dona Neide para confirmar se ele realmente estava lá.)")
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
        
        # 1. CULPADO PEGO (Confissão)
        if item_usado in detalhes_crime['pistas_relevantes'] and alvo == self.culpado:
            self.contador_pressao[alvo['nome']] = 6
            return (f"(Os olhos de {alvo['nome']} se arregalam em pânico)\n"
                    f"\"Isso... Onde você achou isso? {item_usado}...\n"
                    f"Eu... eu posso explicar! Não é o que parece!\""), True 

        # 2. INOCENTE VENDO PROVA REAL (Aqui entra a Novidade 3: Dica de Digitais)
        elif item_usado in detalhes_crime['pistas_relevantes']:
            
            # --- NOVIDADE 3: SISTEMA DE DIGITAIS ---
            # O inocente analisa o item e dá uma dica visual do verdadeiro dono
            dica_visual = self.culpado['visual'].split(' ')[0] # Ex: "Terno", "Vestido", "Luvas"
            return (f"({alvo['nome']} examina o objeto com cuidado)\n"
                    f"\"Isso é prova do crime? Não é meu.\n"
                    f"Mas olhe aqui... tem uma mancha. Parece que foi tocado por alguém usando {dica_visual}.\""), False

        # 3. ITEM LIXO (Personalidade Dinâmica que fizemos antes)
        else:
            if "arrogante" in p_traits:
                resp = f"\"Sério? Você interrompeu meu dia para me mostrar {item_usado}? Patético.\""
            elif "nervoso" in p_traits:
                resp = f"\"E-eu não sei o que é isso! Eu juro! É só {item_usado}!\""
            elif "curiosa" in p_traits:
                resp = f"\"Hmm, {item_usado}? Onde você achou? Posso tirar uma foto?\""
            else:
                resp = f"\"{item_usado}? Não faço ideia do que seja. Verifique as digitais.\""
            
            return f"({alvo['personalidade'].upper()})\n{resp}", False
        
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
            "a Taynara e o Lucas viajaram para Campos do Jordão semana passada!",
            "Maykon e a Kenya falam que sente o Frio da Europa, mesmo morando no Rio, Queria saber o que eles estão aprontando...",
            "O Michael e a Angelica Malha Juntos, ouvi ela falando que ele tem que malhar perna kkkk",
            "o João tem uma namorada que mora em cachoeira de macacu, ele vive falando dela...",
            "Fiquei sabendo que o Maykon corta muito bem os cabelos, viu?",
            "Sabia que todo mundo gosta da Professora Angelica? Um doce de pessoa.",
            "Tem um ator novo na Globo que é a cara do Luciano Huck.",
            "Você já comeu o bolo de cenoura da Kenya? O cheiro veio aqui agora.",
            "Aceita um cafezinho? Acabei de passar. Tá fresquinho!",
            "Ai, minhas costas estão me matando hoje. Deve ser chuva.",
            "Minha neta instalou esse tal de 'Tinder' no meu celular, acredita?"
        ]

        
        self.fofocas = []
        
        # 1. Fofoca sobre um Inocente (Para confundir)
        # Ela vê alguém suspeito, mas que não fez nada
        inocente = random.choice([s for s in 
                                  suspeitos if s != culpado])
        self.fofocas.append(f"Eu não fui com a cara de {inocente['nome']}. Ele(a) estava suando frio!")
        self.fofocas.append(f"Quando fui comprar pão, vi {inocente['nome']} olhando estranho para mim.")
        self.fofocas.append(f"Outro dia, vi {inocente['nome']} falando sozinho(a) no jardim, sera que é o senhor fulano?")
        self.fofocas.append(f"{inocente['nome']} sempre Fala de um grupo, acho que é Los Hermanos.")
        self.fofocas.append(f"Vi {inocente['nome']} mexendo no celular de forma muito suspeita no corredor.")
        
        # 2. Fofoca sobre o Culpado (PISTAS VAGAS - O SEGREDO ESTÁ AQUI)
        visual = culpado['visual'].lower()
        
        # Lógica inteligente para pegar só uma parte da roupa
        if ' e ' in visual:
            # Se for "terno preto e óculos", pega só "terno preto" ou "óculos"
            partes = visual.split(' e ')
            dica_visual = random.choice(partes)
        else:
            # Se for "dólmã branco", pega só a cor ou o tecido se possível
            palavras = visual.split()
            # Tenta pegar a última palavra (geralmente é a cor ou detalhe: "escuros", "branco", "manchado")
            dica_visual = f"algo {palavras[-1]}"
            
        self.fofocas.append(f"Passou alguém correndo... só vi que usava {dica_visual}.")
        self.fofocas.append(f"Não vi o rosto, mas a roupa parecia ter {dica_visual}.")
        self.fofocas.append(f"Alguém com {dica_visual} passou por mim, parecia com pressa.")
        self.fofocas.append(f"Uma pessoa vestindo {dica_visual} estava saindo apressado(a) do prédio.")
        self.fofocas.append(f"Vi um vulto passando rápido com {dica_visual}.")
        
        # 3. Fofoca sobre a Cena (Atmosfera)
        self.fofocas.append(f"Antes do silêncio, ouvi {historia['dica_neide']} caindo no chão.")
        self.fofocas.append(f"Escutei uma discussão acalorada, parecia que alguém estava muito bravo(a).")
        self.fofocas.append(f"Alguém gritou algo como 'Eu vou matar você! menino nessa hora eu fiquei assustada.'")
        self.fofocas.append(f"Ouvi passos apressados saindo do prédio.")
        self.fofocas.append(f"Parece que a porta dos fundos ficou aberta.")
        
        random.shuffle(self.fofocas)

    def fofocar(self):
        intro = random.choice(self.papo_furado)
        if self.fofocas:
            dica = self.fofocas.pop(0) 
            return f"{intro}\n\n(Sussurrando) Mas olha... {dica}", True
        else:
            return f"{intro}\n\nAh, já falei demais. Daqui a pouco o assassino vem atrás de mim!", False
    def __init__(self, suspeitos, culpado, historia):
        # Neide julga as pessoas pela aparência
        self.papo_furado = [
            "Noite passada eu não consegui escutar nada, a Taynara só gritava Bryan!",
            "Fiquei sabendo que o Maykon corta muito bem os cabelos, viu?",
            "Sabia que todo mundo gosta da Professora Angelica? Um doce de pessoa.",
            "Tem um ator novo na Globo que é a cara do Luciano Huck.",
            "Você já comeu o bolo de cenoura da Kenya? O cheiro veio aqui agora.",
            "Aceita um cafezinho? Acabei de passar. Tá fresquinho!",
            "Ai, minhas costas estão me matando hoje. Deve ser chuva.",
            "Minha neta instalou esse tal de 'Tinder' no meu celular, acredita?"
        ]
        
        self.fofocas = []
        
        # 1. Fofoca sobre um Inocente
        inocente = random.choice([s for s in suspeitos if s != culpado])
        self.fofocas.append(f"Eu não fui com a cara de {inocente['nome']}. Tinha um olhar maligno!")
        self.fofocas.append(f"Vi {inocente['nome']} andando de um lado para o outro, parecia preocupado(a).")
        
        # 2. Fofoca sobre o Culpado (COM PROTEÇÃO CONTRA ERROS)
        visual = culpado['visual'].lower()
        
        # Tenta dividir a roupa em duas partes, se der erro, usa a roupa toda
        if ' e ' in visual:
            parte1 = visual.split(' e ')[0]
            parte2 = visual.split(' e ')[1]
        else:
            parte1 = visual
            parte2 = visual

        self.fofocas.append(f"Vi alguém de {parte1} correndo. Parecia nervoso(a).")
        self.fofocas.append(f"Alguém com {parte2} estava saindo apressado(a) do prédio.")
        self.fofocas.append(f"Uma pessoa vestindo {visual} passou por mim, parecia estar com pressa.")
        
        # 3. Fofoca sobre a Cena
        self.fofocas.append(f"Antes do silêncio, ouvi uma gritaria feia. Parecia briga.")
        self.fofocas.append(f"Alguém saiu batendo a porta de incêndio com muita força.")
        self.fofocas.append(f"Escutei um som estranho, parecia {historia['dica_neide']} caindo.")

        random.shuffle(self.fofocas)

    def fofocar(self):
        intro = random.choice(self.papo_furado)
        if self.fofocas:
            dica = self.fofocas.pop(0) 
            return f"{intro}\n\n(Sussurrando) Mas olha... {dica}", True
        else:
            return f"{intro}\n\nAh, já falei demais. Daqui a pouco o assassino vem atrás de mim!", False
        
    def __init__(self, suspeitos, culpado, historia):
        # Neide julga as pessoas pela aparência
        self.papo_furado = [
            "Noite passada eu não consegui escutar nada, a Taynara só gritava Bryan!",
            "Fiquei sabendo que o Maykon corta muito bem os cabelos, viu? Se precisar de um trato, é com ele mesmo.",
            "Fiquei sabendo que o Michael se formou em eletrotécnica, acredita? Dizem que ele conserta qualquer coisa!",
            "Sabia que todo mundo gosta da Professora Angelica? Dizem que ela é um doce de pessoa.",
            "Tem um ator novo na Globo que é a cara do Luciano Huck, você viu? acho que se chama Jhon",
            "Você ja comeu o bolo de cenoura da Kenya? o cheiro veio aqui na minha janela agora pouco.",
            "Aceita um cafezinho? Acabei de passar. Tá fresquinho!",
            "A Rafaela foi la para o Rio de Janeiro semana passada, disse que adorou a praia de Copacabana.",
            "Ai, minhas costas estão me matando hoje. Deve ser chuva.",
            "Você viu o capítulo da novela ontem? A Nazaré não vale nada!",
            "Eu moro aqui há 30 anos, nunca vi uma barulheira dessas.",
            "Esse prédio já foi melhor. Hoje em dia entra qualquer um.",
            "Você é solteiro? Tenho uma sobrinha que é uma jóia..."
        ]

        
        self.fofocas = []
        
        # 1. Fofoca sobre um Inocente (Para confundir)
        inocente = random.choice([s for s in suspeitos if s != culpado])
        self.fofocas.append(f"Eu não fui com a cara de {inocente['nome']}. Tinha um olhar maligno!")
        self.fofocas.append(f"Vi {inocente['nome']} andando de um lado para o outro, parecia preocupado(a).")
        self.fofocas.append(f"Acho que {inocente['nome']} estava tentando esconder algo... Vi ele(a) mexendo no bolso.")
        self.fofocas.append(f"{inocente['nome']} sempre foi meio estranho(a), sabia? Nunca gostei dele(a).")
        self.fofocas.append(f"Vi {inocente['nome']} olhando fixamente para a casa da vítima. Parecia estar tramando algo.")
        
        # 2. Fofoca sobre o Culpado (A Verdade misturada)
        visual = culpado['visual'].lower()
        self.fofocas.append(f"Vi alguém de {visual.split(' e ')[0]} correndo. Parecia nervoso(a).")
        self.fofocas.append(f"Alguém com {visual.split(' e ')[1]} estava saindo apressado(a) do prédio.")
        self.fofocas.append(f"Uma pessoa vestindo {visual} passou por mim, parecia estar com pressa.")
        self.fofocas.append(f"Alguém com {visual} chamou minha atenção. Parecia estar fugindo de algo.")
        self.fofocas.append(f"Vi uma pessoa usando {visual} perto da cena do crime. Parecia nervosa.")
        
        # 3. Fofoca sobre a Cena (Barulhos)
        self.fofocas.append(f"Antes do silêncio, ouvi uma gritaria feia. Parecia briga de casal ou sócios.")
        self.fofocas.append(f"Alguém saiu batendo a porta de incêndio com muita força.")
        self.fofocas.append(f"Ouvi um barulho de vidro quebrando, seguido de um baque surdo.")
        self.fofocas.append(f"Teve um som de passos apressados, como se alguém estivesse fugindo.")
        self.fofocas.append(f"Escutei um som estranho, parecia algo metálico caindo no chão.")
        self.fofocas.append(f"Antes do silêncio, ouvi um grito abafado, parecia de dor ou surpresa.")

        
        random.shuffle(self.fofocas)

    def fofocar(self):
        intro = random.choice(self.papo_furado)
        
        if self.fofocas:
            dica = self.fofocas.pop(0) 
            return f"{intro}\n\n(Sussurrando) Mas olha... {dica}", True
        else:
            return f"{intro}\n\nAh, já falei demais. Daqui a pouco o assassino vem atrás de mim!", False

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
        f"Agentes, visite a Dona Neide, Ela parece que viu bastante coisa.\n"
        
    )
    return relatorio

def gerar_dossie_suspeitos(lista_suspeitos):
    # Cabeçalho Tático
    relatorio = (
        f"📂 *DOSSIÊ TÁTICO: SUSPEITOS (NÍVEL 1)*\n"
        f"CONFIDENCIAL // USO RESTRITO\n"
        f"════════════════════════════════════\n"
    )
    
    for i, s in enumerate(lista_suspeitos):
        icone = "👤"
        if "nervoso" in s['personalidade']: icone = "😰"
        elif "arrogante" in s['personalidade']: icone = "😒"
        elif "calmo" in s['personalidade']: icone = "😐"
        elif "instável" in s['personalidade']: icone = "😭"
        
        # --- AQUI ESTAVA O ERRO DE SINTAXE (CORRIGIDO) ---
        # Note que agora é f"*ID... e não f"*{ID...
        relatorio += f"*ID #{i+1:02d} | CODINOME: {s['nome'].upper()}* {icone}\n"
        
        # Mudei para "Marcadores" em vez de Visual direto, fica mais chique
        relatorio += f"├─ Perfil: {s['personalidade']}\n"
        relatorio += f"├─ Marcadores Visuais: {s['visual']}\n" 
        relatorio += f"└─ Vínculo: {s['relacao_com_vitima']}\n\n"
    
    relatorio += "------------------------------------\n"
    relatorio += "⚠️ *INSTRUÇÃO:* Cruzar dados visuais com relatos das testemunhas."
    return relatorio

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
        
        # --- CORREÇÃO AQUI ---
        # Removi as chaves { } que estavam em volta da palavra ID
        # Antes estava: f"*{ID ...
        # Agora está:   f"*ID ...
        relatorio += f"*ID #{i+1:02d} | {s['nome'].upper()}* {icone}\n"
        
        relatorio += f"├─ Perfil: {s['personalidade']}\n\n"
        
    
    relatorio += "------------------------------------\n"
    relatorio += "⚠️ *CUIDADO:* O assassino está nesta lista."
    return relatorio

    # Cabeçalho do Anexo
    relatorio = (
        f"📂 *LISTA DE PESSOAS SUSPEIAS (PDI)*\n"
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
    print(f"  │ [SERVER]: {Cor.VERDE_NEON}ONLINE{Cor.AZUL_CYBER}   [MEM]: {memoria}GB   [LATENCY]: {random.randint(10,50)}ms   [SEC]: {Cor.AMARELO}HIGH{Cor.AZUL_CYBER} │")
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
        print(f"  ║ [ENTER] INICIAR  ║")
        print(f"  ╚{'═'*20}╝{Cor.RESET}")
        
        op = input(f"\n{Cor.AZUL_CYBER}  TERMINAL >> {Cor.RESET}").upper()
        
        # --- LÓGICA ---
        
        if op == '1': # ADICIONAR
            print(f"\n  {Cor.AMARELO}>> NOVO REGISTRO:{Cor.RESET}")
            n = input("  Nome de Codinome: ")
            t = input("  Frequência (Zap): ")
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

def jogar(agentes):
    barra_carregamento("BAIXANDO DADOS DA INTERPOL")
    
    # 1. GERA OS DADOS
    detalhes = gerar_detalhes_crime()
    
    # Sorteio (Mantenha seu código de sorteio aqui...)
    vitima = random.choice(ARQUETIPOS_COMPLETOS)
    pool = [p for p in ARQUETIPOS_COMPLETOS if p['nome'] != vitima['nome']]
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
    
    
    while True:
        limpar_tela(); logo_profissional()
        print(f"LOCAL ATUAL: {detalhes['local']} | VÍTIMA: {vitima['nome']}\n | HORA DO CRIME: {detalhes['hora']}\n")        
        print(f"\n{Cor.BRANCO}MENU DE AÇÕES:{Cor.RESET}")
        print("[1] 👥  Gerenciar Suspeitos (Interrogar/Perfil)")
        print("[2] 📹  Hackear Câmeras")
        print("[3] 🔬  Forense (Drone)")
        print("[4] ☕  Visitar Dona Neide")
        print(f"{Cor.VERMELHO}[5] 🚨  ACUSAR (FINAL){Cor.RESET}")
        print("[6] ❌  Sair")
        
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
                            # Lógica do Inventário
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
                                        
                                        painel("REAÇÃO DO SUSPEITO", reacao, Cor.VERMELHO_SANGUE)
                                        audio.falar(reacao.replace('"', ''))
                                        
                                        # Cria uma variável para controlar o som
                                        som_tensao = None 
                                        
                                        if ficou_nervoso:
                                            # Guardamos o som na variável
                                            som_tensao = media.tocar_efeito("coracao.mp3", True)
                                        
                                        input(">> Pressione Enter para continuar...")
                                        
                                        # CORREÇÃO: Paramos só o coração, não a música
                                        # 1. Toca a reação (Voz)
                                        audio.falar(reacao.replace('"', ''))
                                        
                                        # 2. CONTROLE DO CORAÇÃO (AQUI ESTA A CORREÇÃO)
                                        som_cardiaco = None # Cria a variável vazia antes
                                        
                                        if ficou_nervoso:
                                            # Guarda o som na variável para poder parar depois
                                            som_cardiaco = media.tocar_efeito("coracao.mp3", loop=True)
                                        
                                        input(f"\n{Cor.AMARELO}>> Pressione Enter para acalmar o suspeito...{Cor.RESET}")
                                        
                                        # 3. PARAR O CORAÇÃO E VOLTAR A MÚSICA
                                        if som_cardiaco:
                                            som_cardiaco.stop() # Para só o coração
                                        
                                        # Garante que a música de fundo continua tocando
                                        # (Se ela tiver parado, isso religa)
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
                    nome_video = alvo.get('video', 'padrao.mp4')
                    print(f"{Cor.AZUL_CYBER}>> CARREGANDO PERFIL VISUAL...{Cor.RESET}")
                    
                    media.tocar_video_hacker(nome_video, "suspense.mp3")
                    
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
            
            # Sorteia se acha pista boa ou lixo
            if random.random() < 0.6: # 60% de chance de pista boa
                item = random.choice(detalhes['pistas_relevantes'])
                tipo = "EVIDÊNCIA CRÍTICA"
                cor = Cor.AMARELO
            else:
                item = random.choice(PISTAS_IRRELEVANTES)
                tipo = "SUCATA/LIXO"
                cor = Cor.CINZA
            
            if som_drone: som_drone.stop()
            
            # --- AQUI GUARDA NO INVENTÁRIO ---
            novo = inv.adicionar_item(item)
            msg_sistema = "ITEM ADICIONADO AO INVENTÁRIO" if novo else "ITEM JÁ POSSUÍDO"
            
            painel(f"SCANNER: {tipo}", [f"Objeto: {item}", f"STATUS: {msg_sistema}"], cor)
            audio.falar(f"Encontrei {item}. Guardando no inventário.")
            input("[ENTER]")

        elif op == '4':
            if os.path.exists("campainha.mp3"): media.tocar_efeito("campainha.mp3")
            digitar(">> Dona Neide atende a porta...", 0.03)
            fofoca, _ = neide.fofocar()
            painel("DONA NEIDE", fofoca, Cor.ROXO)
            audio.falar(fofoca)
            input("[ENTER]")

        elif op == '5':
            # --- ACUSAÇÃO FINAL (Versão Corrigida) ---
            digitar(f"{Cor.VERMELHO}>> INICIANDO PROTOCOLO FINAL...{Cor.RESET}")
            media.parar_ambiente()
            
            print(f"{Cor.AMARELO}>> EXECUTANDO VÍDEO...{Cor.RESET}")
            media.tocar_video_hacker("hack.mp4") 
            
            print(f"\n{Cor.BRANCO}========================================{Cor.RESET}")
            input(f"{Cor.VERMELHO_SANGUE}>> PRESSIONE [ENTER] PARA ACUSAR...{Cor.RESET}")
            
            limpar_tela(); logo_profissional()
            media.tocar_efeito("alarme.mp3", loop=True)
            
            print(f"\n{Cor.VERMELHO_SANGUE}>> SISTEMA COMPROMETIDO <<{Cor.RESET}")
            
            try:
                # FASE 1: ASSASSINO
                lista = [f"[{i+1}] {s['nome']} ({s['visual']})" for i,s in enumerate(suspeitos)]
                painel("PASSO 1/2: QUEM É O ASSASSINO?", lista, Cor.VERMELHO)
                
                # VOZ EM THREAD
                def narrar_acusacao(): audio.falar("Identifique o assassino e a arma.")
                threading.Thread(target=narrar_acusacao).start()

                esc_susp = int(input(f"{Cor.VERMELHO}NÚMERO DO CULPADO >> {Cor.RESET}")) - 1
                
                # FASE 2: ARMA
                todas_armas = [c['arma'] for c in CRIMES_DB]
                random.shuffle(todas_armas)
                limpar_tela(); logo_profissional()
                painel("PASSO 2/2: QUAL FOI A ARMA?", [f"[{i+1}] {a}" for i,a in enumerate(todas_armas)], Cor.VERMELHO)
                
                esc_arma_idx = int(input(f"{Cor.VERMELHO}NÚMERO DA ARMA >> {Cor.RESET}")) - 1
                arma_escolhida = todas_armas[esc_arma_idx]

                media.parar_ambiente() 
                barra_carregamento("PROCESSANDO SENTENÇA")

                acertos = 0
                if suspeitos[esc_susp] == culpado: acertos += 1
                if arma_escolhida == detalhes['arma_real']: acertos += 1
                
                if acertos == 2:
                    media.tocar_efeito("win.mp3")
                    painel("SUCESSO", "CULPADO PRESO E ARMA RECUPERADA.", Cor.VERDE_NEON)
                    audio.falar("Vitória. Caso encerrado.")
                    break 
                else:
                    media.tocar_efeito("fail.mp3")
                    painel("FALHA", "ERRO NA DEDUÇÃO. O CRIMINOSO ESCAPOU.", Cor.VERMELHO)
                    audio.falar("Fracasso total.")
                    break

            except Exception as e:
                media.parar_ambiente(); media.tocar_ambiente("login.mp3")
                print(f"{Cor.VERMELHO}>> ERRO DE ENTRADA: {e}{Cor.RESET}"); time.sleep(2)

        elif op == '6': break

if __name__ == "__main__":
    menu()
    