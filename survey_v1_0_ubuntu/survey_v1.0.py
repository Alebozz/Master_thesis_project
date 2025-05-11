import pygame
import cv2
import os
import random
import numpy as np
from pathlib import Path

#TODO:
# Switch path to new dataset --> need to replace the old images with new ones --> need to recompute with MATLAB

# Initialize pygame
os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init() to try and center the displayed window
pygame.init()

# Constants
CHANNELS_GRID_ROWS = 3
CHANNELS_GRID_COLUMNS = 5
CELL_SIZE = 50
GRID_MARGIN = 5
GRID_WIDTH = CHANNELS_GRID_COLUMNS * (CELL_SIZE + GRID_MARGIN) + GRID_MARGIN
BUTTON_WIDTH = 320
BUTTON_HEIGHT = 40
BUTTON_X = GRID_MARGIN
BUTTON_Y = GRID_WIDTH + 10
# Configuration
IMG_GRID_POS = (47, 25)  # Top-left corner of the grid (x, y)
IMG_GRID_SIZE = (15, 12)  # Number of rows and columns (rows, cols) # CHANGE NUMBER OF ROWS BECAUSE NOW WE CONSIDER ONLY 15 CHANNELS
CELL_SIZE_W = 23  # Width and height of each cell
CELL_SIZE_H = 18 # Width and height of each cell
OUTPUT_FILE = "final_results.txt"  # File to store selected cells
DATASET_PATH = Path("images_datasets_merged") # needs to be changed to a relative path once the whole thing works!!!
REF_TOPOPLOT_PATH = Path("channels_positions_on_topoplot.png") # need to be changed to relative path at the end
FIHSER_SCORE_SIZE = (399, 332) # CHANGE AGAIN DIMENSIONS BECAUSE NOW WE CONSIDER ONLY 15 CHANNELS
#previous (369, 314)

channels_dict = {1:"FC3", 2:"FC1", 3:"FCZ", 4:"FC2", 5:"FC4",
                 6:"C3", 7:"C1", 8:"CZ", 9:"C2", 10:"C4",
                 11:"CP3", 12:"CP1", 13:"CPZ", 14:"CP2", 15:"CP4"}


# Window size
WINDOW_WIDTH = FIHSER_SCORE_SIZE[0]*3
WINDOW_HEIGHT = max(FIHSER_SCORE_SIZE[1]*2, GRID_WIDTH + BUTTON_HEIGHT + 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
CLICKED_COLOR = (100, 200, 100)
BUTTON_COLOR = (180, 180, 180)
BUTTON_HOVER_COLOR = (150, 150, 150)

# Create screen
screen_info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
screen_width,screen_height = screen_info.current_w,screen_info.current_h
screen = pygame.display.set_mode((screen_width-15, screen_height-60), pygame.RESIZABLE)
pygame.display.set_caption("Image and Interactive Grid")

# Font
font = pygame.font.Font(None, 25)
button_font = pygame.font.Font(None, 20)

# Channel selection grid state initialization
grid = [[False for _ in range(CHANNELS_GRID_COLUMNS)] for _ in range(CHANNELS_GRID_ROWS)]

def retrieve_samples_paths(path): # retrieves all the folders in the dataset and returns only a sublist of them picked up randomly
    samples_paths = os.listdir(path)
    selected_samples = random.sample(samples_paths, 20) # should be different at every call based on tests performed
    for i in range(len(selected_samples)):
        selected_samples[i] = DATASET_PATH / selected_samples[i]
    return selected_samples

def retrieve_selected_spectrograms_paths(path, selected_channels):
    token = "spectrogram_"
    spectrograms_names = list(path.glob("*" + token + "*"))
    selected_spectrograms = []
    for ch in selected_channels:
        for name in spectrograms_names:
            if (token+ch) in name.parts[-1]: # -1 because we want to check the last element which is the filename
                selected_spectrograms.append(name)
    
    return selected_spectrograms


def load_spectrogram_minibatch(imgs_list): # working perfectly
    n = len(imgs_list)//3
    row1 = cv2.resize(cv2.imread(str(imgs_list[0]), cv2.IMREAD_COLOR),(350,262))
    row2 = cv2.resize(cv2.imread(str(imgs_list[2]), cv2.IMREAD_COLOR),(350,262))
    row3 = cv2.resize(cv2.imread(str(imgs_list[1]), cv2.IMREAD_COLOR),(350,262))
    for i in range(1,n):
        row1 = cv2.hconcat([row1, cv2.resize(cv2.imread(str(imgs_list[3*i]), cv2.IMREAD_COLOR),(350,262))])
        row2 = cv2.hconcat([row2, cv2.resize(cv2.imread(str(imgs_list[2+3*i]), cv2.IMREAD_COLOR),(350,262))])
        row3 = cv2.hconcat([row3, cv2.resize(cv2.imread(str(imgs_list[1+3*i]), cv2.IMREAD_COLOR),(350,262))])
    final = cv2.vconcat([row1,row2,row3])
    return final

def merge_selected_spectrograms(selected_spectrograms): # working perfectly
    n = len(selected_spectrograms)//3
    
    if n == 0:
        return None
    
    if n <= 4:
        return [load_spectrogram_minibatch(selected_spectrograms[0:(3*n)])]
    elif n <= 8:
        return [load_spectrogram_minibatch(selected_spectrograms[0:12]), load_spectrogram_minibatch(selected_spectrograms[12:(3*n)])]
    elif n <= 12:
        return [load_spectrogram_minibatch(selected_spectrograms[0:12]), load_spectrogram_minibatch(selected_spectrograms[12:24]), load_spectrogram_minibatch(selected_spectrograms[24:(3*n)])]
    elif n <= 16:
        return [load_spectrogram_minibatch(selected_spectrograms[0:12]), load_spectrogram_minibatch(selected_spectrograms[12:24]), load_spectrogram_minibatch(selected_spectrograms[24:36]), load_spectrogram_minibatch(selected_spectrograms[36:(3*n)])]
    
    return None

def load_and_merge_topoplots(path,token):
    selected_topoplots = list(path.glob("*" + token + "*"))
    row1 = cv2.resize(cv2.imread(str(selected_topoplots[0]), cv2.IMREAD_COLOR),(738,269))
    row2 = cv2.resize(cv2.imread(str(selected_topoplots[1]), cv2.IMREAD_COLOR),(738,269))
    row3 = cv2.resize(cv2.imread(str(selected_topoplots[2]), cv2.IMREAD_COLOR),(738,269))
    
    return cv2.vconcat([row1,row2,row3])

def retrieve_fisher_images(path,token):
    feature_maps = list(path.glob("*" + token + "*"))
    feature_maps_imgs = []
    for x in feature_maps:
        feature_maps_imgs.append(cv2.flip(cv2.rotate(cv2.cvtColor(cv2.resize(cv2.imread(str(x),cv2.IMREAD_COLOR),FIHSER_SCORE_SIZE),cv2.COLOR_BGR2RGB),cv2.ROTATE_90_COUNTERCLOCKWISE),0))
    
    return feature_maps_imgs

def draw_grid(selected_cells):
    """Draws the interactive grid."""
    for row in range(IMG_GRID_SIZE[0]):
        for col in range(IMG_GRID_SIZE[1]):
            rect = pygame.Rect(FIHSER_SCORE_SIZE[0] + IMG_GRID_POS[0] + col * CELL_SIZE_W, FIHSER_SCORE_SIZE[1] + IMG_GRID_POS[1] + row * CELL_SIZE_H, CELL_SIZE_W, CELL_SIZE_H)
            color = MAGENTA if selected_cells[row*IMG_GRID_SIZE[1]+col] == 1 else GRAY
            if selected_cells[row*IMG_GRID_SIZE[1]+col] == 1:
                pygame.draw.line(screen, BLACK, (FIHSER_SCORE_SIZE[0] + IMG_GRID_POS[0] + col * CELL_SIZE_W, FIHSER_SCORE_SIZE[1] + IMG_GRID_POS[1] + row * CELL_SIZE_H),
                                 (FIHSER_SCORE_SIZE[0] + IMG_GRID_POS[0] + col * CELL_SIZE_W + CELL_SIZE_W, FIHSER_SCORE_SIZE[1] + IMG_GRID_POS[1] + row * CELL_SIZE_H + CELL_SIZE_H), 2)
                
                pygame.draw.line(screen, BLACK, (FIHSER_SCORE_SIZE[0] + IMG_GRID_POS[0] + col * CELL_SIZE_W + CELL_SIZE_W, FIHSER_SCORE_SIZE[1] + IMG_GRID_POS[1] + row * CELL_SIZE_H),
                                 (FIHSER_SCORE_SIZE[0] + IMG_GRID_POS[0] + col * CELL_SIZE_W, FIHSER_SCORE_SIZE[1] + IMG_GRID_POS[1] + row * CELL_SIZE_H + CELL_SIZE_H), 2)
            pygame.draw.rect(screen, color, rect, 2)
            
def save_selected_cells(sample_path, selected_cells): # CHANGE IN ORDER TO SAVE A SINGLE VECTOR OF ZEROS AND ONES
    """Saves selected cells to a text file."""
    with open(OUTPUT_FILE, "a") as f:
        f.write(f"sample: {sample_path}\n")
        f.write("Cells: " + ", ".join([f"{x}" for x in selected_cells]) + "\n\n")
        
def get_cell_index_from_pos(pos):
    """Returns the index of the cell based on the mouse position, or None if out of bounds."""
    x, y = pos
    grid_x, grid_y = IMG_GRID_POS
    if FIHSER_SCORE_SIZE[0] + grid_x <= x < FIHSER_SCORE_SIZE[0] + grid_x + IMG_GRID_SIZE[1] * CELL_SIZE_W and FIHSER_SCORE_SIZE[1] + grid_y <= y < FIHSER_SCORE_SIZE[1] + grid_y + IMG_GRID_SIZE[0] * CELL_SIZE_H:
        col = int((x - (grid_x + FIHSER_SCORE_SIZE[0])) // CELL_SIZE_W)
        row = int((y - (grid_y + FIHSER_SCORE_SIZE[1])) // CELL_SIZE_H)
        return row*IMG_GRID_SIZE[1]+col
    return None

# Main loop
running = True

clock = pygame.time.Clock()

number = 0

retrieved_samples = retrieve_samples_paths(DATASET_PATH) # contains the randomly selected samples to show and evaluate
sample_index = 0
loaded = False

instr_read = False

# INIZIO SEZIONE ISTRUZIONI PER L'USO
with open("Instruction_file.txt") as file:
    lines = [line.rstrip() for line in file]
        
SCREEN_INSTRUCTION_COLOR = (115, 199, 132) 

#create splash screen were to put instructions
bg = cv2.cvtColor(cv2.imread("bg_lesser.png"), cv2.COLOR_BGR2RGB)

while True:
    # screen.blit(SCREEN_INSTRUCTION_COLOR)
    screen.blit(pygame.surfarray.make_surface(bg), (0, 0))
    label = []
    for line in lines: 
        label.append(font.render(line, True, BLACK))
            
    for line in range(len(label)):
        screen.blit(label[line], (50,50+(line*12)+(10*line)))
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                instr_read = True
                
                break  # Move to the next image
    if instr_read:
        break

# FINE SEZIONE ISTRUZIONI PER L'USO

while running and sample_index < len(retrieved_samples):
    screen.fill(WHITE)
    
    selected_cells = np.zeros(180, dtype=np.uint8)
        
    while running and sample_index < len(retrieved_samples):
        
        current_sample = retrieved_samples[sample_index] # contains the relative path to the current sample folder
    
        # retrieve the images of the Fisher's score feature maps
        if (not loaded):
            fisher_scores_images = retrieve_fisher_images(current_sample,'featuremap')
            loaded = True
        
        screen.fill(WHITE)
        # for now it simply draws the same image 4 times --> final version will draw all the different images

        if len(fisher_scores_images) == 3:
            screen.blit(pygame.surfarray.make_surface(fisher_scores_images[0]), (0, 0))
            screen.blit(pygame.surfarray.make_surface(fisher_scores_images[1]), (FIHSER_SCORE_SIZE[0], 0))
            screen.blit(pygame.surfarray.make_surface(fisher_scores_images[2]), (FIHSER_SCORE_SIZE))
        else:
            screen.blit(pygame.surfarray.make_surface(fisher_scores_images[0]), (0, 0))
            screen.blit(pygame.surfarray.make_surface(fisher_scores_images[1]), (FIHSER_SCORE_SIZE[0], 0))
            screen.blit(pygame.surfarray.make_surface(fisher_scores_images[2]), (FIHSER_SCORE_SIZE[0]*2, 0))
            screen.blit(pygame.surfarray.make_surface(fisher_scores_images[3]), (FIHSER_SCORE_SIZE))
        
        draw_grid(selected_cells) # draws inteactive grid on top of the bottom image
        
        # Draw grid for channel selection
        num = 1
        for row in range(0,CHANNELS_GRID_ROWS):
            for col in range(0,CHANNELS_GRID_COLUMNS):
                x = FIHSER_SCORE_SIZE[0]*2 + GRID_MARGIN + col * (CELL_SIZE + GRID_MARGIN)
                y = FIHSER_SCORE_SIZE[1] + GRID_MARGIN + row * (CELL_SIZE + GRID_MARGIN)
                color = CLICKED_COLOR if grid[row][col] else GRAY
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
                
                # Draw numeration
                text = font.render(channels_dict[num], True, BLACK)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)
                num += 1

        # Button for grid channels selection
        mx, my = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER_COLOR if BUTTON_X + FIHSER_SCORE_SIZE[0]*2 <= mx <= BUTTON_X + FIHSER_SCORE_SIZE[0]*2 + BUTTON_WIDTH and BUTTON_Y + FIHSER_SCORE_SIZE[1] <= my <= BUTTON_Y + FIHSER_SCORE_SIZE[1] + BUTTON_HEIGHT else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, (BUTTON_X + FIHSER_SCORE_SIZE[0]*2, BUTTON_Y + FIHSER_SCORE_SIZE[1], BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, BLACK, (BUTTON_X + FIHSER_SCORE_SIZE[0]*2, BUTTON_Y + FIHSER_SCORE_SIZE[1], BUTTON_WIDTH, BUTTON_HEIGHT), 2)
        button_text = button_font.render("Show ERD/ERS spectrograms of selected channels", True, BLACK)
        button_text_rect = button_text.get_rect(center=(BUTTON_X + FIHSER_SCORE_SIZE[0]*2 + BUTTON_WIDTH // 2, BUTTON_Y + FIHSER_SCORE_SIZE[1] + BUTTON_HEIGHT // 2))
        screen.blit(button_text, button_text_rect)
        
        text = "REMAINING SAMPLES TO CLASSIFY: " + str(len(retrieved_samples)-sample_index)
        counter_text = button_font.render(text, True, BLACK)
        counter_text_rect = counter_text.get_rect(center=(BUTTON_X + FIHSER_SCORE_SIZE[0]*2 + BUTTON_WIDTH // 2, BUTTON_Y + FIHSER_SCORE_SIZE[1] + BUTTON_HEIGHT*3.5 // 2))
        screen.blit(counter_text, counter_text_rect)

        # Button for closing all figures opened
        mx, my = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER_COLOR if BUTTON_X<= mx <= BUTTON_X + BUTTON_WIDTH and FIHSER_SCORE_SIZE[1]*1.05 <= my <= FIHSER_SCORE_SIZE[1]*1.05 + BUTTON_HEIGHT else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, (BUTTON_X, FIHSER_SCORE_SIZE[1]*1.05, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, BLACK, (BUTTON_X, FIHSER_SCORE_SIZE[1]*1.05, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
        button_text = button_font.render("Close all opened images", True, BLACK,)
        button_text_rect = button_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, FIHSER_SCORE_SIZE[1]*1.05 + BUTTON_HEIGHT // 2))
        screen.blit(button_text, button_text_rect)
        
        # Button for topoplots mu band
        mx, my = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER_COLOR if BUTTON_X<= mx <= BUTTON_X + BUTTON_WIDTH and FIHSER_SCORE_SIZE[1]*1.25 <= my <= FIHSER_SCORE_SIZE[1]*1.25 + BUTTON_HEIGHT else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, (BUTTON_X, FIHSER_SCORE_SIZE[1]*1.25, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, BLACK, (BUTTON_X, FIHSER_SCORE_SIZE[1]*1.25, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
        button_text = button_font.render("Show mu band topoplots", True, BLACK)
        button_text_rect = button_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, FIHSER_SCORE_SIZE[1]*1.25 + BUTTON_HEIGHT // 2))
        screen.blit(button_text, button_text_rect)

        # Button for topoplots beta band
        mx, my = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER_COLOR if BUTTON_X<= mx <= BUTTON_X + BUTTON_WIDTH and FIHSER_SCORE_SIZE[1]*1.5 <= my <=  FIHSER_SCORE_SIZE[1]*1.5 + BUTTON_HEIGHT else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, (BUTTON_X, FIHSER_SCORE_SIZE[1]*1.5, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, BLACK, (BUTTON_X, FIHSER_SCORE_SIZE[1]*1.5, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
        button_text = button_font.render("Show beta band topoplots", True, BLACK)
        button_text_rect = button_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, FIHSER_SCORE_SIZE[1]*1.5 + BUTTON_HEIGHT // 2))
        screen.blit(button_text, button_text_rect)

        # Button for topoplots channels schema
        mx, my = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER_COLOR if BUTTON_X <= mx <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y + FIHSER_SCORE_SIZE[1] <= my <= BUTTON_Y + FIHSER_SCORE_SIZE[1] + BUTTON_HEIGHT else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, (BUTTON_X, BUTTON_Y + FIHSER_SCORE_SIZE[1], BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, BLACK, (BUTTON_X, BUTTON_Y + FIHSER_SCORE_SIZE[1], BUTTON_WIDTH, BUTTON_HEIGHT), 2)
        button_text = button_font.render("Show channels positions in topoplot", True, BLACK)
        button_text_rect = button_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + FIHSER_SCORE_SIZE[1] + BUTTON_HEIGHT // 2))
        screen.blit(button_text, button_text_rect)

        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # DEFINE THE VARIOUS EVENTS FOR THE MOUSE POSITIONS WHEN CLICKING --> GRID BUTTON, MU TOPOPLOT, BETA TOPOPLOT, CHANNEL POSITION TOPOPLOTS
                
                if BUTTON_X<= mx <= BUTTON_X + BUTTON_WIDTH and FIHSER_SCORE_SIZE[1]*1.05 <= my <= FIHSER_SCORE_SIZE[1]*1.05 + BUTTON_HEIGHT:
                    try:
                        cv2.destroyAllWindows()
                    except: # only to avoid crashes
                        pass
                
                elif BUTTON_X<= mx <= BUTTON_X + BUTTON_WIDTH and FIHSER_SCORE_SIZE[1]*1.25 <= my <= FIHSER_SCORE_SIZE[1]*1.25 + BUTTON_HEIGHT: # mu topoplot event button
                    mu_topoplots = load_and_merge_topoplots(current_sample,'mu') # change to path of currently displayed folder files
                    try:
                        cv2.destroyWindow('mu topoplots')
                    except: # only to avoid crashes
                        pass
                    finally:
                        cv2.namedWindow('mu topoplots')
                        cv2.imshow('mu topoplots', mu_topoplots)
                
                elif BUTTON_X<= mx <= BUTTON_X + BUTTON_WIDTH and FIHSER_SCORE_SIZE[1]*1.5 <= my <=  FIHSER_SCORE_SIZE[1]*1.5 + BUTTON_HEIGHT: # beta topoplot event button
                    beta_topoplots = load_and_merge_topoplots(current_sample,'beta') # change to path of currently displayed folder files
                    try:
                        cv2.destroyWindow('beta topoplots')
                    except: # only to avoid crashes
                        pass
                    finally:
                        cv2.namedWindow('beta topoplots')
                        cv2.imshow('beta topoplots', beta_topoplots)
                
                elif BUTTON_X <= mx <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y + FIHSER_SCORE_SIZE[1] <= my <= BUTTON_Y + FIHSER_SCORE_SIZE[1] + BUTTON_HEIGHT: # channels topoplot event button
                    try:
                        cv2.destroyWindow('topoplot channels')
                    except: # only to avoid crashes
                        pass
                    finally:
                        cv2.namedWindow('topoplot channels')
                        ref_topoplot = cv2.imread(str(REF_TOPOPLOT_PATH))
                        cv2.imshow('topoplot channels', ref_topoplot)
                
                elif BUTTON_X + FIHSER_SCORE_SIZE[0]*2 <= mx <= BUTTON_X + FIHSER_SCORE_SIZE[0]*2 + BUTTON_WIDTH and BUTTON_Y + FIHSER_SCORE_SIZE[1] <= my <= BUTTON_Y + FIHSER_SCORE_SIZE[1] + BUTTON_HEIGHT: # channel specific info button
                    
                    # perform check on selected cells of grid of channels
                    selected_channels = []
                    for row in range(CHANNELS_GRID_ROWS):
                        for col in range(CHANNELS_GRID_COLUMNS):
                            if grid[row][col]:
                                selected_channels.append(channels_dict[1+col+row*CHANNELS_GRID_COLUMNS]) # 1+ is because the dictionary containing the values starts with the first key with value 1 --> was doing matlab code as well at that time, here's why
                    
                    # if at least one channel has been selected, retrieve all the images for the selected channels and display them
                    if len(selected_channels) != 0: 
                        sc_paths = retrieve_selected_spectrograms_paths(current_sample, selected_channels)
                        spectrograms_imgs = merge_selected_spectrograms(sc_paths)
                        try:
                            cv2.destroyWindow("spectrogram_win_0")
                            cv2.destroyWindow("spectrogram_win_1") # VERY UGLY CODING
                            cv2.destroyWindow("spectrogram_win_2")
                            cv2.destroyWindow("spectrogram_win_3")
                        except:
                            pass
                        finally:
                            if spectrograms_imgs != None:
                                for batch in range(len(spectrograms_imgs)):
                                    cv2.imshow("spectrogram_win_"+str(batch),spectrograms_imgs[batch])
                    
                    grid = [[False for _ in range(CHANNELS_GRID_COLUMNS)] for _ in range(CHANNELS_GRID_ROWS)]
                    
                else:
                    for row in range(CHANNELS_GRID_ROWS):
                        for col in range(CHANNELS_GRID_COLUMNS):
                            x = FIHSER_SCORE_SIZE[0]*2 + GRID_MARGIN + col * (CELL_SIZE + GRID_MARGIN)
                            y = FIHSER_SCORE_SIZE[1] + GRID_MARGIN + row * (CELL_SIZE + GRID_MARGIN)
                            if x <= mx <= x + CELL_SIZE and y <= my <= y + CELL_SIZE:
                                grid[row][col] = not grid[row][col]
                                
                img_cell_index = get_cell_index_from_pos(event.pos)
                if img_cell_index is not None:
                    if selected_cells[img_cell_index] == 1:
                        selected_cells[img_cell_index] = 0
                    else:
                        selected_cells[img_cell_index] = 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.display.quit()
                    
                elif event.key == pygame.K_RETURN:
                    save_selected_cells((current_sample.parts)[-1], selected_cells)
                    sample_index += 1
                    loaded = False
                    selected_cells[:] = 0 # Clear selected cells when moving to the next image
                    cv2.destroyAllWindows()
                    break  # Move to the next image
                    
        clock.tick(30)

pygame.quit()
