# GMO Island II: Epileptic Boogaloo`
# By NoiseGenerator
# Licensed under GNU GPL

import pygame

# Global Constants

# Physics

GRAVITY = 1
JUMP_FORCE = -13

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
        self.jump_bool = False
        
    def update(self):
        self.rect.x += self.new_x
        self.rect.y += self.new_y
        # Gravity
        self.calc_grav()        
    # Player-controlled movement:
    def go_left(self):
        self.new_x = -6
        self.image = player_image_left
    def go_right(self):
        self.new_x = 6
        self.image = player_image_right
    def stop(self):
        self.new_x = 0
        self.new_y = 0
        
    def jump(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.new_y = JUMP_FORCE
        
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.new_y == 0:
            self.new_y = 1
        else:
            self.new_y += GRAVITY
    
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.new_y >= 0:
            self.new_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height    
        
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
     
        # How far this world has been scrolled left/right
        self.world_shift = 0
        self.level_limit = -1000
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(BLUE)
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything:
        """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
 
        self.rect = self.image.get_rect()

class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 500],
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
            
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("GMO Island II: Epileptic Boogaloo")
    
    # Loop until the user clicks the close button.
    done = False
    all_sprites_list = pygame.sprite.Group()
    player = Player()
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    all_sprites_list.add(player)    
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    #level_list.append(Level_02(player))    
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]    
        
         
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()  
    
 
    
    
       
    
    # -------- Main Program Loop -----------
    while not done:
        
                
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                    print('test')
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.new_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.new_x > 0:
                    player.stop()
                if event.key == pygame.K_UP and player.new_y == JUMP_FORCE:
                    player.stop()
        
        all_sprites_list.update() 
        # Update items in the level
        current_level.update()
    
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
    
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)
    
        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            if current_level_no < len(level_list)-1:
                player.rect.x = 120
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
            else:
                # Out of levels. This just exits the program.
                # You'll want to do something better.
                done = True      
        
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        all_sprites_list.draw(screen)
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