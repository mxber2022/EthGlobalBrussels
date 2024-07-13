// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract feedback {
    struct Record {
        string uuid;
        string secretName;
        string partyName;
    }

    mapping(string => Record) private records;
    string[] private uuids;

    function addRecord(string memory _uuid, string memory _secretName, string memory _partyName) public {
        require(bytes(records[_uuid].uuid).length == 0, "Record already exists");

        records[_uuid] = Record({
            uuid: _uuid,
            secretName: _secretName,
            partyName: _partyName
        });

        uuids.push(_uuid);
    }

    function getRecord(string memory _uuid) public view returns (string memory, string memory, string memory) {
        require(bytes(records[_uuid].uuid).length != 0, "Record does not exist");

        Record memory record = records[_uuid];
        return (record.uuid, record.secretName, record.partyName);
    }

    function updateRecord(string memory _uuid, string memory _newSecretName, string memory _newPartyName) public {
        require(bytes(records[_uuid].uuid).length != 0, "Record does not exist");

        records[_uuid].secretName = _newSecretName;
        records[_uuid].partyName = _newPartyName;
    }

    function getUUIDs() public view returns (string[] memory) {
        return uuids;
    }
}
