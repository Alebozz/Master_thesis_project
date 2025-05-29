import pygame
import cv2
import os
import random
import numpy as np
from pathlib import Path
import sys


#TODO:
# Switch path to new dataset --> need to replace the old images with new ones --> need to recompute with MATLAB

# Initialize pygame
os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init() to try and center the displayed window
pygame.init()

# Constants
CHANNELS_GRID_ROWS = 4
CHANNELS_GRID_COLUMNS = 4
CELL_SIZE = 40
GRID_MARGIN = 5
GRID_WIDTH = CHANNELS_GRID_COLUMNS * (CELL_SIZE + GRID_MARGIN) + GRID_MARGIN
BUTTON_WIDTH = 335
BUTTON_HEIGHT = 40
BUTTON_X = GRID_MARGIN
BUTTON_Y = GRID_WIDTH + 10
# Configuration
IMG_GRID_POS = (50, 25)  # Top-left corner of the grid (x, y)
IMG_GRID_SIZE = (16, 12)  # Number of rows and columns (rows, cols) # CHANGE NUMBER OF ROWS BECAUSE NOW WE CONSIDER ONLY 15 CHANNELS
CELL_SIZE_W = 26  # Width and height of each cell
CELL_SIZE_H = 17 # Width and height of each cell
SAMPLE_TRACKING_FILE = "already_done.txt" 
OUTPUT_FILE = "final_results.txt"  # File to store selected cells
DATASET_PATH = Path("images_dataset") 
REF_TOPOPLOT_PATH = Path("channels_positions_on_topoplot.png") 
FAKE_IMAGE_FOR_GRID = Path("feature_selection_grid.png")
FIHSER_SCORE_SIZE = (399, 332) 


channels_dict = {1:"FZ", 2:"FC3", 3:"FC1", 4:"FCZ", 5:"FC2", 6:"FC4",
                 7:"C3", 8:"C1", 9:"CZ", 10:"C2", 11:"C4",
                 12:"CP3", 13:"CP1", 14:"CPZ", 15:"CP2", 16:"CP4"}


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
no_sample_font = pygame.font.Font(None, 40)
font = pygame.font.Font(None, 25)
button_font = pygame.font.Font(None, 20)

# Channel selection grid state initialization
grid = [[False for _ in range(CHANNELS_GRID_COLUMNS)] for _ in range(CHANNELS_GRID_ROWS)]

def retrieve_samples_paths(path): # retrieves all the folders in the dataset and returns only a sublist of them picked up randomly
    if os.path.exists(SAMPLE_TRACKING_FILE):
        with open(SAMPLE_TRACKING_FILE, 'r') as fp:
            banned = fp.readlines()
    for i in range(len(banned)):
        banned[i] = banned[i].strip()

    samples_paths = os.listdir(path)
    valid_paths = []
    for pt in samples_paths:
        if pt in banned:
            pass
        else:
            valid_paths.append(pt)

    number_of_samples = 20
    if len(valid_paths) > 0 and len(valid_paths) < 20:
        number_of_samples = len(valid_paths)
    elif len(valid_paths) == 0:
        return None
    selected_samples = random.sample(valid_paths, number_of_samples) # should be different at every call based on tests performed
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
    n = len(imgs_list)//2
    row1 = cv2.resize(cv2.imread(str(imgs_list[0]), cv2.IMREAD_COLOR),(350,300))
    row2 = cv2.resize(cv2.imread(str(imgs_list[1]), cv2.IMREAD_COLOR),(350,300))
    for i in range(1,n):
        row1 = cv2.hconcat([row1, cv2.resize(cv2.imread(str(imgs_list[2*i]), cv2.IMREAD_COLOR),(350,300))])
        row2 = cv2.hconcat([row2, cv2.resize(cv2.imread(str(imgs_list[1+2*i]), cv2.IMREAD_COLOR),(350,300))])
    final = cv2.vconcat([row1,row2])
    return final

def merge_selected_spectrograms(selected_spectrograms): # working perfectly
    n = len(selected_spectrograms)//2
    
    if n == 0:
        return None
    
    if n <= 4:
        return [load_spectrogram_minibatch(selected_spectrograms[0:(2*n)])]
    elif n <= 8:
        return [load_spectrogram_minibatch(selected_spectrograms[0:8]), load_spectrogram_minibatch(selected_spectrograms[8:(2*n)])]
    elif n <= 12:
        return [load_spectrogram_minibatch(selected_spectrograms[0:8]), load_spectrogram_minibatch(selected_spectrograms[8:16]), load_spectrogram_minibatch(selected_spectrograms[16:(2*n)])]
    elif n <= 16:
        return [load_spectrogram_minibatch(selected_spectrograms[0:8]), load_spectrogram_minibatch(selected_spectrograms[8:16]), load_spectrogram_minibatch(selected_spectrograms[16:24]), load_spectrogram_minibatch(selected_spectrograms[24:(2*n)])]
    
    return None

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
            rect = pygame.Rect(FIHSER_SCORE_SIZE[0]*2 + IMG_GRID_POS[0] + col * CELL_SIZE_W, FIHSER_SCORE_SIZE[1] + IMG_GRID_POS[1] + row * CELL_SIZE_H, CELL_SIZE_W, CELL_SIZE_H)
            color = MAGENTA if selected_cells[row*IMG_GRID_SIZE[1]+col] == 1 else BLACK
            if selected_cells[row*IMG_GRID_SIZE[1]+col] == 1:
                pygame.draw.line(screen, BLACK, (FIHSER_SCORE_SIZE[0]*2 + IMG_GRID_POS[0] + col * CELL_SIZE_W, FIHSER_SCORE_SIZE[1] + IMG_GRID_POS[1] + row * CELL_SIZE_H),
                                 (FIHSER_SCORE_SIZE[0]*2 + IMG_GRID_POS[0] + col * CELL_SIZE_W + CELL_SIZE_W, FIHSER_SCORE_SIZE[1] + IMG_GRID_POS[1] + row * CELL_SIZE_H + CELL_SIZE_H), 2)
                
                pygame.draw.line(screen, BLACK, (FIHSER_SCORE_SIZE[0]*2 + IMG_GRID_POS[0] + col * CELL_SIZE_W + CELL_SIZE_W, FIHSER_SCORE_SIZE[1] + IMG_GRID_POS[1] + row * CELL_SIZE_H),
                                 (FIHSER_SCORE_SIZE[0]*2 + IMG_GRID_POS[0] + col * CELL_SIZE_W, FIHSER_SCORE_SIZE[1] + IMG_GRID_POS[1] + row * CELL_SIZE_H + CELL_SIZE_H), 2)
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
    if FIHSER_SCORE_SIZE[0]*2 + grid_x <= x < FIHSER_SCORE_SIZE[0]*2 + grid_x + IMG_GRID_SIZE[1] * CELL_SIZE_W and FIHSER_SCORE_SIZE[1] + grid_y <= y < FIHSER_SCORE_SIZE[1] + grid_y + IMG_GRID_SIZE[0] * CELL_SIZE_H:
        col = int((x - (grid_x + FIHSER_SCORE_SIZE[0]*2)) // CELL_SIZE_W)
        row = int((y - (grid_y + FIHSER_SCORE_SIZE[1])) // CELL_SIZE_H)
        return row*IMG_GRID_SIZE[1]+col
    return None

def update_sample_tracking(filename, sample_name):
    with open(filename, "a") as fp:
        fp.write(f"{sample_name}" + "\n")


# Main loop
running = True

clock = pygame.time.Clock()

number = 0

if not os.path.exists(SAMPLE_TRACKING_FILE):
    with open(SAMPLE_TRACKING_FILE, 'w') as fp:
        pass

retrieved_samples = retrieve_samples_paths(DATASET_PATH) # contains the randomly selected samples to show and evaluate
no_samples = False
if retrieved_samples == None:
    # INIZIO SEZIONE ISTRUZIONI PER L'USO
    with open("No_More_Samples_Text.txt") as file:
        no_samples_lines = [line.rstrip() for line in file]
        
    SCREEN_INSTRUCTION_COLOR = (115, 199, 132) 

    #create splash screen were to put instructions
    bg = cv2.cvtColor(cv2.imread("bg_lesser.png"), cv2.COLOR_BGR2RGB)

    while True:
        # screen.blit(SCREEN_INSTRUCTION_COLOR)
        screen.blit(pygame.surfarray.make_surface(bg), (0, 0))
        label = []
        for line in no_samples_lines: 
            label.append(no_sample_font.render(line, True, BLACK))
                
        for line in range(len(label)):
            screen.blit(label[line], (50,50+(line*30)+(10*line)))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    no_samples = True
                    break
        if no_samples:
            break

if no_samples:
    pygame.quit()
    sys.exit()
    

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
image_stop = False


while running and sample_index < len(retrieved_samples):
    screen.fill(WHITE)
    
    selected_cells = np.zeros(192, dtype=np.uint8) # change to 192
        
    while running and sample_index < len(retrieved_samples):
        
        current_sample = retrieved_samples[sample_index] # contains the relative path to the current sample folder
    
        # retrieve the images of the Fisher's score feature maps # CHANGE NAME
        if (not loaded):
            fisher_scores_images = retrieve_fisher_images(current_sample,'fisher')
            loaded = True
        
        screen.fill(WHITE)
        # for now it simply draws the same image 4 times --> final version will draw all the different images
        screen.blit(pygame.surfarray.make_surface(fisher_scores_images[0]), (0, 0))
        screen.blit(pygame.surfarray.make_surface(fisher_scores_images[1]), (FIHSER_SCORE_SIZE[0], 0))
        screen.blit(pygame.surfarray.make_surface(fisher_scores_images[2]), (0,FIHSER_SCORE_SIZE[1]))
        screen.blit(pygame.surfarray.make_surface(fisher_scores_images[3]), (FIHSER_SCORE_SIZE))
        under_grid_image = cv2.flip(cv2.rotate(cv2.cvtColor(cv2.resize(cv2.imread(str(FAKE_IMAGE_FOR_GRID),cv2.IMREAD_COLOR),FIHSER_SCORE_SIZE),cv2.COLOR_BGR2RGB),cv2.ROTATE_90_COUNTERCLOCKWISE),0)
        screen.blit(pygame.surfarray.make_surface(under_grid_image), (FIHSER_SCORE_SIZE[0]*2,FIHSER_SCORE_SIZE[1]))
        
        draw_grid(selected_cells) # draws inteactive grid on top of the bottom image
        
        # Draw grid for channel selection
        num = 1
        for row in range(0,CHANNELS_GRID_ROWS):
            for col in range(0,CHANNELS_GRID_COLUMNS):
                x = FIHSER_SCORE_SIZE[0]*2 + GRID_MARGIN + col * (CELL_SIZE + GRID_MARGIN)
                y = GRID_MARGIN + row * (CELL_SIZE + GRID_MARGIN)
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
        button_color = BUTTON_HOVER_COLOR if BUTTON_X + FIHSER_SCORE_SIZE[0]*2 <= mx <= BUTTON_X + FIHSER_SCORE_SIZE[0]*2 + BUTTON_WIDTH and BUTTON_Y  <= my <= BUTTON_Y + BUTTON_HEIGHT else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, (BUTTON_X + FIHSER_SCORE_SIZE[0]*2, BUTTON_Y , BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, BLACK, (BUTTON_X + FIHSER_SCORE_SIZE[0]*2, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
        button_text = button_font.render("Show ERD/ERS spectrograms of selected channels", True, BLACK)
        button_text_rect = button_text.get_rect(center=(BUTTON_X + FIHSER_SCORE_SIZE[0]*2 + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
        screen.blit(button_text, button_text_rect)
        
        text = "REMAINING SAMPLES TO CLASSIFY: " + str(len(retrieved_samples)-sample_index)
        counter_text = button_font.render(text, True, BLACK)
        counter_text_rect = counter_text.get_rect(center=(BUTTON_X + FIHSER_SCORE_SIZE[0]*2 + BUTTON_WIDTH // 2, FIHSER_SCORE_SIZE[1]*0.85 + BUTTON_HEIGHT // 2))
        screen.blit(counter_text, counter_text_rect)

        # Button for closing all figures opened
        mx, my = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER_COLOR if BUTTON_X + FIHSER_SCORE_SIZE[0]*2 <= mx <= BUTTON_X + BUTTON_WIDTH + FIHSER_SCORE_SIZE[0]*2 and FIHSER_SCORE_SIZE[1]*0.72 <= my <= FIHSER_SCORE_SIZE[1]*0.72 + BUTTON_HEIGHT else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, (BUTTON_X + FIHSER_SCORE_SIZE[0]*2, FIHSER_SCORE_SIZE[1]*0.72, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, BLACK, (BUTTON_X + FIHSER_SCORE_SIZE[0]*2, FIHSER_SCORE_SIZE[1]*0.72, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
        button_text = button_font.render("Close all images", True, BLACK,)
        button_text_rect = button_text.get_rect(center=(BUTTON_X + FIHSER_SCORE_SIZE[0]*2 + BUTTON_WIDTH // 2, FIHSER_SCORE_SIZE[1]*0.72 + BUTTON_HEIGHT // 2))
        screen.blit(button_text, button_text_rect)

        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # DEFINE THE VARIOUS EVENTS FOR THE MOUSE POSITIONS WHEN CLICKING --> GRID BUTTON, MU TOPOPLOT, BETA TOPOPLOT, CHANNEL POSITION TOPOPLOTS
                
                if FIHSER_SCORE_SIZE[0]*2 + BUTTON_X <= mx <= FIHSER_SCORE_SIZE[0]*2 + BUTTON_X + BUTTON_WIDTH and FIHSER_SCORE_SIZE[1]*0.72 <= my <= FIHSER_SCORE_SIZE[1]*0.72 + BUTTON_HEIGHT:
                    try:
                        cv2.destroyAllWindows()
                    except: # only to avoid crashes
                        pass
                        
                elif BUTTON_X + FIHSER_SCORE_SIZE[0]*2 <= mx <= BUTTON_X + FIHSER_SCORE_SIZE[0]*2 + BUTTON_WIDTH and BUTTON_Y <= my <= BUTTON_Y + BUTTON_HEIGHT: # channel specific info button
                    
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
                                    cv2.waitKey(2000)
                    
                    grid = [[False for _ in range(CHANNELS_GRID_COLUMNS)] for _ in range(CHANNELS_GRID_ROWS)]
                    
                else:
                    for row in range(CHANNELS_GRID_ROWS):
                        for col in range(CHANNELS_GRID_COLUMNS):
                            x = FIHSER_SCORE_SIZE[0]*2 + GRID_MARGIN + col * (CELL_SIZE + GRID_MARGIN)
                            y = GRID_MARGIN + row * (CELL_SIZE + GRID_MARGIN)
                            if x <= mx <= x + CELL_SIZE and y <= my <= y + CELL_SIZE:
                                grid[row][col] = not grid[row][col]
                                
                img_cell_index = get_cell_index_from_pos(event.pos)
                if img_cell_index is not None:
                    if selected_cells[img_cell_index] == 1:
                        selected_cells[img_cell_index] = 0
                    else:
                        selected_cells[img_cell_index] = 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    save_selected_cells((current_sample.parts)[-1], selected_cells)
                    update_sample_tracking(SAMPLE_TRACKING_FILE,(current_sample.parts)[-1])
                    sample_index += 1
                    loaded = False
                    selected_cells[:] = 0 # Clear selected cells when moving to the next image
                    cv2.destroyAllWindows()
                    break  # Move to the next image
                    
        clock.tick(15)


pygame.quit()
