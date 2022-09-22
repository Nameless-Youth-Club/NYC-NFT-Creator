import { ethers } from "ethers";
import NYCDescriptor from '../utils/NYCDescriptor.json';
import React, { useState } from "react";

//import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';


const CONTRACT_DESCRIPTOR_ADDRESS = "0xCFdf38f7e7Cf2aA267EE70608525590aDA06531E";

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: "#000000",
  padding: theme.spacing(1),
  textAlign: 'center',
  color: '#FD593D',
  fontSize: '25px',
  fontFamily: "myfont"
}));


const OwnedNFTs = () => {

  const [balance, setBalance] = useState("");
  const [tokens, setTokens] = useState([])


  async function getNFTs() {
    const { ethereum } = window;
    if (ethereum) {
      const provider = new ethers.providers.Web3Provider(ethereum);
      const signer = provider.getSigner();
      const accounts = await ethereum.request({ method: 'eth_accounts' });
      const account = accounts[0]

      const connectedDescriptorContract = new ethers.Contract(CONTRACT_DESCRIPTOR_ADDRESS, NYCDescriptor.abi, signer)

      const accountBalance = await connectedDescriptorContract.balanceOf(account);
      setBalance(accountBalance.toNumber())

      const acctTokens = []
    
      for (let i = 0; i < balance; i ++) {
        acctTokens.push(await connectedDescriptorContract.tokenOfOwnerByIndex(account, i))
      }
      setTokens(acctTokens)
    }
  }
   

  getNFTs()

  return (
    <Box sx = {{width: '50%'}}>
      
      <Stack spacing={2}>
        <Item> NFTs owned by you: {balance} </Item>
        <Item> Tokens:  {tokens} </Item>
       
      </Stack>
    </Box>
  );
};

export default OwnedNFTs;