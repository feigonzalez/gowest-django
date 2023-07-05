/*
	Modal Preparation methods
	Each prepareXModal can take a parameter, e. If e is not set, the form will be empty.
	Otherwise, e is expected to be the button that showed the modal (by using the this keyword as parameter).
	If e is set correctly, the form will be filled with the corresponding data.
	Certain functions use e's data-id attribute and make a query to the database. Others use the data from
	the table directly. Which functions do what is not consistent.
*/

//	Prepares the Product Modal in the adminProducts page.
async function prepareProductModal(e){
	makeValid(get("productFormImage"));
	makeValid(get("productFormName"));
	makeValid(get("productFormPrice"));
	makeValid(get("productFormStock"));
	makeValid(get("productFormDescription"));
	if(e){
		//var product = null;
		var parent=e.parentElement.parentElement;
		get("productFormImagePreview").setAttribute("src",parent.children[0].children[0].getAttribute("src"));
		get("productFormName").value=parent.children[1].innerText;
		get("productFormPrice").value=parent.children[2].innerText;
		get("productFormStock").value=parent.children[3].innerText;
		get("productFormCategory").value=parent.children[4].innerText;
		get("productFormDescription").value=parent.children[5].innerHTML;
		get("productFormUpdate").value=true;
	} else {
		get("productFormImagePreview").setAttribute("src","");
		get("productFormName").value="";
		get("productFormPrice").value="";
		get("productFormStock").value="";
		get("productFormCategory").value="";
		get("productFormDescription").value="";
		get("productFormUpdate").value=false;
	}
}

//	Prepares the Category Modal in the adminCategories page.
async function prepareCategoryModal(e){
	makeValid(get("categoryFormName"));
	if(e){
		var parent=e.parentElement.parentElement;
		get("categoryFormName").value=e.dataset["name"];
		get("categoryFormId").value=e.dataset["id"];
		get("categoryFormUpdate").value="true";
	} else {
		get("categoryFormId").value="";
		get("categoryFormName").value="";
		get("categoryFormUpdate").value="false";
	}
}

//	Prepares the Client Modal in the adminClients page.
async function prepareClientModal(e){
	var user = (await selectAllWhere("users",(i)=>{return i["rut"]==e.dataset["id"]}))[0]
	var addresses = (await selectAllWhere("addresses",(i)=>{return i["userID"]==user["id"]}))
	get("clientFormName").innerText=user["name"];
	get("clientFormSurname").innerText=user["surname"];
	get("clientFormRUT").innerText=user["rut"];
	get("clientFormMail").innerText=user["mail"];
	get("clientFormPhone").innerText=user["phone"];
	get("clientFormAddressesHolder").innerHTML="";
	for(a of addresses){
		var district = (await selectAllWhere("districts",(i)=>{return i["id"]==a["districtID"]}))[0]
		get("clientFormAddressesHolder").innerHTML+=`<div>${a["street"]} ${a["number"]}, ${district["name"]}</div>`;
	}
}

/*
	Prepares the Sales Modal in both the adminSales page and the clientSales page.
*/

async function prepareSaleModal(e){
	data = (await fetch("/api/getSaleDetails/"+e.dataset["id"]).then(r=>r.json()));
	saleuser=data["sale"]["user"];
	if(saleuser!=undefined) get("saleFormUser").innerText=saleuser;
	else get("saleFormUserRow").classList.add("hidden");
	get("saleFormAddress").innerText=data["address"];
	get("saleFormSaleDate").innerText=data["sale"]["saleDate"];
	get("saleFormDeliveryDate").innerText=data["sale"]["deliveryDate"];
	get("saleFormStatus").innerHTML=formatSaleStatus(data["sale"]["status"]);
	get("saleFormTotal").innerHTML="$"+data["sale"]["total"];
	var newInnerHTML="<table class='table text-center'>\n<tr><th>Producto</th><th>Precio</th><th>Unidades</th><th>Subtotal</th></tr>\n";
	for(d of data["details"]){
		newInnerHTML+=`<tr><td>${d["productName"]}</td><td>$${d["productPrice"]}</td><td>${d["units"]}</td><td>$${d["subtotal"]}</td></tr>\n`;
	}
	newInnerHTML+="</table>";
	get("saleFormDetailsHolder").innerHTML=newInnerHTML;
}

//	Prepares the Administrator Modal in the adminAdministrators page.
async function prepareAdministratorModal(e){
	makeValid(get("adminFormNewName"));
	makeValid(get("adminFormNewSurname"));
	makeValid(get("adminFormNewRUT"));
	makeValid(get("adminFormNewMail"));
	makeValid(get("adminFormNewPhone"));
	if(e){
		get("adminFormShow").classList.remove("hidden");
		get("adminFormNew").classList.add("hidden");
		var user = (await selectAllWhere("users",(i)=>{return i["rut"]==e.dataset["id"]}))[0];
		get("adminFormShowName").innerText=user["name"];
		get("adminFormShowSurname").innerText=user["surname"];
		get("adminFormShowRUT").innerText=user["rut"];
		get("adminFormShowMail").innerText=user["mail"];
		get("adminFormShowPhone").innerText=user["phone"];
	} else {
		get("adminFormShow").classList.add("hidden");
		get("adminFormNew").classList.remove("hidden");
	}
}
//	Prepares the Address Modal in the clientAccounr page.
async function prepareAddressModal(e){
	makeValid(get("addressFormStreet"));
	makeValid(get("addressFormNumber"));
	makeValid(get("addressFormPostalCode"));
	get("addressFormDistrict").value="";
	if(e==null){
		get("addressFormStreet").value="";
		get("addressFormNumber").value="";
		get("addressFormPostalCode").value="";
		get("addressFormDistrict").value=0;
		get("addressFormUpdate").value=false;
		get("addressFormId").value="";
	} else {
		address = (await fetch("/api/getAddress/"+e.dataset["id"]).then(r=>r.json()))
		get("addressFormStreet").value=address["streetName"];
		get("addressFormNumber").value=address["streetNumber"];
		get("addressFormPostalCode").value=address["postalCode"];
		get("addressFormDistrict").value=address["district"];
		get("addressFormUpdate").value=true;
		get("addressFormId").value=address["id"];
	}
}

/*
	Confirm Action Modals
	Certain actions should require user confirmation before being taken.
	A few modals are used for asking cofirmation, and a function is called in each
	instance to prepare the modal with the correct text and functionality.
*/

//	Prepares the deleteAdministrator delete modal from the adminAdministrators page.
function confirmDeleteAdministrator(e){
	var name=e.parentElement.parentElement.children[0].innerText;
	get("deleteAlertTarget").value=e.dataset["id"];
	get("deleteAlertOrigin").value="adminAdministrators";
	get("deleteAlertMessage").innerText=`¿Eliminar administrador ${name}?`;
	get("deleteAlertConfirm").setAttribute("onclick","moveTo('adminIndex.html',[['t','admins']])");
}

//	Prepares the deleteProduct delete modal from the adminProducts page.
function confirmDeleteProduct(e){
	var name=e.parentElement.parentElement.children[1].innerText;
	get("deleteAlertTarget").value=e.dataset["id"];
	get("deleteAlertOrigin").value="adminProducts";
	get("deleteAlertMessage").innerText=`¿Eliminar producto ${name}?`;
	get("deleteAlertConfirm").setAttribute("onclick","moveTo('adminIndex.html',[['t','products']])");
}

//	Prepares the deleteCategory delete modal from the adminCategories page.
function confirmDeleteCategory(e){
	var name=e.dataset["name"];//e.parentElement.parentElement.children[0].innerText;
	get("deleteAlertTarget").value=e.dataset["id"];
	get("deleteAlertOrigin").value="adminCategories";
	get("deleteAlertMessage").innerText=`¿Eliminar categoría ${name} y todos los productos relacionados?`;
	//get("deleteAlertConfirm").setAttribute("onclick","moveTo('adminIndex.html',[['t','categories']])");
}

//	Prepares the deleteAddress delete modal from the clientAccount page.
function confirmDeleteAddress(e){
	var name=e.parentElement.parentElement.children[0].innerText;
	get("deleteAlertTarget").value=e.dataset["id"];
	get("deleteAlertOrigin").value="clientAccount";
	get("deleteAlertMessage").innerText=`¿Eliminar dirección ${name}?`;
}

//	Prepares the confirmSale confirm modal from the clientSales page.
function confirmSaleReception(e){
	var id=e.dataset["id"];
	get("saleAlertAction").value="reception";
	get("saleAlertTarget").value=e.dataset["id"];
	get("saleAlertMessage").innerText=`¿Confirmar que la compra de código ${id} fue entregada?`;
	get("saleAlertConfirm").setAttribute("onclick","moveTo('account.html',[['t','sales']])");
}

//	Prepares the confirmShipment confirm modal from the adminSales page.
function confirmSaleShipment(e){
	var id=e.dataset["id"];
	get("saleAlertAction").value="shipment";
	get("saleAlertTarget").value=e.dataset["id"];
	get("saleAlertMessage").innerText=`¿Confirmar que la compra de código ${id} fue enviada?`;
	get("saleAlertConfirm").setAttribute("onclick","moveTo('adminIndex.html',[['t','sales']])");
}