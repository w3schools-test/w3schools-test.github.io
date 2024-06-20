(function() {
	const mergeConflict = document.getElementById("mergeConflict");
	const btn2 = document.getElementById("btn2");
	btn2.addEventListener("click", function() {
		mergeConflict.style.border = "5px solid red";
	});	
})();

$(document).ready(function(){
//
$("#btn1").click(function() {
	$(this).siblings("p").css({"color":"red"})
});
//
});