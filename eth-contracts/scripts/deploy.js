const { ethers } = require("hardhat");

async function main() {
    // We get the contract to deploy
    const [owner] = await ethers.getSigners();
    console.log("DEPLOYER: ", owner.address);
    const WordToken = await ethers.getContractFactory("WordToken");
    const wordToken = await WordToken.deploy();
    console.log("Word Token deployed to:", wordToken.address);
    await wordToken.deployTransaction.wait();

    const Wordling = await ethers.getContractFactory("Wordling");
    const wordling = await Wordling.deploy(wordToken.address);
    console.log("Wordling Game deployed to: ", wordling.address);
    await wordling.deployTransaction.wait();

    const txn = await wordling.getWord();
    console.log(txn);
    await txn.wait();
    console.log(await wordling.players(owner.address));
  }
  
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });