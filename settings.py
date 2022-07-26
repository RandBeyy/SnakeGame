class Settings:

    def __init__(self):
        #Screen settings
        self.screen_size = (800, 800)
        self.bg_color = (240, 240, 240)
        

        #Cell settings
        cells_in_row, cells_in_column = (16, 16)
        self.cellx_size = self.screen_size[0] // cells_in_row
        self.celly_size = self.screen_size[1] // cells_in_column
        self.gray_cell_color = (200, 200, 200)
        self.white_cell_color = (240, 240, 240)

        #Snake settings
        self.snake_segment_size = (48, 48)
        self.segment_color = (0,0,0)
        self.amount_of_segment_at_start = 2
        self.snake_speed = 200          #In miliseconds

        #Fruit settings
        self.fruit_size = (48, 48)
        self.fruit_color = (255,0,0)
        self.score_points = 5

        #Text settings
        self.black = (0,0,0)
        self.red = (255,0,0)
