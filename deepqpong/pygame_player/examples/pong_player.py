from pygame.constants import K_DOWN
from deepqpong.pygame_player.pygame_player import PyGamePlayer





class PongPlayer2(PyGamePlayer):
    def __init__(self, force_game_fps=10, run_real_time=False):
        """
        Example class for playing Pong
        """
        super(PongPlayer, self).__init__(force_game_fps=force_game_fps, run_real_time=run_real_time)
        self.last_bar1_score = 0.0
        self.last_bar2_score = 0.0

    def get_keys_pressed(self, screen_array, feedback, terminal):
        # TODO: put an actual learning agent here
        return [K_DOWN]

    def get_feedback(self):
        # import must be done here because otherwise importing would cause the game to start playing
        from deepqpong.pygame_player.games.pong import bar1_score, bar2_score

        # # get the difference in score between this and the last run
        score_change = (bar1_score - self.last_bar1_score) - (bar2_score - self.last_bar2_score)
        self.last_bar1_score = bar1_score
        self.last_bar2_score = bar2_score

        return float(score_change), score_change != 0

    def start(self):
        import time, random
        random.seed(time.time)
        super(PongPlayer, self).start()
        from deepqpong.pygame_player.games import pong




class PongPlayer(PyGamePlayer):
    def __init__(self, force_game_fps=10, run_real_time=False):
        """
        Example class for playing Pong
        """
        super(PongPlayer, self).__init__(force_game_fps=force_game_fps, run_real_time=run_real_time)
        self.last_bar1_score = 0.0
        self.last_bar2_score = 0.0

    def get_keys_pressed(self, screen_array, feedback, terminal):
        # TODO: put an actual learning agent here
        return [K_DOWN]

    def get_feedback(self):
        # import must be done here because otherwise importing would cause the game to start playing
        # from deepqpong.pygame_player.games.pong import bar1_score, bar2_score
        # # get the difference in score between this and the last run
        # score_change = (bar1_score - self.last_bar1_score) - (bar2_score - self.last_bar2_score)
        # self.last_bar1_score = bar1_score
        # self.last_bar2_score = bar2_score

        from deepqpong.pygame_player.games.pong2 import player1, player2

        # get the difference in score between this and the last run
        score_change = (player1.score - self.last_bar1_score) - (player2.score - self.last_bar2_score)
        self.last_bar1_score = player1.score
        self.last_bar2_score = player2.score

        return float(score_change), score_change != 0

    def start(self):
        import time, random
        random.seed(time.time)
        super(PongPlayer, self).start()
        from deepqpong.pygame_player.games import pong2



if __name__ == '__main__':
    player = PongPlayer()
    player.start()
