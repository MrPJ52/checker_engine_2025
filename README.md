# checker_engine_2025

Checker Engine Project. A practice to proceed itself as chess machine later.

Last Update: 16th JUN, 2025

TODO:

0. Promotion while attack and chain attack needs to be moved in attack() method, so that Bots can do the same.

1. Create Board Tree structure and implement min-max algorithm.

2. Update game over condition in Game.game_over() method.

3. Create Learning AI algorithm.

4. (Potential bug fix) Fix error within move_debug() and attack_phase() method in Game class. It is not sure which part is broken(move_debug, attack_phase, find_targets, get_atk_dict), so it would be preceeded with debug play.
