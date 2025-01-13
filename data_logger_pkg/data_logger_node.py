import rclpy
from rclpy.node import Node
import can
import struct
from datetime import datetime
import os
from my_robot_interfaces.msg import BesturingsData

class CanLoggerNode(Node):
    def __init__(self):
        super().__init__('can_logger_node')

        # node voor het loggen van de besturings data

        self.besturingsData_subscrition = self.create_subscription(BesturingsData, 'besturings_data', self.data_callback, 10)

        # Stel het pad in voor het bestand
        package_path = os.path.expanduser('~/ros2_ws/src/data_logger_pkg/data_besturing')
        if not os.path.exists(package_path):
            os.makedirs(package_path)

        file_path = os.path.join(package_path, 'recording.csv')

        # Open het bestand voor schrijven
        with open(file_path, 'w') as file_pointer:
            # Schrijf de headerregel naar het CSV-bestand
            file_pointer.write('Timestamp|Throttle|Brake|Steering|Direction\n')


        # Timer om de gegevens periodiek op te slaan
        self.log_timer = self.create_timer(0.1, self.log_data)

    def data_callback(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Verwerken van de message
        brake = BesturingsData.brake
        steering = BesturingsData.steering
        throttle = BesturingsData.throttle
        direction = BesturingsData.direction

        self.file_pointer.write(f'{timestamp},{throttle},{brake},{steering},{direction}\n')
        self.file_pointer.flush()

def main(args=None):
    rclpy.init(args=args)
    node = CanLoggerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
