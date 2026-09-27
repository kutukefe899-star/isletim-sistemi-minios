import sys
import subprocess
import os

# 1. Otomatik Kütüphane Kontrolü ve Yükleme
try:
    import pygame
except ImportError:
    print("⚠️ Pygame kütüphanesi bulunamadı. Otomatik olarak kuruluyor...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame", "--break-system-packages"])
        import pygame
        print("✅ Pygame başarıyla kuruldu!")
    except Exception as e:
        print(f"❌ Kurulum başarısız. Lütfen terminale şunu yazın:\npip install pygame --break-system-packages\nHata: {e}")
        sys.exit(1)

# 2. Grafik Ekran (X11/Wayland) Kontrolü
if "DISPLAY" not in os.environ:
    print("HATA: Grafik arayüzü (DISPLAY) algılanamadı. Lütfen masaüstü terminalinden çalıştırın.")
    sys.exit(1)

# Pygame Başlatma
pygame.init()

# Renkler
SKY_BLUE = (135, 206, 235)
MATRIX_SKY = (10, 25, 10)
GROUND_COLOR = (222, 184, 135)
GRASS_COLOR = (34, 139, 34)
BIRD_COLOR = (255, 215, 0)
PIPE_COLOR = (46, 139, 87)

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Düzeltilmiş Sürüm")
clock = pygame.time.Clock()

try:
    font = pygame.font.SysFont("DejaVu Sans", 28, bold=True)
    huge_font = pygame.font.SysFont("DejaVu Sans", 40, bold=True)
    small_font = pygame.font.SysFont("DejaVu Sans", 16, bold=True)
except:
    font = pygame.font.Font(None, 32)
    huge_font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 20)

def reset_game():
    return {"x": 80, "y": 300, "vel": 0, "gravity": 0.45, "jump": -8, "radius": 15}

def main():
    bird = reset_game()
    pipes = []
    
    PIPE_WIDTH = 70
    PIPE_GAP = 180       # Kuşun rahatça geçebileceği ideal dikey boşluk!
    PIPE_SPEED = 3
    SPAWN_TIME = 2000    # Boruların arası artık daha ferah ve dengeli
    
    LAST_PIPE = pygame.time.get_ticks()
    score = 0
    game_over = False
    
    click_count = 0
    last_click_time = 0
    easter_egg_active = False
    easter_egg_msg = ""
    msg_timer = 0
    
    # İlk boruyu güvenli bir yükseklikte başlat
    pipes.append({"x": WIDTH, "height": random.randint(100, 300), "passed": False})
    
    while True:
        is_matrix_mode = (score > 0 and score % 10 == 0)
        screen.fill(MATRIX_SKY if is_matrix_mode else SKY_BLUE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                current_time = pygame.time.get_ticks()
                if current_time - last_click_time < 400:
                    click_count += 1
                    if click_count >= 2:
                        easter_egg_active = not easter_egg_active
                        easter_egg_msg = "🌟 TURBO KUŞ AKTİF!" if easter_egg_active else "🌟 Turbo Kapatıldı"
                        msg_timer = current_time + 2000
                        click_count = 0
                else:
                    click_count = 0
                last_click_time = current_time

                if game_over:
                    bird = reset_game()
                    pipes.clear()
                    pipes.append({"x": WIDTH, "height": random.randint(100, 300), "passed": False})
                    score = 0
                    game_over = False
                    easter_egg_active = False
                else:
                    bird["vel"] = bird["jump"] - 2 if easter_egg_active else bird["jump"]

        if not game_over:
            current_pipe_speed = PIPE_SPEED + 1 if score >= 25 else PIPE_SPEED
            bird["vel"] += bird["gravity"]
            bird["y"] += bird["vel"]
            
            # Zemin ve tavan kontrolü
            if bird["y"] >= HEIGHT - 100 - bird["radius"]:
                bird["y"] = HEIGHT - 100 - bird["radius"]
                game_over = True
            if bird["y"] <= bird["radius"]:
                bird["y"] = bird["radius"]
                bird["vel"] = 0
                
            current_time = pygame.time.get_ticks()
            if current_time - LAST_PIPE > SPAWN_TIME:
                pipes.append({"x": WIDTH, "height": random.randint(100, 300), "passed": False})
                LAST_PIPE = current_time
                
            for pipe in pipes[:]:
                pipe["x"] -= current_pipe_speed
                
                if pipe["x"] < -PIPE_WIDTH:
                    pipes.remove(pipe)
                    
                if not pipe["passed"] and pipe["x"] + PIPE_WIDTH < bird["x"]:
                    score += 1
                    pipe["passed"] = True
                    if score == 10:
                        easter_egg_msg = "😎 10 Puan: Matrix Modu!"
                        msg_timer = pygame.time.get_ticks() + 2500
                    elif score == 25:
                        easter_egg_msg = "🔥 25 Puan: Hız Arttı!"
                        msg_timer = pygame.time.get_ticks() + 2500
                    
                # Boru Çarpışma Kutuları (Rect)
                top_rect = pygame.Rect(pipe["x"], 0, PIPE_WIDTH, pipe["height"])
                bot_y = pipe["height"] + PIPE_GAP
                bot_rect = pygame.Rect(pipe["x"], bot_y, PIPE_WIDTH, HEIGHT - bot_y - 100)
                
                bird_rect = pygame.Rect(bird["x"] - bird["radius"], bird["y"] - bird["radius"], bird["radius"] * 2, bird["radius"] * 2)
                
                if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bot_rect):
                    game_over = True

        # --- ÇİZİMLER ---
        active_pipe_color = (0, 255, 128) if is_matrix_mode else PIPE_COLOR
        
        for pipe in pipes:
            # Üst Boru
            pygame.draw.rect(screen, active_pipe_color, (pipe["x"], 0, PIPE_WIDTH, pipe["height"]))
            pygame.draw.rect(screen, (20, 100, 50), (pipe["x"] - 4, pipe["height"] - 24, PIPE_WIDTH + 8, 24))
            
            # Alt Boru
            bot_y = pipe["height"] + PIPE_GAP
            pygame.draw.rect(screen, active_pipe_color, (pipe["x"], bot_y, PIPE_WIDTH, HEIGHT - bot_y - 100))
            pygame.draw.rect(screen, (20, 100, 50), (pipe["x"] - 4, bot_y, PIPE_WIDTH + 8, 24))

        # Zemin
        pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - 100, WIDTH, 100))
        pygame.draw.rect(screen, (10, 150, 10) if is_matrix_mode else GRASS_COLOR, (0, HEIGHT - 100, WIDTH, 20))

        # Kuş
        current_bird_color = (255, 0, 255) if easter_egg_active else BIRD_COLOR
        pygame.draw.circle(screen, current_bird_color, (int(bird["x"]), int(bird["y"])), bird["radius"])
        pygame.draw.circle(screen, (0, 0, 0), (int(bird["x"] + 5), int(bird["y"] - 4)), 3)
        pygame.draw.polygon(screen, (0, 255, 0) if is_matrix_mode else (255, 140, 0), [
            (int(bird["x"] + bird["radius"]), int(bird["y"])),
            (int(bird["x"] + bird["radius"] + 8), int(bird["y"] - 2)),
            (int(bird["x"] + bird["radius"]), int(bird["y"] + 4))
        ])

        # Arayüz Metinleri
        score_surface = font.render(f"Skor: {score}", True, (0, 255, 0) if is_matrix_mode else (255, 255, 255))
        screen.blit(score_surface, (15, 15))

        if pygame.time.get_ticks() < msg_timer:
            msg_surf = small_font.render(easter_egg_msg, True, (255, 255, 0))
            screen.blit(msg_surf, (WIDTH // 2 - msg_surf.get_width() // 2, 60))

        if game_over:
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 140))
            screen.blit(s, (0, 0))
            over_text = huge_font.render("OYUN BİTTİ!", True, (255, 69, 0))
            restart_text = font.render("Yeniden Başlamak İçin Tıkla", True, (255, 255, 255))
            secret_hint = small_font.render("💡 İpucu: Hızlıca 3 kez tıkla!", True, (200, 200, 200))
            screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 60))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 10))
            screen.blit(secret_hint, (WIDTH//2 - secret_hint.get_width()//2, HEIGHT//2 + 60))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    import random
    main()
