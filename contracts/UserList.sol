pragma solidity ^0.5.0;

contract UserList {
  uint public userCount = 0;

  struct User {
    uint listNum;
    uint userID;
  }

  event NewUser(
    uint _listNum,
    uint _userID
  );

  mapping(uint => User) public users;

  constructor() public {}

  function createUser(uint _userID) public {
    userCount ++;
    users[userCount] = User(userCount, _userID);
    emit NewUser(userCount, _userID);
  }

}
