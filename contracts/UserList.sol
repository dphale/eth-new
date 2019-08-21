pragma solidity ^0.5.0;

contract UserList {
  uint public userCount = 0;

  struct User {
    uint listNum;
    uint userID;
  }

  mapping(uint => User) public users;

  constructor() public {
    createUser(23576);
  }

  function createUser(uint _userID) public {
    userCount ++;
    users[userCount] = User(userCount, _userID);
  }

}
