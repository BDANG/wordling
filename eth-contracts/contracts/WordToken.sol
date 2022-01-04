//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.11;
import "@rari-capital/solmate/src/tokens/ERC20.sol";

contract WordToken is ERC20 {
    uint256 public constant PUBLIC_LAUNCH_MINT = 100;
    uint256 public constant PUBLIC_LAUNCH_MAX = 1000;
    uint256 public publicLaunchCount;

    mapping(address => bool) public claims;

    constructor() ERC20("Wordling Token", "WORD", 18){
    }

    /**
     * @dev The initial public launch mint
     */
    function publicMint() external {
        require(publicLaunchCount + PUBLIC_LAUNCH_MINT <= PUBLIC_LAUNCH_MAX, "No claim available");
        require(!claims[msg.sender], "No claim available");
        publicLaunchCount += PUBLIC_LAUNCH_MINT;
        claims[msg.sender] = true;
        _mint(msg.sender, PUBLIC_LAUNCH_MINT);
    }

    /**
     * @dev Giveaway minting
     */
    function privateMint() external {
        // TODO: ecrecover
        require(!claims[msg.sender], "No claim available");
        claims[msg.sender] = true;
        _mint(msg.sender, PUBLIC_LAUNCH_MINT);
    }

    /**
     * @dev Reward minting
     */
    function rewardMint(address winner, uint256 amount) external {
        _mint(winner, amount);
    }
}