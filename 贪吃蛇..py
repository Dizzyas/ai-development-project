import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 游戏类
class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('贪吃蛇游戏')
        self.clock = pygame.time.Clock()
        self.reset_game()
    
    def reset_game(self):
        # 初始化蛇的位置和方向
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        
        # 生成食物
        self.food = self.generate_food()
        
        # 游戏状态
        self.score = 0
        self.game_over = False
    
    def generate_food(self):
        # 生成不在蛇身上的食物
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
    
    def update(self):
        if not self.game_over:
            # 更新方向
            self.direction = self.next_direction
            
            # 移动蛇头
            head = self.snake[0]
            new_head = ((head[0] + self.direction[0]) % GRID_WIDTH, 
                       (head[1] + self.direction[1]) % GRID_HEIGHT)
            
            # 检查是否碰撞到自身
            if new_head in self.snake:
                self.game_over = True
                return
            
            # 检查是否吃到食物
            if new_head == self.food:
                self.score += 10
                self.snake.insert(0, new_head)
                self.food = self.generate_food()
            else:
                self.snake.insert(0, new_head)
                self.snake.pop()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # 绘制分数（放在最前面确保显示）
        try:
            font = pygame.font.SysFont('SimHei', 36)
        except:
            font = pygame.font.Font(None, 36)
        score_text = font.render(f'分数: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 绘制蛇
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN, 
                           (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, 
                            GRID_SIZE, GRID_SIZE))
        
        # 绘制食物
        pygame.draw.rect(self.screen, RED, 
                       (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, 
                        GRID_SIZE, GRID_SIZE))
        
        # 绘制游戏结束界面
        if self.game_over:
            try:
                font = pygame.font.SysFont('SimHei', 72)
            except:
                font = pygame.font.Font(None, 72)
            game_over_text = font.render('游戏结束!', True, WHITE)
            restart_text = font.render('按R键重新开始', True, WHITE)
            self.screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (WIDTH // 2 - 180, HEIGHT // 2 + 20))
        
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # 控制游戏速度

# 运行游戏
if __name__ == '__main__':
    game = SnakeGame()
    game.run()