import random
import cv2
import numpy as np
import pygame

kamera = cv2.VideoCapture(0)
ok, frame = kamera.read()
tinggi_asli, lebar_asli = frame.shape[:2]
LEBAR = 800
TINGGI = LEBAR * tinggi_asli // lebar_asli

# biru HSV
biru_bawah = np.array([86, 64, 113])
biru_atas = np.array([118, 182, 189])

pygame.init()
layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Tangkap Buah")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 30)

# warna buah: merah, kuning, hijau. bom hitam
warna_buah = [(220, 40, 40), (250, 220, 50), (110, 170, 60)]
warna_bom = (30, 30, 30)

keranjang_x = LEBAR // 2
keranjang_lebar = 150
keranjang_tinggi = 50
keranjang_y = TINGGI - 70

items = []  
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

    # cari biru terbesar
    hsv = cv2.cvtColor(cv2.GaussianBlur(frame, (11, 11), 0), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, biru_bawah, biru_atas)
    kontur, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if kontur:
        terbesar = max(kontur, key=cv2.contourArea)
        if cv2.contourArea(terbesar) > 500:
            x, y, w, h = cv2.boundingRect(terbesar)
            keranjang_x = x + w // 2

    if not game_over:
        timer += 1
        if timer > 40:
            bom = random.random() < 0.2  # 20% bom
            warna = warna_bom if bom else random.choice(warna_buah)
            items.append([random.randint(20, LEBAR - 20), 0, warna, bom])
            timer = 0

        for it in items[:]:
            it[1] += 5

            masuk = (keranjang_y <= it[1] <= keranjang_y + keranjang_tinggi
                     and abs(it[0] - keranjang_x) <= keranjang_lebar // 2)

            if masuk:
                items.remove(it)
                if it[3]:
                    nyawa -= 1
                else:
                    skor += 1
            elif it[1] > TINGGI:
                items.remove(it)
                if not it[3]:  # bom lolos aman
                    nyawa -= 1

        if nyawa <= 0:
            game_over = True

    terang = cv2.convertScaleAbs(frame, alpha=1.15, beta=30)
    rgb = cv2.cvtColor(terang, cv2.COLOR_BGR2RGB)
    layar.blit(pygame.image.frombuffer(rgb.tobytes(), (LEBAR, TINGGI), "RGB"), (0, 0))

    for x, y, warna, bom in items:
        pygame.draw.circle(layar, warna, (x, y), 20)

    pygame.draw.rect(layar, (150, 100, 50),
                     (keranjang_x - keranjang_lebar // 2, keranjang_y, keranjang_lebar, keranjang_tinggi))

    layar.blit(font.render(f"Skor: {skor}   Nyawa: {nyawa}", True, (0, 0, 0)), (10, 10))
    if game_over:
        layar.blit(font.render("GAME OVER - tekan R untuk main lagi", True, (255, 255, 0)),
                   (LEBAR // 2 - 220, TINGGI // 2))

    pygame.display.flip()
    clock.tick(60)

kamera.release()
pygame.quit()