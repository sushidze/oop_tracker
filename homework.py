class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):

        print(f'Тип тренировки: {self.training_type}; '
              f'Длительность: {self.duration} ч.; '
              f'Дистанция: {self.distance} км; '
              f'Ср. скорость: {self.speed} км/ч; '
              f'Потрачено ккал: {self.calories}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return round(distance, 3)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return round(speed, 3)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    coeff_running_1 = 18
    coeff_running_2 = 20

    def get_spent_calories(self) -> float:

        spent_calories = ((self.coeff_running_1
                           * self.get_mean_speed()
                          - self.coeff_running_2)
                          * self.weight / self.M_IN_KM * self.duration)
        return round(spent_calories, 3)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coeff_walking_1: float = 0.035
    coeff_walking_2: float = 0.029

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = (self.coeff_walking_1 * self.weight
                          + (self.get_mean_speed() ** 2 // self.height)
                          * self.coeff_walking_2
                          * self.weight * self.duration)
        return round(spent_calories, 3)


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_swimming_1: float = 1.1
    coeff_swimming_2: int = 2
    LEN_STEP = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return round(speed, 3)

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed() + self.coeff_swimming_1)
                          * self.coeff_swimming_2 * self.weight)
        return round(spent_calories, 3)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    sports = {'SWM': Swimming,
              'RUN': Running,
              'WLK': SportsWalking}
    action, duration, weight = data[:3]
    sport = sports[workout_type]
    if workout_type == 'RUN':
        return sport(action, duration, weight)
    elif workout_type == 'WLK':
        height = data[3]
        return sport(action, duration, weight, height)
    else:
        length_pool = data[3]
        count_pool = data[4]
        return sport(action, duration, weight, length_pool, count_pool)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    info.get_message()


if __name__ == '__main__':

    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
