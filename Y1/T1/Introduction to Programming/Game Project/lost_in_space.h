#ifndef LOST_IN_SPACE_H
#define LOST_IN_SPACE_H

#include "splashkit.h"
#include "player.h"
#include "power_up.h"
#include <vector>

using std::vector;
using namespace std;

/**
 * The `game_data` structure stores information related to the game.
 *
 * @field player: An instance of `player_data` to access player information.
 * @field power_ups: A dynamic array of `power_up_data` to manage multiple power-ups.
 */
struct game_data
{
    player_data player;
    vector<power_up_data> power_ups;
};

/**
 * Creates a new game by initializing a new player.
 *
 * @returns The newly created game data.
 */
game_data new_game();

/**
 * Updates the game by updating the player, power-ups, adding new power-ups, and
 * checking for collisions between the player and power-ups.
 *
 * @param game: The game data being updated.
 */
void update_game(game_data &game);

/**
 * Draws the game to the screen, including the heads-up display (HUD), player, and power-ups.
 *
 * @param game: The game data to be drawn to the screen.
 */
void draw_game(const game_data &game);

/**
 * Adds a power-up to the dynamic array of power-ups in the game by generating it at a random position
 * within the range of -1500 to +1500.
 *
 * @param game: The game data to be updated.
 */
void add_power_up(game_data &game);

/**
 * Checks for collisions between the player and power-ups and applies/removes power-ups accordingly.
 *
 * @param game: The game data to be updated.
 */
void check_collisions(game_data &game);

/**
 * Applies the effect of a power-up at the specified index in the game's vector of power-ups and plays
 * an appropriate sound based on the power-up.
 *
 * @param game: The game data to be updated.
 * @param index: The index of the power-up to be updated.
 */
void apply_power_up(game_data &game, int index);

/**
 * Removes the power-up at the specified index from the vector of power-ups in the game.
 *
 * @param game: The game data to be updated.
 * @param index: The index of the power-up to be removed.
 */
void remove_power_up(game_data &game, int index);

/**
 * Checks the position of power-ups to ensure they are within the playing area of 3000 units
 * and removes power-ups that go beyond that area.
 *
 * @param game: The game data to be updated.
 */
void check_power_up_position(game_data &game);

/**
 * Draws the heads-up display (HUD) to the screen, including the score, player location, fuel bar, and health bar.
 *
 * @param game: The game data to be drawn to the screen.
 */
void draw_hud(const game_data &game);

#endif