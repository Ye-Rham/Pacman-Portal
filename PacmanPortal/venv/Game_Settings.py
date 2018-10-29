class Settings:
    def __init__(self):
        self.screen_width = 675
        self.screen_height = 900
        self.bg_color = (0, 0, 0)
        self.text_color1 = (200, 200, 200)
        self.button_color = (0, 0, 50)
        self.game_on = False
        self.score_on = False

        self.block_width = self.screen_height * 3/4 / 60
        self.block_height = self.screen_height * 3/4 / 60
        self.block_color = (0, 0, 150)

        self.pellet_width = self.block_width * 5/9
        self.pellet_height = self.block_height * 5/9
        self.pellet_color = (250, 185, 176)

        self.power_pellet_width = self.block_width * 2
        self.power_pellet_height = self.block_width * 2

        self.entity_width = self.block_width * 3
        self.entity_height = self.block_height * 3

        self.bullet_width = self.block_width
        self.bullet_height = self.block_height

        self.portal_length = self.block_width * 3
        self.portal_width = self.block_width

        self.text_width = self.block_width
        self.text_height = self.text_width * 7 / 5

        self.pacman_speed = None
        self.ghost_speed = None
        self.bullet_speed = 10

        self.pellet_value = 10
        self.power_pellet_value = 50
        self.fruit_value = (100, 300, 500, 700, 1000, 2000, 3000, 5000)
        self.speed_adder = 1

        self.initiate_dynamic_variables()

    def initiate_dynamic_variables(self):
        self.pacman_speed = int(self.block_width / 3)
        self.ghost_speed = self.pacman_speed - 1

    def level_up(self, score):
        score.level += 1
        if score.level % 3 == 0:
            if self.pacman_speed < self.block_width:
                self.pacman_speed += self.speed_adder
            if self.ghost_speed < self.block_width:
                self.ghost_speed += self.speed_adder
