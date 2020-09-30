import pygame, os, math

# Initialization
pygame.init()
pygame.font.init()


# Getting Images
image_dir = os.path.join(os.getcwd(), 'images')
images = list()
for imgName in os.listdir(image_dir):
    imgPath = os.path.join(image_dir, imgName)
    images.append(pygame.image.load(imgPath))


# Game Variables
hangman_status = 0
word = 'tamasha'.upper()
guessed_words = []


# IMPORTANT DIMS
WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
WIDTH, HEIGHT = 1050, 600
FPS = 60
RADIUS = 20
GAP = 15

# Getting Buttons Positions
startX = (WIDTH - 26 * RADIUS - 12 * GAP) // 2
startY = (HEIGHT - 4 * RADIUS - 2 * GAP)
letters = list() # Will be in the shape of (x, y, letter, visible)
for i in range(26):
    x = startX + RADIUS + (i % 13) * (2 * RADIUS + GAP)
    y = startY + RADIUS + (i // 13) * (2 * RADIUS + GAP)
    letter = chr(65 + i)
    letters.append([x, y, letter, True])


# Setting up FONTS and CLOCKS
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD = pygame.font.SysFont('comicsans', 50)
TITLE = pygame.font.SysFont('comicsans', 60)
clock = pygame.time.Clock()

# Setting up Display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hang Man')

# Drawing Functions
def draw(win, letters, radius):
    win.fill(WHITE)
    title = TITLE.render('HANGMAN DEVELOPER', 1, BLACK)
    win.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    display = ''
    for letter in word:
        if letter in guessed_words:
            display += letter + ' '
        else:
            display += '_ '
            
    text = LETTER_FONT.render(display, 1, BLACK)
    win.blit(text, (400, 200))
    
    for letter in letters:
        x, y, ltr, visible = letter
        
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), radius, 2)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            ltrX = x - text.get_width() / 2
            ltrY = y - text.get_height() / 2
            
            win.blit(text, (ltrX, ltrY))
    win.blit(images[hangman_status], (80, 80))
    pygame.display.update()
    
def display_msg(win, msg):
    pygame.time.delay(1500)
    win.fill(WHITE)
    msg = WORD.render(msg, 1, BLACK)
    win.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(3000)

# Main Game Loop
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dist = math.sqrt((x - mouseX)**2 + (y - mouseY)**2)
                    if dist <= RADIUS:
                        letter[3] = False
                        guessed_words.append(ltr)
                        if ltr not in word:
                            hangman_status += 1
    draw(win, letters, RADIUS)
            
    won = True
    for letter in word:
        if letter not in guessed_words:
            won = False
    
    if won:
        display_msg(win, "You've WON !")
        break
    
    if hangman_status == 6:
        display_msg(win, "You've LOST !")
        break

# Wrapping Up
pygame.quit()