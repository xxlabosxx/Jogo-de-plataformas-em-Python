🚀**Jogo de plataforma em Python**🚀
Um jogo de plataforma 2D clássico desenvolvido em Python utilizando a biblioteca Pygame Zero. O projeto foca na implementação de lógica de física, sistemas de animação baseados em estados e geração procedural de elementos de cenário.

**Tecnologias e Conceitos Utilizados**
Linguagem: Python 3.x.

Framework: Pygame Zero (pgzero).

POO (Programação Orientada a Objetos): Classes personalizadas para gerenciamento de animações do herói e dos inimigos.

**Sistemas de Jogo:**

Física: Implementação de gravidade, aceleração vertical e detecção de colisões com múltiplas superfícies.

Geração Procedural: Algoritmo que cria plataformas e caminhos verticais aleatórios a cada nova partida.

IA de Patrulha: Inimigos com lógica de movimento autônomo vinculada às plataformas de origem.

Gerenciamento de Estados: Transições entre Menu, Gameplay, Game Over e Vitória.

**Mecânicas do Jogo**
O objetivo é simples: escalar as plataformas geradas aleatoriamente até alcançar a Moeda de Ouro no topo do mapa, evitando o contato com os inimigos que patrulham o caminho.

Controles
A / D ou Setas: Mover para esquerda e direita.

Espaço: Pular.

T: Ligar/Desligar música.

R: Reiniciar partida.

M: Voltar ao menu principal.

Q / Esc: Sair do jogo.

**Como Executar o Projeto**
Para rodar este jogo em sua máquina local, siga os passos abaixo:

1. Pré-requisitos
Certifique-se de ter o Python instalado. Você também precisará da biblioteca pgzero.

2. Instalação
Abra o seu terminal e instale a dependência necessária:

Bash
pip install pgzero

3. Estrutura de Pastas
Para que o jogo funcione corretamente, os assets (imagens e sons) devem estar organizados da seguinte forma:

Plaintext
pasta_do_projeto/
│
├── jogo.py              # O arquivo de código fornecido
├── images/              # Pasta com os sprites (.png)
│   ├── idle_frame0.png, walk_frame0.png, coin.png, etc.
└── sounds/              # Pasta com os arquivos de áudio (.wav ou .ogg)
    ├── jump.wav, hit.wav, music.ogg, etc.
    
4. Execução
Com o terminal aberto na pasta do projeto, execute o comando:

Bash
pgzrun jogo.py

Organização do Código
SpriteAnimation: Gerencia a troca de frames do jogador, garantindo fluidez visual e espelhamento (flip) conforme a direção do movimento.

generate_platforms: Função responsável por calcular posições válidas para as plataformas, garantindo que o topo seja alcançável.

update_hero & update_enemies: Loops de processamento que lidam com a movimentação e as regras de negócio em tempo real.

📝 **Licença**
Este projeto foi desenvolvido para fins de estudo e prática de desenvolvimento de jogos em Python. Sinta-se à vontade para clonar e modificar!
Este projeto foi desenvolvido para fins de estudo e prática de desenvolvimento de jogos em Python. Sinta-se à vontade para clonar e modificar!

Desenvolvido por Gustavo. 👨‍💻
