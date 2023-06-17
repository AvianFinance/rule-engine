from pinata import Pinata
from services.remove_file import remove

api_key = '27de8ecd448d490b75a8'
api_secret = '4d80dee97df83b16f31b72629d3b98f806db005a6c642b8ce65a7e3c45f50548'
access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJhM2ZiNjlhOS1hYjcxLTQ0ODgtYThkMC03M2FiNmVmODk4YzEiLCJlbWFpbCI6ImZzY2ltcGwuaXJtaW90QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfSx7ImlkIjoiTllDMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiIyN2RlOGVjZDQ0OGQ0OTBiNzVhOCIsInNjb3BlZEtleVNlY3JldCI6IjRkODBkZWU5N2RmODNiMTZmMzFiNzI2MjlkM2I5OGY4MDZkYjAwNWE2YzY0MmI4Y2U2NWE3ZTNjNDVmNTA1NDgiLCJpYXQiOjE2ODYwNjg4NDl9.kcsINOtgCv2k-b-FtFZ7isVSDPnwK-2mEED0bT75Eu4'

pinata = Pinata(api_key, api_secret, access_token)

def upload_contract(contract_name,check_type):

    file_path = "contracts/" + check_type + "/" + contract_name + "_logic.txt"

    upload_response = {"status":"success","data":{"IpfsHash":"QmajLeFicAfU2DQGG7MZ9DGUQQgQWXadiG5zsccvi2obEK"}}#pinata.pin_file(file_path)

    remove(file_path)

    if upload_response['status'] == "success":
        return(upload_response['data']['IpfsHash'])
    else:
        return('File upload failed ! with error')
