import hlt
import logging


class Bot:

    def __init__(self, name):
        self.name = name
        logging.info("Starting my {} bot!".format(name))
        self.speed = hlt.constants.MAX_SPEED
        # self.speed = int(hlt.constants.MAX_SPEED / 2)

    def play(self):
        # Starting game
        game = hlt.Game(self.name)

        while True:
            # TURN START
            game_map = game.update_map()

            command_queue = []
            ships = game_map.get_me().all_ships()
            for ship in ships:
                if ship.docking_status != ship.DockingStatus.UNDOCKED:
                    continue

                entities_by_distance = game_map.nearby_entities_by_distance(ship)
                nearest_planet = None
                for distance in sorted(entities_by_distance):
                    nearest_planet = next((nearest_entity for nearest_entity in entities_by_distance[distance]
                                           if isinstance(nearest_entity, hlt.entity.Planet)), None)

                    if nearest_planet is None or nearest_planet.is_owned():
                        continue
                    else:
                        break

                nearest_ship = None
                for distance in sorted(entities_by_distance):
                    nearest_ship = next((nearest_entity for nearest_entity in entities_by_distance[distance] if
                                         isinstance(nearest_entity, hlt.entity.Ship) and nearest_entity not in ships),
                                        None)

                    if nearest_ship is None:
                        continue
                    else:
                        break

                planets = game_map.all_planets()
                all_ships = [s for s in game_map._all_ships() if s not in ships]
                planet = nearest_planet
                if planet is not None and ship.can_dock(planet):
                    command_queue.append(ship.dock(planet))
                else:
                    if planet is None or nearest_planet.calculate_distance_between(ship) > nearest_ship.calculate_distance_between(ship):
                        entity_to_move_towards = nearest_ship
                    else:
                        entity_to_move_towards = nearest_planet
                    navigate_command = ship.navigate(
                        ship.closest_point_to(entity_to_move_towards),
                        game_map,
                        speed=self.speed,
                        ignore_ships=True)
                    if navigate_command:
                        command_queue.append(navigate_command)

            game.send_command_queue(command_queue)
            # TURN END
        # GAME END


bot = Bot("Settler_V5")
bot.play()




