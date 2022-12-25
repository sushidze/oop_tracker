import pytest
import inspect
from conftest import Capturing
import homework


@pytest.mark.parametrize('input_data, expected', [
    (('SWM', [720, 1, 80, 25, 40]), 'Swimming'),
    (('RUN', [15000, 1, 75]), 'Running'),
    (('WLK', [9000, 1, 75, 180]), 'SportsWalking'),
])
def test_read_package_return(input_data, expected):
    result = homework.read_package(*input_data)
    assert result.__class__.__name__ == expected, (
        'Function `read_package` should return training type '
        'depending on training code.'
    )


def test_InfoMessage():
    info_message = homework.InfoMessage
    info_message_signature = inspect.signature(info_message)
    info_message_signature_list = list(info_message_signature.parameters)
    for p in ['training_type', 'duration', 'distance', 'speed', 'calories']:
        assert p in info_message_signature_list, (
            f'Parameter {p} is missing in `__init__` `InfoMessage`.'
        )


@pytest.mark.parametrize('input_data, expected', [
    (['Swimming', 1, 75, 1, 80],
        'Training type: Swimming; '
        'Duration: 1.000 h.; '
        'Distance: 75.000 km; '
        'Av. speed: 1.000 km/h; '
        'Kcal: 80.000.'
     ),
    (['Running', 4, 20, 4, 20],
        'Training type: Running; '
        'Duration: 4.000 h.; '
        'Distance: 20.000 km; '
        'Av. speed: 4.000 km/h; '
        'Kcal: 20.000.'
     ),
    (['SportsWalking', 12, 6, 12, 6],
        'Training type: SportsWalking; '
        'Duration: 12.000 h.; '
        'Distance: 6.000 km; '
        'Av. speed: 12.000 km/h; '
        'Kcal: 6.000.'
     ),
])
def test_InfoMessage_get_message(input_data, expected):
    info_message = homework.InfoMessage(*input_data)
    result = info_message.get_message()
    assert result == expected, (
        'Method `get_message` should return string.\n'
        'Example: \n'
        'Training type: Swimming; '
        'Duration: 1.000 ч.; '
        'Distance: 75.000 км; '
        'Av. speed: 1.000 км/ч; '
        'Kcal: 80.000.'
    )


def test_Training():
    training = homework.Training
    training_signature = inspect.signature(training)
    training_signature_list = list(training_signature.parameters)
    for param in ['action', 'duration', 'weight']:
        assert param in training_signature_list, (
            f'Parameter {param} is missing in `__init__` `Training`'
        )
    assert training.M_IN_KM == 1000, (
        '1000m in 1km'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 5.85),
    ([420, 4, 20], 0.273),
    ([1206, 12, 6], 0.7838999999999999),
])
def test_Training_get_distance(input_data, expected):
    training = homework.Training(*input_data)
    result = training.get_distance()
    assert result == expected, (
        'Check formula of distance'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 5.85),
    ([420, 4, 20], 0.06825),
    ([1206, 12, 6], 0.065325),
])
def test_Training_get_mean_speed(input_data, expected):
    training = homework.Training(*input_data)
    result = training.get_mean_speed()
    assert result == expected, (
        'Check formula of av.speed'
    )


def test_Swimming():
    swimming = homework.Swimming
    swimming_signature = inspect.signature(swimming)
    swimming_signature_list = list(swimming_signature.parameters)
    for param in ['action', 'duration', 'weight', 'length_pool', 'count_pool']:
        assert param in swimming_signature_list, (
            f'Parameter {param} is missing in `__init__` `Swimming` '
        )


@pytest.mark.parametrize('input_data, expected', [
    ([720, 1, 80, 25, 40], 1.0),
    ([420, 4, 20, 42, 4], 0.042),
    ([1206, 12, 6, 12, 6], 0.005999999999999999),
])
def test_Swimming_get_mean(input_data, expected):
    swimming = homework.Swimming(*input_data)
    result = swimming.get_mean_speed()
    assert result == expected, (
        'Check formula of av.speed in Class `Swimming`'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([720, 1, 80, 25, 40], 336.0),
    ([420, 4, 20, 42, 4], 45.68000000000001),
    ([1206, 12, 6, 12, 6], 13.272000000000002),
])
def test_Swimming_get_spent_calories(input_data, expected):
    swimming = homework.Swimming(*input_data)
    result = swimming.get_spent_calories()
    assert result == expected, (
        'Check formula of kcal in Class `Swimming`'
    )


def test_SportsWalking():
    sports_walking = homework.SportsWalking
    sports_walking_signature = inspect.signature(sports_walking)
    sports_walking_signature_list = list(sports_walking_signature.parameters)
    for param in ['action', 'duration', 'weight', 'height']:
        assert param in sports_walking_signature_list, (
            f'Parameter {param} is missing in `__init__` `SportsWalking` '
        )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75, 180], 157.50000000000003),
    ([420, 4, 20, 42], 168.00000000000003),
    ([1206, 12, 6, 12], 151.20000000000002),
])
def test_SportsWalking_get_spent_calories(input_data, expected):
    sports_walking = homework.SportsWalking(*input_data)
    result = sports_walking.get_spent_calories()
    assert result == expected, (
        'Check formula of kcal in Class `SportsWalking`'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 383.85),
    ([420, 4, 20], -90.1032),
    ([1206, 12, 6], -81.32032799999999),
])
def test_Running_get_spent_calories(input_data, expected):
    running = homework.Running(*input_data)
    result = running.get_spent_calories()
    assert result == expected, (
        'Check formula of kcal in Class `Running`'
    )


@pytest.mark.parametrize('input_data, expected', [
    (['SWM', [720, 1, 80, 25, 40]], [
        'Training type: Swimming; '
        'Duration: 1.000 h.; '
        'Distance: 0.994 km; '
        'Av. speed: 1.000 km/h; '
        'Kcal: 336.000.'
    ]),
    (['RUN', [1206, 12, 6]], [
        'Training type: Running; '
        'Duration: 12.000 h.; '
        'Distance: 0.784 km; '
        'Av. speed: 0.065 km/h; '
        'Kcal: -81.320.'
    ]),
    (['WLK', [9000, 1, 75, 180]], [
        'Training type: SportsWalking; '
        'Duration: 1.000 h.; '
        'Distance: 5.850 km; '
        'Av. speed: 5.850 km/h; '
        'Kcal: 157.500.'
    ])
])
def test_main_output(input_data, expected):
    with Capturing() as get_message_output:
        training = homework.read_package(*input_data)
        homework.main(training)
    assert get_message_output == expected, (
        'Incorrect result'
    )
