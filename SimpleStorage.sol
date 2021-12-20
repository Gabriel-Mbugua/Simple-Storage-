// SPDX-License_Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    // init as zero
    uint256 favNumber;
    bool favBool;

    struct People {
        uint256 favNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavNumber;

    People public person = People({favNumber: 4, name: "Gabe"});

    function store(uint256 _favNumber) public returns (uint256) {
        favNumber = _favNumber;
        return favNumber;
    }

    //view function means we want to read some state of the blockchain
    function retrieve() public view returns (uint256) {
        return favNumber;
    }

    // storage: data will persist even after the function executes
    // memory: data will only be stored during execution of the function
    function addPerson(string memory _name, uint256 _favNumber) public {
        people.push(People({favNumber: _favNumber, name: _name}));
        nameToFavNumber[_name] = _favNumber;
    }
}
