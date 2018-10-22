#\\TODO: Start all levels at y = 300 and make ground kill you
   #Level 3: all moving platforms




# GMO Island II: Epileptic Boogaloo`
# By NoiseGenerator
# Licensed under GNU GPL

import pygame, random

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
player_image_block_large = pygame.image.load('player_block.png')
player_image_block = pygame.transform.scale(player_image_block_large, (30,37))
player_image_block_left = pygame.transform.flip(player_image_block, True, False)


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        
        self.image = player_image_right
        
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.new_x = 0
        self.new_y = 0
 
        # List of sprites we can bump against
        self.level = None
        
        self.blocktype = 0
        self.action = 1
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.new_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.new_x > 0:
                self.rect.right = block.rect.left
            elif self.new_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.new_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.new_y > 0:
                self.rect.bottom = block.rect.top
            elif self.new_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.new_y = 0
            
        
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.new_y == 0:
            self.new_y = 1
        else:
            self.new_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.new_y >= 0:
            self.new_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.new_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.new_x = -6
        self.image = player_image_left
        self.blocktype = 1
        self.action = 2
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.new_x = 6
        self.image = player_image_right
        self.blocktype = 0
        self.action = 1
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.new_x = 0 
        if self.action == 1:
            self.image = player_image_right
        elif self.action == 2:
            self.image = player_image_left
        elif self.action == 0: 
            if self.blocktype == 0:                
                self.action = 1 
                self.image = player_image_right
            elif self.blocktype == 1:
                self.action = 2     
                self.image = player_image_left
        
        
    def block(self):
        self.action = 0
        if self.blocktype == 0:
            self.image = player_image_block
        elif self.blocktype == 1:
            self.image = player_image_block_left
        
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
        screen.fill(WHITE)
 
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
            platform.image.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
 
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
        self.image.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
 
        self.rect = self.image.get_rect()
        
class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    change_x = 0
    change_y = 0
 
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
 
    player = None
 
    level = None
 
    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
 
            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom
 
        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1


class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
        self.level_limit = -250 # Change level size and exit position
        # Array with width, height, x, and y of platform
        level = [[210, 70, 480, 550],
                 [210, 70, 200, 400],
                 [900, 70, 690, 300],
                 [30, 300, 660, 300],
                 
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
            
            
class Level_02(Level):
    """ Definition for level 2. """
 
    def __init__(self, player):
        """ Create level 2. """
 
        # Call the parent constructor
        Level.__init__(self, player)
        self.level_limit = -1000 # Change level size and exit position
        # Array with width, height, x, and y of platform
        level = [[210, 70, 0, 300],
                 [20, 70, 280, 300],
                 [210, 70, 600, 300],
                 [2000, 70, 1150, 300],
                 [70, 500, 1200, 300]
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)  
            # Add a custom moving platform
            block = MovingPlatform(70, 30)
            block.rect.x = 210
            block.rect.y = 300
            block.boundary_top = 300
            block.boundary_bottom = 600
            block.change_y = -2
            block.player = self.player
            block.level = self
            self.platform_list.add(block)   
            
class Level_03(Level):
    """ Definition for level 3. """
 
    def __init__(self, player):
        """ Create level 3. """
 
        # Call the parent constructor
        Level.__init__(self, player)
        self.level_limit = -500 # Change level size and exit position
        # Array with width, height, x, and y of platform
        level = [[210, 70, 0, 300],
                 [210, 500, 210, 300]
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
            for i in range(5):
                # Add a custom moving platform
                block = MovingPlatform(210, 30)
                block.rect.x = 200+(200*i)
                block.rect.y = 300
                block.boundary_top = 300
                block.boundary_bottom = 600
                block.change_y = -2
                block.player = self.player
                block.level = self
                self.platform_list.add(block)
                
        
                        
        
        
        
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("GMO Island II: Epileptic Boogaloo")
    
    # Create the player
    player = Player()
 
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    all_sprites_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    all_sprites_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
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
                if event.key == pygame.K_DOWN:
                    player.block()
                
                    
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.new_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.new_x > 0:
                    player.stop()
                if event.key == pygame.K_UP and player.new_y == JUMP_FORCE:
                    player.stop()
                if event.key == pygame.K_DOWN:
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