# checke_engine_2025

Checker Engine Project. A practice to proceed itself as chess machine later.

TODO:

0. Promotion while attack and chain attack needs to be moved in attack() method, so that Bots can do the same.

1. Update game over condition in Game.game_over() method.

2. Create read_board() method in Game class that gets board notation (either PEN or algebraic) and creates new game and board with it.

3. Create heuristic scoring method to score board situation in heuristic_score.py.

4. Create Learning AI algorthm.

5. (Potential bug fix) Fix error within move_debug() and attack_phase() method in Game class. It is not sure which part is broken(move_debug, attack_phase, find_targets, get_atk_dict), so it would be preceeded with debug play.
