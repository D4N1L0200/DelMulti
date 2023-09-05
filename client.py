import pygame
import networking as net


class GameObject:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Square(GameObject):
    def __init__(self, x: int, y: int, size: int, color: tuple) -> None:
        super().__init__(x, y)
        self.size = size
        self.color = color


class Player(Square):
    def __init__(self, x: int, y: int, size: int, speed: int) -> None:
        super().__init__(x, y, size, (255, 255, 255))
        self.speed = speed


class Game:
    def __init__(self) -> None:
        self.width = 800
        self.height = 600
        # self.width = 400
        # self.height = 300

        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Multiplayer Square")
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.entities: dict = {"player": None, "players": {}}
        player = Player((self.width - 50) // 2, (self.height - 50) // 2, 50, 5)
        self.entities["player"] = player

    def joinplayer(self, clientid: int) -> None:
        self.entities["players"][clientid] = Square(-100, -100, 50, (255, 0, 0))

    def leaveplayer(self, clientid: int) -> None:
        del self.entities["players"][clientid]


# Initialize Client Socket
HOST: str = input("IP: ")
PORT: int = 12345

client = net.Client()
running = True
if not client.init_socket(HOST, PORT):
    running = False
    input("Press Enter to exit.")
else:
    game = Game()

while running:  # TODO: move to game class
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client.send(2400)
            running = False

    keys = pygame.key.get_pressed()  # TODO: move all of this to player class
    move_x = (keys[pygame.K_d] - keys[pygame.K_a]) * game.entities["player"].speed
    move_y = (keys[pygame.K_s] - keys[pygame.K_w]) * game.entities["player"].speed

    game.entities["player"].x = max(0, min(game.entities["player"].x + move_x, game.width - game.entities["player"].size))
    game.entities["player"].y = max(0, min(game.entities["player"].y + move_y, game.height - game.entities["player"].size))

    if client.current_data:
        for item in client.current_data:
            match item[:4]:
                case "1300":
                    for cid in map(int, item[4:].split(",")):
                        if cid != client.client_id:
                            game.joinplayer(cid)
                case "1302":
                    game.joinplayer(int(item[4:]))
                case "1401":
                    game.leaveplayer(int(item[4:]))
                case "1500":
                    print("Echo: " + item[4:])
                case "1501":
                    other_id, other_x, other_y = map(int, item[4:].split(","))
                    game.entities["players"][other_id].x = other_x
                    game.entities["players"][other_id].y = other_y
        client.clear_data()

    # if running:
    #     client.send(2500, f"{game.entities[0].x}, {game.entities[0].y}")

    if running:
        client.send(2501, f"{game.entities['player'].x}, {game.entities['player'].y}")

    game.screen.fill((0, 0, 0))
    for cid, square in game.entities["players"].items():
        pygame.draw.rect(game.screen, square.color, (square.x, square.y, square.size, square.size))
    pygame.draw.rect(game.screen, game.entities["player"].color, (game.entities["player"].x, game.entities["player"].y, game.entities["player"].size, game.entities["player"].size))

    pygame.display.flip()
    game.clock.tick(60)


pygame.quit()
