// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleMedicalRecord {
    struct Record {
        uint id;
        address patient;
        string recordHash;
        uint timestamp;
    }

    Record[] public records;
    mapping(address => uint) public patientRecordCount;

    event RecordCreated(uint id, address indexed patient, string recordHash, uint timestamp);

    function addRecord(address _patient, string memory _recordHash) public {
        uint recordId = records.length;
        records.push(Record(recordId, _patient, _recordHash, block.timestamp));
        patientRecordCount[_patient]++;
        emit RecordCreated(recordId, _patient, _recordHash, block.timestamp);
    }

    function getRecord(uint _recordId) public view returns (uint, address, string memory, uint) {
        Record memory record = records[_recordId];
        return (record.id, record.patient, record.recordHash, record.timestamp);
    }
}
