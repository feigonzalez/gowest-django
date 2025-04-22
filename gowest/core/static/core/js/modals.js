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
		var product = (await fetch("/api/getProduct/"+e.dataset["id"]).then(r=>r.json()))
		if(product === false) return;	//error on API
		get("productFormImagePreview").setAttribute("src",product["image"]);
		get("productFormName").value=product["name"]
		get("productFormPrice").value=product["price"]
		get("productFormStock").value=product["stock"]
		get("productFormCategory").value=product["category"]
		get("productFormDescription").value=product["description"]
		get("productFormId").value=product.id;
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
		var category = (await fetch("/api/getCategory/"+e.dataset["id"]).then(r=>r.json()))
		if(category === false) return;	//error on API
		get("categoryFormName").value=category.name;
		get("categoryFormId").value=e.dataset["id"];
		get("categoryFormUpdate").value="true";
	} else {
		get("categoryFormName").value="";
		get("categoryFormId").value="";
		get("categoryFormUpdate").value="false";
	}
}

//	Prepares the Client Modal in the adminClients page.
async function prepareClientModal(e){
	var user = (await fetch("/api/getUser/"+e.dataset["id"]).then(r=>r.json()))
	var addresses = (await fetch("/api/getAddressesByUser/"+e.dataset["id"]).then(r=>r.json()))
	if(user === false || addresses === false ) return;	//error on API
	get("clientFormName").innerText=user["name"];
	get("clientFormSurname").innerText=user["surname"];
	get("clientFormRUT").innerText=user["rut"];
	get("clientFormMail").innerText=user["mail"];
	get("clientFormPhone").innerText=user["phone"];
	get("clientFormAddressesHolder").innerHTML="";
	for(let a of addresses){
		get("clientFormAddressesHolder").innerHTML+=`<li>${a["streetName"]} ${a["streetNumber"]}, ${a["districtName"]}</li>`;
	}
}

/*
	Prepares the Sales Modal in both the adminSales page and the clientSales page.
*/

async function prepareSaleModal(e){
	let data = (await fetch("/api/getSaleDetails/"+e.dataset["id"]).then(r=>r.json()));
	if(data === false) return;	//error on API
	let saleuser=data["sale"]["user"];
	//hides the client if the session user is an admin.
	//this happens when an admin sees a client's purchase
	if(saleuser!=undefined) get("saleFormUser").innerText=saleuser;
	else get("saleFormUserRow").classList.add("hidden");
	get("saleFormAddress").innerText=data["address"];
	get("saleFormSaleDate").innerText=data["sale"]["saleDate"];
	get("saleFormDeliveryDate").innerText=data["sale"]["deliveryDate"];
	get("saleFormStatus").innerHTML=formatSaleStatus(data["sale"]["status"]);
	get("saleFormDiscount").innerHTML=(data["sale"]["subscribed"]==1?"Sí":"No");
	get("saleFormTotal").innerHTML="$"+Math.floor(parseInt(data["sale"]["total"])*(data["sale"]["subscribed"]==1?0.9:1));
	let newInnerHTML="<table class='table text-center'>\n<tr><th>Producto</th><th>Precio</th><th>Unidades</th><th>Subtotal</th></tr>\n";
	for(let d of data["details"]){
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
		var user = (await fetch("/api/getUser/"+e.dataset["id"]).then(r=>r.json()))
		if(user === false) return;	//error on API
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
//	Prepares the Address Modal in the clientAccount page.
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
		let address = (await fetch("/api/getAddress/"+e.dataset["id"]).then(r=>r.json()))
		if(address === false) return;	//error on API
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
}

//	Prepares the deleteProduct delete modal from the adminProducts page.
function confirmDeleteProduct(e){
	var name=e.dataset["name"];
	get("deleteAlertTarget").value=e.dataset["id"];
	get("deleteAlertOrigin").value="adminProducts";
	get("deleteAlertConfirm").value="Desactivar";
	get("deleteAlertMessage").innerText=`¿Desactivar producto ${name}?`;
}
//	Prepares the activateProduct activation modal from the adminProducts page.
function confirmActivateProduct(e){
	var name=e.dataset["name"];
	get("activateAlertTarget").value=e.dataset["id"];
	get("activateAlertOrigin").value="adminProducts";
	get("activateAlertMessage").innerText=`¿Activar producto ${name}?`;
}

//	Prepares the deleteCategory delete modal from the adminCategories page.
function confirmDeleteCategory(e){
	var name=e.dataset["name"];
	get("deleteAlertTarget").value=e.dataset["id"];
	get("deleteAlertConfirm").value="Desactivar";
	get("deleteAlertOrigin").value="adminCategories";
	get("deleteAlertMessage").innerHTML=`¿Desactivar categoría ${name}?<br>`+
	"<div class='alert alert-warning'>Los productos de esta categoría seguirán "+
	"activos, pero los clientes no podrán verlos.</div>";
}

function confirmActivateCategory(e){
	var name=e.dataset["name"];
	get("activateAlertTarget").value=e.dataset["id"];
	get("activateAlertOrigin").value="adminCategories";
	get("activateAlertMessage").innerText=`¿Activar categoría ${name}?`;
}

//	Prepares the deleteAddress delete modal from the clientAccount page.
function confirmDeleteAddress(e){
	var name=e.parentElement.parentElement.children[0].innerText;
	get("deleteAlertTarget").value=e.dataset["id"];
	get("deleteAlertOrigin").value="clientAccount";
	get("deleteAlertConfirm").value="Eliminar";
	get("deleteAlertMessage").innerText=`¿Eliminar dirección ${name}?`;
}

//	Prepares the confirmSale confirm modal from the clientSales page.
function confirmSaleReception(e){
	var id=e.dataset["id"];
	get("saleAlertAction").value="reception";
	get("saleAlertTarget").value=e.dataset["id"];
	get("saleAlertMessage").innerText=`¿Confirmar que la compra de código ${id} fue entregada?`;
}

//	Prepares the confirmShipment confirm modal from the adminSales page.
function confirmSaleShipment(e){
	var id=e.dataset["id"];
	get("saleAlertAction").value="shipment";
	get("saleAlertTarget").value=e.dataset["id"];
	get("saleAlertMessage").innerText=`¿Confirmar que la compra de código ${id} fue enviada?`;
}