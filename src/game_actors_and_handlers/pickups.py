# coding=utf-8
import logging
from game_state.game_types import GamePickPickup, GamePickItem, GamePickup
from game_actors_and_handlers.base import BaseActor


logger = logging.getLogger(__name__)


class Pickuper(BaseActor):

    def perform_action(self):
        pickups = self._get_game_location().get_pickups()
        self.pick_pickups(pickups)

    def pick_pickups(self, pickups):
        if pickups:
            logger.info(u'Подбираем дроп...')
        for pickup in pickups:
            pick_event = GamePickPickup([pickup])
            self._get_events_sender().send_game_events([pick_event])
            self._get_game_location().remove_pickup(pickup)


class BoxPickuper(BaseActor):

    def perform_action(self):
        boxes = self._get_game_location().get_all_objects_by_type(
                                                    GamePickup.type)
        for box in boxes:
            name = self._get_item_reader().get_name(box)
            logger.info(u'Вскрываем ' + name)
            pick_event = GamePickItem(objId=box.id)
            self._get_events_sender().send_game_events([pick_event])
            self._get_game_location().remove_object_by_id(box.id)


class AddPickupHandler(object):
    def __init__(self, game_location):
        self.__game_loc = game_location

    def handle(self, event_to_handle):
        self.__game_loc.add_pickups(event_to_handle.pickups)
