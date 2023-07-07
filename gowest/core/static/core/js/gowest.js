/*
    Código para ser usado en el proyecto GOWEST, del curso de Programación Web 2023-1
*/

/*
	Utilities
*/

//	get(id) returns the HTML element with the given id, or null if no such element exists.
function get(id){return document.getElementById(id)}

/*
	Site-specific methods
*/

/*
	Queries the database to obtain a user's security question, and fills the
	form in recoverPass.html. The user is determined from the passed element's value.
*/
async function loadSecQuestion(e){
	makeValid(e)
	if(!isValidEmail(get("f_inputMail").value.trim())){
		makeInvalid(get("f_inputMail"),"Correo inválido.")
		return;
	}
	var secQ = (await fetch('/api/getUserSQ/'+get("f_inputMail").value).then(response=>response.json()));
	if(secQ){
		get("secQuestionHolder").innerText=secQ;
		makeValid(get("f_inputMail"))
	} else {
		get("secQuestionHolder").innerText="–";
		makeInvalid(get("f_inputMail"),"Usuario no encontrado");
	}
}

/*
	Adds a badge to the navbar cart button, or replaces its value, according to the number
	of units specified.
	If units is undefined, it is assumed to be called from the product page "Add to Cart" button.
*/
async function addToCart(pID,units){
	if(units==null){
		units = parseInt(get("addToCartUnits").value);
		if(units<1)return;
	}
	await fetch("/api/addToCart?"+ new URLSearchParams({"pID":pID,"amount":units}))
	updateCartBadge()
}

//	Returns a <span> badge element that corresponds to the passed sale status, if valid.
function formatSaleStatus(status){
	switch(status){
		case "Carrito": return `<span class='badge badge-pill badge-secondary badge-saleStatus'>${status}</span>`;
		case "Pagada": return `<span class='badge badge-pill badge-danger badge-saleStatus'>${status}</span>`;
		case "Despachada": return `<span class='badge badge-pill badge-primary badge-saleStatus'>${status}</span>`;
		case "Completada": return `<span class='badge badge-pill badge-success badge-saleStatus'>${status}</span>`;
		default: return status;
	}
}

async function updateCartTotals(e){
	validateCheckoutItemCount(e)
	var price=parseInt(e.parentElement.parentElement.children[1].innerText.substring(1));
	var se=e.parentElement.parentElement.children[3];
	se.innerText="$"+price*e.value;
	var newTotal=0;
	for(row of e.parentElement.parentElement.parentElement.children){
		if(row.children[3].id=="cartTotal")break;
		if(row.children[3].id=="foundationDiscountTotal")break;
		newTotal+=parseInt(row.children[3].innerText.substring(1));
	}
	updateFoundationDiscount(newTotal)
	if(get("foundationDiscountTotal")!=null){
		newTotal=Math.floor(newTotal*0.9)
	}
	get("cartTotal").innerText="$"+newTotal;
	await fetch("/api/setToCart?"+ new URLSearchParams({"pID":e.parentElement.parentElement.dataset["pid"],"amount":e.value}))
	updateCartBadge()
}

async function updateCartBadge(){
	var newUnits=(await fetch("/api/getCartItemAmount").then(response=>response.json()))
	var cartBadge=get("navbarCartUnits");
	cartBadge.classList.remove("hidden");
	cartBadge.innerText=newUnits;
	var cartBtn = get("navbarCartBtn");
	if(cartBtn==null) return;
	cartBtn.dataset["units"]=newUnits;
}

function updateFoundationDiscount(total){
	dCell=get("foundationDiscountTotal")
	if(dCell == null)
		return
	dCell.innerText="$"+Math.floor(total*-0.1)
}

async function removeItemFromCart(e){
	list=e.parentElement.parentElement.parentElement;
	id=e.dataset["id"]
	newTotal=(await fetch("/api/removeFromCart/"+id).then(r=>r.json()));
	e.parentElement.parentElement.remove();
	get("cartTotal").innerText="$"+newTotal;
	updateCartBadge()
	updateFoundationDiscount(newTotal)
}

//original provided by Cedric Ipkiss, in https://stackoverflow.com/questions/5802580/html-input-type-file-get-the-image-before-submitting-the-form
function previewUploadProductImage() {
	var preview = get("productFormImagePreview");
	var file = get("productFormImage").files[0];
	var reader = new FileReader();

	reader.onloadend = function () {
		preview.src = reader.result;
	}

	if (file) {
		reader.readAsDataURL(file);
	} else {
		preview.src = "";
	}
}

window.addEventListener("load",()=>{
	for(e of document.querySelectorAll(".saleStatus")){
		e.innerHTML=formatSaleStatus(e.innerText)
	}
})