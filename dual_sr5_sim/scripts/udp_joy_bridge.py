#!/usr/bin/env python3
import json
import math
import socket

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy


class UDPJoyBridge(Node):
    def __init__(self):
        super().__init__('udp_joy_bridge')

        self.publisher_ = self.create_publisher(Joy, '/joy', 10)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.sock.bind(('0.0.0.0', 9090))

        self.packet_count = 0
        self.error_count = 0

        self.timer = self.create_timer(0.005, self.receive_udp)

        self.get_logger().info(
            'UDP Joy Bridge READY | UDP :9090 -> ROS /joy'
        )

    def receive_udp(self):
        while True:
            try:
                data, address = self.sock.recvfrom(4096)
            except BlockingIOError:
                break
            except OSError as exc:
                self.get_logger().error(f'UDP socket error: {exc}')
                break

            try:
                state = json.loads(data.decode('utf-8'))

                axes = state['axes']
                buttons = state['buttons']

                if not isinstance(axes, list) or not isinstance(buttons, list):
                    raise ValueError('axes/buttons must be lists')

                if len(axes) < 4 or len(buttons) < 6:
                    raise ValueError(
                        f'Unexpected lengths: axes={len(axes)}, '
                        f'buttons={len(buttons)}'
                    )

                msg = Joy()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = 'joy'
                msg.axes = [float(x) for x in axes]
                msg.buttons = [int(x) for x in buttons]

                if not all(math.isfinite(x) for x in msg.axes):
                    raise ValueError('Non-finite axis value')

                self.publisher_.publish(msg)

                self.packet_count += 1

                if self.packet_count == 1 or self.packet_count % 50 == 0:
                    self.get_logger().info(
                        f'Published /joy: {self.packet_count} packets | '
                        f'axes={msg.axes[:4]} | buttons={msg.buttons[:6]}'
                    )

            except Exception as exc:
                self.error_count += 1
                self.get_logger().error(
                    f'Packet rejected from {address}: {exc}'
                )

    def destroy_node(self):
        self.sock.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = UDPJoyBridge()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
