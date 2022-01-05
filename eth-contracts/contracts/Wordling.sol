//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.11;
import "./interfaces/IWordToken.sol";

contract Wordling {
    uint256 cooldown = 180; // number of seconds between fetching words
    uint256 admission = 0; // number of $WORD tokens that need to be held to play
    address private _adminSigner;

    struct Player {
        uint128 word; // index of the list of words that is assigned to the user
        uint128 unclaimed; // number of words attempted since the last reward claim
        uint256 lastAttempt; // timestamp of the last word retrieved, for rate-limiting
    }
    mapping(address => Player) public players;

    // map the number of guesses to scores
    mapping(uint8 => uint256) public scoreRewards;

    IWordToken wordToken;
    uint128 public dictionarySize = 100000;

    constructor(address wordTokenAddr) {
        scoreRewards[uint8(1)] = 100;
        scoreRewards[uint8(2)] = 10;
        scoreRewards[uint8(3)] = 3;
        scoreRewards[uint8(4)] = 2;
        scoreRewards[uint8(5)] = 1;
        // solidity defaults to 0 so no need:
        // scoreRewards[uint8(6)] = 0;

        wordToken = IWordToken(wordTokenAddr);
    }

    /**
     * @dev Assign a word to the user
     */
    function getWord() external {
        require(admission <= wordToken.balanceOf(msg.sender), "Insufficient $WORD to play");

        Player storage player = players[msg.sender];
        uint256 ts = block.timestamp;

        // check that the last assignment was before the cooldown period
        require(player.lastAttempt < (ts - cooldown), "Cooldown");

        // assign the word to the user
        player.word = uint128(bytes16(keccak256(abi.encodePacked(msg.sender, block.difficulty, ts)))) % dictionarySize;
        player.unclaimed += 1;
        player.lastAttempt = ts;
    }

    /**
     * @dev Free word of the day
     */
    function freeWord() external view returns (uint256) {
        // convert timestamp to day-granularity timestamp
        return block.timestamp % 86400;
    }

    /**
     * @dev calculate rewards based on scores
     */
    function calculateReward(uint8[] calldata scores) public view returns (uint256) {
        uint256 amount;
        for (uint256 i = 0; i < scores.length; i++){
            amount += scoreRewards[scores[i]];
        }
        return amount;
    }

    /**
     * @dev Claim your wins
     */
    function mintWins(bytes32 _hash, bytes32 _r, bytes32 _s, uint8 _v, uint8[] calldata scores) external {
        address signer = ecrecover(_hash, _v, _r, _s);
        require(signer == _adminSigner, "Forged signature");
        // TODO invalidate signature

        Player storage player = players[msg.sender];
        require(player.unclaimed != 0, "Incorrect scores");
        require(player.unclaimed == scores.length, "Incorrect scores");

        player.unclaimed = 0;
        uint256 reward = calculateReward(scores);
        wordToken.rewardMint(msg.sender, reward);
    }
}