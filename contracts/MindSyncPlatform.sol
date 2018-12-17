pragma solidity ^0.4.24;


contract Owned {
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    event SetOwner(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function setOwner(address newOwner) external onlyOwner {
        owner = newOwner;
        emit SetOwner(owner, newOwner);
    }
}


contract MindSyncPlatform is Owned {

    /* default 0x0 address constant */
    address public constant address0 = address(0);

    struct providerNodeInfo {
        bytes link;       // link to provider resources to work with and profile info
        address addr;       // address in ethereum
    }

    providerNodeInfo[] public ipfsNodes;
    providerNodeInfo[] public experts;
    providerNodeInfo[] public powerProviders;
    mapping(address => bool) public isRegistered;
    mapping(address => uint256) public reputations;
    mapping(address => bytes) public kycs;
    mapping(address => bool) public isExpert;

    address public mindSyncFoundation;

    uint256 public constant MAX_EXPERT_NODES = 100;
    uint256 public constant MAX_IPFS_NODES = 100;
    uint256 public constant MAX_POWER_PROVIDERS = 100;

    event UpVote(address user, address target);
    event DownVote(address user, address target);
    event RegisterExpert(address user, bytes link);
    event RegisterIpfsNode(address user, bytes link);
    event RegisterPowerProvider(address user, bytes link);
    event RegisterUser(address user);
    event RegisterKyc(address user, bytes kycInfo);
    event ReorderExperts(address user);

    constructor(address mindSyncFoundation_) public {
        mindSyncFoundation = mindSyncFoundation_;
    }

    modifier onlyExpert(address user) {
        require(isExpert[user]);
        _;
    }

    modifier requireUser(address user) {
        require(isRegistered[user]);
        _;
    }

    modifier requireKyc(address user) {
        require(isRegistered[user] && (kycs[user].length > 0));
        _;
    }


    function downVote(address target) external {
        reputations[target] -= 1;
        emit DownVote(msg.sender, target);
    }

    function upVote(address target) external {
        reputations[target] += 1;
        emit UpVote(msg.sender, target);
    }

    function ReorderAccordingToReputations() external onlyExpert(msg.sender) {
        providerNodeInfo[] memory newExperts = new providerNodeInfo[](experts.length);
        for (uint i = 0; i < experts.length; ++i) {
            newExperts[i] = experts[i];
        }
        for (i = 0; i < newExperts.length; ++i) {
            for (uint j = i + 1; j < newExperts.length; ++j) {
                if (reputations[newExperts[i].addr] < reputations[newExperts[j].addr]) {
                    providerNodeInfo memory ex = newExperts[i];
                    newExperts[i] = newExperts[j];
                    newExperts[j] = ex;
                }
            }
        }
        for (i = 0; i < experts.length; ++i) {
            experts[i] = newExperts[i];
        }
        emit ReorderExperts(msg.sender);
    }

    function registerUser() external {
        isRegistered[msg.sender] = true;
        emit RegisterUser(msg.sender);
    }

    function registerKyc(bytes kycInfo) external requireUser(msg.sender) {
        kycs[msg.sender] = kycInfo;
        emit RegisterKyc(msg.sender, kycInfo);
    }

    function registerExpert(bytes link) external requireKyc(msg.sender) {
        providerNodeInfo memory newExpert;
        newExpert.addr = msg.sender;
        newExpert.link = link;
        experts.push(newExpert);
        isExpert[msg.sender] = true;
        emit RegisterExpert(msg.sender, link);
    }

    function registerIpfsNode(bytes link) external requireKyc(msg.sender) {
        providerNodeInfo memory newIpfsNode;
        newIpfsNode.addr = msg.sender;
        newIpfsNode.link = link;
        ipfsNodes.push(newIpfsNode);
        emit RegisterIpfsNode(msg.sender, link);
    }

    function registerPowerProvider(bytes link) external requireKyc(msg.sender) {
        providerNodeInfo memory newPowerProvider;
        newPowerProvider.addr = msg.sender;
        newPowerProvider.link = link;
        powerProviders.push(newPowerProvider);
        emit RegisterPowerProvider(msg.sender, link);
    }



    function modifyMindSyncFoundationAddr(address newMindSyncFoundation_) external onlyOwner {
        mindSyncFoundation = newMindSyncFoundation_;
    }


    function() external {
        revert();
    }
}
