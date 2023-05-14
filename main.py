import os
import random
import pygame
import csv


from Display import Display
from Gift import Gift
from Ship import Ship
from World import World

pygame.mixer.init()

window_width = 1080
window_height = 600
display = Display(window_width, window_height)
window = display.window
border = pygame.Rect(0, 0, window_width, window_height)

CHICKEN_IMAGE = pygame.image.load(os.path.join('Assets', 'kurczak.webp'))
CHICKEN_IMAGE = pygame.transform.scale(CHICKEN_IMAGE, (70, 70))
SPACECRAFT_IMAGE = pygame.image.load(os.path.join('Assets', 'spacecraft.png'))
SPACECRAFT_IMAGE = pygame.transform.scale(SPACECRAFT_IMAGE, (70, 70))
EGG_IMAGE = pygame.image.load(os.path.join('Assets', 'egg.webp'))
EGG_IMAGE = pygame.transform.scale(EGG_IMAGE, (20, 25))


def save_score(row):
    f = open('scores.csv', 'a')
    writer = csv.writer(f)
    writer.writerow(row)
    f.close()


def get_scores():
    with open("scores.csv", 'r') as file:
        csv_reader = csv.reader(file, delimiter=':')
        scores = [int(row[0]) for row in csv_reader if row]
    scores.sort(reverse=True)
    return scores


def main():

    start_over = False

    while True:
        write_to_csv = False
        clock = pygame.time.Clock()
        fps = 60
        is_running = True
        gift_ratio = 100
        enemy_ratio = 40
        world = World(window_height, window_width, display)
        scores = get_scores()

        while not start_over:
            clock.tick(fps)
            pygame.draw.rect(world.display.window, world.background_color, border)
            pygame.font.init()
            x = world.width // 2
            y = world.height // 2
            font = pygame.font.Font('freesansbold.ttf', 28)
            text = font.render("Press SPACE to play", True, (255, 255, 255), (8, 17, 53))
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            window.blit(text, text_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                break

        start_over = True
        count_frames = 1
        while True:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            if count_frames % 2 == 0:
                world.create_star()

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_p]:
                is_running = False
            if keys_pressed[pygame.K_ESCAPE]:
                is_running = True

            if is_running:
                count_frames += 1
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
                    world.ship.move_left()

                if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
                    world.ship.move_right()

                if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
                    world.ship.move_up()

                if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
                    world.ship.move_down()

                world.collisions()

                if count_frames % enemy_ratio == 0:
                    # enemy_ratio = random.randint(100, 500)
                    world.spawn_enemy2()

                if count_frames % gift_ratio == 0:
                    gift_ratio = random.randint(100, 1000)
                    world.spawn_gift()

                pygame.draw.rect(world.display.window, world.background_color, border)

                world.move_enemies()
                world.move_stars()
                world.move_gifts()

                for enemy in world.enemies:
                    enemy.bullets_move()
                    if enemy.is_alive:
                        if count_frames % enemy.bullet_ratio == 0:
                            enemy.create_bullet()
                        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                        # pygame.draw.rect(world.display.window, enemy.color, enemy_rect)
                        window.blit(CHICKEN_IMAGE, (enemy_rect.x - 13, enemy_rect.y - 13))
                    for bullet in enemy.bullets:
                        window.blit(EGG_IMAGE, (bullet.body.x - 3, bullet.body.y - 3))
                        # pygame.draw.rect(world.display.window, bullet.color, bullet.body)

                i = 0
                while i < len(world.enemies):
                    if not world.enemies[i].is_alive and not len(world.enemies[i].bullets):
                        del world.enemies[i]
                        i -= 1
                    i += 1

                world.ship.bullets_move()

                if count_frames % world.ship.bullet_ratio == 0:
                    world.ship.create_bullet()

                ship_rect = pygame.Rect(world.ship.x, world.ship.y, world.ship.width, world.ship.height)
                # pygame.draw.rect(world.display.window, world.ship.color, ship_rect)
                window.blit(SPACECRAFT_IMAGE, (ship_rect.x - 13, ship_rect.y - 13))

                for bullet in world.ship.bullets:
                    pygame.draw.rect(window, bullet.color, bullet.body)

                pygame.font.init()
                x = world.width // 2
                y = 8

                font = pygame.font.Font('freesansbold.ttf', 18)

                text = font.render("SCORE " + str(world.ship.points), True, (255, 255, 255), (8, 17, 53))
                text_rect = text.get_rect()
                text_rect.center = (x, y)
                window.blit(text, text_rect)

                x = world.width - 100
                text = font.render("MAX SCORE " + str(scores[0]), True, (255, 255, 255), (8, 17, 53))
                text_rect = text.get_rect()
                text_rect.center = (x, y)
                window.blit(text, text_rect)

                if world.ship.health_points <= 0:
                    # is_running = False
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound('Assets/game_over_sound.mp3'))
                    break
                    # write_to_csv = True

                pygame.display.update()

            # if not is_running and write_to_csv:
            #     new_row = [str(world.ship.points)]
            #     save_score(new_row)
            #     write_to_csv = False
            #     break

        new_row = [str(world.ship.points)]
        save_score(new_row)
        # write_to_csv = False

        while True:
            clock.tick(fps)
            pygame.draw.rect(world.display.window, world.background_color, border)
            pygame.font.init()
            x = world.width // 2
            y = 150

            font = pygame.font.Font('freesansbold.ttf', 28)
            text = font.render("Press SPACE to play again", True, (255, 255, 255), (8, 17, 53))
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            window.blit(text, text_rect)

            y += 80
            font = pygame.font.Font('freesansbold.ttf', 20)
            text = font.render("Leaderboard", True, (255, 255, 255), (8, 17, 53))
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            window.blit(text, text_rect)

            font = pygame.font.Font('freesansbold.ttf', 18)
            scores = get_scores()
            for i in range(5):
                y += 30
                text = font.render(str(i + 1) + ". " + str(scores[i]), True, (255, 255, 255), (8, 17, 53))
                text_rect = text.get_rect()
                text_rect.top = y
                text_rect.left = x - 30
                window.blit(text, text_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                break


if __name__ == "__main__":
    main()
