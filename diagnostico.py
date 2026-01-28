import os
import time

print("--- 🔊 TESTE DE ÁUDIO CSI ---")

# 1. Tenta Gerar
print("[1] Gerando voz do narrador...")
res_gerar = os.system('edge-tts --voice pt-BR-AntonioNeural --text "Sistema de áudio online. O jogo está pronto." --write-media teste.mp3')

if res_gerar != 0:
    print("❌ FALHA AO GERAR! Tente rodar: pip install edge-tts")
    exit()
else:
    print("✅ Arquivo de áudio criado!")

# 2. Tenta Tocar
print("[2] Tentando tocar...")
if os.path.exists("/usr/bin/cvlc") or os.path.exists("/usr/bin/vlc"):
    # Tenta tocar sem abrir janela (--nodisplay)
    os.system("cvlc --play-and-exit --nodisplay teste.mp3")
    print("✅ Comando enviado ao VLC!")
else:
    print("❌ VLC NÃO ENCONTRADO! Rode: sudo apt install vlc")
