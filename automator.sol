//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract automaticSmartContracts {

/*
* 
* 
*
*/

    struct aContract {
        address conAdd;
        string conName;
        uint lastActi;
        uint autoPeriod;
        bool isActive;
        uint etherBalance;
        address owner;
    }

    aContract[] contracts;

    function registerContract(address yourContract, uint period, string memory name) public {
        aContract memory newContract = aContract(yourContract, name, 0, period, false, 0, msg.sender);
        contracts.push(newContract);
    }

    function depositEth(address whatContract) public payable {
        for(uint i = 0; i < contracts.length; i++) {
            if(contracts[i].conAdd == whatContract){
                contracts[i].isActive = true;
                contracts[i].etherBalance = contracts[i].etherBalance + msg.value;
            }  
        }
    }

    function withdrawEth(uint amount) public {
        bool isOwner;
        uint contBalance;

        for (uint i = 0; i < contracts.length; i++) {
            if(contracts[i].owner == msg.sender) {
                isOwner = true;
                contBalance = contracts[i].etherBalance;
            }
        }

        require(isOwner && amount <= contBalance);

        payable(msg.sender).transfer(amount);
        contBalance = contBalance - amount;
    }


}
