const { ethers } = require("hardhat");

async function main() {
    // We get the contract to deploy
    const [owner] = await ethers.getSigners();
    console.log("DEPLOYER: ", owner.address);
    const WordToken = await ethers.getContractFactory("WordToken");
    const wordToken = await WordToken.deploy("0x1651700c498A5b77A87Df00D7364C2Ed22AfCa2b");
    console.log("Word Token deployed to:", wordToken.address);
    await wordToken.deployTransaction.wait();

    let txn = await wordToken.publicMint();
    await txn.wait();
    
    txn = await wordToken.suggestWord("hello");
    await txn.wait();
  }
  
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });