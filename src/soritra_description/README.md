# soritra_description

Package ROS 2 autonome contenant le modèle URDF du robot Soritra ainsi qu’un
lancement qui ouvre simultanément le contrôleur de joint et RViz.

## Prérequis

- ROS 2 installé et son environnement chargé (`source /opt/ros/<distribution>/setup.bash`).
- Les dépendances déclarées dans `package.xml` : `robot_state_publisher`,
  `joint_state_publisher_gui`, `rviz2`, `xacro`, `launch` et `launch_ros`.
- `colcon` et `rosdep` pour installer les dépendances et construire le package.

Depuis la racine du dépôt :

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
rosdep install --from-paths src/soritra_description --ignore-src -r -y
colcon build --base-paths src/soritra_description --packages-select soritra_description
source install/setup.bash
ros2 launch soritra_description display.launch.py
```

La fenêtre de contrôle expose les curseurs `shoulder_joint` (rotation de L1
sur la base) et `elbow_joint` (rotation de L2 par rapport à L1). RViz affiche
le repère TF `terminal_xy` situé à la pointe du stylo. Ses coordonnées
`terminal_X` et `terminal_Y` sont calculées par la cinématique du bras et
changent avec les deux angles ; ce ne sont pas deux articulations ou curseurs
indépendants. Pour lire les valeurs numériques, lancez
`ros2 run tf2_ros tf2_echo world_link terminal_xy` dans un second terminal.
Le lancement accepte aussi `use_sim_time:=true` et
`rviz_config:=/chemin/vers/config.rviz`.

## Modèle

Le modèle est défini dans `urdf/soritra.urdf`. Il comprend une base et un
support fixes, un segment L1 de 1 m articulé à la base, un segment L2 de 0,8 m
articulé au coude et un stylo à l’extrémité. L’URDF décrit l’apparence et les
liaisons ; le traçage réel, le contrôle du moteur et le contact du stylo
nécessitent des nœuds ou une simulation supplémentaires.
