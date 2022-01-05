const { ethers } = require("hardhat");

async function main() {
    // We get the contract to deploy
    const WordToken = await ethers.getContractFactory("WordToken");
    const wordToken = await WordToken.deploy();
    console.log("Word Token deployed to:", wordToken.address);

    const Wordling = await ethers.getContractAt("Wordling");
    const wordling = await Wordling.deploy(wordToken.address);
    console.log("Wordling Game deployed to: ", wordling.address);
  }
  
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });