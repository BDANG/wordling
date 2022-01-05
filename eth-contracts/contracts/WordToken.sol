//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.11;
import "@rari-capital/solmate/src/tokens/ERC20.sol";

contract WordToken is ERC20 {
    uint256 public cooldown = 60;
    uint256 public admission = 0;
    uint256 public constant PUBLIC_LAUNCH_MINT = 100;
    uint256 public constant PUBLIC_LAUNCH_MAX = 1000;
    uint256 public publicLaunchCount;

    // tracks if the user claimed the public airdrop
    mapping(address => bool) public claims;

    // tracks users' last claim timestamp
    mapping(address => uint256) public lastClaim;

    address private _adminSigner;
    
    // map the number of guesses to scores
    mapping(uint8 => uint256) public scoreRewards;

    constructor(address _admin) ERC20("Wordling Token", "WORD", 18){
        _adminSigner = _admin;
        scoreRewards[uint8(1)] = 100;
        scoreRewards[uint8(2)] = 10;
        scoreRewards[uint8(3)] = 3;
        scoreRewards[uint8(4)] = 2;
        scoreRewards[uint8(5)] = 1;
        // solidity defaults to 0 so no need:
        // scoreRewards[uint8(6)] = 0;
    }

    // -----------------------------------------------------------
    // Minting / Issuance
    //  - functions for issuance
    // -----------------------------------------------------------
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
     * @dev Giveaway / promotional minting
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
    function rewardMint(uint8[] calldata scores, bytes calldata signature) external {
        require(playable(msg.sender), "Insufficient balance");

        // cooldown between claims to prevent abuse and dilution
        require(lastClaim[msg.sender] < (block.timestamp - cooldown), "Cooldown");

        // verify that rewards can be issued
        require(verify(msg.sender, scores, signature), "Invalid signature");

        lastClaim[msg.sender] = block.timestamp;
        _mint(msg.sender, calculateReward(scores));
    }


    // -----------------------------------------------------------
    // Utils
    //  - utility functions for players
    // -----------------------------------------------------------
    /**
     * @dev determine if the user can play
     */
    function playable(address player) public view returns (bool) {
        return admission <= balanceOf[player];
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


    // -----------------------------------------------------------
    // Params & settings
    // -----------------------------------------------------------
    function setParams(address signer, uint256 _cooldown, uint256 _admission) external {
        _adminSigner = signer;
        cooldown = _cooldown;
        admission = _admission;
    }

    function setRewards(uint8 score, uint256 issuance) external {
        scoreRewards[score] = issuance;
    }


    // -----------------------------------------------------------
    // Signature
    //  - rewards are issued by signed messages
    // -----------------------------------------------------------
    /**
     * @dev Produce a message to sign
     */
    function getMessageHash(address winner, uint8[] calldata scores) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(winner, scores));
    }

    /**
     * @dev Produce an ethereum-spec signed message
     */
    function getEthSignedMessageHash(bytes32 messageHash) public pure returns (bytes32) {
        return keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", messageHash));
    }

    // copied from https://solidity-by-example.org/signature/
    function verify(
        address winner,
        uint8[] calldata scores,
        bytes memory signature
    ) public view returns (bool) {
        bytes32 messageHash = getMessageHash(winner, scores);
        bytes32 ethSignedMessageHash = getEthSignedMessageHash(messageHash);

        return recoverSigner(ethSignedMessageHash, signature) == _adminSigner;
    }

    function recoverSigner(bytes32 _ethSignedMessageHash, bytes memory _signature)
        public
        pure
        returns (address)
    {
        (bytes32 r, bytes32 s, uint8 v) = splitSignature(_signature);

        return ecrecover(_ethSignedMessageHash, v, r, s);
    }

    function splitSignature(bytes memory sig)
        public
        pure
        returns (
            bytes32 r,
            bytes32 s,
            uint8 v
        )
    {
        require(sig.length == 65, "invalid signature length");

        assembly {
            /*
            First 32 bytes stores the length of the signature

            add(sig, 32) = pointer of sig + 32
            effectively, skips first 32 bytes of signature

            mload(p) loads next 32 bytes starting at the memory address p into memory
            */

            // first 32 bytes, after the length prefix
            r := mload(add(sig, 32))
            // second 32 bytes
            s := mload(add(sig, 64))
            // final byte (first byte of the next 32 bytes)
            v := byte(0, mload(add(sig, 96)))
        }
        // implicitly return (r, s, v)
    }
}