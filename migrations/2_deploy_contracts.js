const UserList = artifacts.require("./UserList.sol");

module.exports = function(deployer) {
  deployer.deploy(UserList);
};
