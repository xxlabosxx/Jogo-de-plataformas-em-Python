import pgzrun
import random
from pygame import Rect

WIDTH, HEIGHT = 800, 600
TITLE = "Platform Game"

# =============================================================================
# CONFIGURAÇÕES DE HITBOX
# =============================================================================

PLATFORM_HITBOX = {
    "vertical_offset": 0,
    "height": 15,
    "lateral_offset": 0,
    "global_x_offset": 0,
}

HERO_HITBOX = {
    "width": 20,
    "height": 20,
    "offset_x": (10 - 30) // 2,
    "offset_y": 20 - 20,
}

ENEMY_HITBOX = {
    "width": 20,
    "height": 20,
    "offset_x": (10 - 30) // 2,
    "offset_y": 20 - 20,
}

# =============================================================================
# SISTEMA DE ANIMAÇÃO - HERÓI
# =============================================================================

class SpriteAnimation:
    def __init__(self):
        self.current_animation = "idle"
        self.frame_index = 0
        self.animation_timer = 0
        self.facing_right = True

        self.animations = {
            "idle": {
                "right": ["idle_frame0", "idle_frame1", "idle_frame2", "idle_frame3", "idle_frame4", "idle_frame5"],
                "left": ["idle_frame0b", "idle_frame1b", "idle_frame2b", "idle_frame3b", "idle_frame4b", "idle_frame5b"],
                "speed": 10,
            },
            "walk": {
                "right": ["walk_frame0", "walk_frame1", "walk_frame2", "walk_frame3", "walk_frame4", "walk_frame5"],
                "left": ["walk_frame0b", "walk_frame1b", "walk_frame2b", "walk_frame3b", "walk_frame4b", "walk_frame5b"],
                "speed": 6,
            }
        }

        for anim_data in self.animations.values():
            anim_data["right"] = [frame.lower() for frame in anim_data["right"]]
            anim_data["left"] = [frame.lower() for frame in anim_data["left"]]

    def update(self, is_moving=False):
        self.animation_timer += 1

        new_animation = "walk" if is_moving else "idle"

        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.frame_index = 0
            self.animation_timer = 0

        animation_data = self.animations[self.current_animation]
        frames = animation_data["right"] if self.facing_right else animation_data["left"]

        if len(frames) > 1 and self.animation_timer >= animation_data["speed"]:
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.animation_timer = 0

    def get_current_frame(self):
        animation_data = self.animations[self.current_animation]
        frames = animation_data["right"] if self.facing_right else animation_data["left"]

        if not frames:
            frames = animation_data["right"]

        if self.frame_index >= len(frames):
            self.frame_index = 0

        frame_name = frames[self.frame_index]

        if frame_name.endswith('b') and not self.image_exists(frame_name):
            return frame_name.replace('b', '')
        elif not self.image_exists(frame_name):
            return "idle_frame0"

        return frame_name

    def image_exists(self, image_name):
        try:
            Actor(image_name)
            return True
        except:
            return False

    def set_direction(self, facing_right):
        self.facing_right = facing_right

# =============================================================================
# SISTEMA DE ANIMAÇÃO - INIMIGO
# =============================================================================

class EnemySpriteAnimation:
    def __init__(self):
        self.current_animation = "idle"
        self.frame_index = 0
        self.animation_timer = 0
        self.facing_right = False

        self.animations = {
            "idle": {
                "right": ["enemy_idle0", "enemy_idle1", "enemy_idle2", "enemy_idle3", "enemy_idle4", "enemy_idle5", "enemy_idle6"],
                "left": ["enemy_idle0b", "enemy_idle1b", "enemy_idle2b", "enemy_idle3b", "enemy_idle4b", "enemy_idle5b", "enemy_idle6b"],
                "speed": 8,
            },
            "run": {
                "right": ["enemy_run0", "enemy_run1", "enemy_run2", "enemy_run3", "enemy_run4", "enemy_run5"],
                "left": ["enemy_run0b", "enemy_run1b", "enemy_run2b", "enemy_run3b", "enemy_run4b", "enemy_run5b"],
                "speed": 6,
            }
        }

        for anim_data in self.animations.values():
            anim_data["right"] = [frame.lower() for frame in anim_data["right"]]
            anim_data["left"] = [frame.lower() for frame in anim_data["left"]]

    def update(self, is_moving=False):
        self.animation_timer += 1

        new_animation = "run" if is_moving else "idle"

        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.frame_index = 0
            self.animation_timer = 0

        animation_data = self.animations[self.current_animation]
        frames = animation_data["right"] if self.facing_right else animation_data["left"]

        if len(frames) > 1 and self.animation_timer >= animation_data["speed"]:
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.animation_timer = 0

    def get_current_frame(self):
        animation_data = self.animations[self.current_animation]
        frames = animation_data["right"] if self.facing_right else animation_data["left"]

        if not frames:
            frames = animation_data["right"]

        if self.frame_index >= len(frames):
            self.frame_index = 0

        frame_name = frames[self.frame_index]

        if frame_name.endswith('b') and not self.image_exists(frame_name):
            return frame_name.replace('b', '')
        elif not self.image_exists(frame_name):
            return "enemy_idle0"

        return frame_name

    def image_exists(self, image_name):
        try:
            Actor(image_name)
            return True
        except:
            return False

    def set_direction(self, facing_right):
        self.facing_right = facing_right

# =============================================================================
# CONFIGURAÇÕES GLOBAIS
# =============================================================================

game_state = "menu"
music_enabled = True
music_playing = False
music_check_timer = 0

hero = Actor("idle_frame0", (100, 500))
hero_sprite = SpriteAnimation()
hero.velocity_y = 0
hero.on_ground = False

hero.hitbox_width = HERO_HITBOX["width"]
hero.hitbox_height = HERO_HITBOX["height"]
hero.offset_x = HERO_HITBOX["offset_x"]
hero.offset_y = HERO_HITBOX["offset_y"]

platforms = []
enemies = []
buttons = {"menu": [], "game_over": [], "victory": []}
victory_point = None
victory_collected = False

# =============================================================================
# SISTEMA DE ÁUDIO
# =============================================================================

def toggle_music():
    global music_enabled, music_playing
    music_enabled = not music_enabled
    if music_enabled:
        play_background_music()
    else:
        stop_background_music()
    update_button_texts()

def play_sound(sound_name):
    try:
        if hasattr(sounds, sound_name):
            getattr(sounds, sound_name).play()
    except:
        pass

def play_background_music():
    global music_playing
    stop_background_music()
    if music_enabled:
        try:
            sounds.music.play()
            music_playing = True
        except:
            music_playing = False

def stop_background_music():
    global music_playing
    try:
        sounds.music.stop()
        music_playing = False
    except:
        music_playing = False

def check_music_loop():
    global music_playing, music_check_timer
    music_check_timer += 1
    if music_check_timer < 60:
        return
    music_check_timer = 0
    if music_enabled:
        try:
            if not sounds.music.get_busy() and music_playing:
                music_playing = False
                play_background_music()
        except:
            pass

# =============================================================================
# SISTEMA DE PLATAFORMAS
# =============================================================================

def generate_platforms():
    global platforms, victory_point, victory_collected
    platforms = []
    victory_collected = False

    platforms.append((0, 550, WIDTH, 50))
    top_platform = (WIDTH // 2 - 40, 80, 160, 15)
    platforms.append(top_platform)

    num_platforms = random.randint(10, 15)
    create_vertical_path()

    platforms_added = 0
    attempts = 0

    while platforms_added < num_platforms and attempts < 50:
        attempts += 1
        platform_width = random.randint(70, 130)
        pos_x = random.randint(50, WIDTH - platform_width - 50)
        pos_y = random.randint(120, 450)

        too_close = False
        for plat_x, plat_y, plat_l, plat_a in platforms:
            distance_x = abs((pos_x + platform_width / 2) - (plat_x + plat_l / 2))
            distance_y = abs((pos_y + 15 / 2) - (plat_y + plat_a / 2))
            if distance_x < 100 and distance_y < 80:
                too_close = True
                break

        if not too_close:
            platforms.append((pos_x, pos_y, platform_width, 15))
            platforms_added += 1

    try:
        victory_point = Actor("coin", (top_platform[0] + top_platform[2] // 2, top_platform[1] - 25))
    except:
        victory_point = None

def create_vertical_path():
    current_height = 500
    current_x = WIDTH // 2

    while current_height > 120:
        current_height -= random.randint(80, 120)
        if current_height < 120:
            current_height = 120

        current_x = random.choice([random.randint(100, 350), random.randint(450, 700)])
        path_width = random.randint(90, 150)

        if current_x + path_width > WIDTH - 30:
            current_x = WIDTH - path_width - 30
        if current_x < 30:
            current_x = 30

        platforms.append((current_x, current_height, path_width, 15))

def get_hero_hitbox():
    return Rect(
        hero.x + hero.offset_x,
        hero.y + hero.offset_y,
        hero.hitbox_width,
        hero.hitbox_height
    )

def get_enemy_hitbox(enemy):
    return Rect(
        enemy.x + enemy.offset_x,
        enemy.y + enemy.offset_y,
        enemy.hitbox_width,
        enemy.hitbox_height
    )

def get_platform_hitbox(px, py, pl, pa):
    return Rect(
        px + PLATFORM_HITBOX["lateral_offset"] + PLATFORM_HITBOX["global_x_offset"],
        py + PLATFORM_HITBOX["vertical_offset"],
        pl - (PLATFORM_HITBOX["lateral_offset"] * 2),
        PLATFORM_HITBOX["height"]
    )

def check_platform_collision():
    hero_hitbox = get_hero_hitbox()
    hero.on_ground = False

    for px, py, pl, pa in platforms:
        platform_rect = get_platform_hitbox(px, py, pl, pa)

        if not hero_hitbox.colliderect(platform_rect):
            continue

        if (hero.velocity_y >= 0 and
            hero_hitbox.bottom >= platform_rect.top and
            hero_hitbox.bottom <= platform_rect.top + 15):
            hero.y = platform_rect.top - hero.hitbox_height - hero.offset_y
            hero.velocity_y = 0
            hero.on_ground = True
            break

        if (hero.velocity_y < 0 and
            hero_hitbox.top <= platform_rect.bottom and
            hero_hitbox.top >= platform_rect.bottom - 15):
            hero.y = platform_rect.bottom - hero.offset_y
            hero.velocity_y = 0
            break

        if (hero_hitbox.right >= platform_rect.left and
            hero_hitbox.right <= platform_rect.left + 10 and
            hero_hitbox.bottom > platform_rect.top and
            hero_hitbox.top < platform_rect.bottom):
            hero.x = platform_rect.left - hero.hitbox_width - hero.offset_x
            break

        if (hero_hitbox.left <= platform_rect.right and
            hero_hitbox.left >= platform_rect.right - 10 and
            hero_hitbox.bottom > platform_rect.top and
            hero_hitbox.top < platform_rect.bottom):
            hero.x = platform_rect.right - hero.offset_x
            break

# =============================================================================
# SISTEMA DO HERÓI
# =============================================================================

def update_hero():
    global game_state, victory_collected

    movement_x = 0
    if keyboard.A or keyboard.LEFT:
        movement_x -= 5
        hero_sprite.set_direction(False)
    if keyboard.D or keyboard.RIGHT:
        movement_x += 5
        hero_sprite.set_direction(True)

    hero.x += movement_x
    check_platform_collision()

    hero.velocity_y += 0.6
    hero.y += hero.velocity_y
    check_platform_collision()

    if keyboard.SPACE and hero.on_ground:
        hero.velocity_y = -14
        hero.on_ground = False
        play_sound("jump")

    if victory_point and hero.colliderect(victory_point) and not victory_collected:
        victory_collected = True
        game_state = "victory"

    if hero.y > HEIGHT + 100:
        hero.pos = (100, 500)
        hero.velocity_y = 0
        hero.on_ground = False

    hitbox = get_hero_hitbox()
    if hitbox.left < 0:
        hero.x = -hero.offset_x
    if hitbox.right > WIDTH:
        hero.x = WIDTH - hero.hitbox_width - hero.offset_x

    is_moving = movement_x != 0
    hero_sprite.update(is_moving)

    try:
        new_frame = hero_sprite.get_current_frame()
        new_frame = new_frame.lower()
        hero.image = new_frame
    except:
        hero.image = "idle_frame0"

# =============================================================================
# SISTEMA DE INIMIGOS
# =============================================================================

def create_enemies():
    enemies.clear()
    try:
        test_enemy = Actor("enemy_idle0")
        for _ in range(3):
            valid_platforms = [p for p in platforms[1:] if p[1] > 200]
            if valid_platforms:
                px, py, pl, pa = random.choice(valid_platforms)
                x = random.randint(px + 25, px + pl - 25)
                y = py - 20
                enemy = Actor("enemy_idle0", (x, y))

                enemy.hitbox_width = ENEMY_HITBOX["width"]
                enemy.hitbox_height = ENEMY_HITBOX["height"]
                enemy.offset_x = ENEMY_HITBOX["offset_x"]
                enemy.offset_y = ENEMY_HITBOX["offset_y"]

                enemy.sprite = EnemySpriteAnimation()
                enemy.home_platform = (px, py, pl, pa)
                enemy.ai_state = random.choice(["patrol", "idle"])
                enemy.ai_timer = random.randint(60, 120)
                enemy.speed = random.uniform(1.0, 1.8)
                enemy.direction = random.choice([-1, 1])
                enemies.append(enemy)
    except:
        enemies.clear()

def update_enemies():
    for enemy in enemies:
        enemy.ai_timer -= 1
        if enemy.ai_timer <= 0:
            enemy.ai_state = random.choice(["patrol", "idle"])
            enemy.ai_timer = random.randint(60, 120)
            enemy.direction = random.choice([-1, 1])

        px, py, pl, pa = enemy.home_platform
        if enemy.ai_state == "patrol":
            enemy.x += enemy.direction * enemy.speed
            if enemy.x < px + 20 or enemy.x > px + pl - 20:
                enemy.direction *= -1

        enemy.x = max(px + 20, min(enemy.x, px + pl - 20))
        enemy.y = py - 20

        enemy.sprite.set_direction(enemy.direction > 0)
        is_moving = enemy.ai_state == "patrol"
        enemy.sprite.update(is_moving)

        try:
            new_frame = enemy.sprite.get_current_frame()
            new_frame = new_frame.lower()
            enemy.image = new_frame
        except:
            enemy.image = "enemy_idle0"

def check_enemy_collisions():
    hero_hitbox = get_hero_hitbox()
    for enemy in enemies:
        enemy_hitbox = get_enemy_hitbox(enemy)
        if hero_hitbox.colliderect(enemy_hitbox):
            play_sound("hit")
            return True
    return False

# =============================================================================
# INTERFACE DO USUÁRIO
# =============================================================================

def create_buttons():
    buttons["menu"] = [
        {"text": "Começar jogo (S)", "action": "start", "rect": Rect(300, 220, 200, 40)},
        {"text": f" Música (T): {'ON' if music_enabled else 'OFF'}", "action": "toggle_music", "rect": Rect(300, 270, 200, 40)},
        {"text": "Sair do jogo (Q)", "action": "quit", "rect": Rect(300, 320, 200, 40)}
    ]
    buttons["game_over"] = [
        {"text": "Recomeçar jogo (R)", "action": "restart", "rect": Rect(300, 250, 200, 40)},
        {"text": "Menu principal (M)", "action": "menu", "rect": Rect(300, 300, 200, 40)},
        {"text": "Sair do jogo (Q)", "action": "quit", "rect": Rect(300, 350, 200, 40)}
    ]
    buttons["victory"] = [
        {"text": "Jogue denovo (R)", "action": "restart", "rect": Rect(300, 280, 200, 40)},
        {"text": "Menu principal (M)", "action": "menu", "rect": Rect(300, 330, 200, 40)},
        {"text": "Sair do jogo (Q)", "action": "quit", "rect": Rect(300, 380, 200, 40)}
    ]

def update_button_texts():
    status = "ON" if music_enabled else "OFF"
    for button in buttons["menu"]:
        if button["action"] == "toggle_music":
            button["text"] = f"Music: {status}"

def draw_button(button, with_hover=False):
    rect = button["rect"]
    color = (100, 180, 255) if with_hover else (70, 130, 230)
    screen.draw.filled_rect(rect, color)
    screen.draw.rect(rect, (255, 255, 255))
    screen.draw.text(button["text"], center=(rect.x + rect.width / 2, rect.y + rect.height / 2), fontsize=20, color="white")

def check_button_click(pos, button_list):
    for button in button_list:
        if button["rect"].collidepoint(pos):
            execute_button_action(button["action"])
            return True
    return False

def check_button_hover(pos, button_list):
    for button in button_list:
        button["hover"] = button["rect"].collidepoint(pos)

def execute_button_action(action):
    global game_state
    if action == "start" or action == "restart":
        restart_game()
    elif action == "toggle_music":
        toggle_music()
    elif action == "menu":
        game_state = "menu"
    elif action == "quit":
        exit()

def draw_menu():
    try:
        screen.blit("bg", (0, 0))
    except:
        screen.fill((50, 100, 150))
    screen.draw.text("Super Jogo de Plataforma", center=(WIDTH // 2, 80), fontsize=48, color="white")
    screen.draw.text("Chegue no topo e pegue a moeda", center=(WIDTH // 2, 140), fontsize=28, color="yellow")
    screen.draw.text("Use A/D para mover e Espaço para pular", center=(WIDTH // 2, 180), fontsize=18, color="lightblue")
    for button in buttons["menu"]:
        draw_button(button, button.get("hover", False))

def draw_game_over():
    screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0, 180))
    screen.draw.text("GAME OVER", center=(400, 150), fontsize=56, color="red")
    screen.draw.text("Você foi derrotado", center=(400, 200), fontsize=24, color="white")
    for button in buttons["game_over"]:
        draw_button(button, button.get("hover", False))

def draw_victory():
    screen.fill((50, 180, 50))
    screen.draw.text("Vitória", center=(400, 150), fontsize=56, color="gold")
    screen.draw.text("Parabéns, você ganhou", center=(400, 200), fontsize=24, color="white")
    for button in buttons["victory"]:
        draw_button(button, button.get("hover", False))

# =============================================================================
# CONTROLES E EVENTOS
# =============================================================================

def on_key_down(key):
    global game_state
    if key == keys.R:
        restart_game()
    elif key == keys.Q:
        exit()
    elif game_state == "menu" and key == keys.S:
        restart_game()
    elif key == keys.M:
        game_state = "menu"
    elif key == keys.T:
        toggle_music()

def on_mouse_down(pos):
    states = {"menu": buttons["menu"], "game_over": buttons["game_over"], "victory": buttons["victory"]}
    if game_state in states:
        check_button_click(pos, states[game_state])

def on_mouse_move(pos):
    states = {"menu": buttons["menu"], "game_over": buttons["game_over"], "victory": buttons["victory"]}
    if game_state in states:
        check_button_hover(pos, states[game_state])

# =============================================================================
# LOOP PRINCIPAL DO JOGO
# =============================================================================

def restart_game():
    global game_state
    hero.pos = (100, 500)
    hero.velocity_y = 0
    hero.on_ground = False
    generate_platforms()
    create_enemies()
    game_state = "playing"
    if music_enabled:
        play_background_music()

def update():
    global game_state
    check_music_loop()
    if game_state == "menu":
        update_button_texts()
    elif game_state == "playing":
        update_hero()
        update_enemies()
        if check_enemy_collisions():
            game_state = "game_over"

def draw():
    screen.clear()

    if game_state == "menu":
        try:
            screen.blit("bg", (0, 0))
        except:
            screen.fill((50, 100, 150))

        screen.draw.text("Super Jogo de Plataforma", center=(WIDTH // 2, 80), fontsize=48, color="white")
        screen.draw.text("Chegue ao topo e pegue a moeda para ganhar", center=(WIDTH // 2, 140), fontsize=28, color="yellow")
        screen.draw.text("Use A/D para andar e Espaço para pular", center=(WIDTH // 2, 180), fontsize=18, color="lightblue")

        for button in buttons["menu"]:
            draw_button(button, button.get("hover", False))

    elif game_state == "playing":
        try:
            screen.blit("bg", (0, 0))
        except:
            screen.fill((135, 206, 235))

        rainbow_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
        for i, (px, py, pl, pa) in enumerate(platforms):
            screen.draw.filled_rect(Rect((px, py), (pl, pa)), rainbow_colors[i % len(rainbow_colors)])

        if victory_point and not victory_collected:
            victory_point.draw()

        for enemy in enemies:
            enemy.draw()

        hero.draw()

        screen.draw.text("A/D: Mover", (10, 10), color="white", fontsize=16)
        screen.draw.text("Espaço: Pular", (10, 35), color="white", fontsize=16)
        screen.draw.text("T: Música", (10, 60), color="white", fontsize=16)
        screen.draw.text("R: Reiniciar", (10, 85), color="white", fontsize=16)
        screen.draw.text("Q: Sair", (10, 110), color="white", fontsize=16)
        screen.draw.text("M: Menu", (10, 135), color="white", fontsize=16)
        screen.draw.text(f"Música: {'ON' if music_enabled else 'OFF'}", (10, 160), color="yellow" if music_enabled else "gray", fontsize=16)

    elif game_state == "game_over":
        try:
            screen.blit("bg", (0, 0))
        except:
            screen.fill((135, 206, 235))

        for px, py, pl, pa in platforms:
            screen.draw.filled_rect(Rect((px, py), (pl, pa)), (139, 69, 19))

        hero.draw()
        for enemy in enemies:
            enemy.draw()

        draw_game_over()

    elif game_state == "victory":
        draw_victory()

# =============================================================================
# INICIALIZAÇÃO
# =============================================================================

generate_platforms()
create_enemies()
create_buttons()
if music_enabled:
    play_background_music()

pgzrun.go()