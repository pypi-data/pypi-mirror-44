import __main__ 
import requests


class Fg: 
        rs = "\033[00m"
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        orange = "\033[33m"
        blue = "\033[34m"
        purple = "\033[35m"
        cyan = "\033[36m"
        lightgrey = "\033[37m"
        darkgrey = "\033[90m"
        lightred = "\033[91m"
        lightgreen = "\033[92m"
        yellow = "\033[93m"
        lightblue = "\033[94m"
        pink = "\033[95m"
        lightcyan = "\033[96m"


class Bg: 
        rs = "\033[00m"
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        yellow = "\033[43m"
        blue = "\033[44m"
        magenta = "\033[45m"
        cyan = "\033[46m"
        white = "\033[47m"


class Directions:
    N = UP = 0
    S = DOWN = 180
    W = LEFT = 270
    E = RIGHT = 90


class Entity:
    def __init__(self, graphic, game, x, y, fg_color, bg_color):
        self.graphic = graphic
        self.game = game
        self.x = x
        self.y = y
        self.fg_color = fg_color
        self.bg_color = bg_color if bg_color is not None else game.bg_color

    def __str__(self):
        return "{}{} {} {}{}".format(self.fg_color, self.bg_color, self.graphic, Bg.rs, Fg.rs)


class Player(Entity):
    GRAPHICS = {
        0: "^",
        90: ">",
        180: "v",
        270: "<"
    }

    def __init__(self, game, x, y, direction):
        self.tail = [(x, y)]
        Entity.__init__(self, Player.GRAPHICS[direction], game, x, y, Fg.red, Bg.blue)
        self.tail_color = self.bg_color
        self.__moves = []
        self.__direction = direction

    def __set_direction(self, direction):
        if direction == 360:
            direction = 0
        elif direction == -90:
            direction = 270

        self.__direction = direction
        self.graphic = Player.GRAPHICS[direction]

    def get_moves(self):
        return self.__moves

    def get_direction(self):
        return self.__direction

    def turn(self, direction):
        if direction == Directions.RIGHT:
            self.__set_direction(self.__direction + 90)
        elif direction == Directions.LEFT:
            self.__set_direction(self.__direction - 90)

    def move(self, direction):
        if self.game.running:
            next_x = self.x
            next_y = self.y
            if direction == Directions.N and self.y > 0:
                next_y -= 1
            elif direction == Directions.S and self.y < self.game.h - 1:
                next_y += 1
            elif direction == Directions.W and self.x > 0:
                next_x -= 1
            elif direction == Directions.E and self.x < self.game.w - 1:
                next_x += 1

            e = self.game.get_entity_at_coords(next_x, next_y)

            self.x = next_x
            self.y = next_y
            self.__moves.append((self.x, self.y))
            if e is None:
                self.tail.append((self.x, self.y))
            else:
                self.bg_color = e.bg_color
                if type(e) in (Obstacle, Gold):
                    self.game.running = False


class Obstacle(Entity):
    def __init__(self, game, x, y):
        Entity.__init__(self, " ", game, x, y, Fg.lightgrey, Bg.black)
        

class Gold(Entity):
    def __init__(self, game, x, y):
        Entity.__init__(self, "$", game, x, y, Fg.yellow, Bg.yellow)

        
class Level:
    def __init__(self, level):
        self.__level_index = level - 1

        res = requests.get("{}/levels".format(Game.url), headers={"Accept": "application/json"})
        levels = res.json()
        level_data = list(levels.values())[self.__level_index]
        self.id = list(levels.keys())[self.__level_index]
        self.description = level_data["description"]
        self.max_moves = level_data["maxMoves"]
        rows = level_data["map"].split("\n")

        self.__entities = []
        self.__bg_color = Bg.white
        self.running = True

        self.h = len(rows) - 1
        self.w = len(rows[0])

        for y in range(self.h):
            for x in range(self.w):
                char = rows[y][x]
                if char == "$":
                    self.__entities.append(Gold(self, x, y))
                elif char in ("^", ">", "<", "v"):
                    if char == "^":
                        direction = Directions.UP
                    elif char == ">":
                        direction = Directions.RIGHT
                    elif char == "<":
                        direction = Directions.LEFT
                    else:
                        direction = Directions.DOWN

                    self.__player = Player(self, x, y, direction)
                    self.__entities.insert(0, self.__player)
                elif char != " ":
                    self.__entities.append(Obstacle(self, x, y))

    def move(self):
        self.__player.move(self.__player.get_direction())

    def turn_left(self):
        self.__player.turn(Directions.LEFT)

    def turn_right(self):
        self.__player.turn(Directions.RIGHT)

    def get_entity_at_coords(self, x, y):
        for e in self.__entities:
            if e.x == x and e.y == y: 
                return e     

    def go(self):
        print(self)
        code = open(__main__.__file__).read()
        r = requests.post("{}/solution/{}".format(Game.url, self.id), json={
            "code": code,
            "moves": self.__player.get_moves()
        })

        message = r.json()["message"]
        if r.status_code == 200:
            print("{}{}{}".format(Fg.green, message, Fg.rs))
        else:
            print("{}{}{}".format(Fg.red, message, Fg.rs))

    def __str__(self):
        out = "{} (massimo {} mosse):\n".format(self.description, self.max_moves)
        for y in range(self.h):
            for x in range(self.w):
                e = self.get_entity_at_coords(x, y)
                if e is not None:
                    out += str(e)
                elif (x, y) in self.__player.tail:
                    out += "{}   {}".format(self.__player.tail_color, Bg.rs)
                else:
                    out += "{}   {}".format(self.__bg_color, Bg.rs)

            out += "\n"

        return out


class Game:
    url = "http://192.168.1.231:8081"

    @staticmethod
    def sign(name):
        r = requests.post(
            "{}/accreditamento".format(Game.url),
            json={"name": name.upper()}
        ).json()

        print(r["message"])

    @staticmethod
    def start_level(number):
        return Level(number)
