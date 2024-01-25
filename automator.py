from web3 import Web3
from web3.gas_strategies.time_based import fast_gas_price_strategy
import asyncio

infura = "https://sepolia.infura.io/v3/447cd7339330401c9ea044dc8e6aaeae"

w3 = Web3(Web3.HTTPProvider(infura))

if w3.is_connected():
    print("Conexión exitosa a Infura")
else:
    print("No se pudo conectar a Infura")

w3.eth.set_gas_price_strategy(fast_gas_price_strategy)

sender = w3.to_checksum_address("0xA4209d06733c498eBfA092f0844D0948A5a524c0")
p_key = "8df3374506b3bee46f2f09f9e266f92fa61da3c026f8937d71ac67d18e5e7f30"

direccion_contrato = w3.to_checksum_address("0xD508a31dc572BD4b7A671E0363d36131e8BF6Eb8")
abi = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "whatContract",
				"type": "address"
			}
		],
		"name": "depositEth",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "yourContract",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "period",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			}
		],
		"name": "registerContract",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "withdrawEth",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

contrato = w3.eth.contract(address=direccion_contrato, abi=abi)

async def txs(con_add, period, name):
    nonce = w3.eth.get_transaction_count(sender)
    print("txs number", nonce)
    gas_price = w3.eth.generate_gas_price()
    print(type(sender), sender)
    txs = contrato.functions.registerContract(con_add, period, name).build_transaction({
        'from': sender, 
        'gas': 753737,
        'gasPrice': 55000000000,
        'nonce': nonce,
    })

    sign = w3.eth.account.sign_transaction(txs, p_key)
    
    tx_hash = w3.eth.send_raw_transaction(sign.rawTransaction)
    period = period + 1
    
    return tx_hash

con_add = w3.to_checksum_address("0xD508a31dc572BD4b7A671E0363d36131e8BF6Eb8")
period = 1 

name = "myFirstContract"

async def inicio():
    while True:
        tx_hash = await txs(con_add, period, name)
        print(f'Transacción enviada para registrar contrato. Hash: {tx_hash}')
        await asyncio.sleep(30)

asyncio.run(inicio())
