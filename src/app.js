App = {

  loading: false,
  contracts: {},

  load: async () => {
    await App.loadWeb3()
    await App.loadAccount()
    await App.loadContract()
    // await App.render()
  },

  // https://medium.com/metamask/https-medium-com-metamask-breaking-change-injecting-web3-7722797916a8
  loadWeb3: async () => {
    if (typeof web3 !== 'undefined') {
      App.web3Provider = web3.currentProvider
      web3 = new Web3(web3.currentProvider)
    } else {
      window.alert("Please connect to Metamask.")
    }
    // Modern dapp browsers...
    if (window.ethereum) {
      window.web3 = new Web3(ethereum)
      try {
        // Request account access if needed
        await ethereum.enable()
        // Acccounts now exposed
        web3.eth.sendTransaction({/*
          gas:100000
        */})
      } catch (error) {
        // User denied account access...
      }
    }
    // Legacy dapp browsers...
    else if (window.web3) {
      App.web3Provider = web3.currentProvider
      window.web3 = new Web3(web3.currentProvider)
      // Acccounts always exposed
      web3.eth.sendTransaction({/*
        gas:110000
      */})
    }
    // Non-dapp browsers...
    else {
      console.log('Non-Ethereum browser detected. You should consider trying MetaMask!')
    }
  },

  loadAccount: async () => {
    // Set the current blockchain account
    App.account = web3.eth.accounts[0]
  },

  loadContract: async () => {
    // Create a JavaScript version of the smart contract
    const userList = await $.getJSON('UserList.json')
    App.contracts.UserList = TruffleContract(userList)
//    App.contracts.UserList.defaults({gasLimit:6721975})
    App.contracts.UserList.setProvider(App.web3Provider)
    // Hydrate the smart contract with values from the blockchain
    App.userList = await App.contracts.UserList.deployed()
    console.log(App.userList)
  },

  // render: async () => {
  //   // Prevent double render
  //   if (App.loading) {
  //     return
  //   }
  //
  //   // Update app loading state
  //   App.setLoading(true)
  //
  //   // Render Account
  //   $('#account').html(App.account)
  //
  //   // Render Tasks
  //   // await App.renderTasks()
  //
  //   // Update loading state
  //   App.setLoading(false)
  //
  // },
  createUser: async () => {
    await App.userList.createUser(nameCardID)
  }
}

$(() => {
  $(window).load(() => {
    App.load()
  })
})
