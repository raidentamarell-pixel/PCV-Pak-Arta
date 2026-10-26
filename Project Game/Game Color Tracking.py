import os
import random
import cv2
import numpy as np
import pygame

folder = os.path.dirname(os.path.abspath(__file__))

kamera = cv2.VideoCapture(0)
ok, frame = kamera.read()
tinggi_asli, lebar_asli = frame.shape[:2]
LEBAR = 800
TINGGI = LEBAR * tinggi_asli // lebar_asli

# Nilai HSV
BIRU_BAWAH = np.array([33, 49, 163])
BIRU_ATAS = np.array([82, 106, 255])

# Initiate pymgame display
pygame.init()
layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Tangkap Buah")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 30)

# gambar
def muat(nama, ukuran, warna):
    path = os.path.join(folder, nama)
    if os.path.exists(path):
        return pygame.transform.scale(pygame.image.load(path).convert_alpha(), ukuran)
    print("File tidak ada:", nama)
    gambar = pygame.Surface(ukuran, pygame.SRCALPHA)
    pygame.draw.ellipse(gambar, warna, (0, 0, *ukuran))
    return gambar

# Cari image
daftar_buah = [
    muat("apple.png", (60, 60), (220, 40, 40)),
    muat("banana.png", (70, 70), (250, 220, 50)),
    muat("kiwi.png", (60, 70), (110, 170, 60)),
]
gambar_bom = muat("bomb.png", (70, 70), (40, 40, 40))

KERANJANG_LEBAR = 150
gambar_keranjang = muat("basket.png", (KERANJANG_LEBAR, 80), (150, 100, 50))
keranjang_x = LEBAR // 2
keranjang_y = TINGGI - 100

items = []  # [x, y, gambar, bom?]
skor = 0
nyawa = 3
timer = 0
game_over = False

jalan = True
while jalan:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jalan = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                jalan = False
            if event.key == pygame.K_r:
                items, skor, nyawa, game_over = [], 0, 3, False

    ok, frame = kamera.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (LEBAR, TINGGI))

    hsv = cv2.cvtColor(cv2.GaussianBlur(frame, (11, 11), 0), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, BIRU_BAWAH, BIRU_ATAS)
    kontur, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if kontur:
        terbesar = max(kontur, key=cv2.contourArea)
        if cv2.contourArea(terbesar) > 500:
            x, y, w, h = cv2.boundingRect(terbesar)
            keranjang_x = x + w // 2

    if not game_over:
        timer += 1
        if timer > 40:
            bom = random.random() < 0.2
            gambar = gambar_bom if bom else random.choice(daftar_buah)
            items.append([random.randint(30, LEBAR - 30), 0, gambar, bom])
            timer = 0

        for item in items[:]:
            item[1] += 5

            masuk = (keranjang_y <= item[1] <= keranjang_y + 40
                     and abs(item[0] - keranjang_x) <= KERANJANG_LEBAR // 2)

            if masuk:
                items.remove(item)
                if item[3]:
                    nyawa -= 1
                else:
                    skor += 1
            elif item[1] > TINGGI:
                items.remove(item)
                if not item[3]:  # bom lolos aman
                    nyawa -= 1

        if nyawa <= 0:
            game_over = True

    terang = cv2.convertScaleAbs(frame, alpha=1.15, beta=30)
    rgb = cv2.cvtColor(terang, cv2.COLOR_BGR2RGB)
    layar.blit(pygame.image.frombuffer(rgb.tobytes(), (LEBAR, TINGGI), "RGB"), (0, 0))

    for x, y, gambar, _ in items:
        layar.blit(gambar, (x - gambar.get_width() // 2, y - gambar.get_height() // 2))
    layar.blit(gambar_keranjang, (keranjang_x - KERANJANG_LEBAR // 2, keranjang_y))

    layar.blit(font.render(f"Skor: {skor}   Nyawa: {nyawa}", True, (0, 0, 0)), (10, 10))
    if game_over:
        layar.blit(font.render("GAME OVER - tekan R untuk main lagi", True, (255, 255, 0)),
                   (LEBAR // 2 - 220, TINGGI // 2))

    pygame.display.flip()
    clock.tick(60)

kamera.release()
pygame.quit()
