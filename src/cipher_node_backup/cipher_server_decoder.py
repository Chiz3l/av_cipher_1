
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from cipher_interfaces.msg import CipherMessage
from cipher_interfaces.srv import CipherAnswer

# decrypts everything
def caesar_decode(ciphertext, shift) -> str:
    result = []
    for char in ciphertext:
        if char.isupper():
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        elif char.islower():
            result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        else:
            result.append(char)
            
    return_val = ''
    return return_val.join(result)

class CipherSolverNode(Node):
    def __init__(self):
        super().__init__('cipher_solver_node')

        self.has_submitted = False
        self.decoded_message = ''

        # creates the client that will then connect to the server and verify the solution
        self.client_ = self.create_client(CipherAnswer, 'verify_cipher')

        # subscribes to the topic to get the encoded cipher
        self.subscription_ = self.create_subscription(
            CipherMessage,
            'cipher_topic',
            self.cipher_message_callback,
            10 # always need to make sure this is consistent
        )

    def cipher_message_callback(self, msg):
        # process once, dont spam server on every tick (i didnt have this and it was cooked)
        if self.has_submitted:
            return
        self.has_submitted = True

        # decode the message
        self.decoded_message = caesar_decode(msg.message, msg.key)

        # string answer
        # ---
        # bool result

        # send the server service request
        request = CipherAnswer.Request()
        request.header.stamp = self.get_clock().now().to_msg()
        request.header.frame_id = 'solver_frame'
        request.answer = self.decoded_message

        # this is async so that a queue can be built
        future = self.client_.call_async(request)
        # this runs the response once the server has responded async
        future.add_done_callback(self.service_response)

    def service_response(self, future):
        try:
            response = future.result()
            self.get_logger().info('================================================')
            self.get_logger().info(f'Decoded Answer : "{self.decoded_message}"')
            self.get_logger().info(f'Answer Correct?: {response.result}')
            self.get_logger().info('================================================')

        finally:
            # closes the solver node now that it is done
            raise SystemExit


def main(args=None):
    # this initialises the node and then runs it
    rclpy.init(args=args)
    node = CipherSolverNode()
    try:
        # keeps running the node continually in a loop with all the publishing and recieving
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        pass
    # waits for me to kill the node
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()