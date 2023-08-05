import logging
import time

from eventlet.semaphore import Semaphore
from threading import Thread
from concurrent import futures

from simulation.worker import Worker

LOGGER = logging.getLogger(__name__)


class WorkerManager(object):
    """
    Methods of this class must be thread safe unless explicitly stated.
    """
    def __init__(self, port=5000):
        self.player_id_to_worker = {}
        self.port = port

    def get_code(self, player_id):
        return self.player_id_to_worker[player_id].code

    def fetch_all_worker_data(self, player_id_to_game_state):
        """
        Creates a thread for each worker to send a request for their data. After
        a set duration these threads will close, giving a consistent turn time.
        """
        def prepare_request_threads():
            return [Thread(target=worker.fetch_data,
                           args=(player_id_to_game_state[player_id],))
                    for (player_id, worker) in self.player_id_to_worker.items()]

        def timed_process_for_worker_turn_requests(duration):
            threads = prepare_request_threads()

            [thread.setDaemon(True) for thread in threads]
            [thread.start() for thread in threads]
            time.sleep(duration)

        timed_process_for_worker_turn_requests(2)

    def get_player_id_to_serialized_actions(self):
        return {player_id: self.player_id_to_worker[player_id].serialized_action for player_id in self.player_id_to_worker}

    def clear_logs(self):
        for worker in self.player_id_to_worker.values():
            worker.log = None

    def create_worker(self, player_id):
        raise NotImplementedError

    def remove_worker(self, player_id):
        raise NotImplementedError

    def update_code(self, player):
        self.player_id_to_worker[player['id']].code = player['code']

    def add_new_worker(self, player_id):
        worker_url_base = self.create_worker(player_id)
        self.player_id_to_worker[player_id] = Worker(f'{worker_url_base}/turn/')

    def _parallel_map(self, func, iterable_args):
        with futures.ThreadPoolExecutor() as executor:
            results = executor.map(func, iterable_args)

    def add_workers(self, users_to_add):
        self._parallel_map(self.add_new_worker, users_to_add)

    def delete_workers(self, players_to_delete):
        self._parallel_map(self.delete_worker, players_to_delete)

    def delete_worker(self, player):
        del self.player_id_to_worker[player]
        self.remove_worker(player)

    def update_worker_codes(self, players):
        self._parallel_map(self.update_code, players)
