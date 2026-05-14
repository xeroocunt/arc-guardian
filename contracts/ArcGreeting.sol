// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ArcGreeting
 * @dev A simple contract to store and retrieve agent missions on the Arc Network.
 */
contract ArcGreeting {
    struct Mission {
        string text;
        uint256 timestamp;
    }

    string private currentGreeting;
    address public owner;
    Mission[] public missionHistory;

    event GreetingChanged(address indexed setter, string newGreeting, uint256 timestamp);

    constructor(string memory _initialGreeting) {
        currentGreeting = _initialGreeting;
        owner = msg.sender;
        missionHistory.push(Mission(_initialGreeting, block.timestamp));
    }

    /**
     * @dev Sets a new greeting message and records it in history.
     */
    function setGreeting(string calldata _newGreeting) external {
        currentGreeting = _newGreeting;
        missionHistory.push(Mission(_newGreeting, block.timestamp));
        emit GreetingChanged(msg.sender, _newGreeting, block.timestamp);
    }

    /**
     * @dev Retrieves the current greeting message.
     */
    function getGreeting() external view returns (string memory) {
        return currentGreeting;
    }

    /**
     * @dev Retrieves the mission history.
     */
    function getMissionHistory() external view returns (Mission[] memory) {
        return missionHistory;
    }
}
