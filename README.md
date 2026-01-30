🕵️‍♂️ CSI PRO: SYSTEM v15.2
"Não existe crime perfeito, apenas investigações incompletas."

🚨 Sobre o Jogo
CSI PRO é um simulador de investigação criminal de Alta Fidelidade que roda diretamente no seu terminal, mas com uma reviravolta imersiva: ele utiliza Dual-Screen Technology (Janela de Vigilância CCTV + Terminal de Comando).

Assuma o papel de um Agente Especial encarregado de resolver homicídios complexos gerados proceduralmente. Você tem tempo limitado antes que a imprensa destrua a reputação da polícia.

Use drones, hackeie câmeras, interrogue suspeitos e combine evidências químicas no laboratório para pegar o assassino.

🎮 Funcionalidades Principais
👁️ Sistema OMNI-VIEW (Imersão Total)
O jogo não se limita ao texto. Uma segunda janela se abre simulando um monitor de segurança real, exibindo feeds de câmeras, estática e dados em tempo real enquanto você digita os comandos.

🚁 Arsenal Tecnológico
Drone Forense: Varra a cena do crime em busca de itens físicos e digitais.

Hacking de CFTV: Quebre a criptografia do servidor para recuperar imagens do momento do crime.

Laboratório de Crafting: Combine itens (ex: Celular Bloqueado + Senha) para revelar segredos obscuros e reviravoltas na trama.

🧠 Inteligência Artificial de Suspeitos
Sistema de Pressão: Cada suspeito reage diferente. Pressione demais e eles podem entrar em pânico ou se fechar.

Álibis Dinâmicos: Verifique se a história deles bate com as provas.

Dona Neide (HUMINT): A vizinha fofoqueira que sabe de tudo. Ela fornece dicas visuais cruciais e itens escondidos.

📰 Mundo Vivo
Manchetes Dinâmicas: A cada ação sua, o tempo passa. Se demorar, o jornal local começa a criticar a polícia, aumentando a tensão.

Crimes Aleatórios: A vítima, o local, a arma e o culpado mudam a cada partida.

🛠️ Como Jogar (O Protocolo)
Sua missão é identificar QUEM matou e QUAL arma foi usada.

Colete Evidências: Use o Drone [3] para achar pistas físicas (balas, veneno, facas).

Perfil Visual: Hackeie Câmeras [2] ou visite a Dona Neide [4] para descobrir a roupa do assassino.

Interrogatório: Pressione os suspeitos na Opção [1]. Veja quem fica nervoso ao ver as provas.

Laboratório [5]: Descobriu um Cofre e uma Chave? Vá ao laboratório combiná-los para descobrir o motivo do crime.

Acusação Final [6]: Junte as peças. Você tem 2 chances para acertar o Culpado e a Arma.

📸 Screenshots
(Aqui você pode colocar prints do jogo rodando, mostrando o terminal colorido e a janela do vídeo)

🚀 Instalação e Requisitos
Este sistema requer Python 3.x e algumas bibliotecas de elite.

Clone o repositório:

Bash
git clone https://github.com/Lucasssouza527/jogocsiwindows
cd CSI-PRO
Instale as dependências:

Bash
pip install opencv-python pygame edge-tts pyautogui pywhatkit
Inicie a Operação:

Bash
python jogocsi.py
📂 Estrutura de Arquivos
Para o sistema funcionar, a estrutura deve ser mantida:

CSI-PRO/
│
├── jogocsi.py          # O Núcleo do Sistema
├── agentes_csi.json    # Banco de Dados (Save)
└── assets/             # Arquivos de Mídia
    ├── audio/          # Efeitos sonoros (win.mp3, drone.mp3...)
    └── video/          # Loops de vídeo (hack.mp4, camera1.mp4...)
👨‍💻 Autor
Desenvolvido por Lucas souza . Sistema v15.2 - 
