# cipher
ROS2 interface for custom msgs

ros2 pkg create --build-type ament_python cipher_node \
    --dependencies rclpy std_msgs cipher_interfaces

mv cipher_node_backup/cipher_server_encrypter.py cipher_node/cipher_node/
mv cipher_node_backup/cipher_server_decoder.py cipher_node/cipher_node/
rm -rf cipher_node_backup


colcon build --packages-select cipher_interfaces
source install/setup.bash
ros2 pkg create --build-type ament_python caesar_cipher_py \
  --dependencies rclpy std_msgs cipher_interfaces


colcon build
source install/setup.bash

ros2 launch caesar_cipher_py cipher_game.launch.py