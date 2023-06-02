from sm_handler.writer import write_contract
from sm_handler.deployer import deploy_compiled_contract
from services.upload_contract import upload_contract
from sm_handler.compiler import compile_export_contract
from services.db import insert_collection

async def async_upload_contract(contract_name):
    return upload_contract(contract_name)

async def async_compile_export_contract(contract_name):
    return compile_export_contract(contract_name)

async def async_deploy_compiled_contract(contract_name):
    return deploy_compiled_contract(contract_name)

async def update_pending_contract_db(id,contract_type,contract_address,ipfs_hash):
    try:
        new_contract = {
            "id": id,
            "contract_name": contract_type,
            "contract_address": contract_address,
            "address": ipfs_hash,
            "status" : "active"
        }

        insert_collection(new_contract)
        return("Success")
    except Exception as e:
        print(e)
        return("Failed")

async def full_flow(contract_type):

    packet = []

    try:
        write_status = write_contract(contract_type)
        if write_status == "Writing Successful":
            print("Writing Done")
            ipfs_hash = await async_upload_contract(contract_type)
            if ipfs_hash == 'File upload failed ! with error':
                return("Uploading Failed")
            else:
                print("Uploading Done")
                packet.append(str('https://gateway.pinata.cloud/ipfs/' + str(ipfs_hash)))
                compile_status = await async_compile_export_contract(contract_type)
                if compile_status == "Succesful":
                    print("Compiling Done")
                    deploy_status = await async_deploy_compiled_contract(contract_type.capitalize())
                    if deploy_status == False:
                        return("Deploying Failed")
                    else:
                        print("Deploying Done")
                        packet.append(deploy_status)
                        db_status = await update_pending_contract_db(5,contract_type,deploy_status,ipfs_hash)
                        if(db_status=="Success"):
                            print("DB Update Done")
                        return(packet)
                else:
                    return("Compiling Failed")
        else:
            return("Writing Failed")
    except Exception as e:
        print(e)
        return("Full flow failed")


