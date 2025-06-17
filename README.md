# checker_engine_2025

Checker Engine Project. A practice to proceed itself as chess machine later.

Last Update: 17th JUN, 2025

TODO:

1. Promotion while attack and chain attack needs to be moved in attack() method, so that Bots can do the same.

2. Create Board Tree structure and implement min-max algorithm.

3. Update game over condition in Game.game_over() method.

4. Create Learning AI algorithm.

5. (Potential bug fix) Fix error within move_debug() and attack_phase() method in Game class. It is not sure which part is broken(move_debug, attack_phase, find_targets, get_atk_dict), so it would be preceeded with debug play.
