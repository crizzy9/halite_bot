import hlt
import logging
from collections import OrderedDict


def log_stuff(stuff):
    with open('submissions/logfile.txt', 'a') as f:
        f.write(str(stuff) + '\n')


class Bot:

    def __init__(self, name):
        self.name = name
        logging.info("Starting my {} bot!".format(name))
        self.speed = hlt.constants.MAX_SPEED
        # self.speed = int(hlt.constants.MAX_SPEED / 2)

    def play(self):
        # Starting game
        game = hlt.Game(self.name)
        turns = 0

        while True:
            # TURN START
            turns += 1
            game_map = game.update_map()

            command_queue = []

            ships = game_map.get_me().all_ships()
            planets = game_map.all_planets()
            players = game_map.all_players()

            pid = game_map.get_me().id
            for ship in ships:
                if ship.docking_status != ship.DockingStatus.UNDOCKED:
                    continue

                entities_by_distance = game_map.nearby_entities_by_distance(ship)
                entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))
                closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

                # closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and not entities_by_distance[distance][0] not in ships]
                closest_enemy_ships = []

                # closest_enemy_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].owner is not None and not entities_by_distance[distance][0].owner.id != pid]
                closest_enemy_planets = []

                all_pids = [player.id for player in players]
                for id in all_pids:
                    if pid == id:
                        continue
                    else:
                        closest_enemy_planets = [planet for planet in planets if planet.owner is not None and planet.owner.id != pid]
                        closest_enemy_ships = [s for s in game_map._all_ships() if s not in ships]

                # if len(closest_enemy_planets) > 0:
                #     log_stuff("CEP")
                #     for planet in closest_enemy_planets:
                #         if planet.owner is not None:
                #             log_stuff(planet.owner.id)

                log_stuff("Turn:{} closes empty planets:{} closest enemy planets:{} closest enemy ships:{} ships: {}".format(turns, len(closest_empty_planets), len(closest_enemy_planets), len(closest_enemy_ships), len(ships)))

                if len(closest_empty_planets) > 0:
                    nearest_planet = closest_empty_planets[0]
                    if ship.can_dock(nearest_planet):
                        command_queue.append(ship.dock(nearest_planet))
                    else:
                        navigate_command = ship.navigate(
                            ship.closest_point_to(nearest_planet), game_map, speed=self.speed, ignore_ships=False)

                        if navigate_command:
                            command_queue.append(navigate_command)

                elif len(closest_enemy_ships) > 0:
                    nearest_ship = closest_enemy_ships[0]

                    navigate_command = ship.navigate(
                        ship.closest_point_to(nearest_ship), game_map, speed=self.speed, ignore_ships=False)

                    if navigate_command:
                        command_queue.append(navigate_command)

                else:
                    log_stuff("in else")
                    nearest_enemy_planet = closest_enemy_planets[0]
                    navigate_command = ship.navigate(
                        ship.closest_point_to(nearest_enemy_planet), game_map, speed=self.speed, ignore_ships=False)

                    if navigate_command:
                        command_queue.append(navigate_command)

                # elif len(closest_enemy_planets) > 0 and len(closest_enemy_ships) < 3 and len(ships) > 2:
                #     nearest_enemy_planet = closest_enemy_planets[0]
                #     navigate_command = ship.navigate(
                #         ship.closest_point_to(nearest_enemy_planet), game_map, speed=self.speed, ignore_ships=False)
                #
                #     if navigate_command:
                #         command_queue.append(navigate_command)

            game.send_command_queue(command_queue)
            # TURN END
        # GAME END


bot = Bot("exMachina_V7")
bot.play()




