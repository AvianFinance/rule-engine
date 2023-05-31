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

# rental
def write_listing_rental(params):
    commands = [str("payable(_marketOwner).transfer(_listingFee);\n")]      
    commands.append(str("s_listings["+params[0]+"]["+params[1]+"] = Listing_sell(msg.sender, address(0)," + params[0] + "," + params[1] + "," + params[2] + "0);"))
    commands.append("r_listed.increment();")
    commands.append(str("EnumerableSet.add(r_address_tokens[" + params[0] + "]," + params[1] + ");"))
    commands.append(str("EnumerableSet.add(r_address," + params[0] + ");\n"))

    return(commands)

#installment 
def write_listing_installment(params):  
    commands = [str("payable(_marketOwner).transfer(_listingFee);\n")]      
    commands.append(str("i_listings["+params[0]+"]["+params[1]+"] = Listing_sell(msg.sender , address(0)," + params[0] + "," + params[1] + "," + params[2] + "0);"))
    commands.append("i_listed.increment();")
    commands.append(str("EnumerableSet.add(i_address_tokens[" + params[0] + "]," + params[1] + ");"))
    commands.append(str("EnumerableSet.add(i_address," + params[0] + ");\n"))

    return(commands)

# rental
def unlistNFT(params):
    commands = [str("EnumerableSet.remove(r_address_tokens[" + params[0] + "],"+ params[1] + ");\n")]      
    commands.append(str("delete r_listings["+params[0]+"]["+params[1]+"];"))
    commands.append(str("if (EnumerableSet.length(r_address_tokens[" + params[0] + "]) == 0) {"))
    commands.append(str("    EnumerableSet.remove(r_address," + params[0] + ");"))
    commands.append(str("}"))
    commands.append(str("r_listed.decrement();\n"))

    return(commands)

#installment
def unlistInsNFT(params):
    commands = [str("EnumerableSet.remove(i_address_tokens[" + params[0] + "],"+ params[1] + ");\n")]      
    commands.append(str("delete i_listings["+params[0]+"]["+params[1]+"];"))
    commands.append(str("if (EnumerableSet.length(i_address_tokens[" + params[0] + "]) == 0) {"))
    commands.append(str("    EnumerableSet.remove(i_address," + params[0] + ");"))
    commands.append(str("}"))
    commands.append(str("i_listed.decrement();\n"))

    return(commands)

#rental
def updateRentalList(params):
    commands = [str("Listing_rent storage listing = r_listings[" + params[0] + "][" + params[1] + "];")]
    commands.append(str("listing.pricePerDay = pricePerDay;"))

    return (commands)

#rental
def isRentableNFT(params):
    commands = [str("bool _isRentable = false;")]
    commands.append(str("bool _isNFT = false;"))
    commands.append(str("try IERC165(nftContract).supportsInterface(type(IERC4907).interfaceId) returns (bool rentable) {"))
    commands.append(str("   _isRentable = rentable;"))
    commands.append(str("} catch {"))
    commands.append(str("   return false;"))
    commands.append(str("}"))
    commands.append(str("try IERC165(nftContract).supportsInterface(type(IERC721).interfaceId) returns (bool nft) {"))
    commands.append(str("_isNFT = nft;"))
    commands.append(str("} catch {"))
    commands.append(str("return false;"))
    commands.append(str("}"))

    return(commands)

#rental
def isNFT(params):
    commands = [str("bool _isNFT = false;")]
    commands.append(str("try IERC165(nftContract).supportsInterface(type(IERC721).interfaceId) returns (bool nft) {"))
    commands.append(str("    _isNFT = nft;"))
    commands.append(str("} catch {"))
    commands.append(str("   return false;"))
    commands.append(str("}"))

    return(commands)

# Installment
def calculateInstallmentNFT(params):
    commands = [str("uint256 rentalFee =" + params[2] + "*" + params[1] + ";")]
    commands.append(str("uint256 installment_amount;"))
    commands.append(str("uint sum = (" + params[1] + "*(" + params[1] +"+1))/2;"))
    commands.append(str("uint256 unit_price = rentalFee/sum;"))
    commands.append(str("if (" + params[3] + "<" + params[1] + "){"))
    commands.append(str("installment_amount = unit_price*(" + params[1] + "-" + params[3] + "+1);"))
    commands.append(str("} else if (" + params[3] + "==" + params[1] + "){"))
    commands.append(str(" installment_amount = rentalFee -" + params[0] + ";"))
    commands.append(str("}"))

    return(commands)

def update_listing(params):
            
    commands = [str("s_listings["+params[0]+"]["+params[1]+"].price = " + params[2] + ";\n")]

    return(commands)

def delete_listing(params):
            
    commands = [str("delete s_listings["+params[0]+"]["+params[1]+"];")]
    commands.append(str("EnumerableSet.remove(s_address_tokens[" + params[0] + "]," + params[1] + ");"))
    commands.append(str("if (EnumerableSet.length(s_address_tokens[" + params[0] + "]) == 0) {"))
    commands.append(str("    EnumerableSet.remove(s_address," + params[0] + ");"))
    commands.append(str("}"))
    commands.append("s_listed.decrement();\n")

    return(commands)

def load_listing(params):

    if params[0] == "sell":
        command = "Listing_sell memory listedItem = s_listings"
    elif params[1] == "rent":
        command = "Listing_rent memory listedItem = r_listings"
    elif params[1] == "ins":
        command = "Listing_installment memory listedItem = i_listings"

    command = command + "["+params[1]+"]["+params[2]+"];\n"

    return([command])

def is_price_met(params):
            
    commands = [str("if (msg.value < listedItem.price) {")]
    commands.append(str("revert PriceNotMet(nftAddress, tokenId, listedItem.price);"))
    commands.append("}\n")

    return(commands)

def add_proceeds(params):

    command = "s_proceeds"

    if params[0] == "sell":
        command = "s_proceeds"
    elif params[1] == "rent":
        command = "r_proceeds"
    elif params[1] == "ins":
        command = "i_proceeds"

    command = command + "[listedItem.owner] += msg.value;\n"

    return([command])
    
def withdraw_proceeds(params):

    commands = []

    if params[0] == "sell":
        commands.append("uint256 proceeds = s_proceeds[msg.sender];")
    elif params[1] == "rent":
        commands.append("uint256 proceeds = r_proceeds[msg.sender];")
    elif params[1] == "ins":
        commands.append("uint256 proceeds = i_proceeds[msg.sender];")

    commands.append("if (proceeds <= 0) {")
    commands.append("   revert NoProceeds();")
    commands.append("}")

    commands.append('(bool success, ) = payable(msg.sender).call{value: proceeds}("");')
    commands.append('require(success,"Transfer failed");')

    if params[0] == "sell":
        commands.append("s_proceeds[msg.sender] = 0;\n")
    elif params[1] == "rent":
        commands.append("r_proceeds[msg.sender] = 0;\n")
    elif params[1] == "ins":
        commands.append("i_proceeds[msg.sender] = 0;\n")

    # commands.append("\n")

    return(commands)



def owner_transfer(params):

    command = "IERC721("+ params[0] + ").safeTransferFrom(listedItem.owner, msg.sender, " + params[1] + ");\n"

    return([command])


function_map = {
    "is_approved" : is_approved,
    "write_listing" : write_listing,
    "update_listing" : update_listing,
    "delete_listing" : delete_listing,
    "load_listing" : load_listing,
    "is_price_sufficient" : "function5",
    "add_proceeds" : "function6",
    "transfer_owner" : "function7",
    "withdraw_proceeds" : "function8",
    "write_listing_rental" : write_listing_rental,
    "unlistNFT" : unlistNFT,
    "updateRentalList" : updateRentalList,
    "isRentableNFT" : isRentableNFT,
    "isNFT" : isNFT,
    "write_listing_installment" : write_listing_installment,
    "unlistInsNFT" : unlistInsNFT,
    "calculateInstallmentNFT" : calculateInstallmentNFT,
    "is_price_met" : is_price_met,
    "add_proceeds" : add_proceeds,
    "owner_transfer" : owner_transfer,
    "withdraw_proceeds" : withdraw_proceeds
}

def build_rule(rule_name,rule_params):

    if rule_name in function_map:
        selected_function = function_map[rule_name]
        result = selected_function(rule_params)
        return(result)
    else:
        print("Invalid Rule Name")


