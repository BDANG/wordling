//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.11;
import "@rari-capital/solmate/src/tokens/ERC20.sol";

contract WordToken is ERC20 {
    constructor() ERC20("Wordling Token", "WORD", 18){
    }
}