#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from cipher_interfaces.msg import CipherMessage
from cipher_interfaces.srv import CipherAnswer


def caesar_encode(text, shift) -> str:
    result = []
    # checks if the character is upper case or lower case and then shifts it, also wraps caracters around the alphabet
    for char in text:
        if char.isupper():
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        elif char.islower():
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(char)
            
    return_val = ''
    return return_val.join(result)


class CipherServerNode(Node):
    def __init__(self):
        super().__init__('cipher_server_node')

        # declaring params this way allows me to change these vals without rebuilding
        self.declare_parameter('secret_message', 'Redback Racing Autonomous Vehicles')
        self.declare_parameter('cipher_key', 7)
        self.original_message = self.get_parameter('secret_message').get_parameter_value().string_value
        self.cipher_key = self.get_parameter('cipher_key').get_parameter_value().integer_value
        publish_period = 1.0

        # encoding the message
        self.encoded_message = caesar_encode(self.original_message, self.cipher_key)

        # publisher for the message interface
        self.publisher_ = self.create_publisher(CipherMessage, 'cipher_topic', 10) # the 10 is the polling rate essentially
        self.timer_ = self.create_timer(publish_period, self.publish_cipher)

        # creates the server within the node
        self.server_ = self.create_service(
            CipherAnswer,
            'verify_cipher',
            self.verify_answer
        )

    def publish_cipher(self):
        # creating a standard message to publish
        msg = CipherMessage()
        # directly from the interface
        msg.message = self.encoded_message
        msg.key = int(self.cipher_key)
        msg.header.frame_id = 'cipher_frame'
        msg.header.stamp = self.get_clock().now().to_msg()
        # publish the message
        self.publisher_.publish(msg)

    def verify_answer(self, request, response):
        is_correct = (request.answer == self.original_message)
        response.result = is_correct
        return response


def main(args=None):
    # this initialises the node and then runs it
    rclpy.init(args=args)
    node = CipherServerNode()
    try:
        # keeps running the node continually in a loop with all the publishing and recieving
        rclpy.spin(node)
    # waits for me to kill the node
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()