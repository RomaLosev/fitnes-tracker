class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Получить информационное сообщение."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


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
        return self.action * Training.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Калории бег"""
        calories_run = ((Running.COEFF_CALORIE_1 * self.get_mean_speed()
                        - Running.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                        * self.duration * 60)
        return calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Калории ходьба"""
        calories_wlk = ((SportsWalking.COEFF_CALORIE_1
                         * self.weight
                         + (self.get_mean_speed()**2 // self.height)
                         * SportsWalking.COEFF_CALORIE_2
                         * self.weight) * self.duration * 60)
        return calories_wlk


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: float = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    pass

    def get_mean_speed(self) -> float:
        """Ср. скорость плавание"""
        mean_spead_swm = (self.length_pool * self.count_pool
                          / self.M_IN_KM / self.duration)
        return mean_spead_swm

    def get_spent_calories(self) -> float:
        """Калории плавание"""
        calories_swm = ((self.get_mean_speed()
                         + Swimming.COEFF_CALORIE_1)
                        * Swimming.COEFF_CALORIE_2 * self.weight)
        return calories_swm

    def get_distance(self) -> float:
        """Получить дистанцию в км. Плавание"""
        return self.action * Swimming.LEN_STEP / Training.M_IN_KM


TRAINING_TYPE = {'SWM': Swimming,
                 'RUN': Running,
                 'WLK': SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in TRAINING_TYPE:
        raise KeyError

    return TRAINING_TYPE[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    result = InfoMessage.get_message(info)
    print(result)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
