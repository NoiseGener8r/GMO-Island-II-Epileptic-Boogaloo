# GMO Island II: Epileptic Boogaloo`
# By NoiseGenerator
# Licensed under GNU GPL

import pygame

# Global Constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Images

# Player
player_image_right = pygame.image.load('player_right.png')
player_image_left = pygame.image.load('player_left.png')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image_right
        self.new_x = 0
        self.new_y = 0
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += self.new_x
    # Player-controlled movement:
    def go_left(self):
        self.change_x = -6
        self.image = player_image_left
    def go_right(self):
        self.change_x = 6
        self.image = player_image_right
    def stop(self):
        self.change_x = 0    

def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("GMO Island II: Epileptic Boogaloo")
    
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()    
    
    # -------- Main Program Loop -----------
    while not done:
        
        active_sprite_list = pygame.sprite.Group()
        
        player = Player()
        player.rect.x = 340
        player.rect.y = SCREEN_HEIGHT - player.rect.height
        active_sprite_list.add(player)        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.new_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.new_x > 0:
                    player.stop()
        
        active_sprite_list.update() 
        
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        active_sprite_list.draw(screen)
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        
        # Limit to 60 frames per second
        clock.tick(60)
        
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()    



if __name__ == "__main__":
    main()