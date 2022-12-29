class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        message = f'Тип тренировки: {self.training_type}; Длительность: {self.duration:.3f} ч.; ' + \
                  f'Дистанция: {self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч; ' + \
                  f'Потрачено ккал: {self.calories:.3f}.'

        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 type_training: str = None
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight
        self.type_training: str = type_training

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        dist: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        return InfoMessage(self.type_training, self.duration, dist, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: float, weight: float):
        type_training = 'Running'
        super().__init__(action, duration, weight, type_training)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        avg_speed: float = super().get_mean_speed()
        duration_minutes: float = self.duration * self.MIN_IN_H
        total_kkal: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * avg_speed + self.CALORIES_MEAN_SPEED_SHIFT)
                      * self.weight / self.M_IN_KM * duration_minutes)

        return total_kkal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = round(1000 / 3600, 3)
    CM_IN_M: int = 100

    def __init__(self, action: int, duration: float, weight: float, height: float) -> None:
        type_training: str = 'SportsWalking'
        super().__init__(action, duration, weight, type_training)
        self.height: float = height/self.CM_IN_M

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        kkak_multiplier: float = self.CALORIES_WEIGHT_MULTIPLIER * self.weight
        kkal_multiplier_min: float = self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight
        speed_mps: float = self.get_mean_speed() * self.KMH_IN_MSEC
        duration_minutes: float = self.duration * self.MIN_IN_H

        total_kkal: float = (kkak_multiplier + (speed_mps**2 / self.height) * kkal_multiplier_min) * duration_minutes

        return total_kkal


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM_K1: float = 1.1
    SWIM_K2: float = 2

    def __init__(self, action: int, duration: float, weight: float, length_pool: int, count_pool: int):
        type_training = 'Swimming'
        super().__init__(action, duration, weight, type_training)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        avg_speed: float = self.get_mean_speed()
        total_kkal: float = (avg_speed + self.SWIM_K1) * self.SWIM_K2 * self.weight * self.duration
        return total_kkal

    def get_mean_speed(self) -> float:
        avg_speed: float = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return avg_speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings_dct: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    error: bool = False
    if workout_type not in ['SWM', 'RUN', 'WLK']:
        error = True

    if workout_type == 'SWM' and len(data) != 5:
        error = True

    if workout_type == 'RUN' and len(data) != 3:
        error = True

    if workout_type == 'WLK' and len(data) != 4:
        error = True

    if error:
        raise ValueError('Incorrect data type')
    else:
        return trainings_dct[workout_type](*data)


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
