var x = (function()
{
	var button, id;

	function sendRequest(event){
		event.preventDefault();
		button = document.getElementById(id);

		$.ajax({
			url : '/mail/downloadImage',
			type : 'GET',
			data : {'address' : button.getAttribute('address')},
			success : function(data){ alert("Attachment has been saved at the following location :-\n\n\n" + data.response + '\n\n'); },
			error : function(error){ alert("Can't download this attachment, sorry !!!"); }
		});
	}

	function init(obj){
		id = obj.download;
		button = document.getElementById(obj.download);

		if(button)
			button.addEventListener('click', sendRequest);
	}	

	return {
		init : init,
	};
})();