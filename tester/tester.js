window.onload=()=>{
	let initForm = document.querySelector("#initForm");
	let initTarget = document.querySelector("#initTarget");
	initForm.onsubmit=()=>{
		let iframe = document.createElement("iframe");
		iframe.id="targetFrame"
		iframe.src=initTarget.value;
		document.body.appendChild(iframe)
	}
}