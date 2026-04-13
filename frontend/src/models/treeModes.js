/**
 * Tree Load Mode Constants.
 * Define the two modes for loading tree data from files.
 */

/**
 * Topology mode - Load tree structure directly from file.
 * Loads AVL tree structure as-is and builds equivalent BST
 * by inserting nodes in inorder traversal sequence.
 * @type {string}
 */
export const LOAD_MODE_TOPOLOGY = 'topology'

/**
 * Insertion mode - Sequentially insert flights to build both trees.
 * Inserts same flight sequence into both AVL and BST for comparison.
 * Shows difference in structure due to AVL balancing vs BST.
 * @type {string}
 */
export const LOAD_MODE_INSERTION = 'insertion'
