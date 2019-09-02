module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545,
      network_id: "*" // Match any network id
    },
    rinkeby: {
     host: "localhost",
     port: 8545,
     network_id: "4", // Rinkeby ID 4
     from: "0x23C84a67dF9DF877E7989D19fD87dB006ee5B41d", // account from which to deploy
     gas: 4700000
    }
  },
  solc: {
    optimizer: {
      enabled: true,
      runs: 200
    }
  }
}
