// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract Storage {

    string userID;
    string videoID;
    string modality;
    string dateRequest;
    string countryLang;
    string result;

    
    
    // Overwrite stored values in all variables in the memory on the BlockChain
    function storeData(string memory user, string memory video,  string memory mode, string memory date, string memory coun, string memory res) public {
        userID = user;
        videoID = video;
        modality = mode;
        dateRequest = date;
        countryLang = coun;
        result = res;
        
    }

    //Getter that does not consume GAS as it is a view function
    function retrieveData() public view returns (string memory, string memory, string memory, string memory, string memory, string memory){
        return (userID, videoID, modality, dateRequest, countryLang, result);
    }
}