def is_approved(params):

    commands = []
    commands.append(str("IERC721 nft = IERC721(" + str(params[0]) + ");"))
    commands.append(str("if (nft.getApproved(" + str(params[1]) + ") != address(this)) {"))
    commands.append("    return false;")
    commands.append("} else {")
    commands.append("    return true;")
    commands.append("}\n")

    return(commands)

def write_listing(params):
            
    commands = [str("s_listings["+params[0]+"]["+params[1]+"] = Listing_sell(msg.sender," + params[0] + "," + params[1] + "," + params[2] + ");")]
    commands.append(str("EnumerableSet.add(s_address_tokens[" + params[0] + "]," + params[1] + ");"))
    commands.append(str("EnumerableSet.add(s_address," + params[0] + ");\n"))

    return(commands)

def write_listing_rental(params):
    commands = []      
    commands.append(str("r_listings["+params[0]+"]["+params[1]+"] = Listing_rent(msg.sender,address(0)," + params[0] + "," + params[1] + "," + params[2] + ",0);"))
    commands.append(str("EnumerableSet.add(r_address_tokens[" + params[0] + "]," + params[1] + ");"))
    commands.append(str("EnumerableSet.add(r_address," + params[0] + ");\n"))

    return(commands)

def pay_listing_fee(params): 

    commands = ["require(msg.value >= " + params[1] + ",'Not enough ether for payment');","payable(" + params[0] + ").transfer(" + params[1] + ");\n"]      

    return(commands)

def write_listing_installment(params):  
    commands = []      
    commands.append(str("i_listings["+params[0]+"]["+params[1]+"] = Listing_installment(msg.sender,address(0)," + params[0] + "," + params[1] + "," + params[2] + ",0,0,0,0);"))
    commands.append(str("EnumerableSet.add(i_address_tokens[" + params[0] + "]," + params[1] + ");"))
    commands.append(str("EnumerableSet.add(i_address," + params[0] + ");\n"))

    return(commands)

def unlistNFT(params):
    commands = [str("EnumerableSet.remove(r_address_tokens[" + params[0] + "],"+ params[1] + ");")]      
    commands.append(str("delete r_listings["+params[0]+"]["+params[1]+"];"))
    commands.append(str("if (EnumerableSet.length(r_address_tokens[" + params[0] + "]) == 0) {"))
    commands.append(str("    EnumerableSet.remove(r_address," + params[0] + ");"))
    commands.append(str("}\n"))

    return(commands)

def unlistInsNFT(params):
    commands = [str("EnumerableSet.remove(i_address_tokens[" + params[0] + "],"+ params[1] + ");")]
    if params[2] == "full": 
        commands.append(str("delete i_listings["+params[0]+"]["+params[1]+"];"))
    commands.append(str("if (EnumerableSet.length(i_address_tokens[" + params[0] + "]) == 0) {"))
    commands.append(str("    EnumerableSet.remove(i_address," + params[0] + ");"))
    commands.append(str("}\n"))

    return(commands)

def updateRentalList(params):
    commands = [str("Listing_rent storage listing = r_listings[" + params[0] + "][" + params[1] + "];")]
    commands.append(str("listing.pricePerDay = price;\n"))

    return (commands)

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

def isNFT(params):
    commands = [str("bool _isNFT = false;")]
    commands.append(str("try IERC165(nftContract).supportsInterface(type(IERC721).interfaceId) returns (bool nft) {"))
    commands.append(str("    _isNFT = nft;"))
    commands.append(str("} catch {"))
    commands.append(str("   return false;"))
    commands.append(str("}"))

    return(commands)

def calculateInstallmentNFT(params):
    commands = [str("uint256 rentalFee = " + params[2] + "*" + params[1] + ";")]
    commands.append(str("uint256 installment_amount;"))
    commands.append(str("uint sum = (" + params[1] + "*(" + params[1] +"+1))/2;"))
    commands.append(str("uint256 unit_price = rentalFee/sum;"))
    commands.append(str("if (" + params[3] + "<" + params[1] + "){"))
    commands.append(str("installment_amount = unit_price*(" + params[1] + " - " + params[3] + " +1);"))
    commands.append(str("} else if (" + params[3] + "==" + params[1] + "){"))
    commands.append(str(" installment_amount = rentalFee - " + params[0] + ";"))
    commands.append(str("}\n"))

    return(commands)

def update_listing(params):
            
    commands = [str("s_listings["+params[0]+"]["+params[1]+"].price = " + params[2] + ";\n")]

    return(commands)

def delete_listing(params):
            
    commands = [str("delete s_listings["+params[0]+"]["+params[1]+"];")]
    commands.append(str("EnumerableSet.remove(s_address_tokens[" + params[0] + "]," + params[1] + ");"))
    commands.append(str("if (EnumerableSet.length(s_address_tokens[" + params[0] + "]) == 0) {"))
    commands.append(str("    EnumerableSet.remove(s_address," + params[0] + ");"))
    commands.append(str("}\n"))

    return(commands)

def load_listing(params):

    if params[0] == "sell":
        command = "Listing_sell memory listing = s_listings"
    elif params[0] == "rent":
        command = "Listing_rent memory listing = r_listings"
    elif params[0] == "ins":
        command = "Listing_installment memory listing = i_listings"

    command = command + "["+params[1]+"]["+params[2]+"];\n"

    return([command])

def is_price_met(params):
            
    commands = [str("if (msg.value < " + params[0] + ") {")]
    commands.append(str("revert PriceNotMet(nftAddress, tokenId, " + params[0] + ");"))
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

    command = command + "[listing.owner] += msg.value;\n"

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

    command = "IERC721("+ params[0] + ").safeTransferFrom(listing.owner, msg.sender, " + params[1] + ");\n"

    return([command])

def is_nft_listing_rented(params):

    command = "require(listing.user == address(0) || block.timestamp > listing.expires,'NFT already rented');\n"

    return([command])

def is_expiry_in_future(params):
        
    commands = [str("if (isRentableNFT(" + str(params[0]) + ")){")]
    commands.append(str("   IERC4907 nft = IERC4907(" + str(params[0]) + ");"))
    commands.append(str("   uint256 expiry = nft.userExpires(" + str(params[1]) + ");"))
    commands.append(str("   if (block.timestamp < expiry){"))
    commands.append(str("       return false;"))
    commands.append(str("   } else {"))
    commands.append(str("       return true;"))
    commands.append(str("   }"))
    commands.append(str("} else {"))
    commands.append(str("   return true;"))
    commands.append("}\n")

    return(commands)

def rent_nft(params):
    commands = [str("uint256 rentalFee = listing.pricePerDay * numDays;")]
    commands.append(str("uint64 expires = uint64(block.timestamp) + (numDays*86400);"))
    commands.append(str("IERC4907(" + params[0] + ").setUser(" + params[1] + ", msg.sender, expires);"))
    commands.append(str("listing.user = msg.sender;"))
    commands.append(str("listing.expires = expires;\n"))

    return(commands)

def get_ins(params):
    if params[0] == "first":
        command = ["uint256 rentalFee = calculateInstallment(0,numDays,listing.pricePerDay,1);\n"]
    elif params[0] == "next":
        command = ["uint256 rentalFee = calculateInstallment(listing.paidIns,listing.installmentCount,listing.pricePerDay,nextIndex);"]

    return(command)

def add_to_ins_listing(params):
    commands = []
    if params[0] == "first":
        commands.append("uint64 expires = uint64(block.timestamp) + 86400;")
        commands.append("listing.user = msg.sender;")
        commands.append("listing.expires = expires;")
        commands.append("listing.installmentCount = numDays;")
        commands.append("listing.installmentIndex = 1;")
        commands.append("listing.paidIns = rentalFee;\n")
    elif params[0] == "next":
        commands.append("uint64 expires = listing.expires + 86400;")
        commands.append("uint64 currIndex = listing.installmentIndex;")
        commands.append("uint64 nextIndex = currIndex + 1;")
        commands.append("listing.expires = expires;")
        commands.append("uint256 rentalFee = calculateInstallment(listing.paidIns,listing.installmentCount,listing.pricePerDay,nextIndex);")
        commands.append("uint256 totalPaid = listing.paidIns + rentalFee;")
        commands.append("listing.installmentIndex = nextIndex;")
        commands.append("listing.paidIns = totalPaid;\n")

    return commands

def update_nft_for_rent(params):
    commands = ["IERC4907(" + params[0] + ").setUser(" + params[1] + ", " + params[2] + ", " + params[3] + ");\n"]
    return commands

def conds_pay_ins(params):
    commands = []
    commands.append("require(listing.user == msg.sender,'You are not the current renter');")
    commands.append("require(listing.installmentIndex < listing.installmentCount,'Rental fee is fully paid');")
    commands.append("require(listing.installmentIndex >= 1,'Rental agreement not yet made');")
    commands.append("require(block.timestamp < listing.expires,'NFT expired');\n")

    return(commands)

def finalise_ins_pay(params):
    commands = []

    commands.append("emit InstNftInsPaid(IERC721(nftAddress).ownerOf(tokenId), msg.sender, nftAddress, tokenId, expires, listing.installmentCount, nextIndex, rentalFee);")
    commands.append("if (listing.installmentIndex == listing.installmentCount){")
    commands.append("   delete i_listings[nftAddress][tokenId];")
    commands.append("}\n")
    
    return commands

function_map = {
    "is_approved" : is_approved,
    "write_listing" : write_listing,
    "update_listing" : update_listing,
    "delete_listing" : delete_listing,
    "load_listing" : load_listing,
    "write_listing_rental" : write_listing_rental,
    "unlistNFT" : unlistNFT,
    "updateRentalList" : updateRentalList,
    "isRentableNFT" : isRentableNFT,
    "isNFT" : isNFT,
    "write_listing_installment" : write_listing_installment,
    "unlistInsFull" : unlistInsNFT,
    "unlistInsPartial" : unlistInsNFT,
    "calculateInstallmentNFT" : calculateInstallmentNFT,
    "is_price_met" : is_price_met,
    "add_proceeds" : add_proceeds,
    "owner_transfer" : owner_transfer,
    "withdraw_proceeds" : withdraw_proceeds,
    "pay_market_owner" : pay_listing_fee,
    "pay_rentalFee" : pay_listing_fee,
    "pay_price" : pay_listing_fee,
    "is_nft_listing_rented" : is_nft_listing_rented,
    "is_expiry_in_future" : is_expiry_in_future,
    "rent_nft" : rent_nft,
    "get_ins" : get_ins,
    "update_next_ins_listing" : add_to_ins_listing,
    "update_first_ins_listing" : add_to_ins_listing,
    "update_nft_for_rent" : update_nft_for_rent,
    "conds_pay_ins" : conds_pay_ins,
    "finalise_ins_pay" : finalise_ins_pay
}

def build_rule(rule_name,rule_params):

    if rule_name in function_map:
        selected_function = function_map[rule_name]
        result = selected_function(rule_params)
        return(result)
    else:
        print("Invalid Rule Name")


