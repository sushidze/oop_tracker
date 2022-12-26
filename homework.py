from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Information message about training."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Generate message."""
        info = (
            f"Training type: {self.training_type}; "
            f"Duration: {round(self.duration,3):.3f} h.; "
            f"Distance: {round(self.distance,3):.3f} km; "
            f"Av. speed: {round(self.speed,3):.3f} km/h; "
            f"Kcal: {round(self.calories,3):.3f}."
        )
        return info


class Training:
    """Base class of training."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        info = InfoMessage(
            self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )
        return info


class Running(Training):
    """Training type: running."""

    KOEFF_RUNNING_1: int = 18
    KOEFF_RUNNING_2: int = 20

    def get_spent_calories(self) -> float:

        spent_calories = (
            (
                self.KOEFF_RUNNING_1 * self.get_mean_speed()
                - self.KOEFF_RUNNING_2
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_HOUR
        )
        return spent_calories


class SportsWalking(Training):
    """Training type: sports walking."""

    KOEFF_WALKING_1: float = 0.035
    KOEFF_WALKING_2: float = 0.029

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = (
            (
                self.KOEFF_WALKING_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.KOEFF_WALKING_2
                * self.weight
            )
            * self.duration
            * self.MIN_IN_HOUR
        )
        return spent_calories


class Swimming(Training):
    """Training type: swimming."""

    KOEFF_SWIMMING_1: float = 1.1
    KOEFF_SWIMMING_2: int = 2
    LEN_STEP = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )
        return speed

    def get_spent_calories(self) -> float:
        spent_calories = (
            (self.get_mean_speed() + self.KOEFF_SWIMMING_1)
            * self.KOEFF_SWIMMING_2
            * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Read data, which was received from module."""

    sports = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    sport = sports[workout_type](*data)
    return sport


def main(training: Training) -> None:
    info = training.show_training_info().get_message()
    print(info)


if __name__ == '__main__':

    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
