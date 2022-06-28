import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    '''管理游戏资源和行为的类'''
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)        #创建一个覆盖全屏的游戏界面
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.bg_color = self.settings.bg_color                 #设置屏幕颜色
        pygame.display.set_caption('Alien Invasion')
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        '''开始游戏的主循环'''
        while True:
            self._check_events()
            self.ship.update()                              #刷新飞船的位置
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():                    #监视键盘和鼠标的事件
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        '''响应按键'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        '''响应松开键'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''创建一颗子弹，并将其加入编组bullets中。'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''更新子弹位置并删除消失的子弹'''
        #更新子弹位置
        self.bullets.update()
        #删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        '''更新屏幕上的图像，并切换到新屏幕。'''
        self.screen.fill(self.bg_color)                     # 给屏幕上色
        self.ship.blitme()                                  # 创建飞船
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        pygame.display.flip()                                #让最近绘制的屏幕可见


if __name__ == '__main__':
    ai = AlienInvasion()                                           #创建游戏实例并运行游戏
    ai.run_game()