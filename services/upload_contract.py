from pinata import Pinata

api_key = '10a00ea393b986710b82'
api_secret = '3d1595df8852a11e7606afa6fbd2aecbaf7575509368316c679cb1706845b801'
access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJhM2ZiNjlhOS1hYjcxLTQ0ODgtYThkMC03M2FiNmVmODk4YzEiLCJlbWFpbCI6ImZzY2ltcGwuaXJtaW90QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfSx7ImlkIjoiTllDMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiIxMGEwMGVhMzkzYjk4NjcxMGI4MiIsInNjb3BlZEtleVNlY3JldCI6IjNkMTU5NWRmODg1MmExMWU3NjA2YWZhNmZiZDJhZWNiYWY3NTc1NTA5MzY4MzE2YzY3OWNiMTcwNjg0NWI4MDEiLCJpYXQiOjE2ODU2MTA1MjV9.1fKA8IWg3GIkpIG5hh3pLzAk5JlKtbwtbP8k_JMhQ8c'

pinata = Pinata(api_key, api_secret, access_token)

def upload_contract(contract_name):

    file_path = "contracts/new/" + contract_name +"_logic.txt"

    upload_response = pinata.pin_file(file_path)

    print(upload_response)

    if upload_response['status'] == "success":
        return(upload_response['data']['IpfsHash'])
    else:
        return('File upload failed ! with error')


