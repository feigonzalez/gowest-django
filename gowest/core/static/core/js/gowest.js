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
	Builds a <div> element containing the category title, and a number of products from that category.
	The built <div> element is then appended to the element passed as e.
	If link is set to true, the category title will be a link that redirects to the corresponding
	category page, and will also show the total number of products from that category.
*/
async function loadCategoryGalleryInto(cat="",e,link=false){
	var cn = (await selectAllWhere("categories",(i)=>{return i["code"]==cat}))[0]["name"]
	var c = await selectAllWhere("products",(i)=>{return i["category"]==cat});
    //var c=json["categories"][cat];
    var cl=c.length //category length
    r="<div class='row bg-gowest categoryTitle'>"+
        (link?"<a href='#' onclick='moveTo(\"category.html\",[[\"c\",\""+cat+"\"]])'>":"")+
        cn+
        (link?" <span class='productCount'>Ver "+cl+" productos</span></a>":"")+"</div>";
    var template=
        "<div class='galleryItem'>"+
		"<a class='galleryItemLink' href='#' onclick='moveTo(\"product.html\",[[\"p\",\"{ID}\"]])'>"+
        "<img class='galleryItemImage mx-auto d-block' src='img/products/{ID}.png'>"+
        "<div class='galleryItemLabel'>{CONTENT}</div>"+
        "<div class='galleryItemPrice'>{PRICE}</div></a>"+
		"<button class='btn btn-success galleryCartBtn' onclick='addToCart(1)'>Añadir al carrito</button></div>";
    for(var i=0;i<(link?1:Math.ceil(cl/4));i++){
        r+="<div class='row galleryRow'>";
        for(var j=0;j<4;j++){
            index=i*4+j;
            content="";
            if(index<cl){
                item=c[index]
                content=template;
                content=content.replaceAll("{ID}",item["code"])
                content=content.replaceAll("{CONTENT}",item["name"])
                content=content.replaceAll("{PRICE}","$"+item["price"])
            }
            r+="<div class='col-sm-3'>"+content+"</div>";
        }
        r+="</div>";
    }
    e.innerHTML=r;
}

/*
	Queries the database to obtain a user's security question, and fills the
	form in recoverPass.html. The user is determined from the passed element's value.
*/
async function loadSecQuestion(e){
	makeValid(get("f_inputRut"))
	if(get("f_inputRut").value.trim().match(/^\d{1,3}(\.\d\d\d)*\-[0-9K]$/)==null){
		makeInvalid(get("f_inputRut"),"Formato incorrecto (Ingrese con puntos y guión).")
		return;
	}
	var secQ = (await fetch('/api/getUserSQ/'+get("f_inputRut").value).then(response=>response.json()));
	if(secQ){
		get("secQuestionHolder").innerText=secQ;
		//get("f_rut").value=user["rut"];
		makeValid(get("f_inputRut"))
	} else {
		get("secQuestionHolder").innerText="–";
		//get("f_rut").value="";
		makeInvalid(get("f_inputRut"),"RUT no encontrado");
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
		newTotal+=parseInt(row.children[3].innerText.substring(1));
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

async function removeItemFromCart(e){
	list=e.parentElement.parentElement.parentElement;
	id=e.dataset["id"]
	await fetch("/api/removeFromCart/"+id);
	e.parentElement.parentElement.remove();
	newTotal=0;
	for(row of list.children){
		if(row.children[3].id=="cartTotal")break;
		newTotal+=parseInt(row.children[3].innerText.substring(1));
	}
	get("cartTotal").innerText="$"+newTotal;
	updateCartBadge()
}

window.addEventListener("load",()=>{
})