import pygame, sys, random
from pygame.locals import *
import yfinance as yf
import pandas as pd
import datetime as dt

pygame.init()

# Colours
BACKGROUND = (255, 255, 255)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('SPY Daytrading Simulator')
pygame.font.init()

# The main function that controls the game
def main():
    score = 0
    tries = 0
    dup_last_5 = [0, 0, 0, 0, 0]
    last_5 = [0, 0, 0, 0, 0]

    location = 0
    looping = True
    my_font = pygame.font.SysFont('Times New Roman', 30)
    small_font = pygame.font.SysFont('Times New Roman', 20)

    spy = yf.Ticker("SPY")

    # get historical market data
    hist = spy.history(period="7y")

    index = random.randint(5, len(hist['Close'].keys()) - 2)
    for i in range(5):
        last_5[i] = hist['Close'][hist['Close'].index[index - i]]
        dup_last_5[i] = hist['Close'][hist['Close'].index[index - i]]

    # The main game loop
    while looping:
        # Get inputs
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    tries += 1
                    if hist['Close'][hist['Close'].index[index + 1]] < hist['Close'][hist['Close'].index[index]]:
                        score += 1
                    index = random.randint(5, len(hist['Close'].keys()) - 2)
                    for i in range(5):
                        last_5[i] = hist['Close'][hist['Close'].index[index - i]]
                        dup_last_5[i] = hist['Close'][hist['Close'].index[index - i]]
                        print(hist['Close'].index[index - i], ":", hist['Close'][hist['Close'].index[index - i]])
                        print(last_5)

                if event.key == pygame.K_UP:
                    tries += 1
                    if hist['Close'][hist['Close'].index[index + 1]] > hist['Close'][hist['Close'].index[index]]:
                        score += 1
                    index = random.randint(5, len(hist['Close'].keys()) - 2)
                    for i in range(5):
                        last_5[i] = hist['Close'][hist['Close'].index[index - i]]
                        dup_last_5[i] = hist['Close'][hist['Close'].index[index - i]]

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Processing
        # This section will be built out later

        # Render elements of the game

        WINDOW.fill(BACKGROUND)
        # Background for chart
        pygame.draw.rect(WINDOW, (70, 70, 70), pygame.Rect(30, 30, 640, 400))

        # Normalize last_5 values for plotting
        if last_5 == dup_last_5:
            min_val = min(dup_last_5)
            max_val = max(dup_last_5)
            for i in range(5):
                last_5[i] = 430 -((last_5[i] - min_val) / (max_val - min_val)) * 400
            last_5.reverse()

        # Draw the line
        x_positions = [30, 190, 350, 510, 670]
        points = [(x_positions[i], last_5[i]) for i in range(5)]
        pygame.draw.lines(WINDOW, (25, 255, 255), False, points)

        # Lower bound text
        text_surface = my_font.render("{:.2f}".format(min(dup_last_5)), False, (0, 0, 0))
        WINDOW.blit(text_surface, (30, 400))

        # Upper bound text
        text_surface = my_font.render("{:.2f}".format(max(dup_last_5)), False, (0, 0, 0))
        WINDOW.blit(text_surface, (30, 30))

        # SPY text
        text_surface = my_font.render('SPY', False, (0, 0, 0))
        WINDOW.blit(text_surface, (340, 0))

        # Score text
        score_text = f'Score: {score}, Total tries: {tries}'
        text_color = (0, 255, 0) if score > tries / 2 else (255, 0, 0)
        text_surface = small_font.render(score_text, False, text_color)
        WINDOW.blit(text_surface, (20, 640))

        # Explanation text
        text_surface = small_font.render('Press Up to predict the stock will go up and Down to predict it will go down', False, (0, 0, 0))
        WINDOW.blit(text_surface, (20, 670))

        # Date text
        end_date_text = f"End Date: {hist['Close'].index[index].strftime('%Y/%m/%d')}"
        text_surface = small_font.render(end_date_text, False, (0, 0, 0))
        WINDOW.blit(text_surface, (20, 610))

        pygame.display.update()
        fpsClock.tick(FPS)

main()
