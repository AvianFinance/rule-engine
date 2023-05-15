def is_approved(params):

    commands = []
    commands.append(str("IERC721 nft = IERC721(" + str(params[0]) + ");"))
    commands.append(str("if (nft.getApproved(" + str(params[1]) + ") != address(this)) {"))
    commands.append("    revert NotApprovedForMarketplace();")
    commands.append("}\n")

    return(commands)


def write_listing(params):
            
    commands = [str("s_listings["+params[0]+"]["+params[1]+"] = Listing_sell(msg.sender," + params[0] + "," + params[1] + "," + params[2] + ");")]
    commands.append("s_listed.increment();")
    commands.append(str("EnumerableSet.add(s_address_tokens[" + params[0] + "]," + params[1] + ");"))
    commands.append(str("EnumerableSet.add(s_address," + params[0] + ");\n"))

    return(commands)

function_map = {
    "is_approved" : is_approved,
    "write_listing" : write_listing,
    "update_listing" : "update_listing",
    "delete_listing" : "function3",
    "load_listing" : "function4",
    "is_price_sufficient" : "function5",
    "add_proceeds" : "function6",
    "transfer_owner" : "function7",
    "withdraw_proceeds" : "function8"
}

def build_rule(rule_name,rule_params):

    if rule_name in function_map:
        selected_function = function_map[rule_name]
        result = selected_function(rule_params)
        for command in result:
            print(command)
        return(result)
    else:
        print("Invalid Rule Name")


