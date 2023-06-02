from sm_handler.writer import write_contract
from sm_handler.deployer import deploy_compiled_contract
from services.upload_contract import upload_contract
from sm_handler.compiler import compile_export_contract


async def async_upload_contract(contract_name):
    return upload_contract(contract_name)

async def async_compile_export_contract(contract_name):
    return compile_export_contract(contract_name)

async def async_deploy_compiled_contract(contract_name):
    return deploy_compiled_contract(contract_name)

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
                packet.append(str('https://gateway.pinata.cloud/ipfs/' + str(ipfs_hash)))
                print("Uploading Done")
                compile_status = await async_compile_export_contract(contract_type)
                if compile_status == "Succesful":
                    print("Compiling Done")
                    deploy_status = await async_deploy_compiled_contract(contract_type.capitalize())
                    if deploy_status == False:
                        return("Deploying Failed")
                    else:
                        packet.append(deploy_status)
                        return(packet)
        else:
            return("Writing Failed")
    except Exception as e:
        print(e)
        return("Full flow failed")


    # body = request.data
    # data = json.loads(body)
    # id = get_collections_length()

    # new_contract = {
    #   "id": id,
    #   "contract_name": contract_type,
    #   "contract_address": result,
    #   "address": "url",
    #   "events": data["eventsList"],
    #   "modifiers": data["modifiersList"],
    #   "errors": data["errorsList"],
    #   "status" : "active"
    # }
    # insert_collection(new_contract)
    # return jsonify({result, "url"})
