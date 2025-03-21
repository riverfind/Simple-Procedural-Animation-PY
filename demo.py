import pygame
import math
import pygame.gfxdraw
# pygame setup
pygame.init()
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
running = True


# initialize 5 core points
leading_point = (screen_size[0]//2, screen_size[1]//2) 
radius = 60
maximum_cos = -1 / 2
coordinates = list((leading_point[0], leading_point[1] - i * radius)
                           for i in range(5))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        screen.fill("white")
        
        # Update coordinates
        coordinates[0] = pygame.mouse.get_pos()
        for i in range(1, len(coordinates)):

            # Distance Constrain
            delta_x = coordinates[i][0] - coordinates[i-1][0]
            delta_y = coordinates[i][1] - coordinates[i-1][1]
            distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
            radio = radius / distance
            
            new_delta_x = delta_x * radio
            new_delta_y = delta_y * radio
            
            new_coordinate = (int(coordinates[i-1][0] + new_delta_x),
                              int(coordinates[i-1][1] + new_delta_y))
            # Angle Constrain
            if i > 1:
                vec_CB_x = delta_x
                vec_CB_y = delta_y
                length_CB = math.sqrt(vec_CB_x ** 2 + vec_CB_y ** 2)

                vec_AB_x = coordinates[i-2][0] - coordinates[i-1][0]
                vec_AB_y = coordinates[i-2][1] - coordinates[i-1][1]
                length_AB = math.sqrt(vec_AB_x ** 2 + vec_AB_y ** 2)

                dot_product_ABCB = vec_AB_x * vec_CB_x + vec_AB_y * vec_CB_y
                cos_ABC = dot_product_ABCB / (length_AB * length_CB)
                
                
                if cos_ABC >= maximum_cos:
                    new_dot_product_ABCB = maximum_cos * length_AB * radius
                    parallel_AB_CB_radio = new_dot_product_ABCB  \
                                            / (length_AB ** 2)

                    parallel_AB_CB_x = parallel_AB_CB_radio * vec_AB_x
                    parallel_AB_CB_y = parallel_AB_CB_radio * vec_AB_y

                    vectical_AB_CB_length = math.sqrt(
                            radius ** 2 - 
                            parallel_AB_CB_x ** 2 + parallel_AB_CB_y ** 2
                            )

                    vectical_AB_CB_x_1 = vectical_AB_CB_length / length_AB \
                            * -1 * vec_AB_y
                    vectical_AB_CB_y_1 = vectical_AB_CB_length / length_AB \
                            * vec_AB_x

                    vectical_AB_CB_x_2 = vectical_AB_CB_length / length_AB \
                            * vec_AB_y
                    vectical_AB_CB_y_2 = vectical_AB_CB_length / length_AB \
                            * vec_AB_x * -1

                    new_delta_x_1 = parallel_AB_CB_x + vectical_AB_CB_x_1
                    new_delta_y_1 = parallel_AB_CB_y + vectical_AB_CB_y_1
                    new_delta_x_2 = parallel_AB_CB_x + vectical_AB_CB_x_2
                    new_delta_y_2 = parallel_AB_CB_y + vectical_AB_CB_y_2

                    candidate_1_x = coordinates[i-1][0] + new_delta_x_1
                    candidate_1_y = coordinates[i-1][1] + new_delta_y_1
                    candidate_1_movement = \
                            (candidate_1_x - coordinates[i][0]) ** 2 + \
                            (candidate_1_y - coordinates[i][1]) ** 2

                    candidate_2_x = coordinates[i-1][0] + new_delta_x_2
                    candidate_2_y = coordinates[i-1][1] + new_delta_y_2
                    candidate_2_movement = \
                            (candidate_2_x - coordinates[i][0]) ** 2 + \
                            (candidate_2_y - coordinates[i][1]) ** 2

                    if candidate_1_movement < candidate_2_movement:
                        new_coordinate = (int(candidate_1_x),
                                          int(candidate_1_y))
                    else:
                        new_coordinate = (int(candidate_2_x),
                                          int(candidate_2_y))


            coordinates[i] = new_coordinate


        # Draw the items
        pygame.draw.aalines(screen, (0,0,0), False, coordinates)
        for item in coordinates:
            pygame.gfxdraw.pixel(screen,
                                 item[0],
                                 item[1],
                                 (255, 0, 0))
            pygame.gfxdraw.aacircle(screen,
                                    item[0],
                                    item[1],
                                    radius,
                                    (0, 0, 0))
        
        # Update Screen
        pygame.display.flip()

        clock.tick(60)

pygame.quit()
