from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Deque, Dict, List, Set

# Места в кинотеатре расположены в один ряд. Только что пришедший зритель выбирает место, чтобы сидеть максимально далеко от остальных зрителей в ряду.
# То есть расстояние от того места, куда сядет зритель до ближайшего к нему зрителя должно быть максимально.
# Гарантируется, что в ряду всегда есть свободные места и уже сидит хотя бы один зритель.
# Напишите функцию, которая по заданному ряду мест (массиву из нулей и единиц) вернёт расстояние от выбранного пришедшим зрителем места до другого ближайшего зрителя.


def f(s: List[int]) -> int:
    max_len = 0
    cur_len = 0
    for i, c in enumerate(s):
        if c == 0:
            cur_len += 1
        else:
            if cur_len > max_len:
                max_len = cur_len
            cur_len = 0

    if cur_len > max_len:
        max_len = cur_len

    first_zeroes = 0
    for c in s:
        if c == 0:
            first_zeroes += 1
        else:
            break
    last_zeroes = 0
    for c in reversed(s):
        if c == 0:
            last_zeroes += 1
        else:
            break

    return max([first_zeroes - 1, last_zeroes - 1, int((max_len - 1) / 2)])


# Есть последовательность событий, каждое событие это пара user_id, time , события отсортированы по времени.
# Нужно уметь отвечать на вопрос, сколько за последние 5 минут было пользователей, которые задали >= 1000 запросов.

# class RobotStatistics {
#   void OnEvent(time_t now, int userId);
#   int GetRobotCount(time_t now);
# };


@dataclass
class Elem:
    t: datetime
    user_id: str


class Statistics:
    def __init__(self):
        self.queue: Deque[Elem] = deque([])
        self.user_count: Dict[str, int] = {}
        self.user_set: Set[str] = set()

    def on_event(self, now: datetime, user_id: str) -> None:
        self.clean_queue(now)
        self.queue.append(Elem(user_id=user_id, t=now))
        self.user_count.setdefault(user_id, 0)
        self.user_count[user_id] += 1
        if self.user_count == 1000:
            self.user_set.add(user_id)

    def get_robot_count(self, now: datetime) -> int:
        self.clean_queue(now)
        return len(self.user_set)

    def clean_queue(self, now: datetime) -> None:
        while len(self.queue):
            elem = self.queue[0]
            if elem.t < now - timedelta(minutes=5):
                self.queue.popleft()
                self.user_count[elem.user_id] -= 1
                if self.user_count[elem.user_id] == 999:
                    self.user_set.remove(elem.user_id)
                if self.user_count[elem.user_id] == 0:
                    self.user_count.pop(elem.user_id)
            else:
                return
