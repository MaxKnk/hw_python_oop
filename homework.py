from dataclasses import dataclass
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float
    ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_minutes: float = self.duration * self.MIN_IN_H
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * super().get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * duration_minutes)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = round(1000 / 3600, 3)
    CM_IN_M: int = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height / self.CM_IN_M

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        kkak_multiplier: float = self.CALORIES_WEIGHT_MULTIPLIER * self.weight
        kkal_multiplier_min: float = (self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                                      * self.weight)
        speed_mps: float = self.get_mean_speed() * self.KMH_IN_MSEC
        duration_minutes: float = self.duration * self.MIN_IN_H

        return ((kkak_multiplier + (speed_mps ** 2 / self.height)
                 * kkal_multiplier_min) * duration_minutes)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM_K1: float = 1.1
    SWIM_K2: float = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        avg_speed: float = self.get_mean_speed()
        total_kkal: float = ((avg_speed + self.SWIM_K1)
                             * self.SWIM_K2 * self.weight * self.duration)
        return total_kkal

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings: dict = {
        'SWM': (Swimming, 5),
        'RUN': (Running, 3),
        'WLK': (SportsWalking, 4)
    }

    if workout_type not in trainings:
        raise ValueError('Incorrect workout type')

    if trainings[workout_type][1] != len(data):
        raise ValueError('Incorrect data type')

    return trainings[workout_type][0](*data)


def main(training1: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training1.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
