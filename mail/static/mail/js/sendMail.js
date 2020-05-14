var x = (function()
{
	var userID, draftButton, subjectField, bodyField, attachmentField,resultBox;

	function getDraftURL(){
		return '/mail/saveDraft';
	}

	function sendRequest(){
		var form = document.querySelector('form');
		var formData = new FormData(form);
		console.log(form);
		console.log(formData);

		$.ajax({
			url : getDraftURL(),
			type : 'POST',
			data : formData,
			dataType : 'JSON',
			contentType: false,
			processData: false,
			success : displayMessage,
			error : function(error){ console.log(error); }
		});
	}

	function displayMessage(data){
		resultBox.innerHTML = data.response;
		resultBox.style.display = 'block';
	}

	function init(obj){
		var form = document.querySelectorAll('form > p > input');
		subjectField = form[1];
		bodyField = form[2];
		attachmentField = form[3];

		userID = obj.userID;
		draftButton = document.getElementById(obj.draft);
		resultBox = document.getElementById(obj.replyMessage);
		draftButton.addEventListener('click', sendRequest);
	}

	return {
		init : init,
	};


})();