""" Create an elevator system that is able to move between floors, open and close doors and
call emergency center.

Application: The elevator
Command: EmergencyButtonCommand, DoorsCloseButtonCommand, DoorsOpenButtonCommand, NumberButtonCommand
Invoker: A physical elevator button that is linked to a given button command
Receiver: The elevator API and the emergency center API
"""

import abc
import enum
import time
import typing as t


class DoorState(enum.Enum):
    OPEN = enum.auto()
    CLOSED = enum.auto()


class Lights(enum.Enum):
    HIGH = enum.auto()
    LOW = enum.auto()
    CLOSED = enum.auto()


class ElevatorState(enum.Enum):
    RUNNING = enum.auto()
    IDLE = enum.auto()


# Receivers
class EmergencyCenter:
    def call(self):
        print('Calling emergency service!')


class ElevatorApi:
    def __init__(self) -> None:
        self.current_floor = 0
        self.lights_intensity = Lights.HIGH
        self.doors = DoorState.OPEN
        self.state = ElevatorState.IDLE

    def switch_low_energy_mode(self):
        self.lights_intensity = Lights.LOW

    def on_floor(self):
        return self.state == ElevatorState.IDLE

    def close_doors(self):
        self.doors = DoorState.CLOSED

    def open_doors(self):
        if self.state == ElevatorState.IDLE:
            self.doors = DoorState.OPEN

    def move_to_floor(self, floor: int):
        """ This method is best written as an async method with a requests queue
        But we'll ignore that for the sake of brevity
        """
        print('Moving to floor', floor)
        if self.on_floor():
            print('     Closing the doors')
            time.sleep(2)
            self.close_doors()

        self.state = ElevatorState.RUNNING
        print('     Elevator running')
        time.sleep(3)
        self.state = ElevatorState.IDLE
        self.current_floor = floor
        self.open_doors()
        print('     Arrived at destination')


# Commands
class Command(abc.ABC):
    def __init__(self, elevator_api: ElevatorApi, emergency_center: EmergencyCenter):
        self.emergency_center = emergency_center
        self.elevator_api = elevator_api

    @abc.abstractmethod
    def execute(self) -> None:
        pass


class EmergencyButtonCommand(Command):
    def execute(self) -> None:
        self.elevator_api.switch_low_energy_mode()
        self.emergency_center.call()


class DoorsCloseButtonCommand(Command):
    def execute(self) -> None:
        if self.elevator_api.doors == DoorState.OPEN:
            self.elevator_api.close_doors()


class DoorsOpenButtonCommand(Command):
    def execute(self) -> None:
        if self.elevator_api.on_floor():
            self.elevator_api.open_doors()


class NumberButtonCommand(Command):
    def __init__(self,
            number: int,
            elevator_api: ElevatorApi,
            emergency_center: EmergencyCenter):
        super().__init__(elevator_api, emergency_center)
        self.number = number

    def execute(self) -> None:
        if self.elevator_api.current_floor == self.number:
            return

        self.elevator_api.move_to_floor(self.number)


# Invoker/Sender
class ElevatorButton:
    def __init__(self, command: Command):
        self.command = command

    def execute(self) -> None:
        self.command.execute()


# Application
class Elevator:
    def __init__(self, max_floors: int, elevator_api, emergency_center):
        self.max_floors = max_floors
        self.elevator_api = elevator_api
        self.emergency_center = emergency_center
        self.board: t.Dict[str, ElevatorButton] = None

    def create_board(self) -> None:
        board = {}
        for floor in range(self.max_floors + 1):
            cmd = NumberButtonCommand(floor, self.elevator_api, self.emergency_center)
            board[str(floor)] = ElevatorButton(cmd)

        door_open_cmd = DoorsOpenButtonCommand(self.elevator_api, self.emergency_center)
        door_closed_cmd = DoorsCloseButtonCommand(self.elevator_api, self.emergency_center)
        emergency_cmd = EmergencyButtonCommand(self.elevator_api, self.emergency_center)

        self.board = board
        self.board['door_open'] = ElevatorButton(door_open_cmd)
        self.board['door_closed'] = ElevatorButton(door_closed_cmd)
        self.board['emergency'] = ElevatorButton(emergency_cmd)

    def select(self, selection: str):
        if selection.isnumeric() and int(selection) > self.max_floors:
            print(f'Not a valid floor number {selection}!')
            return

        if selection not in self.board:
            print('Not a valid selection, try one of', tuple(self.board.keys()))
            return

        self.board[selection].execute()


if __name__ == '__main__':
    elevator_api = ElevatorApi()
    emergency_center = EmergencyCenter()
    elevator = Elevator(
        max_floors=9,
        elevator_api=elevator_api,
        emergency_center=emergency_center)
    elevator.create_board()

    elevator.select('1')
    elevator.select('door_open')
    print('Door state', elevator_api.doors)

    elevator.select('4')
    elevator.select('door_closed')

    print('Door state', elevator_api.doors)
    elevator.select('9')

    elevator.select('emergency')
    print('Lights', elevator_api.lights_intensity)

    elevator.select('12')
    elevator.select('invalid_option')
