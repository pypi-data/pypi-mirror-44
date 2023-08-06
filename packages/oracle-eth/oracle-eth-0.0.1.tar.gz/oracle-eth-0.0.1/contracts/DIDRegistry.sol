pragma solidity ^0.4.4;

contract DIDRegistry {

    address public contract_owner;
    mapping(address => address) public id_owners;
    mapping(bytes32 => mapping(address => uint)) public organizations; // attribute to its organization
    mapping(address => uint) public DIDOperators;
    mapping(address => uint) public organizationOperators;

    event ContractOwnerChange(address indexed newOwner);
    event DIDOwnerChanged(address indexed identity, address newOwner);
    event DIDOrganizationChanged(bytes32 organizationType, address organization, uint value);
    event DIDAttributeChange(address indexed identity, bytes32 name, bytes value);
    event DIDAttributeConfirmed(address indexed identity, bytes32 name, bytes value);

    event SetAttributeSignedCalled(address indexed identity, uint8 sigV, bytes32 sigR, bytes32 sigS, bytes32 name, bytes value);
    event CheckSignatureCalled(address indexed identity, uint8 sigV, bytes32 sigR, bytes32 sigS, bytes32 hash);
    event SignatureOK(address indexed identity, address idOwner);
    event ComputedHash(bytes32 computedHash);


    modifier onlyDIDOperator() {
        require (DIDOperators[msg.sender] == 1);
        _;
    }

    modifier onlyOrganizationsOperator() {
        require (organizationOperators[msg.sender] == 1);
        _;
    }

    modifier onlyContractOwner {
        require (msg.sender == contract_owner);
        _;
    }

    function changeContractOwner(address newOwner) public onlyContractOwner {
        contract_owner = newOwner;
        ContractOwnerChange(newOwner);
    }

    function getContractOwner() public returns(address) {
        return contract_owner;
    }

    function setDIDOperator(address operator, uint value) public onlyContractOwner {
        DIDOperators[operator] = value;
    }

    function getDIDOperator(address operator) public returns(uint) {
        return DIDOperators[operator];
    }

    function setOrganizationOperator(address operator, uint value) public onlyContractOwner {
        organizationOperators[operator] = value;
    }

    function getOrganizationOperator(address operator) public returns(uint) {
        return organizationOperators[operator];
    }

    modifier onlyOrganization(bytes32 attribute) {
        require (organizations[attribute][msg.sender] == 1);
        _;
    }

    function setOrganization(bytes32 attribute, address organization, uint value) public onlyOrganizationsOperator {
        organizations[attribute][organization] = value;
        DIDOrganizationChanged(attribute, organization, value);
    }

    function getOrganization(bytes32 attribute, address organization) public returns(uint) {
        return organizations[attribute][organization];
    }

    function DIDRegistry() public {
        contract_owner = msg.sender;
    }

    function identityOwner(address identity) public view returns(address) {
        address owner = id_owners[identity];
        if (owner != 0x0) {
            return owner;
        }
        return identity;
    }

    modifier onlyDIDOwner(address identity, address owner) {
        require (identityOwner(identity) == owner);
        _;
    }

    function changeDIDOwner(address identity, address newOwner) public onlyDIDOperator {
        id_owners[identity] = newOwner;
        DIDOwnerChanged(identity, newOwner);
    }

    function checkSignature(address identity, uint8 sigV, bytes32 sigR, bytes32 sigS, bytes32 hash) internal returns(address) {
        address signer = ecrecover(hash, sigV, sigR, sigS);
        require(signer == identityOwner(identity));
        return signer;
    }

    function setAttributeSigned(address identity, uint8 sigV, bytes32 sigR, bytes32 sigS, bytes32 name, bytes value) public {
        // bytes32 hash = keccak256(this, identity, name, value);
        // address signer = ecrecover(name, sigV, sigR, sigS);
        // setAttribute(identity, checkSignature(identity, sigV, sigR, sigS, hash), name, value);
        DIDAttributeChange(identity, name, value);
    }

    function setAttribute(address identity, address owner, bytes32 name, bytes value) public onlyDIDOwner(identity, owner) {
        DIDAttributeChange(identity, name, value);
    }

    function confirmAttribute(address identity, bytes32 name, bytes value) public onlyOrganization(name) {
        DIDAttributeConfirmed(identity, name, value);
    }

//    function getSender(uint8 sigV, bytes32 sigR, bytes32 sigS, bytes32 hash) public returns(address) {
//        return ecrecover(hash, sigV, sigR, sigS);
//    }

}


