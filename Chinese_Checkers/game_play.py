import pygame
import sys
from copy import deepcopy
import math

color_light = (202, 203, 213)
color_dark = (22, 22, 22)
color_purple = (106, 13, 173)
color_green = (0, 155, 119)


def TwoPlayers(level):
    pygame.init()

    import numpy
    # initialize matrix values to 1
    matrix = numpy.ones((17, 25))

    # set all matrix valuest to -1
    matrix *= -1

    # The Initial positions of the marbles for each of the players
    first_player = [[0, 12], [1, 11], [1, 13], [2, 10], [
        2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]]
    second_player = [[16, 12], [15, 11], [15, 13], [14, 10], [
        14, 12], [14, 14], [13, 9], [13, 11], [13, 13], [13, 15]]

    move_index = [[-1, -1], [-1, 1], [0, 2], [1, 1], [1, -1], [0, -2]]

    matrix_index = [1, 2, 3, 4, 13, 12, 11, 10, 9]
    for i in range(9):
        j = 12
        first_time = True
        while matrix_index[i] > 0:
            if (i % 2 == 0) and first_time:
                first_time = False
                # print(i,j)
                matrix[i][j] = matrix[16 - i][j] = 0

                matrix_index[i] -= 1
            else:
                j -= 1
                matrix[i][j] = matrix[i][24 - j] = matrix[16 -
                                                          i][j] = matrix[16 - i][24 - j] = 0
                matrix_index[i] -= 2
            j -= 1

    # Matrix modification for player no.
    def add_player(index):
        if index == 1:
            for i in range(len(first_player)):
                matrix[first_player[i][0]][first_player[i][1]] = index
        if index == 2:
            for i in range(len(second_player)):
                matrix[second_player[i][0]][second_player[i][1]] = index

    # Adding players' marbles
    class Filling:
        def __init__(self):
            self_x = 0
            self_y = 0

        def marble(self):
            colors = [(240, 230, 230), "red", "green"]
            for i in range(0, 17):
                for j in range(0, 25):
                    if matrix[i][j] >= 0:
                        rect = pygame.Rect(
                            j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        marble_rect.append(pygame.draw.rect(
                            screen, colors[int(matrix[i][j])], rect, border_radius=20))

    def valid_moves(coor):
        valid_index = []
        for i in range(len(move_index)):
            x = coor[0] + move_index[i][0]
            y = coor[1] + move_index[i][1]
            if -1 < x < 17 and -1 < y < 25:
                if matrix[x][y] == 0:
                    valid_index.append([x, y])
                elif matrix[x][y] != -1:
                    check_path(move_index[i], x, y, valid_index)

        return valid_index

    # Possible Jumps
    def check_path(path_coor, x, y, moves_array):
        # print('before:', x, y)
        x2 = x + path_coor[0]
        y2 = y + path_coor[1]
        if [x2, y2] not in moves_array:
            if -1 < x2 < 17 and -1 < y2 < 25:
                if matrix[x2][y2] == 0:
                    moves_array.append([x2, y2])
                    for j in range(len(move_index)):
                        x3 = x2 + move_index[j][0]
                        y3 = y2 + move_index[j][1]
                        if [x3, y3] not in moves_array:
                            if -1 < x3 < 17 and -1 < y3 < 25:
                                if matrix[x3][y3] > 0:
                                    check_path(
                                        move_index[j], x3, y3, moves_array)

    # Move Function
    def move(pos, target):
        matrix[target[0]][target[1]] = matrix[pos[0]][pos[1]]
        matrix[pos[0]][pos[1]] = 0

    def move2(pos, target, matrixCpy):
        matrixCpy[target[0]][target[1]] = matrixCpy[pos[0]][pos[1]]
        matrixCpy[pos[0]][pos[1]] = 0

    def fullyOccupiedCol(playerIndex, col, matrixCpy):
        if(playerIndex == 2):
            for pos in first_player:
                if pos[1] == col:
                    if matrixCpy[pos[0]][pos[1]] != playerIndex:
                        return False
        elif (playerIndex == 1):
            for pos in second_player:
                if pos[1] == col:
                    if matrixCpy[pos[0]][pos[1]] != playerIndex:
                        return False
        return True

    # Calculate avg distance
    def calculateAvgDistance(playerIndex, matrixCpy):
        xend = 0
        yend = 0
        totalDistance = 0
        if (playerIndex == 1):
            xend = 18
        elif (playerIndex == 2):
            xend = -2

        for i in range(len(matrixCpy)):
            for j in range(len(matrixCpy[i])):
                if (matrixCpy[i][j] == playerIndex):
                    yend = calculateYend(matrixCpy, playerIndex)
                    totalDistance += math.sqrt(((xend - i)
                                                ** 2) + ((yend - j) ** 2))
        return totalDistance / 10

    def calculateYend(matrixCpy, playerIndex):
        unoccupied = 0
        unoccupiedw2 = 0
        yend = 0
        if playerIndex == 1:
            for pos in second_player:
                if matrixCpy[pos[0]][pos[1]] != playerIndex:
                    unoccupied += (matrixCpy[pos[0]][pos[1]] != 0)
                    unoccupiedw2 += (matrixCpy[pos[0]][pos[1]] == 0)
                    yend += pos[1] + pos[1] * \
                        (19*(matrixCpy[pos[0]][pos[1]] == 0))
        elif playerIndex == 2:
            for pos in first_player:
                if matrixCpy[pos[0]][pos[1]] != playerIndex:
                    unoccupied += (matrixCpy[pos[0]][pos[1]] != 0)
                    unoccupiedw2 += (matrixCpy[pos[0]][pos[1]] == 0)
                    yend += pos[1] + pos[1] * \
                        (19*(matrixCpy[pos[0]][pos[1]] == 0))
        if unoccupied == 0 and unoccupiedw2 == 0:
            return 12
        yend /= (unoccupied + 20*unoccupiedw2)
        if yend <= 12.5:
            return 12
        else:
            return 13

    # calculate score
    def calculateScore(matrixCpy):
        return calculateAvgDistance(1, matrixCpy) - calculateAvgDistance(2, matrixCpy)

    def getMoveNewMatrix(newMatrix=[]):
        movefrom = []
        moveTo = []
        x = 0
        for i in range(len(newMatrix)):
            for j in range(len(newMatrix[i])):
                if (matrix[i][j] != newMatrix[i][j]):
                    x += 1
                    if (newMatrix[i][j] == 0):
                        movefrom = [i, j]
                    else:
                        moveTo = [i, j]
        return [x, movefrom, moveTo]

    def minimax(matrixCpy, depth, max_player):
        if depth == 0 or winnerCpy(matrixCpy):
            return calculateScore(matrixCpy), matrixCpy
        playerIndex = 0
        if (max_player):
            playerIndex = 2
        else:
            playerIndex = 1
        if max_player:
            maxEval = float('-inf')
            best_move = None
            for state in get_all_picecs_moves(matrixCpy, playerIndex):
                score = minimax(state, depth - 1, False)[0]
                maxEval = max(maxEval, score)
                if maxEval == score:
                    best_move = state

            return maxEval, best_move
        else:
            minEval = float('inf')
            best_move = None
            for state in get_all_picecs_moves(matrixCpy, playerIndex):
                score = minimax(state, depth - 1, True)[0]
                minEval = min(minEval, score)
                if minEval == score:
                    best_move = state
            return minEval, best_move

    # the coordinates relative to the grid

    # get all

    def get_all_picecs_moves(matrixCpy, playerIndex):
        matrices = []
        for i in range(len(matrixCpy)):
            for j in range(len(matrixCpy[i])):
                if (matrix[i][j] == playerIndex):
                    moves = valid_moves((i, j))
                    for movei in moves:
                        matrixCpy2 = deepcopy(matrixCpy)
                        move2((i, j), movei, matrixCpy2)
                        matrices.append(matrixCpy2)
        return matrices

    def get_token_coor(x, y):
        grid_width = 0
        grid_heigth = 0
        coor = [int((y - grid_heigth) / 20), int((x - grid_width) / 20)]
        return coor

    # Show possible moves
    def animation(moves=[], clicked_token=None):
        colors = [(240, 230, 230), "red", "green"]
        moves.append(clicked_token)
        for i in range(0, 17):
            for j in range(0, 25):
                if matrix[i][j] >= 0:
                    rect = pygame.Rect(j * CELL_SIZE, i *
                                       CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    marble_rect.append(pygame.draw.rect(
                        screen, colors[int(matrix[i][j])], rect, border_radius=20))
                if [i, j] in moves:
                    test_circle = pygame.image.load('circle.png')
                    test_circle = pygame.transform.scale(
                        test_circle, (CELL_SIZE + 2, CELL_SIZE + 2))
                    screen.blit(
                        test_circle, (j * CELL_SIZE - 1, i * CELL_SIZE - 1))

    # Draw grid
    def show_grid():
        for i in range(0, nb_col):
            for j in range(0, nb_ligne):
                rect = pygame.Rect(i * CELL_SIZE, j *
                                   CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, pygame.Color("white"), rect, width=1)

    # function to add text to the screen
    def WriteText(text, text_pos_x, text_pos_y, text_size, col):
        text_font = pygame.font.SysFont(None, text_size)
        text_render = text_font.render(text, True, col)
        screen.blit(text_render, (text_pos_x, text_pos_y))

    # display the winner
    def winner():
        first = True
        second = True
        for i in range(len(first_player)):
            if matrix[first_player[i][0]][first_player[i][1]] != 2:
                second = False
                break
        for i in range(len(second_player)):
            if matrix[second_player[i][0]][second_player[i][1]] != 1:
                first = False
                break
        if second == True:
            WriteText('Player 2 had won!', nb_col * CELL_SIZE - 370,
                      nb_ligne * CELL_SIZE - 130, 50, "green")
            return True

        elif first == True:
            WriteText('Player 1 had won!', nb_col * CELL_SIZE - 370,
                      nb_ligne * CELL_SIZE - 130, 50, "red")
            return True
        else:
            return False

    def winnerCpy(matrixCpy):
        first = True
        second = True
        for i in range(len(first_player)):
            if matrixCpy[first_player[i][0]][first_player[i][1]] != 2:
                second = False
                break
        for i in range(len(second_player)):
            if matrixCpy[second_player[i][0]][second_player[i][1]] != 1:
                first = False
                break
        return first or second
    add_player(1)
    add_player(2)
    # game window display
    nb_col = 25
    nb_ligne = 25
    CELL_SIZE = 20
    screen = pygame.display.set_mode(
        size=(nb_col * CELL_SIZE, nb_ligne * CELL_SIZE))
    timer = pygame.time.Clock()
    game_on = True
    marble_rect = []
    players = Filling()
    screen.fill(pygame.Color(color_dark))
    players.marble()
    player_index = 1
    is_selecting = False
    player_valid_moves = []
    last_selected_token = []

    # Button Functions
    def text_objects(text, font):
        textsurface = font.render(text, True, "white")
        return textsurface, textsurface.get_rect()

    def button(msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))
        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(textSurf, textRect)
    playerwon = False
    AiWon = False
    while game_on:
        # player turn
        if player_index == 2:
            col = "green"
        if player_index == 1:
            col = "red"
        if (not winnerCpy(matrix)):
            WriteText('Player ' + str(player_index) + '\'s Turn', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100,
                      50, col)
        else:
            if playerwon:
                col = "red"
                WriteText('Player Wins', nb_col * CELL_SIZE - 370,
                          nb_ligne * CELL_SIZE - 100,
                          50, col)
            else:
                col = "green"
                WriteText('AI Wins', nb_col * CELL_SIZE - 370,
                          nb_ligne * CELL_SIZE - 100,
                          50, col)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (player_index == 1 and not winnerCpy(matrix)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # get a list of all sprites that are under the mouse cursor
                    clicked_sprites = [
                        s for s in marble_rect if s.collidepoint(pos)]
                    if clicked_sprites:
                        clicked_token = get_token_coor(
                            clicked_sprites[0].x, clicked_sprites[0].y)
                        if matrix[clicked_token[0], clicked_token[1]] == player_index:
                            if clicked_token == last_selected_token:
                                is_selecting = False
                                last_selected_token = []
                                player_valid_moves = []
                                screen.fill(pygame.Color(color_dark))
                                animation()
                            else:
                                player_valid_moves = valid_moves(clicked_token)
                                last_selected_token = clicked_token
                                is_selecting = True
                                screen.fill(pygame.Color(color_dark))
                                animation(player_valid_moves,
                                          last_selected_token)
                        elif clicked_token in player_valid_moves:
                            move(last_selected_token, clicked_token)
                            if winnerCpy(matrix):
                                WriteText('Player Wins', nb_col * CELL_SIZE - 370,
                                          nb_ligne * CELL_SIZE - 100,
                                          50, col)
                                playerwon = True
                            is_selecting = False
                            last_selected_token = []
                            player_valid_moves = []
                            screen.fill(pygame.Color(color_dark))
                            player_index = (player_index + 1) % 3
                            if player_index == 0:
                                player_index += 1
                            animation()
            else:
                if not winnerCpy(matrix):
                    newMatrix = minimax(matrix, level, True)[1]
                    lz = getMoveNewMatrix(
                        newMatrix)
                    x = lz[0]
                    last_selected_token = lz[1]
                    clicked_token = lz[2]
                    move(last_selected_token, clicked_token)
                    if winnerCpy(matrix):
                        WriteText('AI Wins', nb_col * CELL_SIZE - 370,
                                  nb_ligne * CELL_SIZE - 100,
                                  50, col)
                        AiWon = True
                    is_selecting = False
                    last_selected_token = []
                    player_valid_moves = []
                    screen.fill(pygame.Color(color_dark))
                    player_index = (player_index + 1) % 3
                    if player_index == 0:
                        player_index += 1
                    animation()
        pygame.display.update()
        timer.tick(60)
